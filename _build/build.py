#!/usr/bin/env python3
"""Build the standalone IPTV guide site: folder-based clean URLs, no redirects."""
import pathlib, json, re, shutil

# ============================================================ CONFIGURATION
# CHANGEZ CES DEUX LIGNES, c'est tout ce qui dépend de votre domaine.
DOMAIN = 'https://guide-iptv.fr'      # <- votre domaine, sans barre oblique finale
BRAND  = 'Guide IPTV'                 # <- le nom affiché dans l'en-tête

D = pathlib.Path(__file__).parent.parent
SRC = json.loads((pathlib.Path(__file__).parent / 'articles.json').read_text(encoding='utf-8'))

NBSP = '\u202f'
_TYPO = [(' ?', NBSP + '?'), (' !', NBSP + '!'), (' ;', NBSP + ';'),
         (' :', NBSP + ':'), ('« ', '«' + NBSP), (' »', NBSP + '»'), (' %', NBSP + '%')]


def _chunk(s):
    for a, b in _TYPO:
        s = s.replace(a, b)
    return s


def typo(s):
    """French spacing, applied to text only — never inside tags, style or script."""
    out, i = [], 0
    for m in re.finditer(r'<(style|script)\b.*?</\1>', s, re.S):
        out.append(_outside(s[i:m.start()])); out.append(m.group(0)); i = m.end()
    out.append(_outside(s[i:]))
    return ''.join(out)


def _outside(s):
    out, i = [], 0
    for m in re.finditer(r'<[^>]+>', s):
        out.append(_chunk(s[i:m.start()])); out.append(m.group(0)); i = m.end()
    out.append(_chunk(s[i:]))
    return ''.join(out)


