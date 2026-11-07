"""Direct language URLs stay put. Browser language only suggests a link."""
import json
from pathlib import Path
from language_suggest import suggest

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
supported = json.loads((ROOT / 'scripts' / 'supported-languages.json').read_text(encoding='utf-8'))['languages']
base = config['base_url'].rstrip('/') + '/'

def page(code, name='index.html'):
    return (ROOT / name).read_text(encoding='utf-8') if code == 'en' else (ROOT / code / name).read_text(encoding='utf-8')

site_js = (ROOT / 'assets' / 'site.js').read_text(encoding='utf-8')
assert 'location.replace' not in site_js
assert 'function (page, languages, saved, dismissed, search, supported)' in site_js or 'window.dubseeSuggest = function' in site_js
assert 'dubsee-suggest-dismissed' in site_js
assert 'navigator.languages' in site_js

for code in supported:
    html = page(code)
    assert 'location.replace' not in html
    assert 'data-auto-language' not in html
    for name in ('privacy.html', 'terms.html', 'support.html'):
        legal = page(code, name)
        assert 'location.replace' not in legal
        assert f'href="{name}"' in legal or 'support.html' in legal

assert suggest('en', ['tr-TR'], '', '', '', supported) == 'tr'
assert suggest('en', ['ja-JP'], '', '', '', supported) == 'ja'
assert suggest('en', ['tr-TR'], 'de', '', '', supported) == 'de'
assert suggest('en', ['tr-TR'], 'en', '', '', supported) == ''
assert suggest('en', ['zh-CN'], '', '', '', supported) == ''
assert suggest('en', ['tr-TR'], '', '', '?lang=en', supported) == ''
assert suggest('tr', ['en-US'], '', '', '', supported) == 'en'
assert suggest('de', ['tr-TR'], '', 'tr', '', supported) == ''
assert suggest('de', ['tr-TR'], 'de', '', '', supported) == ''
assert suggest('tr', ['de-DE'], 'de', '', '', supported) == 'de'
assert base.startswith('https://')
print('PASS: browser language suggests a link; direct language, legal, and support URLs are not redirected.')
