"""Pages détaillées « Mon chat peut-il manger … ? » (français), une par aliment très recherché pour le chat.

Usage : python3 tools/pages/aliments_chat.py   (puis python3 tools/pages/aliments.py pour les liens du hub)
Verdicts repris de tools/pages/aliments.py (colonne chat) ; textes propres au chat, même prudence.
"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import creer_page  # noqa: E402
from aliments import A, DETAIL, VERDICT  # noqa: E402

e = html.escape
PAR_ID = {a[0]: a for a in A}

# id aliments.py → (slug, question, nom court, pourquoi, comment, si_mange)
PAGES = [
 ("poulet", "chat-peut-il-manger-poulet", "Mon chat peut-il manger du poulet ?", "le poulet",
  "Oui : le poulet cuit est l'une des meilleures friandises pour un chat. Carnivore strict, le chat a besoin de protéines animales, et la plupart des chats adorent le blanc de poulet. Ce n'est pas pour autant un repas complet : seul, il ne couvre pas tous ses besoins.",
  "Donnez-le cuit à l'eau ou à la vapeur, nature, sans peau, sans os, sans sel ni assaisonnement, en petits morceaux. Évitez les restes de poulet rôti ou cuisiné (ail, oignon, épices) et le poulet cru, qui peut transmettre des bactéries. Si vous envisagez une ration « maison », faites-la établir par un vétérinaire : un régime fait maison mal équilibré peut entraîner des carences.",
  "Un morceau de poulet nature n'est pas un problème. S'il a avalé un os cuit, surveillez-le : les os cuits peuvent se briser en éclats. En cas de vomissements, d'efforts pour vomir, de douleur ou s'il ne mange plus, appelez votre vétérinaire."),
 ("poisson", "chat-peut-il-manger-poisson", "Mon chat peut-il manger du poisson ?", "le poisson",
  "Oui, un peu de poisson cuit fait une très bonne friandise : saumon, cabillaud, colin… Mais le poisson ne doit pas devenir son alimentation habituelle, et certains poissons crus contiennent une enzyme qui détruit une vitamine importante pour le chat.",
  "Proposez-le cuit, nature, sans arêtes, sans peau grillée, sans sel ni sauce, en petite quantité. Évitez le saumon fumé, très salé, et les conserves à l'huile ou en sauce. Le poisson cru donné régulièrement est déconseillé.",
  "Un morceau de poisson cuit n'est pas un problème. S'il a avalé une arête et qu'il bave, se gratte la bouche, tousse ou vomit, consultez votre vétérinaire sans essayer de la retirer vous-même."),
 ("oeuf", "chat-peut-il-manger-oeuf", "Mon chat peut-il manger des œufs ?", "l'œuf",
  "Oui, l'œuf cuit est une bonne source de protéines pour le chat, en petite quantité. C'est l'œuf cru qui pose problème : il peut transmettre des bactéries, et le blanc cru perturbe l'absorption d'une vitamine.",
  "Proposez-le dur ou brouillé, sans sel, sans lait, sans beurre ni matière grasse, en tout petits morceaux. C'est une friandise occasionnelle, pas un repas.",
  "Un peu d'œuf cru léché une fois n'est en général pas grave, mais surveillez sa digestion. Si les vomissements ou la diarrhée durent, parlez-en à votre vétérinaire."),
 ("fromage", "chat-peut-il-manger-fromage", "Mon chat peut-il manger du fromage ?", "le fromage",
  "Le fromage n'est pas toxique pour le chat, mais il ne lui est pas utile. Il est gras, souvent salé, et contient du lactose, que la plupart des chats adultes digèrent mal. Une miette de temps en temps ne pose pas de problème à un chat en bonne santé.",
  "Si votre chat le réclame, donnez une toute petite quantité de fromage simple (pâte dure, peu salé). Évitez les fromages bleus, à l'ail ou aux herbes, et les fromages très gras. Un minuscule morceau peut aider à faire prendre un comprimé, si votre vétérinaire est d'accord.",
  "S'il a mangé un gros morceau, il peut avoir la diarrhée ou vomir. Proposez de l'eau fraîche et surveillez-le. Si les troubles durent plus d'une journée ou s'il semble abattu, consultez votre vétérinaire."),
 ("yaourt", "chat-peut-il-manger-yaourt", "Mon chat peut-il manger du yaourt ?", "le yaourt",
  "Un peu de yaourt nature est généralement mieux toléré que le lait, car il contient moins de lactose. Mais il n'est pas nécessaire à l'alimentation du chat, et certains chats le digèrent mal.",
  "Seulement nature, sans sucre, sans arôme, sans fruits et sans édulcorant (certains, comme le xylitol, sont dangereux pour les animaux). Une cuillère à café à lécher, de temps en temps, suffit largement. Pas de crème dessert, de yaourt aux fruits ni de fromage blanc sucré.",
  "S'il a mangé un yaourt entier ou un yaourt sucré, surveillez sa digestion. En cas de diarrhée ou de vomissements qui durent, ou si le produit contenait un édulcorant, appelez votre vétérinaire."),
 ("charcuterie", "chat-peut-il-manger-jambon", "Mon chat peut-il manger du jambon ?", "le jambon et la charcuterie",
  "Mieux vaut l'éviter. Le jambon et la charcuterie sont très salés, souvent gras, et certains contiennent de l'ail, de l'oignon ou des épices. Ce n'est pas un aliment pour le chat, même s'il le réclame.",
  "Préférez un petit morceau de poulet ou de dinde cuits nature : il lui fera tout autant plaisir. Gardez les assiettes de charcuterie hors de portée, en particulier pendant les apéritifs et les fêtes.",
  "Un petit morceau de jambon n'est en général pas grave chez un chat en bonne santé. S'il a mangé beaucoup de charcuterie, ou un produit à l'ail ou à l'oignon, et qu'il vomit, a la diarrhée, boit beaucoup ou semble abattu, appelez votre vétérinaire."),
 ("chocolat", "chat-peut-il-manger-chocolat", "Mon chat peut-il manger du chocolat ?", "le chocolat",
  "Non, jamais. Le chocolat contient de la théobromine et de la caféine, toxiques pour le chat comme pour le chien. Plus il est noir (et surtout le chocolat de cuisine), plus il est dangereux. Les chats en mangent moins souvent que les chiens, mais le risque est bien réel.",
  "Gardez tout le chocolat hors de portée : boîtes de chocolats, gâteaux, pâte à tartiner, cacao en poudre, en particulier à Noël, Pâques et Halloween.",
  "Appelez immédiatement votre vétérinaire ou un centre antipoison vétérinaire, même s'il semble aller bien et même pour une petite quantité. Indiquez le type de chocolat et la quantité. Ne le faites pas vomir sans avis vétérinaire."),
 ("oignon", "chat-peut-il-manger-oignon", "Mon chat peut-il manger de l'oignon ?", "l'oignon",
  "Non. L'oignon, comme l'échalote et le poireau, abîme les globules rouges, et le chat y est encore plus sensible que le chien. Il est toxique cru, cuit, en poudre, et caché dans les soupes, sauces, bouillons et certains aliments pour bébé.",
  "Ne donnez jamais de restes de plats cuisinés, de bouillon ou de sauce à votre chat. Si vous utilisez un petit pot pour bébé pour faire manger un chat convalescent (sur conseil vétérinaire), vérifiez l'étiquette : il ne doit contenir ni oignon ni ail.",
  "Appelez votre vétérinaire, même si votre chat semble aller bien : les signes peuvent apparaître plusieurs jours après (fatigue, gencives pâles, respiration rapide, urine foncée)."),
 ("ail", "chat-peut-il-manger-ail", "Mon chat peut-il manger de l'ail ?", "l'ail",
  "Non. L'ail appartient à la même famille que l'oignon et présente le même danger pour le sang du chat, cru, cuit ou en poudre. Méfiez-vous des « remèdes naturels » à l'ail contre les parasites : ils ne sont pas adaptés au chat.",
  "Ne donnez aucun aliment contenant de l'ail : restes de viande assaisonnée, sauces, pizza, charcuterie, beurre à l'ail. Pour les parasites, demandez à votre vétérinaire un traitement adapté.",
  "Appelez votre vétérinaire, même si votre chat semble aller bien : comme pour l'oignon, les signes peuvent être retardés."),
 ("raisin", "chat-peut-il-manger-raisin", "Mon chat peut-il manger du raisin ?", "le raisin",
  "Non. Le raisin frais et les raisins secs sont connus pour atteindre gravement les reins du chien, et par précaution on les évite aussi chez le chat. Il n'en a de toute façon aucun besoin.",
  "Gardez les grappes, les raisins secs et les gâteaux qui en contiennent (pain aux raisins, brioches, panettone) hors de portée. Certains chats jouent avec les grains qui roulent : ramassez-les.",
  "Appelez votre vétérinaire, même s'il n'a mangé qu'un grain et qu'il semble aller bien : une prise en charge rapide est importante."),
 ("autre-espece", "chat-peut-il-manger-croquettes-chien", "Mon chat peut-il manger des croquettes pour chien ?", "les croquettes pour chien",
  "Pas comme alimentation. La nourriture pour chien ne couvre pas les besoins du chat : il lui faut plus de protéines et certains nutriments en quantité suffisante, comme la taurine, dont le manque peut à terme causer des problèmes au cœur et aux yeux.",
  "Quelques croquettes de chien grignotées de temps en temps ne sont pas dangereuses, mais donnez-lui toujours une alimentation formulée pour chat. Si vos animaux se volent leurs gamelles, nourrissez-les dans des pièces séparées ou à des hauteurs différentes (le chat en hauteur).",
  "Une poignée de croquettes de chien n'est pas une urgence : surveillez sa digestion. S'il en mange régulièrement à la place de sa nourriture, parlez-en à votre vétérinaire."),
 ("pasteque", "chat-peut-il-manger-melon", "Mon chat peut-il manger du melon ?", "le melon",
  "Le melon et la pastèque ne sont pas toxiques pour le chat, et certains chats sont étonnamment attirés par le melon. Mais ce sont des fruits sucrés, dont le chat carnivore n'a pas besoin : une petite friandise rare, pas plus.",
  "Seulement la chair, en tout petits morceaux, sans peau, sans écorce et sans pépins. Pas de melon au jambon ni de salade de fruits sucrée.",
  "S'il a mangé beaucoup de melon ou de l'écorce, il peut avoir des troubles digestifs. Si les vomissements ou la diarrhée durent, consultez votre vétérinaire."),
 ("courgette", "chat-peut-il-manger-concombre", "Mon chat peut-il manger du concombre ?", "le concombre",
  "Le concombre et la courgette ne sont pas toxiques pour le chat. Pleins d'eau et peu caloriques, ils n'apportent pas grand-chose à un carnivore, mais un petit morceau ne pose pas de problème s'il en a envie.",
  "Un petit morceau de concombre lavé, ou de courgette cuite à l'eau, nature. Et à propos des vidéos où l'on pose un concombre derrière un chat pour le faire sursauter : à ne pas faire, cela lui fait vraiment peur et peut le stresser durablement.",
  "Un morceau de concombre n'est pas un problème. En cas de troubles digestifs qui durent, consultez votre vétérinaire."),
 ("potiron", "chat-peut-il-manger-potiron", "Mon chat peut-il manger du potiron ?", "le potiron",
  "Oui, un peu de potiron ou de courge cuits et nature ne pose pas de problème au chat. Les vétérinaires le conseillent parfois, en petite quantité, pour aider le transit : demandez-lui conseil si votre chat a des soucis digestifs.",
  "Cuit à l'eau ou à la vapeur, réduit en purée, sans sel, sans sucre, sans beurre ni épices. Jamais de garniture pour tarte ou de soupe préparée (oignon, crème, sel). Une petite cuillère à café suffit.",
  "Un peu de potiron nature n'est pas un problème. S'il a mangé une soupe ou une tarte au potiron, vérifiez les ingrédients (oignon, ail, chocolat, raisins) et appelez votre vétérinaire en cas de doute."),
 ("banane", "chat-peut-il-manger-banane", "Mon chat peut-il manger de la banane ?", "la banane",
  "La banane n'est pas toxique pour le chat, mais elle ne lui sert à rien : elle est sucrée et le chat, carnivore strict, n'a pas besoin de fruits. Beaucoup de chats ne s'y intéressent d'ailleurs pas.",
  "Si votre chat en réclame, une toute petite rondelle, sans peau, de temps en temps. Pour lui faire plaisir, un morceau de poulet cuit ou une friandise pour chat sera plus adapté.",
  "Un morceau de banane n'est pas un problème. S'il en a mangé beaucoup, ou la peau, et qu'il vomit ou a la diarrhée qui dure, consultez votre vétérinaire."),
]


def corps(page):
    ident, slug, question, nom, pourquoi, comment, si_mange = page
    _, emoji, noms, vchien, vchat, note = PAR_ID[ident]
    vs = VERDICT["fr"]
    couleur = " warn" if vchat == "non" else ""
    autres = [p for p in PAGES if p[1] != slug]
    liens = " · ".join(f'<a href="{p[1]}.html">{e(p[2])}</a>' for p in autres)
    chien = (f' Pour le chien, voir <a href="{DETAIL[ident]}.html">notre page dédiée</a>.' if ident in DETAIL else "")
    return f"""    <section class="page-hero">
      <div class="container article">
        <p class="breadcrumb"><a href="index.html">Accueil</a> › <a href="aliments-chien-chat.html">Peut-il manger… ?</a> › Chat : {e(noms["fr"])}</p>
        <h1>{emoji} {e(question)}</h1>
        <p class="meta">🐈 Chat · Alimentation · Lecture 3 min</p>
        <div class="callout{couleur}"><strong>Réponse courte :</strong> 🐈 Chat : <strong>{vs[vchat]}</strong> · 🐕 Chien : <strong>{vs[vchien]}</strong>. {e(note["fr"])}</div>
        <h2>Pourquoi ?</h2>
        <p>{e(pourquoi)}</p>
        <h2>Comment lui en donner (ou l'éviter)</h2>
        <p>{e(comment)}</p>
        <h2>Il en a mangé : que faire ?</h2>
        <p>{e(si_mange)}</p>
        <div class="callout warn"><strong>Urgence :</strong> en cas de doute après l'ingestion d'un aliment, appelez votre vétérinaire ou un centre antipoison vétérinaire. N'essayez pas de faire vomir votre chat sans avis vétérinaire.</div>
        <h2>Le chat, un carnivore strict</h2>
        <p>Contrairement au chien, le chat a besoin d'une alimentation riche en protéines animales et de nutriments qu'il ne fabrique pas lui-même, comme la taurine. Une alimentation complète formulée pour chat couvre ces besoins : la nourriture humaine doit rester une petite friandise.{chien}</p>
        <h2>Les règles d'or des friandises pour chat</h2>
        <ul>
          <li><strong>Toujours nature</strong> : sans sel, sucre, sauce, épices, oignon ni ail.</li>
          <li><strong>En petite quantité</strong> : les friandises ne devraient pas dépasser environ 10&nbsp;% de ce qu'il mange dans la journée.</li>
          <li><strong>Une nouveauté à la fois</strong>, pour vérifier qu'il la digère bien.</li>
          <li><strong>De l'eau fraîche à volonté</strong> : beaucoup de chats boivent peu, une fontaine peut les y encourager.</li>
          <li><strong>Maladie ou régime particulier</strong> : demandez toujours l'avis de votre vétérinaire.</li>
        </ul>
        <p>👉 Voir la liste complète : <a href="aliments-chien-chat.html">37 aliments, ce que votre chien et votre chat peuvent manger</a> · <a href="chat.html">le guide du chat</a> · <a href="peut-il-boire-lait.html">mon chat peut-il boire du lait ?</a> · <a href="peut-il-manger-thon.html">mon chat peut-il manger du thon ?</a></p>
        <p class="small muted">Autres aliments pour le chat : {liens}</p>
        <p class="small muted">Sources : listes d'aliments toxiques de l'ASPCA Animal Poison Control Center et recommandations des associations vétérinaires. Cette page ne remplace pas l'avis d'un vétérinaire.</p>
      </div>
    </section>"""


if __name__ == "__main__":
    for page in PAGES:
        ident, slug, question = page[:3]
        vchat = PAR_ID[ident][4]
        v = VERDICT["fr"][vchat].split(" ", 1)[1]
        desc = f"{question} {v.capitalize()} : la réponse claire, pourquoi, quelle quantité et que faire s'il en a mangé."
        creer_page.creer("fr", slug, question, desc, corps(page))
    creer_page.finir()
    print(len(PAGES), "pages aliments chat")
