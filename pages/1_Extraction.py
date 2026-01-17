import streamlit as st
import pandas as pd
from pathlib import Path
from extract import extraction_complete

st.set_page_config(page_title="Extraction", page_icon="📡")

st.title("📡 Étape 1 : Extraction des Données")
st.write("Cette page permet de lancer l'extraction des données depuis les flux RSS du CERT-FR (Avis et Alertes).")

# Check for existing data
RAW_OUTPUT_FILE = Path("data") / "raw_bulletins.csv"
if RAW_OUTPUT_FILE.exists():
    st.info(f"Un fichier de données brutes (`{RAW_OUTPUT_FILE}`) existe déjà. L'exécution va l'écraser.")

if st.button("Lancer l'extraction", type="primary"):
    try:
        with st.spinner("Extraction en cours... Connexion aux flux RSS..."):
            # This calls the main function from your script
            bulletins = extraction_complete()
        
        st.success(f"Extraction terminée ! {len(bulletins)} bulletins récupérés.")
        
        # Convert to DataFrame and save
        df = pd.DataFrame(bulletins)
        df.to_csv(RAW_OUTPUT_FILE, index=False)
        
        st.write("### Aperçu des données extraites")
        st.dataframe(df)
        
        st.download_button(
            label="Télécharger les données brutes (CSV)",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='raw_bulletins.csv',
            mime='text/csv',
        )
        
    except Exception as e:
        st.error(f"Une erreur est survenue lors de l'extraction : {e}")

st.markdown("---")
st.write("L'étape suivante est la **Consolidation**.")
