#!/usr/bin/env python3
"""Compact preview: localized HTML text plus one shared copy of each image."""
import base64,json,re,io
from pathlib import Path
from PIL import Image
from build import ROOT,LOCALES

def safe_json(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')

def main():
    assets={};pages={}
    for code in LOCALES:
        for name in ['index','privacy','terms','support']:
            html=(ROOT/('' if code=='en' else code)/(name+'.html')).read_text()
            body=re.search(r'<body>([\s\S]*)</body>',html)[1]
            suffix='' if name=='index' else '-'+name;key=code+suffix
            body=re.sub(r'(<a class="language-option"[^>]*data-code="([^"]+)"[^>]*href=")[^"]+("[^>]*>)',lambda m:m[1]+'#page-'+m[2]+suffix+m[3],body)
            for legal in ['privacy','terms','support']:
                body=re.sub(r'href="(?:\.\./)?'+legal+r'\.html"',f'href="#page-{code}-{legal}"',body)
            body=re.sub(r'href="index.html(?:#([^"]*))?"',lambda m:'href="#page-'+code+(':'+m[1] if m[1] else '')+'"',body)
            body=re.sub(r'<source\b[^>]*>','',body)
            for src in re.findall(r'<img[^>]*src="([^"]+)"',body):
                file=ROOT/'assets'/src.split('/')[-1]
                if file.name in assets:continue
                if file.suffix=='.jpg':
                    high_resolution = file.name.startswith(('study-','craft-'))
                    original = file.with_name(file.stem.split('-')[0]+'-1600.webp') if high_resolution else file
                    image=Image.open(original).convert('RGB');image.thumbnail((1200 if high_resolution else 540,2000));output=io.BytesIO();image.save(output,'JPEG',quality=87 if high_resolution else 80,optimize=True)
                    data=output.getvalue();mime='image/jpeg'
                else:data=file.read_bytes();mime='image/png'
                assets[file.name]='data:'+mime+';base64,'+base64.b64encode(data).decode()
            pages[key]={'body':body,'code':code,'title':re.search(r'<title>(.*?)</title>',html)[1],'dir':'rtl' if code=='ar' else 'ltr'}
    def initial_image(match):
        tag=match[0];src=re.search(r'src="([^"]+)"',tag)
        return tag.replace(src[0],'src="'+assets[src[1].split('/')[-1]]+'"')
    initial=re.sub(r'<img\b[^>]*>',initial_image,pages['tr']['body'])
    css=(ROOT/'assets/site.css').read_text()+'\n'+(ROOT/'assets/mobile-refinement.css').read_text()
    js='''
const pages=PAGES, assets=ASSETS;
function init(){ SITEJS }
function hydrate(){document.querySelectorAll('img').forEach(image=>{const file=image.getAttribute('src').split('/').pop();if(assets[file]){image.src=assets[file];}});}
let current='tr';
function show(key,anchor='',scroll=true){
 const page=pages[key];if(!page)return;
 document.documentElement.lang=page.code;document.documentElement.dir=page.dir;document.title=page.title;
 if(current!==key){document.body.innerHTML=page.body;current=key;hydrate();init();}
 if(anchor){requestAnimationFrame(()=>document.getElementById(anchor)?.scrollIntoView());}
 else if(scroll)window.scrollTo(0,0);
}
function route(){if(!location.hash.startsWith('#page-'))return;const [key,anchor]=location.hash.slice(6).split(':');show(key,anchor||'');}
window.addEventListener('hashchange',route);
let saved='';try{saved=localStorage.getItem('dubsee-language')||'';}catch(_){}
const supported=SUPPORTED;
const choices=saved&&supported.includes(saved)?[saved]:Array.from(navigator.languages||[navigator.language||'en']);
const preferred=choices.map(x=>x.toLowerCase().split(/[-_]/)[0]).find(x=>supported.includes(x))||'en';
hydrate();init();
if(location.hash.startsWith('#page-'))route();else show(preferred,'',false);
'''.replace('PAGES',safe_json(pages)).replace('ASSETS',safe_json(assets)).replace('SITEJS',(ROOT/'assets/site.js').read_text()).replace('SUPPORTED',safe_json(list(LOCALES)))
    template='''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>DUBSEE</title><meta name="robots" content="noindex,follow"><link rel="icon" href="ICON"><style>CSS</style></head><body>BODY<script>RUNTIME</script></body></html>'''
    result=template.replace('ICON',assets['app-icon.png']).replace('CSS',css).replace('BODY',initial).replace('RUNTIME',js)
    out=ROOT.parent/'DubSee-Preview.html';out.write_text(result)
    print(f'Compact offline preview: {len(pages)} page variants; {len(assets)} shared images; {out.stat().st_size:,} bytes')

if __name__=='__main__':main()
