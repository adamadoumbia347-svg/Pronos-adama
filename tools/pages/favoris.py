"""Page « Mes favoris » (FR / EN / IT) : la liste est remplie par docs/js/main.js (stockage du navigateur).

Usage : python3 tools/pages/favoris.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import creer_page  # noqa: E402

T = {
 "fr": ("Mes favoris", "Retrouvez les articles et fiches que vous avez enregistrés sur Éduc'Animaux, pour les relire quand vous voulez.",
        "Accueil", "Vos articles enregistrés", "Les favoris sont gardés uniquement dans ce navigateur, sur cet appareil : rien n'est envoyé ni stocké ailleurs.",
        '<a class="btn" href="conseils.html">Voir tous les conseils</a>', "❤️ Mes favoris"),
 "en": ("My favourites", "Find the articles and profiles you saved on Éduc'Animaux, to read again whenever you like.",
        "Home", "Your saved articles", "Favourites are kept only in this browser, on this device: nothing is sent or stored anywhere else.",
        '<a class="btn" href="conseils.html">See all tips</a>', "❤️ My favourites"),
 "it": ("I miei preferiti", "Ritrova gli articoli e le schede che hai salvato su Éduc'Animaux, per rileggerli quando vuoi.",
        "Home", "I tuoi articoli salvati", "I preferiti restano solo in questo browser, su questo dispositivo: niente viene inviato o salvato altrove.",
        '<a class="btn" href="conseils.html">Vedi tutti i consigli</a>', "❤️ I miei preferiti"),
}

if __name__ == "__main__":
    for lang, (titre, desc, fil, h2, note, lien, menu) in T.items():
        corps = f"""    <section class="page-hero">
      <div class="container">
        <p class="breadcrumb"><a href="index.html">{fil}</a> › {titre}</p>
        <h1>❤️ {titre}</h1>
        <p class="lead">{desc}</p>
        <h2>{h2}</h2>
        <div id="liste-favoris"></div>
        <p class="small muted">{note}</p>
        <div class="btn-row">{lien}</div>
      </div>
    </section>"""
        creer_page.creer(lang, "favoris", titre, desc, corps, menu=menu)
    creer_page.finir()
    print("favoris ok")
