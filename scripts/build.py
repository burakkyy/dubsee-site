#!/usr/bin/env python3
"""Generate crawlable multilingual HTML. Python 3 standard library only."""
import json
import shutil
from datetime import date
from html import escape as esc
from pathlib import Path
from xml.sax.saxutils import escape as xml
from locales import translations
from extras import EXTRAS
from taglines import TAGLINES
from search_copy import SEARCH
from legal_pages import render_legal

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'config.json').read_text())
BASE = CONFIG['base_url'].rstrip('/')
STORE = CONFIG['app_store_url'].strip()
if STORE and not STORE.startswith('https://apps.apple.com/'):
    raise ValueError('app_store_url must be empty or an https://apps.apple.com/ URL')
LOCALES = translations()
HREFLANG = {c:c for c in LOCALES}
assert set(LOCALES) == set(EXTRAS) == set(SEARCH)
assert set(LOCALES) == set(json.loads((ROOT / "scripts/supported-languages.json").read_text())["languages"])

PATHS = {
 'arrow': '<path d="m5 12 14 0m-5-5 5 5-5 5"/>',
 'left': '<path d="m14 6-6 6 6 6"/>',
 'right': '<path d="m10 6 6 6-6 6"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a18 18 0 0 1 0 18 18 18 0 0 1 0-18Z"/>',
 'menu': '<path d="M5 8h14M5 16h14"/>',
 'link': '<path d="m10 14 4-4m-6 6-1 1a4 4 0 0 1-6-6l4-4a4 4 0 0 1 6 0m2 0 1-1a4 4 0 0 1 6 6l-4 4a4 4 0 0 1-6 0"/>',
 'play': '<path d="m9 5 10 7-10 7Z"/>',
 'check': '<path d="m5 12 4 4L19 6"/>',
 'wave': '<path d="M4 10v4m4-8v12m4-16v20m4-16v12m4-8v4"/>',
 'headphones': '<path d="M4 14v-3a8 8 0 0 1 16 0v3M4 12h3v8H4a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2Zm16 0h-3v8h3a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2Z"/>',
 'volume': '<path d="M11 4 5 9H2v6h3l6 5Zm4 4a6 6 0 0 1 0 8m3-11a10 10 0 0 1 0 14"/>',
 'book': '<path d="M4 4h6a2 2 0 0 1 2 2v15a3 3 0 0 0-3-2H3V4Zm16 0h-6a2 2 0 0 0-2 2v15a3 3 0 0 1 3-2h6V4Z"/>',
 'infinity': '<path d="M12 12C9 5 2 5 2 12s7 7 10 0 10-7 10 0-7 7-10 0Z"/>',
 'shield': '<path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6Zm-4 9 3 3 5-6"/>',
 'apple': '<path d="M16.4 1.3c.1 1.2-.4 2.4-1.1 3.3-.8.9-2 1.5-3.1 1.4-.2-1.2.4-2.4 1.1-3.2.8-.9 2-1.5 3.1-1.5ZM20.8 17c-.5 1.2-.8 1.7-1.5 2.8-1 1.4-2.3 3.1-3.9 3.1-1.4 0-1.8-.9-3.7-.9-1.9 0-2.3.9-3.8.9-1.5 0-2.7-1.5-3.7-3C1.4 15.7.4 10.5 2.2 7.7c1.2-2 3.2-3.1 5.1-3.1 1.6 0 2.6.9 3.9.9 1.2 0 2.1-.9 3.9-.9 1.5 0 3.2.8 4.4 2.2-3.9 2.2-3.3 7.9 1.3 10.2Z"/>'
}

def icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{PATHS[name]}</svg>'

def wave():
    heights = [8,16,23,12,27,34,21,12,29,19,9,25,33,17,24,13,28,17,10,22,14,7]
    return '<span class="wave" aria-hidden="true">'+''.join(f'<i style="--h:{h}px"></i>' for h in heights)+'</span>'

def url(code):
    return BASE + ('/' if code == 'en' else f'/{code}/')

