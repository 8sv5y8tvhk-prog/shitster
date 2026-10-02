"""Sucht für jede Serie/jeden Film in serien_entries.py die beste Deezer-Version.

Aufruf: python3 search_serien.py  →  resolved-serien.json + Log mit Vorschlag (★) und Alternativen.
Cover-Bands, Karaoke, Spieluhr- und 8-Bit-Versionen werden aussortiert.
"""
import json, re, time, unicodedata, urllib.parse, urllib.request
from serien_entries import ENTRIES

UA = {'User-Agent': 'Shitster/0.2 (private music quiz)'}
JUNK = re.compile(r'karaoke|cover|tribute|made famous|originally performed|in the style|8-bit|8 bit|lullaby|music box|spieluhr|piano version|'
                  r'kinderlied|remix|workout|sped up|slowed|tv theme band|theme players|tv sounds|the tv|soundtrack wonder|movie sounds', re.I)


def get(url):
    for _ in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
                d = json.load(r)
            if 'error' not in d:
                return d
        except Exception:
            pass
        time.sleep(2)
    return {}


def norm(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s.lower()))


out = []
for show, year, query, hint in ENTRIES:
    data = get('https://api.deezer.com/search?limit=25&q=' + urllib.parse.quote(query)).get('data', [])
    clean = [t for t in data if not JUNK.search(t['title'] + ' ' + t['artist']['name'] + ' ' + t['album']['title'])]
    hinted = [t for t in clean if hint and norm(hint) in norm(t['artist']['name'] + ' ' + t['title'])]
    pick = max(hinted or clean or data, key=lambda t: t['rank']) if data else None
    print(f'== {show} ({year}) | Suche: {query}')
    for t in sorted(data, key=lambda t: -t['rank'])[:6]:
        mark = '★' if pick and t['id'] == pick['id'] else ('✗' if t not in clean else ' ')
        print(f"  {mark} {t['id']} r{t['rank'] // 1000} {t['duration']}s | {t['artist']['name']} - {t['title']} | {t['album']['title']}")
    if pick:
        out.append({'show': show, 'year': year, 'query': query, 'id': pick['id'], 'artist': pick['artist']['name'],
                    'title': pick['title'], 'rank': pick['rank'], 'hinted': bool(hinted)})
    else:
        print('  MISSING')
    time.sleep(0.15)
json.dump(out, open('resolved-serien.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('fertig:', len(out), 'von', len(ENTRIES))
