#!/usr/bin/env python3
"""Assemble the France IPTV site: splice CSS/JS into index.html and generate the blog."""
import pathlib, urllib.parse, re

D = pathlib.Path(__file__).parent.parent
PHONE = '16728962871'
PHONE_V = '+1 672 896 2871'
DOMAIN = 'https://france-iptv.website'

def wa(msg):
    return 'https://wa.me/%s?text=%s' % (PHONE, urllib.parse.quote(msg, safe=''))

PLANS = [
    ('BRONZE',    'Bronze',    '12 mois',              39.99),
    ('GOLD',      'Gold',      '15 mois +3 offerts',   49.99),
    ('PLATINUM',  'Platinum',  '15 mois +3 offerts',   59.99),
    ('EXCLUSIVE', 'Exclusive', '24 mois +3 offerts',   84.99),
]

WA = {
    'WA_GENERIC': wa("Bonjour, j'ai une question sur vos offres."),
    'WA_HELP':    wa("Bonjour, j'ai besoin d'aide s'il vous plaît."),
}
for key, name, term, price in PLANS:
    WA['WA_' + key] = wa(
        "Bonjour, je suis intéressé par l'offre %s (%s) avec 1 connexion — total %s EUR. "
        "Merci de m'envoyer les détails." % (name, term, ('%.2f' % price).replace('.', ','))
    )

NBSP = ' '
_TYPO = [(' ?', NBSP + '?'), (' !', NBSP + '!'), (' ;', NBSP + ';'),
         (' :', NBSP + ':'), ('« ', '«' + NBSP), (' »', NBSP + '»'),
         (' %', NBSP + '%')]

def _typo_chunk(s):
    """French spacing before double punctuation, on text only."""
    for a, b in _TYPO:
        s = s.replace(a, b)
    return s

def typo(s):
    """Apply French spacing outside <style>/<script> and outside HTML tags."""
    out, i = [], 0
    for m in re.finditer(r'<(style|script)\b.*?</\1>', s, re.S):
        out.append(_typo_outside_tags(s[i:m.start()]))
        out.append(m.group(0))
        i = m.end()
    out.append(_typo_outside_tags(s[i:]))
    return ''.join(out)

def _typo_outside_tags(s):
    out, i = [], 0
    for m in re.finditer(r'<[^>]+>', s):
        out.append(_typo_chunk(s[i:m.start()]))
        out.append(m.group(0))
        i = m.end()
    out.append(_typo_chunk(s[i:]))
    return ''.join(out)

def fill(s):
    for k, v in WA.items():
        s = s.replace('{{%s}}' % k, v)
    return typo(s)

# ---------------------------------------------------------------- index.html
css   = (D / '_build' / '_style.css').read_text(encoding='utf-8')
body  = (D / '_build' / '_body.html').read_text(encoding='utf-8')
brands = (D / '_build' / '_brands.svg').read_text(encoding='utf-8')
body  = body.replace('<!--BRANDS-->', brands)
js    = (D / '_build' / '_script.js').read_text(encoding='utf-8')
index = (D / 'index.html').read_text(encoding='utf-8')

if '<style>' in index:
    index = re.sub(r'<style>.*?</style>\n?', '', index, flags=re.S)
index = index.replace('</head>', '<style>\n%s\n</style>\n</head>' % css)
_new_body = '<body>\n%s\n<script>\n%s\n</script>\n</body>' % (body, js)
index = re.sub(r'<body>.*</body>', lambda m: _new_body, index, flags=re.S)
(D / 'index.html').write_text(fill(index), encoding='utf-8')
print('index.html assembled')

# ---------------------------------------------------------------- blog shell
ICONS = re.search(r'(<svg width="0" height="0".*?</svg>\n)', body, re.S).group(1)

def shell(title, desc, slug, inner, extra_head=''):
    return fill("""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0A0A0C">
<title>%(title)s | France IPTV</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(domain)s/%(slug)s">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="format-detection" content="telephone=no">
<link rel="alternate" hreflang="fr" href="%(domain)s/%(slug)s">
<meta property="og:type" content="article">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="France IPTV">
<meta property="og:url" content="%(domain)s/%(slug)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(domain)s/assets/og-image.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/logo-512.webp" type="image/webp">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">
%(extra_head)s
<style>
%(css)s
/* ---- blog ---- */
.bhero{padding:132px 0 56px;position:relative;overflow:hidden}
.bhero__bg{position:absolute;inset:0;pointer-events:none}
.bhero__bg::before{content:"";position:absolute;top:-300px;left:50%%;transform:translateX(-50%%);width:min(1100px,140vw);height:760px;background:radial-gradient(circle at 50%% 42%%,rgba(227,178,60,.17),transparent 66%%)}
.bhero h1{font-size:clamp(31px,4.6vw,52px);margin:20px 0 16px;max-width:22ch}
.bhero .lead{font-size:17.5px}
.bmeta{display:flex;gap:16px;flex-wrap:wrap;color:var(--dim);font-size:13.4px;margin-top:20px}
.bmeta span{display:inline-flex;align-items:center;gap:7px}
.bmeta svg{width:15px;height:15px;color:var(--gold)}
.bgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.bcard{display:block;padding:30px 28px;border-radius:var(--r-xl);background:linear-gradient(168deg,var(--card-2),var(--card));border:1px solid var(--line-2);transition:.32s var(--ease)}
.bcard:hover{transform:translateY(-6px);border-color:var(--line);box-shadow:var(--shadow-l)}
.bcard span.eyebrow{margin-bottom:16px}
.bcard h2{font-family:Sora,sans-serif;font-size:20px;margin:16px 0 11px;letter-spacing:-.03em;line-height:1.3}
.bcard p{color:var(--muted);font-size:14.6px;line-height:1.72}
.bcard em{font-style:normal;display:inline-flex;align-items:center;gap:7px;margin-top:16px;color:var(--gold);font-weight:700;font-size:14px}
.article{max-width:790px;margin-inline:auto}
.article .prose h2{margin-top:44px}
.toc{padding:24px 26px;border-radius:var(--r-l);background:var(--card);border:1px solid var(--line);margin:8px 0 36px}
.toc b{display:block;font-family:Sora,sans-serif;font-size:13px;letter-spacing:.13em;text-transform:uppercase;color:var(--gold);margin-bottom:13px}
.toc ol{margin:0 0 0 18px;color:var(--muted);font-size:14.6px;line-height:1.85}
.toc a{color:var(--muted);border:0}
.toc a:hover{color:var(--gold)}
.cta-band{margin-top:52px;padding:44px 38px;border-radius:var(--r-xl);text-align:center;background:linear-gradient(168deg,var(--card-2),var(--card));border:1px solid var(--line);box-shadow:var(--shadow-m)}
.cta-band h2{font-size:clamp(24px,3vw,33px);margin-bottom:13px}
.cta-band p{color:var(--muted);font-size:15.6px;max-width:52ch;margin:0 auto 24px}
.cta-band .btn{margin-inline:auto;max-width:340px}
.cta-band small{display:block;margin-top:13px;font-size:12.6px;color:var(--dim)}
@media (max-width:1000px){.bgrid{grid-template-columns:1fr 1fr}}
@media (max-width:760px){.bgrid{grid-template-columns:1fr}.bhero{padding-top:112px}}
</style>
</head>
<body>
%(icons)s
<header class="hdr is-stuck" id="hdr">
  <div class="wrap hdr__in">
    <a href="index.html" class="logo" aria-label="France IPTV, accueil">
      <span class="logo__mark" aria-hidden="true"><svg><use href="#i-logomark"></use></svg></span>
      <span><b>FRANCE</b> <i>IPTV</i></span>
    </a>
    <nav class="nav" aria-label="Navigation principale">
      <a href="index.html">Accueil</a>
      <a href="index.html#abonnement">Abonnement</a>
      <a href="index.html#appareils">Appareils</a>
      <a href="index.html#tarifs">Tarifs</a>
      <a href="index.html#faq">FAQ</a>
      <a href="blog.html" class="is-active">Blog</a>
      <a href="index.html#contact">Contact</a>
    </nav>
    <div class="hdr__right">
      <a class="hdr__wa" href="{{WA_GENERIC}}" target="_blank" rel="noopener" aria-label="Nous écrire sur WhatsApp">
        <svg><use href="#i-wa"></use></svg><span>WhatsApp &bull; +1 672 896 2871</span></a>
      <a class="btn btn-gold" href="index.html#tarifs">Commencer</a>
      <button class="burger" id="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="mnav"><span></span></button>
    </div>
  </div>
</header>
<div class="mnav" id="mnav">
  <a class="mnav__l" href="index.html">Accueil</a>
  <a class="mnav__l" href="index.html#abonnement">Abonnement IPTV</a>
  <a class="mnav__l" href="index.html#appareils">Appareils compatibles</a>
  <a class="mnav__l" href="index.html#tarifs">Tarifs</a>
  <a class="mnav__l" href="index.html#faq">FAQ</a>
  <a class="mnav__l" href="blog.html">Blog</a>
  <a class="mnav__l" href="index.html#contact">Contact</a>
  <a class="btn btn-wa btn-block btn-lg" href="{{WA_GENERIC}}" target="_blank" rel="noopener"><svg><use href="#i-wa"></use></svg> Nous écrire sur WhatsApp</a>
</div>
<main>
%(inner)s
</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr__grid">
      <div class="ftr__about">
        <a href="index.html" class="logo">
          <span class="logo__mark" aria-hidden="true"><svg><use href="#i-logomark"></use></svg></span>
          <span><b>FRANCE</b> <i>IPTV</i></span>
        </a>
        <p>Un service d'abonnement IPTV pensé pour la France : installation simple, large compatibilité et une
          assistance assurée par de vraies personnes.</p>
        <a class="ftr__wa" href="{{WA_GENERIC}}" target="_blank" rel="noopener"><svg><use href="#i-wa"></use></svg> +1 672 896 2871</a>
      </div>
      <div><h4>Navigation</h4><ul>
        <li><a href="index.html">Accueil</a></li>
        <li><a href="index.html#abonnement">Abonnement IPTV</a></li>
        <li><a href="index.html#appareils">Appareils</a></li>
        <li><a href="index.html#tarifs">Tarifs</a></li>
      </ul></div>
      <div><h4>En savoir plus</h4><ul>
        <li><a href="blog.html">Blog</a></li>
        <li><a href="index.html#guide">Guide IPTV</a></li>
        <li><a href="index.html#faq">FAQ</a></li>
        <li><a href="index.html#contact">Contact</a></li>
      </ul></div>
      <div><h4>Assistance</h4><ul>
        <li><a href="{{WA_GENERIC}}" target="_blank" rel="noopener">Assistance WhatsApp</a></li>
        <li><a href="blog-abonnement-iptv-france.html">Abonnement IPTV : le guide</a></li>
        <li><a href="blog-comment-fonctionne-iptv.html">Comment fonctionne l'IPTV</a></li>
        <li><a href="blog-box-iptv-france.html">Quel appareil choisir</a></li>
        <li><a href="blog-installer-playlist-m3u.html">Installer une playlist M3U</a></li>
        <li><a href="blog-film-francais-iptv.html">Mettre un film en français</a></li>
        <li><a href="blog-meilleur-iptv-france.html">Quel IPTV choisir</a></li>
        <li><a href="blog-iptv-legal-france.html">IPTV et légalité</a></li>
      </ul></div>
    </div>
    <p class="disclaimer">France IPTV fournit une prestation technique et une configuration de playlist ; le service
      ne vend ni ne cède aucun droit sur des contenus appartenant à des tiers. Il appartient au client de n'accéder
      qu'aux contenus qu'il est légalement autorisé à regarder. Les noms de chaînes, titres de programmes et visuels
      éventuellement présentés sur ce site sont des exemples génériques créés à titre d'illustration.</p>
    <div class="ftr__bot">
      <span>&copy; <span id="yr">2026</span> France IPTV &mdash; france-iptv.website</span>
      <span>Fait pour la France &bull; assistance en français</span>
    </div>
  </div>
</footer>
<div class="wa" id="wa">
  <div class="wa__panel" id="waPanel" role="dialog" aria-label="Discuter sur WhatsApp">
    <div class="wa__head">
      <span class="wa__av"><svg><use href="#i-wa"></use></svg></span>
      <span><b>France IPTV</b><small>Nous répondons en général vite</small></span>
      <button class="wa__x" id="waClose" aria-label="Fermer">&times;</button>
    </div>
    <div class="wa__body">
      <div class="wa__msg">Bonjour 👋<br>Une question sur une offre, une installation ou une commande en cours ?
        Écrivez-nous, une personne réelle vous répond.<span class="wa__time">En ligne</span></div>
    </div>
    <div class="wa__foot">
      <a class="btn btn-wa btn-lg btn-block" href="{{WA_GENERIC}}" target="_blank" rel="noopener"><svg><use href="#i-wa"></use></svg> Démarrer la discussion</a>
      <p>Vous serez redirigé vers WhatsApp.<br>+1 672 896 2871</p>
    </div>
  </div>
  <button class="wa__bubble" id="waBubble" aria-label="Ouvrir la discussion WhatsApp" aria-expanded="false" aria-controls="waPanel">
    <svg><use href="#i-wa"></use></svg><span class="wa__dot" aria-hidden="true">1</span>
  </button>
</div>
<script>
%(js)s
</script>
</body>
</html>
""" % dict(title=title, desc=desc, slug=slug, inner=inner, css=css, js=js,
           icons=ICONS, domain=DOMAIN, extra_head=extra_head))