CSS = """
:root{
  --paper:#FBFAF7; --paper-2:#F3F1EA; --card:#FFFFFF;
  --ink:#1C1B18;   --body:#3E3B35;   --muted:#6E6A61; --faint:#9C978C;
  --rule:#E2DED3;  --rule-2:#EFECE3;
  --accent:#2F5D50; --accent-hi:#3E7A69; --accent-soft:#EAF1EE;
  --r-s:8px; --r-m:12px; --r-l:18px;
  --ease:cubic-bezier(.22,.61,.36,1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;scroll-padding-top:88px;-webkit-text-size-adjust:100%}
body{
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  background:var(--paper);color:var(--body);line-height:1.72;font-size:17px;
  overflow-x:clip;-webkit-font-smoothing:antialiased;
}
img,svg{display:block;max-width:100%}
a{color:inherit}
h1,h2,h3{font-family:"Source Serif 4",Georgia,serif;color:var(--ink);line-height:1.2;letter-spacing:-.015em;font-weight:600}
::selection{background:var(--accent-soft)}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
.wrap{width:min(1080px,100% - 40px);margin-inline:auto}
.narrow{width:min(680px,100% - 40px);margin-inline:auto}

/* ---------------- header ---------------- */
.hdr{position:sticky;top:0;z-index:50;background:rgba(251,250,247,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--rule)}
.hdr__in{display:flex;align-items:center;justify-content:space-between;gap:24px;height:64px}
.logo{display:inline-flex;align-items:baseline;gap:8px;text-decoration:none;font-family:"Source Serif 4",Georgia,serif;font-size:19px;font-weight:600;color:var(--ink)}
.logo i{font-style:normal;color:var(--accent)}
.nav{display:flex;gap:26px;font-size:15px}
.nav a{color:var(--muted);text-decoration:none;transition:color .2s var(--ease)}
.nav a:hover,.nav a.is-active{color:var(--accent)}
@media(max-width:680px){.nav{gap:18px;font-size:14px}.logo{font-size:17px}}

/* ---------------- hero ---------------- */
.hero{padding:76px 0 52px;border-bottom:1px solid var(--rule)}
.hero h1{font-size:clamp(32px,5vw,50px);max-width:16ch;margin-bottom:20px}
.hero p{font-size:19px;color:var(--muted);max-width:60ch}
.kicker{display:inline-block;font-family:Inter,sans-serif;font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:18px}

/* ---------------- article list ---------------- */
.list{padding:56px 0 84px}
.entry{display:block;text-decoration:none;padding:30px 0;border-bottom:1px solid var(--rule-2);transition:.25s var(--ease)}
.entry:hover{padding-left:8px}
.entry:hover h2{color:var(--accent)}
.entry h2{font-size:24px;margin-bottom:9px;transition:color .25s var(--ease)}
.entry p{color:var(--muted);font-size:16px;max-width:68ch}
.entry .meta{display:flex;gap:14px;font-size:13px;color:var(--faint);margin-top:12px;font-family:Inter,sans-serif}

/* ---------------- article page ---------------- */
.ahero{padding:64px 0 34px}
.ahero h1{font-size:clamp(29px,4.4vw,42px);max-width:22ch;margin-bottom:18px}
.ahero .lead{font-size:19.5px;color:var(--muted);line-height:1.62}
.ahero .meta{display:flex;gap:16px;font-size:13.5px;color:var(--faint);margin-top:22px;flex-wrap:wrap}
.toc{background:var(--paper-2);border:1px solid var(--rule);border-radius:var(--r-l);padding:24px 26px;margin:14px 0 42px}
.toc b{display:block;font-family:Inter,sans-serif;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:12px}
.toc ol{margin-left:18px;font-size:15.5px;line-height:1.9}
.toc a{color:var(--muted);text-decoration:none}
.toc a:hover{color:var(--accent);text-decoration:underline}
.prose{padding-bottom:34px}
.prose h2{font-size:27px;margin:46px 0 16px;padding-top:6px}
.prose p{margin-bottom:19px}
.prose ul,.prose ol{margin:0 0 22px 22px}
.prose li{margin-bottom:10px}
.prose b{color:var(--ink);font-weight:600}
.prose i{color:var(--muted)}
.prose a{color:var(--accent);text-decoration:underline;text-underline-offset:2px;text-decoration-thickness:1px}
.prose a:hover{background:var(--accent-soft)}
.next{margin:44px 0 76px;padding:28px 30px;background:var(--paper-2);border:1px solid var(--rule);border-radius:var(--r-l)}
.next b{display:block;font-family:Inter,sans-serif;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:14px}
.next ul{list-style:none;margin:0}
.next li{margin-bottom:9px}
.next a{color:var(--ink);text-decoration:none;font-weight:500}
.next a:hover{color:var(--accent);text-decoration:underline}

/* ---------------- footer ---------------- */
.ftr{border-top:1px solid var(--rule);padding:44px 0 56px;font-size:14.5px;color:var(--muted)}
.ftr__nav{display:flex;flex-wrap:wrap;gap:20px;margin-bottom:22px}
.ftr__nav a{color:var(--muted);text-decoration:none}
.ftr__nav a:hover{color:var(--accent)}
.ftr .note{font-size:13.5px;color:var(--faint);max-width:76ch;line-height:1.7}
.ftr .bot{margin-top:22px;padding-top:18px;border-top:1px solid var(--rule-2);font-size:13.5px;color:var(--faint)}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""


def page(title, desc, path, inner, extra_head=''):
    """path is '' for the home page, else 'slug'."""
    url = DOMAIN + '/' + (path + '/' if path else '')
    return typo("""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#FBFAF7">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(url)s">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="alternate" hreflang="fr" href="%(url)s">
<meta property="og:type" content="article">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="%(brand)s">
<meta property="og:url" content="%(url)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
%(extra_head)s
<style>%(css)s</style>
</head>
<body>
<header class="hdr">
  <div class="wrap hdr__in">
    <a class="logo" href="/"><span>%(brand_a)s</span><i>%(brand_b)s</i></a>
    <nav class="nav" aria-label="Navigation principale">
      <a href="/">Tous les guides</a>
      <a href="/comment-fonctionne-iptv/">Comprendre</a>
      <a href="/installer-playlist-m3u/">Installer</a>
      <a href="/iptv-legal-france/">Cadre légal</a>
    </nav>
  </div>
