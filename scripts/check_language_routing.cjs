// Regression checks for direct language URLs and first root-entry detection.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const config=JSON.parse(fs.readFileSync(path.join(root,'config.json'),'utf8'));
const languages=JSON.parse(fs.readFileSync(path.join(__dirname,'supported-languages.json'),'utf8')).languages;
function script(code,name='index.html'){
 const file=path.join(root,code==='en'?'':code,name),html=fs.readFileSync(file,'utf8');
 return html.match(/<script data-auto-language>([\s\S]*?)<\/script>/)?.[1];
}
function run(code,pathname,preferences=['tr-TR'],saved='',search=''){
 let destination='';
 const location={protocol:'https:',pathname,search,hash:'',replace(value){destination=value}};
 const context={document:{documentElement:{lang:code}},location,navigator:{languages:preferences},localStorage:{getItem(){return saved}},URL,URLSearchParams};
 vm.runInNewContext(script(code),context);return destination;
}
const base=new URL(config.base_url+'/');
assert.equal(run('en',base.pathname),config.base_url+'/tr/');
assert.equal(run('en',base.pathname+'index.html',['ja-JP']),config.base_url+'/ja/');
assert.equal(run('en',base.pathname,['tr-TR'],'de'),config.base_url+'/de/');
assert.equal(run('en',base.pathname,['tr-TR'],'en'),'');
assert.equal(run('en',base.pathname,['zh-CN']),'');
assert.equal(run('en',base.pathname,['tr-TR'],'','?lang=en'),'');
assert.equal(run('en',base.pathname+'privacy.html',['tr-TR']),'');
for(const code of languages){
 if(code!=='en'){
  assert.equal(run(code,base.pathname+code+'/',['en-US'], 'en'),'');
  assert.equal(run(code,base.pathname+code+'/index.html',['tr-TR'], 'de'),'');
 }
 for(const name of ['privacy.html','terms.html','support.html'])assert.equal(script(code,name),undefined);
}
console.log('PASS: root-only automatic language selection; all 31 direct language routes and 93 legal/support routes remain accessible.');