# ---------------------------------------------------------------- articles
ARTICLES = []

ARTICLES.append(dict(
    slug='blog-abonnement-iptv-france.html',
    title="Abonnement IPTV France : le guide complet 2026",
    desc="Abonnement IPTV France : fonctionnement, chaînes et replay, appareils compatibles, VPN, prix et piste audio française. Le guide complet, sans promesse creuse.",
    eyebrow="Le guide",
    lead="Fonctionnement, contenu, appareils, VPN, prix : le tour complet de l'IPTV en France, sans jargon et sans promesse que personne ne peut tenir.",
    read="9 min de lecture",
    toc=[("Comment fonctionne l'IPTV en France", "#fonctionnement"),
         ("Chaînes, replay et VOD : ce que vous obtenez", "#contenu"),
         ("SD, HD, 4K : ce qui dépend de vous", "#qualite"),
         ("Box, boîtier ou clé HDMI", "#appareils"),
         ("Faut-il un VPN pour l'IPTV en France", "#vpn"),
         ("Mettre un film en français", "#francais"),
         ("Combien coûte un abonnement IPTV", "#prix"),
         ("Pour aller plus loin", "#suite")],
    body="""
<p>Chercher un <b>abonnement IPTV en France</b> aujourd'hui, c'est tomber sur des dizaines d'offres qui promettent
  toutes la même chose, avec les mêmes mots et des chiffres de plus en plus gros. Ce guide ne cherche pas à vous
  convaincre : il explique comment la technologie fonctionne, ce que vous obtenez réellement, ce qui dépend de votre
  installation plutôt que du fournisseur, et combien tout cela coûte.</p>

<h2 id="fonctionnement">Comment fonctionne l'IPTV en France</h2>
<p>IPTV signifie <i>Internet Protocol Television</i> : la télévision transmise par votre connexion internet plutôt
  que par une antenne, le câble ou le satellite. Le flux arrive sur votre appareil comme n'importe quelle vidéo en
  ligne, mais présenté sous forme de chaînes que vous parcourez à la télécommande.</p>
<p>Ce n'est pas une technologie marginale : les box d'Orange, Free, SFR et Bouygues diffusent leurs bouquets en IPTV
  depuis des années. Ce qui change d'un service à l'autre, ce n'est pas la technologie, c'est le fournisseur du flux
  et le catalogue proposé.</p>
<p>Trois éléments suffisent à faire fonctionner l'ensemble :</p>
<ul>
  <li><b>Le serveur</b> qui héberge et diffuse les flux.</li>
  <li><b>La playlist</b> — un lien M3U ou des identifiants Xtream — qui vous donne accès à ce serveur.</li>
  <li><b>L'application de lecture</b> installée sur votre téléviseur, votre box ou votre téléphone.</li>
</ul>
<p>Si vous voulez le détail du trajet d'un flux, le rôle de l'EPG et la différence avec une box opérateur, tout est
  expliqué ici : <a href="blog-comment-fonctionne-iptv.html">comment fonctionne l'IPTV en France</a>.</p>
<p>Côté débit, comptez environ 15 Mb/s pour du Full HD confortable et 25 à 30 Mb/s si vous visez la 4K, surtout si
  plusieurs personnes regardent en même temps. Un point qu'on lit rarement : la <b>régularité</b> de votre connexion
  compte davantage que son débit maximal. Une fibre à 1 Gb/s qui décroche toutes les dix minutes donnera une moins
  bonne expérience qu'un ADSL stable à 20 Mb/s.</p>

<h2 id="contenu">Chaînes, replay et VOD : ce que vous obtenez</h2>
<p>Un abonnement se juge sur trois éléments, et le premier est celui dont on parle le plus alors qu'il compte le
  moins.</p>
<p><b>Les chaînes.</b> Les offres du marché annoncent des catalogues allant de quelques milliers à plus de cent
  mille entrées. C'est le chiffre le plus facile à afficher et le plus difficile à vérifier. La vraie question n'est
  pas « combien de chaînes ? » mais « est-ce que <i>mes</i> chaînes sont là ? ». Faites la liste de ce que vous
  regardez réellement dans une semaine — vous serez surpris de sa brièveté — et demandez confirmation avant de
  payer.</p>
<p><b>Le replay.</b> La fonction de rattrapage permet de remonter généralement jusqu'à sept jours en arrière sur une
  partie des chaînes. C'est ce qui distingue un service confortable d'un service qui vous oblige à être devant votre
  écran à l'heure exacte. Vérifiez sur quelles chaînes elle est active, car ce n'est jamais l'intégralité du
  bouquet.</p>
<p><b>La VOD.</b> Une bibliothèque de films et de séries consultable à la demande, souvent avec plusieurs pistes
  audio et sous-titres. C'est la partie du catalogue qui vieillit le plus vite : un fournisseur sérieux l'alimente
  régulièrement.</p>

<h2 id="qualite">SD, HD, 4K : ce qui dépend de vous</h2>
<p>La mention « 4K » figure aujourd'hui sur pratiquement toutes les offres du marché français. Voici ce qu'elle
  signifie honnêtement.</p>
<p>La qualité d'un flux dépend de trois choses : la résolution de la <b>source</b>, la bande passante disponible sur
  le serveur, et votre propre connexion. Un fournisseur ne maîtrise que la deuxième. Aucune offre — la nôtre pas
  plus qu'une autre — ne peut garantir la 4K sur l'intégralité d'un catalogue, pour la simple raison que toutes les
  chaînes ne sont pas diffusées en 4K à la source.</p>
<p>Ce que vous pouvez raisonnablement attendre : du Full HD sur les chaînes principales, de la 4K là où la source le
  permet, et une lecture stable aux heures de forte affluence. Si vous voulez tester ce dernier point avant de vous
  engager, faites-le un soir de match entre 20 h et 22 h : c'est le moment où les serveurs sous-dimensionnés
  lâchent.</p>

<h2 id="appareils">Box, boîtier ou clé HDMI</h2>
<p>Beaucoup de personnes cherchent une <b>box IPTV</b> ou un <b>boîtier</b> en pensant qu'un appareil dédié est
  obligatoire. Ce n'est pas le cas : dans l'immense majorité des situations, vous avez déjà ce qu'il faut.</p>
<ul>
  <li><b>Smart TV Samsung (Tizen) et LG (webOS)</b> : une application de lecture s'installe depuis le magasin du
    téléviseur. Sur les modèles de plus de cinq ou six ans, vérifiez que le magasin est encore accessible.</li>
  <li><b>Android TV, Google TV, Sony, Philips, TCL</b> : le cas le plus simple, avec le choix d'applications le plus
    large.</li>
  <li><b>Fire TV Stick d'Amazon</b> : la solution la moins chère pour transformer un téléviseur classique en
    téléviseur connecté. Autour de 40 €, elle règle définitivement le problème de compatibilité.</li>
  <li><b>Boîtier dédié (MAG, Formuler)</b> : intéressant si vous voulez une interface pensée uniquement pour ça,
    notamment pour un utilisateur peu à l'aise avec la technologie.</li>
  <li><b>Smartphone, tablette, ordinateur</b> : utiles en déplacement ou en complément.</li>
</ul>
<p>Ne changez jamais de téléviseur pour de l'IPTV. Une clé HDMI coûte cent fois moins cher et fait exactement le même
  travail. Nous avons comparé les options et les prix dans
  <a href="blog-box-iptv-france.html">box IPTV, boîtier ou clé HDMI : que choisir</a>, et la mise en place concrète
  est détaillée appareil par appareil dans notre
  <a href="blog-installer-playlist-m3u.html">guide d'installation d'une playlist M3U</a>.</p>

<h2 id="vpn">Faut-il un VPN pour l'IPTV en France</h2>
<p>La question revient souvent, et elle mélange en réalité deux sujets distincts qu'il vaut mieux séparer.</p>
<p><b>La stabilité.</b> Certains fournisseurs d'accès appliquent une gestion de trafic sur les flux vidéo continus
  aux heures de pointe. Dans ce cas précis, un VPN peut aider. Mais il ajoute aussi de la latence et une étape de
  chiffrement, donc il dégrade parfois ce qu'il était censé améliorer. Testez d'abord sans : si votre lecture est
  fluide, n'ajoutez rien.</p>
<p><b>La confidentialité.</b> Un VPN chiffre votre trafic et masque votre adresse IP à votre fournisseur d'accès.
  C'est un choix personnel qui dépasse largement le cadre de l'IPTV et que nous ne trancherons pas à votre
  place.</p>
<p>Si vous en utilisez un, deux règles pratiques : choisissez un serveur en France ou dans un pays limitrophe, car
  la distance coûte du débit, et vérifiez que le service ne bride pas la bande passante, sans quoi la haute
  définition deviendra inconfortable.</p>

<h2 id="francais">Mettre un film en français</h2>
<p>Beaucoup de films de la section VOD contiennent une piste française mais démarrent en version originale. Le
  réglage se trouve dans le menu du lecteur, sous <b>Piste audio</b> : sélectionnez la ligne marquée <b>FR</b>.</p>
<p>La manipulation exacte varie selon l'application, et la plupart d'entre elles acceptent une langue par défaut qui
  vous évite de recommencer à chaque film. Nous avons détaillé chaque cas dans un guide dédié :
  <a href="blog-film-francais-iptv.html">comment mettre un film en français sur l'IPTV</a>.</p>

<h2 id="prix">Combien coûte un abonnement IPTV en France</h2>
<p>Le marché français se situe globalement entre 4 € et 12 € par mois selon la durée d'engagement, avec des remises
  importantes sur les formules longues. Nos offres vont de 39,99 € pour douze mois à 84,99 € pour vingt-quatre mois
  avec trois mois offerts, et chaque connexion supplémentaire est facturée 15 % moins cher que la première.</p>
<p>Deux repères pour ne pas se tromper :</p>
<ul>
  <li><b>Une offre anormalement basse est un mauvais signe.</b> Un an d'accès pour dix euros ne finance ni serveurs
    ni assistance. Le service fermera avant la fin de votre abonnement, et vous n'aurez aucun recours.</li>
  <li><b>Le prix doit être total et annoncé d'avance.</b> Pas de reconduction automatique, pas de frais qui
    apparaissent à l'étape suivante. Si vous ne savez pas ce que vous paierez au final, ne payez pas.</li>
</ul>
<p>Comptez aussi le nombre de connexions simultanées dont vous avez réellement besoin. Une connexion correspond à un
  écran actif à un instant donné : vous pouvez installer la playlist sur cinq appareils, mais un seul lira à la
  fois. Deux connexions suffisent à la plupart des foyers ; payer pour cinq quand vous vivez seul n'apporte
  rien.</p>

<h2 id="suite">Pour aller plus loin</h2>
<p>Trois sujets méritaient leur propre article plutôt qu'un paragraphe ici :</p>
<ul>
  <li><a href="blog-meilleur-iptv-france.html">Quel est le meilleur IPTV en France</a> — les critères vérifiables
    avant de payer, et les signaux qui doivent vous alerter.</li>
  <li><a href="blog-iptv-legal-france.html">Est-ce que l'IPTV est légal en France</a> — la distinction entre la
    technologie et les droits sur les contenus, expliquée sans langue de bois.</li>
  <li><a href="blog-installer-playlist-m3u.html">Installer une playlist M3U</a> — la procédure appareil par
    appareil, et quoi faire quand ça ne marche pas.</li>
</ul>
<p>Et si vous préférez poser directement votre question plutôt que lire trois guides de plus : dites-nous quel
  appareil vous utilisez et combien de personnes regardent en même temps chez vous. C'est en général tout ce qu'il
  faut pour savoir quelle offre a du sens.</p>
"""))