</header>
<main>
%(inner)s
</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr__nav">
      <a href="/">Accueil</a>
      <a href="/comment-fonctionne-iptv/">Comment fonctionne l'IPTV</a>
      <a href="/choisir-abonnement-iptv/">Bien choisir</a>
      <a href="/box-iptv-appareils/">Appareils</a>
      <a href="/installer-playlist-m3u/">Installation</a>
      <a href="/film-francais-iptv/">Piste audio française</a>
      <a href="/iptv-legal-france/">Cadre légal</a>
    </div>
    <p class="note">%(brand)s est un site d'information indépendant. Nous ne vendons aucun abonnement et ne
      distribuons aucun contenu. Les explications publiées ici portent sur le fonctionnement de la technologie IPTV
      et sur le cadre légal français ; il appartient à chacun de n'accéder qu'aux contenus qu'il est légalement
      autorisé à regarder. Les marques citées appartiennent à leurs propriétaires respectifs et sont mentionnées à
      titre de compatibilité technique.</p>
    <div class="bot">&copy; <span id="yr">2026</span> %(brand)s</div>
  </div>
</footer>
<script>document.getElementById('yr').textContent=new Date().getFullYear();</script>
</body>
</html>
""" % dict(title=title, desc=desc, url=url, css=CSS, inner=inner, extra_head=extra_head,
           brand=BRAND, brand_a=BRAND.split()[0], brand_b=' ' + ' '.join(BRAND.split()[1:])))


# ============================================================ ARTICLES
ORDER = ['comment-fonctionne-iptv', 'choisir-abonnement-iptv', 'box-iptv-appareils',
         'installer-playlist-m3u', 'film-francais-iptv', 'iptv-legal-france']

RELATED = {
    'comment-fonctionne-iptv': ['choisir-abonnement-iptv', 'box-iptv-appareils', 'installer-playlist-m3u'],
    'choisir-abonnement-iptv': ['comment-fonctionne-iptv', 'box-iptv-appareils', 'iptv-legal-france'],
    'box-iptv-appareils':      ['installer-playlist-m3u', 'comment-fonctionne-iptv', 'choisir-abonnement-iptv'],
    'installer-playlist-m3u':  ['film-francais-iptv', 'box-iptv-appareils', 'comment-fonctionne-iptv'],
    'film-francais-iptv':      ['installer-playlist-m3u', 'comment-fonctionne-iptv', 'box-iptv-appareils'],
    'iptv-legal-france':       ['comment-fonctionne-iptv', 'choisir-abonnement-iptv'],
}

arts = {a['slug']: a for a in SRC}
assert set(arts) == set(ORDER), 'articles.json ne correspond pas à ORDER'

# ============================================================ WRITE PAGES
for slug in ORDER:
    a = arts[slug]
    toc = '\n'.join('      <li><a href="%s">%s</a></li>' % (h, t) for t, h in a['toc'])
    rel = '\n'.join('      <li><a href="/%s/">%s</a></li>' % (r, arts[r]['title']) for r in RELATED[slug])
    ld = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"%s","description":"%s",
"inLanguage":"fr-FR","mainEntityOfPage":"%s/%s/","isAccessibleForFree":true,
"publisher":{"@type":"Organization","name":"%s","url":"%s/"}}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"Accueil","item":"%s/"},
{"@type":"ListItem","position":2,"name":"%s"}]}
</script>""" % (a['title'].replace('"', '\\"'), a['desc'].replace('"', '\\"'),
                DOMAIN, slug, BRAND, DOMAIN, DOMAIN, a['title'].replace('"', '\\"'))

    inner = """
<section class="ahero">
  <div class="narrow">
    <span class="kicker">%(eyebrow)s</span>
    <h1>%(title)s</h1>
    <p class="lead">%(lead)s</p>
    <div class="meta"><span>%(read)s</span><span>Guide en français</span><span><a href="/" style="color:var(--accent)">&larr; Tous les guides</a></span></div>
  </div>
</section>
<section>
  <div class="narrow">
    <div class="toc">
      <b>Au sommaire</b>
      <ol>
%(toc)s
      </ol>
    </div>
    <div class="prose">
%(body)s
    </div>
    <div class="next">
      <b>À lire ensuite</b>
      <ul>
%(rel)s
      </ul>
    </div>
  </div>
</section>
""" % dict(eyebrow=a['eyebrow'], title=a['title'], lead=a['lead'], read=a['read'],
           toc=toc, body=a['body'], rel=rel)

    out = D / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(
        page('%s | %s' % (a['short'], BRAND), a['desc'], slug, inner, extra_head=ld), encoding='utf-8')
    print('wrote', slug + '/index.html')

