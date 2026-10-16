/*
 * ============================================================
 *  CONFIGURATION DES LIENS D'AFFILIATION (toutes les langues)
 *  C'est le SEUL fichier à modifier pour gagner des commissions.
 * ============================================================
 *
 * Chaque boutique Amazon a son propre programme Partenaires et son propre
 * identifiant (tag). Inscrivez-vous dans chaque pays qui vous intéresse et
 * collez l'identifiant dans "tag" :
 *   - France    : https://partenaires.amazon.fr          (tag en -21)
 *   - Italie    : https://programma-affiliazione.amazon.it (tag en -21)
 *   - Espagne   : https://afiliados.amazon.es            (tag en -21)
 *   - Allemagne : https://partnernet.amazon.de           (tag en -21)
 *   - Royaume-Uni : https://affiliate-program.amazon.co.uk (tag en -21)
 *   - États-Unis  : https://affiliate-program.amazon.com   (tag en -20)
 *   - Canada      : https://associates.amazon.ca          (tag en -20)
 * Une boutique sans tag fonctionne quand même, mais ne rapporte rien.
 *
 * Le site choisit automatiquement la boutique du visiteur :
 *   1. d'après la langue et le pays de son navigateur (ex. en-GB → Royaume-Uni) ;
 *   2. sinon, la boutique par défaut de la langue de la page.
 */
window.AFFILIATION = {
  boutiques: {
    fr: { nom: "Amazon.fr", domaine: "amazon.fr", tag: "dobam0b-21" },
    it: { nom: "Amazon.it", domaine: "amazon.it", tag: "dobam01-21" },
    es: { nom: "Amazon.es", domaine: "amazon.es", tag: "" },
    de: { nom: "Amazon.de", domaine: "amazon.de", tag: "" },
    uk: { nom: "Amazon.co.uk", domaine: "amazon.co.uk", tag: "" },
    us: { nom: "Amazon.com", domaine: "amazon.com", tag: "" },
    ca: { nom: "Amazon.ca", domaine: "amazon.ca", tag: "" }
  },

  // Boutique par défaut selon la langue de la page.
  boutiqueParLangue: { fr: "fr", it: "it", en: "us" },

  // Boutique selon le pays du navigateur du visiteur (code pays ISO).
  boutiqueParPays: {
    FR: "fr", BE: "fr", LU: "fr", MC: "fr",
    IT: "it", SM: "it", VA: "it",
    ES: "es", DE: "de", AT: "de",
    GB: "uk", IE: "uk",
    US: "us", CA: "ca"
  },

  // Liens précis qui remplacent la recherche Amazon pour un produit donné,
  // par boutique. La clé correspond à l'attribut data-aff du lien.
  // Exemple : liensPersonnalises: { fr: { harnais: "https://..." } }
  liensPersonnalises: {}
};
