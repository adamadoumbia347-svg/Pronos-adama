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

/* ---------- 4. Calendrier de diversification ---------- */
(function () {
  var form = document.getElementById("form-diversif");
  if (!form) return;
  // Repères du Programme national nutrition santé (« Pas à pas, votre enfant mange comme un grand ») et de la Société française de pédiatrie.
  var ETAPES = [
    { max: 3, titre: "Lait uniquement", liste: ["Lait maternel ou lait infantile 1er âge, à la demande.", "Aucun autre aliment ni eau sucrée ou tisane avant 4 mois."], ensuite: "Entre 4 et 6 mois révolus : premières cuillères de légumes et de fruits." },
    { max: 5, titre: "Les premières cuillères (si bébé est prêt)", liste: ["Légumes cuits et mixés lisses, un à la fois : carotte, courgette, haricot vert, potiron…", "Fruits cuits mixés : pomme, poire, banane écrasée.", "Féculents mixés : pomme de terre, petites pâtes ou semoule.", "Les allergènes (œuf bien cuit, arachide en poudre ou purée lisse, gluten, poisson) peuvent être introduits dès le début, sans attendre.", "Le lait reste l'aliment principal (au moins 500 ml par jour)."], ensuite: "À 6 mois : viande, poisson ou œuf, 10 g par jour." },
    { max: 7, titre: "On élargit", liste: ["Viande, poisson ou œuf dur : <strong>10 g par jour</strong> (2 cuillères à café, ou ¼ d'œuf dur).", "Une cuillère à café d'huile (colza, noix) ou une noisette de beurre dans les purées.", "Laitages : yaourt nature, petit-suisse, fromages pasteurisés.", "Texture : mixée, puis moulinée avec de petits grumeaux."], ensuite: "Vers 8 mois : 20 g de protéines et des petits morceaux fondants." },
    { max: 11, titre: "Les morceaux", liste: ["Viande, poisson ou œuf : <strong>20 g par jour</strong> (4 cuillères à café, ou ½ œuf).", "Petits morceaux fondants que bébé attrape avec les doigts : légumes bien cuits, pâtes, fruits mûrs.", "Légumineuses (lentilles, pois chiches) bien cuites et écrasées.", "4 repas par jour, dont un goûter."], ensuite: "À 1 an : il mange presque comme vous, en adaptant." },
    { max: 36, titre: "Il mange comme un grand (ou presque)", liste: ["Viande, poisson ou œuf : <strong>30 g par jour</strong> (6 cuillères à café, ou ½ gros œuf).", "Lait de croissance conseillé jusqu'à 3 ans (environ 500 ml par jour avec les laitages).", "Repas à table avec la famille, morceaux coupés petits.", "Toujours peu de sel et pas de boissons sucrées."], ensuite: null }
  ];
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var n = new Date(document.getElementById("d-naissance").value), a = new Date();
    var r = document.getElementById("res-diversif");
    if (isNaN(n)) return;
    var m = (a.getFullYear() - n.getFullYear()) * 12 + (a.getMonth() - n.getMonth()) - (a.getDate() < n.getDate() ? 1 : 0);
    if (m < 0 || m > 36) { r.innerHTML = "Ce calendrier concerne les enfants de 0 à 3 ans."; r.classList.add("visible"); return; }
    var t = ETAPES.filter(function (x) { return m <= x.max; })[0];
    r.innerHTML = "<p><strong>À " + m + " mois : " + t.titre + "</strong></p><ul><li>" + t.liste.join("</li><li>") + "</li></ul>" +
      (t.ensuite ? "<p>➡️ <strong>Prochaine étape :</strong> " + t.ensuite + "</p>" : "") +
      "<p>⚠️ <strong>Toujours avant 1 an :</strong> pas de miel, pas de sel ni de sucre ajouté, pas de lait de vache en boisson. Avant 5 ans : pas de fruits à coque entiers, raisins et tomates cerises coupés en 4.</p>";
    r.classList.add("visible");
  });
})();

