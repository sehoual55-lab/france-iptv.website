# France IPTV — site français « Noir & Or » pour france-iptv.website

> **Mise en ligne :** ce dépôt se déploie sur **Vercel** en quelques clics —
> voir **[DEPLOIEMENT.md](DEPLOIEMENT.md)**. Aucune commande de build, aucun framework :
> `index.html` est à la racine, Vercel sert le dossier tel quel.

Site statique en **français**, ciblant les mots-clés IPTV France relevés dans Semrush. Même
architecture de sections que le site rouge existant, mais une identité visuelle entièrement
différente : fond noir profond, accents or, typographie Sora + Inter, grain fin sur le fond.

Aucun framework, aucune étape de build obligatoire, aucune base de données. Vous téléversez, ça
fonctionne.

---

## 1. Fichiers

```
index.html                              La page d'accueil complète (HTML + CSS + JS + icônes SVG)
blog.html                               L'index du blog
blog-meilleur-iptv-france.html          Article : quel est le meilleur IPTV en France
blog-iptv-legal-france.html             Article : est-ce que l'IPTV est légal en France
blog-installer-playlist-m3u.html        Article : installer une playlist M3U, appareil par appareil
robots.txt                              Règles pour les robots
sitemap.xml                             Plan du site XML
.htaccess                               HTTPS, www → non-www, gzip, cache, en-têtes de sécurité
assets/og-image.webp                    Image de partage social, 1200×630
assets/logo-512.webp                    Logo carré, 512×512
assets/apple-touch-icon.webp            Icône application, 180×180
google-sheet/Code.gs                    Script de réception des commandes — NE PAS TÉLÉVERSER
google-sheet/INSTALLATION.md            Comment le brancher, en 5 minutes
_build/                                 Sources du générateur — NE PAS TÉLÉVERSER
README.md                               Ce fichier
```

**Téléversez tout sauf `_build/` et `google-sheet/`** (ces deux dossiers restent chez vous ; le
script Google ne vit pas sur votre hébergement mais dans votre compte Google).

## 2. Avant la mise en ligne

Le domaine **france-iptv.website** est déjà écrit partout : balise canonique, Open Graph, données
structurées, sitemap et robots.txt. Il n'y a **aucun `your-domain.com` à remplacer** — c'est vérifié.

| À faire | Où |
|---|---|
| Ajuster prix, durées, connexions | objet `PLANS` dans le `<script>` **et** les cartes `<article class="plan">` |
| Changer le numéro | chercher `16728962871` (liens), `+1 672 896 2871` (texte visible) et reconstruire `assets/og-image.webp`, le numéro y est dessiné |
| Pages légales | mentions légales, politique de confidentialité et CGV sont généralement attendues en France pour une vente en ligne — dites-moi si vous voulez que je les rédige |

## 3. Téléversement

**Namecheap / cPanel ou tout hébergeur Apache :** déposez le contenu dans `public_html`, `index.html`
directement à la racine, `assets/` à côté. Activez *Afficher les fichiers cachés* dans le
gestionnaire de fichiers pour voir et téléverser `.htaccess`, puis lancez AutoSSL avant de compter
sur la redirection HTTPS.

**Vercel, Netlify, Cloudflare Pages :** dossier statique, aucune commande de build, répertoire de
sortie = racine. `.htaccess` y est ignoré, ces plateformes gèrent HTTPS et la compression.

## 4. Sections

En-tête collant (avec WhatsApp) · Héros sombre centré avec badges et quatre tuiles · Abonnement
(3 cartes) · **Pourquoi nous** (6 raisons + bandeau de faits) · Appareils compatibles (12 cas) ·
Tarifs (4 offres avec compteur de connexions et liste complète des fonctionnalités) · Bloc guide
SEO avec colonne latérale collante · FAQ (7 questions) · Contact · Pied de page · Blog (index +
3 articles) · **fenêtre de commande (checkout)** · widget WhatsApp flottant.

## 4b. Appareils compatibles

