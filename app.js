const ISSUES = [
  { cle: "domicile", libelle: "1" },
  { cle: "nul", libelle: "N" },
  { cle: "exterieur", libelle: "2" },
];

function formaterDate(iso) {
  return new Date(iso).toLocaleString("fr-FR", {
    weekday: "short",
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formaterCote(cote) {
  return typeof cote === "number" && cote > 1 ? cote.toFixed(2) : "–";
}

function creerCarte(match) {
  const cotes = match.cotes || {};
  const valides = ISSUES.map((i) => cotes[i.cle]).filter((c) => c > 1);
  const favorite = valides.length ? Math.min(...valides) : null;
  const marge = valides.length === ISSUES.length
    ? valides.reduce((s, c) => s + 1 / c, 0) - 1
    : null;

  const carte = document.createElement("article");
  carte.className = "match";

  const entete = document.createElement("div");
  entete.className = "entete";
  entete.textContent = `${match.competition} · ${formaterDate(match.date)}`;
  carte.appendChild(entete);

  const equipes = document.createElement("div");
  equipes.className = "equipes";
  equipes.textContent = `${match.domicile} – ${match.exterieur}`;
  carte.appendChild(equipes);

  const grille = document.createElement("div");
  grille.className = "cotes";
  for (const issue of ISSUES) {
    const cote = cotes[issue.cle];
    const case_ = document.createElement("div");
    case_.className = "cote";
    if (cote === favorite) case_.classList.add("favorite");
    if (match.prono === issue.libelle) case_.classList.add("prono");

    const libelle = document.createElement("span");
    libelle.className = "libelle";
    libelle.textContent = issue.libelle;
    const valeur = document.createElement("span");
    valeur.className = "valeur";
    valeur.textContent = formaterCote(cote);
    const proba = document.createElement("span");
    proba.className = "proba";
    proba.textContent = cote > 1 ? `${Math.round(100 / cote)} %` : "";

    case_.append(libelle, valeur, proba);
    grille.appendChild(case_);
  }
  carte.appendChild(grille);

  const pied = document.createElement("div");
  pied.className = "pied";
  const textes = [];
  if (match.prono) {
    const issue = ISSUES.find((i) => i.libelle === match.prono);
    textes.push(`Prono : ${match.prono}` + (issue ? ` @ ${formaterCote(cotes[issue.cle])}` : ""));
  }
  if (marge !== null) textes.push(`Marge : ${(marge * 100).toFixed(1)} %`);
  pied.textContent = textes.join(" · ");
  carte.appendChild(pied);

  return carte;
}

const conteneur = document.getElementById("matchs");
[...MATCHS]
  .sort((a, b) => new Date(a.date) - new Date(b.date))
  .forEach((m) => conteneur.appendChild(creerCarte(m)));
