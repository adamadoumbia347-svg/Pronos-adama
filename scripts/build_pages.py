#!/usr/bin/env python3
"""Génère les pages trajets, les pages légales, le sitemap et la liste des guides de la page d'accueil.

Lancer : python3 scripts/build_pages.py   (Netlify le lance aussi à chaque déploiement)
"""
import datetime
import html
import pathlib
import re
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DOMAIN = "https://escale-voyage.netlify.app"
TODAY = datetime.date.today().isoformat()

# from, to, ville départ, ville arrivée, pays, aéroport arrivée, durée directe (ou None), haute saison, note
ROUTES = [
    ("CDG", "BKO", "Paris", "Bamako", "Mali", "Aéroport international Modibo-Keïta", None,
     "juillet-août, les fêtes de fin d'année et la Tabaski",
     "Les vols directs depuis Paris sont rares ou suspendus selon les périodes : la plupart des trajets passent par Casablanca, Alger, Tunis, Istanbul ou Addis-Abeba. Comparez la durée totale, pas seulement le prix."),
    ("CDG", "DSS", "Paris", "Dakar", "Sénégal", "Aéroport international Blaise-Diagne (AIBD), à environ 45 km de Dakar", "5 h 30",
     "juillet-août, les fêtes de fin d'année, la Tabaski et le Magal de Touba",
     "Des vols partent aussi d'Orly : cochez les deux aéroports parisiens dans les comparateurs pour élargir le choix."),
    ("CDG", "ABJ", "Paris", "Abidjan", "Côte d'Ivoire", "Aéroport international Félix-Houphouët-Boigny", "6 h 30",
     "juillet-août et les fêtes de fin d'année",
     "Plusieurs compagnies desservent la ligne depuis Roissy et Orly : la concurrence fait souvent baisser les prix en basse saison."),
    ("CDG", "CKY", "Paris", "Conakry", "Guinée", "Aéroport international de Conakry-Gbessia", "6 h",
     "juillet-août et les fêtes de fin d'année",
     "Les vols avec escale à Casablanca, Dakar ou Bruxelles sont parfois nettement moins chers que le direct."),
    ("CDG", "DLA", "Paris", "Douala", "Cameroun", "Aéroport international de Douala", "6 h 30",
     "juillet-août et les fêtes de fin d'année",
     "Pensez aussi à Yaoundé-Nsimalen (NSI) si votre destination finale est dans le centre du pays."),
    ("CDG", "LFW", "Paris", "Lomé", "Togo", "Aéroport international Gnassingbé-Eyadéma", "6 h",
     "juillet-août et les fêtes de fin d'année",
     "Comparez avec un vol vers Cotonou (COO) ou Accra (ACC), puis la route : c'est parfois moins cher."),
    ("CDG", "COO", "Paris", "Cotonou", "Bénin", "Aéroport international Cardinal-Bernardin-Gantin de Cotonou-Cadjehoun", "6 h",
     "juillet-août et les fêtes de fin d'année",
     "Comparez avec Lomé (LFW) : les deux villes sont proches et les prix varient beaucoup."),
    ("CDG", "OUA", "Paris", "Ouagadougou", "Burkina Faso", "Aéroport international de Ouagadougou", None,
     "juillet-août et les fêtes de fin d'année",
     "L'offre de vols directs varie selon la situation : les trajets avec escale via Abidjan, Casablanca, Alger ou Istanbul sont fréquents."),
    ("BRU", "FIH", "Bruxelles", "Kinshasa", "RD Congo", "Aéroport international de N'djili", "8 h",
     "juillet-août et les fêtes de fin d'année",
     "Depuis Paris, comparez avec un départ de Bruxelles : il est souvent plus avantageux, même en ajoutant le train."),
    ("ORY", "CMN", "Paris", "Casablanca", "Maroc", "Aéroport Mohammed-V", "3 h",
     "juillet-août, les vacances scolaires et l'Aïd",
     "Les compagnies low-cost desservent aussi Marrakech, Rabat et Tanger : regardez la ville la plus proche de votre destination."),
    ("CDG", "ALG", "Paris", "Alger", "Algérie", "Aéroport Houari-Boumédiène", "2 h 15",
     "juillet-août, l'Aïd et les vacances scolaires",
     "Comparez avec Lyon, Marseille ou Bordeaux si vous pouvez partir d'une autre ville : les prix d'été changent beaucoup d'un aéroport à l'autre."),
    ("CDG", "TUN", "Paris", "Tunis", "Tunisie", "Aéroport international de Tunis-Carthage", "2 h 15",
     "juillet-août et l'Aïd",
     "Pensez aussi à Djerba (DJE) et Monastir (MIR), souvent desservis par des vols moins chers en été."),
    ("CDG", "YUL", "Paris", "Montréal", "Canada", "Aéroport international Montréal-Trudeau", "7 h 30",
     "juillet-août et les fêtes de fin d'année",
     "Une autorisation de voyage électronique (AVE) est exigée pour la plupart des voyageurs : vérifiez avant de réserver."),
    ("CDG", "DXB", "Paris", "Dubaï", "Émirats arabes unis", "Aéroport international de Dubaï", "6 h 45",
     "de novembre à mars, quand il fait moins chaud",
     "Dubaï est aussi une escale pratique vers l'Asie et l'Afrique de l'Est : un stop de quelques jours ne coûte parfois rien de plus."),
]

