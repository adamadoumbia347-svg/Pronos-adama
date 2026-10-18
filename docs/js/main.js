(function () {
  var cfg = window.AFFILIATION || {};
  var boutiques = cfg.boutiques || { fr: { nom: "Amazon.fr", domaine: "amazon.fr", tag: "" } };
  var langue = (document.documentElement.lang || "fr").slice(0, 2);
  // Boutique du visiteur : pays du navigateur, sinon langue de la page.
  function boutiqueDuVisiteur() {
    var parPays = cfg.boutiqueParPays || {};
    var langues = navigator.languages || [navigator.language || ""];
    var defaut = (cfg.boutiqueParLangue || {})[langue];
    if (!boutiques[defaut]) defaut = Object.keys(boutiques)[0];
    for (var i = 0; i < langues.length; i++) {
      var pays = (langues[i].split("-")[1] || "").toUpperCase();
      if (!pays) continue;
      var code = parPays[pays];
      if (code && boutiques[code] && boutiques[code].tag) return code;
      // Visiteur européen dont la boutique n'a pas encore d'identifiant : on l'envoie vers
      // la boutique de la page si elle en a un, sinon vers la boutique de secours (Amazon.fr livre toute l'Europe).
      if ((cfg.europe || []).indexOf(pays) !== -1) {
        if (boutiques[defaut].tag) return defaut;
        if (cfg.secoursEurope && boutiques[cfg.secoursEurope]) return cfg.secoursEurope;
      }
      if (code && boutiques[code]) return code;
    }
    return defaut;
  }

  // Construit chaque lien produit : lien personnalisé si défini, sinon recherche Amazon taguée.
  function construireLiens(code, racine) {
    var b = boutiques[code];
    var perso = (cfg.liensPersonnalises || {})[code] || {};
    (racine || document).querySelectorAll("a.aff").forEach(function (a) {
      var id = a.getAttribute("data-aff");
      var recherche = a.getAttribute("data-q") || a.textContent.trim();
      var url;
      if (id && perso[id]) {
        url = perso[id];
      } else {
        url = "https://www." + b.domaine + "/s?k=" + encodeURIComponent(recherche);
        if (b.tag) url += "&tag=" + encodeURIComponent(b.tag);
      }
      a.href = url;
      a.target = "_blank";
      a.rel = "sponsored nofollow noopener";
    });
  }

  var boutique = boutiqueDuVisiteur();
  construireLiens(boutique);
  // Pour les contenus ajoutés après le chargement (quiz, calculateur)
  window.lierProduits = function (racine) { construireLiens(boutique, racine); };

  // Articles : sommaire automatique et barre de progression de lecture
  var article = document.querySelector(".container.article");
  if (article) {
    var TXT = { fr: "Sommaire", en: "Contents", it: "Indice" };
    var titres = article.querySelectorAll("h2");
    if (titres.length >= 3) {
      var details = document.createElement("details");
      details.className = "toc-art";
      details.open = window.innerWidth > 820;
      var liste = document.createElement("ol");
      titres.forEach(function (h, i) {
        if (!h.id) h.id = "partie-" + (i + 1);
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = "#" + h.id;
        a.textContent = h.textContent;
        li.appendChild(a);
        liste.appendChild(li);
      });
      details.innerHTML = "<summary>📑 " + (TXT[langue] || TXT.fr) + "</summary>";
      details.appendChild(liste);
      var apres = article.querySelector(".lead");
      if (apres) apres.insertAdjacentElement("afterend", details);
    }
    var barre = document.createElement("div");
    barre.className = "lecture";
    barre.setAttribute("aria-hidden", "true");
    document.body.appendChild(barre);
    var majBarre = function () {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight;
      var k = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 1;
      barre.style.transform = "scaleX(" + k + ")";
    };
    window.addEventListener("scroll", majBarre, { passive: true });
    majBarre();
  }

  // Menu mobile
  var bouton = document.querySelector(".nav-toggle");
  var menu = document.querySelector(".nav-links");
  if (bouton && menu) {
    bouton.addEventListener("click", function () {
      var ouvert = menu.classList.toggle("open");
      bouton.setAttribute("aria-expanded", ouvert ? "true" : "false");
    });
  }

  // Filtres du catalogue de méthodes
  var filtres = document.querySelectorAll("[data-filter-group]");
  var methodes = document.querySelectorAll(".method");
  var recherche = document.getElementById("method-search");
  var compteur = document.getElementById("method-count");
  var etat = { animal: "tous", niveau: "tous" };

  function appliquer() {
    var texte = recherche ? recherche.value.trim().toLowerCase() : "";
    var visibles = 0;
    methodes.forEach(function (m) {
      var animaux = (m.getAttribute("data-animals") || "").split(" ");
      var ok =
        (etat.animal === "tous" || animaux.indexOf(etat.animal) !== -1) &&
        (etat.niveau === "tous" || m.getAttribute("data-level") === etat.niveau) &&
        (!texte || m.textContent.toLowerCase().indexOf(texte) !== -1);
      m.hidden = !ok;
      if (ok) visibles++;
    });
    var mots = { fr: ["méthode", "méthodes"], en: ["method", "methods"], it: ["metodo", "metodi"] }[langue] || ["méthode", "méthodes"];
    if (compteur) compteur.textContent = visibles + " " + mots[visibles > 1 ? 1 : 0];
  }

  filtres.forEach(function (groupe) {
    var cle = groupe.getAttribute("data-filter-group");
    groupe.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () {
        groupe.querySelectorAll("button").forEach(function (x) {
          x.setAttribute("aria-pressed", "false");
        });
        b.setAttribute("aria-pressed", "true");
        etat[cle] = b.getAttribute("data-value");
        appliquer();
      });
    });
  });
  if (recherche) recherche.addEventListener("input", appliquer);

  // Pré-filtre via l'URL : methodes.html?animal=chat
  var params = new URLSearchParams(location.search);
  var animalUrl = params.get("animal");
  if (animalUrl) {
    var b = document.querySelector('[data-filter-group="animal"] button[data-value="' + animalUrl + '"]');
    if (b) b.click();
  }
  if (methodes.length) appliquer();

  // Recherche dans le site : loupe dans le bandeau, résultats instantanés (index recherche.json de la langue)
  (function () {
    var nav = document.querySelector(".site-header .nav");
    if (!nav) return;
    var T = {
      fr: ["Rechercher", "Rechercher un conseil, une méthode, un produit…", "Aucun résultat. Essayez un autre mot (ex. : rappel, griffoir, chiot).", "Fermer", "résultat", "résultats"],
      en: ["Search", "Search for a tip, a method, some gear…", "No results. Try another word (e.g. recall, scratching post, puppy).", "Close", "result", "results"],
      it: ["Cerca", "Cerca un consiglio, un metodo, un accessorio…", "Nessun risultato. Prova un'altra parola (es. richiamo, tiragraffi, cucciolo).", "Chiudi", "risultato", "risultati"]
    }[langue] || [];
    if (!T.length) return;
    var btn = document.createElement("button");
    btn.className = "btn-recherche";
    btn.type = "button";
    btn.setAttribute("aria-label", T[0]);
    btn.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>';
    var toggle = nav.querySelector(".nav-toggle");
    nav.insertBefore(btn, toggle);

    var fenetre = document.createElement("div");
    fenetre.className = "recherche";
    fenetre.hidden = true;
    fenetre.setAttribute("role", "dialog");
    fenetre.setAttribute("aria-label", T[0]);
    fenetre.innerHTML = '<div class="recherche-boite"><div class="recherche-ligne"><input type="search" autocomplete="off"><button type="button" class="recherche-fermer">✕</button></div><p class="recherche-info"></p><ul class="recherche-resultats"></ul></div>';
    document.body.appendChild(fenetre);
    var champ = fenetre.querySelector("input"), liste = fenetre.querySelector("ul"), info = fenetre.querySelector(".recherche-info");
    champ.placeholder = T[1];
    champ.setAttribute("aria-label", T[0]);
    fenetre.querySelector(".recherche-fermer").setAttribute("aria-label", T[3]);

    var index = null;
    function normal(t) { return (t || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
    function charger() {
      if (index) return Promise.resolve(index);
      return fetch("recherche.json").then(function (r) { return r.json(); }).then(function (d) {
        index = d.map(function (p) { return { p: p, t: normal(p.t), h: normal(p.h), d: normal(p.d), x: normal(p.x) }; });
        return index;
      });
    }
    function chercher() {
      var q = normal(champ.value).trim();
      liste.innerHTML = "";
      info.textContent = "";
      if (q.length < 2 || !index) return;
      var mots = q.split(/\s+/).filter(function (m) { return m.length > 1; });
      var res = index.map(function (e) {
        var score = 0;
        for (var i = 0; i < mots.length; i++) {
          var m = mots[i], s = 0;
          if (e.t.indexOf(m) !== -1) s += 10;
          if (e.h.indexOf(m) !== -1) s += 4;
          if (e.d.indexOf(m) !== -1) s += 3;
          if (e.x.indexOf(m) !== -1) s += 1;
          if (!s) return null;   // tous les mots doivent être trouvés
          score += s;
        }
        return { e: e, score: score };
      }).filter(Boolean).sort(function (a, b) { return b.score - a.score; }).slice(0, 12);
      if (!res.length) { info.textContent = T[2]; return; }
      info.textContent = res.length + " " + T[res.length > 1 ? 5 : 4];
      res.forEach(function (r) {
        var li = document.createElement("li"), a = document.createElement("a"), t = document.createElement("strong"), d = document.createElement("span");
        a.href = r.e.p.u;
        t.textContent = r.e.p.t;
        d.textContent = r.e.p.d;
        a.appendChild(t); a.appendChild(d); li.appendChild(a); liste.appendChild(li);
      });
    }
    function ouvrir() {
      fenetre.hidden = false;
      document.body.classList.add("recherche-ouverte");
      champ.focus();
      charger().then(chercher);
    }
    function fermer() {
      fenetre.hidden = true;
      document.body.classList.remove("recherche-ouverte");
      btn.focus();
    }
    btn.addEventListener("click", ouvrir);
    fenetre.querySelector(".recherche-fermer").addEventListener("click", fermer);
    fenetre.addEventListener("click", function (e) { if (e.target === fenetre) fermer(); });
    champ.addEventListener("input", chercher);
    champ.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { var a = liste.querySelector("a"); if (a) location.href = a.href; }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !fenetre.hidden) fermer();
      if (e.key === "/" && fenetre.hidden && !/input|textarea/i.test((document.activeElement || {}).tagName || "")) { e.preventDefault(); ouvrir(); }
    });
  })();

  // Boutons de partage (articles et pages du site)
  (function () {
    var main = document.querySelector("main");
    if (!main || document.querySelector(".partage")) return;
    var lang = (document.documentElement.lang || "fr").slice(0, 2);
    var T = {
      fr: { titre: "Partager cette page", partager: "Partager", copier: "Copier le lien", copie: "Lien copié ✓", mail: "E-mail" },
      en: { titre: "Share this page", partager: "Share", copier: "Copy link", copie: "Link copied ✓", mail: "Email" },
      it: { titre: "Condividi questa pagina", partager: "Condividi", copier: "Copia link", copie: "Link copiato ✓", mail: "E-mail" }
    }[lang] || {};
    var can = document.querySelector('link[rel="canonical"]');
    var url = can ? can.href : location.href;
    var titre = document.title;
    var img = document.querySelector('meta[property="og:image"]');
    var u = encodeURIComponent(url), t = encodeURIComponent(titre);
    var liens = [
      ["whatsapp", "💬", "WhatsApp", "https://wa.me/?text=" + t + "%20" + u],
      ["facebook", "f", "Facebook", "https://www.facebook.com/sharer/sharer.php?u=" + u],
      ["pinterest", "P", "Pinterest", "https://pinterest.com/pin/create/button/?url=" + u + "&description=" + t + (img ? "&media=" + encodeURIComponent(img.content) : "")],
      ["x", "𝕏", "X", "https://twitter.com/intent/tweet?url=" + u + "&text=" + t],
      ["mail", "✉", T.mail, "mailto:?subject=" + t + "&body=" + u]
    ];
    function bloc() {
      var d = document.createElement("div"); d.className = "partage";
      var h = document.createElement("p"); h.className = "partage-titre"; h.textContent = T.titre; d.appendChild(h);
      var r = document.createElement("div"); r.className = "partage-liens"; d.appendChild(r);
      if (navigator.share) {
        var n = document.createElement("button"); n.type = "button"; n.className = "partage-btn partage-natif";
        n.innerHTML = '<span class="partage-ic" aria-hidden="true">↗</span>' + T.partager;
        n.addEventListener("click", function () { navigator.share({ title: titre, url: url }).catch(function () {}); });
        r.appendChild(n);
      }
      liens.forEach(function (l) {
        var a = document.createElement("a"); a.className = "partage-btn partage-" + l[0]; a.href = l[3];
        if (l[0] !== "mail") { a.target = "_blank"; a.rel = "noopener"; }
        a.innerHTML = '<span class="partage-ic" aria-hidden="true">' + l[1] + "</span>" + l[2];
        r.appendChild(a);
      });
      var c = document.createElement("button"); c.type = "button"; c.className = "partage-btn partage-copier";
      c.innerHTML = '<span class="partage-ic" aria-hidden="true">🔗</span><span>' + T.copier + "</span>";
      c.addEventListener("click", function () {
        var ok = function () { c.lastChild.textContent = T.copie; setTimeout(function () { c.lastChild.textContent = T.copier; }, 2000); };
        if (navigator.clipboard) navigator.clipboard.writeText(url).then(ok, function () {});
        else { var i = document.createElement("input"); i.value = url; document.body.appendChild(i); i.select(); try { document.execCommand("copy"); ok(); } catch (e) {} i.remove(); }
      });
      r.appendChild(c);
      return d;
    }
    var article = document.querySelector(".article");
    if (article) article.appendChild(bloc());
    else {
      var wrap = document.createElement("section"); wrap.className = "container";
      wrap.appendChild(bloc());
      var avant = main.querySelector(".lire-aussi");
      if (avant) main.insertBefore(wrap, avant); else main.appendChild(wrap);
    }
  })();

  var annee = document.getElementById("annee");
  if (annee) annee.textContent = new Date().getFullYear();
})();
