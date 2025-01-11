import sqlite3


def _build_violation(data):
    violation = {
        "id_pursuit": data[0],
        "buisness_id": data[1],
        "date": data[2],
        "description": data[3],
        "adresse": data[4],
        "date_jugement": data[5],
        "etablissement": data[6],
        "montant": data[7],
        "proprietaire": data[8],
        "ville": data[9],
        "statut": data[10],
        "date_statut": data[11],
        "categorie": data[12],
    }
    return violation


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db/database.db")
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def recherche(self, mot_cle):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM Violations WHERE "
            "etablissement LIKE '%' || ? || '%' "
            "OR proprietaire LIKE '%' || ? || '%' "
            "OR adresse LIKE '%' || ? || '%'",
            (mot_cle, mot_cle, mot_cle),
        )
        violations_data = cursor.fetchall()
        violations = [
            _build_violation(violation_data)
            for violation_data in violations_data
        ]
        return violations

    def get_contrevenants(self, du, au):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT etablissement, COUNT(etablissement) "
            "AS occurrences "
            "FROM violations WHERE date "
            "BETWEEN ? AND ? GROUP BY etablissement ",
            (du, au),
        )
        contrevenants_data = cursor.fetchall()
        contrevenants = [
            {"etablissement": row[0], "nb_contraventions": row[1]}
            for row in contrevenants_data
        ]
        return contrevenants

    def get_contrevenants_ordre(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT etablissement, COUNT(etablissement) "
            "AS occurrences "
            "FROM violations "
            "GROUP BY etablissement "
            "ORDER BY occurrences DESC"
        )
        contrevenants_data = cursor.fetchall()
        contrevenants = [
            {"etablissement": row[0], "nb_contraventions": row[1]}
            for row in contrevenants_data
        ]
        return contrevenants

    def get_contraventions(self, etablissement):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM violations WHERE etablissement = ?",
            (etablissement,)
        )
        violations_data = cursor.fetchall()
        violations = [
            _build_violation(violation_data)
            for violation_data in violations_data
        ]
        return violations

    def get_etablissements(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT DISTINCT etablissement"
            " FROM violations "
            "ORDER BY etablissement"
        )
        unique_etablissements_data = cursor.fetchall()
        unique_etablissements = [row[0] for row in unique_etablissements_data]
        return unique_etablissements

    def ajouter_plainte(self, plainte):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO plainte (etablissement, adresse, "
            "ville, date_visite, prenom, "
            "nom, description_probleme) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                plainte["etablissement"],
                plainte["adresse"],
                plainte["ville"],
                plainte["date_visite"],
                plainte["prenom"],
                plainte["nom"],
                plainte["description_probleme"],
            ),
        )
        connection.commit()
