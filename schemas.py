plainte_schema = {
    "type": "object",
    "properties": {
        "etablissement": {"type": "string"},
        "adresse": {"type": "string", "maxLength": 40, "minLength": 1},
        "ville": {"type": "string", "maxLength": 20, "minLength": 1},
        "date_visite": {"type": "string", "format": "date", "minLength": 1},
        "prenom": {"type": "string", "maxLength": 25, "minLength": 1},
        "nom": {"type": "string", "maxLength": 25, "minLength": 1},
        "description_probleme": {
            "type": "string",
            "maxLength": 500,
            "minLength": 1
            },
    },
    "required": [
        "etablissement",
        "adresse",
        "ville",
        "date_visite",
        "prenom",
        "nom",
        "description_probleme",
    ],
    "additionalProperties": False,
}