ARTICLES.append(dict(
    slug='blog-meilleur-iptv-france.html',
    title="Quel est le meilleur IPTV en France ? Les critères qui comptent vraiment",
    desc="Comment choisir un abonnement IPTV en France sans se fier aux promesses invérifiables : compatibilité, connexions simultanées et qualité de l'assistance.",
    eyebrow="Bien choisir",
    lead="Les comparatifs d'IPTV en France se ressemblent tous : des nombres de chaînes énormes et des taux de disponibilité que personne ne peut vérifier. Voici une autre méthode.",
    read="7 min de lecture",
    toc=[("Pourquoi les classements ne servent à rien", "#classements"),
         ("Critère 1 : la compatibilité de vos appareils", "#compat"),
         ("Critère 2 : les connexions simultanées", "#connexions"),
         ("Critère 3 : parler à quelqu'un avant de payer", "#humain"),
         ("Les signaux qui doivent vous alerter", "#alertes"),
         ("Notre réponse honnête", "#reponse")],
    body="""
<h2 id="classements">Pourquoi les classements se ressemblent tous</h2>
<p>Tapez « <b>quel est le meilleur IPTV en France</b> » et vous tomberez sur des dizaines de pages qui comparent
  essentiellement des tailles de catalogue. C'est une information utile, mais c'est la plus facile à afficher et la
  moins facile à vérifier — et surtout, ce n'est pas elle qui décide de votre expérience une fois l'abonnement
  activé.</p>
<p>Il existe trois critères que vous pouvez, eux, vérifier avant de payer un centime, et qui changent vraiment votre
  quotidien. Commencez par ceux-là, le catalogue viendra ensuite.</p>

<h2 id="compat">Critère 1 : la compatibilité de vos appareils</h2>
<p>Un abonnement IPTV n'est utile que s'il fonctionne sur ce que vous avez déjà chez vous. Posez-vous la question
  appareil par appareil :</p>
<ul>
  <li><b>Smart TV Samsung (Tizen) ou LG (webOS)</b> : elles proposent des applications de lecture compatibles dans
    leur magasin. Vérifiez que votre modèle, s'il a quelques années, y a toujours accès.</li>
  <li><b>Android TV, Google TV, Philips, Sony, TCL</b> : le choix d'applications est le plus large, c'est le cas le
    plus simple.</li>
  <li><b>Fire TV Stick</b> : très populaire en France, fonctionne bien et coûte peu.</li>
  <li><b>Téléviseur sans application adaptée</b> : une clé HDMI à une trentaine d'euros règle définitivement le
    problème. Ne changez pas de téléviseur pour ça.</li>
</ul>
<p>Si un vendeur ne peut pas vous dire clairement ce qui fonctionne sur votre modèle précis, c'est déjà une
  réponse.</p>

<h2 id="connexions">Critère 2 : les connexions simultanées</h2>
<p>C'est le seul chiffre qui compte vraiment. Une <b>connexion</b> correspond à un flux lu au même instant. Avec une
  seule connexion, vous pouvez installer votre playlist sur le téléviseur, la tablette et le téléphone — mais un seul
  de ces appareils peut regarder à la fois.</p>
<p>Comptez de façon réaliste : combien de personnes chez vous regardent la télévision <b>en même temps</b> un
  dimanche soir ? Deux connexions suffisent à la plupart des foyers, trois à une famille avec adolescents. Payer pour
  cinq quand vous vivez seul n'apporte rien.</p>

<h2 id="humain">Critère 3 : parler à quelqu'un avant de payer</h2>
<p>Testez le service avant d'acheter, gratuitement : envoyez une question précise et un peu gênante. « Est-ce que ça
  marche sur mon téléviseur Samsung de 2018 ? », « Que se passe-t-il si un flux ne fonctionne pas ? », « Est-ce que
  la 4K est garantie ? ».</p>
<p>Une réponse honnête ressemble à : <i>« La 4K dépend de la source, on ne peut pas la garantir sur tout. »</i> Une
  réponse commerciale ressemble à : <i>« Oui tout est en 4K, achetez maintenant. »</i> La première vous dit la
  vérité ; la seconde vous dit ce que vous voulez entendre.</p>

<h2 id="alertes">Les signaux qui doivent vous alerter</h2>
<ul>
  <li>Des taux de disponibilité chiffrés (« 99,99 % ») affichés comme une garantie.</li>
  <li>Une insistance sur le paiement immédiat, avec un compte à rebours.</li>
  <li>L'impossibilité d'obtenir une réponse claire sur ce que le service <b>ne</b> fait <b>pas</b>.</li>
  <li>Un site qui vous demande vos coordonnées bancaires dans un formulaire non sécurisé.</li>
</ul>

<h2 id="reponse">Notre réponse honnête</h2>
<p>Nous ne prétendrons pas être « le meilleur IPTV de France » : cette phrase ne veut rien dire et personne ne peut
  la prouver. Ce que nous pouvons décrire précisément, c'est ce que vous obtenez — une playlist M3U compatible avec
  les appareils listés plus haut, de une à cinq connexions simultanées selon l'offre, un guide d'installation en
  français, un prix total annoncé d'avance sans reconduction automatique, et une personne réelle au bout de
  WhatsApp, avant comme après l'achat.</p>
<p>Si vous en êtes au tout début et que vous cherchez d'abord à comprendre ce que recouvre un abonnement, commencez
  plutôt par notre <a href="blog-abonnement-iptv-france.html">guide de l'abonnement IPTV en France</a> : chaînes,
  replay, appareils, prix, tout y est repris dans l'ordre.</p>
<p>Un point que nous préférons écrire noir sur blanc plutôt que vous laisser le découvrir : la qualité d'image et la
  stabilité d'un flux donné dépendent de la source et de votre connexion. La 4K est possible quand le flux d'origine
  la permet — comme sur n'importe quel service de streaming — et personne ne peut vous la garantir sur l'intégralité
  d'un catalogue.</p>
"""))

