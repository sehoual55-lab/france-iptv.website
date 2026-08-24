# Mettre le site en ligne — GitHub + Vercel

Durée : une dizaine de minutes, la première fois. Ensuite, chaque `git push` met le site à jour
tout seul.

Vercel est gratuit pour ce type de site : HTTPS, CDN mondial et compression sont inclus, sans carte
bancaire.

---

## 1. Créer le dépôt GitHub

Sur [github.com/new](https://github.com/new) :

- **Repository name** : `france-iptv` (ou ce que vous voulez)
- **Private** est recommandé — le dépôt contient l'URL de votre script Google. Elle est de toute
  façon visible dans le code du site en ligne, mais autant ne pas l'afficher deux fois. Vercel
  déploie les dépôts privés sans supplément.
- **Ne cochez rien d'autre** : pas de README, pas de .gitignore, pas de licence. Ils sont déjà là.

## 2. Envoyer les fichiers

Ouvrez un terminal dans ce dossier (celui qui contient `index.html`) et lancez :

```bash
git init
git branch -M main
git add .
git commit -m "Site France IPTV"
git remote add origin https://github.com/VOTRE-COMPTE/france-iptv.git
git push -u origin main
```

Remplacez `VOTRE-COMPTE` par votre nom d'utilisateur GitHub. Git vous demandera de vous identifier :
utilisez un **jeton d'accès personnel** (GitHub → Settings → Developer settings → Personal access
tokens) comme mot de passe, pas votre mot de passe de compte.

> **Sans terminal ?** Sur la page de votre dépôt vide, cliquez sur *uploading an existing file* et
> glissez-déposez tout le contenu du dossier. Pensez à glisser aussi `assets/` en entier.

## 3. Connecter Vercel

1. Allez sur [vercel.com](https://vercel.com) et connectez-vous **avec GitHub**.
2. **Add New… → Project**.
3. Votre dépôt `france-iptv` apparaît dans la liste → **Import**.
4. Vercel détecte un site statique. **Ne touchez à rien :**
   - Framework Preset : `Other`
   - Build Command : *vide*
   - Output Directory : *vide* (la racine)
   - Install Command : *vide*
5. **Deploy**.

Une minute plus tard, votre site est en ligne sur une adresse du type
`france-iptv.vercel.app`. Ouvrez-la et vérifiez que tout s'affiche.

## 4. Brancher votre nom de domaine

Dans le projet Vercel : **Settings → Domains**.

1. Tapez `france-iptv.website` → **Add**
2. Ajoutez aussi `www.france-iptv.website` → **Add**

Vercel vous indique alors quoi configurer chez votre registrar (Namecheap, OVH…). En général :

| Type | Nom | Valeur |
|---|---|---|
| `A` | `@` | `76.76.21.21` |
| `CNAME` | `www` | `cname.vercel-dns.com` |

**Utilisez les valeurs affichées par Vercel**, pas celles de ce tableau : elles peuvent changer.

La propagation DNS prend de quelques minutes à quelques heures. Vercel installe le certificat HTTPS
automatiquement une fois le domaine pointé.

Le fichier `vercel.json` redirige déjà `www.france-iptv.website` vers `france-iptv.website`, ce qui
évite le contenu dupliqué. Le domaine sans `www` est donc le domaine canonique — c'est bien celui
qui est écrit dans les balises `canonical` et dans le sitemap.

## 5. Vérifier

- `https://france-iptv.website` s'affiche en HTTPS
- `https://www.france-iptv.website` redirige vers la version sans `www`
- `https://france-iptv.website/index.html` redirige vers `/`
- `https://france-iptv.website/sitemap.xml` s'affiche
- `https://france-iptv.website/google-sheet/Code.gs` renvoie **404** — c'est voulu, `.vercelignore`
  empêche la mise en ligne de vos fichiers de travail
- Passez une commande de test : ligne dans la feuille + e-mail + onglet WhatsApp

Puis, dans la Search Console de Google, ajoutez la propriété et soumettez le sitemap.

## 6. Mettre le site à jour, ensuite

```bash
git add .
git commit -m "Mise à jour des tarifs"
git push
```

Vercel redéploie tout seul en une trentaine de secondes. Chaque déploiement est conservé : en cas de
problème, **Deployments → … → Promote to Production** sur une version précédente vous ramène en
arrière instantanément.

---

## Ce que fait `vercel.json`

C'est l'équivalent Vercel du `.htaccess` (que Vercel ignore, mais que je garde dans le dépôt au cas
où vous hébergeriez aussi chez un Apache / cPanel).

| Réglage | Effet |
|---|---|
| `redirects` | `www` → sans `www`, et `/index.html` → `/` (évite le contenu dupliqué) |
| En-têtes de sécurité | `nosniff`, `SAMEORIGIN`, `Referrer-Policy`, `Permissions-Policy`, HSTS |
| Cache `assets/` | un an, `immutable` — logos et images servis depuis le CDN |
| Cache `.html` | revalidation immédiate côté navigateur, une heure côté CDN |
| `cleanUrls: false` | les adresses gardent leur `.html`, exactement comme dans le sitemap et les balises `canonical` |

### Si vous préférez des adresses sans `.html`

`france-iptv.website/blog` est plus élégant que `/blog.html`. Pour y passer proprement il faut
changer trois choses en même temps : `cleanUrls: true` dans `vercel.json`, les liens internes des
cinq pages, et les `canonical` + le `sitemap.xml`. Ne changez pas seulement `cleanUrls` : vous
créeriez une redirection sur chacun de vos liens internes. Dites-le-moi et je fais les trois d'un
coup.

## Dossiers non publiés

`.vercelignore` empêche la mise en ligne de :

- `_build/` — les sources qui régénèrent le site
- `google-sheet/` — le script Apps Script et sa notice
- `*.md` — ce guide et le README
- `.htaccess` — utile seulement sur un hébergement Apache

Ils restent dans le dépôt GitHub, ils ne sont simplement pas servis par le site.
