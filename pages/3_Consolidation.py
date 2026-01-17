import streamlit as st
import pandas as pd
from pathlib import Path
import subprocess
import sys
import pandas as pd

st.set_page_config(page_title="Consolidation", page_icon="🛠️")

st.title("🛠️ Étape 3 : Consolidation des Données")
st.write("Cette page fusionne les données brutes extraites avec les données enrichies pour créer le jeu de données final.")

RAW_INPUT_FILE = Path("data") / "raw_bulletins.csv"
ENRICHED_INPUT_FILE = Path("enriched_cves.csv")
CONSOLIDATED_OUTPUT_FILE = Path("consolidated_data.csv")

if not RAW_INPUT_FILE.exists() or not ENRICHED_INPUT_FILE.exists():
    st.warning(f"Un ou plusieurs fichiers sont manquants. Assurez-vous que l'**Extraction** (`{RAW_INPUT_FILE}`) et l'**Enrichissement** (`{ENRICHED_INPUT_FILE}`) ont été exécutés.")
else:
    if st.button("Lancer la consolidation", type="primary"):
        try:
            with st.spinner("Consolidation en cours... Exécution du script `consolidation.py`."):
                # Execute the script as a separate process
                python_executable = sys.executable
                result = subprocess.run(
                    [python_executable, "consolidation.py"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                st.text_area("Log de l'exécution", result.stdout, height=200)

            st.success(f"Consolidation terminée ! Fichier sauvegardé dans `{CONSOLIDATED_OUTPUT_FILE}`.")
            
            if CONSOLIDATED_OUTPUT_FILE.exists():
                df_consolidated = pd.read_csv(CONSOLIDATED_OUTPUT_FILE)
                st.write("### Aperçu des données consolidées")
                st.dataframe(df_consolidated)

                st.download_button(
                    label="Télécharger les données consolidées (CSV)",
                    data=df_consolidated.to_csv(index=False).encode('utf-8'),
                    file_name='consolidated_data.csv',
                    mime='text/csv',
                )
            else:
                st.error("Le fichier de sortie n'a pas été créé. Vérifiez le log ci-dessus.")

        except subprocess.CalledProcessError as e:
            st.error(f"Une erreur est survenue lors de l'exécution de `consolidation.py`:")
            st.text_area("Erreur", e.stderr, height=200)
        except Exception as e:
            st.error(f"Une erreur inattendue est survenue : {e}")

st.markdown("---")
st.write("L'étape suivante est l'**Analyse & Visualisation**.")
