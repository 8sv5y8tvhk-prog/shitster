"""Löst eine Songliste (Zeilen „Interpret|Titel“) über Deezer auf und sammelt Jahreshinweise.

Aufruf: python3 resolve.py <songs.txt> <resolved.json>

Für jeden Song:
- beste Deezer-Version (höchster Rang, passender Interpret, keine Remixe/Live/Cover/Neuaufnahmen)
- dzMin: frühestes Album-Datum aller passenden Deezer-Versionen
- mbMin: frühestes „first-release-date“ laut MusicBrainz
Die endgültigen Jahre werden danach in build.py von Hand geprüft.
"""
import json, re, sys, time, unicodedata, urllib.parse, urllib.request

UA = {'User-Agent': 'Shitster/0.2 (private music quiz)'}
BAD = re.compile(r"remix|live|instrumental|karaoke|acoustic|sped up|slowed|taylor.s version|re-?record|cover|edit\)|version\)|mix\)|demo", re.I)


def get(url):
    for _ in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
                return json.load(r)
        except Exception:
            time.sleep(1.5)
    return {}


def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    s = re.sub(r'\(.*?\)|\[.*?\]|feat\..*|ft\..*', '', s)
    return re.sub(r'[^a-z0-9]', '', s)


def raw(s):
    # wie norm, aber Klammer-Inhalte bleiben erhalten (für gezielte Remix-Suche)
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s.lower()))


def artist_ok(want, got):
    w, g = norm(want), norm(got)
    return w in g or g in w


def main(src, dst):
    out = []
    for line in open(src, encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        artist, title = line.split('|')
        base = re.sub(r'\s*\([^)]*remix[^)]*\)', '', title, flags=re.I)
        d = get("https://api.deezer.com/search?limit=50&q=" + urllib.parse.quote(f'artist:"{artist}" track:"{base}"'))
        hits = [t for t in d.get('data', []) if norm(title) in norm(t['title']) and artist_ok(artist, t['artist']['name'])]
        if not hits:
            d = get("https://api.deezer.com/search?limit=50&q=" + urllib.parse.quote(f'{artist} {title.replace("(", "").replace(")", "")}'))
            hits = [t for t in d.get('data', []) if norm(title) in norm(t['title']) and artist_ok(artist, t['artist']['name'])]
        if not hits:
            print('MISSING', artist, '-', title, flush=True)
            continue
        remix = re.search(r'\(([^)]*remix[^)]*)\)', title, re.I)
        if remix:
            # Gewünschter Remix steht in der Liste → genau diese Version, Remixe nicht aussortieren
            clean = [t for t in hits if raw(remix.group(1)) in raw(t['title'] + (t.get('title_version') or ''))]
        else:
            clean = [t for t in hits if not BAD.search(t['title']) and not BAD.search(t.get('title_version') or '')]
        best = max(clean or hits, key=lambda t: t['rank'])
        dz = []
        for t in (clean or hits)[:10]:
            a = get(f"https://api.deezer.com/album/{t['album']['id']}")
            if a.get('release_date'):
                dz.append(a['release_date'])
        mb = get("https://musicbrainz.org/ws/2/recording?fmt=json&limit=25&query=" + urllib.parse.quote(f'recording:"{title}" AND artist:"{artist}"'))
        time.sleep(1.1)
        mbd = [r.get('first-release-date') for r in mb.get('recordings', []) if r.get('score', 0) >= 90 and r.get('first-release-date')]
        e = {'artist': artist, 'title': title, 'id': best['id'], 'dzTitle': best['title'], 'dzArtist': best['artist']['name'],
             'rank': best['rank'], 'dzMin': min(dz) if dz else None, 'mbMin': min(mbd) if mbd else None, 'dirty': not clean}
        print(e['dzMin'], e['mbMin'], artist, '-', title, '|', e['dzArtist'], '-', e['dzTitle'], e['rank'] // 1000, '(!)' if e['dirty'] else '', flush=True)
        out.append(e)
    json.dump(out, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main(*(sys.argv[1:3] if len(sys.argv) >= 3 else ('songs.txt', 'resolved.json')))
