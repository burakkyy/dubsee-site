#!/usr/bin/env python3
"""Check generated files and SEO integrity, without pretending to render a browser."""
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from build import ROOT, BASE, LOCALES, HREFLANG, url
from search_copy import SEARCH

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
    files=list(ROOT.glob('*.html'))+list(ROOT.glob('*/*.html'))
    for file in files:
        text=file.read_text();p=Page(text)
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
        text=file.read_text();p=Page(text)
        require(any(tag=='html' and a.get('lang')==code for tag,a in p.tags),f'{code}: document language')
        if code=='ar':require('dir="rtl"' in text,'ar: RTL missing')
        canon=[a['href'] for tag,a in p.tags if tag=='link' and a.get('rel')=='canonical']
        require(canon==[url(code)],f'{code}: canonical')
        alts={a.get('hreflang'):a.get('href') for tag,a in p.tags if tag=='link' and a.get('rel')=='alternate'}
        require(alts==({HREFLANG[c]:url(c) for c in LOCALES}|{'x-default':BASE+'/'}),f'{code}: hreflang')
        schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text).group(1))
        require(len(schema['@graph'])==5,f'{code}: structured data')
        visible=set(LOCALES[code].values())|{SEARCH[code]['question'],SEARCH[code]['answer']}
        require(all(q['name'] in visible and q['acceptedAnswer']['text'] in visible for q in schema['@graph'][-1]['mainEntity']),f'{code}: visible FAQ agreement')
        require(f'<h2 class="section-heading">{SEARCH[code]["heading"]}</h2>' in text,f'{code}: language search heading')
        require(f'<title>{SEARCH[code]["title"]}</title>' in text,f'{code}: search title')
        require('95%' not in text and '%95' not in text,f'{code}: unverified statistic')
        require('google-analytics' not in text,f'{code}: unexpected tracking')
    ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
    sitemap=ET.parse(ROOT/'sitemap.xml').getroot()
    locations={x.find('sm:loc',ns).text for x in sitemap}
    expected={url(c) for c in LOCALES}|{url(c)+x+'.html' for c in ['en','tr'] for x in ['privacy','terms','support']}
    require(locations==expected,'sitemap locations')
    for item in list(sitemap)[:len(LOCALES)]:require(len(item.findall('x:link',ns))==len(LOCALES)+1,'sitemap alternates')
    require('Allow: /' in (ROOT/'robots.txt').read_text(),'robots')
    from legal_pages import source_content
    for code in LOCALES:
        dest=ROOT if code=='en' else ROOT/code
        for name in ['privacy','terms','support']:
            text=(dest/(name+'.html')).read_text()
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
        canonical=[a['href'] for tag,a in Page(file.read_text()).tags if tag=='link' and a.get('rel')=='canonical']
        require(canonical==[address],f'sitemap contains a noncanonical URL: {address}')

    require(set(SEARCH)==set(LOCALES),'search copy covers every language')
    for field in ('title','heading','description','question','answer'):
        values=[SEARCH[code][field] for code in LOCALES]
        require(len(values)==len(set(values)),f'search {field} values are unique')
        require(all(values),f'search {field} is present')
    require(all(len(SEARCH[code]['title'])<=70 for code in LOCALES),'search titles stay within 70 characters')
    require(all(60<=len(SEARCH[code]['description'])<=180 for code in LOCALES),'search descriptions stay within 60–180 characters')
    if failures:raise SystemExit('\n'.join(failures))
    print(f'PASS: {len(files)} HTML files; {len(LOCALES)} localized landing pages; {checked_links} local resource/anchor references; canonical/hreflang; JSON-LD; sitemap; RTL; legal content preservation.')
    print('Browser rendering, screen-reader testing and Lighthouse measurements were not performed.')

if __name__=='__main__':check()
