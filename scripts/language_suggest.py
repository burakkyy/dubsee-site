"""Language suggestion rules mirrored by assets/site.js window.dubseeSuggest."""

def suggest(page, languages, saved, dismissed, search, supported):
    if 'lang' in _query(search):
        return ''
    browser = 'en'
    for tag in languages or ['en']:
        code = str(tag or '').lower().replace('_', '-').split('-')[0]
        if code in supported:
            browser = code
            break
    preferred = saved if saved in supported else browser
    if not preferred or preferred == page or dismissed == preferred:
        return ''
    return preferred

def _query(search):
    text = search[1:] if str(search).startswith('?') else str(search or '')
    found = set()
    for part in text.split('&'):
        if not part:
            continue
        key = part.split('=', 1)[0]
        if key:
            found.add(key)
    return found
