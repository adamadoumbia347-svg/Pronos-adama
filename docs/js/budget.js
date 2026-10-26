// Calculateur de budget : additionne uniquement les montants saisis (gardés sur l'appareil)
(function () {
  var bloc = document.getElementById("calc-budget");
  if (!bloc) return;
  var CLE = "budget-animal";
  var champs = [].slice.call(bloc.querySelectorAll("input[data-periode]"));
  var lire = function () { try { return JSON.parse(localStorage.getItem(CLE)) || {}; } catch (e) { return {}; } };
  var ecrire = function (o) { try { localStorage.setItem(CLE, JSON.stringify(o)); } catch (e) {} };
  var euros = function (x) { return Math.round(x).toLocaleString(document.documentElement.lang || "fr") + " €"; };
  var etat = lire();
  function espece() { return bloc.querySelector("input[name=b-espece]:checked").value; }
  function calculer() {
    var e = espece(), mois = 0, an = 0, unique = 0;
    bloc.querySelectorAll(".poste").forEach(function (p) {
      var actif = p.getAttribute("data-especes").indexOf(e) !== -1;
      p.hidden = !actif;
      var i = p.querySelector("input"), v = parseFloat(i.value) || 0;
      if (!actif || v < 0) return;
      var per = i.getAttribute("data-periode");
      if (per === "mois") mois += v; else if (per === "an") an += v; else unique += v;
    });
    var total = mois * 12 + an;
    document.getElementById("t-mois").textContent = euros(total / 12);
    document.getElementById("t-an").textContent = euros(total);
    document.getElementById("t-premiere").textContent = euros(total + unique);
    var o = { espece: e }; champs.forEach(function (c) { if (c.value) o[c.id] = c.value; }); ecrire(o);
  }
  champs.forEach(function (c) { if (etat[c.id]) c.value = etat[c.id]; c.addEventListener("input", calculer); });
  if (etat.espece) { var r = bloc.querySelector('input[name=b-espece][value="' + etat.espece + '"]'); if (r) r.checked = true; }
  bloc.querySelectorAll("input[name=b-espece]").forEach(function (r) { r.addEventListener("change", calculer); });
  calculer();
})();
