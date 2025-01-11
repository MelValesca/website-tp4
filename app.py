from flask import Flask, render_template, request, jsonify, Response
from .database import Database
from flask import g
from apscheduler.schedulers.background import BackgroundScheduler
from .trouver_violation import ajouter_donnees
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError
import dicttoxml
import csv
import io
from .plainte import Plainte

from .schemas import plainte_schema

app = Flask(__name__, static_url_path="", static_folder="static")
schema = JsonSchema(app)
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(ajouter_donnees, "cron", day_of_week="*", hour=0, minute=0)
app.config["JSON_AS_ASCII"] = False


def start_scheduler():
    scheduler.start()
    print("BackgroundScheduler démarré.")


@app.before_request
def before_request():
    if not scheduler.running:
        start_scheduler()


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.disconnect()


@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({"error": e.message, "errors": errors}), 400


@app.route("/", methods=["GET", "POST"])
def accueil():
    db = get_db()
    etablissements = db.get_etablissements()
    return render_template("index.html", etablissements=etablissements)


@app.route("/doc", methods=["GET"])
def doc():
    return render_template("doc.html")


@app.route("/recherche", methods=["POST"])
def recherche():
    mot_cle = request.form["recherche"]
    db = get_db()
    recherche = db.recherche(mot_cle)
    return render_template(
        "recherche.html",
        recherche=recherche,
        mot_cle=mot_cle,
        nb_resultat=len(recherche),
    )


@app.route("/contrevenants", methods=["GET"])
def get_contrevenants():
    db = get_db()
    du = request.args.get("du")
    au = request.args.get("au")
    return jsonify(db.get_contrevenants(du, au))


@app.route("/contrevenants/json", methods=["GET"])
def get_contrevenants_json():
    db = get_db()
    return jsonify(db.get_contrevenants_ordre())


@app.route("/contrevenants/xml", methods=["GET"])
def get_contrevenants_xml():
    db = get_db()
    contrevenants = db.get_contrevenants_ordre()
    xml_data = dicttoxml.dicttoxml(
        contrevenants, custom_root="contrevenants", attr_type=False
    )
    return Response(xml_data, content_type="application/xml")


@app.route("/contrevenants/csv", methods=["GET"])
def get_contrevenants_csv():
    db = get_db()
    contrevenants = db.get_contrevenants_ordre()

    csv_output = io.StringIO()
    writer = csv.writer(csv_output)
    writer.writerow(["etablissement", "nb_contraventions"])

    for contrevenant in contrevenants:
        writer.writerow(
            [contrevenant["etablissement"], contrevenant["nb_contraventions"]]
        )

    return Response(csv_output.getvalue(), content_type="text/csv")


@app.route("/etablissement", methods=["GET"])
def get_etablissement():
    db = get_db()
    etablissement = request.args.get("nom")
    contraventions = db.get_contraventions(etablissement)
    return jsonify(contraventions)


@app.route("/plainte", methods=["GET"])
def creer_plainte():
    return render_template("plainte.html")


@app.route("/formuler-plainte", methods=["POST"])
@schema.validate(plainte_schema)
def ajouter_plainte():
    db = get_db()
    data = request.get_json()
    plainte = Plainte(
        data["etablissement"],
        data["adresse"],
        data["ville"],
        data["date_visite"],
        data["prenom"],
        data["nom"],
        data["description_probleme"],
    )
    db.ajouter_plainte(plainte.asDictionary())
    return jsonify(plainte.asDictionary()), 201


@app.errorhandler(404)
def page_not_found(erreur):
    return render_template("404.html"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("405.html"), 405
