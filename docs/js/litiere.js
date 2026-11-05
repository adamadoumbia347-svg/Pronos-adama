/* Calculateur du coût mensuel de la litière (FR / EN / IT) : prix du sac et durée → coût par mois, pour 2 litières. */
(function () {
  var box = document.getElementById("calcul-litiere");
  if (!box) return;
  var T = {
    fr: {a: "Litière A", b: "Litière B", prix: "Prix du sac", duree: "Un sac dure (semaines)", mois: "par mois", an: "par an",
         moins: "La litière {x} revient moins cher : {d} d'économie par mois.", egal: "Les deux litières coûtent autant par mois.", vide: "Indiquez le prix et la durée de chaque litière."},
    en: {a: "Litter A", b: "Litter B", prix: "Price per bag", duree: "One bag lasts (weeks)", mois: "per month", an: "per year",
         moins: "Litter {x} is cheaper: you save {d} per month.", egal: "Both litters cost the same per month.", vide: "Enter the price and how long each litter lasts."},
    it: {a: "Lettiera A", b: "Lettiera B", prix: "Prezzo del sacco", duree: "Un sacco dura (settimane)", mois: "al mese", an: "all'anno",
         moins: "La lettiera {x} costa meno: risparmi {d} al mese.", egal: "Le due lettiere costano uguale al mese.", vide: "Inserisci il prezzo e la durata di ogni lettiera."}
  };
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var t = T[lang] || T.fr;
  var fmt = function (n) { return n.toLocaleString(lang, {minimumFractionDigits: 2, maximumFractionDigits: 2}); };
  var col = function (k, nom) {
    return '<div class="calc-col"><h3>' + nom + '</h3>' +
      '<label>' + t.prix + ' <input type="number" min="0" step="0.01" inputmode="decimal" id="lit-prix-' + k + '"></label>' +
      '<label>' + t.duree + ' <input type="number" min="0.5" step="0.5" inputmode="decimal" id="lit-duree-' + k + '"></label>' +
      '<p class="calc-res" id="lit-res-' + k + '" aria-live="polite"></p></div>';
  };
  box.innerHTML = '<div class="calc-cols">' + col("a", t.a) + col("b", t.b) + '</div><p class="calc-verdict" id="lit-verdict" aria-live="polite">' + t.vide + '</p>';
  var SEMAINES_PAR_MOIS = 52 / 12;
  function cout(k) {
    var p = parseFloat(document.getElementById("lit-prix-" + k).value);
    var s = parseFloat(document.getElementById("lit-duree-" + k).value);
    var res = document.getElementById("lit-res-" + k);
    if (!(p > 0) || !(s > 0)) { res.textContent = ""; return null; }
    var m = p / s * SEMAINES_PAR_MOIS;
    res.innerHTML = "<strong>" + fmt(m) + "</strong> " + t.mois + " · " + fmt(m * 12) + " " + t.an;
    return m;
  }
  function maj() {
    var a = cout("a"), b = cout("b"), v = document.getElementById("lit-verdict");
    if (a === null || b === null) { v.textContent = t.vide; return; }
    if (Math.abs(a - b) < 0.005) { v.textContent = t.egal; return; }
    v.textContent = t.moins.replace("{x}", a < b ? "A" : "B").replace("{d}", fmt(Math.abs(a - b)));
  }
  box.addEventListener("input", maj);
})();
