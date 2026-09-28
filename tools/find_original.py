"""Sucht die Originalversion eines Songs in den Top-Songs des Künstlers (die normale Suche liefert oft Remixe/Cover).

Aufruf: python3 find_original.py "Interpret|Titel" "Interpret|Titel" ...
Ausgabe je Song: Kandidaten mit ID, Rang, Dauer, Album und Album-Datum – die beste saubere Version zuerst.
"""
import json, re, sys, time, unicodedata, urllib.parse, urllib.request

UA = {'User-Agent': 'Shitster/0.2 (private music quiz)'}
BAD = re.compile(r"remix|live|instrumental|karaoke|acoustic|sped up|slowed|cover|mashup|re-?record|version\)|mix\)|edit\)|demo|\b20\d\d\b(?! remaster)", re.I)


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
    s = unicodedata.normalize('NFKD', s.lower())
    s = re.sub(r'\(.*?\)|\[.*?\]', '', s)
    return re.sub(r'[^a-z0-9]', '', s)


def candidates(artist, title):
    arts = get('https://api.deezer.com/search/artist?q=' + urllib.parse.quote(artist)).get('data', [])
    art = next((a for a in arts if norm(a['name']) == norm(artist)), arts[0] if arts else None)
    found = []
    if art:
        for t in get(f"https://api.deezer.com/artist/{art['id']}/top?limit=100").get('data', []):
            if norm(title) in norm(t['title']) or norm(t['title']) in norm(title):
                found.append(t)
    q = get('https://api.deezer.com/search?limit=50&q=' + urllib.parse.quote(f'artist:"{artist}" track:"{title}"')).get('data', [])
    found += [t for t in q if (norm(title) in norm(t['title'])) and norm(artist) in norm(t['artist']['name'])]
    uniq = {t['id']: t for t in found}.values()
    return sorted(uniq, key=lambda t: (bool(BAD.search(t['title'])), t.get('duration', 0) < 90, -t['rank']))


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        artist, title = arg.split('|')
        print('==', artist, '-', title)
        for t in candidates(artist, title)[:5]:
            al = get(f"https://api.deezer.com/album/{t['album']['id']}")
            flag = ' (!)' if BAD.search(t['title']) else ''
            print(f"   {t['id']} rank {t['rank'] // 1000} dur {t.get('duration')} | {t['artist']['name']} - {t['title']}{flag} | {al.get('release_date')} {al.get('title')}")
