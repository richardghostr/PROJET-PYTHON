import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Projet-Python | Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Dashboard d'Analyse de Vulnérabilités")
st.markdown("---")

st.sidebar.success("Sélectionnez une page d'analyse ci-dessus.")

st.header("Bienvenue sur le tableau de bord du projet")
st.write("""
Ce dashboard est l'interface centrale pour piloter l'ensemble du projet d'analyse de vulnérabilités. 
Utilisez le menu sur la gauche pour naviguer entre les différentes étapes :

- **TABLEAU DE BORD**: Cette page d'accueil.
- **1 Extraction**: Pour lancer la collecte des données depuis les flux RSS du CERT-FR.
- **2 Enrichissement**: Pour augmenter les données CVE avec des informations de contexte (CVSS, EPSS, etc.).
- **3 Consolidation**: Pour traiter et unifier les données brutes collectées.
- **4 Analyse et Visualisation**: Pour explorer interactivement les données finales.
- **5 Alertes**: Pour configurer et envoyer des rapports par email.


                  
Chaque page vous guidera à travers les actions nécessaires.
""")

st.info("Le projet est structuré pour suivre un pipeline de données, de la collecte à la visualisation. Assurez-vous d'exécuter les étapes dans l'ordre pour garantir que les données sont disponibles pour l'étape suivante.", icon="ℹ️")

# Create necessary directories if they don't exist
Path("processed").mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True) # Assuming you might save raw data here
Path("figures").mkdir(exist_ok=True)

st.markdown("---")
st.write("Prêt à commencer ? Sélectionnez une page dans le menu latéral.")

st.markdown("---")
st.header("Automatisation du Pipeline")
st.write("Exécutez l'ensemble du pipeline de données, de l'extraction à la consolidation, en un seul clic.")

if st.button("🚀 Lancer le Pipeline Complet", type="primary"):
    import subprocess
    import sys
    import time
    import pandas as pd

    scripts_and_files = {
        "Étape 1: Extraction": ("extract.py", "data/raw_bulletins.csv"),
        "Étape 2: Enrichissement": ("enrichissement.py", "enriched_cves.csv"),
        "Étape 3: Consolidation": ("consolidation.py", "consolidated_data.csv")
    }

    with st.status("🚀 Lancement du pipeline...", expanded=True) as status:
        all_success = True
        for step_title, (script_name, output_file) in scripts_and_files.items():
            st.write(f"Exécution de **{step_title}** (`{script_name}`)...")
            python_executable = sys.executable
            try:
                process = subprocess.run(
                    [python_executable, script_name],
                    capture_output=True, text=True, check=True, encoding='utf-8'
                )
                # Afficher les logs dans un expander
                with st.expander(f"Log de {step_title}"):
                    st.code(process.stdout if process.stdout else "Aucune sortie standard.")

                # Afficher un aperçu des données
                st.write(f"Aperçu des données générées par **{step_title}** (`{output_file}`):")
                try:
                    df = pd.read_csv(output_file)
                    st.dataframe(df.head())
                except FileNotFoundError:
                    st.warning(f"Le fichier de sortie `{output_file}` n'a pas été trouvé. L'aperçu ne peut être affiché.")
                except Exception as e:
                    st.error(f"Erreur lors de la lecture du fichier `{output_file}`: {e}")
                
                time.sleep(1) # Pause pour l'UX

            except subprocess.CalledProcessError as e:
                st.error(f"Échec de **{step_title}**.")
                with st.expander(f"Détails de l'erreur pour {step_title}", expanded=True):
                    st.code(e.stderr)
                all_success = False
                break # Arrêter le pipeline en cas d'erreur
            except FileNotFoundError:
                st.error(f"Le script `{script_name}` est introuvable.")
                all_success = False
                break
        
        if all_success:
            status.update(label="🎉 Pipeline Terminé !", state="complete", expanded=False)
        else:
            status.update(label="❌ Échec du Pipeline", state="error", expanded=True)

    if all_success:
        st.balloons()
        st.success("Toutes les étapes ont été exécutées avec succès !")
        
        st.markdown("---")
        st.info("Le pipeline a terminé. Choisissez votre prochaine étape :", icon="🎉")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <a href="/Analyse_et_Visualisation" target="_self" style="
                display: inline-block;
                padding: 0.75rem 1.25rem;
                border-radius: 0.5rem;
                background-color: #1976D2;
                color: white;
                text-decoration: none;
                font-weight: bold;
                font-size: 1.1rem;
                text-align: center;
                width: 100%;
                box-sizing: border-box;
            ">
                📊 Explorer les Données
            </a>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <a href="/Alertes" target="_self" style="
                display: inline-block;
                padding: 0.75rem 1.25rem;
                border-radius: 0.5rem;
                background-color: #FF9800;
                color: white;
                text-decoration: none;
                font-weight: bold;
                font-size: 1.1rem;
                text-align: center;
                width: 100%;
                box-sizing: border-box;
            ">
                🔔 Envoyer un Rapport
            </a>
            """, unsafe_allow_html=True)
