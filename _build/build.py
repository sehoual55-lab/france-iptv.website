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
        <li><a href="blog-installer-playlist-m3u.html">Installer une playlist M3U</a></li>
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
<p>Et si rien de tout cela ne suffit : écrivez-nous sur WhatsApp en indiquant votre appareil, l'application utilisée
  et ce qui s'affiche exactement à l'écran. Avec ces trois informations, le dépannage prend en général deux
  minutes.</p>
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
