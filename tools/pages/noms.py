"""Page « Noms de chien et de chat 2026 (lettre B) et 2027 (lettre C) » avec générateur (français).

Usage : python3 tools/pages/noms.py
La lettre de l'année concerne les chiens inscrits au LOF : elle change le 1er janvier dans l'ordre
alphabétique, sans K, Q, W, X, Y ni Z (2025 = A, 2026 = B, 2027 = C…). Simple recommandation.
"""
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import creer_page  # noqa: E402

# nom, sexe (m / f / u = les deux), styles, espèces (c = chien, t = chat)
N = """
Balto m original c|Bandit m original ct|Baloo m mignon ct|Barney m classique c|Basile m classique ct|Benji m mignon c
Bilbo m original ct|Biscuit u gourmand ct|Blues m original c|Bob m classique ct|Bolt m original c|Boris m classique ct
Boston m original c|Brownie u gourmand ct|Bruno m classique c|Buddy m mignon c|Buzz m original ct|Byron m original ct
Bambou u nature ct|Banjo u original c|Bowie m original ct|Balthazar m classique t|Bagheera m original t|Berlioz m original t
Bastet f original t|Bella f classique ct|Belle f classique ct|Betty f classique ct|Bianca f classique ct|Billie f mignon ct
Blanche f classique ct|Blossom f mignon ct|Bonnie f classique ct|Brune f nature c|Bulle f mignon ct|Bambi f mignon ct
Bijou u mignon ct|Biba f mignon ct|Brindille f nature ct|Babette f classique ct|Bora f nature c|Berlingot u gourmand ct
Brioche f gourmand ct|Biscotte f gourmand ct|Bounty u gourmand ct|Bonbon u gourmand ct|Brume f nature ct|Baie f nature t
Boule u mignon t|Babou m mignon t|Bluebell f mignon t|Beignet u gourmand ct|Bagel u gourmand c|Bouleau m nature c
Caramel u gourmand ct|Cachou u gourmand ct|Câlin m mignon ct|Capitaine m original c|Casper m original ct|Cassius m classique c
Charlie u classique ct|Chester m classique ct|Chico m mignon c|Choco u gourmand ct|Cookie u gourmand ct|Cooper m classique c
Copain m mignon c|Cosmo m original ct|Crumble u gourmand ct|Cyrus m classique c|César m classique ct|Cachemire u original t
Cali f mignon ct|Camille f classique ct|Candy f gourmand ct|Cannelle f gourmand ct|Capucine f nature ct|Carla f classique c
Cerise f gourmand ct|Chanel f classique ct|Chipie f mignon ct|Cléo f classique ct|Clochette f mignon ct|Coco u classique ct
Colette f classique ct|Comète f original ct|Cora f classique c|Câline f mignon ct|Capri f nature c|Callie f mignon ct
Clémentine f gourmand ct|Cumulus m nature ct|Cosmos m nature ct|Chaussette f mignon t|Cléopâtre f original t|Chamallow u gourmand ct
Cèdre m nature c|Cactus m original ct|Crocus f nature ct|Clafoutis u gourmand t|Calypso f original ct|Cyprès m nature c
"""
NOMS = []
for ligne in N.strip().splitlines():
    for item in ligne.split("|"):
        nom, sexe, style, esp = item.split()
        NOMS.append({"n": nom, "s": sexe, "st": style, "e": esp})

STYLES = {"classique": "Classique", "mignon": "Mignon", "gourmand": "Gourmand", "nature": "Nature", "original": "Original"}
ANNEES = [(2024, "V"), (2025, "A"), (2026, "B"), (2027, "C"), (2028, "D"), (2029, "E"), (2030, "F")]


def liste(lettre, sexe, espece):
    noms = [x["n"] for x in NOMS if x["n"].startswith(lettre) and (x["s"] == sexe or x["s"] == "u") and espece in x["e"]]
    return ", ".join(noms)


