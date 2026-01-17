# PROJET-PYTHON

Projet d'analyse et de visualisation de vulnérabilités (bulletins ANSSI + CVE enrichies).

## Aperçu
Ce dépôt contient un pipeline léger pour extraire, enrichir, consolider et visualiser des vulnérabilités (CVE) à partir des bulletins de sécurité ANSSI. Le but est de produire des jeux de données nettoyés et des visualisations exploitables pour l'analyse de risques.

## Structure du dépôt
- `extract.py` : extraction des bulletins/source
- `enrichissement.py` : enrichissement des CVE (scores CVSS, EPSS, méta-données)
- `consolidation.py` : consolidation des données en CSV unique
- `visualisation.ipynb` : notebook de visualisation (graphes interactifs)
- `test.py` : script de test / envoi d'email (Mailtrap)
- `alertes.py` : génération d'alertes (si présente)
- `consolidated_data.csv` : données consolidées (résultat attendu)
- `enriched_cves.csv` : CVE enrichies (résultat attendu)
- `requirements.txt` : dépendances Python
- `main.py` : execution globale du code 

## Prérequis
- Python 3.10+ recommandé
- Créer et activer un environnement virtuel (venv)

## Installation
1. Créer le venv :
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2. Installer les dépendances :
```powershell
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Variables d'environnement
- GMAIL_USER : l'email pour l'envoi de l'email
- GMAIL_APP_PASSWORD : le mot de passe SMTP gmail de la configuration 


## Usage rapide en console 
- Exécuter le pipeline d'extraction/enrichissement/consolidation :
```powershell
& .\.venv\Scripts\python.exe main.py

```


## Usage rapide avec interface 
- Exécuter le pipeline d'extraction/enrichissement/consolidation :
```powershell
& .venv/Scripts/Activate.ps1 
streamlit run TABLEAU_DE_BORD.py


```
- Lancer le notebook de visualisation (Jupyter) et ouvrir `visualisation.ipynb` :
```powershell
& .\.venv\Scripts\python.exe -m jupyter notebook
```

Remarque : certaines étapes (enrichissement) peuvent requérir des clés/API externes selon l'implémentation.

## Notions de visualisation proposées
- Distribution des scores CVSS / EPSS
- Corrélation CVSS vs EPSS (avec régression)
- Évolution cumulative des vulnérabilités par date
- Top vendors / produits affectés
- Heatmap de corrélations entre métriques
- ...

## Fichiers de données
- `consolidated_data.csv` : colonnes attendues (Titre du bulletin, Type de bulletin, Date de publication, Identifiant CVE, Score CVSS, Base Severity, Type CWE, Score EPSS, Lien, Description, Éditeur/Vendor, Produit, Versions affectées)
- `enriched_cves.csv` : colonnes attendues (cve_id, description, cvss_score, cwe, epss_score)

## Contribution
Contribuez par Pull Request en expliquant les modifications. Respectez les bonnes pratiques : tests, documentation minimale, et mise à jour de `requirements.txt` si nécessaire.

## Contact
Pour questions / amélioration : ouvrez une issue ou contactez l'auteur du projet.
