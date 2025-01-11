CREATE TABLE violations (
    id_pursuit INTEGER PRIMARY KEY,
    buisness_id INTEGER,
    date DATE,
    description VARCHAR(500),
    adresse VARCHAR(40),
    date_jugement DATE,
    etablissement VARCHAR(255),
    montant INTEGER, 
    proprietaire VARCHAR(40),
    ville VARCHAR(30),
    statut VARCHAR(20),
    date_statut DATE,
    categorie VARCHAR(40)
);
CREATE TABLE plainte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    etablissement VARCHAR(255),
    adresse VARCHAR(40),
    ville VARCHAR(20),
    date_visite DATE,
    prenom VARCHAR(25),
    nom VARCHAR(25),
    description_probleme VARCHAR(500)
);