# ---------------------------------------------------------------- home page
entries = '\n'.join("""      <a class="entry" href="/%s/">
        <h2>%s</h2>
        <p>%s</p>
        <div class="meta"><span>%s</span><span>%s</span></div>
      </a>""" % (s, arts[s]['title'], arts[s]['desc'], arts[s]['eyebrow'], arts[s]['read'])
                    for s in ORDER)

home = """
<section class="hero">
  <div class="wrap">
    <span class="kicker">Guides indépendants</span>
    <h1>Comprendre l'IPTV, sans jargon et sans promesse creuse</h1>
    <p>Comment la technologie fonctionne, quels appareils la prennent en charge, comment installer une playlist,
      et ce que dit vraiment la loi française. Des explications écrites pour être utiles, pas pour vous vendre
      quelque chose.</p>
  </div>
</section>
<section class="list">
  <div class="wrap">
%s
  </div>
</section>
""" % entries

home_ld = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite","name":"%s","url":"%s/","inLanguage":"fr-FR"}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ItemList","itemListElement":[
%s]}
</script>""" % (BRAND, DOMAIN, ',\n'.join(
    '{"@type":"ListItem","position":%d,"url":"%s/%s/","name":"%s"}'
    % (i, DOMAIN, s_, arts[s_]['title'].replace('"', '\\"')) for i, s_ in enumerate(ORDER, 1)))

(D / 'index.html').write_text(
    page("%s — comprendre l'IPTV en France" % BRAND,
         "Guides indépendants sur l'IPTV en France : fonctionnement, appareils compatibles, installation d'une playlist M3U, piste audio française et cadre légal.",
         '', home, extra_head=home_ld), encoding='utf-8')
print('wrote index.html')

# ---------------------------------------------------------------- robots / sitemap / vercel
(D / 'robots.txt').write_text("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN, encoding='utf-8')

urls = ['  <url>\n    <loc>%s/</loc>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>' % DOMAIN]
urls += ['  <url>\n    <loc>%s/%s/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>'
         % (DOMAIN, s) for s in ORDER]
(D / 'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n'
    % '\n'.join(urls), encoding='utf-8')

(D / 'vercel.json').write_text(json.dumps({
    "$schema": "https://openapi.vercel.sh/vercel.json",
    "trailingSlash": True,
    "headers": [
        {"source": "/(.*)", "headers": [
            {"key": "X-Content-Type-Options", "value": "nosniff"},
            {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
            {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
            {"key": "Permissions-Policy", "value": "geolocation=(), microphone=(), camera=(), payment=()"},
            {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
            {"key": "Cache-Control", "value": "public, max-age=0, s-maxage=3600, must-revalidate"}
        ]}
    ]
}, indent=2) + '\n', encoding='utf-8')
print('wrote robots.txt + sitemap.xml + vercel.json')