ARTICLES.append(dict(
    slug='blog-iptv-legal-france.html',
    title="Est-ce que l'IPTV est légal en France ? Ce que dit vraiment la loi",
    desc="La technologie IPTV est légale en France. Ce qui compte, ce sont les droits sur les contenus diffusés. Explication claire, sans langue de bois.",
    eyebrow="Cadre légal",
    lead="La question revient constamment, et les réponses trouvées en ligne sont souvent soit alarmistes, soit trop rassurantes. Voici la distinction qui compte.",
    read="6 min de lecture",
    toc=[("La technologie n'est pas en cause", "#techno"),
         ("Ce qui fait la différence : les droits", "#droits"),
         ("Ce que dit le cadre français", "#cadre"),
         ("Ce que vous risquez concrètement", "#risques"),
         ("Notre position, écrite noir sur blanc", "#position")],
    body="""
<h2 id="techno">La technologie n'est pas en cause</h2>
<p>Commençons par le point le plus simple : <b>l'IPTV en tant que technologie est parfaitement légale en France</b>.
  C'est même la norme. Les box internet des opérateurs français diffusent la télévision par protocole IP depuis des
  années. Molotov, les services de replay, les plateformes de streaming : tous reposent sur le même principe
  technique que celui décrit sur ce site.</p>
<p>Poser la question « est-ce que l'IPTV est légal » revient donc à demander si le courriel est légal. La réponse
  dépend entièrement de ce que vous en faites.</p>

<h2 id="droits">Ce qui fait la différence : les droits</h2>
<p>Ce qui détermine la légalité d'un flux, ce n'est pas le tuyau, c'est le <b>contenu</b> qui y circule et les droits
  qui s'y rattachent. Une chaîne dispose de droits de diffusion pour un territoire et une durée donnés ; un
  distributeur doit être autorisé à la retransmettre.</p>
<p>Autrement dit : regarder une chaîne à laquelle vous avez légitimement accès est licite ; accéder à des contenus
  protégés sans que les droits nécessaires aient été acquis ne l'est pas — quelle que soit la technologie
  employée.</p>

<h2 id="cadre">Ce que dit le cadre français</h2>
<p>En France, la protection des œuvres relève du Code de la propriété intellectuelle, et la lutte contre la
  retransmission non autorisée — en particulier des compétitions sportives — s'est nettement renforcée ces dernières
  années. L'<b>Arcom</b>, née de la fusion du CSA et de la Hadopi, dispose de moyens pour faire bloquer des services
  diffusant illicitement des contenus protégés, et les ayants droit obtiennent régulièrement des décisions de
  blocage auprès des juridictions.</p>
<p>Ce cadre vise avant tout les services qui diffusent sans droits, et les personnes qui les exploitent. Il ne rend
  pas illégale la technologie, ni le fait de posséder une application de lecture ou un fichier M3U.</p>

<h2 id="risques">Ce que vous risquez concrètement</h2>
<p>Nous ne sommes pas avocats et cet article n'est pas un conseil juridique : pour votre situation personnelle,
  adressez-vous à un professionnel du droit. Ce que l'on peut dire de général, c'est que les autorités et les ayants
  droit concentrent leurs actions sur les diffuseurs et les revendeurs plutôt que sur les particuliers, et que le
  risque le plus courant pour un abonné est plus prosaïque : un service bloqué du jour au lendemain, et un
  abonnement payé qui ne fonctionne plus.</p>
<p>C'est une raison de plus pour privilégier des durées que vous acceptez de perdre, et un interlocuteur qui répond
  quand quelque chose cesse de marcher.</p>

<h2 id="position">Notre position, écrite noir sur blanc</h2>
<p>Notre prestation est de <b>nature technique</b> : nous fournissons une configuration de playlist et un
  accompagnement à l'installation. Nous ne vendons ni ne cédons aucun droit sur des contenus appartenant à des tiers,
  et nous ne prétendons pas le faire.</p>
<p>Il appartient au client de <b>n'accéder qu'aux contenus qu'il est légalement autorisé à regarder</b>. Cette phrase
  figure dans le pied de page de chaque page de ce site. Elle n'est pas une clause décorative : c'est la
  description exacte de ce que nous vendons, et de ce que nous ne vendons pas.</p>
<p>Si un site vous affirme qu'un abonnement vous donne un droit d'accès à tout, sans nuance, méfiez-vous : cette
  affirmation est fausse, et un vendeur qui ment sur ce point mentira aussi sur le reste.</p>
"""))

