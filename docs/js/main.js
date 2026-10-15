(function () {
  var cfg = window.AFFILIATION || {};
  var tagValide = cfg.amazonTag && cfg.amazonTag !== "VOTRE-TAG-21";
  var domaine = cfg.amazonDomaine || "amazon.fr";
  var perso = cfg.liensPersonnalises || {};

  // Construit chaque lien produit : lien personnalisé si défini, sinon recherche Amazon taguée.
  document.querySelectorAll("a.aff").forEach(function (a) {
    var id = a.getAttribute("data-aff");
    var recherche = a.getAttribute("data-q") || a.textContent.trim();
    var url;
    if (id && perso[id]) {
      url = perso[id];
    } else {
      url = "https://www." + domaine + "/s?k=" + encodeURIComponent(recherche);
      if (tagValide) url += "&tag=" + encodeURIComponent(cfg.amazonTag);
    }
    a.href = url;
    a.target = "_blank";
    a.rel = "sponsored nofollow noopener";
  });

  // Menu mobile
  var bouton = document.querySelector(".nav-toggle");
  var menu = document.querySelector(".nav-links");
  if (bouton && menu) {
    bouton.addEventListener("click", function () {
      var ouvert = menu.classList.toggle("open");
      bouton.setAttribute("aria-expanded", ouvert ? "true" : "false");
    });
  }

  // Filtres du catalogue de méthodes
  var filtres = document.querySelectorAll("[data-filter-group]");
  var methodes = document.querySelectorAll(".method");
  var recherche = document.getElementById("method-search");
  var compteur = document.getElementById("method-count");
  var etat = { animal: "tous", niveau: "tous" };

  function appliquer() {
    var texte = recherche ? recherche.value.trim().toLowerCase() : "";
    var visibles = 0;
    methodes.forEach(function (m) {
      var animaux = (m.getAttribute("data-animals") || "").split(" ");
      var ok =
        (etat.animal === "tous" || animaux.indexOf(etat.animal) !== -1) &&
        (etat.niveau === "tous" || m.getAttribute("data-level") === etat.niveau) &&
        (!texte || m.textContent.toLowerCase().indexOf(texte) !== -1);
      m.hidden = !ok;
      if (ok) visibles++;
    });
    if (compteur) compteur.textContent = visibles + " méthode" + (visibles > 1 ? "s" : "");
  }

  filtres.forEach(function (groupe) {
    var cle = groupe.getAttribute("data-filter-group");
    groupe.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () {
        groupe.querySelectorAll("button").forEach(function (x) {
          x.setAttribute("aria-pressed", "false");
        });
        b.setAttribute("aria-pressed", "true");
        etat[cle] = b.getAttribute("data-value");
        appliquer();
      });
    });
  });
  if (recherche) recherche.addEventListener("input", appliquer);

  // Pré-filtre via l'URL : methodes.html?animal=chat
  var params = new URLSearchParams(location.search);
  var animalUrl = params.get("animal");
  if (animalUrl) {
    var b = document.querySelector('[data-filter-group="animal"] button[data-value="' + animalUrl + '"]');
    if (b) b.click();
  }
  if (methodes.length) appliquer();

  var annee = document.getElementById("annee");
  if (annee) annee.textContent = new Date().getFullYear();
})();
