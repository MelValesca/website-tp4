import csv
import sqlite3
import urllib.request
from datetime import datetime


def inserer_donnees(donnees):
    conn = sqlite3.connect("db/database.db")
    c = conn.cursor()
    c.executemany(
        """INSERT OR IGNORE INTO violations
            (id_pursuit, buisness_id, date, description, adresse,
            date_jugement,etablissement, montant, proprietaire,
           ville, statut, date_statut, categorie)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        donnees,
    )
    conn.commit()
    conn.close()


def effectuer_requete(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    reponse = urllib.request.urlopen(req)
    return reponse.read().decode("utf-8").splitlines()


def lire_fichier(donnees):
    lecteur_csv = csv.reader(donnees)
    next(lecteur_csv)
    donnees_csv = []
    for ligne in lecteur_csv:
        date = datetime.strptime(ligne[2],
                                 "%Y%m%d").strftime("%Y-%m-%d")
        date_jugement = datetime.strptime(ligne[5],
                                          "%Y%m%d").strftime("%Y-%m-%d")
        date_statut = datetime.strptime(ligne[11],
                                        "%Y%m%d").strftime("%Y-%m-%d")
        donnees_csv.append(
            (
                int(ligne[0]),
                int(ligne[1]),
                date,
                ligne[3],
                ligne[4],
                date_jugement,
                ligne[6],
                int(ligne[7]),
                ligne[8],
                ligne[9],
                ligne[10],
                date_statut,
                ligne[12],
            )
        )
    return donnees_csv


def ajouter_donnees():
    url = (
        "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-"
        "5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/"
        "download/violations.csv"
    )
    donnees = effectuer_requete(url)
    donnees_csv = lire_fichier(donnees)
    inserer_donnees(donnees_csv)
    print("Données insérées avec succès dans la base de données.")


if __name__ == "__main__":
    ajouter_donnees()
