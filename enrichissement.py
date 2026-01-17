import requests
import time 


def _to_float(value):
    try:
        return float(value)
    except Exception:
        return None


def _cvss_level(score):
    if score is None:
        return "Non disponible"
    if score <= 3:
        return "Faible"
    if score <= 6:
        return "Moyenne"
    if score <= 8:
        return "Élevée"
    return "Critique"

def enrich_cves(cve_list):
    results = []
    total_cves = len(cve_list)
    
    for idx, cve_id in enumerate(cve_list, 1):
        print(f"[{idx}/{total_cves}] Traitement de {cve_id}...")
        
        data = {
            "cve_id": cve_id,
            "description": "Non disponible",
            "cvss_score": "Non disponible",  # À quel point c’est grave ?
            "cwe": "Non disponible",          # Type de vulnérabilité
            "epss_score": "Non disponible"   # Probabilité d’exploitation
        }
        
        # API MITRE
        try:
            url = f"https://cveawg.mitre.org/api/cve/{cve_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                print(f"[MITRE] {cve_id} - Non trouvée (404)")
                data["description"] = "CVE non publiée"
            elif response.status_code != 200:
                print(f"[MITRE] {cve_id} - Erreur HTTP {response.status_code}")
            else:
                mitre_data = response.json()
                
                # Description
                try:
                    data["description"] = mitre_data["containers"]["cna"]["descriptions"][0]["value"]
                except (KeyError, IndexError):
                    print(f"[MITRE] {cve_id} - Description manquante")
                
                # CVSS
                cvss_found = False
                try:
                    if "metrics" in mitre_data["containers"]["cna"]:
                        metrics = mitre_data["containers"]["cna"]["metrics"]
                        for metric in metrics:
                            if "cvssV3_1" in metric:
                                data["cvss_score"] = metric["cvssV3_1"]["baseScore"]
                                cvss_found = True
                                break
                            elif "cvssV3_0" in metric:
                                data["cvss_score"] = metric["cvssV3_0"]["baseScore"]
                                cvss_found = True
                                break
                            elif "cvssV2_0" in metric:
                                data["cvss_score"] = metric["cvssV2_0"]["baseScore"]
                                cvss_found = True
                                break
                except (KeyError, IndexError, TypeError):
                    pass
                
                if not cvss_found:
                    data["cvss_score"] = "Non disponible"
                
                # CWE
                try:
                    data["cwe"] = mitre_data["containers"]["cna"]["problemTypes"][0]["descriptions"][0]["cweId"]
                except (KeyError, IndexError):
                    data["cwe"] = "Non disponible"
        
        except requests.exceptions.RequestException as e:
            print(f"[MITRE] {cve_id} - Erreur réseau: {type(e).__name__}")
        except Exception as e:
            print(f"[MITRE] {cve_id} - Erreur: {type(e).__name__}")

        time.sleep(1)     
        # API EPSS
        try:
            epss_url = f"https://api.first.org/data/v1/epss?cve={cve_id}"
            response = requests.get(epss_url, timeout=10)
            
            if response.status_code != 200:
                print(f"[EPSS] {cve_id} - Erreur HTTP {response.status_code}")
            else:
                epss_data = response.json()
                if epss_data.get("data") and len(epss_data["data"]) > 0:
                    data["epss_score"] = epss_data["data"][0]["epss"]
                else:
                    print(f"[EPSS] {cve_id} - Données vides")
        except requests.exceptions.RequestException as e:
            print(f"[EPSS] {cve_id} - Erreur réseau: {type(e).__name__}")
        except Exception as e:
            print(f"[EPSS] {cve_id} - Erreur: {type(e).__name__}")
        
        # Normaliser les types numériques et ajouter la classification CVSS
        numeric_cvss = _to_float(data.get("cvss_score"))
        data["cvss_score"] = numeric_cvss if numeric_cvss is not None else "Non disponible"
        data["cvss_level"] = _cvss_level(numeric_cvss)

        numeric_epss = _to_float(data.get("epss_score"))
        data["epss_score"] = numeric_epss if numeric_epss is not None else "Non disponible"

        results.append(data)
    
    return results