ARTICLES.append(dict(
    slug='blog-installer-playlist-m3u.html',
    title="Installer une playlist M3U : le guide en français, appareil par appareil",
    desc="Comment charger une playlist M3U dans un IPTV player en français sur Smart TV, Fire TV Stick, Android TV, mobile et ordinateur, et régler les pistes audio VF.",
    eyebrow="Installation",
    lead="Une playlist M3U, un lecteur compatible, et cinq minutes. Voici la marche à suivre sur chaque type d'appareil, avec les pièges qui font perdre du temps.",
    read="8 min de lecture",
    toc=[("Ce qu'est une playlist M3U", "#m3u"),
         ("Ce que vous devez avoir sous la main", "#prerequis"),
         ("Smart TV Samsung et LG", "#smarttv"),
         ("Fire TV Stick et Android TV", "#firetv"),
         ("Mobile, tablette et ordinateur", "#mobile"),
         ("Mettre un film en français : pistes audio et sous-titres", "#vf"),
         ("Quand ça ne marche pas", "#depannage")],
    body="""
<h2 id="m3u">Ce qu'est une playlist M3U</h2>
<p>Un fichier <b>M3U</b> est un simple fichier texte qui liste des adresses de flux, avec pour chacune un nom et,
  souvent, un logo et une catégorie. Ce n'est pas une vidéo : c'est un annuaire. Votre lecteur le lit, affiche la
  liste des chaînes, et va chercher le flux correspondant quand vous en sélectionnez une.</p>
<p>À côté du M3U, vous entendrez parler d'<b>EPG</b> (<i>Electronic Program Guide</i>), un second fichier qui remplit
  la grille horaire : ce qui passe maintenant, ce qui passe ensuite. Les deux se configurent au même endroit dans la
  plupart des applications.</p>

<h2 id="prerequis">Ce que vous devez avoir sous la main</h2>
<ul>
  <li>Vos <b>identifiants de playlist</b> (une URL, ou un identifiant et un mot de passe selon le lecteur).</li>
  <li>Une <b>application de lecture compatible</b> installée sur l'appareil.</li>
  <li>Une connexion internet correcte : environ 15 Mb/s pour du HD confortable, davantage pour de la 4K.</li>
  <li>Cinq minutes de calme. La première installation est la seule qui prend du temps.</li>
</ul>
<p>Un conseil qui évite beaucoup d'erreurs : ne retapez jamais l'URL à la main sur un téléviseur. Copiez-collez-la,
  ou utilisez la fonction de saisie depuis le téléphone si votre application la propose. Une seule lettre de travers
  et rien ne se charge.</p>

<h2 id="smarttv">Smart TV Samsung et LG</h2>
<p>Sur les téléviseurs Samsung (Tizen) et LG (webOS), la marche à suivre est la même dans les grandes lignes :</p>
<ol>
  <li>Ouvrez le magasin d'applications du téléviseur et installez une application de lecture IPTV compatible.</li>
  <li>Lancez-la : elle affiche en général un <b>identifiant d'appareil</b> ou une adresse MAC.</li>
  <li>Renseignez votre playlist là où l'application le demande — soit directement sur le téléviseur, soit via son
    portail web depuis un ordinateur.</li>
  <li>Redémarrez l'application. La liste des chaînes se charge.</li>
</ol>
<p>Si votre modèle est ancien et que son magasin ne propose plus d'application adaptée, ne cherchez pas midi à
  quatorze heures : une clé HDMI règle le problème pour une trentaine d'euros.</p>

<h2 id="firetv">Fire TV Stick et Android TV</h2>
<p>C'est le cas le plus simple, parce que le choix de lecteurs y est le plus large.</p>
<ol>
  <li>Installez une application de lecture IPTV depuis le magasin de l'appareil.</li>
  <li>Ouvrez-la et choisissez d'ajouter une playlist — selon le lecteur, l'option s'appelle <i>Add playlist</i>,
    <i>Ajouter une liste</i> ou <i>Xtream Codes</i>.</li>
  <li>Collez l'URL M3U, ou saisissez l'identifiant et le mot de passe fournis.</li>
  <li>Ajoutez l'EPG si un champ séparé le demande, puis validez.</li>
</ol>
<p>Sur Fire TV Stick, pensez à laisser la clé branchée sur un port assez alimenté et, si l'image saccade, testez le
  Wi-Fi 5 GHz plutôt que le 2,4 GHz : c'est la cause d'un problème de fluidité sur deux.</p>

<h2 id="mobile">Mobile, tablette et ordinateur</h2>
<p>Sur Android et iOS, les étapes sont identiques à celles d'Android TV : installez un lecteur compatible, ajoutez la
  playlist, laissez-la se charger. Sur ordinateur, un lecteur multimédia classique sait ouvrir un fichier M3U
  directement via <i>Média → Ouvrir un flux réseau</i>, ce qui est pratique pour vérifier rapidement qu'une playlist
  fonctionne avant de l'installer sur le téléviseur.</p>
<p>C'est d'ailleurs notre astuce préférée en cas de doute : testez toujours sur ordinateur d'abord. Si la playlist
  fonctionne là et pas sur la télé, le problème vient de l'application ou du réseau, pas de la playlist.</p>

<h2 id="vf">Mettre un film en français : pistes audio et sous-titres</h2>
<p>La question la plus fréquente après l'installation. Pendant la lecture, ouvrez le menu du lecteur — un appui sur
  la touche centrale ou un balayage vers le haut selon l'application — puis cherchez <b>Audio</b>, <b>Pistes</b> ou
  une icône de haut-parleur. Sélectionnez la piste française. Le menu voisin, <b>Sous-titres</b>, fonctionne de la
  même façon.</p>
<p>La plupart des lecteurs mémorisent ce choix et appliquent la même préférence aux lectures suivantes. Si les
  contenus sont classés par catégories, une rubrique <b>VF</b> ou <b>Films français</b> regroupe généralement les
  versions françaises, ce qui évite d'avoir à changer la piste à chaque fois.</p>

<h2 id="depannage">Quand ça ne marche pas</h2>
<ul>
  <li><b>Rien ne se charge</b> : l'URL comporte presque toujours une faute de frappe. Copiez-collez-la à nouveau.</li>
  <li><b>La liste se charge mais aucune chaîne ne démarre</b> : vérifiez que vous ne dépassez pas le nombre de
    connexions simultanées de votre offre. Un flux resté ouvert sur un autre appareil compte.</li>
  <li><b>L'image saccade</b> : testez sur un autre appareil et, si possible, en Ethernet. Cela distingue un problème
    de réseau d'un problème de source.</li>
  <li><b>Le guide des programmes est vide</b> : l'EPG n'a pas été renseigné, ou met simplement quelques minutes à se
    charger la première fois.</li>
</ul>
<p>Pour le reste — choix de l'offre, chaînes, replay, connexions simultanées — reportez-vous au
  <a href="blog-abonnement-iptv-france.html">guide de l'abonnement IPTV en France</a>.</p>
<p>Et si rien de tout cela ne suffit : écrivez-nous sur WhatsApp en indiquant votre appareil, l'application utilisée
  et ce qui s'affiche exactement à l'écran. Avec ces trois informations, le dépannage prend en général deux
  minutes.</p>
"""))

