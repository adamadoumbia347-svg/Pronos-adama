/* Parents Sereins — outils interactifs (sommeil, écrans, liste de naissance) */
(function () {
  function $(id) { return document.getElementById(id); }
  function ageEnMois(dateNaissance) {
    var n = new Date(dateNaissance), a = new Date();
    if (isNaN(n)) return null;
    var m = (a.getFullYear() - n.getFullYear()) * 12 + (a.getMonth() - n.getMonth());
    if (a.getDate() < n.getDate()) m--;
    return m;
  }
  function libelleAge(m) {
    if (m < 24) return m + " mois";
    var ans = Math.floor(m / 12);
    return ans + " an" + (ans > 1 ? "s" : "");
  }
  function heure(min) {
    min = ((min % 1440) + 1440) % 1440;
    var h = Math.floor(min / 60), mm = min % 60;
    return h + "h" + (mm < 10 ? "0" : "") + mm;
  }

  /* ---------- 1. Calculateur de sommeil ---------- */
  // Repères de l'Académie américaine de médecine du sommeil et de la National Sleep Foundation.
  var SOMMEIL = [
    { max: 3, total: "14 à 17 h", nuit: null, siestes: "Nombreuses : bébé dort par cycles de 2 à 4 h, jour et nuit", conseil: "Pas encore de rythme jour/nuit : c'est normal. Exposez-le à la lumière le jour, gardez la nuit sombre et calme." },
    { max: 11, total: "12 à 16 h", nuit: 11 * 60, siestes: "2 à 3 siestes (environ 3 h au total)", conseil: "Un rituel court et toujours identique (bain, pyjama, histoire, câlin) aide bébé à repérer l'heure du dodo." },
    { max: 35, total: "11 à 14 h", nuit: 11 * 60, siestes: "1 à 2 siestes (1 h 30 à 3 h), une seule vers 15-18 mois", conseil: "Gardez la sieste de début d'après-midi ; ne la faites pas finir trop tard (après 16 h) pour ne pas retarder le coucher." },
    { max: 71, total: "10 à 13 h", nuit: 10 * 60 + 45, siestes: "0 à 1 sieste ; un temps calme suffit souvent après 4 ans", conseil: "Pas d'écran dans l'heure qui précède le coucher : la lumière et l'excitation retardent l'endormissement." },
    { max: 155, total: "9 à 12 h", nuit: 10 * 60, siestes: "Aucune", conseil: "Même heure de coucher la semaine ; le week-end, pas plus d'une heure de décalage." },
    { max: 227, total: "8 à 10 h", nuit: 9 * 60, siestes: "Aucune", conseil: "À l'adolescence l'horloge interne se décale : le téléphone hors de la chambre la nuit fait une vraie différence." }
  ];
  var formS = $("form-sommeil");
  if (formS) {
    formS.addEventListener("submit", function (e) {
      e.preventDefault();
      var m = ageEnMois($("s-naissance").value);
      var r = $("res-sommeil");
      if (m === null || m < 0) { r.innerHTML = "Indiquez une date de naissance valide."; r.classList.add("visible"); return; }
      if (m > 227) { r.innerHTML = "Ce calculateur s'adresse aux enfants de 0 à 18 ans."; r.classList.add("visible"); return; }
      var t = SOMMEIL.filter(function (x) { return m <= x.max; })[0];
      var reveil = $("s-reveil").value.split(":");
      var minReveil = parseInt(reveil[0], 10) * 60 + parseInt(reveil[1] || 0, 10);
      var html = "<p><strong>À " + libelleAge(m) + "</strong>, un enfant a besoin de <strong>" + t.total + "</strong> de sommeil par 24 h.</p>" +
        "<p><strong>Siestes :</strong> " + t.siestes + ".</p>";
      if (t.nuit && !isNaN(minReveil)) {
        html += "<p><strong>Heure de coucher conseillée</strong> pour un réveil à " + heure(minReveil) + " : <strong>vers " +
          heure(minReveil - t.nuit) + "</strong> (endormi, pas seulement au lit).</p>";
      }
      html += "<p>💡 " + t.conseil + "</p>";
      r.innerHTML = html;
      r.classList.add("visible");
    });
  }

  /* ---------- 2. Repères écrans ---------- */
  // Repères de la commission d'experts « Enfants et écrans » (rapport remis à l'Élysée, 2024) et de l'OMS.
  var ECRANS = [
    { max: 35, titre: "Avant 3 ans : pas d'écran", texte: "Ni télévision, ni tablette, ni téléphone, même « éducatifs ». Le cerveau apprend par le jeu, la manipulation et les échanges en face à face. Les appels vidéo avec la famille sont une exception acceptée.", idees: "Livres cartonnés, jeux d'éveil, cubes, comptines." },
    { max: 71, titre: "De 3 à 6 ans : occasionnel et accompagné", texte: "Des contenus adaptés, de qualité, toujours avec un adulte qui commente. Pas d'écran le matin avant l'école, pendant les repas, ni avant de dormir. Pas de tablette ou de téléphone personnels.", idees: "Puzzles, jeux de société simples, pâte à modeler, conteuse audio sans écran." },
    { max: 131, titre: "De 6 à 11 ans : modéré et encadré", texte: "Des temps d'écran définis à l'avance (par exemple le mercredi et le week-end), des contenus choisis ensemble. Pas de téléphone personnel avant 11 ans ; pas d'écran dans la chambre.", idees: "Jeux de société, kits créatifs et scientifiques, BD, sport." },
    { max: 179, titre: "De 11 à 15 ans : téléphone sans internet, puis progressif", texte: "Un premier téléphone sans accès à internet est recommandé jusqu'à 13 ans, puis un smartphone sans réseaux sociaux jusqu'à 15 ans. Les écrans restent hors de la chambre la nuit.", idees: "Réveil classique (pour sortir le téléphone de la chambre), livres, activités de groupe." },
    { max: 227, titre: "Après 15 ans : autonomie accompagnée", texte: "Accès aux réseaux sociaux « éthiques » possible. Parlez des contenus, du cyberharcèlement et du temps passé, plutôt que d'interdire. Montrez l'exemple : le téléphone des parents compte aussi.", idees: "Réveil classique, chargeur dans le salon la nuit." }
  ];
  var formE = $("form-ecrans");
  if (formE) {
    formE.addEventListener("submit", function (e) {
      e.preventDefault();
      var ans = parseInt($("e-age").value, 10);
      var r = $("res-ecrans");
      if (isNaN(ans)) return;
      var t = ECRANS.filter(function (x) { return ans * 12 <= x.max; })[0] || ECRANS[ECRANS.length - 1];
      r.innerHTML = "<p><strong>" + t.titre + "</strong></p><p>" + t.texte + "</p><p>🧸 <strong>À la place :</strong> " + t.idees + "</p>";
      r.classList.add("visible");
    });
  }

  /* ---------- 3. Liste de naissance (enregistrée dans ce navigateur) ---------- */
  var liste = $("liste-naissance");
  if (liste) {
    var CLE = "parents-sereins-liste";
    var coches = {};
    try { coches = JSON.parse(localStorage.getItem(CLE) || "{}"); } catch (err) { coches = {}; }
    var cases = liste.querySelectorAll("input[type=checkbox]");
    function maj() {
      var n = 0;
      cases.forEach(function (c) {
        c.parentNode.querySelector("span").classList.toggle("fait", c.checked);
        if (c.checked) n++;
      });
      $("liste-compte").textContent = n + " / " + cases.length;
      $("liste-barre").style.width = (cases.length ? n / cases.length * 100 : 0) + "%";
    }
    cases.forEach(function (c) {
      c.checked = !!coches[c.id];
      c.addEventListener("change", function () {
        coches[c.id] = c.checked;
        try { localStorage.setItem(CLE, JSON.stringify(coches)); } catch (err) { /* navigation privée */ }
        maj();
      });
    });
    maj();
    var raz = $("liste-raz");
    if (raz) raz.addEventListener("click", function () {
      coches = {};
      try { localStorage.removeItem(CLE); } catch (err) {}
      cases.forEach(function (c) { c.checked = false; });
      maj();
    });
  }
})();
