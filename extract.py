import warnings
import feedparser
import requests
import re
import time
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+")

# Constantes
URL_AVIS = "https://www.cert.ssi.gouv.fr/avis/feed/"
URL_ALERTES = "https://www.cert.ssi.gouv.fr/alerte/feed/"
CVE_PATTERN = r"CVE-\d{4}-\d{4,7}"

def extract_rss(url, bulletin_type):
    rss_feed = feedparser.parse(url)
    results = []
    for entry in rss_feed.entries:
        bulletin = {
            "titre": entry.title,
            "date": entry.published,
            "lien": entry.link,
            "type": bulletin_type,
            "cves": [] 
        }
        results.append(bulletin)
    return results

def get_json_url(url):
    return url.rstrip("/") + "/json/"

def extract_cves(json_url):
    try:
        response = requests.get(json_url, timeout=10) 
        if response.status_code != 200:
            return []
            
        data = response.json()
        found_cves = set()

        # Méthode 1 : Clé Dictionnaire 
        if "cves" in data:
            for item in data["cves"]:
                if isinstance(item, dict) and "name" in item:
                    found_cves.add(item["name"])

        # Méthode 2 : Regex brute sur tout le contenu 
        found_cves.update(re.findall(CVE_PATTERN, str(data)))
        
        return list(found_cves)

    except Exception as e:
        print(f"Erreur sur {json_url}: {e}")
        return []

def extraction_complete():
    print("1. Récupération des flux RSS...")
    avis = extract_rss(URL_AVIS, "Avis")
    alertes = extract_rss(URL_ALERTES, "Alerte")
    tous_bulletins = avis + alertes

    print(f"2. Analyse de {len(tous_bulletins)} bulletins en cours...")
    
    
    for bulletin in tous_bulletins[35:45]: 
        json_link = get_json_url(bulletin["lien"])
        
        cves_trouves = extract_cves(json_link)
        bulletin["cves"] = cves_trouves 
        
        print(f"[{bulletin['type']}] {len(cves_trouves)} CVEs trouvés dans {bulletin['titre'][:30]}...")
        
        # Pause obligatoire 
        time.sleep(2)

    return tous_bulletins

if __name__ == "__main__":
    resultats = extraction_complete()
    
