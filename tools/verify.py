"""Prüft jeden Song einer Kategorie auf Deezer: Ausschnitt vorhanden, richtiger Interpret,
keine Remix/Live/Cover-Version, Dauer > 90 s (30 s = Snippet).

Aufruf: python3 verify.py <id> [<id> ...]
"""
import json, os, re, sys, time, unicodedata, urllib.request

DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
BAD = re.compile(r'remix|\blive\b|cover|karaoke|instrumental|sped up|acoustic|taylor.s version', re.I)


def get(url):
    for _ in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Shitster/0.2'}), timeout=20) as r:
                d = json.load(r)
            if 'error' not in d:
                return d
        except Exception:
            pass
        time.sleep(2)
    return {}


def norm(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s.lower()))


for cid in sys.argv[1:]:
    songs = json.load(open(os.path.join(DATA, f'{cid}.json'), encoding='utf-8'))['songs']
    probs = 0
    for s in songs:
        t = get(f"https://api.deezer.com/track/{s['id']}")
        if not t:
            probs += 1
            print('  NICHT ERREICHBAR', s)
            continue
        first = re.split(r' feat\. | & |, ', s['artist'])[0]
        names = [t['artist']['name']] + [c['name'] for c in t.get('contributors', [])]
        art_ok = any(norm(first) in norm(n) or norm(n) in norm(first) for n in names)
        if not t.get('preview') or not art_ok or BAD.search(t['title']) or t.get('duration', 0) < 90:
            probs += 1
            print(f"  {s['year']} {s['artist']} - {s['title']} | Deezer: {t['artist']['name']} - {t['title']} | "
                  f"preview {bool(t.get('preview'))} dur {t.get('duration')}")
        time.sleep(0.1)
    print(f'{cid}: {len(songs)} geprüft, {probs} Probleme')
