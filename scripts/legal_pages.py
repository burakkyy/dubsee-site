"""Dedicated pages using the supplied site's actual English/Turkish articles."""
import re
import json
from html import escape
from pathlib import Path

def source_content(root, name, code):
    source = root/'content'/f'{name}.source'
    text = source.read_text()
    article = re.search(r'<article>(.*?)</article>',text,re.S).group(1)
    parts = re.split(r'<p class="lang">(?:English|Türkçe)</p>',article)
    # The source publishes English and Turkish; do not invent different legal terms.
    content = parts[2] if code == 'tr' else parts[1]
    return content.strip().replace('DubSee','DUBSEE')

def render_legal(root, name, code, landing, locales, base):
    prefix='' if code=='en' else '../'
    lang='tr' if code=='tr' else 'en'
    t=locales[code]
    title='DUBSEE — '+t[{'privacy':'privacy','terms':'terms','support':'support'}[name]]
    head = re.search(r'<head>(.*?)</head>',landing,re.S).group(1)
    head = re.sub(r'<title>.*?</title>', '<title>'+escape(title)+'</title>',head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '',head,flags=re.S)
    canonical=base+('/tr/' if lang=='tr' else '/')+name+'.html'
    head=re.sub(r'<script data-auto-language>.*?</script>', '', head, flags=re.S)
    head=re.sub(r'<link rel="(?:canonical|alternate)"[^>]*>', '', head)
    head += '<link rel="canonical" href="'+canonical+'">'
    for actual in ['en','tr']:
        address=base+('/tr/' if actual=='tr' else '/')+name+'.html'
        head += '<link rel="alternate" hreflang="'+actual+'" href="'+address+'">'
    head += '<link rel="alternate" hreflang="x-default" href="'+base+'/'+name+'.html">'
    descriptions={
        'en':{
            'privacy':'How DUBSEE handles account data, on-device storage, analytics, advertising and subscriptions.',
            'terms':'Terms for using DUBSEE, including content access, subscriptions, cancellation and responsibilities.',
            'support':'Contact DUBSEE support and find help with dubbing, voice downloads, local data and subscriptions.'},
        'tr':{
            'privacy':'DUBSEE hesap bilgileri, cihaz içi veriler, analiz, reklam ve aboneliklerine ilişkin gizlilik politikası.',
            'terms':'DUBSEE kullanımı, içerik erişimi, abonelikler, iptal ve kullanıcı sorumluluklarına ilişkin şartlar.',
            'support':'DUBSEE desteğine ulaşın; dublaj, ses paketi indirme, cihaz verileri ve abonelikler hakkında yardım alın.'}}
    description=descriptions[lang][name]
    head=re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*("[^>]*>)', lambda m:m[1]+escape(description,quote=True)+m[2],head)
    head=re.sub(r'(<meta property="og:url" content=")[^"]+("[^>]*>)',lambda m:m[1]+canonical+m[2],head)
    head=re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]+("[^>]*>)',lambda m:m[1]+escape(title,quote=True)+m[2],head)
    schema={'@context':'https://schema.org','@type':'WebPage','name':title,'description':description,'inLanguage':lang,'url':canonical}
    head += '<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>'
    header = re.search(r'<div class="header-shell">.*?</header></div>',landing,re.S).group(0)
    footer = re.search(r'<footer class="site-footer">.*?</footer>',landing,re.S).group(0)
    for section in ['main','how','features','faq','download']:
        header=header.replace(f'href="#{section}"',f'href="index.html#{section}"')
        footer=footer.replace(f'href="#{section}"',f'href="index.html#{section}"')
    # Match locale changes to the same legal page, not back to a landing page.
    header=re.sub(r'(class="language-option"[^>]*data-code="([^"]+)"[^>]*href=")[^"]+("[^>]*>)',lambda m:m[1]+prefix+('' if m[2]=='en' else m[2]+'/')+name+'.html'+m[3],header)
    article=source_content(root,name,code)
    original=(root/'content'/f'{name}.source').read_text()
    meta=re.search(r'<p class="meta">(.*?)</p>',original,re.S)
    updated=''
    if name!='support' and meta:
        updated='<p class="legal-source-language" lang="en">'+meta[1]+'</p>'
    # Clear source-language identification for text not published in a chosen locale.
    note='' if code in ('en','tr') else '<p class="legal-source-language">English · Türkçe</p>'
    return f'''<!doctype html><html lang="{code}" dir="{'rtl' if code=='ar' else 'ltr'}"><head>{head}</head><body>{header}
<main id="main" class="legal-page wrap"><p class="eyebrow">DUBSEE</p><h1 class="section-heading">{escape(t[name])}</h1>{updated}{note}<article class="legal-copy" lang="{lang}" dir="ltr" data-source-content="{name}">{article}</article></main>{footer}</body></html>'''
