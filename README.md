# Guide IPTV — site d'information indépendant

Site statique en français. Aucun framework, aucune base de données, aucune étape de build
obligatoire pour le déploiement : vous téléversez le dossier tel quel.

## Avant la mise en ligne — les deux seules lignes à changer

Dans `_build/build.py`, tout en haut :

```python
DOMAIN = 'https://guide-iptv.fr'   # votre domaine, sans barre oblique finale
BRAND  = 'Guide IPTV'              # le nom affiché dans l'en-tête
```

Puis régénérez :

```bash
python3 _build/build.py
```

Le domaine est repris automatiquement dans les balises canoniques, l'Open Graph, les données
structurées, le sitemap et le robots.txt. Il n'y a rien d'autre à remplacer.

## URLs

Les URLs sont propres **par construction** : chaque article est un dossier contenant un
`index.html`. Le serveur sert `/comment-fonctionne-iptv/` directement depuis le système de
fichiers — aucune réécriture, aucune redirection, donc aucune boucle possible.

```
/                            Accueil (liste des guides)
/comment-fonctionne-iptv/    Comment fonctionne l'IPTV en France
/choisir-abonnement-iptv/    Quel est le meilleur IPTV en France
/box-iptv-appareils/         Box, boîtier ou clé HDMI
/installer-playlist-m3u/     Installer une playlist M3U
/film-francais-iptv/         Mettre un film en français
/iptv-legal-france/          Est-ce que l'IPTV est légal en France
```

## Hébergement

**Vercel / Netlify / Cloudflare Pages :** dossier statique, aucune commande de build,
répertoire de sortie = racine. `vercel.json` ne contient que des en-têtes de sécurité et de
cache — aucune redirection.

**cPanel / Apache :** déposez le contenu dans `public_html`. Les dossiers fonctionnent nativement,
aucun `.htaccess` n'est nécessaire pour les URLs propres.

## Ce que ce site n'est pas

Aucune offre, aucun prix, aucun formulaire de commande, aucun widget de messagerie, aucun lien
sortant commercial. C'est délibéré : la valeur de ce site tient à son indépendance éditoriale.
Ajouter des liens vers un site marchand associerait publiquement les deux domaines et annulerait
l'intérêt de les séparer.

## Mise en ligne depuis GitHub

1. Créez un dépôt **vide** sur GitHub (privé ou public, au choix).
2. Depuis ce dossier :

```bash
git init
git add .
git commit -m "Guide IPTV — mise en place"
git branch -M main
git remote add origin git@github.com:VOTRE-COMPTE/VOTRE-DEPOT.git
git push -u origin main
```

3. Sur Vercel : **Add New → Project → Import** ce dépôt.
   Framework preset **Other**, aucune commande de build, répertoire de sortie = racine.
4. Ajoutez votre domaine dans **Settings → Domains**.

Chaque `git push` redéploie automatiquement.

## Fichiers

```
index.html                   Accueil
<slug>/index.html            Un dossier par guide
sitemap.xml, robots.txt      Générés
vercel.json                  En-têtes uniquement
_build/build.py              Le générateur — NE PAS TÉLÉVERSER
_build/articles.json         Le contenu des articles — NE PAS TÉLÉVERSER
```

Téléversez tout **sauf `_build/`**.
