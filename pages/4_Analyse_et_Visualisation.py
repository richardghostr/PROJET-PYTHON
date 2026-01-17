import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Analyse & Visualisation", page_icon="📈")

st.title("📈 Étape 4 : Analyse & Visualisation")
st.write("Explorez les données consolidées et enrichies à travers des visualisations interactives.")

# --- Data Loading ---
@st.cache_data
def load_data(file_path):
    if not file_path.exists():
        st.warning(f"Fichier de données introuvable : `{file_path}`. Veuillez exécuter les étapes précédentes.")
        return None
    return pd.read_csv(file_path)

CONSOLIDATED_FILE = Path("consolidated_data.csv")
ENRICHED_FILE = Path("enriched_cves.csv")

df_consolidated = load_data(CONSOLIDATED_FILE)
df_enriched = load_data(ENRICHED_FILE)

if df_consolidated is None or df_enriched is None:
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("Filtres Globaux")

# Date range filter for consolidated data
if 'Date de publication' in df_consolidated.columns:
    df_consolidated['Date de publication'] = pd.to_datetime(df_consolidated['Date de publication'], errors='coerce')
    min_date, max_date = df_consolidated['Date de publication'].min(), df_consolidated['Date de publication'].max()
    
    date_range = st.sidebar.slider(
        "Filtrer par date de publication",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        format="DD/MM/YYYY"
    )
    
    # Apply date filter
    df_consolidated = df_consolidated[
        (df_consolidated['Date de publication'] >= pd.to_datetime(date_range[0])) &
        (df_consolidated['Date de publication'] <= pd.to_datetime(date_range[1]))
    ]

# CVSS Level filter for enriched data
if 'cvss_level' in df_enriched.columns:
    levels = ['Critique', 'Élevée', 'Moyenne', 'Faible', 'Non disponible']
    selected_levels = st.sidebar.multiselect(
        "Filtrer par niveau CVSS",
        options=levels,
        default=levels
    )
    df_enriched = df_enriched[df_enriched['cvss_level'].isin(selected_levels)]


# --- Main Page Layout ---
st.header("Analyse des Données Enrichies")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Répartition par Niveau CVSS")
    if 'cvss_level' in df_enriched.columns:
        level_counts = df_enriched['cvss_level'].value_counts().reindex(['Critique', 'Élevée', 'Moyenne', 'Faible']).fillna(0)
        fig = px.bar(level_counts, y=level_counts.values, x=level_counts.index,
                     title="Nombre de CVEs par Niveau de Criticité",
                     labels={'y': 'Nombre de CVEs', 'x': 'Niveau CVSS'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top 10 des Types de Failles (CWE)")
    if 'cwe' in df_enriched.columns:
        cwe_counts = df_enriched['cwe'].value_counts().nlargest(10)
        fig = px.pie(cwe_counts, values=cwe_counts.values, names=cwe_counts.index,
                     title="Top 10 des CWEs les plus fréquents")
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Corrélation entre Criticité (CVSS) et Probabilité d'Exploitation (EPSS)")
if 'cvss_score' in df_enriched.columns and 'epss_score' in df_enriched.columns:
    # Ensure scores are numeric for plotting
    df_enriched['cvss_score'] = pd.to_numeric(df_enriched['cvss_score'], errors='coerce')
    df_enriched['epss_score'] = pd.to_numeric(df_enriched['epss_score'], errors='coerce')
    
    fig = px.scatter(
        df_enriched.dropna(subset=['cvss_score', 'epss_score']),
        x="cvss_score",
        y="epss_score",
        color="cvss_level",
        color_discrete_map={
            'Critique': '#d62728', 'Élevée': '#ff7f0e',
            'Moyenne': '#ffbb78', 'Faible': '#1f77b4'
        },
        hover_data=['cve_id'],
        title="CVSS vs. EPSS"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.header("Analyse des Bulletins (Données Consolidées)")
st.subheader("Évolution temporelle des publications")
if 'Date de publication' in df_consolidated.columns:
    vulns_per_day = df_consolidated.set_index('Date de publication').resample('D').size().rename("Nombre de bulletins")
    fig = px.line(vulns_per_day, title="Nombre de bulletins publiés par jour")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Aperçu des données filtrées")
st.write("Données consolidées :")
st.dataframe(df_consolidated)
st.write("Données enrichies :")
st.dataframe(df_enriched)

st.markdown("---")
st.header("Analyses Approfondies")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Distribution des Scores EPSS")
    if 'epss_score' in df_enriched.columns:
        fig = px.histogram(df_enriched, x="epss_score", nbins=20,
                           title="Distribution de la Probabilité d'Exploitation (EPSS)")
        st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Scores CVSS par Type de Faille (Top 5 CWE)")
    if 'cwe' in df_enriched.columns and 'cvss_score' in df_enriched.columns:
        top_5_cwe = df_enriched['cwe'].value_counts().nlargest(5).index
        df_top_cwe = df_enriched[df_enriched['cwe'].isin(top_5_cwe)]
        fig = px.box(df_top_cwe, x='cwe', y='cvss_score',
                     title="Distribution des Scores CVSS pour le Top 5 des CWEs",
                     labels={'cwe': 'Type de Faille (CWE)', 'cvss_score': 'Score CVSS'})
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Publications par Type et par Mois")
if 'Date de publication' in df_consolidated.columns and 'Type de bulletin' in df_consolidated.columns:
    df_monthly = df_consolidated.copy()
    df_monthly['Mois'] = df_monthly['Date de publication'].dt.to_period('M').astype(str)
    monthly_counts = df_monthly.groupby(['Mois', 'Type de bulletin']).size().reset_index(name='Nombre')
    fig = px.bar(monthly_counts, x='Mois', y='Nombre', color='Type de bulletin',
                 title="Nombre de Bulletins Publiés par Mois et par Type",
                 barmode='stack')
    st.plotly_chart(fig, use_container_width=True)