def slug(t):
    t = t.lower().replace("'", "-")
    for a, b in (("é", "e"), ("è", "e"), ("ê", "e"), ("ë", "e"), ("à", "a"), ("â", "a"), ("ï", "i"), ("î", "i"), ("ô", "o"), ("û", "u"), ("ü", "u"), ("ç", "c")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

def route_slug(r):
    return f"vol-{slug(r[2])}-{slug(r[3])}"

E = html.escape

HEAD = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#18202c">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="manifest" href="/manifest.webmanifest">
<meta property="og:type" content="article">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Escale">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{domain}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@700&display=swap">
<link rel="stylesheet" href="/pages.css">
{ld}
</head>
<body>
<header class="board"><div class="wrap">
  <a class="brand" href="/"><span class="brand-mark">ESC</span><span class="brand-name">Escale</span></a>
  {hero}
</div></header>
<main class="wrap">
{body}
</main>
<footer class="wrap">
  <nav class="foot-nav" aria-label="Pages du site"><a href="/">Comparer vols, hôtels et voitures</a><a href="/#guides">Guides des trajets</a><a href="/mentions-legales/">Mentions légales</a><a href="/confidentialite/">Confidentialité</a><a href="/contact/">Contact</a></nav>
  <p>Escale ne vend pas de billets et ne fixe aucun prix. Les durées et informations sont indicatives : les programmes des compagnies changent, vérifiez toujours sur le site de réservation.</p>
</footer>
</body>
</html>
"""

def page(path, title, desc, hero, body, ld=""):
    url = f"{DOMAIN}/{path}" if path else f"{DOMAIN}/"
    out = HEAD.format(title=E(title), desc=E(desc), url=url, domain=DOMAIN, hero=hero, body=body, ld=ld)
    d = SITE / path
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(out, encoding="utf-8")
    return url

def route_page(r):
    fr, to, cf, ct, country, airport, dur, peak, note = r
    s = route_slug(r)
    title = f"Vol pas cher {cf} {ct} : comparer les prix"
    desc = (f"Trouvez un billet d'avion pas cher {cf} – {ct} ({fr} → {to}) : durée du vol, aéroport, meilleure période pour réserver "
            f"et comparaison des prix sur Google Flights, Skyscanner, Kayak et momondo.")
    app = "/?" + urllib.parse.urlencode({"type": "vols", "from": fr, "to": to})
    back = "/?" + urllib.parse.urlencode({"type": "vols", "from": to, "to": fr})
    hotels = "/?" + urllib.parse.urlencode({"type": "hotels", "dest": ct})
    cars = "/?" + urllib.parse.urlencode({"type": "voitures", "pick": to})
    gf = "https://www.google.com/travel/flights?" + urllib.parse.urlencode({"q": f"Flights from {fr} to {to}", "hl": "fr", "curr": "EUR"})
    sky = f"https://www.skyscanner.fr/transport/vols/{fr.lower()}/{to.lower()}/"
    dur_txt = f"environ {dur} en vol direct" if dur else "variable : la plupart des trajets ont au moins une escale"
    faq = [
        (f"Combien de temps dure un vol {cf} – {ct} ?", f"Comptez {dur_txt}. Avec une escale, le trajet total dure souvent plusieurs heures de plus selon la correspondance."),
        (f"Quand réserver un vol {cf} – {ct} pas cher ?", f"En général deux à trois mois avant le départ. Les prix montent fortement pendant {peak} : réservez plus tôt pour ces périodes."),
        (f"Quel aéroport à {ct} ?", f"Les vols arrivent à l'{airport[0].lower() + airport[1:]} (code {to})."),
        ("Les bagages sont-ils inclus ?", "Pas toujours. Les tarifs les plus bas n'incluent parfois qu'un petit sac. Vérifiez la franchise bagage en soute avant de payer, surtout si vous voyagez avec des valises."),
    ]
    ld = '<script type="application/ld+json">' + __import__("json").dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    }, ensure_ascii=False) + "</script>"
    hero = f"""<p class="eyebrow">{E(country)}</p>
  <h1>Vol pas cher {E(cf)} <span>→</span> {E(ct)}</h1>
  <p class="codes">{fr} → {to}</p>
  <div class="cta-row"><a class="btn" href="{E(app)}">Comparer les prix maintenant</a><a class="btn ghost" href="{E(back)}">Trajet retour {E(ct)} → {E(cf)}</a></div>"""
    facts = f"""<dl class="facts">
  <div><dt>Durée</dt><dd>{E(dur_txt[0].upper() + dur_txt[1:])}</dd></div>
  <div><dt>Arrivée</dt><dd>{E(airport)} ({to})</dd></div>
  <div><dt>Prix les plus hauts</dt><dd>{E(peak[0].upper() + peak[1:])}</dd></div>
</dl>"""
    body = f"""{facts}
<section><h2>Notre conseil pour ce trajet</h2><p>{E(note)}</p></section>
<section><h2>Comment payer moins cher</h2>
<ol class="steps">
  <li><strong>Activez les dates flexibles.</strong> Décaler le départ d'un ou deux jours change souvent plus le prix que le choix du site.</li>
  <li><strong>Comparez au moins trois sites.</strong> Escale ouvre votre recherche déjà triée par prix sur Google Flights, Skyscanner, Kayak et momondo.</li>
  <li><strong>Vérifiez les bagages.</strong> Ajoutez le prix de la valise avant de comparer deux tarifs.</li>
  <li><strong>Créez une alerte prix</strong> sur Google Flights ou Kayak si vous partez dans plusieurs mois.</li>
</ol>
<p><a class="btn" href="{E(app)}">Lancer la recherche {E(cf)} → {E(ct)}</a></p>
</section>
<section><h2>Accès direct aux comparateurs</h2>
<ul class="links">
  <li><a href="{E(gf)}" target="_blank" rel="noopener noreferrer">Calendrier des prix sur Google Flights</a></li>
  <li><a href="{E(sky)}" target="_blank" rel="noopener noreferrer">Prix du mois sur Skyscanner</a></li>
  <li><a href="{E(hotels)}">Hôtels à {E(ct)}</a></li>
  <li><a href="{E(cars)}">Location de voiture à {E(ct)}</a></li>
</ul></section>
<section class="faq"><h2>Questions fréquentes</h2>
{''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)}
</section>
<section><h2>Autres trajets</h2><ul class="route-links">{''.join(f'<li><a href="/{route_slug(o)}/">{E(o[2])} → {E(o[3])}</a></li>' for o in ROUTES if o is not r)}</ul></section>"""
    return page(s, title, desc, hero, body, ld)

def legal_pages():
    urls = []
    hero = '<h1>Mentions légales</h1>'
    body = """<section><h2>Éditeur du site</h2>