ARTICLES.append(dict(
    slug='blog-film-francais-iptv.html',
    title="Comment mettre un film en français sur l'IPTV",
    desc="Votre film démarre en anglais ? Comment changer la piste audio et activer les sous-titres français, application par application, et que faire sans VF.",
    eyebrow="Prise en main",
    lead="Le film se lance, et c'est de l'anglais. Rien n'est cassé : la piste française existe presque toujours, elle n'est simplement pas sélectionnée par défaut.",
    read="5 min de lecture",
    toc=[("Pourquoi le film démarre en anglais", "#pourquoi"),
         ("Changer la piste audio, application par application", "#pistes"),
         ("Activer les sous-titres français", "#soustitres"),
         ("VF, VOSTFR, MULTI : décoder les mentions", "#mentions"),
         ("Quand la piste française n'existe pas", "#absente"),
         ("Régler le problème une fois pour toutes", "#defaut")],
    body="""
<h2 id="pourquoi">Pourquoi le film démarre en anglais</h2>
<p>Un fichier vidéo peut contenir plusieurs pistes audio dans le même conteneur : une version originale, une version
  française, parfois une espagnole ou une arabe. Quand vous lancez la lecture, votre application en choisit une —
  et sauf réglage contraire, elle prend la première de la liste, qui est presque toujours la version originale.</p>
<p>Autrement dit, ce n'est ni un défaut du fichier ni un problème de votre abonnement. C'est un réglage de lecture,
  et il se change en trois secondes une fois qu'on sait où regarder.</p>

<h2 id="pistes">Changer la piste audio, application par application</h2>
<p>Le principe est identique partout : ouvrir le menu pendant la lecture, trouver l'entrée audio, choisir la piste
  marquée FR. Seul le chemin change.</p>
<p><b>IPTV Smarters / Smarters Pro.</b> Pendant la lecture, appuyez sur <b>OK</b> pour afficher la barre de contrôle,
  puis sélectionnez l'icône en forme de bulle ou l'entrée <b>Audio</b> à droite. La liste des pistes s'affiche avec
  leurs codes de langue.</p>
<p><b>TiviMate.</b> Appui long sur <b>OK</b>, puis <b>Pistes audio</b> dans le menu latéral. TiviMate mémorise votre
  choix par chaîne, ce qui est pratique.</p>
<p><b>Smart IPTV (SIPTV).</b> Touche <b>Menu</b> de la télécommande pendant la lecture, puis <b>Audio</b>. Sur
  certaines Smart TV Samsung, c'est la touche <b>Tools</b> ou <b>Options</b> qui ouvre ce menu.</p>
<p><b>VLC (ordinateur, Android, iOS).</b> Sur ordinateur : menu <b>Audio</b> puis <b>Piste audio</b>, ou le raccourci
  clavier <b>B</b> qui fait défiler les pistes. Sur mobile : touchez l'écran, puis l'icône en forme de cône ou de
  haut-parleur.</p>
<p><b>Fire TV Stick.</b> Le geste dépend de l'application installée dessus, pas de la clé elle-même. Reportez-vous à
  la ligne correspondante ci-dessus.</p>
<p>Si vous ne trouvez pas le menu, cherchez une icône de dialogue, de haut-parleur, ou les lettres <b>CC</b> ou
  <b>AUDIO</b> dans la barre qui apparaît quand vous appuyez sur OK.</p>

<h2 id="soustitres">Activer les sous-titres français</h2>
<p>Le chemin est le même, une entrée plus bas : cherchez <b>Sous-titres</b>, <b>Subtitles</b> ou <b>CC</b> dans le
  même menu, puis sélectionnez la ligne <b>French</b> ou <b>fre</b>.</p>
<p>Deux cas à distinguer, parce qu'ils ne se règlent pas pareil. Les <b>sous-titres intégrés</b> apparaissent dans
  cette liste et se désactivent normalement. Les <b>sous-titres incrustés</b>, eux, font partie de l'image : ils sont
  gravés dans la vidéo et aucun réglage ne les enlèvera. Si vos sous-titres refusent de disparaître, c'est qu'ils
  sont incrustés — il faut chercher une autre version du film.</p>

<h2 id="mentions">VF, VOSTFR, MULTI : décoder les mentions</h2>
<p>Les catalogues VOD un peu sérieux indiquent la langue dès le titre. Savoir lire ces abréviations vous évite
  d'ouvrir dix fichiers pour rien :</p>
<ul>
  <li><b>VF</b> — version française. Doublage en français, c'est ce que vous cherchez la plupart du temps.</li>
  <li><b>VFF</b> — version française de France, par opposition à un doublage québécois.</li>
  <li><b>VFQ</b> — version française québécoise. Même langue, autres comédiens et autres expressions.</li>
  <li><b>VOSTFR</b> — version originale, sous-titrée en français. L'audio reste en anglais.</li>
  <li><b>VO</b> — version originale sans sous-titres.</li>
  <li><b>MULTI</b> — plusieurs pistes audio dans le fichier, dont normalement le français.</li>
  <li><b>TRUEFRENCH</b> — utilisé comme synonyme de VFF dans la plupart des catalogues.</li>
</ul>
<p>Un fichier marqué <b>MULTI</b> est celui qui vous laisse le plus de latitude : c'est là que le changement de
  piste audio prend tout son sens.</p>

<h2 id="absente">Quand la piste française n'existe pas</h2>
<p>Il arrive que le menu audio ne propose qu'une seule ligne. Dans ce cas, aucun réglage ne fera apparaître une VF :
  elle n'est pas dans le fichier. Trois options :</p>
<ul>
  <li>Cherchez le même titre dans le catalogue avec la mention <b>VF</b> ou <b>MULTI</b> — les deux versions
    coexistent souvent.</li>
  <li>Rabattez-vous sur les sous-titres français si la piste de sous-titres, elle, est présente.</li>
  <li>Pour un film très récent, la VF n'existe parfois pas encore du tout, y compris ailleurs. Il faut attendre la
    sortie du doublage.</li>
</ul>

<h2 id="defaut">Régler le problème une fois pour toutes</h2>
<p>Plutôt que de refaire la manipulation à chaque film, la plupart des applications acceptent une langue audio par
  défaut. Cherchez dans les réglages généraux une entrée du type <b>Langue audio préférée</b> ou <b>Preferred audio
  language</b>, et mettez-la sur <b>Français</b>. L'application choisira alors automatiquement la piste FR quand
  elle existe, et retombera sur la VO seulement quand il n'y a pas d'alternative.</p>
<p>C'est le réglage que je vous conseille de faire dès l'installation. Pour le reste de la mise en place, notre
  <a href="blog-installer-playlist-m3u.html">guide d'installation d'une playlist M3U</a> reprend chaque appareil, et
  le <a href="blog-abonnement-iptv-france.html">guide de l'abonnement IPTV en France</a> couvre le reste des
  questions courantes.</p>
"""))

