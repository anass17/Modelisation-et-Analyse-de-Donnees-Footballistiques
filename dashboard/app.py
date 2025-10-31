import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy.orm import joinedload
from database import SessionLocal
from models import (
    Competition, Saison, Equipe, Joueur, Match, ResultatMatch, StatistiqueJoueur
)

# ----------------------------
# STREAMLIT CONFIG
# ----------------------------
st.set_page_config(page_title="Football Dashboard", layout="wide")
st.title("Tableau de bord")

# ----------------------------
# SESSION
# ----------------------------
@st.cache_resource
def get_session():
    return SessionLocal()

session = get_session()

# ----------------------------
# FILTERS
# ----------------------------
competitions = session.query(Competition).all()
seasons = session.query(Saison).order_by(Saison.annee.desc()).all()

col1, col2 = st.columns(2)
with col1:
    comp_choice = st.selectbox("Compétition", ["Toutes"] + [c.nom_competition for c in competitions])
with col2:
    season_choice = st.selectbox("Saison", ["Toutes"] + [str(s.annee) for s in seasons])

# ----------------------------
# LOAD DATA WITH ORM
# ----------------------------

def get_player_stats():
    """Join joueur, equipe, and statistique_joueur"""
    q = (
        session.query(
            Joueur.id_joueur,
            Joueur.nom_joueur,
            Joueur.position,
            Joueur.nationalite,
            Equipe.nom_equipe,
            StatistiqueJoueur.buts,
            StatistiqueJoueur.passes_decisives,
            StatistiqueJoueur.nb_matches_played,
            StatistiqueJoueur.cartons_jaunes,
            StatistiqueJoueur.cartons_rouges,
        )
        .join(Equipe, Joueur.id_equipe == Equipe.id_equipe)
        .join(StatistiqueJoueur, StatistiqueJoueur.id_joueur == Joueur.id_joueur)
    )
    return pd.DataFrame(q.all(), columns=[c["name"] for c in q.column_descriptions])

def get_match_results():
    q = (
        session.query(
            ResultatMatch.id_resultat,
            ResultatMatch.buts_marques,
            ResultatMatch.buts_concedes,
            ResultatMatch.resultat,
            Equipe.nom_equipe,
            Match.id_match,
            Match.date_match,
            Match.round,
            Match.id_competition,
            Match.id_saison,
        )
        .join(Match, ResultatMatch.id_match == Match.id_match)
        .join(Equipe, ResultatMatch.id_equipe == Equipe.id_equipe)
    )
    return pd.DataFrame(q.all(), columns=[c["name"] for c in q.column_descriptions])

df_players = get_player_stats()
df_results = get_match_results()

# Filter if needed
if comp_choice != "Toutes":
    comp_id = next(c.id_competition for c in competitions if c.nom_competition == comp_choice)
    df_results = df_results[df_results["id_competition"] == comp_id]

if season_choice != "Toutes":
    season_id = next(s.id_saison for s in seasons if str(s.annee) == season_choice)
    df_results = df_results[df_results["id_saison"] == season_id]

# Filter players to teams present in results
teams_in_scope = df_results["nom_equipe"].unique()
if len(teams_in_scope) > 0:
    df_players = df_players[df_players["nom_equipe"].isin(teams_in_scope)]



def joueurs_disciplinés(session):
    data = (
        session.query(
            Joueur.nom_joueur,
            StatistiqueJoueur.cartons_jaunes,
            StatistiqueJoueur.cartons_rouges
        )
        .join(StatistiqueJoueur, Joueur.id_joueur == StatistiqueJoueur.id_joueur)
        .all()
    )
    df = pd.DataFrame(data, columns=["Joueur", "Cartons Jaunes", "Cartons Rouges"])
    df["Total Cartons"] = df["Cartons Jaunes"] + df["Cartons Rouges"]
    df = df.sort_values(by="Total Cartons", ascending=False)

    fig = px.bar(df, x="Joueur", y=["Cartons Jaunes", "Cartons Rouges"],
                 title="Joueurs les plus disciplinés (cartons jaunes et rouges)",
                 barmode="stack")
    st.plotly_chart(fig, use_container_width=True)

def repartition_nationalites(session):
    data = (
        session.query(
            Equipe.nom_equipe,
            Joueur.nationalite
        )
        .join(Joueur, Joueur.id_equipe == Equipe.id_equipe)
        .all()
    )
    df = pd.DataFrame(data, columns=["Équipe", "Nationalité"])

    fig = px.histogram(df, x="Équipe", color="Nationalité",
                       title="Répartition des nationalités par équipe",
                       barmode="group")
    st.plotly_chart(fig, use_container_width=True)

def buts_par_equipe(session):
    data = (
        session.query(
            Equipe.nom_equipe,
            ResultatMatch.buts_marques
        )
        .join(ResultatMatch, ResultatMatch.id_equipe == Equipe.id_equipe)
        .all()
    )
    df = pd.DataFrame(data, columns=["Équipe", "Buts Marqués"])
    df = df.groupby("Équipe", as_index=False)["Buts Marqués"].sum()

    fig = px.bar(df, x="Équipe", y="Buts Marqués",
                 title="Nombre total de buts par équipe")
    st.plotly_chart(fig, use_container_width=True)

