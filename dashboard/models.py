from sqlalchemy import (
    Column, Integer, String, ForeignKey, Enum, Date, Time, Float
)
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# --- ENUM type ---
class ResultatEnum(enum.Enum):
    Victoire = "Victoire"
    Defaite = "Defaite"
    Nul = "Nul"

# --- Tables ---
class Competition(Base):
    __tablename__ = "competition"
    id_competition = Column(Integer, primary_key=True)
    nom_competition = Column(String, nullable=False)

    equipes = relationship("Equipe", back_populates="competition")
    matchs = relationship("Match", back_populates="competition")


class Saison(Base):
    __tablename__ = "saison"
    id_saison = Column(Integer, primary_key=True)
    annee = Column(Integer, nullable=False)

    equipes = relationship("Equipe", back_populates="saison")
    matchs = relationship("Match", back_populates="saison")


class Equipe(Base):
    __tablename__ = "equipe"
    id_equipe = Column(Integer, primary_key=True)
    nom_equipe = Column(String, nullable=False)
    id_competition = Column(Integer, ForeignKey("competition.id_competition"))
    id_saison = Column(Integer, ForeignKey("saison.id_saison"))

    competition = relationship("Competition", back_populates="equipes")
    saison = relationship("Saison", back_populates="equipes")
    joueurs = relationship("Joueur", back_populates="equipe")
    resultats = relationship("ResultatMatch", back_populates="equipe")


class Joueur(Base):
    __tablename__ = "joueur"
    id_joueur = Column(Integer, primary_key=True)
    nom_joueur = Column(String, nullable=False)
    position = Column(String)
    nationalite = Column(String)
    id_equipe = Column(Integer, ForeignKey("equipe.id_equipe"))

    equipe = relationship("Equipe", back_populates="joueurs")
    stats = relationship("StatistiqueJoueur", back_populates="joueur")


class Match(Base):
    __tablename__ = "match"
    id_match = Column(Integer, primary_key=True)
    date_match = Column(Date)
    heure = Column(Time)
    round = Column(String)
    venue = Column(String)
    id_team_home = Column(Integer, ForeignKey("equipe.id_equipe"))
    id_team_away = Column(Integer, ForeignKey("equipe.id_equipe"))
    id_competition = Column(Integer, ForeignKey("competition.id_competition"))
    id_saison = Column(Integer, ForeignKey("saison.id_saison"))

    competition = relationship("Competition", back_populates="matchs")
    saison = relationship("Saison", back_populates="matchs")
    resultats = relationship("ResultatMatch", back_populates="match")


class ResultatMatch(Base):
    __tablename__ = "resultat_match"
    id_resultat = Column(Integer, primary_key=True)
    id_match = Column(Integer, ForeignKey("match.id_match"))
    id_equipe = Column(Integer, ForeignKey("equipe.id_equipe"))
    buts_marques = Column(Integer)
    buts_concedes = Column(Integer)
    resultat = Column(Enum(ResultatEnum))

    match = relationship("Match", back_populates="resultats")
    equipe = relationship("Equipe", back_populates="resultats")


class StatistiqueJoueur(Base):
    __tablename__ = "statistique_joueur"
    id_stats = Column(Integer, primary_key=True)
    id_joueur = Column(Integer, ForeignKey("joueur.id_joueur"))
    buts = Column(Integer, default=0)
    passes_decisives = Column(Integer, default=0)
    nb_matches_played = Column(Integer, default=0)
    cartons_jaunes = Column(Integer, default=0)
    cartons_rouges = Column(Integer, default=0)

    joueur = relationship("Joueur", back_populates="stats")