ARTICLES.append(dict(
    slug='blog-comment-fonctionne-iptv.html',
    title="Comment fonctionne l'IPTV en France ?",
    desc="Le trajet du flux, la playlist M3U, l'EPG, le débit nécessaire et la différence avec une box opérateur ou Netflix. L'IPTV expliquée simplement.",
    eyebrow="Comprendre",
    lead="Derrière un mot un peu technique se cache un mécanisme simple, que vous utilisez sans doute déjà tous les jours sans le savoir.",
    read="7 min de lecture",
    toc=[("Ce que veut dire IPTV", "#definition"),
         ("Le trajet d'un flux, de bout en bout", "#trajet"),
         ("Playlist M3U ou identifiants Xtream", "#playlist"),
         ("L'EPG, ce guide des programmes", "#epg"),
         ("Quel débit faut-il vraiment", "#debit"),
         ("Box opérateur, Netflix, IPTV : les différences", "#differences"),
         ("Pourquoi l'image saccade parfois", "#saccade")],
    body="""
<h2 id="definition">Ce que veut dire IPTV</h2>
<p>IPTV est l'abréviation d'<i>Internet Protocol Television</i> : la télévision acheminée par le même protocole
  réseau que vos pages web et vos e-mails, au lieu d'une antenne, d'un câble coaxial ou d'une parabole.</p>
<p>Ce n'est pas une nouveauté ni une technologie parallèle. Si vous êtes chez Orange, Free, SFR ou Bouygues et que
  vous regardez la télévision par la box, vous faites déjà de l'IPTV. La différence entre ces services et un
  abonnement indépendant ne tient pas à la technologie employée, mais au fournisseur du flux et au catalogue
  proposé.</p>

<h2 id="trajet">Le trajet d'un flux, de bout en bout</h2>
<p>Une chaîne parcourt quatre étapes avant d'arriver sur votre écran :</p>
<ul>
  <li><b>La source.</b> Le signal d'origine de la chaîne, dans sa résolution native.</li>
  <li><b>L'encodage.</b> Le signal est compressé en plusieurs qualités — c'est ce qui permet de le transporter sans
    saturer les réseaux.</li>
  <li><b>Le serveur de diffusion.</b> Il met ces flux à disposition et gère les accès. C'est la seule étape que le
    fournisseur d'abonnement maîtrise réellement, et donc celle qui distingue un service stable d'un service qui
    coupe.</li>
  <li><b>Votre lecteur.</b> L'application sur votre téléviseur, votre box ou votre téléphone, qui réclame le flux et
    le décode à l'écran.</li>
</ul>
<p>Cette chaîne explique pourquoi la qualité d'image n'est jamais entièrement entre les mains du fournisseur : si la
  source diffuse en 720p, aucun serveur au monde n'en fera de la 4K.</p>

<h2 id="playlist">Playlist M3U ou identifiants Xtream</h2>
<p>Pour que votre lecteur sache où chercher, il lui faut une clé d'accès. Elle prend deux formes.</p>
<p><b>La playlist M3U</b> est un simple fichier texte contenant la liste des chaînes et l'adresse de chaque flux.
  Vous recevez une URL longue, vous la collez dans votre application, et la liste se remplit. C'est universel :
  pratiquement tous les lecteurs la comprennent, y compris VLC.</p>
<p><b>Les identifiants Xtream</b> (une adresse de serveur, un nom d'utilisateur, un mot de passe) font la même chose
  autrement. L'avantage : l'application peut organiser le contenu en catégories, afficher les affiches de films et
  gérer la reprise de lecture, ce qu'une simple liste M3U ne permet pas.</p>
<p>Si votre application propose les deux, prenez Xtream — l'interface est nettement plus agréable. La procédure
  détaillée figure dans notre <a href="blog-installer-playlist-m3u.html">guide d'installation</a>.</p>

<h2 id="epg">L'EPG, ce guide des programmes</h2>
<p>L'EPG (<i>Electronic Program Guide</i>) est le fichier qui alimente la grille des programmes : ce qui passe
  maintenant, ce qui suit, et souvent les jours à venir. Il est transmis séparément des flux vidéo.</p>
<p>D'où deux conséquences que beaucoup découvrent en s'énervant : un EPG vide ne signifie pas que votre abonnement
  ne fonctionne pas, et il met parfois plusieurs minutes à se charger à la première ouverture. Laissez tourner avant
  de conclure à un problème.</p>

<h2 id="debit">Quel débit faut-il vraiment</h2>
<p>Les ordres de grandeur utiles, par flux simultané :</p>
<ul>
  <li><b>SD</b> : 3 à 5 Mb/s</li>
  <li><b>HD / Full HD</b> : 8 à 15 Mb/s</li>
  <li><b>4K</b> : 25 à 30 Mb/s</li>
</ul>
<p>Ces chiffres s'additionnent : deux écrans en Full HD réclament le double. Mais le chiffre annoncé par votre
  opérateur n'est pas le bon indicateur. Ce qui compte, c'est la <b>régularité</b> du débit. Une fibre à 1 Gb/s qui
  s'effondre trois secondes toutes les dix minutes donnera une expérience bien pire qu'un ADSL stable à 20 Mb/s,
  parce que la vidéo en direct n'a pas de marge : contrairement à un téléchargement, elle ne peut pas rattraper le
  retard.</p>

<h2 id="differences">Box opérateur, Netflix, IPTV : les différences</h2>
<p>Les trois utilisent internet pour transporter de la vidéo, mais ne fonctionnent pas de la même manière.</p>
<p><b>La box de votre opérateur</b> diffuse sur son propre réseau, séparé de votre trafic internet ordinaire. C'est
  pourquoi la qualité y est très stable : le flux ne se bat pas contre vos téléchargements pour passer.</p>
<p><b>Netflix, Prime Video, Disney+</b> sont des services de vidéo à la demande. Vous choisissez un titre, il se
  lance. Il n'y a pas de notion de direct ni de grille de programmes.</p>
<p><b>Un abonnement IPTV indépendant</b> transite par votre connexion internet classique et propose du direct
  organisé en chaînes, généralement complété d'une section à la demande. C'est ce mélange direct plus catalogue qui
  fait sa particularité — et le fait qu'il passe par votre connexion ordinaire explique qu'il soit plus sensible aux
  conditions de réseau que la box de votre opérateur.</p>

<h2 id="saccade">Pourquoi l'image saccade parfois</h2>
<p>Quand une chaîne se met à bégayer, la cause se trouve à l'un des quatre étages du trajet décrit plus haut. Pour
  l'identifier sans tâtonner, procédez par élimination :</p>
<ul>
  <li><b>Une seule chaîne saccade, les autres non</b> : le problème vient de la source ou de ce flux précis. Rien à
    régler chez vous.</li>
  <li><b>Toutes les chaînes saccadent, sur tous les appareils</b> : c'est votre connexion ou le serveur. Testez un
    autre service vidéo pour trancher.</li>
  <li><b>Un seul appareil est concerné</b> : le Wi-Fi de cet appareil, ou sa puissance de décodage. Un câble
    Ethernet règle la question en une minute.</li>
  <li><b>Uniquement le soir</b> : saturation, chez votre opérateur ou côté serveur. C'est le test qu'il faut faire
    avant de s'engager sur une longue durée.</li>
</ul>
<p>Pour le reste — chaînes, replay, appareils compatibles, prix — le
  <a href="blog-abonnement-iptv-france.html">guide de l'abonnement IPTV en France</a> fait le tour de la
  question.</p>
"""))

