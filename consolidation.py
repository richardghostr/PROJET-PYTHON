import pandas as pd

# Récupérer les données des bulletins
def consolidate_data(bulletins, enriched_df):

    # Créer un dictionnaire pour un accès rapide aux données enrichies
    enriched_dict = {row['cve_id']: row for _, row in enriched_df.iterrows()}

    # Créer une liste pour les données consolidées
    consolidated_data = []

    # Pour chaque bulletin, pour chaque CVE, créer une ligne
    for bulletin in bulletins:
        titre = bulletin['titre']
        type_bulletin = bulletin['type']
        date = bulletin['date']
        lien = bulletin['lien']
        
        for cve_id in bulletin['cves']:
            # Trouver les données enrichies pour ce CVE
            enriched_row = enriched_dict.get(cve_id)
            if enriched_row is not None:
                consolidated_data.append({
                    'Titre du bulletin (ANSSI)': titre,
                    'Type de bulletin': type_bulletin,
                    'Date de publication': date,
                    'Identifiant CVE': cve_id,
                    'Score CVSS': enriched_row['cvss_score'],
                    'Level CVSS': enriched_row['cvss_level'],
                    'Base Severity': 'Non disponible',  # À calculer si besoin (ex. basé sur CVSS)
                    'Type CWE': enriched_row['cwe'],
                    'Score EPSS': enriched_row['epss_score'],
                    'Lien du bulletin (ANSSI)': lien,
                    'Description': enriched_row['description'],
                    'Éditeur/Vendor': 'Non disponible',  # Pas extrait dans l'enrichissement actuel
                    'Produit': 'Non disponible',
                    'Versions affectées': 'Non disponible'
                })

    # Créer le DataFrame consolidé
    df_consolidated = pd.DataFrame(consolidated_data)

    # Sauvegarder en CSV
    df_consolidated.to_csv('consolidated_data.csv', index=False)
    print("Données consolidées sauvegardées dans consolidated_data.csv")
    print(df_consolidated.head())  # Aperçu des premières lignes