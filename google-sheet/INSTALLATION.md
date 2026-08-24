# Brancher le checkout sur votre Google Sheet — 5 minutes

À la fin de ces étapes, chaque commande passée sur **france-iptv.website** :

1. ajoute une ligne dans votre feuille `1lLcKbzQuhHccz_-k8ayCJ9J97DdR-lRJRLKdehQ7LrY`,
2. vous envoie un e-mail à **xyz905391@gmail.com**,
3. ouvre quand même WhatsApp avec la commande rédigée — donc même si Google tombe, vous ne perdez
   jamais une vente.

Vous n'avez besoin d'aucun serveur, d'aucun abonnement et d'aucune carte bancaire : tout tient dans
Google Apps Script, qui est gratuit.

---

## Étape 1 — Ouvrir l'éditeur de script

Ouvrez votre feuille de calcul, puis le menu **Extensions → Apps Script**.

Un onglet s'ouvre avec un fichier `Code.gs` contenant quelques lignes vides
(`function myFunction() { }`).

## Étape 2 — Coller le script

**Effacez tout** le contenu de `Code.gs`, puis collez l'intégralité du fichier `Code.gs` fourni à
côté de ce document.

Les réglages sont déjà remplis — votre identifiant de feuille et votre adresse e-mail y sont écrits.
Vous n'avez rien à modifier.

Cliquez sur l'icône **disquette** (Enregistrer) ou faites `Ctrl + S`.

## Étape 3 — Autoriser le script

Dans la liste déroulante en haut, choisissez la fonction **`testCommande`**, puis cliquez sur
**Exécuter**.

Google vous demande alors une autorisation. C'est normal : le script doit pouvoir écrire dans votre
feuille et envoyer un e-mail depuis votre compte.

- **Examiner les autorisations** → choisissez votre compte Google
- L'écran « Google n'a pas validé cette application » s'affiche : c'est attendu pour un script que
  vous venez d'écrire vous-même. Cliquez sur **Paramètres avancés**, puis sur
  **Accéder à … (non sécurisé)**
- **Autoriser**

Retournez voir votre feuille : une ligne de test **« Test Dupont »** doit y être apparue, et un
e-mail doit être arrivé. **Supprimez cette ligne de test.**

> Si rien n'apparaît, l'onglet ciblé n'est pas le bon : mettez son nom exact dans `SHEET_NAME`
> en haut du script.

## Étape 4 — Déployer en application web

En haut à droite : **Déployer → Nouveau déploiement**.

1. Cliquez sur la roue dentée à gauche de « Sélectionner le type » → **Application web**
2. **Description** : `France IPTV — commandes` (ce que vous voulez)
3. **Exécuter en tant que** : **Moi** (votre adresse)
4. **Qui a accès** : **Tout le monde** ← indispensable, sinon le site ne peut pas écrire
5. **Déployer**

Google affiche une **URL d'application web** qui ressemble à :

```
https://script.google.com/macros/s/AKfycbx…………/exec
```

**Copiez-la.**

> « Tout le monde » ne veut pas dire que quelqu'un peut lire votre feuille : le script n'expose
> aucune donnée. Cela autorise seulement l'envoi d'une commande. Un jeton (`TOKEN`) écarte en plus
> les envois qui ne viennent pas de votre site.

## Étape 5 — Coller l'URL dans le site

Ouvrez `index.html` et cherchez `ORDER_ENDPOINT`. Vous trouverez, dans le bloc de commande :

```js
var ORDER_ENDPOINT = '';                    /* ex. https://script.google.com/macros/s/AKfy.../exec */
var ORDER_TOKEN    = 'fr-iptv-2026';        /* doit être identique à TOKEN dans Code.gs */
```

Collez votre URL entre les guillemets :

```js
var ORDER_ENDPOINT = 'https://script.google.com/macros/s/AKfycbx…………/exec';
```

Enregistrez, téléversez `index.html` sur votre hébergement. **C'est terminé.**

## Étape 6 — Vérifier

Ouvrez le site, cliquez sur **« Choisir cette offre »**, remplissez le formulaire avec vos propres
coordonnées et validez.

En quelques secondes : une ligne apparaît dans la feuille, un e-mail arrive, et l'onglet WhatsApp
s'ouvre avec la commande. Supprimez ensuite votre ligne de test.

---

## Questions fréquentes

**La colonne Prix affiche-t-elle un vrai nombre ?**
Oui. Le prix est envoyé en nombre brut (`134.97`) et formaté en euros par le script, donc vous
pouvez faire des `SOMME()` sur la colonne F sans rien retoucher.

**Puis-je changer le statut d'une commande ?**
Bien sûr : la colonne I est écrite une fois avec « En attente de paiement », ensuite elle est à
vous. Rien ne la réécrira.

**Comment ajouter une deuxième adresse d'alerte ?**
Dans `Code.gs`, séparez-les par une virgule :
`var NOTIFY_EMAIL = 'xyz905391@gmail.com,autre@exemple.com';`

**J'ai modifié le script, les commandes n'arrivent plus / rien ne change.**
Après chaque modification il faut redéployer : **Déployer → Gérer les déploiements →** l'icône
crayon **→ Version : Nouvelle version → Déployer**. L'URL, elle, ne change pas.

**Quelle est la limite ?**
Le quota gratuit d'un compte Gmail classique est de l'ordre de 100 e-mails par jour et de très
nombreuses écritures — sans commune mesure avec un volume de commandes normal.

**Est-ce que des données bancaires transitent par là ?**
Non, jamais. Le site ne demande aucun numéro de carte : il recueille le nom, l'e-mail, le téléphone
et le moyen de paiement *souhaité*. C'est ensuite vous qui envoyez les instructions de paiement.

**Et le RGPD ?**
À partir du moment où ces informations sont conservées dans une feuille, il vous faut une
**politique de confidentialité** accessible depuis le formulaire (quelles données, pourquoi, combien
de temps, comment les faire supprimer). Dites-le-moi et je la rédige avec les mentions légales.
