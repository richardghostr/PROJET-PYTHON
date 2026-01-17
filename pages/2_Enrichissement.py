import streamlit as st
import pandas as pd
from pathlib import Path
from enrichissement import enrich_cves

st.set_page_config(page_title="Enrichissement", page_icon="✨")

st.title("✨ Étape 2 : Enrichissement des Données CVE")
st.write("Cette page enrichit les identifiants CVE avec des données provenant d'API externes (MITRE, EPSS).")

RAW_INPUT_FILE = Path("data") / "raw_bulletins.csv"
ENRICHED_OUTPUT_FILE = Path("enriched_cves.csv")

if not RAW_INPUT_FILE.exists():
    st.warning(f"Le fichier de données brutes `{RAW_INPUT_FILE}` est introuvable. Veuillez d'abord exécuter l'étape d'**Extraction**.")
else:
    st.info("Cette opération peut prendre du temps en raison des appels aux API externes.")
    
    # Extract unique CVEs from the raw bulletins file
    try:
        df_raw = pd.read_csv(RAW_INPUT_FILE)
        all_cves = set()
        # The 'cves' column is a string representation of a list, e.g., "['CVE-2023-1234']"
        import ast
        cve_series = df_raw['cves'].dropna().apply(ast.literal_eval)
        for cve_list in cve_series:
            all_cves.update(cve_list)
        unique_cves = sorted(list(all_cves))
    except Exception as e:
        st.error(f"Erreur lors de la lecture des CVEs depuis `{RAW_INPUT_FILE}`: {e}")
        unique_cves = []
        st.stop()
    
    st.write(f"**{len(unique_cves)}** CVEs uniques trouvées dans les données brutes.")

    if st.button("Lancer l'enrichissement", type="primary"):
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            with st.spinner("Enrichissement en cours... Cela peut prendre plusieurs minutes."):
                enriched_data = enrich_cves(unique_cves)

            st.success(f"Enrichissement terminé ! {len(enriched_data)} CVEs traitées.")
            
            df_enriched = pd.DataFrame(enriched_data)
            df_enriched.to_csv(ENRICHED_OUTPUT_FILE, index=False)
            
            st.write("### Aperçu des données enrichies")
            st.dataframe(df_enriched)

            st.download_button(
                label="Télécharger les données enrichies (CSV)",
                data=df_enriched.to_csv(index=False).encode('utf-8'),
                file_name='enriched_cves.csv',
                mime='text/csv',
            )

        except Exception as e:
            st.error(f"Une erreur est survenue lors de l'enrichissement : {e}")

st.markdown("---")
st.write("L'étape suivante est la **Consolidation**.")
