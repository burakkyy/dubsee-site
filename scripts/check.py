#!/usr/bin/env python3
"""Check generated files and SEO integrity, without pretending to render a browser."""
import json
import re
import xml.etree.ElementTree as ET
from html import escape as html_escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from build import ROOT, BASE, CONFIG, LOCALES, HREFLANG, STORE, url
from search_copy import ABOUT, SEARCH, EXTRA_FAQ
from positioning import FACTS
from guides import guide_urls

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.tags=[]
        self.feed(text)
    def handle_starttag(self,tag,attrs): self.tags.append((tag,dict(attrs)))
    def handle_startendtag(self,tag,attrs): self.handle_starttag(tag,attrs)

def check():
    failures=[]; checked_links=0
    def require(ok,msg):
        if not ok: failures.append(msg)
    files=sorted({*ROOT.glob('*.html'), *ROOT.glob('*/*.html'), *ROOT.glob('*/*/index.html')})
    for file in files:
        text=file.read_text(encoding='utf-8');p=Page(text)
        ids={a['id'] for _,a in p.tags if 'id' in a}
        idlist=[a['id'] for _,a in p.tags if 'id' in a]
        require(len(ids)==len(idlist),f'{file}: duplicate ID')
        require(sum(tag=='h1' for tag,_ in p.tags)==1,f'{file}: H1 count')
        for tag,a in p.tags:
            if tag=='img':require('alt' in a,f'{file}: missing alt')
            values=[a[k] for k in ['href','src'] if k in a]
            if 'srcset' in a:values += [x.strip().split()[0] for x in a['srcset'].split(',')]
            for value in values:
                split=urlsplit(value)
                if split.scheme or split.netloc:continue
                dest=(file.parent/unquote(split.path)).resolve() if split.path else file
                if dest.is_dir():dest=dest/'index.html'
                require(dest.is_file(),f'{file}: broken path {value}')
                if dest==file and split.fragment:require(split.fragment in ids,f'{file}: broken fragment {value}')
                checked_links+=1
    for code in LOCALES:
        file=ROOT/('index.html' if code=='en' else code+'/index.html')
        text=file.read_text(encoding='utf-8');p=Page(text)
        require(any(tag=='html' and a.get('lang')==code for tag,a in p.tags),f'{code}: document language')
        if code=='ar':require('dir="rtl"' in text,'ar: RTL missing')
        canon=[a['href'] for tag,a in p.tags if tag=='link' and a.get('rel')=='canonical']
        require(canon==[url(code)],f'{code}: canonical')
        alts={a.get('hreflang'):a.get('href') for tag,a in p.tags if tag=='link' and a.get('rel')=='alternate'}
        require(alts==({HREFLANG[c]:url(c) for c in LOCALES}|{'x-default':BASE+'/'}),f'{code}: hreflang')
        schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text).group(1))
        require(len(schema['@graph'])==5,f'{code}: structured data')
        visible=set(LOCALES[code].values())|set(FACTS[code].values())|{SEARCH[code]['question'],SEARCH[code]['answer'],ABOUT[code]['q'],ABOUT[code]['a']}
        for item in EXTRA_FAQ[code]:
            visible.add(item['q']); visible.add(item['a'])
        require(all(q['name'] in visible and q['acceptedAnswer']['text'] in visible for q in schema['@graph'][-1]['mainEntity']),f'{code}: visible FAQ agreement')
        app=next(node for node in schema['@graph'] if node['@type']=='SoftwareApplication')
        require(app['description']==ABOUT[code]['a'] and app['isAccessibleForFree'] is True, f'{code}: application facts')
        require(app.get('inLanguage')==code, f'{code}: page language on the app node')
        require(app.get('installUrl')==STORE if STORE else 'installUrl' not in app, f'{code}: store link')
        require(app.get('downloadUrl')==STORE if STORE else 'downloadUrl' not in app, f'{code}: download link')
        require(f'<h2 class="section-heading">{html_escape(SEARCH[code]["heading"])}</h2>' in text,f'{code}: language search heading')
        require(f'<title>{html_escape(SEARCH[code]["title"])}</title>' in text,f'{code}: search title')
        require('Unlimited dubbing' not in text and 'Ad-free listening' not in text, f'{code}: unqualified unlimited or ad-free tag')
        require('95%' not in text and '%95' not in text,f'{code}: unverified statistic')
        require('google-analytics' not in text,f'{code}: unexpected tracking')
    ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
    sitemap=ET.parse(ROOT/'sitemap.xml').getroot()
    locations={x.find('sm:loc',ns).text for x in sitemap}
    guide_locations={address for pair in guide_urls(BASE) for address in pair}
    expected={url(c) for c in LOCALES}|{url(c)+x+'.html' for c in ['en','tr'] for x in ['privacy','terms','support']}|guide_locations
    require(locations==expected,'sitemap locations')
    require(len(list(sitemap))==len(locations),'sitemap has no duplicate URLs')
    raw_sitemap=(ROOT/'sitemap.xml').read_bytes()
    require(not raw_sitemap.startswith(b'\xef\xbb\xbf'),'sitemap has no BOM')
    require(raw_sitemap.startswith(b'<?xml version="1.0" encoding="UTF-8"?>'),'sitemap XML declaration')
    require(b'xmlns:xhtml' not in raw_sitemap and b'\r\n' not in raw_sitemap,'sitemap is a plain LF urlset')
    for item in sitemap:
        require(item.find('sm:lastmod',ns) is not None and not item.findall('x:link',ns),'sitemap entries are loc plus lastmod')
    text_sitemap=(ROOT/'sitemap.txt').read_bytes()
    require(not text_sitemap.startswith(b'\xef\xbb\xbf') and b'\r' not in text_sitemap,'text sitemap is UTF-8 LF without a BOM')
    text_lines=text_sitemap.decode('utf-8').splitlines()
    require(text_lines==[item.find('sm:loc',ns).text for item in sitemap],'text sitemap lists the same URLs in the same order')
    require(all(line.startswith('https://') and ' ' not in line for line in text_lines),'text sitemap lines are absolute URLs')
    robots=(ROOT/'robots.txt').read_text(encoding='utf-8')
    require('Allow: /' in robots,'robots')
    require('User-agent: OAI-SearchBot\nAllow: /' in robots,'OAI-SearchBot allowed')
    require('User-agent: GPTBot\nDisallow: /' in robots,'GPTBot not used for training crawl')
    require('User-agent: Googlebot\nAllow: /' in robots,'Googlebot allowed')
    require('User-agent: Bingbot\nAllow: /' in robots,'Bingbot allowed')
    require('User-agent: *\nAllow: /' in robots and 'User-agent: \\*' not in robots,'wildcard user-agent is a real asterisk')
    require(f'Sitemap: {BASE}/sitemap.xml\nSitemap: {BASE}/sitemap.txt\n' in robots,'robots lists both sitemaps')
    require('location.replace' not in (ROOT/'assets'/'site.js').read_text(encoding='utf-8'),'no forced language redirect in site.js')
    for file in files:
        require('location.replace' not in file.read_text(encoding='utf-8') and 'data-auto-language' not in file.read_text(encoding='utf-8'), f'{file.name}: forced language redirect')
    for en_url, tr_url in guide_urls(BASE):
        for address in (en_url, tr_url):
            guide_file=ROOT/address.removeprefix(BASE+'/')
            if guide_file.is_dir(): guide_file=guide_file/'index.html'
            guide_text=guide_file.read_text(encoding='utf-8')
            guide_page=Page(guide_text)
            guide_canon=[a['href'] for tag,a in guide_page.tags if tag=='link' and a.get('rel')=='canonical']
            require(guide_canon==[address], f'guide canonical {address}')
            guide_alts={a.get('hreflang'):a.get('href') for tag,a in guide_page.tags if tag=='link' and a.get('rel')=='alternate'}
            require(guide_alts=={'en':en_url,'tr':tr_url,'x-default':en_url}, f'guide hreflang {address}')
            require('support.html' in guide_text and (STORE in guide_text if STORE else True), f'guide keeps support and store links {address}')
            guide_schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', guide_text).group(1))
            guide_faq=next(node for node in guide_schema['@graph'] if node['@type']=='FAQPage')
            require(all(html_escape(item['name']) in guide_text and html_escape(item['acceptedAnswer']['text']) in guide_text for item in guide_faq['mainEntity']), f'guide FAQ visible {address}')
    from legal_pages import source_content
    for code in LOCALES:
        dest=ROOT if code=='en' else ROOT/code
        for name in ['privacy','terms','support']:
            text=(dest/(name+'.html')).read_text(encoding='utf-8')
            article=re.search(r'<article[^>]*data-source-content="[^"]+">(.*?)</article>',text,re.S).group(1)
            require(article==source_content(ROOT,name,code),f'{code}/{name}: source content mismatch')
            info=Page(text)
            canonical=[a['href'] for tag,a in info.tags if tag=='link' and a.get('rel')=='canonical']
            actual='tr' if code=='tr' else 'en'
            require(canonical==[url(actual)+name+'.html'],f'{code}/{name}: canonical of source language')
            alts={a['hreflang']:a['href'] for tag,a in info.tags if tag=='link' and a.get('rel')=='alternate'}
            require(alts=={'en':url('en')+name+'.html','tr':url('tr')+name+'.html','x-default':url('en')+name+'.html'},f'{code}/{name}: actual translated content alternates')
            require('data-auto-language' not in text,f'{code}/{name}: unexpected language redirect')
            ogurl=[a['content'] for tag,a in info.tags if tag=='meta' and a.get('property')=='og:url']
            require(ogurl==canonical,f'{code}/{name}: Open Graph canonical alignment')
    for entry in list(sitemap):
        address=entry.find('sm:loc',ns).text
        relative=address.removeprefix(BASE+'/')
        file=ROOT/relative
        if file.is_dir():file=file/'index.html'
        canonical=[a['href'] for tag,a in Page(file.read_text(encoding='utf-8')).tags if tag=='link' and a.get('rel')=='canonical']
        require(canonical==[address],f'sitemap contains a noncanonical URL: {address}')

    require(set(SEARCH)==set(ABOUT)==set(LOCALES),'search copy covers every language')
    for field in ('title','heading','description','question','answer'):
        values=[SEARCH[code][field] for code in LOCALES]
        require(len(values)==len(set(values)),f'search {field} values are unique')
        require(all(values),f'search {field} is present')
    for field in ('q','a'):
        values=[ABOUT[code][field] for code in LOCALES]
        require(len(values)==len(set(values)),f'about {field} values are unique')
        require(all(len(value)>=80 for value in values) if field=='a' else all(values),f'about {field} is present')
    require(all(len(SEARCH[code]['title'])<=70 for code in LOCALES),'search titles stay within 70 characters')
    require(all(60<=len(SEARCH[code]['description'])<=180 for code in LOCALES),'search descriptions stay within 60–180 characters')
    facts=(ROOT/'llms.txt').read_text(encoding='utf-8')
    require(ABOUT['en']['a'] in facts and CONFIG['support_email'] in facts,'llms facts')
    require(all(url(code) in facts and ABOUT[code]['a'] in facts for code in LOCALES),'llms language pages')
    require('apps.apple.com' not in facts and '95%' not in facts,'llms stays factual')
    outdated = (
        'voice pack', 'advanced voice pack', 'ses paketi', 'gelişmiş ses paket',
        'Sprachpaket', 'pack vocal', 'paquete de voz', 'pacchetto vocale', 'pacote de voz',
        'stempakket', 'pakiet głosu', 'röstpaket', 'stemmepakke', 'äänipaketti', 'Äänipaketti',
        'πακέτο φωνής', 'hlasový balíček', 'hlasový balík', 'glasovni paket', 'hangcsomag',
        'pachet de voce', 'гласов пакет', 'häälepaket', 'balss pakotne', 'balso paket',
        'голосовой пакет', 'голосовий пакет', 'حزمة صوت', 'حزمة الصوت', '音声パック', '음성 팩',
        'वॉइस पैक', 'paket suara', 'gói giọng', 'Fetch language data', 'Cached language data',
        'dil verisini almak',
    )
    corpus = '\n'.join(file.read_text(encoding='utf-8') for file in files)
    for phrase in outdated:
        require(phrase not in corpus, f'outdated app-flow claim remains: {phrase}')
    if failures:raise SystemExit('\n'.join(failures))
    print(f'PASS: {len(files)} HTML files; {len(LOCALES)} localized landing pages; {checked_links} local resource/anchor references; canonical/hreflang; JSON-LD; sitemap; RTL; legal content preservation.')
    print('Browser rendering, screen-reader testing and Lighthouse measurements were not performed.')

if __name__=='__main__':check()
