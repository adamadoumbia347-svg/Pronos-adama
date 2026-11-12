/* Parents Sereins — liens d'affiliation et menu mobile */
(function () {
  var cfg = window.AFFILIATION || {};
  var boutiques = cfg.boutiques || { fr: { nom: "Amazon.fr", domaine: "amazon.fr", tag: "" } };

  // Boutique du visiteur : pays du navigateur, sinon Amazon.fr.
  function boutiqueDuVisiteur() {
    var defaut = boutiques.fr ? "fr" : Object.keys(boutiques)[0];
    var langues = navigator.languages || [navigator.language || ""];
    for (var i = 0; i < langues.length; i++) {
      var pays = (langues[i].split("-")[1] || "").toUpperCase();
      if (!pays) continue;
      var code = (cfg.boutiqueParPays || {})[pays];
      if (code && boutiques[code] && boutiques[code].tag) return code;
      if ((cfg.europe || []).indexOf(pays) !== -1) return defaut;
    }
    return defaut;
  }

  var code = boutiqueDuVisiteur();
  function construireLiens(racine) {
    var b = boutiques[code];
    var perso = (cfg.liensPersonnalises || {})[code] || {};
    (racine || document).querySelectorAll("a.aff").forEach(function (a) {
      var id = a.getAttribute("data-aff");
      var q = a.getAttribute("data-q") || a.textContent.trim();
      var url = id && perso[id] ? perso[id]
        : "https://www." + b.domaine + "/s?k=" + encodeURIComponent(q) + (b.tag ? "&tag=" + encodeURIComponent(b.tag) : "");
      a.href = url;
      a.target = "_blank";
      a.rel = "sponsored nofollow noopener";
    });
  }
  construireLiens();
  window.lierProduits = construireLiens;

  // Menu mobile
  var burger = document.querySelector(".burger");
  var menu = document.querySelector("nav.menu");
  if (burger && menu) {
    burger.addEventListener("click", function () {
      var ouvert = menu.classList.toggle("ouvert");
      burger.setAttribute("aria-expanded", ouvert ? "true" : "false");
    });
  }

  // Année du pied de page
  document.querySelectorAll(".annee").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