Douze plateformes avec leur **vrai logo de marque** en SVG inline, en monochrome sur fond noir :
Samsung, LG, Sony, Amazon (Fire TV), Android, Apple, Apple TV, Chromecast, Roku, Xbox, Windows et
Linux. Les logos sont des `<symbol id="b-…">` dans le sprite en haut de chaque page ; pour en
ajouter un, déposez le chemin SVG dans `_build/brands.py` et relancez le build.

Une mention sous la grille rappelle que les marques citées appartiennent à leurs propriétaires
respectifs et sont indiquées uniquement à titre de compatibilité — gardez-la.

## 5. Commande — fenêtre de checkout, carte bancaire ou PayPal

Les quatre boutons **« Choisir cette offre »** ouvrent la fenêtre *Finalisez votre commande* :
récapitulatif (offre, connexions, total), puis nom complet, adresse e-mail, téléphone avec sélecteur
d'indicatif (**FR +33 par défaut**, 17 pays), et le mode de paiement — **uniquement Carte bancaire
et PayPal**, comme demandé.

Les deux options portent les **logos officiels** : le monogramme PayPal dans son bleu de marque
`#002991` sur pastille blanche, et les marques **Visa** et **Mastercard** à droite de « Carte
bancaire ». Ce sont les tracés officiels (jeu d'icônes Simple Icons, source `paypal.com`), en SVG
inline — aucune image à charger, aucune requête externe. Ils apparaissent uniquement pour indiquer
les moyens de paiement acceptés ; ces marques appartiennent à leurs propriétaires respectifs.

**Aucun numéro de carte n'est demandé ni traité sur ce site.** Le formulaire recueille seulement le
nom, l'e-mail, le téléphone et le mode de paiement souhaité ; l'encadré sous le bouton le dit
explicitement au client. C'est un formulaire de commande, pas une page de paiement — vous restez
donc hors du champ PCI-DSS.

### Où arrive la commande

Un site statique n'a pas de base de données : il faut donc que la commande parte quelque part. Par
défaut, **elle est envoyée sur votre WhatsApp**, entièrement rédigée :

> Bonjour, je souhaite commander l'offre Gold — 15 mois (+3 mois offerts).
> Connexions : 3 · Total : 134,97 € · Nom : Jean Dupont · E-mail : … · Téléphone : +33 … ·
> Paiement : PayPal · Merci de m'envoyer les instructions de paiement.

L'onglet WhatsApp s'ouvre tout seul, et l'écran de confirmation affiche un bouton de secours si le
navigateur a bloqué la fenêtre. Aucune configuration n'est nécessaire.

## 5b. Google Sheets — enregistrer chaque commande

✅ **C'est déjà branché.** Votre URL de déploiement est en place dans `index.html` :

```js
var ORDER_ENDPOINT = 'https://script.google.com/macros/s/AKfycbwA3HmyJoR_SijlkVSNFL6JpV4i0e1uhZIUj6AgS6YfTyRDryjDQBpfqbNs8G0eH7qN/exec';
var ORDER_TOKEN    = 'fr-iptv-2026';   // identique à TOKEN dans Code.gs
```

Chaque commande part donc vers votre feuille `1lLcKbzQuhHccz_-k8ayCJ9J97DdR-lRJRLKdehQ7LrY` et
déclenche un e-mail sur **xyz905391@gmail.com**. Il vous reste seulement à passer une commande de
test sur le site en ligne pour confirmer que le déploiement Google répond (voir « Vérifier » ci-dessous).

### Vérifier

Ouvrez le site en ligne, cliquez sur **« Choisir cette offre »**, remplissez avec vos coordonnées et
validez. En quelques secondes : une ligne dans la feuille, un e-mail, et l'onglet WhatsApp qui
s'ouvre. Supprimez ensuite la ligne de test.

**Si la ligne n'apparaît pas**, la cause est presque toujours la même : dans
**Déployer → Gérer les déploiements**, le champ *Qui a accès* doit être sur **Tout le monde**, et
*Exécuter en tant que* sur **Moi**. Corrigez, puis **Version : Nouvelle version → Déployer**
(l'URL ne change pas). Vérifiez aussi que `TOKEN` dans `Code.gs` vaut bien `fr-iptv-2026`.

Le dossier `google-sheet/` contient le script (`Code.gs`, vos identifiants déjà renseignés) et le
mode d'emploi pas à pas (`INSTALLATION.md`). Pour mémoire :

1. Dans votre feuille : **Extensions → Apps Script**, collez `Code.gs`, enregistrez.
2. Lancez la fonction `testCommande` une fois pour autoriser le script — une ligne de test apparaît
   dans la feuille, supprimez-la.
3. **Déployer → Nouveau déploiement → Application web**, *Exécuter en tant que* **Moi**,
   *Qui a accès* **Tout le monde**.
4. Copiez l'URL `…/exec` et collez-la dans `index.html` :

```js
var ORDER_ENDPOINT = 'https://script.google.com/macros/s/AKfycbx…/exec';
var ORDER_TOKEN    = 'fr-iptv-2026';   // identique à TOKEN dans Code.gs
```

Chaque commande remplit alors les neuf colonnes de votre feuille — Date, Nom, Email, Téléphone,
Formule, Prix (€), Connexions, Paiement, Statut — dans cet ordre exact, avec la date au format
`jj/mm/aaaa hh:mm` et le prix en nombre (colonne F sommable). Le statut est initialisé à
« En attente de paiement » puis vous appartient : rien ne le réécrira.

**Détail technique, pour information.** L'envoi part en `application/x-www-form-urlencoded` via
`navigator.sendBeacon`, avec `fetch` en secours. C'est volontaire : une requête « simple » évite le
pré-vol CORS, que les applications web Apps Script ne savent pas traiter — c'est la raison n°1 pour
laquelle ce genre de branchement échoue habituellement. Le jeton `ORDER_TOKEN` écarte les envois qui
ne viennent pas de votre site.

**Et si Google est indisponible ?** La commande part quand même sur WhatsApp, comme avant. L'écriture
dans la feuille ne bloque jamais le client et ne peut pas faire échouer une vente.

### Toujours vrai

- **Aucun lien `tel:` ni `mailto:`** nulle part : le téléphone n'est joignable que par WhatsApp.
- Le lien de chaque bouton d'offre reste un vrai `<a href="https://wa.me/…">` : si le JavaScript ne
  s'exécute pas, le bouton ouvre WhatsApp avec la commande pré-remplie au lieu de ne rien faire.
- Les messages WhatsApp générés depuis les cartes d'offre **ne contiennent jamais le mot « IPTV »**
  ni le nom de la marque. Le message envoyé depuis le checkout, lui, reprend le nom de l'offre
  (Gold, Platinum…) mais pas non plus le mot « IPTV ».
- Un champ piège invisible (`societe`) bloque les robots spammeurs sans gêner personne.

⚠️ **Nouveauté à traiter :** le site collecte désormais des données personnelles (nom, e-mail,
téléphone). En France et dans l'UE, cela implique une **politique de confidentialité** et une
information RGPD accessibles depuis le formulaire. Dites-moi si je les rédige.

## 6. Offres, connexions et calcul du prix

| Offre | Durée | Bonus | Prix (1 connexion) |
|---|---|---|---|
| Bronze | 12 mois | – | 39,99 € |
| Gold | 15 mois | +3 mois offerts | 49,99 € |
| Platinum | 15 mois | +3 mois offerts | 59,99 € |
| Exclusive | 24 mois | +3 mois offerts | 84,99 € |

Chaque carte porte un compteur de connexions (1 à 5). La première connexion est au prix plein,
chaque connexion supplémentaire est **15 % moins chère**.

Formule : `total = base × (1 + 0,85 × (connexions − 1))`
Exemple — Gold avec 3 connexions : 49,99 + 42,49 + 42,49 = **134,97 €**

```js
var PLANS = {
  bronze:    {name:'Bronze',    months:12, bonus:0, price:39.99},
  gold:      {name:'Gold',      months:15, bonus:3, price:49.99},
  platinum:  {name:'Platinum',  months:15, bonus:3, price:59.99},
  exclusive: {name:'Exclusive', months:24, bonus:3, price:84.99}
};
var EXTRA = 0.85;   // remise sur les connexions supplémentaires
var MAXQ  = 5;      // connexions maximum
```

Les prix affichés dans les cartes et dans le `href` de repli doivent être modifiés en même temps.

Chaque carte porte aussi une **liste de dix fonctionnalités** (chaînes, films et séries, qualité,
chaînes internationales, compatibilité, EPG, VOD, serveurs, assistance, activation). Bronze, Gold et
Platinum partagent la même liste ; Exclusive affiche des volumes supérieurs et « toutes les chaînes
internationales ». Ces listes se modifient dans `_build/_body.html`, ou directement dans les cartes
`<article class="plan">` du HTML final.

## 7. SEO — les mots-clés visés

Ciblage construit à partir de votre relevé Semrush (France, desktop) :

| Mot-clé | Volume | KD | Où il est utilisé |
|---|---|---|---|
| iptv france | 8,1 K | 41 | H1, titre, H2 du guide, FAQ, corps de texte |
| france iptv | 3,6 K | 11 | nom de marque, H1, balise title, pied de page |
| abonnement iptv france | 2,4 K | 19 | H2 Tarifs, meta description, guide |
| iptv abonnement france | 1,6 K | 25 | variante dans le guide et la FAQ |
| iptv player m3u playlist français | 1,3 K | 20 | section guide + article d'installation |
| french iptv / meilleurs iptv / quel iptv choisir | cluster | – | article « meilleur IPTV » + FAQ |

Les questions à fort volume ont chacune leur réponse dédiée, en H2 ou en FAQ :
*quel est le meilleur iptv en france* (50), *comment mettre un film en français sur iptv* (40),
*est-ce que l'iptv est légal en france* (40), *comment fonctionne iptv en france* (20).

Technique :

- `lang="fr"`, `og:locale=fr_FR`, `hreflang="fr"` et `x-default`
- Un seul `<h1>` par page, structure `<h2>` propre par section
- Données structurées : Organization, WebSite, **FAQPage** (7 questions éligibles aux rich results),
  Article et BreadcrumbList sur chaque article
- Balise canonique sur chaque page, sitemap et robots.txt inclus, maillage interne entre les
  sections, le guide et les trois articles
- Typographie française appliquée automatiquement : espace insécable avant `? ! ; :` et autour des
  guillemets, ce qui évite qu'un point d'interrogation se retrouve seul en début de ligne

Après la mise en ligne : soumettez le sitemap dans la Search Console et lancez le test des
résultats enrichis.

## 8. Choix de rédaction assumés

Les cartes d'offre annoncent désormais des volumes de catalogue (25 000+ chaînes, 100 000+ films et
séries, 130 000+ pour Exclusive), comme vous l'avez demandé. La première version du site disait
l'inverse — l'une des six raisons de « Pourquoi nous » affirmait que nous ne citions jamais ces
chiffres — ce qui aurait contredit vos propres tarifs. Cette raison a donc été remplacée par
**« Un prix clair, une durée claire »** (prix total annoncé d'avance, paiement unique, sans
reconduction automatique), la réponse FAQ « quel IPTV choisir » a été reformulée, et l'article de
blog correspondant présente maintenant la taille du catalogue comme « un point de départ, pas un
critère de décision » au lieu de la dénoncer.

Ce qui reste inchangé : le bandeau de faits rappelle que la HD et la 4K dépendent de la source, et
l'article précise que personne ne peut garantir la 4K sur l'intégralité d'un catalogue. Ce sont des
formulations que je vous conseille de garder : elles évitent une promesse invérifiable tout en
laissant vos chiffres de catalogue en place.

Sur la légalité, la page et l'article dédié disent la même chose, sans détour : **la technologie
IPTV est légale en France**, ce qui détermine la légalité c'est le contenu et les droits qui s'y
rattachent, la prestation est de nature technique et ne cède aucun droit sur des contenus tiers, et
il appartient au client de n'accéder qu'aux contenus qu'il est légalement autorisé à regarder.
Cette ligne figure dans le pied de page de chaque page. Elle vous protège et ne coûte aucune
conversion — je la laisserais.

## 9. Le thème — Noir & Or

Contrairement au site rouge, **tout le site est sombre**, pas seulement le héros. Le fond tourne
autour de `#0A0A0C` avec un halo doré radial dans le héros, une grille masquée et un grain fin
appliqué sur toute la page pour que le noir ne paraisse jamais plat.

L'or retenu est `#E3B23C`, avec `#F6D179` en haut de dégradé et `#A97C16` en bas. Sur le fond
quasi noir, le contraste dépasse largement le seuil AA pour le texte courant comme pour les prix et
les petits labels en majuscules. Les boutons dorés portent du texte `#1A1204` (presque noir), ce
qui donne un contraste très élevé dans l'autre sens.

Les jetons de couleur sont en haut du bloc `<style>` :

```css
--bg:#0A0A0C;      --bg-2:#0E0E11;    --bg-3:#131317;
--card:#121216;    --card-2:#17171C;
--ink:#F6F3ED;     --muted:#A7A096;   --dim:#736D64;
--gold:#E3B23C;    --gold-hi:#F6D179; --gold-deep:#A97C16;
```

Changez ces lignes et toute la page suit. Les titres sont en **Sora**, le texte courant en
**Inter** — un couple volontairement différent du site rouge, qui n'utilise qu'Inter.

## 10. Performance

Un fichier HTML par page, aucune bibliothèque JavaScript, aucune image sur le chemin critique,
toutes les icônes en SVG inline. La seule requête externe concerne les polices Google : hébergez-les
vous-même (`@font-face` + WOFF2 dans `assets/fonts/`) si vous voulez zéro requête tierce. Sans
elles, la page retombe sur la pile système et reste correcte.

## 11. Vérifié

- Aucun défilement horizontal à 320 / 360 / 390 / 430 / 540 / 600 / 720 / 768 / 820 / 1024 / 1180 /
  1300 / 1440 / 1600 / 1920 px, sur les cinq pages
- Zéro lien `tel:` et zéro `mailto:`, tous les liens WhatsApp vers `wa.me/16728962871`
- Aucun champ de carte bancaire nulle part (vérifié : 0 champ `cc-*`)
- Aucun message WhatsApp issu des cartes d'offre ne contient « IPTV »
- Compteur de connexions : Gold ×3 → 134,97 €, repris à l'identique dans le checkout
- Checkout : ouverture, récapitulatif juste, refus d'un envoi incomplet, message d'erreur par champ,
  écran de confirmation et lien WhatsApp de secours corrects
- Les douze logos de marque s'affichent (symboles présents et référencés)
- Les quatre cartes d'offre s'alignent à la ligne près (compteur et listes au même pixel)
- Accordéon FAQ, en-tête collant, scroll-spy, menu mobile, widget WhatsApp
- Aucune erreur JavaScript en console
- `prefers-reduced-motion` désactive les animations
- Aucun `your-domain.com` résiduel

## 12. Régénérer le site

Le dossier `_build/` contient les sources : `_style.css`, `_body.html`, `_script.js` et `build.py`.
Le script assemble `index.html`, génère le blog, le sitemap et le robots.txt, et applique la
typographie française.

```bash
python3 _build/build.py
```

Vous pouvez aussi éditer les fichiers HTML finaux directement : ils sont autonomes. Si vous le
faites, gardez à l'esprit qu'une régénération écraserait vos modifications.
