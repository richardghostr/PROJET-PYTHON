from extract import extraction_complete
from enrichissement import enrich_cves
from alertes import check_for_alerts
from consolidation import consolidate_data
import pandas as pd
import os
from dotenv import load_dotenv


def main():
    bulletins = extraction_complete()
    print(f"\nTotal bulletins récupérés : {len(bulletins)}")

    all_cve = set()
    for bulletin in bulletins:
        all_cve.update(bulletin['cves'])

    print(f"Total CVE uniques trouvés : {len(all_cve)}")

  
    LIMIT = 15
    cve_to_process = list(all_cve)[:LIMIT] if LIMIT > 0 else list(all_cve)

    print(f"CVEs à enrichir : {len(cve_to_process)}")
    print("\nDébut de l'enrichissement...\n")
    enriched_data = enrich_cves(cve_to_process)
    print("\n" + "="*60)
    print("RÉSUMÉ")
    print("="*60)
    total = len(enriched_data)
    with_cvss = sum(1 for item in enriched_data if item["cvss_score"] != "Non disponible")
    with_cwe = sum(1 for item in enriched_data if item["cwe"] != "Non disponible")
    with_epss = sum(1 for item in enriched_data if item["epss_score"] != "Non disponible")
    with_desc = sum(1 for item in enriched_data if item["description"] not in ["Non disponible", "CVE non publiée"])
    print(f"CVEs enrichies      : {total}")
    print(f"Descriptions        : {with_desc}/{total} ({with_desc*100//total if total else 0}%)")
    print(f"CVSS scores         : {with_cvss}/{total} ({with_cvss*100//total if total else 0}%)")
    print(f"CWE                 : {with_cwe}/{total} ({with_cwe*100//total if total else 0}%)")
    print(f"EPSS scores         : {with_epss}/{total} ({with_epss*100//total if total else 0}%)")
    print("="*60 + "\n")

    # Créer DataFrame enrichi
    enriched_df = pd.DataFrame(enriched_data)

    # Exporter en CSV pour référence
    enriched_df.to_csv('enriched_cves.csv', index=False)
    print("Données enrichies exportées dans enriched_cves.csv")

    # Consolidation
    consolidate_data(bulletins, enriched_df)

    # Envoi d'alertes
    load_dotenv()
    FROM_EMAIL = os.getenv("GMAIL_USER")
    PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # Utiliser un mot de passe d'application pour Gmail
    TO_EMAIL = "ESILV@gmail.com"  # Remplacer par l'email du destinataire

    check_for_alerts(FROM_EMAIL, PASSWORD, TO_EMAIL)


if __name__ == "__main__":
    main()