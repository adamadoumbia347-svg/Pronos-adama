"""Pages détaillées « Mon chien peut-il manger … ? » (français), une par aliment très recherché.

Usage : python3 tools/pages/aliments_detail.py   (puis python3 tools/pages/aliments.py pour les liens du hub)
Verdicts repris de tools/pages/aliments.py (même source, même prudence) ; textes propres à chaque aliment.
"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import creer_page  # noqa: E402
from aliments import A, VERDICT  # noqa: E402

e = html.escape
PAR_ID = {a[0]: a for a in A}

# id aliments.py → (slug, animal principal « chien »/« chat », question, verbe, pourquoi, comment, si_mange)
PAGES = [
 ("banane", "peut-il-manger-banane", "chien", "Mon chien peut-il manger de la banane ?", "manger de la banane",
  "La banane n'est pas toxique pour le chien. Elle apporte des fibres et du potassium, et beaucoup de chiens l'adorent. Mais elle est riche en sucre : c'est une friandise, pas un aliment de tous les jours.",
  "Retirez toujours la peau, difficile à digérer, et coupez quelques fines rondelles, adaptées à la taille de votre chien. En été, des rondelles congelées font une friandise rafraîchissante. Pour un chien en surpoids ou diabétique, demandez d'abord l'avis de votre vétérinaire.",
  "S'il a mangé une banane entière, surveillez sa digestion : quelques selles molles sont possibles. S'il a avalé la peau et vomit, semble avoir mal au ventre ou ne mange plus, appelez votre vétérinaire."),
 ("fromage", "peut-il-manger-fromage", "chien", "Mon chien peut-il manger du fromage ?", "manger du fromage",
  "Le fromage n'est pas toxique, mais il est gras, souvent salé et contient du lactose, que beaucoup de chiens adultes digèrent mal. Un tout petit morceau de temps en temps ne pose pas de problème à un chien en bonne santé.",
  "Choisissez un fromage simple, en tout petits dés, comme récompense de grande valeur. Évitez les fromages aux herbes, à l'ail ou à l'oignon, ainsi que les fromages bleus. Un morceau de fromage peut aider à faire prendre un comprimé, si votre vétérinaire est d'accord.",
  "S'il a mangé un gros morceau ou un plateau entier, il peut avoir la diarrhée ou vomir. Un repas très gras peut aussi déclencher une pancréatite : en cas de vomissements répétés, de douleur ou d'abattement, consultez rapidement."),
 ("oeuf", "peut-il-manger-oeuf", "chien", "Mon chien peut-il manger des œufs ?", "manger des œufs",
  "Oui, l'œuf cuit est une bonne source de protéines pour le chien. C'est l'œuf cru qui pose problème : il peut transmettre des bactéries, et le blanc cru perturbe l'absorption d'une vitamine.",
  "Proposez-le dur ou brouillé, sans sel, sans beurre ni matière grasse, en petite quantité et en complément de sa ration habituelle. Un œuf dur coupé en morceaux fait une excellente friandise d'éducation.",
  "Un œuf cru avalé une fois n'est en général pas grave, mais surveillez sa digestion. En cas de vomissements ou de diarrhée qui durent, parlez-en à votre vétérinaire."),
 ("pomme", "peut-il-manger-pomme", "chien", "Mon chien peut-il manger des pommes ?", "manger des pommes",
  "La chair de la pomme convient très bien au chien : croquante, peu calorique, elle fait une friandise légère. Il faut seulement retirer le trognon et les pépins, qui contiennent une substance indésirable et peuvent gêner la digestion.",
  "Lavez la pomme, retirez le trognon et les pépins, puis coupez-la en petits morceaux adaptés à sa taille. Même règle pour la poire. Commencez par une petite quantité pour vérifier qu'il la digère bien.",
  "S'il a croqué une pomme entière avec le trognon, il n'y a généralement pas d'urgence, mais surveillez-le. Un trognon avalé d'un coup peut gêner un petit chien : en cas de vomissements ou de douleur, consultez."),
 ("carotte", "peut-il-manger-carotte", "chien", "Mon chien peut-il manger des carottes ?", "manger des carottes",
  "Oui : la carotte est l'une des meilleures friandises pour le chien. Peu calorique, riche en fibres, elle peut se donner crue ou cuite. Beaucoup de chiens aiment la croquer.",
  "Crue, coupez-la en bâtonnets adaptés à sa taille pour éviter qu'il l'avale de travers. Cuite à l'eau, sans sel ni beurre, elle est plus facile à digérer. Pour le chat, préférez de petits morceaux cuits, s'il en veut.",
  "Une carotte entière avalée trop vite peut gêner un petit chien. S'il tousse, s'étouffe ou vomit, appelez votre vétérinaire."),
 ("chocolat", "peut-il-manger-chocolat", "chien", "Mon chien peut-il manger du chocolat ?", "manger du chocolat",
  "Non, jamais. Le chocolat contient de la théobromine et de la caféine, que le chien élimine très mal. Plus le chocolat est noir (et surtout le chocolat de cuisine), plus il est dangereux, mais aucun chocolat n'est sans risque.",
  "Gardez tout le chocolat hors de sa portée, en particulier à Pâques, Halloween et Noël : boîtes de chocolats, bûches, gâteaux, sapin décoré. Pour lui faire plaisir, préférez une friandise pour chien.",
  "Appelez immédiatement votre vétérinaire ou un centre antipoison vétérinaire, même s'il semble aller bien et même pour une petite quantité. Indiquez le type de chocolat, la quantité et le poids de votre chien. Vomissements, agitation, cœur qui bat vite ou tremblements sont des signes d'alerte. Ne le faites pas vomir sans avis vétérinaire."),
 ("raisin", "peut-il-manger-raisin", "chien", "Mon chien peut-il manger du raisin ?", "manger du raisin",
  "Non. Le raisin frais et les raisins secs peuvent provoquer une atteinte grave des reins chez le chien. On ne connaît pas de quantité « sans danger » : certains chiens réagissent même à quelques grains.",
  "Attention aux raisins cachés : pain aux raisins, brioches, gâteaux, céréales, mélanges de fruits secs. Gardez aussi les grappes hors de portée. Les chats doivent également éviter le raisin.",
  "Appelez immédiatement votre vétérinaire, même s'il n'a mangé que quelques grains et qu'il semble aller bien : une prise en charge rapide est importante."),
 ("riz", "peut-il-manger-riz", "chien", "Mon chien peut-il manger du riz ?", "manger du riz",
  "Oui, le riz blanc bien cuit et nature se digère facilement. Les vétérinaires le proposent parfois dans un repas léger, de façon temporaire, après un trouble digestif.",
  "Faites-le cuire à l'eau, sans sel, beurre ni épices, et donnez-le en petite quantité en complément de sa ration. N'utilisez pas de riz frit ou de restes cuisinés. En cas de diarrhée, demandez à votre vétérinaire comment l'utiliser : le riz seul n'est pas un repas équilibré.",
  "Un reste de riz nature n'est pas un problème. S'il a mangé un plat cuisiné (avec oignon, ail, sauce), surveillez-le et appelez votre vétérinaire en cas de doute."),
 ("tomate", "peut-il-manger-tomate", "chien", "Mon chien peut-il manger des tomates ?", "manger des tomates",
  "Un peu de tomate bien mûre ne pose généralement pas de problème au chien. En revanche, les parties vertes (tiges, feuilles, tomates pas mûres) contiennent des substances irritantes à éviter. Pour le chat, mieux vaut s'abstenir.",
  "Si vous lui en donnez, choisissez un petit morceau de tomate bien rouge, lavée, sans parties vertes. Jamais de sauce tomate, de ketchup ou de plats cuisinés : ils contiennent souvent de l'oignon, de l'ail et du sel. Attention aussi aux plants de tomates au jardin.",
  "S'il a mâchouillé un plant de tomate ou des tomates vertes, surveillez-le : vomissements, diarrhée, fatigue ou comportement inhabituel justifient un appel au vétérinaire."),
 ("pasteque", "peut-il-manger-pasteque", "chien", "Mon chien peut-il manger de la pastèque ?", "manger de la pastèque",
  "Oui, la chair de la pastèque est rafraîchissante et pleine d'eau, parfaite en été. Il faut seulement retirer les pépins et l'écorce, difficile à digérer.",
  "Coupez la chair en petits cubes, sans pépins ni écorce. Vous pouvez les congeler pour un en-cas frais. Comme elle est sucrée, restez sur une petite quantité. Même règle pour le melon.",
  "S'il a mangé de l'écorce ou beaucoup de pépins, surveillez sa digestion. Vomissements, ventre gonflé ou absence de selles doivent vous faire consulter."),
 ("avocat", "peut-il-manger-avocat", "chien", "Mon chien peut-il manger de l'avocat ?", "manger de l'avocat",
  "Mieux vaut l'éviter. L'avocat est très gras, ce qui peut provoquer des troubles digestifs, voire une pancréatite. Son gros noyau peut boucher l'intestin, et la peau, les feuilles et le noyau contiennent une substance irritante.",
  "Ne lui en donnez pas, et gardez les noyaux hors de portée (poubelle fermée). Attention au guacamole : il contient souvent de l'oignon et de l'ail, toxiques.",
  "S'il a avalé un noyau, appelez votre vétérinaire, surtout s'il vomit, ne mange plus ou semble avoir mal au ventre. Un morceau de chair sans noyau est moins inquiétant, mais surveillez sa digestion."),
 ("oignon", "peut-il-manger-oignon", "chien", "Mon chien peut-il manger de l'oignon ?", "manger de l'oignon",
  "Non. L'oignon, comme l'ail, l'échalote, le poireau et la ciboulette, abîme les globules rouges du chien et du chat. Il est toxique cru, cuit, en poudre ou caché dans une soupe, une sauce ou des restes de repas. Le chat y est encore plus sensible.",
  "Ne donnez jamais de restes de plats cuisinés, de bouillons ou de sauces : ils contiennent très souvent de l'oignon ou de l'ail. Lisez les étiquettes des aliments pour bébé ou des préparations que vous utiliseriez.",
  "Appelez votre vétérinaire, même si votre chien semble aller bien : les signes peuvent apparaître plusieurs jours après (fatigue, gencives pâles, urine foncée, essoufflement)."),
 ("pates", "peut-il-manger-pates", "chien", "Mon chien peut-il manger des pâtes ?", "manger des pâtes",
  "Les pâtes cuites nature ne sont pas toxiques pour le chien, mais elles n'apportent pas grand-chose et sont riches en glucides. Un peu de temps en temps, sans sauce, ne pose pas de problème.",
  "Donnez-les cuites, sans sel, sans beurre, sans fromage et surtout sans sauce : les sauces contiennent souvent de l'oignon, de l'ail et beaucoup de gras. Réduisez un peu sa ration le jour où il en mange.",
  "S'il a mangé un plat de pâtes en sauce (bolognaise, carbonara…), surveillez-le et appelez votre vétérinaire si la sauce contenait de l'oignon ou de l'ail, ou s'il vomit."),
 ("lait", "peut-il-boire-lait", "chat", "Mon chat peut-il boire du lait ?", "boire du lait",
  "C'est une fausse bonne idée. La plupart des chats adultes digèrent mal le lactose du lait de vache, ce qui provoque souvent de la diarrhée. La meilleure boisson pour un chat reste l'eau fraîche.",
  "Si vous voulez lui faire plaisir, il existe des laits spéciaux pour chats, à donner seulement en friandise. Pour un chaton orphelin, utilisez un lait maternisé pour chatons, jamais du lait de vache, et demandez conseil à votre vétérinaire. Pour aider un chat à boire, une fontaine à eau marche souvent bien.",
  "S'il a bu un peu de lait et a la diarrhée, proposez-lui de l'eau fraîche et surveillez-le. Si la diarrhée dure, s'il vomit ou semble abattu, consultez votre vétérinaire, surtout s'il s'agit d'un chaton."),
 ("thon", "peut-il-manger-thon", "chat", "Mon chat peut-il manger du thon ?", "manger du thon",
  "Un peu de thon de temps en temps ne pose pas de problème au chat, qui l'adore souvent. Mais le thon seul n'est pas un repas équilibré, et en donner trop souvent n'est pas conseillé.",
  "Choisissez du thon au naturel, pas à l'huile, ni à la sauce, ni salé, et donnez-le en petite quantité, comme une friandise. Il peut aider à faire manger un chat difficile ou à cacher un médicament, avec l'accord de votre vétérinaire. Même règle pour le chien.",
  "Une boîte de thon mangée d'un coup peut donner des troubles digestifs. Si votre chat vomit ou a la diarrhée plus d'une journée, consultez votre vétérinaire."),
]

SIMILAIRES = {"chien": [p for p in PAGES if p[2] == "chien"], "chat": [p for p in PAGES if p[2] == "chat"]}


def corps(page):
    ident, slug, animal, question, verbe, pourquoi, comment, si_mange = page
    _, emoji, noms, vchien, vchat, note = PAR_ID[ident]
    vs = VERDICT["fr"]
    principal = vchien if animal == "chien" else vchat
    couleur = {"oui": "", "modere": "", "non": " warn"}[principal]
    autres = [p for p in PAGES if p[1] != slug][:8]
    liens = " · ".join(f'<a href="{p[1]}.html">{e(p[3])}</a>' for p in autres)
    autre_animal = "chat" if animal == "chien" else "chien"
    v_autre = vchat if animal == "chien" else vchien
    return f"""    <section class="page-hero">
      <div class="container article">
        <p class="breadcrumb"><a href="index.html">Accueil</a> › <a href="aliments-chien-chat.html">Peut-il manger… ?</a> › {e(noms["fr"])}</p>
        <h1>{emoji} {e(question)}</h1>
        <p class="meta">{emoji} Alimentation · Lecture 3 min</p>
        <div class="callout{couleur}"><strong>Réponse courte :</strong> {"🐕 Chien" if animal == "chien" else "🐈 Chat"} : <strong>{vs[principal]}</strong> · {"🐈 Chat" if animal == "chien" else "🐕 Chien"} : <strong>{vs[v_autre]}</strong>. {e(note["fr"])}</div>
        <h2>Pourquoi ?</h2>
        <p>{e(pourquoi)}</p>
        <h2>Comment lui en donner (ou l'éviter)</h2>
        <p>{e(comment)}</p>
        <h2>Il en a mangé : que faire ?</h2>
        <p>{e(si_mange)}</p>
        <div class="callout warn"><strong>Urgence :</strong> en cas de doute après l'ingestion d'un aliment, appelez votre vétérinaire ou un centre antipoison vétérinaire. N'essayez pas de faire vomir votre animal sans avis vétérinaire.</div>
        <h2>Et pour le {autre_animal} ?</h2>
        <p>{"🐈" if autre_animal == "chat" else "🐕"} {vs[v_autre]}. {"Le chat est un carnivore strict : les aliments végétaux ne lui sont pas utiles, et il vaut mieux lui proposer un peu de viande ou de poisson cuits." if autre_animal == "chat" else "Les mêmes règles de prudence s'appliquent : toujours nature, en petite quantité, et jamais d'aliments toxiques."}</p>
        <h2>Les règles d'or des friandises</h2>
        <ul>
          <li><strong>Toujours nature</strong> : sans sel, sucre, sauce, épices, oignon ni ail.</li>
          <li><strong>En petite quantité</strong> : les friandises ne devraient pas dépasser environ 10&nbsp;% de ce qu'il mange dans la journée.</li>
          <li><strong>Une nouveauté à la fois</strong>, pour vérifier qu'il la digère bien.</li>
          <li><strong>Maladie ou régime particulier</strong> : demandez toujours l'avis de votre vétérinaire.</li>
        </ul>
        <p>👉 Voir la liste complète : <a href="aliments-chien-chat.html">37 aliments, ce que votre chien et votre chat peuvent manger</a> · <a href="meilleures-friandises-education-chien.html">quelles friandises d'éducation choisir ?</a></p>
        <p class="small muted">Autres aliments : {liens}</p>
        <p class="small muted">Sources : listes d'aliments toxiques de l'ASPCA Animal Poison Control Center et recommandations des associations vétérinaires. Cette page ne remplace pas l'avis d'un vétérinaire.</p>
      </div>
    </section>"""


if __name__ == "__main__":
    for page in PAGES:
        ident, slug, animal, question, verbe = page[:5]
        _, _, noms, vchien, vchat, note = PAR_ID[ident]
        v = VERDICT["fr"][vchien if animal == "chien" else vchat].split(" ", 1)[1]
        desc = f"{question} {v.capitalize()} : la réponse claire, pourquoi, quelle quantité et que faire s'il en a mangé, pour le chien comme pour le chat."
        if len(desc) > 160:
            desc = f"{question} {v.capitalize()} : la réponse, la bonne quantité et que faire s'il en a mangé."
        creer_page.creer("fr", slug, question, desc, corps(page))
    creer_page.finir()
    print(len(PAGES), "pages aliments")
