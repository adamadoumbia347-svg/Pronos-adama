/* Parents Sereins — liens d'affiliation, animations et options (thème, favoris, taille du texte, partage) */
(function () {
  var doc = document.documentElement;
  var mouvementReduit = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function lire(cle, defaut) { try { var v = localStorage.getItem(cle); return v === null ? defaut : JSON.parse(v); } catch (e) { return defaut; } }
  function ecrire(cle, v) { try { localStorage.setItem(cle, JSON.stringify(v)); } catch (e) { /* navigation privée */ } }

  /* ---------- Thème clair / sombre ---------- */
  var THEMES = ["auto", "light", "dark"], ICONES = { auto: "🌗", light: "☀️", dark: "🌙" }, NOMS = { auto: "automatique", light: "clair", dark: "sombre" };
  function appliquerTheme(t) {
    if (t === "auto") doc.removeAttribute("data-theme"); else doc.setAttribute("data-theme", t);
    var b = document.getElementById("theme");
    if (b) { b.textContent = ICONES[t]; b.setAttribute("aria-label", "Thème : " + NOMS[t] + " (changer)"); b.title = "Thème " + NOMS[t]; }
  }
  var theme = lire("ps-theme", "auto");
  appliquerTheme(theme);
  var btnTheme = document.getElementById("theme");
  if (btnTheme) btnTheme.addEventListener("click", function () {
    theme = THEMES[(THEMES.indexOf(theme) + 1) % 3];
    ecrire("ps-theme", theme); appliquerTheme(theme); toast("Thème " + NOMS[theme]);
  });

  /* ---------- Liens d'affiliation ---------- */
  var cfg = window.AFFILIATION || {};
  var boutiques = cfg.boutiques || { fr: { nom: "Amazon.fr", domaine: "amazon.fr", tag: "" } };
  function boutiqueDuVisiteur() {
    var defaut = boutiques.fr ? "fr" : Object.keys(boutiques)[0];
    var langues = navigator.languages || [navigator.language || ""];
    for (var i = 0; i < langues.length; i++) {
      var pays = (langues[i].split("-")[1] || "").toUpperCase();
      if (!pays) continue;
      var code = (cfg.boutiqueParPays || {})[pays];
      if (code && boutiques[code] && boutiques[code].tag) return code;
      if ((cfg.europe || []).indexOf(pays) !== -1) return defaut;
    }
    return defaut;
  }
  var code = boutiqueDuVisiteur();
  function construireLiens(racine) {
    var b = boutiques[code];
    var perso = (cfg.liensPersonnalises || {})[code] || {};
    (racine || document).querySelectorAll("a.aff").forEach(function (a) {
      var id = a.getAttribute("data-aff");
      var q = a.getAttribute("data-q") || a.textContent.trim();
      a.href = id && perso[id] ? perso[id]
        : "https://www." + b.domaine + "/s?k=" + encodeURIComponent(q) + (b.tag ? "&tag=" + encodeURIComponent(b.tag) : "");
      a.target = "_blank";
      a.rel = "sponsored nofollow noopener";
    });
  }
  construireLiens();
  window.lierProduits = construireLiens;

  /* ---------- Petit message ---------- */
  var toastEl;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("visible");
    clearTimeout(toastEl._t); toastEl._t = setTimeout(function () { toastEl.classList.remove("visible"); }, 2200);
  }
  window.toast = toast;

  /* ---------- Menu mobile ---------- */
  var burger = document.querySelector(".burger"), menu = document.querySelector("nav.menu");
  if (burger && menu) burger.addEventListener("click", function () {
    var ouvert = menu.classList.toggle("ouvert");
    burger.setAttribute("aria-expanded", ouvert ? "true" : "false");
    burger.textContent = ouvert ? "✕" : "☰";
  });

  /* ---------- Article : sommaire, temps de lecture, outils ---------- */
  var contenu = document.querySelector(".contenu-article");
  if (contenu) {
    var mots = contenu.textContent.trim().split(/\s+/).length;
    var duree = document.querySelector(".duree");
    if (duree) duree.textContent = "⏱ " + Math.max(1, Math.round(mots / 220)) + " min de lecture";
    var titres = contenu.querySelectorAll("h2");
    if (titres.length >= 3) {
      var s = document.createElement("nav"); s.className = "sommaire"; s.setAttribute("aria-label", "Sommaire");
      var html = "<strong>Au sommaire</strong><ol>";
      titres.forEach(function (h, i) { h.id = h.id || "partie-" + (i + 1); html += '<li><a href="#' + h.id + '">' + h.textContent + "</a></li>"; });
      s.innerHTML = html + "</ol>";
      contenu.insertBefore(s, titres[0]);
    }
    // Taille du texte
    var taille = lire("ps-taille", 1);
    function majTaille() { contenu.style.setProperty("--taille", taille); }
    majTaille();
    document.querySelectorAll("[data-taille]").forEach(function (b) {
      b.addEventListener("click", function () {
        taille = Math.min(1.3, Math.max(.9, Math.round((taille + parseFloat(b.getAttribute("data-taille"))) * 10) / 10));
        ecrire("ps-taille", taille); majTaille();
      });
    });
    // Partage
    var partage = document.getElementById("partager");
    if (partage) partage.addEventListener("click", function () {
      var d = { title: document.title, url: location.href };
      if (navigator.share) { navigator.share(d).catch(function () {}); return; }
      if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(function () { toast("Lien copié 📋"); }, function () { toast(location.href); });
      else toast(location.href);
    });
  }

  /* ---------- Favoris ---------- */
  var favoris = lire("ps-favoris", []);
  function majPastille(anim) {
    document.querySelectorAll(".pastille-favoris").forEach(function (p) {
      p.textContent = favoris.length || "";
      if (anim) { p.classList.remove("pop"); void p.offsetWidth; p.classList.add("pop"); }
    });
  }
  majPastille();
  var page = location.pathname.split("/").pop() || "index.html";
  var btnFav = document.getElementById("favori");
  if (btnFav) {
    var estFavori = function () { return favoris.some(function (f) { return f.url === page; }); };
    var majBtn = function () {
      var oui = estFavori();
      btnFav.setAttribute("aria-pressed", oui ? "true" : "false");
      btnFav.querySelector(".libelle").textContent = oui ? "Enregistré" : "Enregistrer";
    };
    majBtn();
    btnFav.addEventListener("click", function () {
      if (estFavori()) { favoris = favoris.filter(function (f) { return f.url !== page; }); toast("Retiré de vos favoris"); }
      else {
        var img = document.querySelector(".photo-article img");
        favoris.push({ url: page, titre: document.querySelector("h1").textContent, image: img ? img.getAttribute("src") : "", desc: (document.querySelector(".chapeau") || {}).textContent || "" });
        toast("Ajouté à vos favoris ❤️");
      }
      ecrire("ps-favoris", favoris); majBtn(); majPastille(true);
    });
  }
  var listeFav = document.getElementById("liste-favoris");
  if (listeFav) {
    var dessinerFav = function () {
      document.getElementById("favoris-vide").style.display = favoris.length ? "none" : "block";
      listeFav.innerHTML = favoris.map(function (f) {
        var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
        if (!/^[a-z0-9-]+\.html$/.test(f.url)) return "";
        return '<div class="carte vu" style="padding-bottom:16px">' + (f.image ? '<div class="photo"><img src="' + esc(f.image) + '" alt="" loading="lazy"></div>' : "") +
          '<h3><a href="' + f.url + '" style="color:inherit;text-decoration:none">' + esc(f.titre) + '</a></h3><p>' + esc(f.desc).slice(0, 120) + '…</p>' +
          '<p style="margin-top:12px;display:flex;gap:8px"><a class="btn petit" href="' + f.url + '">Lire</a><button class="pilule" data-retirer="' + f.url + '">Retirer</button></p></div>';
      }).join("");
    };
    listeFav.addEventListener("click", function (e) {
      var u = e.target.getAttribute("data-retirer");
      if (!u) return;
      favoris = favoris.filter(function (f) { return f.url !== u; });
      ecrire("ps-favoris", favoris); dessinerFav(); majPastille(true);
    });
    dessinerFav();
  }

  /* ---------- Apparition au défilement ---------- */
  var cibles = document.querySelectorAll(".grille > *, .produit, .contenu-article > h2, .encadre, .outil, details, .tableau, .bandeau-photo, .section-titre, .chiffres > div, .liste-coche li");
  cibles.forEach(function (el) {
    if (el.hasAttribute("data-reveal")) return;
    el.setAttribute("data-reveal", el.matches(".produit") ? "gauche" : el.matches(".bandeau-photo") ? "zoom" : "");
    var parent = el.parentElement, freres = parent ? Array.prototype.indexOf.call(parent.children, el) : 0;
    if (parent && (parent.matches(".grille") || parent.matches(".chiffres"))) el.style.setProperty("--delai", (freres % 4) * 0.09 + "s");
  });
  if ("IntersectionObserver" in window && !mouvementReduit) {
    var obs = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("vu"); obs.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    document.querySelectorAll("[data-reveal]").forEach(function (el) { obs.observe(el); });
  } else {
    document.querySelectorAll("[data-reveal]").forEach(function (el) { el.classList.add("vu"); });
  }

  /* ---------- Compteurs animés ---------- */
  document.querySelectorAll("[data-compte]").forEach(function (el) {
    var fin = parseInt(el.getAttribute("data-compte"), 10), suffixe = el.getAttribute("data-suffixe") || "";
    if (mouvementReduit) { el.textContent = fin + suffixe; return; }
    var t0 = null;
    function pas(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / 1600), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(fin * e) + suffixe;
      if (p < 1) requestAnimationFrame(pas);
    }
    setTimeout(function () { requestAnimationFrame(pas); }, 600);
  });

  /* ---------- Défilement : en-tête, barre de lecture, parallaxe, retour en haut ---------- */
  var header = document.querySelector("header.site");
  var barre = document.querySelector(".barre-lecture");
  var parallaxes = document.querySelectorAll(".bandeau-photo img");
  var haut = document.createElement("button");
  haut.className = "haut"; haut.setAttribute("aria-label", "Revenir en haut"); haut.textContent = "↑";
  haut.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: mouvementReduit ? "auto" : "smooth" }); });
  document.body.appendChild(haut);
  var attente = false;
  function surDefilement() {
    attente = false;
    var y = window.scrollY, h = doc.scrollHeight - innerHeight;
    if (header) header.classList.toggle("defile", y > 10);
    haut.classList.toggle("visible", y > 700);
    if (barre) barre.style.transform = "scaleX(" + (h > 0 ? y / h : 0) + ")";
    if (!mouvementReduit) parallaxes.forEach(function (img) {
      var r = img.parentElement.getBoundingClientRect();
      if (r.bottom > 0 && r.top < innerHeight) img.style.transform = "translateY(" + ((r.top - innerHeight) * 0.12) + "px)";
    });
  }
  window.addEventListener("scroll", function () { if (!attente) { attente = true; requestAnimationFrame(surDefilement); } }, { passive: true });
  surDefilement();

  document.querySelectorAll(".annee").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
