#!/usr/bin/env python3
"""Reusable SEO checks for the generated DubSee site.

Local files are always checked. Pass --live to also request the deployed URLs.

    python scripts/check_seo.py
    python scripts/check_seo.py --live

Python 3 standard library only. This does not call Search Console and does not
claim that Google has indexed anything.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, unquote
from urllib.request import Request, urlopen

from build import BASE, CONFIG, LOCALES, ROOT, STORE, url
from guides import guide_urls

SITEMAP_NS = {
    'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9',
    'x': 'http://www.w3.org/1999/xhtml',
}
HOST_ROBOTS = 'https://burakkyy.github.io/robots.txt'
APP_ADS = 'https://burakkyy.github.io/app-ads.txt'
GOOGLEBOT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
BROWSER = 'DubSeeSEOCheck/1.0'
LEGAL = ('privacy.html', 'terms.html', 'support.html')


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.parts = []
        self.skip = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag in ('script', 'style'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def fail(failures, message):
    failures.append(message)


def meta_content(page, name=None, prop=None):
    values = []
    for tag, attrs in page.tags:
        if tag != 'meta':
            continue
        if name and attrs.get('name') == name:
            values.append(attrs.get('content', ''))
        if prop and attrs.get('property') == prop:
            values.append(attrs.get('content', ''))
    return values


def links(page, rel):
    return [(attrs.get('hreflang'), attrs.get('href')) for tag, attrs in page.tags if tag == 'link' and attrs.get('rel') == rel]


def html_lang(page):
    for tag, attrs in page.tags:
        if tag == 'html':
            return attrs.get('lang'), attrs.get('dir')
    return None, None


def title_text(raw):
    match = re.search(r'<title>(.*?)</title>', raw, re.S)
    return match.group(1).strip() if match else ''


def json_ld_blocks(raw):
    return [json.loads(block) for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S)]


def local_path(address):
    relative = address.removeprefix(BASE + '/')
    path = ROOT / relative
    if path.is_dir() or address.endswith('/'):
        path = path / 'index.html'
    return path


def expected_locations():
    homes = {url(code) for code in LOCALES}
    legal = {url(code) + name for code in ('en', 'tr') for name in LEGAL}
    guides = {address for pair in guide_urls(BASE) for address in pair}
    return homes, legal, guides


def fetch(address, user_agent=BROWSER, timeout=30):
    request = Request(address, headers={'User-Agent': user_agent})
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read()
            headers = {key.lower(): value for key, value in response.headers.items()}
            return response.status, headers, body
    except HTTPError as error:
        body = error.read() if error.fp else b''
        headers = {key.lower(): value for key, value in error.headers.items()} if error.headers else {}
        return error.code, headers, body


def check_document(failures, address, raw, *, kind):
    page = Page(raw)
    lang, direction = html_lang(page)
    title = title_text(raw)
    descriptions = meta_content(page, name='description')
    canonical = [href for _, href in links(page, 'canonical')]
    alternates = {code: href for code, href in links(page, 'alternate') if code}
    if not title:
        fail(failures, f'{address}: missing title')
    if not descriptions or not descriptions[0].strip():
        fail(failures, f'{address}: missing meta description')
    if kind == 'home':
        code = 'en' if address == url('en') else address.rstrip('/').rsplit('/', 1)[-1]
        if lang != code:
            fail(failures, f'{address}: html lang is {lang}, expected {code}')
        if code == 'ar' and direction != 'rtl':
            fail(failures, f'{address}: Arabic page is not dir=rtl')
        if canonical != [address]:
            fail(failures, f'{address}: canonical {canonical} is not the page itself')
        expected = {code: url(code) for code in LOCALES}
        expected['x-default'] = BASE + '/'
        if alternates != expected:
            missing = set(expected) - set(alternates)
            extra = set(alternates) - set(expected)
            mismatch = [item for item in expected if alternates.get(item) != expected[item]]
            fail(failures, f'{address}: hreflang mismatch missing={sorted(missing)} extra={sorted(extra)} wrong={mismatch}')
        blocks = json_ld_blocks(raw)
        if len(blocks) != 1 or '@graph' not in blocks[0]:
            fail(failures, f'{address}: JSON-LD graph missing')
        else:
            types = [node.get('@type') for node in blocks[0]['@graph']]
            for required in ('Organization', 'WebSite', 'SoftwareApplication'):
                if required not in types:
                    fail(failures, f'{address}: JSON-LD missing {required}')
            if 'AggregateRating' in types or 'Review' in types:
                fail(failures, f'{address}: unexpected rating structured data')
            app = next(node for node in blocks[0]['@graph'] if node.get('@type') == 'SoftwareApplication')
            if app.get('installUrl') != STORE or app.get('downloadUrl') != STORE:
                fail(failures, f'{address}: store URL in JSON-LD is not the App Store listing')
        if STORE not in raw:
            fail(failures, f'{address}: App Store link missing')
        for name in LEGAL:
            if f'href="{name}"' not in raw:
                fail(failures, f'{address}: missing link to {name}')
        static_html = re.sub(r'<script\b[^>]*>.*?</script>', '', raw, flags=re.S | re.I)
        static_html = re.sub(r'<style\b[^>]*>.*?</style>', '', static_html, flags=re.S | re.I)
        if not re.search(r'<h1\b[^>]*>\s*\S', static_html, re.S):
            fail(failures, f'{address}: H1 is not in the HTML that a crawler reads without JavaScript')
        og = meta_content(page, prop='og:title')
        twitter = meta_content(page, name='twitter:card')
        if not og or not twitter:
            fail(failures, f'{address}: Open Graph title or Twitter card missing')
    elif kind == 'guide':
        if canonical != [address]:
            fail(failures, f'{address}: guide canonical {canonical}')
        pair = next(pair for pair in guide_urls(BASE) if address in pair)
        expected = {'en': pair[0], 'tr': pair[1], 'x-default': pair[0]}
        if alternates != expected:
            fail(failures, f'{address}: guide hreflang {alternates}')
        if lang not in ('en', 'tr'):
            fail(failures, f'{address}: guide html lang {lang}')
    elif kind == 'legal':
        source = 'tr' if '/tr/' in address else 'en'
        expected_canonical = url(source) + address.rsplit('/', 1)[-1]
        if canonical != [expected_canonical]:
            fail(failures, f'{address}: legal canonical {canonical}')
        expected = {
            'en': url('en') + address.rsplit('/', 1)[-1],
            'tr': url('tr') + address.rsplit('/', 1)[-1],
            'x-default': url('en') + address.rsplit('/', 1)[-1],
        }
        if alternates != expected:
            fail(failures, f'{address}: legal hreflang should only name the real English and Turkish documents')
    if 'location.replace' in raw:
        fail(failures, f'{address}: forced redirect script')
    for tag, attrs in page.tags:
        if tag == 'img' and 'alt' not in attrs:
            fail(failures, f'{address}: image without alt')
        for key in ('href', 'src'):
            value = attrs.get(key)
            if not value or urlsplit(value).scheme or urlsplit(value).netloc or value.startswith('#'):
                continue
            target = (local_path(address).parent / unquote(urlsplit(value).path)).resolve()
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                fail(failures, f'{address}: broken local link {value}')


def check_sitemap_tree(failures, root):
    locations = []
    for item in list(root):
        if item.tag != f'{{{SITEMAP_NS["sm"]}}}url':
            fail(failures, f'sitemap child is not url: {item.tag}')
            continue
        loc = item.find('sm:loc', SITEMAP_NS)
        text = loc.text if loc is not None else ''
        locations.append(text)
        if not text or not text.startswith(BASE + '/'):
            fail(failures, f'sitemap location outside the site: {text}')
        lastmod = item.find('sm:lastmod', SITEMAP_NS)
        if lastmod is None or not lastmod.text or len(lastmod.text) != 10:
            fail(failures, f'sitemap lastmod missing for {text}')
        if item.findall('x:link', SITEMAP_NS):
            fail(failures, f'sitemap should not repeat hreflang inside {text}')
    if len(locations) != len(set(locations)):
        fail(failures, 'sitemap contains duplicate URLs')
    homes, legal, guides = expected_locations()
    found = set(locations)
    if found != homes | legal | guides:
        fail(failures, f'sitemap URL set differs: missing={sorted((homes|legal|guides)-found)} extra={sorted(found-(homes|legal|guides))}')
    if len(locations) != 43:
        fail(failures, f'sitemap has {len(locations)} URLs, expected 43')
    if 'xmlns:xhtml' in (ROOT / 'sitemap.xml').read_text(encoding='utf-8'):
        fail(failures, 'sitemap still declares the xhtml namespace')
    return locations


def check_robots_text(failures, text, label):
    required = (
        'User-agent: OAI-SearchBot\nAllow: /',
        'User-agent: GPTBot\nDisallow: /',
        'User-agent: Googlebot\nAllow: /',
        'User-agent: Bingbot\nAllow: /',
        'User-agent: *\nAllow: /',
        f'Sitemap: {BASE}/sitemap.xml',
        f'Sitemap: {BASE}/sitemap.txt',
        f'Sitemap: {BASE}/sitemap-generated.xml',
    )
    for rule in required:
        if rule not in text:
            fail(failures, f'{label} missing rule: {rule.splitlines()[0]}')
    if 'User-agent: \\*' in text:
        fail(failures, f'{label} wildcard is escaped with a backslash')
    if b'\\*' in text.encode('utf-8'):
        fail(failures, f'{label} contains a backslash before the wildcard')


def main():
    live = '--live' in sys.argv
    failures = []
    sitemap_bytes = (ROOT / 'sitemap.xml').read_bytes()
    if sitemap_bytes.startswith(b'\xef\xbb\xbf'):
        fail(failures, 'local sitemap starts with a UTF-8 BOM')
    try:
        sitemap = ET.fromstring(sitemap_bytes)
    except ET.ParseError as error:
        fail(failures, f'local sitemap is not XML: {error}')
        sitemap = None
    if sitemap is not None:
        if sitemap.tag != f'{{{SITEMAP_NS["sm"]}}}urlset':
            fail(failures, f'sitemap root is {sitemap.tag}')
        locations = check_sitemap_tree(failures, sitemap)
    else:
        locations = []
    check_robots_text(failures, (ROOT / 'robots.txt').read_text(encoding='utf-8'), 'project robots.txt')

    homes, legal, guides = expected_locations()
    documents = [(address, 'home') for address in homes]
    documents += [(address, 'guide') for address in guides]
    documents += [(url(code) + name, 'legal') for code in LOCALES for name in LEGAL]
    for address, kind in documents:
        path = local_path(address)
        if not path.is_file():
            fail(failures, f'missing file for {address}')
            continue
        check_document(failures, address, path.read_text(encoding='utf-8'), kind=kind)

    if live:
        status, headers, body = fetch(BASE + '/sitemap.xml', GOOGLEBOT)
        content_type = headers.get('content-type', '')
        if status != 200:
            fail(failures, f'live sitemap status {status}')
        elif not content_type.startswith('application/xml') and not content_type.startswith('text/xml'):
            fail(failures, f'live sitemap content-type {content_type}')
        elif body.lstrip().startswith(b'<!') or body.lstrip().lower().startswith(b'<html'):
            fail(failures, 'live sitemap response is HTML')
        else:
            try:
                live_root = ET.fromstring(body)
            except ET.ParseError as error:
                fail(failures, f'live sitemap is not XML for Googlebot: {error}')
            else:
                check_sitemap_tree(failures, live_root)
        for address in locations:
            status, headers, body = fetch(address)
            if status != 200:
                fail(failures, f'live {address} status {status}')
                continue
            if b'<html' not in body.lower():
                fail(failures, f'live {address} is not HTML')
                continue
            kind = 'home' if address in homes else 'guide' if address in guides else 'legal'
            check_document(failures, address, body.decode('utf-8'), kind=kind)
        status, headers, body = fetch(HOST_ROBOTS, GOOGLEBOT)
        if status != 200:
            fail(failures, f'host robots.txt status {status}')
        else:
            text = body.decode('utf-8')
            check_robots_text(failures, text, 'host robots.txt')
            wildcard = 'User-agent: *'.encode('utf-8')
            if wildcard not in body:
                fail(failures, 'host robots.txt wildcard line is not the raw asterisk byte')
        status, _, ads = fetch(APP_ADS)
        if status != 200 or b'google.com, pub-' not in ads:
            fail(failures, f'app-ads.txt was not left intact (status {status})')
        for probe in (BASE + '/no-such-page-seo-check', BASE + '/missing/'):
            status, _, _ = fetch(probe)
            if status != 404:
                fail(failures, f'expected 404 for {probe}, got {status}')

    if failures:
        print('\n'.join(failures))
        print(f'FAIL: {len(failures)} SEO check(s)')
        return 1
    scope = 'local files and live URLs' if live else 'local files'
    print(f'PASS: {scope}; {len(LOCALES)} language homepages; sitemap locations {len(locations)}; robots groups checked.')
    if not live:
        print('Live HTTP status was not requested. Run with --live to check the deployed site.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (URLError, TimeoutError) as error:
        print(f'FAIL: network error {error}')
        raise SystemExit(1)
