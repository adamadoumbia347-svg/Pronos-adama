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

  // Visiteurs européens dont la boutique n'a pas d'identifiant (ex. Allemagne, Espagne) :
  // ils sont envoyés vers la boutique de la page (fr ou it), sinon vers celle-ci, pour toucher la commission.
  // Dès qu'un identifiant est ajouté pour leur pays, ils retrouvent leur propre boutique.
  secoursEurope: "fr",
  europe: ["AT", "BE", "BG", "CH", "CY", "CZ", "DE", "DK", "EE", "ES", "FI", "FR", "GR", "HR", "HU",
           "IE", "IT", "LT", "LU", "LV", "MC", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK"],

  // Lettre d'information (Brevo, MailerLite…) : collez l'adresse « action » du formulaire d'inscription
  // pour chaque langue. Tant qu'elle est vide, l'encadré n'apparaît pas sur le site.
  // champ : nom du champ e-mail attendu par l'outil (Brevo : "EMAIL", MailerLite : "fields[email]").
  newsletter: {
    action: {
      fr: "https://a8a62cc8.sibforms.com/serve/MUIFAIFF-ztBeCjyRZ2UuK-qQIjy6hQXuy3_M4cZp2Jx85_ttvar1gAlzaomMD3bgUZjDTBvS4du0qN1aRekX3GSaWj-uu-DlyWjXO3MnMEZgOniVr_X-UFCJHRKSIAIe5iC8C3kLBMP6df2TU_6f0v3cINKbotWM4vRIAi4FHTZc349aa40ylN4Xk2kG2zkLUGmz66S8wOzu4R1qw==",
      en: "",
      it: ""
    },
    champ: "EMAIL",
    // Champs cachés demandés par le formulaire Brevo
    champsCaches: { email_address_check: "", locale: "fr", html_type: "simple" }
  },

  // Produits numériques vendus par le site (Payhip, Gumroad…) : collez le lien de la page d'achat.
  // Tant qu'il est vide, la page du produit affiche « Bientôt disponible ».
  produits: {
    programmeChiot: { url: "https://payhip.com/b/yckpA", prix: "12 €" }
  },

  // Liens précis qui remplacent la recherche Amazon pour un produit donné,
  // par boutique. La clé correspond à l'attribut data-aff du lien.
  // Exemple : liensPersonnalises: { fr: { harnais: "https://..." } }
  liensPersonnalises: {}
};
