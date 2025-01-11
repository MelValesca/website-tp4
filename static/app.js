function rechercherContravenants(event) {
  event.preventDefault();
  var du = document.getElementById("du").value;
  var au = document.getElementById("au").value;
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        afficherResultat(xhr.responseText);
      } else {
        document.getElementById("resultat").innerHTML =
          "Une erreur s'est produite.";
      }
    }
  };
  xhr.open("GET", "/contrevenants?du=" + du + "&au=" + au, true);
  xhr.send();
}

function rechercherEtablissement(event) {
  event.preventDefault();
  var etablissement = document.getElementById("nom").value;
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        afficherContraventions(xhr.responseText);
      } else {
        document.getElementById("resultat-etablissement").innerHTML =
          "Une erreur s'est produite.";
      }
    }
  };
  xhr.open("GET", "/etablissement?nom=" + etablissement, true);
  xhr.send();
}

function afficherContraventions(reponse) {
  var resultatDiv = document.getElementById("resultat-etablissement");
  resultatDiv.innerHTML = "";
  var contraventions = JSON.parse(reponse);

  contraventions.forEach(function (violation) {
    var violationDiv = document.createElement("div");
    violationDiv.className = "contravention";

    var idPoursuite = document.createElement("span");
    idPoursuite.textContent = "ID de poursuite: " + violation["id_pursuit"];
    violationDiv.appendChild(idPoursuite);

    var idBuisness = document.createElement("span");
    idBuisness.textContent = "ID de buisness: " + violation["buisness_id"];
    violationDiv.appendChild(idBuisness);

    var etablissement = document.createElement("span");
    etablissement.textContent =
      "Nom de l'établissement: " + violation["etablissement"];
    violationDiv.appendChild(etablissement);

    var proprietaire = document.createElement("span");
    proprietaire.textContent = "Propriétaire: " + violation["proprietaire"];
    violationDiv.appendChild(proprietaire);

    var date = document.createElement("span");
    date.textContent = "Date: " + violation["date"];
    violationDiv.appendChild(date);

    var description = document.createElement("span");
    description.textContent = "Description: " + violation["description"];
    violationDiv.appendChild(description);

    var adresse = document.createElement("span");
    adresse.textContent = "Adresse: " + violation["adresse"];
    violationDiv.appendChild(adresse);

    var ville = document.createElement("span");
    ville.textContent = "Ville: " + violation["ville"];
    violationDiv.appendChild(ville);

    var dateJugement = document.createElement("span");
    dateJugement.textContent =
      "Date de jugement: " + violation["date_jugement"];
    violationDiv.appendChild(dateJugement);

    var montant = document.createElement("span");
    montant.textContent =
      "Montant de la contravention: " + violation["montant"];
    violationDiv.appendChild(montant);

    var statut = document.createElement("span");
    statut.textContent = "Statut: " + violation["statut"];
    violationDiv.appendChild(statut);

    var dateStatut = document.createElement("span");
    dateStatut.textContent = "Date du statut: " + violation["date_statut"];
    violationDiv.appendChild(dateStatut);

    var categorie = document.createElement("span");
    categorie.textContent = "Catégorie: " + violation["categorie"];
    violationDiv.appendChild(categorie);

    resultatDiv.appendChild(violationDiv);
  });
}

function afficherResultat(reponse) {
  var resultatDiv = document.getElementById("resultat");
  var contraventions = JSON.parse(reponse);
  var tableauHtml =
    "<table><tr><th>Nom de l'établissement</th><th>Nombre de contraventions</th></tr>";

  contraventions.forEach(function (contravention) {
    tableauHtml +=
      "<tr><td>" +
      contravention["etablissement"] +
      "</td><td>" +
      contravention["nb_contraventions"] +
      "</td></tr>";
  });

  tableauHtml += "</table>";
  resultatDiv.innerHTML = tableauHtml;
}

document
  .getElementById("recherche-par-date")
  .addEventListener("submit", rechercherContravenants);

document
  .getElementById("recherche-etablissement")
  .addEventListener("submit", rechercherEtablissement);
