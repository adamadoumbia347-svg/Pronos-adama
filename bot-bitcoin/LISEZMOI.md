# Bot Bitcoin 4H — signaux forts et actualités fortes par courriel

Le bot analyse **uniquement les bougies 4 heures du Bitcoin** et ne vous écrit que dans trois cas :

| Courriel | Quand | Objet (visible sur l'écran verrouillé) |
|---|---|---|
| **Ticket de trade** | signal fort d'achat ou de vente (score ≥ 70/100 **et** un déclencheur) | `🟢 ACHAT FORT BTC · 81 229 $ · 72/100` |
| **Bilan** | le signal a touché l'objectif 1, 2, 3 ou son stop | `✅ BTC ACHAT · OBJECTIF 2 ATTEINT · 98 080 $` |
| **Flash actu** | actualité forte (ETF, Fed, piratage, réserve d'État…) | `⚡ ACTU FORTE BTC · SEC approves…` |

Il tourne tout seul sur GitHub (gratuit), toutes les heures. Pas de Telegram : tout arrive dans votre boîte mail sur le téléphone.

## Ce qui est nouveau

- **Score de confluence sur 100** : 8 critères notés (tendance EMA 50/200, Supertrend, MACD, RSI, ADX, volume,
  cassure ou divergence, sentiment Fear & Greed à contre-courant). Jauge et barres détaillées dans le courriel.
- **Déclencheur obligatoire** : pas de signal sans événement précis sur la dernière bougie fermée
  (retournement Supertrend, croisement MACD, cassure des 20 bougies, sortie de survente/surachat, reprise de l'EMA 21).
  Résultat : environ un signal par semaine, pas un courriel toutes les 4 heures.
- **Plan de trade complet** : entrée, stop (basé sur l'ATR et le dernier creux/sommet), 3 objectifs (1,5 R, 2,5 R, 4 R)
  et la **taille de position** pour ne risquer que 1 % de votre capital.
- **Graphique des 7 derniers jours dans le courriel** (dessiné en HTML, s'affiche dans Gmail sans image à charger),
  avec les niveaux stop / entrée / objectifs.
- **Suivi automatique** : le bot surveille son propre signal et vous prévient quand un objectif ou le stop est touché,
  puis tient un **historique** (taux de réussite, R cumulés) affiché dans chaque courriel.
- **Actualités notées** : 7 sources (Cointelegraph, CoinDesk, Decrypt, Bitcoin Magazine, The Block, Journal du Coin,
  Cryptoast). Une nouvelle relayée par plusieurs médias est regroupée et pèse plus lourd. Impact 🔴 à 🔴🔴🔴.
- **Météo du marché** : indice Fear & Greed affiché en ⛈️ 🌧️ ⛅ ☀️ 🔥.
- **Option notification instantanée** avec l'application gratuite **ntfy** (pas Telegram), en plus du courriel.

## Tableau de bord (page web privée)

**https://educanimaux.fr/btc-cffec35843/** — à ajouter à l'écran d'accueil du téléphone.

Graphique 4H (EMA 21/50/200, Supertrend, niveaux du trade, signaux passés), prix en direct, compte à rebours
jusqu'à la clôture de la bougie, rapport de force acheteurs/vendeurs, radar des 8 critères, trade suivi avec
position en direct, actualités notées des dernières 24 h, historique et courbe de gains, météo Fear & Greed.
Le bot met à jour `docs/btc-cffec35843/donnees.json` à chaque passage. La page n'est pas référencée par Google
(`noindex`, absente du plan du site) mais reste publique pour qui connaît l'adresse.

## Mise en route (10 minutes)

1. **Mot de passe d'application Gmail** : sur https://myaccount.google.com/apppasswords (validation en 2 étapes
   obligatoire), créez un mot de passe « Bot Bitcoin ». Gardez les 16 lettres.
2. Sur GitHub, dépôt → **Settings → Secrets and variables → Actions → New repository secret** :
   - `MAIL_EXPEDITEUR` : votre adresse Gmail
   - `MAIL_MOT_DE_PASSE` : les 16 lettres du mot de passe d'application
   - `MAIL_DESTINATAIRE` : l'adresse qui reçoit les alertes (facultatif, sinon la même)
3. Fusionnez la branche dans `main` (GitHub ne lance les tâches programmées que depuis la branche principale).
4. Onglet **Actions → Bot Bitcoin 4H → Run workflow**, cochez « Envoyer un courriel d'essai » : vous devez recevoir
   un ticket `[TEST]` sur le téléphone.
5. Dans l'application Gmail du téléphone, activez les notifications pour ce libellé (ou marquez l'expéditeur
   comme important) pour être alerté immédiatement.

### Facultatif : notification push ntfy

Installez l'application **ntfy** (Android / iPhone), abonnez-vous à un nom secret difficile à deviner
(ex. `btc-adama-7f3k9q`), puis ajoutez le secret `NTFY_SUJET` avec ce nom.

### Réglages (Settings → Secrets and variables → Actions → onglet Variables)

| Variable | Défaut | Rôle |
|---|---|---|
| `SEUIL_SIGNAL` | `70` | score minimum ; 80 = moins de signaux, plus sélectifs |
| `CAPITAL` | `1000` | votre capital en dollars, pour calculer la taille de position |
| `RISQUE_PCT` | `1` | pourcentage du capital risqué par trade |
| `ENVOYER_BILANS` | `1` | `0` pour ne recevoir que les signaux et les actus |
| `FUSEAU` | `Europe/Paris` | fuseau horaire des heures affichées (ex. `Africa/Abidjan`) |

## Fichiers

| Fichier | Rôle |
|---|---|
| `bot.py` | programme principal (`--test` : courriel d'essai, `--demo` : aperçus HTML dans `apercus/` sans rien envoyer) |
| `strategie.py` | score de confluence, déclencheurs, plan de trade |
| `indicateurs.py` | EMA, RSI, MACD, ATR, ADX, Supertrend, Bollinger (aucune bibliothèque externe) |
| `donnees.py` | bougies 4H (Kraken, puis Bitstamp, puis Binance en secours), Fear & Greed, flux d'actualités |
| `courriel.py` | les trois designs de courriel et l'envoi |
| `tableau.py` | données du tableau de bord (`docs/btc-cffec35843/donnees.json`) |
| `etat.json` | mémoire du bot, mise à jour automatiquement |

> Outil d'aide à la décision, pas un conseil financier. Aucun indicateur ne gagne à tous les coups :
> respectez toujours le stop et ne risquez que ce que vous acceptez de perdre.
