// Pages trajets : affiche le prix aller-retour le plus bas repéré récemment pour les 3 prochains mois.
// Les données viennent de /api/prix (Travelpayouts). Sans réponse, la section reste masquée.
(function () {
  "use strict";
  var box = document.getElementById("route-prices");
  if (!box) return;
  var from = box.getAttribute("data-from"), to = box.getAttribute("data-to");
  var heroPrice = document.getElementById("hero-price");

  var now = new Date(), months = [];
  for (var i = 0; i < 3; i++) {
    var d = new Date(now.getFullYear(), now.getMonth() + i, 1);
    months.push(d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-01");
  }
  var label = function (iso) {
    var p = iso.split("-");
    return new Date(+p[0], +p[1] - 1, 1).toLocaleDateString("fr-FR", { month: "long", year: "numeric" });
  };
  var day = function (iso) {
    return iso ? new Date(iso).toLocaleDateString("fr-FR", { day: "numeric", month: "short" }) : "";
  };
  var esc = function (t) {
    return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  };

  Promise.all(months.map(function (m) {
    return fetch("/api/prix?from=" + from + "&to=" + to + "&dep=" + m + "&rt=1")
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; })
      .then(function (d) { return { month: m, data: d }; });
  })).then(function (rows) {
    var today = new Date().toISOString().slice(0, 10);
    var found = rows.filter(function (r) {
      return r.data && r.data.available && r.data.price && (r.data.departure_at || "").slice(0, 10) >= today;
    });
    if (!found.length) return;
    var best = Math.min.apply(null, found.map(function (r) { return r.data.price; }));
    if (heroPrice) {
      heroPrice.innerHTML = "Aller-retour repéré dès <strong>" + Math.round(best) + " €</strong>";
      heroPrice.hidden = false;
    }
    var list = found.map(function (r) {
      var d = r.data, dep = (d.departure_at || "").slice(0, 10), ret = (d.return_at || "").slice(0, 10);
      var stops = d.transfers === 0 ? "vol direct" : d.transfers === 1 ? "1 escale" : d.transfers + " escales";
      var href = "/?type=vols&from=" + from + "&to=" + to + (dep ? "&dep=" + dep : "") + (ret ? "&ret=" + ret : "");
      var cheapest = d.price === best ? ' <span class="pill-best">Le moins cher</span>' : "";
      return '<li class="price-row"><div><span class="price-month">' + esc(label(r.month)) + cheapest + "</span>" +
        '<span class="price-meta">' + esc(dep ? day(dep) + (ret ? " → " + day(ret) : "") + " · " + stops : stops) + "</span></div>" +
        '<strong class="price-val">dès ' + Math.round(d.price) + " €</strong>" +
        '<a class="price-go" href="' + esc(href) + '">Voir ces dates</a></li>';
    }).join("");
    box.querySelector(".price-list").innerHTML = list;
    box.hidden = false;
  });
})();
