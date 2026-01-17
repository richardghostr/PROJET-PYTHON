import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd


def send_alert_email(subject, body, to_email, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email envoyé avec succès")
    except Exception as e:
        print(f"Échec de l'envoi de l'email: {e}")


def check_for_alerts(from_email, password, to_email):
    try:
        df = pd.read_csv('consolidated_data.csv')
    except FileNotFoundError:
        print("Fichier consolidated_data.csv non trouvé. Veuillez exécuter la consolidation d'abord.")
        return

    if df.empty:
        subject = "Rapport des bulletins de sécurité ANSSI"
        body = "Aucun bulletin dans consolidated_data.csv"
        send_alert_email(subject, body, to_email, from_email, password)
        return

    # Normaliser et sécuriser l'accès aux colonnes attendues
    if 'Date de publication' in df.columns:
        df['Date de publication'] = pd.to_datetime(df['Date de publication'], errors='coerce', utc=True)

    # Filtrer les CVEs critiques (Score EPSS > 0.5) si la colonne existe
    if 'Score EPSS' in df.columns:
        df['Score EPSS'] = pd.to_numeric(df['Score EPSS'], errors='coerce')
        critical_cves = df[df['Score EPSS'] > 0.5]
    else:
        critical_cves = pd.DataFrame()

    if not critical_cves.empty:
        subject = "Alerte: CVEs critiques détectées"
        cols = [c for c in ['Titre du bulletin (ANSSI)', 'Identifiant CVE', 'Score EPSS'] if c in critical_cves.columns]
        body = f"Nombre total de bulletins: {len(df)}\nNombre de CVEs critiques: {len(critical_cves)}\n\nDétails:\n{critical_cves[cols].to_string(index=False)}"
    else:
        subject = "Rapport: Bulletins ANSSI"
        cols = [c for c in ['Titre du bulletin (ANSSI)', 'Date de publication', 'Type de bulletin'] if c in df.columns]
        body = f"Nombre total de bulletins: {len(df)}\n\nAperçu:\n{df[cols].to_string(index=False)}"

    send_alert_email(subject, body, to_email, from_email, password)