ARTICLES.append(dict(
    slug='blog-box-iptv-france.html',
    title="Box IPTV, boîtier ou clé HDMI : que choisir ?",
    desc="Smart TV, Fire TV Stick, boîtier dédié ou Android TV : ce qui fonctionne vraiment pour l'IPTV en France, à quel prix, et ce qu'il ne faut surtout pas acheter.",
    eyebrow="Matériel",
    lead="Avant d'acheter quoi que ce soit : dans la plupart des cas, l'appareil qu'il vous faut est déjà branché à votre téléviseur.",
    read="7 min de lecture",
    toc=[("Vous avez probablement déjà ce qu'il faut", "#deja"),
         ("Smart TV Samsung et LG", "#smarttv"),
         ("Android TV et Google TV", "#androidtv"),
         ("La clé HDMI : le meilleur rapport qualité-prix", "#cle"),
         ("Les boîtiers dédiés", "#boitiers"),
         ("Téléphone, tablette, ordinateur", "#mobile"),
         ("Ce qu'il ne faut pas acheter", "#eviter"),
         ("Récapitulatif par budget", "#recap")],
    body="""
<h2 id="deja">Vous avez probablement déjà ce qu'il faut</h2>
<p>La recherche « box IPTV » laisse croire qu'un appareil spécifique est nécessaire. C'est rarement vrai. Un
  abonnement IPTV n'est qu'une playlist lue par une application : tout appareil capable d'installer une application
  et de décoder de la vidéo fait l'affaire.</p>
<p>Avant de dépenser quoi que ce soit, posez-vous la question dans cet ordre : mon téléviseur est-il connecté ?
  Ai-je déjà une clé HDMI ou une console ? Si la réponse est oui, commencez par là — vous verrez ensuite si quelque
  chose vous manque vraiment.</p>

<h2 id="smarttv">Smart TV Samsung et LG</h2>
<p>Les téléviseurs Samsung tournent sous <b>Tizen</b>, les LG sous <b>webOS</b>. Les deux disposent d'applications de
  lecture IPTV dans leur magasin, et l'installation ne demande aucun matériel supplémentaire.</p>
<p>Deux réserves, qu'il vaut mieux connaître avant d'acheter un abonnement :</p>
<ul>
  <li><b>L'âge du téléviseur.</b> Passé cinq ou six ans, le magasin d'applications finit par ne plus être mis à
    jour, et certaines applications deviennent indisponibles ou instables.</li>
  <li><b>Le choix restreint.</b> Ces deux systèmes proposent nettement moins d'applications qu'Android. Si celle qui
    vous convient n'y est pas, vous n'aurez pas d'alternative.</li>
</ul>
<p>Dans les deux cas, une clé HDMI à 40 € contourne le problème sans remplacer le téléviseur.</p>

<h2 id="androidtv">Android TV et Google TV</h2>
<p>C'est le cas le plus confortable. Les téléviseurs Sony, Philips, TCL et une partie des Hisense embarquent Android
  TV ou Google TV, ce qui donne accès à la totalité des lecteurs IPTV existants, y compris les plus aboutis.</p>
<p>Si vous achetez un téléviseur prochainement et que l'IPTV compte pour vous, c'est le système que je regarderais
  en priorité — non pour la qualité d'image, qui dépend de la dalle, mais pour ne jamais être bloqué côté
  logiciel.</p>

<h2 id="cle">La clé HDMI : le meilleur rapport qualité-prix</h2>
<p>Une clé HDMI se branche derrière le téléviseur et le transforme en appareil connecté, quel que soit son âge. Deux
  familles :</p>
<p><b>Le Fire TV Stick d'Amazon</b>, entre 35 et 70 € selon le modèle. Très répandu en France, simple à mettre en
  route. Le modèle 4K se justifie si votre téléviseur est effectivement 4K ; sinon, la version standard suffit
  amplement.</p>
<p><b>Les clés Android TV</b> (Chromecast avec Google TV et équivalents), dans la même gamme de prix, avec l'accès
  complet au magasin Google.</p>
<p>C'est le conseil que je donne le plus souvent : pour le prix d'un mois et demi d'abonnement, une clé règle
  définitivement toute question de compatibilité, et elle vous suivra sur votre prochain téléviseur.</p>

<h2 id="boitiers">Les boîtiers dédiés</h2>
<p>Les boîtiers de type <b>MAG</b> ou <b>Formuler</b> sont conçus spécifiquement pour ce genre d'usage. Ils coûtent
  généralement entre 80 et 150 €.</p>
<p>Leur intérêt est réel mais précis : l'interface ne fait que ça, la télécommande est simple, et il n'y a pas de
  système d'exploitation généraliste à naviguer. Pour un parent ou un grand-parent qui veut une expérience proche de
  celle d'une box classique, c'est le meilleur choix — et souvent le seul qui évitera les appels au secours.</p>
<p>Pour un utilisateur à l'aise avec un smartphone, en revanche, ils n'apportent pas grand-chose de plus qu'une clé
  à moitié prix.</p>

<h2 id="mobile">Téléphone, tablette, ordinateur</h2>
<p>Ces appareils fonctionnent parfaitement et ne coûtent rien de plus, mais ils répondent à un autre besoin :
  regarder ailleurs que dans le salon, ou tester rapidement un abonnement avant de l'installer sur le
  téléviseur.</p>
<p>Sur ordinateur, VLC lit une playlist M3U sans rien installer d'autre. C'est la manière la plus rapide de vérifier
  qu'un accès fonctionne — utile avant de passer une demi-heure sur la configuration du téléviseur.</p>

<h2 id="eviter">Ce qu'il ne faut pas acheter</h2>
<ul>
  <li><b>Un téléviseur neuf pour faire de l'IPTV.</b> Une clé à 40 € fait exactement le même travail. C'est cent
    fois moins cher.</li>
  <li><b>Un boîtier vendu « avec abonnement à vie inclus ».</b> Aucun service ne peut financer un accès illimité
    avec un paiement unique. Ces offres disparaissent, et vous restez avec un boîtier verrouillé.</li>
  <li><b>Un boîtier de marque inconnue à très bas prix.</b> Sans mises à jour, il devient inutilisable en un ou deux
    ans, et les performances de décodage sont souvent insuffisantes pour de la Full HD fluide.</li>
  <li><b>Un appareil acheté avant d'avoir testé.</b> Vérifiez d'abord sur ce que vous possédez déjà, ne serait-ce
    que sur un téléphone.</li>
</ul>

<h2 id="recap">Récapitulatif par budget</h2>
<ul>
  <li><b>0 €</b> — Smart TV récente, Android TV, ou simplement votre téléphone. Commencez toujours par là.</li>
  <li><b>35 à 70 €</b> — clé HDMI. Le meilleur choix dans la grande majorité des situations.</li>
  <li><b>80 à 150 €</b> — boîtier dédié. Justifié pour un utilisateur qui veut une interface simple et rien
    d'autre.</li>
</ul>
<p>Une fois le matériel choisi, la mise en place prend quelques minutes :
  <a href="blog-installer-playlist-m3u.html">notre guide d'installation</a> détaille la procédure appareil par
  appareil, et le <a href="blog-abonnement-iptv-france.html">guide de l'abonnement IPTV en France</a> couvre les
  chaînes, le replay et les prix.</p>
"""))

BREADCRUMB = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"Accueil","item":"%s/"},
{"@type":"ListItem","position":2,"name":"Blog","item":"%s/blog.html"},
{"@type":"ListItem","position":3,"name":"%%s"}]}
</script>""" % (DOMAIN, DOMAIN)

for a in ARTICLES:
    toc_html = '\n'.join('    <li><a href="%s">%s</a></li>' % (h, t) for t, h in a['toc'])
    art_ld = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"%s","description":"%s",
"inLanguage":"fr-FR","mainEntityOfPage":"%s/%s",
"image":"%s/assets/og-image.webp",
"publisher":{"@type":"Organization","name":"France IPTV","url":"%s/"}}
</script>""" % (a['title'].replace('"', '\\"'), a['desc'].replace('"', '\\"'), DOMAIN, a['slug'], DOMAIN, DOMAIN)

    inner = """
<section class="bhero">
  <div class="bhero__bg" aria-hidden="true"></div>
  <div class="wrap article">
    <span class="eyebrow">%(eyebrow)s</span>
    <h1>%(title)s</h1>
    <p class="lead">%(lead)s</p>
    <div class="bmeta">
      <span><svg><use href="#i-clock"></use></svg> %(read)s</span>
      <span><svg><use href="#i-globe"></use></svg> Guide en français</span>
      <span><a href="blog.html" style="color:var(--gold);font-weight:700">&larr; Tous les articles</a></span>
    </div>
  </div>
</section>

<section class="section" style="padding-top:22px">
  <div class="wrap article">
    <div class="toc">
      <b>Au sommaire</b>
      <ol>
%(toc)s
      </ol>
    </div>
    <div class="prose">
%(body)s
    </div>

    <div class="cta-band">
      <span class="eyebrow">Prêt à commencer ?</span>
      <h2 style="margin-top:18px">Une question avant de choisir ?</h2>
      <p>Dites-nous quel appareil vous utilisez et combien de personnes regardent en même temps chez vous. Nous vous
        dirons quelle offre a du sens — et laquelle n'en a pas.</p>
      <a class="btn btn-wa btn-lg btn-block" href="{{WA_GENERIC}}" target="_blank" rel="noopener"><svg><use href="#i-wa"></use></svg> Écrire sur WhatsApp</a>
      <small>+1 672 896 2871 &bull; réponse en général en quelques minutes</small>
    </div>
  </div>
</section>
""" % dict(eyebrow=a['eyebrow'], title=a['title'], lead=a['lead'], read=a['read'],
           toc=toc_html, body=a['body'])

    html = shell(a['title'], a['desc'], a['slug'], inner,
                 extra_head=art_ld + '\n' + (BREADCRUMB % a['title']))
    (D / a['slug']).write_text(html, encoding='utf-8')
    print('wrote', a['slug'])

# ---------------------------------------------------------------- blog index
cards = '\n'.join("""      <a class="bcard" href="%s">
        <span class="eyebrow">%s</span>
        <h2>%s</h2>
        <p>%s</p>
        <em>Lire l'article &rarr;</em>
      </a>""" % (a['slug'], a['eyebrow'], a['title'], a['desc']) for a in ARTICLES)

blog_inner = """
<section class="bhero">
  <div class="bhero__bg" aria-hidden="true"></div>
  <div class="wrap" style="text-align:center;display:flex;flex-direction:column;align-items:center">
    <span class="eyebrow">Le blog</span>
    <h1 style="max-width:20ch">Guides IPTV en <span style="color:var(--gold)">français</span></h1>
    <p class="lead" style="text-align:center">Des explications claires sur l'IPTV en France : comment choisir,
      comment installer une playlist M3U, et ce que dit vraiment la loi. Sans jargon et sans promesses
      invérifiables.</p>
    <a class="btn btn-wa btn-lg" style="margin-top:26px" href="{{WA_GENERIC}}" target="_blank" rel="noopener"><svg><use href="#i-wa"></use></svg> Poser une question</a>
  </div>
</section>

<section class="section" style="padding-top:34px">
  <div class="wrap">
    <div class="bgrid">
%s
    </div>
  </div>
</section>
""" % cards

(D / 'blog.html').write_text(
    shell("Blog — guides IPTV en français",
          "Guides et explications sur l'IPTV en France : choisir un abonnement, installer une playlist M3U, comprendre le cadre légal.",
          'blog.html', blog_inner), encoding='utf-8')
print('wrote blog.html')

# ---------------------------------------------------------------- robots / sitemap
(D / 'robots.txt').write_text(
    "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN, encoding='utf-8')

pages = ['', 'blog.html'] + [a['slug'] for a in ARTICLES]
prio  = {'': '1.0', 'blog.html': '0.8'}
urls = '\n'.join(
    '  <url>\n    <loc>%s/%s</loc>\n    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>'
    % (DOMAIN, p, 'weekly' if p in prio else 'monthly', prio.get(p, '0.7')) for p in pages)
(D / 'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % urls,
    encoding='utf-8')
print('wrote robots.txt + sitemap.xml')