def moyenne_buts_par_match(session):
    data = (
        session.query(
            Equipe.nom_equipe,
            ResultatMatch.buts_marques,
            ResultatMatch.buts_concedes
        )
        .join(ResultatMatch, ResultatMatch.id_equipe == Equipe.id_equipe)
        .all()
    )
    df = pd.DataFrame(data, columns=["Équipe", "Buts Marqués", "Buts Concédés"])
    df = df.groupby("Équipe", as_index=False).mean()

    fig = px.bar(df, x="Équipe", y=["Buts Marqués", "Buts Concédés"],
                 title="Moyenne des buts marqués et encaissés par match",
                 barmode="group")
    st.plotly_chart(fig, use_container_width=True)

def meilleures_defenses(session):
    data = (
        session.query(
            Equipe.nom_equipe,
            ResultatMatch.buts_concedes
        )
        .join(ResultatMatch, ResultatMatch.id_equipe == Equipe.id_equipe)
        .all()
    )

    df = pd.DataFrame(data, columns=["Équipe", "Buts Concédés"])
    df = df.groupby("Équipe", as_index=False)["Buts Concédés"].sum()
    df = df.sort_values(by="Buts Concédés", ascending=True)

    fig = px.bar(df, x="Équipe", y="Buts Concédés",
                 title="Équipes avec la meilleure défense (moins de buts concédés)")
    st.plotly_chart(fig, use_container_width=True)

def meilleurs_buteurs_par_equipe(session):
    data = (
        session.query(
            Equipe.nom_equipe,
            Joueur.nom_joueur,
            StatistiqueJoueur.buts
        )
        .join(Joueur, Joueur.id_equipe == Equipe.id_equipe)
        .join(StatistiqueJoueur, Joueur.id_joueur == StatistiqueJoueur.id_joueur)
        .all()
    )

    df = pd.DataFrame(data, columns=["Équipe", "Joueur", "Buts"])

    # Sélectionner le joueur avec le plus de buts dans chaque équipe
    df_top = df.loc[df.groupby("Équipe")["Buts"].idxmax()]

    fig = px.bar(df_top, x="Équipe", y="Buts", color="Joueur",
                 title="Meilleurs buteurs par équipe", text="Joueur")
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

def matchs_par_equipe(session):
    data = (
        session.query(
            Equipe.nom_equipe,
            Match.id_match
        )
        .join(ResultatMatch, ResultatMatch.id_equipe == Equipe.id_equipe)
        .join(Match, Match.id_match == ResultatMatch.id_match)
        .all()
    )

    df = pd.DataFrame(data, columns=["Équipe", "Match"])
    df = df.groupby("Équipe", as_index=False)["Match"].count()
    df.rename(columns={"Match": "Nombre de matchs joués"}, inplace=True)

    fig = px.bar(df, x="Équipe", y="Nombre de matchs joués",
                 title="Nombre total de matchs joués par équipe")
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# VISUALIZATIONS
# ----------------------------
st.subheader("Top 10 des meilleurs buteurs")
top_scorers = df_players.groupby(["nom_joueur","nom_equipe"])["buts"].sum().sort_values(ascending=False).head(10).reset_index()
fig1 = px.bar(top_scorers, x="nom_joueur", y="buts", color="nom_equipe", title="Top 10 buteurs")
st.plotly_chart(fig1, use_container_width=True)
st.dataframe(top_scorers)

st.subheader("Joueurs les plus décisifs (buts + passes)")
df_players["total"] = df_players["buts"] + df_players["passes_decisives"]
decisive = df_players.groupby(["nom_joueur","nom_equipe"])["total"].sum().sort_values(ascending=False).head(10).reset_index()
fig2 = px.bar(decisive, x="nom_joueur", y="total", color="nom_equipe", title="Joueurs les plus décisifs")
st.plotly_chart(fig2, use_container_width=True)

joueurs_disciplinés(session)
repartition_nationalites(session)
buts_par_equipe(session)
moyenne_buts_par_match(session)

meilleures_defenses(session)
meilleurs_buteurs_par_equipe(session)
matchs_par_equipe(session)


st.subheader("Classement des équipes")
df_results["points"] = df_results["resultat"].map({"Victoire": 3, "Nul": 1, "Défaite": 0})
ranking = df_results.groupby("nom_equipe", as_index=False).agg(
    pts=("points","sum"),
    buts_marques=("buts_marques","sum"),
    buts_concedes=("buts_concedes","sum")
).sort_values("pts", ascending=False)
st.dataframe(ranking)

# ----------------------------
# DOWNLOAD
# ----------------------------
csv = ranking.to_csv(index=False).encode("utf-8")
st.download_button(
    "Télécharger le classement (CSV)",
    csv,
    "classement.csv",
    "text/csv"
)