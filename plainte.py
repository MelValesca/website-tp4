class Plainte:
    def __init__(self, etablissement, adresse, ville, date_visite, prenom, nom, description_probleme):
        self.etablissement = etablissement
        self.adresse = adresse
        self.ville = ville
        self.date_visite = date_visite
        self.prenom = prenom
        self.nom = nom
        self.description_probleme = description_probleme

    def asDictionary(self):
        return {"etablissement": self.etablissement,
                "adresse": self.adresse,
                "ville": self.ville,
                "date_visite": self.date_visite,
                "prenom": self.prenom,
                "nom": self.nom,
                "description_probleme": self.description_probleme}