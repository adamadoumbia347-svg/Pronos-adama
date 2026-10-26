// Quiz « Quel animal pour moi ? » : 6 questions, points par profil, résultat avec le profil le mieux noté
(function () {
  var bloc = document.getElementById("quel-animal");
  if (!bloc) return;
  var D = JSON.parse(document.getElementById("donnees-quel-animal").textContent);
  var zone = bloc.querySelector(".qa-zone"), etape = 0, choix = [];
  var L = {
    fr: { q: "Question ", sur: " sur ", prec: "← Question précédente", guide: "Lire notre guide", autre: "Autre possibilité : ", plus: "En savoir plus", again: "↺ Recommencer le quiz" },
    en: { q: "Question ", sur: " of ", prec: "← Previous question", guide: "Read our guide", autre: "Another option: ", plus: "Find out more", again: "↺ Take the quiz again" },
    it: { q: "Domanda ", sur: " di ", prec: "← Domanda precedente", guide: "Leggi la nostra guida", autre: "Un'altra possibilità: ", plus: "Scopri di più", again: "↺ Rifai il quiz" }
  }[document.documentElement.lang] || null;
  if (!L) L = { q: "Question ", sur: " sur ", prec: "← Question précédente", guide: "Lire notre guide", autre: "Autre possibilité : ", plus: "En savoir plus", again: "↺ Recommencer le quiz" };
  var esc = function (s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  function afficher() {
    var q = D.q[etape];
    zone.innerHTML = '<p class="quiz-etape">' + L.q + (etape + 1) + L.sur + D.q.length + '</p><div class="quiz-barre"><i style="width:' + (etape / D.q.length * 100) + '%"></i></div>' +
      "<h2>" + esc(q.t) + '</h2><div class="quiz-options">' +
      q.r.map(function (r, i) { return '<button type="button" class="quiz-choix" data-i="' + i + '">' + esc(r.t) + "</button>"; }).join("") + "</div>" +
      (etape > 0 ? '<button type="button" class="quiz-retour">' + L.prec + "</button>" : "");
    zone.querySelectorAll(".quiz-choix").forEach(function (b) {
      b.addEventListener("click", function () {
        choix[etape] = +b.getAttribute("data-i"); etape++;
        etape < D.q.length ? afficher() : resultat();
      });
    });
    var r = zone.querySelector(".quiz-retour");
    if (r) r.addEventListener("click", function () { etape--; afficher(); });
  }
  function resultat() {
    var score = D.res.map(function () { return 0; });
    choix.forEach(function (c, i) { D.q[i].r[c].p.forEach(function (p, k) { score[k] += p; }); });
    var ordre = score.map(function (s, k) { return k; }).sort(function (a, b) { return score[b] - score[a]; });
    var top = D.res[ordre[0]], deux = D.res[ordre[1]];
    zone.innerHTML = '<div class="quiz-barre"><i style="width:100%"></i></div><h2>🎯 ' + esc(top.t) + "</h2><p>" + esc(top.d) + "</p>" +
      '<p><a class="btn btn-sm" href="' + top.l + '">' + L.guide + "</a></p>" +
      '<p class="muted">' + L.autre + "<strong>" + esc(deux.t) + '</strong>. <a href="' + deux.l + '">' + L.plus + "</a></p>" +
      '<button type="button" class="quiz-retour">' + L.again + "</button>";
    zone.querySelector(".quiz-retour").addEventListener("click", function () { etape = 0; choix = []; afficher(); });
  }
  afficher();
})();