/* ---------- 5. Budget de la première année ---------- */
(function () {
  var form = document.getElementById("form-budget");
  if (!form) return;
  // Estimations moyennes en euros, prix constatés en France en 2026. Hors frais de garde.
  var POSTES = {
    lait: { allaitement: 150, infantile: 750 },          // allaitement : tire-lait, coussinets…
    couches: { jetables: 650, lavables: 450 },
    equipement: { neuf: 1600, mixte: 1000, occasion: 550 },
    vetements: { neuf: 500, mixte: 300, occasion: 150 }
  };
  var FIXES = { "Repas après la diversification (petits pots ou fait maison)": 350, "Toilette, soins et pharmacie": 200, "Jouets et livres d'éveil": 150 };
  function euros(x) { return x.toLocaleString("fr-FR") + " €"; }
  form.addEventListener("change", calcul);
  form.addEventListener("submit", function (e) { e.preventDefault(); calcul(); });
  function val(nom) { var c = form.querySelector("input[name=" + nom + "]:checked"); return c ? c.value : null; }
  function calcul() {
    var achat = val("achat");
    var lignes = [
      ["Lait (" + (val("lait") === "allaitement" ? "allaitement : accessoires" : "lait infantile") + ")", POSTES.lait[val("lait")]],
      ["Couches " + val("couches"), POSTES.couches[val("couches")]],
      ["Équipement (lit, poussette, siège-auto, chaise haute…)", POSTES.equipement[achat]],
      ["Vêtements", POSTES.vetements[achat]]
    ];
    Object.keys(FIXES).forEach(function (k) { lignes.push([k, FIXES[k]]); });
    var total = lignes.reduce(function (s, l) { return s + l[1]; }, 0);
    var r = document.getElementById("res-budget");
    r.innerHTML = "<div class='tableau'><table>" + lignes.map(function (l) { return "<tr><td>" + l[0] + "</td><td style='text-align:right;white-space:nowrap'>" + euros(l[1]) + "</td></tr>"; }).join("") +
      "<tr><th>Total estimé sur 12 mois</th><th style='text-align:right;white-space:nowrap'>" + euros(total) + "</th></tr></table></div>" +
      "<p>Soit environ <strong>" + euros(Math.round(total / 12)) + " par mois</strong>, hors frais de garde. Pensez à vérifier vos droits à la prime à la naissance et à l'allocation de base (PAJE) sur caf.fr.</p>";
    r.classList.add("visible");
  }
})();

