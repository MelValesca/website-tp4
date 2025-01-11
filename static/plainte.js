document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("ajouter-plainte");
  var resultatDiv = document.querySelector(".resultat");
  var erreurDiv = document.querySelector(".erreur");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var formData = {
      etablissement: document.getElementById("etablissement").value,
      adresse: document.getElementById("adresse").value,
      ville: document.getElementById("ville").value,
      date_visite: document.getElementById("date_visite").value,
      prenom: document.getElementById("prenom").value,
      nom: document.getElementById("nom").value,
      description_probleme: document.getElementById("description_probleme")
        .value,
    };
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 201) {
          resultatDiv.innerHTML = "Plainte envoyée avec succès !";
        } else {
          erreurDiv.innerHTML = "Erreur lors de l'envoie du formulaire.";
        }
      }
    };
    xhr.open("POST", "/formuler-plainte");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(formData));
  });
});

function updateCountdown() {
  var textarea = document.getElementById("description_probleme");
  var countDisplay = document.getElementById("wordCount");
  var maxLength = 500;
  var currentLength = textarea.value.length;

  countDisplay.textContent = currentLength + "/" + maxLength;

  if (currentLength > maxLength) {
    countDisplay.style.color = "red";
  } else {
    countDisplay.style.color = "black";
  }
}
