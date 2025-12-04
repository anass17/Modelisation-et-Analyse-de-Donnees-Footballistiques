This README is in English. For the French version, see [README.md](README.md).

# Football Analytics — Analysis for Professional Football

## Project Context

This innovative project aims to develop a comprehensive solution for professional football analysis. The goal is to create a data-driven ecosystem capable of:

- Predicting match outcomes.
- Optimizing team strategies.

---

## Technologies Used

- **Python 3:** data processing and development
- **Selenium:** web scraping
- **Pandas / NumPy:** data manipulation
- **SQLAlchemy / PostgreSQL:** storage and queries
- **Matplotlib / Seaborn:** data visualization
- **Streamlit:** interactive dashboard

---

## Project Structure

```
Modelisation-et-Analyse-de-Donnees-Footballistiques/
|
├── data/
│   ├── raw/                  # Raw CSV files from scraping
│   └── processed/            # Cleaned and standardized data
│
├── notebooks/
│   ├── scraping.ipynb        # Selenium scraping scripts
│   ├── nettoyage.ipynb       # Data cleaning and transformation
│   ├── stockage.ipynb        # Storage in PostgreSQL with SQLAlchemy
│
├── dashboard/
│   ├── app.py                # Streamlit dashboard
│   ├── database.py           # Database connection
│   ├── models.py             # Table definitions
│
├── docs/
│   ├── ERD.png               # ERD diagram of the database
│
├── .env                      # Environment variables
├── .gitignore
├── requirements.txt          # Python dependencies
├── README.md                 # French documentation
└── README_en.md              # English documentation
```

---

## Execution Instructions

1. Clone the project:
```Bash
git clone https://github.com/anass17/Modelisation-et-Analyse-de-Donnees-Footballistiques
cd Modelisation-et-Analyse-de-Donnees-Footballistiques
```

2. Install dependencies:
```Bash
pip install -r requirements.txt
```

3. Create the .env file and set environment variables:
- Create a file named .env in the root of the project.
- Add the required variables, for example:

```
DB_USER=your_db_username
DB_PASS=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=football_db
```

4. Launch the Streamlit dashboard:
```Bash
streamlit run dashboard/app.py
```

5. Open the dashboard in your browser (if it does not open automatically):
`http://localhost:8501/`

---

## Project Pipeline

The project relies on a structured data pipeline composed of the following steps:

### 1. Data Collection — Web Scraping

- Collect football data from FBref using **Selenium**.
- Extract Premier League team information for the 2024–2025 season.
- For each team, retrieve:
    - Detailed player information (name, position, nationality, etc.)
    - Matches played with key statistics
- Organize the data and export it to `CSV` for further processing.

---

### 2. Data Transformation

- **Cleaning:** handle missing or inconsistent values.
- **Standardization:** harmonize units, date formats, and column names for consistent quality.

---

### 3. Data Storage and Modeling

- Store the transformed data in a PostgreSQL database with a structured schema.
- Database schema:
    - competition(idcompetition, nomcompetition)
    - saison(id_saison, annee)
    - equipe(idequipe, nomequipe, idcompetition, idsaison)
    - joueur(idjoueur, nomjoueur, position, nationalite, id_equipe)
    - match(idmatch_, date_match, heure, round, venue, idteamhome, idteam_away, id_competition, id_saison)
    - resultatmatch(idresultat, idmatch, idequipe, butsmarques, butsconcedes, resultat ENUM('Victory', 'Defeat', 'Draw'))
    - statistiquejoueur(idstats, idjoueur, buts, passesdecisives, nbmatchesplayed, cartonsjaunes, cartonsrouges)

---

### 4. Data Analysis

- Perform SQL queries to extract key insights about player and team performance:
    - Top 10 goal scorers
    - Most decisive players (goals + assists)
    - Most disciplined players (yellow/red cards)
    - Player nationality distribution by team
    - Total goals per team
    - Average goals scored/conceded per match
    - Team ranking (win = 3 pts, draw = 1 pt)
    - Teams with best defense (least goals conceded)
    - Top scorer per team
    - Total matches played per team

---

### 5. Dashboard — Streamlit

- Configure database connection via **SQLAlchemy**
- Retrieve data using SQL queries
- Create interactive visualizations in **Streamlit**:
    - Python functions for each chart
    - Dynamic display based on user-selected filters
- Add an interactive table `(st.dataframe)` for filtered data
- Include a download button to export filtered data as CSV

## Visualisations

### Diagram (ERD)
![ERD](https://github.com/user-attachments/assets/b0c16ea4-83c6-452b-8fab-ee163a38b342)

### Streamlit Interface 
![Streamlit UI](https://github.com/user-attachments/assets/4b717d0c-b8c6-4a88-bf0d-0cc1d00c311f)
