// Page « Peut-il manger… ? » : recherche d'un aliment et filtre par verdict
(function () {
  var champ = document.getElementById("cherche-aliment");
  if (!champ) return;
  var cartes = [].slice.call(document.querySelectorAll(".aliment"));
  var puces = [].slice.call(document.querySelectorAll(".chip[data-filtre]"));
  var aucun = document.querySelector(".aucun-aliment");
  var filtre = "";
  var sansAccent = function (s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
  function maj() {
    var q = sansAccent(champ.value.trim()), vus = 0;
    cartes.forEach(function (c) {
      var ok = (!q || sansAccent(c.getAttribute("data-nom")).indexOf(q) !== -1) &&
               (!filtre || c.getAttribute("data-verdicts").split(" ").indexOf(filtre) !== -1);
      c.hidden = !ok; if (ok) vus++;
    });
    aucun.hidden = vus > 0;
  }
  champ.addEventListener("input", maj);
  puces.forEach(function (b) {
    b.addEventListener("click", function () {
      filtre = b.getAttribute("data-filtre");
      puces.forEach(function (x) { x.classList.toggle("actif", x === b); x.setAttribute("aria-pressed", x === b); });
      maj();
    });
  });
  // Lien direct vers un aliment (#banane) : on le met en évidence
  if (location.hash) { var c = document.getElementById(location.hash.slice(1)); if (c) c.classList.add("cible"); }
})();