def picture(prefix, name, alt, cls='', eager=False):
    widths = (800,1600) if name in ('study','craft') else ((640,1200) if name=='discover' else (600,1000))
    w,h = {'study':(800,343),'craft':(800,450),'discover':(640,427)}.get(name,(600,1301))
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return f'<picture class="{cls}"><source type="image/webp" srcset="{prefix}assets/{name}-{widths[0]}.webp {widths[0]}w, {prefix}assets/{name}-{widths[1]}.webp {widths[1]}w" sizes="(max-width:620px) 90vw, 550px"><img src="{prefix}assets/{name}-{widths[0]}.jpg" width="{w}" height="{h}" alt="{esc(alt)}" loading="{loading}"{priority} decoding="async"></picture>'

def render(code):
    t = LOCALES[code] | EXTRAS[code]
    t['title'] = t['title'].rstrip('.。։')
    if STORE:
        t = t | {'cta':'App Store', 'badge':t['badge'].split('·')[0].strip()}
    prefix = '' if code == 'en' else '../'
    def s(k): return esc(t[k])
    def brand(): return f'<a class="brand" href="#main" aria-label="DUBSEE"><img src="{prefix}assets/app-icon.png" width="37" height="37" alt=""><span class="brand-copy"><strong>DUBSEE</strong><small>{esc(TAGLINES[code])}</small></span></a>'
    def cta():
        if STORE:
            return f'<a class="store-button" href="{esc(STORE)}" rel="external">{icon("apple")}<span>{s("cta")}</span></a>'
        # Real store URL can be connected later; until then use the local download section.
        return f'<a class="store-button" href="#download" aria-label="App Store">{icon("apple")}<span>App Store</span></a>'
    alternates = '\n'.join(f'<link rel="alternate" hreflang="{HREFLANG[c]}" href="{url(c)}">' for c in LOCALES)
    def language_href(c):
        if c == "en" and not prefix:
            return "./"
        if c == "en":
            return ""
        return c + "/"
    def language_current(c):
        return ' aria-current="page"' if c == code else ""
    language_links = ''.join(f'<a class="language-option" data-code="{c}" lang="{c}" hreflang="{HREFLANG[c]}" href="{prefix}{language_href(c)}"{language_current(c)}>{esc(v["native"])}</a>' for c,v in LOCALES.items())
    search = SEARCH[code]
    title = search['title']
    summary = search['description']
    schema = {
      '@context': 'https://schema.org', '@graph': [
        {'@type':'Organization','@id':BASE+'/#organization','name':'DUBSEE','url':BASE+'/', 'logo':BASE+'/assets/app-icon.png','email':CONFIG['support_email']},
        {'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'DUBSEE','inLanguage':list(LOCALES),'publisher':{'@id':BASE+'/#organization'}},
        {'@type':'WebPage','@id':url(code)+'#webpage','url':url(code),'name':title,'description':summary,'inLanguage':code,'isPartOf':{'@id':BASE+'/#website'},'about':{'@id':BASE+'/#app'},'mainEntity':{'@id':BASE+'/#app'}},
        {'@type':'SoftwareApplication','@id':BASE+'/#app','name':'DUBSEE','applicationCategory':'MultimediaApplication','operatingSystem':'iOS','publisher':{'@id':BASE+'/#organization'},'url':BASE+'/','image':BASE+'/assets/app-icon.png','description':t['lead'], 'featureList':[t['realtime'], '30+ '+t['languages'],'10 '+t['voices'],t['backgroundbody'],t['boostbody'],t['librarybody'],t['unlimited'],t['adfree']], **({'installUrl':STORE} if STORE else {})},
        {'@type':'FAQPage','@id':url(code)+'#faq','inLanguage':code,'mainEntity':[{'@type':'Question','name':search['question'],'acceptedAnswer':{'@type':'Answer','text':search['answer']}}]+[{'@type':'Question','name':t[q],'acceptedAnswer':{'@type':'Answer','text':t[a]}} for q,a in [('compatible','compatiblebody'),('free','freebody')]]}
      ]
    }
    steps = ''.join(f'<li><span class="step-icon">{icon(ic)}</span><span class="step-index">0{i}</span><h3>{s("step"+str(i))}</h3><p>{s("step"+str(i)+"body")}</p></li>' for i,ic in [(1,'link'),(2,'globe'),(3,'play')])
    def controls(target, count, label):
        dots = ''.join(f'<button type="button" class="carousel-dot" data-carousel-target="{target}" data-slide="{i}" aria-label="{esc(label)} {i+1} / {count}" aria-pressed="{str(i==0).lower()}"></button>' for i in range(count))
        return f'<div class="carousel-controls" data-controls="{target}"><button type="button" class="round-button" data-carousel-target="{target}" data-direction="-1" aria-label="{esc(label)} −1">{icon("left")}</button><div class="carousel-state"><div class="carousel-dots">{dots}</div><span class="carousel-count" data-carousel-count aria-live="polite">1 / {count}</span></div><button type="button" class="round-button" data-carousel-target="{target}" data-direction="1" aria-label="{esc(label)} +1">{icon("right")}</button></div>'
    gallery = ''.join(f'<figure>{picture(prefix,n,t[label])}<figcaption>{s(label)}</figcaption></figure>' for n,label in [('home','step3'),('open','step1'),('player','boost'),('languages','step2')])
    faq = f'<details class="faq-item" open><summary>{esc(search["question"])}</summary><p>{esc(search["answer"])}</p></details>' + ''.join(f'<details class="faq-item"><summary>{s(q)}</summary><p>{s(a)}</p></details>' for q,a in [('compatible','compatiblebody'),('free','freebody')])
    legal = ''.join(f'<a href="{file}.html">{s(k)} </a>' for k,file in [('privacy','privacy'),('terms','terms'),('support','support')])
    schema_json = json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')
    return f'''<!doctype html>
<html lang="{code}" dir="{'rtl' if code=='ar' else 'ltr'}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{esc(summary)}">
{('<meta name="google-site-verification" content="'+esc(CONFIG.get('google_site_verification',''),quote=True)+'">') if CONFIG.get('google_site_verification') else ''}
<meta name="theme-color" content="#ffffff"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url(code)}">
{alternates}<link rel="alternate" hreflang="x-default" href="{BASE}/">
<link rel="icon" href="{prefix}assets/app-icon.png" type="image/png"><link rel="apple-touch-icon" href="{prefix}assets/app-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="DUBSEE"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(summary)}"><meta property="og:url" content="{url(code)}"><meta property="og:image" content="{BASE}/assets/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="800"><meta property="og:image:alt" content="{esc(summary)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(summary)}"><meta name="twitter:image" content="{BASE}/assets/og.jpg">
<script data-auto-language>
(() => {{
  if (!['https:','http:'].includes(location.protocol)) return;
  if (document.documentElement.lang !== 'en') return;
  const root = new URL({json.dumps(BASE+'/')});
  if (location.pathname !== root.pathname && location.pathname !== root.pathname + 'index.html') return;
  if (new URLSearchParams(location.search).has('lang')) return;
  const supported = {json.dumps(list(LOCALES))};
  let saved = ''; try {{ saved = localStorage.getItem('dubsee-language') || ''; }} catch (_) {{}}
  const languages = saved && supported.includes(saved) ? [saved] : Array.from(navigator.languages || [navigator.language || 'en']);
  const chosen = languages.map(x => x.toLowerCase().split(/[-_]/)[0]).find(x => supported.includes(x)) || 'en';
  if (chosen !== 'en') location.replace(new URL(chosen + '/' + location.search + location.hash, root).href);
}})();
</script>
<link rel="stylesheet" href="{prefix}assets/site.css"><link rel="stylesheet" href="{prefix}assets/mobile-refinement.css"><script src="{prefix}assets/site.js" defer></script>
<script type="application/ld+json">{schema_json}</script>
</head>
<body>
<a class="skip" href="#main">{s('how')}</a>
<div class="header-shell"><header class="site-header wrap">{brand()}
<nav class="main-nav" id="main-nav" aria-label="DUBSEE"><a href="#how">{s('how')}</a><a href="#features">{s('features')}</a><a href="#faq">{s('faq')}</a></nav>
<div class="header-actions"><a class="header-store" href="{esc(STORE) if STORE else '#download'}" aria-label="App Store">{icon('apple')}</a>
<details class="language-picker"><summary aria-label="{s('languages')}">{icon('globe')}<span>{code.upper()}</span></summary><div class="language-panel"><input type="search" data-language-search placeholder="{s('languages')}" aria-label="{s('languages')}" autocomplete="off"><nav class="language-list" aria-label="{s('languages')}">{language_links}</nav></div></details>
<details class="mobile-menu"><summary aria-label="{s('how')} / {s('features')}">{icon('menu')}</summary><nav aria-label="DUBSEE"><a href="#how">{s('how')}</a><a href="#features">{s('features')}</a><a href="#faq">{s('faq')}</a><a href="privacy.html">{s('privacy')}</a><a href="terms.html">{s('terms')}</a><a href="support.html">{s('support')}</a></nav></details></div></header></div>
<main id="main">
<section class="hero"><div class="wrap"><div class="hero-main"><div class="hero-copy"><div class="hero-kicker"><span>{s('badge')}</span></div><h1>{s('title')} <span>{s('accent')}</span></h1><p class="hero-lead">{s('lead')}</p><div class="cta-row">{cta()}<a class="text-link" href="#how">{s('how')}{icon('arrow')}</a></div><div class="hero-proof"><span>{icon('check')}30+ {s('languages')}</span><span>{icon('check')}10 {s('voices')}</span></div></div>
<div class="hero-art"><span class="halo" aria-hidden="true"></span><div class="hero-phone">{picture(prefix,'home',t['gallery'],eager=True)}</div><div class="float-card language-chip" aria-hidden="true"><span class="chip-icon">{icon('globe')}</span><div><strong>30+ {s('languages')}</strong><small>English · Türkçe · 日本語</small></div></div><div class="float-card audio-chip" aria-hidden="true"><div class="audio-label">{icon('wave')}{s('realtime')}</div>{wave()}</div></div></div>
<div class="metrics"><div class="metric"><strong>30+</strong><span>{s('languages')}</span></div><div class="metric"><strong>10</strong><span>{s('voices')}</span></div><div class="metric">{icon('wave')}<span>{s('realtime')}</span></div></div></div></section>
<section class="section listen wrap" id="listen" lang="{code}"><p class="eyebrow">YouTube · {esc(t['native'])}</p><h2 class="section-heading">{esc(search['heading'])}</h2><p class="section-sub">{esc(summary)}</p></section>
<section class="section wrap" id="how"><div class="how-heading"><div><p class="eyebrow">DUBSEE / 01</p><h2 class="section-heading">{s('how')}</h2></div><span class="brand-stamp"><img src="{prefix}assets/app-icon.png" alt="" width="32" height="32"></span></div><ol class="steps">{steps}</ol></section>
<section class="section life"><div class="wrap"><div class="life-heading"><div><p class="eyebrow">DUBSEE / 02</p><h2 class="section-heading">{s('life')}</h2></div></div><div class="stories" id="story-track" data-carousel tabindex="0" role="region" aria-label="{s('life')}"><article class="story study">{picture(prefix,'study',t['studybody'])}<div class="story-copy"><p class="eyebrow">01 / {s('study')}</p><h3>{s('study')}</h3><p>{s('studybody')}</p></div></article><article class="story craft">{picture(prefix,'craft',t['craftbody'])}<div class="story-copy"><p class="eyebrow">02 / {s('craft')}</p><h3>{s('craft')}</h3><p>{s('craftbody')}</p></div></article></div>{controls("story-track",2,t["life"])}</div></section>
<section class="section features wrap" id="features"><p class="eyebrow">DUBSEE / 03</p><h2 class="section-heading">{s('features')}<span class="blue">.</span></h2><div class="feature-tags"><span>{icon('infinity')}{s('unlimited')}</span><span>{icon('wave')}10 {s('voices')}</span><span>{icon('shield')}{s('adfree')}</span><span>{icon('globe')}30+ {s('languages')}</span></div><div class="feature-grid" id="feature-track" data-carousel tabindex="0" role="region" aria-label="{s('features')}"><article class="feature-card blue-card">{icon('headphones')}<h3>{s('background')}</h3><p>{s('backgroundbody')}</p><div class="mini-player" aria-hidden="true"><img src="{prefix}assets/app-icon.png" alt="" width="35" height="35">{wave()}{icon('play')}</div></article><article class="feature-card">{icon('volume')}<h3>{s('boost')}</h3><p>{s('boostbody')}</p><div class="boost-ui" aria-hidden="true"><div class="boost-label">{icon('volume')}<span>+6 dB</span></div><div class="slider-art"></div></div></article><article class="feature-card">{icon('book')}<h3>{s('library')}</h3><p>{s('librarybody')}</p><div class="library-art" aria-hidden="true"><span>{icon('play')}</span><span>{icon('book')}</span><span>{icon('link')}</span></div></article></div>{controls("feature-track",3,t["features"])}<p class="feature-note">{s('freebody')}</p></section>
<section class="gallery-section wrap" aria-labelledby="gallery-heading"><div class="gallery-head"><div><p class="eyebrow">DUBSEE / 04</p><h2 class="section-heading" id="gallery-heading">{s('gallery')}</h2></div><div class="gallery-controls"><button class="round-button" type="button" data-gallery-shift="-1" aria-label="{s('gallery')} −1">{icon('left')}</button><button class="round-button" type="button" data-gallery-shift="1" aria-label="{s('gallery')} +1">{icon('right')}</button></div></div><div class="gallery-track" tabindex="0" role="region" aria-label="{s('gallery')}">{gallery}</div></section>
<section class="section faq-section" id="faq"><div class="wrap faq-layout"><div class="faq-intro"><p class="eyebrow">DUBSEE / 05</p><h2 class="section-heading">{s('faq')}<span class="blue">.</span></h2><a class="text-link" href="mailto:{esc(CONFIG['support_email'])}">{s('support')}{icon('arrow')}</a></div><div class="faq-list">{faq}<details class="faq-item"><summary>{s('how')}</summary><p>{s('step1body')} {s('step2body')} {s('step3body')}</p></details></div></div></section>
<section class="closing wrap" id="download"><img src="{prefix}assets/app-icon.png" alt="DUBSEE" width="63" height="63"><h2 class="section-heading">{s('finish')}</h2>{cta()}</section>
</main>
<footer class="site-footer"><div class="wrap"><div class="footer-top">{brand()}<nav class="footer-links" aria-label="{s('support')}">{legal}</nav></div><div class="footer-bottom"><p>{s('disclaimer')}</p><span class="copyright">© {date.today().year} DUBSEE</span></div></div></footer>
<aside class="mobile-store" aria-label="DUBSEE">{brand()}{cta()}</aside>
</body></html>'''

def build():
    for code in LOCALES:
        dest = ROOT if code == 'en' else ROOT/code
        dest.mkdir(exist_ok=True)
        page = render(code)
        (dest/'index.html').write_text(page,encoding='utf-8')
        for name in ['privacy','terms','support']:
            (dest/(name+'.html')).write_text(render_legal(ROOT,name,code,page,LOCALES,BASE),encoding='utf-8')
    entries = []
    for c in LOCALES:
        links = ''.join(f'<xhtml:link rel="alternate" hreflang="{HREFLANG[a]}" href="{xml(url(a))}"/>' for a in LOCALES)
        entries.append(f'<url><loc>{xml(url(c))}</loc>{links}<xhtml:link rel="alternate" hreflang="x-default" href="{xml(BASE)}/"/></url>')
    for code in ['en','tr']:
        for name in ['privacy','terms','support']:
            entries.append(f'<url><loc>{xml(url(code))}{name}.html</loc></url>')
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'+''.join(entries)+'</urlset>')
    (ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
    print(f'Built {len(LOCALES)} languages, sitemap.xml and robots.txt.')

if __name__ == '__main__':
    build()
