/* Outils interactifs : calculateur d'âge (#calc-age) et quiz (#quiz). Textes en fr / en / it. */
(function () {
  var L = (document.documentElement.lang || "fr").slice(0, 2);
  if (!{ fr: 1, en: 1, it: 1 }[L]) L = "fr";
  var esc = function (s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; };
  var lier = function (el) { if (window.lierProduits) window.lierProduits(el); };

  // ---------- Données communes ----------
  var METHODES = {
    "renforcement-positif": ["Renforcement positif", "Positive reinforcement", "Rinforzo positivo"],
    "clicker": ["Clicker training", "Clicker training", "Clicker training"],
    "leurre": ["Le leurre", "Luring", "L'adescamento"],
    "capture": ["La capture", "Capturing", "La cattura"],
    "faconnage": ["Le façonnage", "Shaping", "Lo shaping"],
    "ciblage": ["Le ciblage", "Targeting", "Il targeting"],
    "desensibilisation": ["Désensibilisation", "Desensitisation", "Desensibilizzazione"],
    "gestion": ["Gestion de l'environnement", "Managing the environment", "Gestione dell'ambiente"],
    "socialisation": ["Socialisation", "Socialisation", "Socializzazione"],
    "cooperative-care": ["Soins coopératifs", "Cooperative care", "Cure cooperative"],
    "premack": ["Principe de Premack", "The Premack principle", "Principio di Premack"],
    "rien-gratuit": ["Apprendre à mériter", "Learn to Earn", "Guadagnarsi le cose"],
    "lat": ["« Regarde ça » (LAT)", "Look At That (LAT)", "«Guarda quello» (LAT)"],
    "bat": ["BAT", "BAT", "BAT"],
    "extinction": ["Ignorer + renforcer l'alternative", "Ignore + reward the alternative", "Ignorare + premiare l'alternativa"],
    "modele-rival": ["Modèle-rival", "Model/rival method", "Metodo modello/rivale"]
  };
  var IDX = { fr: 0, en: 1, it: 2 };
  // Pages du site (titres par langue ; null = page absente dans cette langue)
  var PAGES = {
    "rappel-chien.html": ["Apprendre le rappel en 7 étapes", "Teach a reliable recall in 7 steps", "Il richiamo in 7 tappe"],
    "marche-en-laisse.html": ["Chien qui tire en laisse", "Dog pulling on the lead", "Il cane tira al guinzaglio"],
    "chat-griffe-canape.html": ["Chat qui griffe le canapé", "Cat scratching the sofa", "Il gatto graffia il divano"],
    "chiot-mord.html": ["Mon chiot mord : que faire ?", "My puppy bites: what to do?", "Il mio cucciolo morde"],
    "proprete-chiot.html": ["La propreté du chiot", "House training your puppy", "La pulizia del cucciolo"],
    "meilleur-harnais-chien.html": ["Quel harnais choisir ?", null, null],
    "meilleur-griffoir-chat.html": ["Quel griffoir choisir ?", null, null],
    "meilleur-clicker.html": ["Quel clicker choisir ?", null, null],
    "chien.html": ["Le guide complet du chien", "The complete dog guide", "La guida completa del cane"],
    "chien.html#solitude": ["Apprendre à rester seul", "Learning to be left alone", "Imparare a restare da solo"],
    "chien.html#aboiements": ["Les aboiements", "Barking", "L'abbaio"],
    "chat.html": ["Le guide complet du chat", "The complete cat guide", "La guida completa del gatto"],
    "nac.html": ["Lapins, rongeurs et furets", "Rabbits, rodents and ferrets", "Conigli, roditori e furetti"],
    "nac.html#lapin": ["Éduquer son lapin", "Training your rabbit", "Educare il coniglio"],
    "nac.html#oiseau": ["Éduquer son oiseau", "Training your bird", "Educare l'uccello"],
    "methodes.html": ["Toutes les méthodes", "Every method", "Tutti i metodi"]
  };
  var REMPLACE = { "meilleur-harnais-chien.html": "chien.html", "meilleur-griffoir-chat.html": "chat-griffe-canape.html", "meilleur-clicker.html": "methodes.html" };
  function page(href) {
    var t = PAGES[href][IDX[L]];
    if (t === null) { href = REMPLACE[href]; t = PAGES[href][IDX[L]]; }
    return '<a href="' + href + '">' + esc(t) + "</a>";
  }
  function methode(id) { return '<a href="methodes.html#' + id + '">' + esc(METHODES[id][IDX[L]]) + "</a>"; }
  // Produits : libellé + recherche Amazon par langue
  var PRODUITS = {
    "longe": [["Longe de 10 m", "longe dressage chien 10m"], ["10 m long line", "long line dog training 10m"], ["Lunghina da 10 m", "lunghina addestramento cane 10 metri"]],
    "sifflet": [["Sifflet de rappel", "sifflet dressage chien"], ["Recall whistle", "dog training whistle"], ["Fischietto per il richiamo", "fischietto addestramento cane"]],
    "harnais": [["Harnais en Y", "harnais chien en Y"], ["Y-shaped harness", "y front dog harness"], ["Pettorina a Y", "pettorina cane a Y"]],
    "jouet-dentition": [["Jouets de dentition", "jouet dentition chiot"], ["Teething toys", "puppy teething toys"], ["Giochi per la dentizione", "giochi dentizione cucciolo"]],
    "kong": [["Jouet à garnir", "jouet kong chien"], ["Stuffable toy", "kong dog toy"], ["Gioco da riempire", "kong cane"]],
    "griffoir": [["Griffoir haut et stable", "griffoir chat haut stable sisal"], ["Tall scratching post", "tall sturdy cat scratching post"], ["Tiragraffi alto", "tiragraffi alto stabile"]],
    "nettoyant-enzymatique": [["Nettoyant enzymatique", "nettoyant enzymatique urine"], ["Enzymatic cleaner", "enzyme cleaner pet urine"], ["Detergente enzimatico", "detergente enzimatico urina"]],
    "litiere": [["Litière sans parfum", "litière agglomérante sans parfum"], ["Unscented litter", "unscented clumping cat litter"], ["Lettiera non profumata", "lettiera agglomerante non profumata"]],
    "litiere-lapin": [["Litière végétale", "litière végétale lapin"], ["Paper-based litter", "paper rabbit litter"], ["Lettiera vegetale", "lettiera vegetale coniglio"]],
    "diffuseur-apaisant": [["Diffuseur apaisant", "diffuseur phéromones apaisant"], ["Calming diffuser", "pheromone calming diffuser"], ["Diffusore calmante", "diffusore feromoni calmanti"]],
    "tapis-fouille": [["Tapis de fouille", "tapis de fouille chien"], ["Snuffle mat", "snuffle mat dog"], ["Tappeto olfattivo", "tappeto olfattivo cane"]],
    "jouet-intelligence-chat": [["Jeu d'intelligence", "jouet intelligence chat"], ["Puzzle toy", "cat puzzle toy"], ["Gioco di attivazione", "gioco di attivazione gatto"]],
    "canne-plumes": [["Canne à plumes", "canne plumes chat"], ["Feather wand", "feather wand cat toy"], ["Canna con piume", "canna con piume gatto"]],
    "jouets-fourragement": [["Jouets de fourragement", "jouet fourragement oiseau"], ["Foraging toys", "bird foraging toy"], ["Giochi di foraging", "gioco foraging uccelli"]],
    "jeux-rongeurs": [["Jouets d'enrichissement", "jouets enrichissement rongeurs"], ["Enrichment toys", "small animal enrichment toys"], ["Giochi di arricchimento", "giochi arricchimento roditori"]],
    "clicker": [["Clicker", "clicker dressage animaux"], ["Clicker", "pet training clicker"], ["Clicker", "clicker addestramento"]],
    "target-stick": [["Kit clicker + baguette", "clicker target stick"], ["Clicker + target stick", "clicker target stick"], ["Clicker + target stick", "clicker target stick addestramento"]],
    "friandises": [["Friandises d'éducation", "friandises éducation chien"], ["Training treats", "small soft dog training treats"], ["Premietti", "premietti addestramento cane"]],
    "friandise-liquide": [["Friandises liquides", "friandise liquide chat"], ["Lickable treats", "lickable cat treats"], ["Snack cremosi", "snack cremoso gatto"]]
  };
  function produits(cles) {
    return cles.map(function (k) {
      var p = PRODUITS[k][IDX[L]];
      return '<a class="btn btn-sm aff" data-aff="' + k + '" data-q="' + esc(p[1]) + '" href="#">🛒 ' + esc(p[0]) + "</a>";
    }).join(" ");
  }
  function partager(btn, titre) {
    btn.addEventListener("click", function () {
      var url = location.href.split("#")[0];
      if (navigator.share) { navigator.share({ title: titre, url: url }).catch(function () {}); return; }
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { btn.textContent = T.copie; });
    });
  }

  var T = {
    fr: { copie: "✅ Lien copié !", partager: "📤 Partager", recommence: "↺ Recommencer",
      methodes: "Les méthodes à utiliser", lire: "À lire", materiel: "Le matériel utile",
      vet: "Un changement soudain de comportement mérite une visite chez le vétérinaire : une douleur peut en être la cause." },
    en: { copie: "✅ Link copied!", partager: "📤 Share", recommence: "↺ Start again",
      methodes: "Methods to use", lire: "Read", materiel: "Useful gear",
      vet: "A sudden change in behaviour is worth a vet visit: pain can be the cause." },
    it: { copie: "✅ Link copiato!", partager: "📤 Condividi", recommence: "↺ Ricomincia",
      methodes: "I metodi da usare", lire: "Da leggere", materiel: "Gli accessori utili",
      vet: "Un cambiamento improvviso di comportamento merita una visita dal veterinario: la causa può essere un dolore." }
  }[L];

  // ---------- Calculateur d'âge ----------
  var calc = document.getElementById("calc-age");
  if (calc) {
    var C = {
      fr: { ans: "ans", humain: "en âge humain", estim: "Estimation : l'âge réel dépend aussi de la race et de la santé.",
        etapes: { chiot: "🍼 Chiot", jeune: "⚡ Jeune adulte", adulte: "💪 Adulte", senior: "🧓 Senior", chaton: "🍼 Chaton", junior: "⚡ Junior", mature: "😺 Adulte mûr" },
        conseils: {
          chiot: "La période idéale pour la socialisation et les premiers apprentissages : propreté, mordillements, séances très courtes.",
          jeune: "L'âge de l'énergie… et des bêtises ! C'est le bon moment pour solidifier le rappel et la marche en laisse.",
          adulte: "Il peut apprendre toute sa vie : tours au clicker, jeux de flair et exercices pour garder son esprit en forme.",
          senior: "Privilégiez des séances courtes et douces, les jeux de flair et les soins coopératifs. Un bilan vétérinaire régulier est conseillé.",
          chaton: "La période idéale pour lui apprendre la litière, le griffoir et la manipulation en douceur.",
          junior: "Plein d'énergie : prévoyez des jeux de chasse quotidiens et redirigez les griffades vers un griffoir.",
          mature: "Gardez-le actif avec des jeux d'intelligence et habituez-le aux soins (griffes, brossage) avant qu'il ne vieillisse." } },
      en: { ans: "years", humain: "in human years", estim: "Estimate: the real figure also depends on breed and health.",
        etapes: { chiot: "🍼 Puppy", jeune: "⚡ Young adult", adulte: "💪 Adult", senior: "🧓 Senior", chaton: "🍼 Kitten", junior: "⚡ Junior", mature: "😺 Mature adult" },
        conseils: {
          chiot: "The ideal time for socialisation and first lessons: house training, puppy biting, very short sessions.",
          jeune: "The age of energy… and mischief! A great time to strengthen recall and loose-lead walking.",
          adulte: "Dogs keep learning all their lives: clicker tricks, sniffing games and exercises to keep the mind sharp.",
          senior: "Choose short, gentle sessions, sniffing games and cooperative care. Regular vet check-ups are recommended.",
          chaton: "The ideal time to teach the litter tray, the scratching post and gentle handling.",
          junior: "Full of energy: plan daily hunting games and redirect scratching to a scratching post.",
          mature: "Keep your cat active with puzzle toys and get it used to care (nails, brushing) before it gets older." } },
      it: { ans: "anni", humain: "in età umana", estim: "Stima: l'età reale dipende anche dalla razza e dalla salute.",
        etapes: { chiot: "🍼 Cucciolo", jeune: "⚡ Giovane adulto", adulte: "💪 Adulto", senior: "🧓 Anziano", chaton: "🍼 Gattino", junior: "⚡ Junior", mature: "😺 Adulto maturo" },
        conseils: {
          chiot: "Il periodo ideale per la socializzazione e i primi apprendimenti: pulizia, morsi, sessioni brevissime.",
          jeune: "L'età dell'energia… e delle marachelle! Il momento giusto per consolidare richiamo e guinzaglio.",
          adulte: "Il cane impara per tutta la vita: trucchi con il clicker, giochi di fiuto ed esercizi per tenere la mente in forma.",
          senior: "Preferisci sessioni brevi e delicate, giochi di fiuto e cure cooperative. Sono consigliati controlli veterinari regolari.",
          chaton: "Il periodo ideale per insegnare la lettiera, il tiragraffi e la manipolazione delicata.",
          junior: "Pieno di energia: prevedi giochi di caccia quotidiani e reindirizza i graffi verso un tiragraffi.",
          mature: "Tienilo attivo con giochi di attivazione e abitualo alle cure (unghie, spazzola) prima che invecchi." } }
    }[L];
    var LIENS = {
      chiot: ["proprete-chiot.html", "chiot-mord.html"], jeune: ["rappel-chien.html", "marche-en-laisse.html"],
      adulte: ["methodes.html", "meilleur-harnais-chien.html"], senior: ["chien.html", "methodes.html"],
      chaton: ["chat.html", "chat-griffe-canape.html"], junior: ["chat-griffe-canape.html", "meilleur-griffoir-chat.html"],
      mature: ["chat.html", "methodes.html"]
    };
    var form = calc.querySelector("form"), sortie = calc.querySelector(".resultat");
    var champTaille = calc.querySelector("[data-taille]");
    var majTaille = function () { champTaille.hidden = form.espece.value !== "chien"; };
    form.addEventListener("change", majTaille); majTaille();
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var age = (parseFloat(form.annees.value) || 0) + (parseInt(form.mois.value, 10) || 0) / 12;
      if (age <= 0) { form.annees.focus(); return; }
      var chien = form.espece.value === "chien", taille = form.taille.value;
      var pente = chien ? { petit: 4, moyen: 5, grand: 6 }[taille] : 4;
      var h = age <= 1 ? 15 * age : age <= 2 ? 15 + 9 * (age - 1) : 24 + pente * (age - 2);
      var etape;
      if (chien) etape = age < 1 ? "chiot" : age < 3 ? "jeune" : age >= (taille === "grand" ? 6 : 7) ? "senior" : "adulte";
      else etape = age < 1 ? "chaton" : age < 3 ? "junior" : age < 7 ? "adulte" : age < 11 ? "mature" : "senior";
      var conseil = C.conseils[etape === "adulte" && !chien ? "mature" : etape === "senior" && !chien ? "senior" : etape];
      var liens = (etape === "senior" && !chien) ? ["chat.html", "methodes.html"] : LIENS[etape === "adulte" && !chien ? "mature" : etape];
      sortie.innerHTML = '<div class="card resultat-carte"><div class="age-gros">≈ ' + Math.round(h) + " " + esc(C.ans) +
        '</div><p class="muted">' + esc(C.humain) + '</p><p><span class="tag green">' + esc(C.etapes[etape]) + "</span></p>" +
        "<p>" + esc(conseil) + "</p><p>📖 " + liens.map(page).join(" · ") + '</p><p class="muted small">' + esc(C.estim) + "</p>" +
        '<div class="btn-row"><button type="button" class="btn btn-sm partager">' + esc(T.partager) + "</button></div></div>";
      partager(sortie.querySelector(".partager"), document.title);
      sortie.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  }

  // ---------- Quiz ----------
  var quiz = document.getElementById("quiz");
  if (quiz) {
    var Q = {
      fr: { question: "Question", sur: "sur", retour: "← Retour", titreRes: "Notre recommandation", pour: { chien: "pour votre chien", chat: "pour votre chat", nac: "pour votre petit compagnon", oiseau: "pour votre oiseau" },
        q: ["Quel est votre animal ?", "Quel est le problème principal ?", "Quel âge a-t-il ?", "Combien de temps pouvez-vous y consacrer par jour ?"],
        animaux: { chien: "🐕 Un chien", chat: "🐈 Un chat", nac: "🐇 Un lapin, rongeur ou furet", oiseau: "🦜 Un oiseau" },
        pb: { rappel: "Il ne vient pas quand je l'appelle", laisse: "Il tire en laisse", mord: "Il mord ou mordille", proprete: "Il fait ses besoins au mauvais endroit",
          peur: "Il a peur (bruits, gens, vétérinaire…)", ennui: "Il s'ennuie ou fait des bêtises", bruit: "Il est trop bruyant", tours: "Je veux lui apprendre des tours" },
        pbAnimal: { chat: { mord: "Il griffe ou mord (meubles, mains)", bruit: "Il miaule beaucoup (la nuit…)" }, chien: { bruit: "Il aboie trop" }, oiseau: { bruit: "Il crie trop", mord: "Il pince ou mord" }, nac: { mord: "Il mord ou pince" } },
        ages: { bebe: "Bébé (moins d'un an)", adulte: "Adulte", senior: "Âgé" },
        temps: { t5: "⏱️ 5 minutes", t15: "⏱️ 15 minutes", t30: "⏱️ 30 minutes ou plus" },
        noteAge: { bebe: "Bébé : séances de 2-3 minutes, plusieurs fois par jour, avec beaucoup de socialisation.", adulte: "Il n'est jamais trop tard pour apprendre : la régularité fait tout.", senior: "Animal âgé : séances courtes et douces. Une douleur peut expliquer certains comportements, pensez au bilan vétérinaire." },
        noteTemps: { t5: "5 minutes suffisent : 1 ou 2 mini-séances bien ciblées chaque jour.", t15: "Idéal : 2 ou 3 séances de 5 minutes par jour.", t30: "Super ! Répartissez ce temps en plusieurs séances courtes plutôt qu'une longue." } },
      en: { question: "Question", sur: "of", retour: "← Back", titreRes: "Our recommendation", pour: { chien: "for your dog", chat: "for your cat", nac: "for your small pet", oiseau: "for your bird" },
        q: ["What pet do you have?", "What's the main problem?", "How old is it?", "How much time can you spend on it each day?"],
        animaux: { chien: "🐕 A dog", chat: "🐈 A cat", nac: "🐇 A rabbit, rodent or ferret", oiseau: "🦜 A bird" },
        pb: { rappel: "It doesn't come when called", laisse: "It pulls on the lead", mord: "It bites or nips", proprete: "It goes to the toilet in the wrong place",
          peur: "It's scared (noises, people, the vet…)", ennui: "It's bored or gets into mischief", bruit: "It's too noisy", tours: "I want to teach it tricks" },
        pbAnimal: { chat: { mord: "It scratches or bites (furniture, hands)", bruit: "It meows a lot (at night…)" }, chien: { bruit: "It barks too much" }, oiseau: { bruit: "It screams too much", mord: "It nips or bites" }, nac: { mord: "It bites or nips" } },
        ages: { bebe: "Baby (under a year)", adulte: "Adult", senior: "Senior" },
        temps: { t5: "⏱️ 5 minutes", t15: "⏱️ 15 minutes", t30: "⏱️ 30 minutes or more" },
        noteAge: { bebe: "Baby: 2-3 minute sessions, several times a day, with lots of socialisation.", adulte: "It's never too late to learn: consistency is everything.", senior: "Older pet: short, gentle sessions. Pain can explain some behaviours, so consider a vet check-up." },
        noteTemps: { t5: "5 minutes is enough: 1 or 2 focused mini-sessions every day.", t15: "Ideal: 2 or 3 five-minute sessions a day.", t30: "Great! Split this time into several short sessions rather than one long one." } },
      it: { question: "Domanda", sur: "di", retour: "← Indietro", titreRes: "Il nostro consiglio", pour: { chien: "per il tuo cane", chat: "per il tuo gatto", nac: "per il tuo piccolo amico", oiseau: "per il tuo uccello" },
        q: ["Che animale hai?", "Qual è il problema principale?", "Quanti anni ha?", "Quanto tempo puoi dedicarci ogni giorno?"],
        animaux: { chien: "🐕 Un cane", chat: "🐈 Un gatto", nac: "🐇 Un coniglio, roditore o furetto", oiseau: "🦜 Un uccello" },
        pb: { rappel: "Non viene quando lo chiamo", laisse: "Tira al guinzaglio", mord: "Morde o mordicchia", proprete: "Fa i bisogni nel posto sbagliato",
          peur: "Ha paura (rumori, persone, veterinario…)", ennui: "Si annoia o combina guai", bruit: "È troppo rumoroso", tours: "Voglio insegnargli dei trucchi" },
        pbAnimal: { chat: { mord: "Graffia o morde (mobili, mani)", bruit: "Miagola molto (di notte…)" }, chien: { bruit: "Abbaia troppo" }, oiseau: { bruit: "Urla troppo", mord: "Pizzica o morde" }, nac: { mord: "Morde o pizzica" } },
        ages: { bebe: "Cucciolo (meno di un anno)", adulte: "Adulto", senior: "Anziano" },
        temps: { t5: "⏱️ 5 minuti", t15: "⏱️ 15 minuti", t30: "⏱️ 30 minuti o più" },
        noteAge: { bebe: "Cucciolo: sessioni di 2-3 minuti, più volte al giorno, con tanta socializzazione.", adulte: "Non è mai troppo tardi per imparare: la costanza è tutto.", senior: "Animale anziano: sessioni brevi e delicate. Un dolore può spiegare alcuni comportamenti, pensa a un controllo veterinario." },
        noteTemps: { t5: "5 minuti bastano: 1 o 2 mini-sessioni mirate ogni giorno.", t15: "Ideale: 2 o 3 sessioni da 5 minuti al giorno.", t30: "Ottimo! Dividi questo tempo in più sessioni brevi invece di una lunga." } }
    }[L];
    // Recommandations : méthodes, pages à lire, produits
    var R = {
      chien: { rappel: [["renforcement-positif", "premack", "gestion"], ["rappel-chien.html"], ["longe", "sifflet"]],
        laisse: [["premack", "renforcement-positif"], ["marche-en-laisse.html", "meilleur-harnais-chien.html"], ["harnais"]],
        mord: [["extinction", "gestion"], ["chiot-mord.html"], ["jouet-dentition", "kong"]],
        proprete: [["renforcement-positif", "gestion"], ["proprete-chiot.html"], ["nettoyant-enzymatique"]],
        peur: [["desensibilisation", "lat", "bat"], ["chien.html"], ["diffuseur-apaisant"]],
        ennui: [["rien-gratuit", "gestion"], ["chien.html#solitude"], ["tapis-fouille", "kong"]],
        bruit: [["extinction", "desensibilisation"], ["chien.html#aboiements"], ["tapis-fouille"]],
        tours: [["clicker", "leurre", "faconnage"], ["meilleur-clicker.html"], ["clicker", "friandises"]] },
      chat: { rappel: [["clicker", "capture"], ["chat.html"], ["friandise-liquide"]],
        mord: [["extinction", "gestion"], ["chat-griffe-canape.html", "meilleur-griffoir-chat.html"], ["griffoir", "canne-plumes"]],
        proprete: [["gestion", "renforcement-positif"], ["chat.html"], ["litiere"]],
        peur: [["desensibilisation", "cooperative-care"], ["chat.html"], ["diffuseur-apaisant"]],
        ennui: [["gestion", "renforcement-positif"], ["chat.html"], ["canne-plumes", "jouet-intelligence-chat"]],
        bruit: [["extinction", "gestion"], ["chat.html"], ["jouet-intelligence-chat"]],
        tours: [["clicker", "ciblage", "capture"], ["meilleur-clicker.html"], ["clicker"]] },
      nac: { rappel: [["ciblage", "clicker"], ["nac.html#lapin"], ["target-stick"]],
        mord: [["extinction", "cooperative-care"], ["nac.html"], ["jeux-rongeurs"]],
        proprete: [["gestion", "renforcement-positif"], ["nac.html#lapin"], ["litiere-lapin"]],
        peur: [["desensibilisation", "cooperative-care"], ["nac.html#lapin"], []],
        ennui: [["gestion", "ciblage"], ["nac.html"], ["jeux-rongeurs"]],
        tours: [["ciblage", "clicker"], ["nac.html#lapin"], ["target-stick"]] },
      oiseau: { rappel: [["ciblage", "clicker"], ["nac.html#oiseau"], ["target-stick"]],
        mord: [["extinction", "desensibilisation"], ["nac.html#oiseau"], ["jouets-fourragement"]],
        peur: [["desensibilisation", "ciblage"], ["nac.html#oiseau"], []],
        ennui: [["gestion", "ciblage"], ["nac.html#oiseau"], ["jouets-fourragement"]],
        bruit: [["extinction", "renforcement-positif"], ["nac.html#oiseau"], ["jouets-fourragement"]],
        tours: [["modele-rival", "ciblage", "clicker"], ["nac.html#oiseau"], ["target-stick"]] }
    };
    var rep = {}, etape = 0;
    var zone = quiz.querySelector(".quiz-zone");
    function bouton(val, txt) { return '<button type="button" class="quiz-choix" data-v="' + val + '">' + esc(txt) + "</button>"; }
    function afficher() {
      var opts = "";
      if (etape === 0) Object.keys(Q.animaux).forEach(function (k) { opts += bouton(k, Q.animaux[k]); });
      if (etape === 1) Object.keys(R[rep.animal]).forEach(function (k) { opts += bouton(k, (Q.pbAnimal[rep.animal] || {})[k] || Q.pb[k]); });
      if (etape === 2) Object.keys(Q.ages).forEach(function (k) { opts += bouton(k, Q.ages[k]); });
      if (etape === 3) Object.keys(Q.temps).forEach(function (k) { opts += bouton(k, Q.temps[k]); });
      zone.innerHTML = '<p class="quiz-etape">' + Q.question + " " + (etape + 1) + " " + Q.sur + ' 4</p><div class="quiz-barre"><i style="width:' + (etape * 25) + '%"></i></div>' +
        "<h2>" + esc(Q.q[etape]) + '</h2><div class="quiz-options">' + opts + "</div>" +
        (etape > 0 ? '<button type="button" class="quiz-retour">' + esc(Q.retour) + "</button>" : "");
      zone.querySelectorAll(".quiz-choix").forEach(function (b) {
        b.addEventListener("click", function () {
          rep[["animal", "pb", "age", "temps"][etape]] = b.getAttribute("data-v");
          etape++; etape < 4 ? afficher() : resultat();
        });
      });
      var r = zone.querySelector(".quiz-retour");
      if (r) r.addEventListener("click", function () { etape--; afficher(); });
    }
    function resultat() {
      var reco = R[rep.animal][rep.pb];
      var pbTexte = (Q.pbAnimal[rep.animal] || {})[rep.pb] || Q.pb[rep.pb];
      var vet = (rep.pb === "proprete" || rep.pb === "peur" || rep.pb === "bruit" || rep.age === "senior") ? '<p class="callout warn">' + esc(T.vet) + "</p>" : "";
      zone.innerHTML = '<div class="quiz-barre"><i style="width:100%"></i></div>' +
        "<h2>🎯 " + esc(Q.titreRes) + " " + esc(Q.pour[rep.animal]) + "</h2>" +
        '<p class="muted">« ' + esc(pbTexte) + " »</p>" +
        "<h3>" + esc(T.methodes) + "</h3><ul>" + reco[0].map(function (m) { return "<li>" + methode(m) + "</li>"; }).join("") + "</ul>" +
        "<h3>" + esc(T.lire) + "</h3><p>📖 " + reco[1].map(page).join(" · ") + "</p>" +
        (reco[2].length ? "<h3>" + esc(T.materiel) + '</h3><div class="btn-row" style="margin-top:8px">' + produits(reco[2]) + "</div>" : "") +
        '<div class="callout"><p>💡 ' + esc(Q.noteAge[rep.age]) + "</p><p>⏱️ " + esc(Q.noteTemps[rep.temps]) + "</p></div>" + vet +
        '<div class="btn-row"><button type="button" class="btn btn-sm partager">' + esc(T.partager) + '</button><button type="button" class="btn btn-sm btn-outline quiz-reset">' + esc(T.recommence) + "</button></div>";
      lier(zone);
      partager(zone.querySelector(".partager"), document.title);
      zone.querySelector(".quiz-reset").addEventListener("click", function () { rep = {}; etape = 0; afficher(); });
      quiz.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    afficher();
  }
})();