def corps():
    e = html.escape
    sel = lambda nom, opts: f'<select id="{nom}" name="{nom}">' + "".join(f'<option value="{v}">{l}</option>' for v, l in opts) + "</select>"
    annees = "".join(f'<tr{" class=\"actuelle\"" if a == 2026 else ""}><td>{a}</td><td><strong>{l}</strong></td></tr>' for a, l in ANNEES)
    listes = ""
    for lettre, annee in (("B", 2026), ("C", 2027)):
        listes += f"""        <h2>Noms en {lettre} pour {annee}</h2>
        <h3>🐕 Chien mâle</h3><p>{liste(lettre, "m", "c")}</p>
        <h3>🐕 Chienne</h3><p>{liste(lettre, "f", "c")}</p>
        <h3>🐈 Chat</h3><p>{liste(lettre, "m", "t")}</p>
        <h3>🐈 Chatte</h3><p>{liste(lettre, "f", "t")}</p>
"""
    return f"""    <section class="page-hero">
      <div class="container outil">
        <p class="breadcrumb"><a href="index.html">Accueil</a> › Noms de chien et de chat</p>
        <h1>🏷️ Noms de chien et de chat : la lettre B en 2026 (et C en 2027)</h1>
        <p class="lead">Votre chiot ou votre chaton arrive bientôt ? Choisissez l'espèce, le sexe, la lettre et le style : notre générateur vous propose des idées de noms. Plus de {len(NOMS)} noms, classés et expliqués.</p>
        <div class="card" id="generateur-noms">
          <form>
            <div class="duo">
              <div><label for="espece">Animal</label>{sel("espece", [("c", "🐕 Chien"), ("t", "🐈 Chat")])}</div>
              <div><label for="sexe">Sexe</label>{sel("sexe", [("", "Peu importe"), ("m", "Mâle"), ("f", "Femelle")])}</div>
            </div>
            <div class="duo">
              <div><label for="lettre">Lettre</label>{sel("lettre", [("B", "B · 2026"), ("C", "C · 2027"), ("", "B ou C")])}</div>
              <div><label for="style">Style</label>{sel("style", [("", "Tous")] + list(STYLES.items()))}</div>
            </div>
            <button class="btn" type="submit">✨ Proposer des noms</button>
          </form>
          <div class="noms-resultat" aria-live="polite"></div>
        </div>
        <script type="application/json" id="donnees-noms">{json.dumps(NOMS, ensure_ascii=False)}</script>

        <h2>Quelle lettre pour un chien né en 2026 ?</h2>
        <p>En France, les chiens de race inscrits au LOF (Livre des origines français) reçoivent un nom qui commence par la lettre de leur <strong>année de naissance</strong>. La lettre change le 1<sup>er</sup> janvier, dans l'ordre de l'alphabet, en sautant les lettres K, Q, W, X, Y et Z. <strong>2026 est l'année du B</strong>, 2027 sera celle du C.</p>
        <div class="table-wrap"><table><thead><tr><th>Année de naissance</th><th>Lettre</th></tr></thead><tbody>{annees}</tbody></table></div>
        <p>Cette règle ne concerne que les chiens inscrits au LOF, et il s'agit d'une recommandation. Un chien sans pedigree, un chien adopté en refuge ou un chat peuvent porter le nom de votre choix. Beaucoup de familles suivent quand même la lettre de l'année, par tradition ou pour s'inspirer.</p>

        <h2>5 conseils pour bien choisir son nom</h2>
        <ul>
          <li><strong>Court</strong> : une ou deux syllabes, c'est plus facile à appeler et à reconnaître (Bob, Cali, Bijou).</li>
          <li><strong>Différent des ordres</strong> : évitez un nom qui ressemble à « assis », « non » ou « viens », pour ne pas embrouiller votre animal.</li>
          <li><strong>Facile à crier</strong> : imaginez-vous l'appeler au parc, devant tout le monde.</li>
          <li><strong>Qui plaît à toute la famille</strong> : tout le monde doit utiliser le même nom, sans surnoms qui changent tout le temps.</li>
          <li><strong>Toujours associé à du positif</strong> : n'utilisez jamais son nom pour le gronder.</li>
        </ul>

        <h2>Apprendre son nom à son chiot ou à son chaton</h2>
        <p>Dites son nom d'une voix joyeuse, une seule fois. Dès qu'il tourne la tête vers vous, récompensez-le avec une friandise. Répétez quelques fois par jour, dans un endroit calme, puis avec un peu plus de distractions. Très vite, son nom voudra dire « regarde-moi, il va se passer quelque chose de bien ». C'est la première étape d'un bon <a href="rappel-chien.html">rappel</a>.</p>

{listes}        <p>Pour bien démarrer avec votre nouveau compagnon : <a href="kit-accueil-chiot.html">la liste du matériel pour accueillir un chiot</a> · <a href="proprete-chiot.html">la propreté du chiot</a> · <a href="chat.html">le guide du chat</a>.</p>
      </div>
    </section>"""


if __name__ == "__main__":
    creer_page.creer("fr", "noms-chien-chat", "Noms de chien et de chat 2026 : lettre B (et C en 2027)",
                     f"Nom de chien en B pour 2026, en C pour 2027, noms de chat : notre générateur et plus de {len(NOMS)} idées classées par sexe et par style.",
                     corps(), scripts=["js/noms.js"], menu="🏷️ Idées de noms")
    creer_page.finir()
    print(len(NOMS), "noms")
