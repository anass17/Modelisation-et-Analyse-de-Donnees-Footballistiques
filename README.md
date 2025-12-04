Ce README est en français. Pour la version anglaise, voir [README_en.md](README_en.md).

# Football Analytics — Analyse pour le Football Professionnel

## Contexte du Projet

Ce projet innovant vise à développer une solution complète d’analyse pour le football professionnel. L’objectif est de créer un écosystème data-driven capable de :

- Anticiper les résultats des matchs.
- Optimiser les stratégies des équipes.

--- 

## Technologies Utilisées

- **Python 3 :** traitement des données et développement
- **Selenium :** web scraping
- **Pandas / NumPy :** manipulation des données
- **SQLAlchemy / PostgreSQL :** stockage et requêtes
- **Matplotlib / Seaborn :** visualisation des données
- **Streamlit :** tableau de bord interactif

---

## Structure du Projet

```
Modelisation-et-Analyse-de-Donnees-Footballistiques/
│
├── data/
│   ├── raw/                        # Fichiers CSV bruts issus du scraping
│   └── processed/                  # Données nettoyées et standardisées
│
├── notebooks/
│   ├── scraping.ipynb              # Scripts de scraping Selenium
│   ├── nettoyage.ipynb             
│   ├── stockage.ipynb              # Stockage avec SQLAlchemy
│
├── dashboard/
│   ├── app.py                      # Tableau de bord Streamlit
│   ├── database.py                 # Connexion avec la base de données
│   ├── models.py                   # Définitions des tables
│
├── docs/
│   ├── ERD.png                     # Diagramme ERD de la base de données
│
├── .env                            # Variables d'environnement
├── .gitignore                      
├── requirements.txt                # Dépendances Python
├── README.md                       # Documentation du projet en français
└── README_en.md                    # Documentation du projet en anglais
```

---

## Instructions d’Exécution

1. Cloner le projet :
```Bash
git clone https://github.com/anass17/Modelisation-et-Analyse-de-Donnees-Footballistiques
cd Modelisation-et-Analyse-de-Donnees-Footballistiques
```

2. Installer les dépendances :
```Bash
pip install -r requirements.txt
```

3. Créer le fichier .env et définir les variables d’environnement :
- Créez un fichier nommé .env à la racine du projet.
- Ajoutez-y les variables nécessaires:

```
DB_USER=your_db_username
DB_PASS=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=football_db
```

4. Lancer le tableau de bord Streamlit :
```Bash
streamlit run dashboard/app.py
```

5. Ouvrir l’application dans le navigateur (si elle ne s’ouvre pas automatiquement) :
`http://localhost:8501/`

--- 

### Étapes de réalisation

Le projet repose sur un pipeline de données structuré composé de plusieurs étapes.

### 1. Collecte des Données — Web Scraping
- Collecter les données de football depuis FBref à l’aide de **Selenium**.
- Extraire les informations des équipes de la Premier League pour la saison 2024–2025.
- Pour chaque équipe, récupérer :
    - Les informations détaillées des joueurs (nom, poste, nationalité, etc.)
    - Les matchs joués durant la saison avec les statistiques clés
- Organiser les données et les exporter au format `CSV` pour les étapes suivantes.

---

### 2. Transformation des Données

- **Nettoyage :** gestion des valeurs manquantes ou incohérentes.
- **Standardisation :** harmonisation des unités, formats de date et noms de colonnes pour assurer la qualité des données.

---

### 3. Stockage et Modélisation des Données

- Stocker les données transformées dans une base de données PostgreSQL avec un modèle structuré.
- Schéma de la base de données :
    - competition(idcompetition, nomcompetition)
    - saison(id_saison, annee)
    - equipe(idequipe, nomequipe, idcompetition, idsaison)
    - joueur(idjoueur, nomjoueur, position, nationalite, id_equipe)
    - match(idmatch_, date_match, heure, round, venue, idteamhome, idteam_away, id_competition, id_saison)
    - resultatmatch(idresultat, idmatch, idequipe, butsmarques, butsconcedes, resultat ENUM('Victoire', 'Défaite', 'Nul'))
    - statistiquejoueur(idstats, idjoueur, buts, passesdecisives, nbmatchesplayed, cartonsjaunes, cartonsrouges)

---

### 4. Analyse des Données

Réaliser des requêtes SQL pour extraire des informations clés sur les performances des joueurs et des équipes :

- Top 10 des meilleurs buteurs — joueurs ayant marqué le plus de buts.
- Joueurs les plus décisifs — calcul du total buts + passes décisives.
- Joueurs les plus disciplinés — statistiques de cartons jaunes et rouges.
- Répartition des nationalités par équipe.
- Nombre total de buts par équipe — évaluer la puissance offensive.
- Moyenne de buts marqués et encaissés par match — mesurer l’efficacité et la défense.
- Classement des équipes — victoire = 3 pts, nul = 1 pt.
- Équipes avec la meilleure défense — moins de buts encaissés.
- Meilleur buteur par équipe
- Nombre total de matchs joués par équipe

---

### 5. Tableau de Bord — Streamlit

- Configurer la connexion à la base avec **SQLAlchemy**.
- Récupérer les données via requêtes SQL.
- Créer des visualisations interactives avec **Streamlit** :
    - Fonctions Python pour chaque graphique
    - Affichage dynamique selon les filtres sélectionnés par l’utilisateur
- Ajouter un tableau interactif `(st.dataframe)` pour les données filtrées
- Intégrer un bouton de téléchargement pour exporter les données en CSV

## Visualisations du projet

### Diagramme (ERD)
![ERD](https://github.com/user-attachments/assets/b0c16ea4-83c6-452b-8fab-ee163a38b342)

### Interface Streamlit
![Streamlit UI](https://github.com/user-attachments/assets/4b717d0c-b8c6-4a88-bf0d-0cc1d00c311f)
