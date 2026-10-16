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

  // Encadré « lettre d'information » : affiché seulement si un formulaire est configuré
  // dans config.js (newsletter.action[langue]). Placé avant « À lire aussi », ou en bas de l'accueil.
  (function () {
    var nl = cfg.newsletter || {};
    var action = (nl.action || {})[langue];
    if (!action) return;
    var T = {
      fr: ["🎁 Le guide offert : les 10 ordres de base", "Recevez gratuitement notre guide PDF illustré, puis un conseil d'éducation par semaine. Désinscription en un clic.", "Votre adresse e-mail", "Je le reçois", "Votre adresse sert uniquement à vous envoyer la lettre d'Éduc'Animaux.", "Merci ! Ouvrez l'e-mail de confirmation que nous venons de vous envoyer (pensez aux spams) : le guide s'ouvre dès que vous cliquez sur le lien."],
      en: ["🎁 Free guide: the 10 basic cues", "Get our free illustrated PDF guide, then one training tip a week. Unsubscribe in one click.", "Your email address", "Send it to me", "Your address is only used to send you the Éduc'Animaux newsletter.", "Thank you! Open the confirmation email we have just sent you (check your spam folder): the guide opens as soon as you click the link."],
      it: ["🎁 Guida in regalo: i 10 comandi di base", "Ricevi gratis la nostra guida PDF illustrata, poi un consiglio educativo a settimana. Disiscrizione in un clic.", "Il tuo indirizzo e-mail", "La voglio", "Il tuo indirizzo serve solo a inviarti la newsletter di Éduc'Animaux.", "Grazie! Apri l'e-mail di conferma che ti abbiamo appena inviato (controlla lo spam): la guida si apre appena clicchi sul link."]
    }[langue] || [];
    if (!T.length) return;
    var bloc = document.createElement("section");
    bloc.className = "newsletter";
    bloc.innerHTML = '<div class="container"><div class="nl-boite"><h2></h2><p></p>' +
      '<form method="post" target="_blank"><input type="email" required autocomplete="email"><button class="btn" type="submit"></button></form>' +
      '<p class="nl-mention"></p></div></div>';
    bloc.querySelector("h2").textContent = T[0];
    bloc.querySelector("p").textContent = T[1];
    var f = bloc.querySelector("form");
    f.action = action;
    var champ = f.querySelector("input");
    champ.name = nl.champ || "EMAIL";
    champ.placeholder = T[2];
    champ.setAttribute("aria-label", T[2]);
    f.querySelector("button").textContent = T[3];
    var caches = nl.champsCaches || {};
    Object.keys(caches).forEach(function (nom) {
      var h = document.createElement("input");
      h.type = "hidden"; h.name = nom; h.value = caches[nom];
      f.appendChild(h);
    });
    // Envoi en arrière-plan puis message de remerciement ; en cas d'échec réseau, envoi classique.
    f.addEventListener("submit", function (e) {
      if (!window.fetch || !window.FormData) return;
      e.preventDefault();
      var bouton = f.querySelector("button");
      bouton.disabled = true;
      fetch(f.action, { method: "POST", body: new FormData(f), mode: "no-cors" })
        .then(function () {
          var merci = document.createElement("p");
          merci.className = "nl-merci";
          merci.textContent = T[5];
          f.replaceWith(merci);
        })
        .catch(function () { bouton.disabled = false; f.submit(); });
    });
    bloc.querySelector(".nl-mention").textContent = T[4];
    var ancre = document.querySelector(".lire-aussi") || document.querySelector("main > section:last-of-type");
    if (ancre && ancre.parentNode) ancre.parentNode.insertBefore(bloc, document.querySelector(".lire-aussi") ? ancre : ancre.nextSibling);
  })();

  // Page produit : bouton d'achat si un lien est configuré, sinon « Bientôt disponible »
  (function () {
    var bouton = document.getElementById("bouton-achat");
    if (!bouton) return;
    var prod = (cfg.produits || {}).programmeChiot || {};
    if (prod.prix) document.getElementById("prix-produit").textContent = prod.prix;
    if (prod.url) {
      bouton.href = prod.url;
      bouton.hidden = false;
      document.getElementById("bientot").hidden = true;
    }
  })();

  var annee = document.getElementById("annee");
  if (annee) annee.textContent = new Date().getFullYear();
})();