/* ---------- 6. Tableau de routine à imprimer ---------- */
(function () {
  var zone = document.getElementById("routine-choix");
  if (!zone) return;
  var ROUTINES = {
    matin: ["⏰ Je me lève", "🚽 Je vais aux toilettes", "🥣 Je prends mon petit-déjeuner", "👕 Je m'habille", "🪥 Je me brosse les dents", "💇 Je me coiffe", "🧥 Je mets mes chaussures et mon manteau", "🎒 Je prends mon cartable"],
    soir: ["🍽️ Je dîne", "🛁 Je prends mon bain", "🩳 Je mets mon pyjama", "🪥 Je me brosse les dents", "🚽 Je vais aux toilettes", "🎒 Je prépare mes affaires pour demain", "📖 On lit une histoire", "🤗 Câlin et au lit"]
  };
  var moment = document.getElementById("routine-moment");
  var prenom = document.getElementById("routine-prenom");
  var apercu = document.getElementById("routine-apercu");
  function remplir() {
    zone.innerHTML = ROUTINES[moment.value].map(function (t, i) {
      return "<li><label><input type='checkbox' checked data-t='" + t.replace(/'/g, "&#39;") + "'><span>" + t + "</span></label></li>";
    }).join("");
    dessiner();
  }
  function dessiner() {
    var choisis = Array.prototype.filter.call(zone.querySelectorAll("input"), function (c) { return c.checked; });
    var nom = prenom.value.trim();
    var titre = (moment.value === "matin" ? "☀️ Ma routine du matin" : "🌙 Ma routine du soir") + (nom ? " — " + nom.replace(/[<>&]/g, "") : "");
    apercu.innerHTML = "<h2>" + titre + "</h2><ol class='routine'>" + choisis.map(function (c) {
      var t = c.getAttribute("data-t"), i = t.indexOf(" ");
      return "<li><span class='r-ico'>" + t.slice(0, i) + "</span><span class='r-txt'>" + t.slice(i + 1) + "</span><span class='r-case'></span></li>";
    }).join("") + "</ol>";
  }
  moment.addEventListener("change", remplir);
  prenom.addEventListener("input", dessiner);
  zone.addEventListener("change", dessiner);
  document.getElementById("routine-imprimer").addEventListener("click", function () { window.print(); });
  remplir();
})();

/* ---------- 7. Recherche dans les articles ---------- */
(function () {
  var champ = document.getElementById("recherche");
  if (!champ) return;
  var cartes = document.querySelectorAll("[data-recherche]");
  var vide = document.getElementById("recherche-vide");
  function norm(s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function filtrer() {
    var mots = norm(champ.value).split(/\s+/).filter(Boolean), n = 0;
    cartes.forEach(function (c) {
      var texte = norm(c.textContent + " " + c.getAttribute("data-recherche"));
      var ok = mots.every(function (m) { return texte.indexOf(m) !== -1; });
      c.style.display = ok ? "" : "none";
      if (ok) n++;
    });
    document.querySelectorAll(".groupe-conseils").forEach(function (g) {
      g.style.display = g.querySelector("[data-recherche]:not([style*='none'])") ? "" : "none";
    });
    if (vide) vide.style.display = n ? "none" : "block";
  }
  champ.addEventListener("input", filtrer);
  var q = new URLSearchParams(location.search).get("q");
  if (q) { champ.value = q; }
  filtrer();
})();

/* ---------- 8. Idée d'activité au hasard ---------- */
(function () {
  var btn = document.getElementById("idee-tirer");
  if (!btn) return;
  var IDEES = {
    petit: [["🫘", "Transvaser des pâtes avec une cuillère (sous surveillance)"], ["🎨", "Peindre à l'eau sur un tableau noir"], ["🏕️", "Construire une cabane sous la table"], ["🛁", "Bac d'eau tiède, gobelets et éponges"], ["📚", "Mimer les animaux d'un imagier"], ["🧦", "Trier les chaussettes par couleur"], ["🎵", "Faire de la musique avec des casseroles"], ["🫧", "Faire des bulles de savon"]],
    moyen: [["🗺️", "Chasse au trésor avec des indices en dessins"], ["🥞", "Cuisiner des crêpes ensemble"], ["🛋️", "Parcours de motricité avec les coussins"], ["✂️", "Collage avec de vieux magazines"], ["🧦", "Spectacle de marionnettes-chaussettes"], ["📦", "Construire une ville en cartons"], ["💃", "Jacques a dit… en musique"], ["🌱", "Planter des lentilles dans du coton"]],
    grand: [["🌋", "Volcan bicarbonate + vinaigre"], ["💬", "Écrire et dessiner sa propre BD"], ["✈️", "Concours d'avions en papier"], ["🧱", "Défi : le pont le plus long en briques"], ["🍝", "Cuisiner un vrai repas en suivant la recette"], ["🔍", "Préparer un jeu de piste pour les parents"], ["🧪", "Fabriquer du slime"], ["🎬", "Tourner un mini-film d'animation en pâte à modeler"]],
    famille: [["🎲", "Soirée jeux de société, sans écran"], ["🧺", "Pique-nique dans le salon"], ["🎤", "Karaoké en famille"], ["📸", "Décorer un album photo ensemble"], ["🧁", "Atelier pâtisserie"], ["📖", "Lecture partagée : chacun lit une page"], ["🧹", "Grand rangement en musique, chronométré"], ["🔢", "Loto maison avec des petits lots"]]
  };
  var carte = document.getElementById("idee-carte"), derniere = -1;
  btn.addEventListener("click", function () {
    var age = (document.querySelector("input[name=idee-age]:checked") || {}).value || "petit";
    var l = IDEES[age], i;
    do { i = Math.floor(Math.random() * l.length); } while (i === derniere && l.length > 1);
    derniere = i;
    carte.classList.remove("tourne"); void carte.offsetWidth; carte.classList.add("tourne");
    setTimeout(function () { carte.querySelector(".face").innerHTML = "<div><span class='em'>" + l[i][0] + "</span>" + l[i][1] + "</div>"; }, 300);
  });
})();

/* ---------- 9. Argent de poche ---------- */
(function () {
  var form = document.getElementById("form-argent");
  if (!form) return;
  var REPERES = [
    { max: 7, montant: "1 à 2 € par semaine", conseil: "Une petite somme hebdomadaire, dans une tirelire transparente : il voit l'argent s'accumuler. Idéal pour apprendre à compter et à attendre." },
    { max: 10, montant: "2 à 5 € par semaine", conseil: "Il peut payer lui-même ses petits plaisirs (cartes, magazines). Laissez-le se tromper sur de petites sommes : c'est comme ça qu'il apprend." },
    { max: 13, montant: "15 à 25 € par mois", conseil: "Passez à un versement mensuel pour apprendre à gérer sur la durée. Fixez ensemble ce qu'il paie lui-même (sorties, cadeaux aux copains…)." },
    { max: 17, montant: "25 à 50 € par mois", conseil: "Une carte bancaire pour mineurs avec plafond peut l'aider à suivre ses dépenses. Plus il paie de choses lui-même (forfait, vêtements), plus le montant peut monter." }
  ];
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var age = parseInt(document.getElementById("a-age").value, 10), r = document.getElementById("res-argent");
    if (isNaN(age)) return;
    if (age < 6) { r.innerHTML = "<p>Avant 6 ans, l'argent de poche n'est pas nécessaire : jouez plutôt à la marchande pour découvrir les pièces et les billets.</p>"; r.classList.add("visible"); return; }
    var t = REPERES.filter(function (x) { return age <= x.max; })[0];
    r.innerHTML = "<p><strong>À " + age + " ans : " + t.montant + "</strong> (fourchette courante).</p><p>💡 " + t.conseil + "</p>" +
      "<p>👉 L'argent de poche ne devrait pas servir de punition ou de récompense aux notes : il sert à apprendre à gérer.</p>";
    r.classList.add("visible");
  });
})();
