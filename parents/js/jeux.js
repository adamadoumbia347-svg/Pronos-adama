/* Parents Sereins — journal de bébé, suivi tétées/sommeil, histoires du soir, prénoms, quiz */
(function () {
  var PS = window.PS || {};
  var lire = PS.lire, ecrire = PS.ecrire, esc = PS.esc;
  function $(id) { return document.getElementById(id); }
  function hasard(l) { return l[Math.floor(Math.random() * l.length)]; }
  function melanger(l) { l = l.slice(); for (var i = l.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = l[i]; l[i] = l[j]; l[j] = t; } return l; }
  function remplirEnfants(select) {
    if (!select) return;
    var l = PS.enfants();
    select.innerHTML = (l.length ? l.map(function (e, i) { return '<option value="' + i + '">' + esc(e.prenom) + "</option>"; }).join("") : "") + '<option value="">Sans prénom</option>';
  }

  /* =================== Journal de bébé =================== */
  var formJ = $("form-journal");
  if (formJ) {
    var selJ = $("j-enfant"); remplirEnfants(selJ);
    $("j-date").value = PS.jour();
    $("j-moment").addEventListener("change", function () { $("j-autre-zone").style.display = this.value === "autre" ? "block" : "none"; });
    function dessinerJournal() {
      var l = lire("ps-journal", []);
      l.sort(function (a, b) { return a.date < b.date ? 1 : -1; });
      $("journal-vide").style.display = l.length ? "none" : "block";
      $("journal-compte").textContent = l.length;
      $("frise").innerHTML = l.map(function (s) {
        var age = s.naissance ? PS.ageMois(s.naissance) : null, ageTxt = "";
        if (s.naissance) { var n = new Date(s.naissance), d = new Date(s.date); var m = (d.getFullYear() - n.getFullYear()) * 12 + d.getMonth() - n.getMonth() - (d.getDate() < n.getDate() ? 1 : 0); ageTxt = m >= 0 ? " · à " + PS.libelleAge(m).replace("moins d'1 mois", (Math.max(0, Math.round((d - n) / 864e5))) + " jours") : ""; }
        return '<li class="souvenir"><span class="souvenir-ico">' + esc(s.ico) + '</span><div><small>' + new Date(s.date).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" }) + esc(ageTxt) + '</small><h3>' + esc(s.titre) + (s.prenom ? " — " + esc(s.prenom) : "") + "</h3>" +
          (s.note ? "<p>" + esc(s.note) + "</p>" : "") + '<button class="pilule pas-imprimer" type="button" data-suppr="' + esc(s.id) + '">Supprimer</button></div></li>';
      }).join("");
    }
    formJ.addEventListener("submit", function (e) {
      e.preventDefault();
      var opt = $("j-moment").selectedOptions[0], enfant = PS.enfants()[selJ.value];
      var titre = $("j-moment").value === "autre" ? ($("j-autre").value.trim() || "Un moment à retenir") : opt.textContent.replace(/^\S+\s/, "");
      var l = lire("ps-journal", []);
      l.push({ id: Date.now().toString(36), ico: opt.getAttribute("data-ico") || "⭐", titre: titre.slice(0, 80), date: $("j-date").value || PS.jour(), note: $("j-note").value.trim().slice(0, 500), prenom: enfant ? enfant.prenom : "", naissance: enfant ? enfant.naissance : "" });
      ecrire("ps-journal", l);
      formJ.reset(); $("j-date").value = PS.jour(); remplirEnfants(selJ); $("j-autre-zone").style.display = "none";
      PS.gagner("souvenir", 5); dessinerJournal();
      var premier = $("frise").firstElementChild; if (premier) premier.classList.add("nouveau");
    });
    $("frise").addEventListener("click", function (e) {
      var id = e.target.getAttribute("data-suppr"); if (!id || !confirm("Supprimer ce souvenir ?")) return;
      ecrire("ps-journal", lire("ps-journal", []).filter(function (s) { return s.id !== id; })); dessinerJournal();
    });
    $("j-imprimer").addEventListener("click", function () { window.print(); });
    dessinerJournal();
  }

  /* =================== Suivi de bébé =================== */
  var zoneS = $("suivi");
  if (zoneS) {
    var TYPES = {
      teteeG: { ico: "🤱", nom: "Tétée gauche", duree: true }, teteeD: { ico: "🤱", nom: "Tétée droite", duree: true },
      biberon: { ico: "🍼", nom: "Biberon" }, sommeil: { ico: "😴", nom: "Sommeil", duree: true },
      pipi: { ico: "💧", nom: "Couche pipi" }, selles: { ico: "💩", nom: "Couche selles" }, soin: { ico: "🩹", nom: "Soin / médicament" }
    };
    function donnees() { var d = lire("ps-suivi", { liste: [], encours: {} }); d.liste = d.liste || []; d.encours = d.encours || {}; return d; }
    function sauverS(d) { var limite = Date.now() - 14 * 864e5; d.liste = d.liste.filter(function (x) { return x.t > limite; }); ecrire("ps-suivi", d); }
    function hm(t) { var d = new Date(t); return ("0" + d.getHours()).slice(-2) + "h" + ("0" + d.getMinutes()).slice(-2); }
    function dureeTxt(ms) { var m = Math.round(ms / 6e4); return m < 60 ? m + " min" : Math.floor(m / 60) + " h " + ("0" + (m % 60)).slice(-2); }
    function ilya(t) { return "il y a " + dureeTxt(Date.now() - t); }
    function debutJour(dec) { var d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - (dec || 0)); return d.getTime(); }
    function dessinerS() {
      var d = donnees(), auj = d.liste.filter(function (x) { return x.t >= debutJour(); });
      document.querySelectorAll("[data-suivi]").forEach(function (b) {
        var k = b.getAttribute("data-suivi"), ec = d.encours[k];
        b.classList.toggle("en-cours", !!ec);
        b.querySelector(".etat").textContent = ec ? "⏹ " + dureeTxt(Date.now() - ec) : (TYPES[k].duree ? "▶ Démarrer" : "+ Noter");
      });
      var tetees = d.liste.filter(function (x) { return x.k === "teteeG" || x.k === "teteeD" || x.k === "biberon"; }).sort(function (a, b) { return b.t - a.t; });
      var der = tetees[0], cote = "";
      var dg = d.liste.filter(function (x) { return x.k === "teteeG" || x.k === "teteeD"; }).sort(function (a, b) { return b.t - a.t; })[0];
      if (dg) cote = " · prochain côté conseillé : <strong>" + (dg.k === "teteeG" ? "droit" : "gauche") + "</strong>";
      var sommeil = auj.filter(function (x) { return x.k === "sommeil"; }).reduce(function (s, x) { return s + (x.duree || 0); }, 0);
      $("suivi-resume").innerHTML =
        '<div class="stat-s"><span>🍼</span><strong>' + auj.filter(function (x) { return /tetee|biberon/.test(x.k); }).length + '</strong>repas aujourd\'hui</div>' +
        '<div class="stat-s"><span>😴</span><strong>' + dureeTxt(sommeil) + '</strong>de sommeil noté</div>' +
        '<div class="stat-s"><span>🧷</span><strong>' + auj.filter(function (x) { return x.k === "pipi" || x.k === "selles"; }).length + '</strong>couches</div>' +
        '<p class="dernier">' + (der ? "Dernier repas : <strong>" + hm(der.t) + "</strong> (" + ilya(der.t) + ")" + cote : "Aucun repas noté pour l'instant.") + "</p>";
      // Barres des 7 derniers jours
      var html = "";
      for (var i = 6; i >= 0; i--) {
        var a = debutJour(i), b = a + 864e5, n = d.liste.filter(function (x) { return x.t >= a && x.t < b && /tetee|biberon/.test(x.k); }).length;
        html += '<div class="barre-jour"><div class="barre" style="height:' + Math.min(100, n * 8) + '%"><span>' + (n || "") + '</span></div><small>' + new Date(a).toLocaleDateString("fr-FR", { weekday: "short" }).replace(".", "") + "</small></div>";
      }
      $("suivi-semaine").innerHTML = html;
      $("suivi-liste").innerHTML = auj.length ? auj.sort(function (a, b) { return b.t - a.t; }).map(function (x) {
        return '<li><span class="h">' + hm(x.t) + '</span><span>' + TYPES[x.k].ico + " " + TYPES[x.k].nom + (x.duree ? " · " + dureeTxt(x.duree) : "") + (x.ml ? " · " + x.ml + " ml" : "") + '</span><button class="pilule" type="button" data-supprs="' + x.t + '" aria-label="Supprimer">✕</button></li>';
      }).join("") : '<li class="mention-aff">Rien de noté aujourd\'hui.</li>';
    }
    zoneS.addEventListener("click", function (e) {
      var b = e.target.closest("[data-suivi]"), s = e.target.closest("[data-supprs]");
      var d = donnees();
      if (s) { var t = +s.getAttribute("data-supprs"); d.liste = d.liste.filter(function (x) { return x.t !== t; }); sauverS(d); dessinerS(); return; }
      if (!b) return;
      var k = b.getAttribute("data-suivi");
      b.classList.remove("tape"); void b.offsetWidth; b.classList.add("tape");
      if (TYPES[k].duree) {
        if (d.encours[k]) { d.liste.push({ k: k, t: d.encours[k], duree: Date.now() - d.encours[k] }); delete d.encours[k]; PS.gagner("suivi", 2); }
        else { if (k !== "sommeil") { delete d.encours.teteeG; delete d.encours.teteeD; } d.encours[k] = Date.now(); }
      } else {
        var item = { k: k, t: Date.now() };
        if (k === "biberon") { var ml = prompt("Quantité bue (en ml) ? Laissez vide si vous ne savez pas.", ""); if (ml === null) return; if (+ml > 0) item.ml = Math.min(400, Math.round(+ml)); }
        d.liste.push(item); PS.gagner("suivi", 2);
      }
      sauverS(d); dessinerS();
    });
    dessinerS(); setInterval(dessinerS, 20000);
  }

  /* =================== Histoires du soir =================== */
  var formH = $("form-histoire");
  if (formH) {
    var l = PS.enfants(); if (l.length) $("h-prenom").value = l[0].prenom;
    var AMIS = {
      lapin: ["un petit lapin aux oreilles toutes douces", "le lapin"], dragon: ["un minuscule dragon qui crachait des bulles au lieu du feu", "le petit dragon"],
      ours: ["un ourson gourmand", "l'ourson"], licorne: ["une licorne à la crinière arc-en-ciel", "la licorne"], renard: ["un renard malicieux", "le renard"],
      dinosaure: ["un dinosaure très gentil (mais très maladroit)", "le dinosaure"], hibou: ["un vieux hibou plein de sagesse", "le hibou"], chat: ["un chat qui savait parler", "le chat"]
    };
    var LIEUX = {
      foret: ["la forêt enchantée", "Les arbres chuchotaient des secrets et les champignons brillaient comme des lanternes."],
      ocean: ["le fond de l'océan", "Des poissons multicolores faisaient la ronde autour d'un château de corail."],
      lune: ["la Lune", "Là-haut, on rebondissait à chaque pas, comme sur un énorme matelas."],
      chateau: ["un château dans les nuages", "Les escaliers étaient en guimauve et les fenêtres donnaient sur les étoiles."],
      jungle: ["la grande jungle", "Les perroquets racontaient des blagues et les singes jouaient du tambour."],
      banquise: ["la banquise", "Les pingouins glissaient sur le ventre en riant aux éclats."]
    };
    var OBJETS = { cle: "une petite clé dorée qui ouvrait toutes les portes", lampe: "une lampe de poche qui éclairait aussi les cœurs", carte: "une carte au trésor qui se dessinait toute seule", flute: "une flûte dont la musique rendait tout le monde joyeux", graine: "une graine magique qui poussait en un clin d'œil", plume: "une plume qui permettait de voler quelques instants" };
    var VALEURS = {
      courage: ["Mais au milieu du chemin se dressait un pont tout branlant, au-dessus d'une rivière qui grondait.", "{P} prit une grande respiration. « J'ai un peu peur, dit {P}, mais avoir peur, ce n'est pas grave : on peut avancer quand même. » Pas après pas, nos deux amis traversèrent le pont.", "Ce soir-là, {P} avait appris qu'avoir du courage, ce n'est pas ne jamais avoir peur : c'est essayer quand même."],
      amitie: ["Soudain, ils entendirent des pleurs : un petit hérisson s'était perdu et personne ne voulait jouer avec lui, à cause de ses piquants.", "« Viens avec nous ! » dit {P} en lui tendant la main, tout doucement pour ne pas se piquer. Le hérisson sourit pour la première fois de la journée.", "Ce soir-là, {P} avait appris qu'un ami, c'est quelqu'un qui nous accepte tel qu'on est."],
      partage: ["En chemin, ils trouvèrent un panier rempli des plus délicieuses fraises du monde. Mais tout autour, d'autres animaux avaient faim.", "{P} réfléchit un instant, puis distribua les fraises une à une. Et, comme par magie, plus on partageait, plus le goûter devenait joyeux.", "Ce soir-là, {P} avait appris que le bonheur partagé est deux fois plus grand."],
      patience: ["Mais le trésor était caché derrière une porte qui ne s'ouvrait qu'au lever de la lune. Il fallait attendre…", "Alors {P} s'assit, compta les étoiles, écouta le vent, raconta des devinettes. Et quand la lune se leva enfin, la porte s'ouvrit dans un grand éclat d'argent.", "Ce soir-là, {P} avait appris que les plus belles choses valent la peine d'attendre."],
      confiance: ["Mais {L} avait un problème : il fallait chanter une chanson devant tout le monde pour ouvrir le passage, et {P} ne se sentait pas capable.", "« Tu peux le faire », murmura {A}. {P} chanta d'abord tout bas, puis un peu plus fort, puis à pleine voix. Et le passage s'ouvrit sous les applaudissements !", "Ce soir-là, {P} avait appris à croire en soi."]
    };
    var DEBUTS = ["Il était une fois, dans une maison où l'on entendait rire tous les jours, un enfant qui s'appelait {P}.", "Ce soir-là, alors que la lune se cachait derrière un nuage, {P} entendit toc-toc-toc à la fenêtre.", "Tout le monde dormait déjà, sauf {P}, qui regardait les étoiles en se demandant ce qu'il y avait là-haut."];
    var FINS = ["Puis {A} raccompagna {P} jusqu'à la maison. Le lit était tout chaud, l'oreiller tout doux. {P} ferma les yeux en souriant, et s'endormit en rêvant à de nouvelles aventures.", "Sur le chemin du retour, les étoiles s'allumèrent une à une, comme pour dire bravo. {P} bâilla, bâilla encore… et s'endormit, bien au chaud, le cœur plein de lumière.", "« À demain ! » chuchota {A}. Et {P}, sous sa couette toute douce, ferma doucement les yeux. Bonne nuit, {P}. Fais de beaux rêves."];
    var derniere = "";
    formH.addEventListener("submit", function (e) {
      e.preventDefault();
      var P = ($("h-prenom").value.trim() || "Petit Loup").replace(/[<>]/g, "").slice(0, 25);
      var ami = AMIS[$("h-ami").value], lieu = LIEUX[$("h-lieu").value], objet = OBJETS[$("h-objet").value], val = VALEURS[$("h-valeur").value];
      var A = ami[1], longue = $("h-longueur").value === "longue";
      function r(t) { return t.replace(/\{P\}/g, P).replace(/\{A\}/g, A).replace(/\{L\}/g, lieu[0]); }
      var par = [
        r(hasard(DEBUTS)),
        r("Cette nuit-là, " + ami[0] + " apparut au pied du lit. « Viens vite, dit " + A + ", j'ai besoin de toi ! » Et hop, nos deux amis partirent pour " + lieu[0] + "."),
        lieu[1],
        r(val[0]),
        r(val[1]),
        r("Heureusement, " + A + " avait apporté " + objet + ". Grâce à elle, la route fut plus facile et l'aventure plus belle encore.")
      ];
      if (longue) par.splice(3, 0, r("En chemin, ils rencontrèrent des créatures étonnantes : une tortue qui faisait la course avec un escargot, des lucioles qui jouaient à cache-cache, et un nuage qui avait le hoquet. {P} riait tellement que " + A + " dut s'asseoir pour reprendre son souffle."));
      par.push(r(val[2]), r(hasard(FINS)));
      var titre = P + " et " + A + " dans " + lieu[0];
      derniere = titre + ". " + par.join(" ");
      $("histoire").innerHTML = '<h2>' + esc(titre.charAt(0).toUpperCase() + titre.slice(1)) + "</h2>" + par.map(function (p, i) { return '<p style="animation-delay:' + (i * 0.12) + 's">' + esc(p) + "</p>"; }).join("") + '<p class="fin-histoire">✨ Fin ✨</p>';
      $("histoire-zone").style.display = "block";
      $("histoire-zone").scrollIntoView({ behavior: "smooth", block: "start" });
      PS.gagner("histoire", 5);
    });
    var voix = window.speechSynthesis;
    $("h-lire").addEventListener("click", function () {
      if (!voix) { window.toast && toast("La lecture à voix haute n'est pas disponible sur ce navigateur"); return; }
      if (voix.speaking) { voix.cancel(); this.textContent = "🔊 Lire à voix haute"; return; }
      var u = new SpeechSynthesisUtterance(derniere); u.lang = "fr-FR"; u.rate = .88; u.pitch = 1.05;
      var fr = voix.getVoices().filter(function (v) { return /^fr/i.test(v.lang); })[0]; if (fr) u.voice = fr;
      var btn = this; u.onend = function () { btn.textContent = "🔊 Lire à voix haute"; };
      voix.speak(u); this.textContent = "⏹ Arrêter la lecture";
    });
    $("h-autre").addEventListener("click", function () { formH.requestSubmit ? formH.requestSubmit() : formH.dispatchEvent(new Event("submit")); });
    $("h-hasard").addEventListener("click", function () {
      ["h-ami", "h-lieu", "h-objet", "h-valeur"].forEach(function (id) { var s = $(id); s.selectedIndex = Math.floor(Math.random() * s.options.length); s.classList.remove("secoue-champ"); void s.offsetWidth; s.classList.add("secoue-champ"); });
    });
  }

  /* =================== Prénoms =================== */
  var zoneP = $("prenoms");
  if (zoneP) {
    var F = "Jade Louise Ambre Alba Emma Rose Alice Romy Anna Lina Mia Julia Chloé Léna Agathe Iris Inès Juliette Victoire Mila Léa Lou Margaux Zoé Nina Sofia Éva Olivia Clémence Capucine Héloïse Apolline Joséphine Adèle Manon Lucie Sarah Romane Gabrielle Valentine Constance Suzanne Marguerite Jeanne Céleste Elena Maya Luna Livia Nour Aya Yasmine Salomé Clara Pauline Élise Ninon Billie Margot Diane Hortense Garance Lison Thaïs Philippine Anaïs Faustine Albane Bérénice Ava Giulia Lya Maëlys Lyna Kenza Assia Maryam Fatou Violette Mathilde Louna".split(" ");
    var M = "Gabriel Raphaël Léo Louis Maël Noah Jules Arthur Adam Lucas Hugo Liam Gabin Mohamed Paul Aaron Tom Nathan Léon Martin Théo Victor Isaac Ethan Noé Timéo Marius Malo Augustin Côme Gaspard Lucien Joseph Marcel Achille Basile Félix Antoine Oscar Baptiste Valentin Mathis Axel Enzo Samuel Elio Milo Ezra Nino Ilyes Ayoub Yanis Rayan Amir Ismaël Ibrahim Moussa Mamadou Abel Simon Robin Olivier Pierre Jean Hector Anatole Octave Lazare Tiago Diego Mathéo Clément Thomas Alexandre Maxime Kylian Léandre Sylvain".split(" ");
    var X = "Sacha Charlie Camille Eden Alix Noa Andrea Swann Morgan Gaby Dominique Ange".split(" ");
    var RETRO = "Louise Rose Alice Agathe Victoire Joséphine Adèle Suzanne Marguerite Jeanne Céleste Hortense Philippine Albane Bérénice Constance Mathilde Violette Marcel Lucien Joseph Achille Augustin Côme Gaspard Hector Anatole Octave Lazare Léon Marius Basile Félix Oscar Abel Pierre Jean Simon".split(" ");
    var NATURE = "Jade Ambre Rose Iris Capucine Marguerite Garance Luna Céleste Violette Olivier Basile Sylvain Swann Noé Maya".split(" ");
    var INTER = "Emma Mia Julia Sofia Olivia Elena Maya Luna Ava Giulia Anna Liam Noah Ethan Isaac Aaron Ezra Milo Tiago Diego Elio Nino Axel Samuel Adam Andrea Charlie Sacha Eden Morgan Billie Livia".split(" ");
    var TOUS = [];
    F.forEach(function (n) { TOUS.push({ n: n, g: "f" }); }); M.forEach(function (n) { TOUS.push({ n: n, g: "m" }); }); X.forEach(function (n) { TOUS.push({ n: n, g: "x" }); });
    TOUS.forEach(function (p) {
      p.s = []; var sansAccent = p.n.normalize("NFD").replace(/[̀-ͯ]/g, "");
      if (sansAccent.length <= 4) p.s.push("court"); if (RETRO.indexOf(p.n) !== -1) p.s.push("retro");
      if (NATURE.indexOf(p.n) !== -1) p.s.push("nature"); if (INTER.indexOf(p.n) !== -1) p.s.push("international");
      p.i = sansAccent.charAt(0).toUpperCase();
    });
    var aimes = lire("ps-prenoms", { oui: [], non: [] }); aimes.oui = aimes.oui || []; aimes.non = aimes.non || [];
    var pile = [], courant = null;
    function filtres() { return { g: zoneP.querySelector("input[name=p-genre]:checked").value, s: $("p-style").value, i: $("p-initiale").value }; }
    function construirePile() {
      var f = filtres();
      pile = melanger(TOUS.filter(function (p) {
        return (f.g === "tous" || p.g === f.g || (p.g === "x" && f.g !== "x" && $("p-mixtes").checked)) && (!f.s || p.s.indexOf(f.s) !== -1) && (!f.i || p.i === f.i) &&
          aimes.oui.indexOf(p.n) === -1 && aimes.non.indexOf(p.n) === -1;
      }));
      suivant();
    }
    function suivant() {
      courant = pile.shift();
      var c = $("p-carte");
      c.className = "carte-prenom entre";
      if (!courant) { c.innerHTML = '<div class="p-nom" style="font-size:1.4rem">Plus de prénoms avec ces filtres 🎉</div><p>Changez les filtres ou remettez les « non » à zéro.</p>'; return; }
      var genre = { f: "Fille", m: "Garçon", x: "Mixte" }[courant.g];
      c.innerHTML = '<span class="p-genre p-' + courant.g + '">' + genre + '</span><div class="p-nom">' + courant.n.split("").map(function (l, i) { return '<span style="animation-delay:' + (i * .04) + 's">' + esc(l) + "</span>"; }).join("") + '</div><div class="p-tags">' + courant.s.map(function (s) { return "<span>" + { court: "Court", retro: "Rétro", nature: "Nature", international: "International" }[s] + "</span>"; }).join("") + "</div>";
      $("p-restants").textContent = pile.length + " prénom" + (pile.length > 1 ? "s" : "") + " restant" + (pile.length > 1 ? "s" : "");
    }
    function choisir(oui) {
      if (!courant) return;
      var c = $("p-carte");
      (oui ? aimes.oui : aimes.non).push(courant.n); ecrire("ps-prenoms", aimes);
      if (oui) PS.gagner("prenom", 1, null, true);
      c.className = "carte-prenom " + (oui ? "part-droite" : "part-gauche");
      dessinerAimes();
      setTimeout(suivant, 320);
    }
    function dessinerAimes() {
      $("p-aimes").innerHTML = aimes.oui.length ? aimes.oui.map(function (n) { return '<li><span>' + esc(n) + '</span><button type="button" aria-label="Retirer ' + esc(n) + '" data-retire="' + esc(n) + '">✕</button></li>'; }).join("") : '<li class="mention-aff">Vos coups de cœur apparaîtront ici.</li>';
      $("p-nb").textContent = aimes.oui.length;
    }
    $("p-oui").addEventListener("click", function () { choisir(true); });
    $("p-non").addEventListener("click", function () { choisir(false); });
    document.addEventListener("keydown", function (e) { if (e.target.matches("input, textarea, select")) return; if (e.key === "ArrowRight") choisir(true); if (e.key === "ArrowLeft") choisir(false); });
    // Glisser la carte au doigt
    var carte = $("p-carte"), x0 = null;
    carte.addEventListener("pointerdown", function (e) { x0 = e.clientX; carte.setPointerCapture(e.pointerId); carte.style.transition = "none"; });
    carte.addEventListener("pointermove", function (e) { if (x0 === null) return; var dx = e.clientX - x0; carte.style.transform = "translateX(" + dx + "px) rotate(" + dx / 18 + "deg)"; carte.classList.toggle("vers-oui", dx > 60); carte.classList.toggle("vers-non", dx < -60); });
    carte.addEventListener("pointerup", function (e) {
      if (x0 === null) return; var dx = e.clientX - x0; x0 = null; carte.style.transition = ""; carte.style.transform = ""; carte.classList.remove("vers-oui", "vers-non");
      if (dx > 90) choisir(true); else if (dx < -90) choisir(false);
    });
    zoneP.querySelectorAll("input[name=p-genre], #p-style, #p-initiale, #p-mixtes").forEach(function (el) { el.addEventListener("change", construirePile); });
    $("p-aimes").addEventListener("click", function (e) { var n = e.target.getAttribute("data-retire"); if (!n) return; aimes.oui = aimes.oui.filter(function (x) { return x !== n; }); ecrire("ps-prenoms", aimes); dessinerAimes(); });
    $("p-raz").addEventListener("click", function () { aimes.non = []; ecrire("ps-prenoms", aimes); construirePile(); window.toast && toast("Les prénoms refusés reviennent dans la pile"); });
    $("p-copier").addEventListener("click", function () {
      var t = "Mes prénoms coups de cœur : " + aimes.oui.join(", ");
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(function () { window.toast && toast("Liste copiée : envoyez-la à l'autre parent 💌"); });
    });
    $("p-comparer").addEventListener("click", function () {
      var autre = $("p-autre").value.replace(/^.*?:/, "").split(/[,;\n]/).map(function (s) { return s.trim().toLowerCase(); }).filter(Boolean);
      var communs = aimes.oui.filter(function (n) { return autre.indexOf(n.toLowerCase()) !== -1; });
      $("p-match").innerHTML = communs.length ? "<p><strong>💞 " + communs.length + " prénom" + (communs.length > 1 ? "s" : "") + " en commun :</strong></p><p class='matchs'>" + communs.map(function (n) { return "<span>" + esc(n) + "</span>"; }).join("") + "</p>" : "<p>Aucun prénom en commun pour l'instant… continuez à jouer chacun de votre côté !</p>";
      $("p-match").classList.add("visible");
      if (communs.length) PS.confettis();
    });
    var lettres = "ABCDEFGHIJKLMNOPRSTVWXYZ".split("").filter(function (l) { return TOUS.some(function (p) { return p.i === l; }); });
    $("p-initiale").innerHTML = '<option value="">Toutes</option>' + lettres.map(function (l) { return "<option>" + l + "</option>"; }).join("");
    dessinerAimes(); construirePile();
  }

  /* =================== Quiz =================== */
  var zoneQ = $("quiz");
  if (zoneQ) {
    var QUESTIONS = [
      ["Le miel peut être donné à bébé dès 6 mois.", false, "Pas de miel avant 1 an, même dans une préparation : il peut contenir la bactérie responsable du botulisme infantile."],
      ["Un bébé doit être couché sur le dos pour dormir.", true, "C'est la position recommandée pour réduire le risque de mort inattendue du nourrisson."],
      ["Retarder l'œuf et l'arachide évite les allergies.", false, "C'est l'inverse : les allergènes peuvent être introduits dès le début de la diversification, sans attendre."],
      ["Une poussée dentaire peut donner une forte fièvre (39 °C).", false, "Une poussée dentaire ne donne pas de forte fièvre. Au-delà de 38,5 °C, cherchez une autre cause et consultez si besoin."],
      ["Les experts recommandent zéro écran avant 3 ans.", true, "C'est la recommandation de la commission « Enfants et écrans » (2024)."],
      ["Les colliers d'ambre sont conseillés pour les dents.", false, "Ils sont déconseillés : risque d'étranglement et d'étouffement, sans efficacité prouvée."],
      ["On peut commencer la diversification dès 3 mois.", false, "Jamais avant 4 mois révolus. Elle commence entre 4 et 6 mois."],
      ["Pendant une terreur nocturne, il faut réveiller l'enfant.", false, "Mieux vaut ne pas le réveiller : restez près de lui pour qu'il ne se blesse pas, l'épisode passe tout seul."],
      ["Parler deux langues à la maison retarde le langage.", false, "Le bilinguisme ne crée pas de retard de langage."],
      ["Le dentifrice fluoré s'utilise dès la première dent.", true, "Oui, une trace (grain de riz) de dentifrice à 1 000 ppm de fluor, deux fois par jour."],
      ["La propreté de nuit arrive souvent après celle du jour.", true, "Oui, et c'est normal de porter une couche la nuit jusqu'à 4 ou 5 ans."],
      ["Dire « tu es doué » motive plus que « tu as bien travaillé ».", false, "Féliciter l'effort encourage l'enfant à relever des défis ; féliciter le « don » le rend plus prudent."],
      ["Il faut parfois proposer un aliment 8 à 10 fois avant qu'il soit accepté.", true, "Oui ! Proposer sans forcer, plusieurs fois, sous différentes formes."],
      ["Le lait de vache peut remplacer le lait infantile avant 1 an.", false, "Avant 1 an, le lait de vache ne couvre pas les besoins de bébé (notamment en fer)."],
      ["Secouer un bébé, même brièvement, peut causer des lésions graves.", true, "Oui. Si vous êtes à bout, posez bébé en sécurité dans son lit, sortez de la pièce et appelez quelqu'un."],
      ["Partir en cachette de la crèche évite les pleurs et rassure l'enfant.", false, "Au contraire : il se sent trahi. Un au revoir court et toujours le même rassure bien plus."],
      ["Les fruits à coque entiers sont déconseillés avant 5 ans.", true, "Oui, à cause du risque d'étouffement. Les raisins et tomates cerises se coupent en 4."],
      ["« Faire ses nuits » veut dire dormir 12 heures d'affilée.", false, "Chez un bébé, on parle de « faire ses nuits » à partir d'environ 6 heures d'affilée."],
      ["Le 3018 est le numéro contre le harcèlement à l'école et en ligne.", true, "Oui : gratuit, anonyme, et joignable aussi par tchat et sur l'appli 3018."],
      ["Lire une histoire à un bébé de 6 mois ne sert à rien : il ne comprend pas.", false, "Au contraire : il entend la musique de la langue, découvre les images et partage un moment avec vous."]
    ];
    var serie = [], idx = 0, score = 0;
    function demarrer() {
      serie = melanger(QUESTIONS).slice(0, 10); idx = 0; score = 0;
      $("q-fin").style.display = "none"; $("q-jeu").style.display = "block"; poser();
    }
    function poser() {
      var q = serie[idx];
      $("q-num").textContent = "Question " + (idx + 1) + " / 10";
      $("q-barre").style.width = (idx / 10 * 100) + "%";
      $("q-score").textContent = score + " ✓";
      var c = $("q-carte"); c.classList.remove("entre"); void c.offsetWidth; c.classList.add("entre");
      $("q-texte").textContent = q[0];
      $("q-expli").className = "q-expli"; $("q-expli").innerHTML = "";
      $("q-suivant").style.display = "none";
      zoneQ.querySelectorAll("[data-rep]").forEach(function (b) { b.disabled = false; b.classList.remove("bon", "faux"); });
    }
    zoneQ.addEventListener("click", function (e) {
      var b = e.target.closest("[data-rep]"); if (!b || b.disabled) return;
      var q = serie[idx], rep = b.getAttribute("data-rep") === "vrai", juste = rep === q[1];
      zoneQ.querySelectorAll("[data-rep]").forEach(function (x) { x.disabled = true; if ((x.getAttribute("data-rep") === "vrai") === q[1]) x.classList.add("bon"); });
      if (!juste) b.classList.add("faux");
      if (juste) { score++; PS.gagner("quiz", 2, null, false); }
      $("q-score").textContent = score + " ✓";
      $("q-expli").innerHTML = "<strong>" + (juste ? "🎉 Bonne réponse !" : "😅 Raté !") + "</strong> " + esc(q[2]);
      $("q-expli").className = "q-expli visible " + (juste ? "ok" : "ko");
      $("q-suivant").style.display = "inline-flex"; $("q-suivant").focus();
      $("q-suivant").textContent = idx === 9 ? "Voir mon score" : "Question suivante →";
    });
    $("q-suivant").addEventListener("click", function () {
      idx++;
      if (idx < 10) { poser(); return; }
      $("q-barre").style.width = "100%";
      var meilleur = Math.max(lire("ps-quiz", 0), score); ecrire("ps-quiz", meilleur);
      $("q-jeu").style.display = "none"; $("q-fin").style.display = "block";
      var msg = score === 10 ? ["🏆", "Sans faute !", "Vous êtes incollable."] : score >= 7 ? ["🌟", "Excellent !", "Vous connaissez très bien le sujet."] : score >= 4 ? ["👍", "Pas mal !", "Quelques articles à lire pour devenir incollable."] : ["🌱", "C'est un début !", "Les articles du site vont vous aider."];
      $("q-fin").innerHTML = '<div class="q-ico">' + msg[0] + '</div><h2>' + msg[1] + " " + score + "/10</h2><p>" + msg[2] + "</p><p class='mention-aff'>Meilleur score : " + meilleur + "/10</p><p><button class='btn' type='button' id='q-rejouer'>Rejouer avec d'autres questions</button> <a class='btn clair' href='conseils.html'>Lire les conseils</a></p>";
      $("q-rejouer").addEventListener("click", demarrer);
      if (score === 10) PS.gagner("quiz_parfait", 20, "quiz10");
      if (score >= 7) PS.confettis();
    });
    demarrer();
  }
})();
