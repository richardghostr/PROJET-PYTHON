import streamlit as st
from pathlib import Path
from alertes import check_for_alerts
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

st.set_page_config(page_title="Alertes", page_icon="🔔")

st.title("🔔 Gestion des Alertes par Email")
st.write("Envoyez des alertes par email basées sur les données de vulnérabilité.")

# --- Configuration Section ---
st.header("Configuration")

# Récupérer les identifiants depuis les variables d'environnement
FROM_EMAIL = os.getenv("GMAIL_USER")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

if not FROM_EMAIL or not PASSWORD:
    st.error(
        "Les variables d'environnement `GMAIL_USER` et `GMAIL_APP_PASSWORD` "
        "doivent être définies dans votre fichier `.env` à la racine du projet."
    )
    st.code("GMAIL_USER=votre_email@gmail.com\nGMAIL_APP_PASSWORD=votre_mot_de_passe_application", language="shell")
    st.stop()

st.success(f"L'email d'expédition est configuré sur : **{FROM_EMAIL}**.", icon="📧")
st.info("Cet email est lu depuis votre fichier `.env`. Le mot de passe d'application est également chargé depuis ce fichier.", icon="ℹ️")

# Utiliser st.session_state pour conserver l'email du destinataire
if 'to_email' not in st.session_state:
    st.session_state.to_email = "noe.wales@laposte.net" # Valeur par défaut

to_email = st.text_input("Email du destinataire", value=st.session_state.to_email)
st.session_state.to_email = to_email # Mettre à jour l'état de la session à chaque saisie

st.markdown("---")

# --- Alerting Section ---
st.header("Déclencher une Alerte")

# Vérifier si le fichier de données existe
CONSOLIDATED_FILE = Path("consolidated_data.csv")
if not CONSOLIDATED_FILE.exists():
    st.error(f"Le fichier `{CONSOLIDATED_FILE}` est introuvable. Veuillez exécuter les étapes de consolidation avant d'envoyer une alerte.")
else:
    st.info(f"Prêt à analyser `{CONSOLIDATED_FILE}` et à envoyer un rapport.")
    
    if st.button("Envoyer l'email d'alerte maintenant", type="primary"):
        if not st.session_state.to_email:
            st.error("Veuillez d'abord renseigner l'email du destinataire.")
        else:
            try:
                with st.spinner("Analyse des données et envoi de l'email..."):
                    # La fonction check_for_alerts de votre script sera appelée
                    # avec les identifiants du fichier .env.
                    check_for_alerts(
                        from_email=FROM_EMAIL,
                        password=PASSWORD,
                        to_email=st.session_state.to_email
                    )
                st.success(f"Email d'alerte envoyé avec succès à {st.session_state.to_email}!")
                st.balloons()
            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'envoi de l'alerte : {e}")

st.markdown("---")
st.write("Cette page utilise la logique du script `alertes.py` pour déterminer le contenu de l'email (rapport standard ou alerte critique si EPSS > 0.5).")
