/* Parents Sereins — « Mon espace » : profil des enfants, graines, niveaux, badges, série, défi du jour.
   Tout est enregistré uniquement dans le navigateur du visiteur (localStorage). */
(function () {
  function lire(cle, defaut) { try { var v = localStorage.getItem(cle); return v === null ? defaut : JSON.parse(v); } catch (e) { return defaut; } }
  function ecrire(cle, v) { try { localStorage.setItem(cle, JSON.stringify(v)); } catch (e) {} }
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function jour(d) { d = d || new Date(); return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); }
  function hier() { var d = new Date(); d.setDate(d.getDate() - 1); return jour(d); }
  var mouvementReduit = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  var etat = lire("ps-progres", null) || { graines: 0, actions: {}, compteurs: {}, outils: {}, badges: {}, serie: { n: 0, dernier: "", record: 0 }, defis: {}, bonus: "" };
  function sauver() { ecrire("ps-progres", etat); }
  // Une série non entretenue (dernier jour actif avant hier) retombe à 0
  if (etat.serie.dernier && etat.serie.dernier !== jour() && etat.serie.dernier !== hier()) { etat.serie.n = 0; sauver(); }

  /* ---------- Niveaux ---------- */
  var NIVEAUX = [
    { min: 0, nom: "Graine", ico: "🫘" }, { min: 30, nom: "Pousse", ico: "🌱" }, { min: 100, nom: "Bourgeon", ico: "🌿" },
    { min: 220, nom: "Fleur", ico: "🌷" }, { min: 400, nom: "Arbuste", ico: "🪴" }, { min: 700, nom: "Arbre", ico: "🌳" }, { min: 1100, nom: "Forêt", ico: "🏞️" }
  ];
  function niveau(g) {
    var i = 0; while (i + 1 < NIVEAUX.length && g >= NIVEAUX[i + 1].min) i++;
    var suivant = NIVEAUX[i + 1];
    return { i: i, n: NIVEAUX[i], suivant: suivant, pct: suivant ? (g - NIVEAUX[i].min) / (suivant.min - NIVEAUX[i].min) : 1 };
  }

  /* ---------- Badges ---------- */
  function c(k) { return etat.compteurs[k] || 0; }
  var BADGES = [
    { id: "famille", ico: "👨‍👩‍👧", nom: "Bienvenue !", desc: "Ajouter un enfant dans Mon espace", ok: function () { return (lire("ps-enfants", []) || []).length > 0; } },
    { id: "lecteur1", ico: "📖", nom: "Première lecture", desc: "Lire un article jusqu'au bout", ok: function () { return c("lecture") >= 1; } },
    { id: "lecteur5", ico: "📚", nom: "Curieux", desc: "Lire 5 articles", ok: function () { return c("lecture") >= 5; } },
    { id: "lecteur15", ico: "🎓", nom: "Parent encyclopédie", desc: "Lire 15 articles", ok: function () { return c("lecture") >= 15; } },
    { id: "serie3", ico: "🔥", nom: "Sur la lancée", desc: "Revenir 3 jours de suite", ok: function () { return etat.serie.record >= 3; } },
    { id: "serie7", ico: "⚡", nom: "Une semaine pile", desc: "Revenir 7 jours de suite", ok: function () { return etat.serie.record >= 7; } },
    { id: "serie30", ico: "🏆", nom: "Inarrêtable", desc: "Revenir 30 jours de suite", ok: function () { return etat.serie.record >= 30; } },
    { id: "defi1", ico: "🎯", nom: "Premier défi", desc: "Réussir un défi du jour", ok: function () { return c("defi") >= 1; } },
    { id: "defi10", ico: "🏅", nom: "Champion des défis", desc: "Réussir 10 défis du jour", ok: function () { return c("defi") >= 10; } },
    { id: "souvenir1", ico: "📸", nom: "Gardien des souvenirs", desc: "Noter un premier souvenir dans le journal", ok: function () { return c("souvenir") >= 1; } },
    { id: "souvenir10", ico: "💝", nom: "Album précieux", desc: "Noter 10 souvenirs", ok: function () { return c("souvenir") >= 10; } },
    { id: "conteur", ico: "🧚", nom: "Conteur du soir", desc: "Créer 3 histoires du soir", ok: function () { return c("histoire") >= 3; } },
    { id: "quiz", ico: "🧠", nom: "Sans faute", desc: "Faire 10/10 au quiz", ok: function () { return c("quiz_parfait") >= 1; } },
    { id: "prenoms", ico: "💘", nom: "Coups de cœur", desc: "Aimer 10 prénoms", ok: function () { return c("prenom") >= 10; } },
    { id: "explorateur", ico: "🧭", nom: "Explorateur", desc: "Utiliser 5 outils différents", ok: function () { return Object.keys(etat.outils).length >= 5; } },
    { id: "suivi", ico: "🍼", nom: "Bien organisé", desc: "Noter 10 moments dans le suivi de bébé", ok: function () { return c("suivi") >= 10; } },
    { id: "hibou", ico: "🦉", nom: "Veilleur de nuit", desc: "Passer sur le site entre minuit et 5 h (courage !)", ok: function () { return c("nuit") >= 1; } }
  ];

  /* ---------- Effets : graines flottantes, confettis, célébration ---------- */
  function flotter(texte) {
    var el = document.createElement("div");
    el.className = "graine-flottante"; el.textContent = texte;
    document.body.appendChild(el);
    setTimeout(function () { el.remove(); }, 1600);
  }
  function confettis() {
    if (mouvementReduit) return;
    var cv = document.createElement("canvas"); cv.className = "confettis";
    cv.width = innerWidth; cv.height = innerHeight; document.body.appendChild(cv);
    var ctx = cv.getContext("2d"), couleurs = ["#e8735a", "#2f8f84", "#ffcf5c", "#9b8cff", "#ff9ec4"], ps = [];
    for (var i = 0; i < 140; i++) ps.push({ x: innerWidth / 2, y: innerHeight / 2.4, vx: (Math.random() - .5) * 16, vy: Math.random() * -15 - 4, r: Math.random() * 6 + 4, c: couleurs[i % 5], a: Math.random() * 6, va: (Math.random() - .5) * .4 });
    var t = 0;
    (function anim() {
      ctx.clearRect(0, 0, cv.width, cv.height);
      ps.forEach(function (p) { p.vy += .45; p.vx *= .99; p.x += p.vx; p.y += p.vy; p.a += p.va;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.fillStyle = p.c; ctx.fillRect(-p.r / 2, -p.r / 4, p.r, p.r / 2); ctx.restore(); });
      if (++t < 150) requestAnimationFrame(anim); else cv.remove();
    })();
  }
  var fileCelebrations = [], celebrationOuverte = false;
  function celebrer(ico, titre, texte) {
    fileCelebrations.push([ico, titre, texte]);
    if (!celebrationOuverte) suivante();
  }
  function suivante() {
    var x = fileCelebrations.shift();
    if (!x) { celebrationOuverte = false; return; }
    celebrationOuverte = true;
    var m = document.createElement("div"); m.className = "celebration"; m.setAttribute("role", "dialog"); m.setAttribute("aria-modal", "true");
    m.innerHTML = '<div class="celebration-boite"><div class="celebration-ico">' + x[0] + '</div><h2>' + esc(x[1]) + '</h2><p>' + esc(x[2]) + '</p>' +
      '<p><a class="btn" href="mon-espace.html">Voir mes badges</a> <button class="btn clair" type="button">Continuer</button></p></div>';
    document.body.appendChild(m);
    confettis();
    function fermer() { m.classList.add("sort"); setTimeout(function () { m.remove(); suivante(); }, 300); }
    m.querySelector("button").addEventListener("click", fermer);
    m.addEventListener("click", function (e) { if (e.target === m) fermer(); });
    m.querySelector("button").focus();
  }

  function verifierBadges() {
    BADGES.forEach(function (b) {
      if (!etat.badges[b.id] && b.ok()) {
        etat.badges[b.id] = jour(); sauver();
        celebrer(b.ico, "Badge débloqué : " + b.nom, b.desc + ". Bravo !");
      }
    });
  }

  /* ---------- Série de jours ---------- */
  function marquerJourActif() {
    var a = jour();
    if (etat.serie.dernier === a) return;
    etat.serie.n = etat.serie.dernier === hier() ? etat.serie.n + 1 : 1;
    etat.serie.dernier = a;
    etat.serie.record = Math.max(etat.serie.record || 0, etat.serie.n);
    sauver();
  }

  /* ---------- Gagner des graines ---------- */
  // action : type de compteur ; cle : identifiant unique (une seule fois), ou null pour répétable
  function gagner(action, points, cle, discret) {
    if (cle) { if (etat.actions[cle]) return false; etat.actions[cle] = jour(); }
    var avant = niveau(etat.graines).i;
    etat.graines += points;
    etat.compteurs[action] = (etat.compteurs[action] || 0) + 1;
    marquerJourActif();
    sauver();
    if (!discret) flotter("+" + points + " 🌱");
    majPuce(true);
    var apres = niveau(etat.graines);
    if (apres.i > avant) celebrer(apres.n.ico, "Niveau " + apres.n.nom + " !", "Vous avez " + etat.graines + " graines. Votre jardin de parent grandit 🌱");
    verifierBadges();
    document.dispatchEvent(new CustomEvent("ps:progres"));
    return true;
  }

  /* ---------- Défi du jour et « le saviez-vous ? » ---------- */
  var DEFIS = [
    "Faire un câlin de 20 secondes à chaque enfant", "Dîner tous ensemble sans aucun écran sur la table", "Lire une histoire de plus que d'habitude ce soir",
    "Dire à votre enfant une qualité précise que vous aimez chez lui", "Jouer 15 minutes à SON jeu préféré, en le laissant diriger", "Danser ensemble sur une chanson qu'il choisit",
    "Sortir prendre l'air 30 minutes, même s'il fait gris", "Cuisiner quelque chose ensemble (même une simple tartine décorée)", "Poser la question : « Quel a été le meilleur moment de ta journée ? »",
    "Laisser votre enfant faire seul une chose que vous faites d'habitude à sa place", "Raconter un souvenir de quand vous étiez petit", "Faire une bataille de chatouilles (ou d'oreillers !)",
    "Ranger ensemble en musique, chrono lancé", "Remplacer un « non » par une proposition : « pas maintenant, mais après le bain »", "Regarder les étoiles ou la lune ensemble ce soir",
    "Écrire un petit mot doux et le glisser dans son cartable ou sous son oreiller", "Prendre 10 minutes rien que pour vous, sans culpabilité", "Faire un dessin à quatre mains",
    "Passer une heure sans téléphone quand vous êtes avec les enfants", "Chanter une comptine avec les gestes", "Inventer ensemble la fin d'une histoire connue",
    "Faire une photo souvenir et la noter dans le journal de bébé", "Remercier votre enfant pour quelque chose qu'il a fait aujourd'hui", "Jouer à « Jacques a dit » pendant 5 minutes",
    "Préparer ensemble les affaires du lendemain", "Proposer un choix plutôt qu'un ordre au moins 3 fois aujourd'hui", "Faire une cabane avec des draps et des coussins",
    "Appeler un grand-parent en famille", "Se coucher 30 minutes plus tôt que d'habitude (oui, vous aussi)", "Lui demander de vous apprendre quelque chose",
    "Faire un pique-nique (dehors ou sur le tapis du salon)", "Chuchoter toute une conversation, juste pour rire", "Faire une promenade où chacun ramasse un trésor naturel",
    "Prendre le goûter assis ensemble, sans se presser", "Raconter votre journée à votre enfant avec vos émotions (« j'étais fier quand… »)",
    "Tester une recette avec un légume qu'il n'aime pas… et goûter tous ensemble", "Faire un concours de grimaces", "Lire à voix haute une page d'un livre pour adultes… en voix rigolotes",
    "Construire la plus haute tour possible avec ce que vous avez", "Dire « je t'aime » sans raison particulière"
  ];
  var FAITS = [
    "Un nouveau-né voit net seulement à 20-30 cm : la distance de votre visage quand vous le tenez dans les bras.",
    "Les bébés naissent avec environ 300 os ; certains fusionnent en grandissant pour arriver à 206 chez l'adulte.",
    "Avant 3 ans, le cerveau d'un enfant crée plus d'un million de nouvelles connexions par seconde.",
    "Il faut parfois proposer un aliment 8 à 10 fois avant qu'un enfant l'accepte. Ne lâchez rien !",
    "Les enfants rient en moyenne beaucoup plus souvent que les adultes : profitez-en, c'est contagieux.",
    "Lire 15 minutes par jour à un enfant l'expose à des centaines de milliers de mots par an.",
    "Le sommeil profond est le moment où l'hormone de croissance est la plus sécrétée.",
    "Un bébé reconnaît la voix de sa mère dès la naissance : il l'entendait déjà dans le ventre.",
    "Les premières dents apparaissent en moyenne vers 6 mois, mais certains bébés naissent avec une dent !",
    "Le « non » vers 2 ans est une étape normale : l'enfant découvre qu'il est une personne à part entière.",
    "Les bébés ont plus de papilles gustatives que les adultes, y compris sur les joues et le palais.",
    "Jouer, c'est apprendre : la plupart des compétences des tout-petits se construisent dans le jeu libre.",
    "Les câlins libèrent de l'ocytocine, chez l'enfant comme chez le parent : un antistress naturel.",
    "Un enfant de 4 ans pose en moyenne plusieurs centaines de questions par jour. Courage !",
    "L'ennui est utile : c'est souvent quand il s'ennuie qu'un enfant invente ses propres jeux.",
    "Chanter des comptines aide les bébés à repérer les sons et le rythme de la langue."
  ];
  function indiceDuJour(n) { var d = new Date(), debut = new Date(d.getFullYear(), 0, 0); return Math.floor((d - debut) / 864e5) % n; }
  function defiDuJour() { return DEFIS[indiceDuJour(DEFIS.length)]; }
  function faitDuJour() { return FAITS[indiceDuJour(FAITS.length)]; }

  /* ---------- Enfants ---------- */
  function enfants() { return lire("ps-enfants", []) || []; }
  function ageMois(naissance) {
    var n = new Date(naissance), a = new Date();
    if (isNaN(n)) return null;
    var m = (a.getFullYear() - n.getFullYear()) * 12 + (a.getMonth() - n.getMonth());
    if (a.getDate() < n.getDate()) m--;
    return m;
  }
  function libelleAge(m) {
    if (m === null) return "";
    if (m < 0) return "à naître";
    if (m < 1) return "moins d'1 mois";
    if (m < 24) return m + " mois";
    var a = Math.floor(m / 12), r = m % 12;
    return a + " an" + (a > 1 ? "s" : "") + (r && a < 6 ? " et " + r + " mois" : "");
  }
  var POUR_AGE = [
    { max: -1, titre: "Bébé arrive bientôt", texte: "C'est le moment de préparer la liste de naissance et la valise de maternité.", liens: [["liste-naissance.html", "Liste de naissance"], ["prenoms.html", "Trouver un prénom"], ["sommeil-bebe.html", "Le sommeil de bébé"]] },
    { max: 3, titre: "Les premières semaines", texte: "Bébé dort par cycles jour et nuit : c'est normal. Pensez à vous reposer quand il dort.", liens: [["pleurs-bebe.html", "Comprendre ses pleurs"], ["suivi-bebe.html", "Suivi tétées et sommeil"], ["sommeil-bebe.html", "Le sommeil de bébé"]] },
    { max: 6, titre: "L'âge des découvertes", texte: "Il gazouille, attrape, se retourne. La diversification approche (entre 4 et 6 mois).", liens: [["diversification-alimentaire.html", "La diversification"], ["langage-enfant.html", "Les premiers mots"], ["outils.html#diversification", "Calendrier des aliments"]] },
    { max: 12, titre: "Bientôt 1 an", texte: "Les dents, les morceaux, les premiers pas… et parfois des nuits agitées.", liens: [["poussees-dentaires.html", "Poussées dentaires"], ["diversification-alimentaire.html", "Les morceaux"], ["journal.html", "Noter ses premières fois"]] },
    { max: 36, titre: "Le petit explorateur", texte: "Il dit « non », veut tout faire seul, et ses émotions débordent : c'est l'âge de l'autonomie.", liens: [["coleres-enfant.html", "Les colères"], ["proprete-enfant.html", "La propreté"], ["adaptation-creche-ecole.html", "Crèche et école"]] },
    { max: 72, titre: "L'âge des pourquoi", texte: "Il pose mille questions, adore les histoires et commence l'école.", liens: [["histoires.html", "Histoire du soir personnalisée"], ["cauchemars-terreurs-nocturnes.html", "Cauchemars"], ["ecrans-enfants.html", "Les écrans"]] },
    { max: 144, titre: "Le grand écolier", texte: "Devoirs, copains, confiance en soi : il a besoin de vous autrement.", liens: [["devoirs-sans-crise.html", "Devoirs sans crise"], ["confiance-en-soi-enfant.html", "La confiance en soi"], ["gout-de-la-lecture.html", "Le goût de la lecture"]] },
    { max: 999, titre: "L'adolescence", texte: "Il prend ses distances, mais a toujours besoin de vous. Restez disponible.", liens: [["communiquer-avec-ado.html", "Parler avec son ado"], ["harcelement-scolaire.html", "Harcèlement scolaire"], ["ecrans-enfants.html", "Écrans et réseaux"]] }
  ];
  function pourAge(m) { return POUR_AGE.filter(function (x) { return m <= x.max; })[0] || POUR_AGE[POUR_AGE.length - 1]; }

  /* ---------- Puce de niveau dans l'en-tête ---------- */
  var puce;
  function majPuce(anim) {
    if (!puce) return;
    var nv = niveau(etat.graines);
    puce.innerHTML = '<span aria-hidden="true">' + nv.n.ico + '</span> <strong>' + etat.graines + '</strong>' + (etat.serie.n > 1 ? ' <span class="puce-serie">🔥' + etat.serie.n + '</span>' : "");
    puce.title = "Niveau " + nv.n.nom + " · " + etat.graines + " graines";
    if (anim && !mouvementReduit) { puce.classList.remove("pop"); void puce.offsetWidth; puce.classList.add("pop"); }
  }
  var hc = document.querySelector("header.site .container");
  var fav = hc && hc.querySelector('a[href="favoris.html"]');
  if (fav) {
    puce = document.createElement("a"); puce.href = "mon-espace.html"; puce.className = "puce-niveau";
    puce.setAttribute("aria-label", "Mon espace et ma progression");
    hc.insertBefore(puce, fav); majPuce();
  }

  /* ---------- Gains automatiques ---------- */
  var page = location.pathname.split("/").pop() || "index.html";
  var h = new Date().getHours();
  if (h < 5) gagner("nuit", 5, "nuit:" + jour(), true);
  // Lecture d'un article jusqu'au bout
  var contenu = document.querySelector(".contenu-article");
  if (contenu && "IntersectionObserver" in window) {
    var fin = document.createElement("div"); fin.setAttribute("aria-hidden", "true"); contenu.appendChild(fin);
    var debut = Date.now();
    var obs = new IntersectionObserver(function (e) {
      if (e[0].isIntersecting && Date.now() - debut > 8000) {
        obs.disconnect();
        if (gagner("lecture", 10, "lu:" + page)) { var lus = lire("ps-lus", []); lus.push(page); ecrire("ps-lus", lus); }
      }
    });
    setTimeout(function () { obs.observe(fin); }, 8000);
  }
  // Utilisation des outils
  document.addEventListener("submit", function (e) {
    if (["form-journal", "form-enfant", "form-histoire"].indexOf(e.target.id) !== -1) return;
    var o = e.target.closest(".outil, [data-outil]"); if (!o) return;
    var id = o.id || e.target.id || page;
    etat.outils[id] = true;
    gagner("outil", 5, "outil:" + id + ":" + jour());
  }, true);
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-gain]"); if (!b) return;
    var id = b.getAttribute("data-gain");
    etat.outils[id] = true;
    gagner("outil", 5, "outil:" + id + ":" + jour());
  });

  /* ---------- Widget d'accueil personnalisé ---------- */
  function carteDefi() {
    var fait = etat.defis[jour()];
    return '<div class="widget defi' + (fait ? " fait" : "") + '"><span class="widget-tag">🎯 Défi du jour</span><p class="defi-texte">' + esc(defiDuJour()) + '</p>' +
      (fait ? '<p class="defi-ok">✅ Défi réussi, bravo ! Revenez demain pour le suivant.</p>' : '<button class="btn" type="button" data-defi>J\'ai réussi le défi (+15 🌱)</button>') + "</div>";
  }
  function carteBonus() {
    var pris = etat.bonus === jour();
    var montant = Math.min(15, 5 + (etat.serie.dernier === hier() ? etat.serie.n : 0));
    return '<div class="widget bonus' + (pris ? " fait" : "") + '"><span class="widget-tag">🎁 Graines du jour</span>' +
      (pris ? '<p>Récoltées ! Revenez demain : plus votre série est longue, plus la récolte est grosse (jusqu\'à 15 🌱).</p>'
            : '<p>Votre récolte quotidienne vous attend.</p><button class="btn graine-btn" type="button" data-bonus="' + montant + '"><span class="secoue">🌱</span> Récolter ' + montant + ' graines</button>') +
      '<p class="mention-aff">🔥 Série : ' + etat.serie.n + ' jour' + (etat.serie.n > 1 ? "s" : "") + ' · record ' + (etat.serie.record || 0) + "</p></div>";
  }
  function carteNiveau() {
    var nv = niveau(etat.graines), nb = Object.keys(etat.badges).length;
    return '<a class="widget niveau-w" href="mon-espace.html"><span class="widget-tag">' + nv.n.ico + " Niveau " + nv.n.nom + '</span>' +
      '<div class="jauge"><div style="width:' + Math.round(nv.pct * 100) + '%"></div></div>' +
      '<p><strong>' + etat.graines + ' graines</strong>' + (nv.suivant ? " · encore " + (nv.suivant.min - etat.graines) + " pour " + nv.suivant.ico + " " + nv.suivant.nom : " · niveau maximum !") + '</p>' +
      '<p class="mention-aff">🏅 ' + nb + " / " + BADGES.length + " badges · Voir mon espace →</p></a>";
  }
  function blocEnfants() {
    var l = enfants();
    if (!l.length) return '<div class="widget accueil-perso"><span class="widget-tag">👋 Personnalisez le site</span><h3>Des conseils adaptés à l\'âge de votre enfant</h3><p>Indiquez son prénom et sa date de naissance (ou la date du terme) : le site vous montrera chaque jour ce qui compte à son âge.</p><a class="btn" href="mon-espace.html#enfants">Ajouter mon enfant <span class="fleche">→</span></a></div>';
    return l.map(function (e) {
      var m = ageMois(e.naissance), p = pourAge(m);
      return '<div class="widget accueil-perso"><span class="widget-tag">' + (m < 0 ? "🤰" : "🧒") + " " + esc(e.prenom) + " · " + libelleAge(m) + '</span><h3>' + esc(p.titre) + '</h3><p>' + esc(p.texte) + '</p><p class="liens-age">' +
        p.liens.map(function (x) { return '<a href="' + x[0] + '">' + esc(x[1]) + " →</a>"; }).join("") + "</p></div>";
    }).join("");
  }
  function brancherWidgets(zone) {
    zone.querySelectorAll("[data-defi]").forEach(function (b) {
      b.addEventListener("click", function () { etat.defis[jour()] = true; sauver(); gagner("defi", 15, "defi:" + jour()); dessinerAccueil(); dessinerEspace(); });
    });
    zone.querySelectorAll("[data-bonus]").forEach(function (b) {
      b.addEventListener("click", function () {
        etat.bonus = jour(); sauver(); b.classList.add("recolte");
        setTimeout(function () { gagner("bonus", parseInt(b.getAttribute("data-bonus"), 10), "bonus:" + jour()); dessinerAccueil(); dessinerEspace(); }, mouvementReduit ? 0 : 450);
      });
    });
  }
  var zoneAccueil = document.getElementById("widgets-accueil");
  function dessinerAccueil() {
    if (!zoneAccueil) return;
    zoneAccueil.innerHTML = '<div class="widgets">' + blocEnfants() + carteBonus() + carteDefi() + carteNiveau() +
      '<div class="widget fait-jour"><span class="widget-tag">💡 Le saviez-vous ?</span><p>' + esc(faitDuJour()) + "</p></div></div>";
    brancherWidgets(zoneAccueil);
  }
  dessinerAccueil();

  /* ---------- Page « Mon espace » ---------- */
  var zoneEspace = document.getElementById("espace");
  function dessinerEspace() {
    if (!zoneEspace) return;
    var nv = niveau(etat.graines), l = enfants(), lus = lire("ps-lus", []);
    var r = 54, circ = 2 * Math.PI * r;
    document.getElementById("espace-niveau").innerHTML =
      '<div class="anneau"><svg viewBox="0 0 130 130" aria-hidden="true"><circle cx="65" cy="65" r="' + r + '" class="anneau-fond"/><circle cx="65" cy="65" r="' + r + '" class="anneau-plein" style="stroke-dasharray:' + circ + ';stroke-dashoffset:' + (circ * (1 - nv.pct)) + '"/></svg><span>' + nv.n.ico + "</span></div>" +
      '<div><p class="widget-tag">Niveau ' + (nv.i + 1) + " / " + NIVEAUX.length + '</p><h2 style="margin:.1em 0">' + nv.n.nom + '</h2><p><strong>' + etat.graines + " graines</strong>" +
      (nv.suivant ? " · plus que " + (nv.suivant.min - etat.graines) + " avant " + nv.suivant.ico + " " + nv.suivant.nom : "") + '</p>' +
      '<div class="stats"><span>🔥 Série <strong>' + etat.serie.n + '</strong></span><span>🏆 Record <strong>' + (etat.serie.record || 0) + '</strong></span><span>📖 Lus <strong>' + lus.length + '</strong></span><span>🎯 Défis <strong>' + c("defi") + '</strong></span><span>🏅 Badges <strong>' + Object.keys(etat.badges).length + "/" + BADGES.length + "</strong></span></div></div>";
    document.getElementById("espace-jour").innerHTML = '<div class="widgets">' + carteBonus() + carteDefi() + "</div>";
    brancherWidgets(document.getElementById("espace-jour"));
    document.getElementById("espace-badges").innerHTML = BADGES.map(function (b) {
      var ok = etat.badges[b.id];
      return '<div class="badge' + (ok ? " gagne" : "") + '" title="' + esc(b.desc) + '"><span class="badge-ico">' + (ok ? b.ico : "🔒") + '</span><strong>' + esc(b.nom) + '</strong><small>' + esc(b.desc) + (ok ? " · " + ok.split("-").reverse().join("/") : "") + "</small></div>";
    }).join("");
    document.getElementById("espace-enfants").innerHTML = l.length ? l.map(function (e, i) {
      var m = ageMois(e.naissance);
      return '<li><span class="avatar">' + esc(e.prenom.charAt(0).toUpperCase()) + '</span><span><strong>' + esc(e.prenom) + "</strong><br><small>" + libelleAge(m) + '</small></span><button class="pilule" type="button" data-suppr="' + i + '" aria-label="Retirer ' + esc(e.prenom) + '">Retirer</button></li>';
    }).join("") : '<li class="mention-aff">Aucun enfant pour l\'instant.</li>';
    document.getElementById("espace-pourage").innerHTML = blocEnfants();
    var chemins = [["sommeil-bebe.html", "Sommeil"], ["diversification-alimentaire.html", "Diversification"], ["coleres-enfant.html", "Colères"], ["ecrans-enfants.html", "Écrans"], ["pleurs-bebe.html", "Pleurs"], ["langage-enfant.html", "Langage"], ["proprete-enfant.html", "Propreté"], ["poussees-dentaires.html", "Dents"], ["freres-et-soeurs.html", "Fratrie"], ["adaptation-creche-ecole.html", "Séparation"], ["cauchemars-terreurs-nocturnes.html", "Cauchemars"], ["enfant-ne-mange-pas.html", "Repas"], ["devoirs-sans-crise.html", "Devoirs"], ["confiance-en-soi-enfant.html", "Confiance"], ["gout-de-la-lecture.html", "Lecture"], ["harcelement-scolaire.html", "Harcèlement"], ["communiquer-avec-ado.html", "Ados"], ["voyager-avec-enfants.html", "Voyages"], ["activites-enfants-maison.html", "Activités"]];
    document.getElementById("espace-lectures").innerHTML = chemins.map(function (x) {
      var ok = lus.indexOf(x[0]) !== -1;
      return '<a class="case-lecture' + (ok ? " lu" : "") + '" href="' + x[0] + '">' + (ok ? "✅ " : "○ ") + x[1] + "</a>";
    }).join("");
  }
  if (zoneEspace) {
    dessinerEspace();
    document.getElementById("form-enfant").addEventListener("submit", function (e) {
      e.preventDefault();
      var p = document.getElementById("enfant-prenom").value.trim().slice(0, 30), d = document.getElementById("enfant-naissance").value;
      if (!p || !d) return;
      var l = enfants(); l.push({ prenom: p, naissance: d }); ecrire("ps-enfants", l);
      e.target.reset(); gagner("profil", 10, "profil:" + p.toLowerCase()); dessinerEspace();
    });
    document.getElementById("espace-enfants").addEventListener("click", function (e) {
      var i = e.target.getAttribute("data-suppr"); if (i === null) return;
      var l = enfants(); l.splice(+i, 1); ecrire("ps-enfants", l); dessinerEspace();
    });
    // Sauvegarde / restauration de toutes les données
    var CLES = ["ps-progres", "ps-enfants", "ps-lus", "ps-favoris", "ps-journal", "ps-suivi", "ps-prenoms", "ps-histoires", "parents-sereins-liste", "ps-theme", "ps-taille", "ps-quiz"];
    document.getElementById("exporter").addEventListener("click", function () {
      var d = {}; CLES.forEach(function (k) { var v = lire(k, null); if (v !== null) d[k] = v; });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([JSON.stringify(d, null, 1)], { type: "application/json" }));
      a.download = "parents-sereins-sauvegarde-" + jour() + ".json"; document.body.appendChild(a); a.click(); a.remove();
      window.toast && toast("Sauvegarde téléchargée 💾");
    });
    document.getElementById("importer").addEventListener("change", function (e) {
      var f = e.target.files[0]; if (!f) return;
      var r = new FileReader();
      r.onload = function () {
        try { var d = JSON.parse(r.result); Object.keys(d).forEach(function (k) { if (CLES.indexOf(k) !== -1) ecrire(k, d[k]); }); location.reload(); }
        catch (err) { window.toast && toast("Ce fichier n'est pas une sauvegarde valide"); }
      };
      r.readAsText(f);
    });
    document.getElementById("effacer").addEventListener("click", function () {
      if (!confirm("Effacer toutes vos données sur cet appareil (progression, enfants, journal, favoris…) ?")) return;
      CLES.forEach(function (k) { try { localStorage.removeItem(k); } catch (err) {} });
      location.reload();
    });
  }
  document.addEventListener("ps:progres", function () { if (zoneEspace) dessinerEspace(); });

  window.PS = { gagner: gagner, lire: lire, ecrire: ecrire, esc: esc, jour: jour, enfants: enfants, ageMois: ageMois, libelleAge: libelleAge, celebrer: celebrer, confettis: confettis };
  verifierBadges();
})();