<p>Le site Escale (escale-voyage.netlify.app) est édité à titre non professionnel.</p>
<p>Conformément à l'article 6, III-2 de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie numérique, l'éditeur non professionnel peut ne tenir à la disposition du public que le nom et l'adresse de son hébergeur, après lui avoir communiqué ses éléments d'identification.</p>
<p>Contact : <a href="/contact/">formulaire de contact</a>.</p>
</section>
<section><h2>Hébergeur</h2>
<p>Netlify, Inc.<br>512 2nd Street, Suite 200<br>San Francisco, CA 94107, États-Unis<br>netlify.com</p>
</section>
<section><h2>Nature du service</h2>
<p>Escale est un outil de recherche gratuit. Il ne vend aucun billet, nuit d'hôtel ou location et ne fixe aucun prix. Chaque bouton « Voir les prix » ouvre une recherche sur un site tiers, qui est seul responsable de ses tarifs, de ses conditions et des réservations.</p>
<p>Certains liens peuvent être des liens partenaires : si vous réservez, Escale peut percevoir une commission, sans surcoût pour vous.</p>
</section>
<section><h2>Propriété intellectuelle</h2>
<p>Les textes et le design du site sont la propriété de l'éditeur. Les marques citées (Google Flights, Skyscanner, Kayak, momondo, Booking.com, Hotels.com, Agoda, Airbnb, Rentalcars, Discover Cars) appartiennent à leurs propriétaires respectifs et sont citées uniquement pour identifier les services comparés.</p>
</section>"""
    urls.append(page("mentions-legales", "Mentions légales | Escale", "Mentions légales du site Escale, comparateur de vols, hôtels et locations de voitures.", hero, body))
    hero = '<h1>Confidentialité</h1>'
    body = """<section><h2>En bref</h2>
<p>Escale ne demande aucun compte, ne collecte ni nom, ni e-mail, ni numéro de téléphone, et n'utilise aucun cookie publicitaire ou de suivi.</p>
</section>
<section><h2>Ce qui reste sur votre appareil</h2>
<p>Vos dernières recherches et le dernier onglet utilisé sont enregistrés dans le stockage local de votre navigateur, uniquement pour vous les reproposer. Ces données ne quittent pas votre appareil. Vous pouvez les effacer à tout moment en supprimant les données du site dans votre navigateur.</p>
</section>
<section><h2>Prix indicatifs</h2>
<p>Pour afficher un prix indicatif, le site envoie le trajet et les dates recherchés (par exemple CDG → BKO en novembre) à notre serveur, qui interroge un fournisseur de données de prix. Aucune donnée personnelle n'est transmise.</p>
</section>
<section><h2>Hébergement</h2>
<p>Comme tout hébergeur, Netlify enregistre des journaux techniques (adresse IP, page demandée, date) nécessaires au fonctionnement et à la sécurité du site.</p>
</section>
<section><h2>Sites partenaires</h2>
<p>Quand vous cliquez sur « Voir les prix », vous quittez Escale. Le site ouvert (Google, Skyscanner, Booking, etc.) applique sa propre politique de confidentialité et ses propres cookies.</p>
</section>
<section><h2>Vos droits</h2>
<p>Conformément au RGPD, vous pouvez demander l'accès, la rectification ou l'effacement de données vous concernant. Escale ne détenant aucune donnée personnelle sur ses visiteurs, aucune information ne peut normalement vous être rattachée.</p>
</section>"""
    urls.append(page("confidentialite", "Confidentialité | Escale", "Politique de confidentialité du site Escale : aucun compte, aucun cookie de suivi.", hero, body))
    hero = '<h1>Contact</h1>'
    body = """<section><p>Une question, une erreur sur le site, une destination à ajouter ? Écrivez-nous. Pour une réservation, contactez directement le site où vous avez réservé : Escale ne gère aucune réservation.</p>
<form class="contact" name="contact" method="POST" action="/contact/merci/" data-netlify="true" netlify-honeypot="site-web">
  <input type="hidden" name="form-name" value="contact">
  <p class="hp"><label>Ne pas remplir : <input name="site-web"></label></p>
  <label for="c-nom">Votre nom</label><input id="c-nom" name="nom" autocomplete="name">
  <label for="c-mail">Votre e-mail</label><input id="c-mail" name="email" type="email" autocomplete="email" required>
  <label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required></textarea>
  <button class="btn" type="submit">Envoyer</button>
</form>
<p class="small">Votre e-mail sert uniquement à vous répondre.</p></section>"""
    urls.append(page("contact", "Contact | Escale", "Contacter l'équipe Escale : question, erreur, destination à ajouter.", hero, body))
    page("contact/merci", "Message envoyé | Escale", "Merci pour votre message.", "<h1>Message envoyé</h1>",
         '<section><p>Merci, votre message est bien arrivé. Nous vous répondrons par e-mail.</p><p><a class="btn" href="/">Retour à la recherche</a></p></section>')
    return urls

def main():
    urls = [f"{DOMAIN}/"]
    urls += [route_page(r) for r in ROUTES]
    urls += legal_pages()

    # Liste des guides sur la page d'accueil
    idx = SITE / "index.html"
    s = idx.read_text(encoding="utf-8")
    links = '<ul class="route-links">' + "".join(
        f'<li><a href="/{route_slug(r)}/">Vol {E(r[2])} → {E(r[3])}</a></li>' for r in ROUTES) + "</ul>"
    s = re.sub(r"<!-- ROUTES:START -->.*?<!-- ROUTES:END -->",
               "<!-- ROUTES:START -->\n    " + links + "\n    <!-- ROUTES:END -->", s, flags=re.S)
    idx.write_text(s, encoding="utf-8")

    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    print(f"{len(urls)} pages dans le sitemap")

if __name__ == "__main__":
    main()
