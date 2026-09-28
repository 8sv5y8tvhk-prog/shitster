"""Gemeinsamer Baukasten für Kategorie-Builds (build_<id>.py).

Jahresregel: Jahr der ERSTEN Veröffentlichung der gespielten Aufnahme (Album oder Single),
nie Remaster, Neuauflage oder Compilation. None im YEAR-Dict = bewusst nicht aufgenommen.
Danach immer: python3 fix_artists.py <id> && python3 make_index.py
"""
import json, os
from collections import Counter

HERE = os.path.dirname(__file__)


def build(cid, name, description, year, id_fix=None, extra=None, artist=None, title=None):
    id_fix, extra, artist, title = id_fix or {}, extra or [], artist or {}, title or {}
    res = {f"{e['artist']}|{e['title']}": e for e in json.load(open(os.path.join(HERE, f'resolved-{cid}.json'), encoding='utf-8'))}
    songs, missing = [], []
    for key, y in year.items():
        if not y:
            continue
        e = res.get(key)
        if not e and key not in id_fix:
            missing.append(key)
            continue
        a, t = key.split('|')
        songs.append({'id': id_fix.get(key) or e['id'], 'artist': artist.get(key, a), 'title': title.get(key, t), 'year': y})
    for i, a, t, y in extra:
        songs.append({'id': i, 'artist': a, 'title': t, 'year': y})
    seen = set()
    songs = [s for s in songs if not (s['id'] in seen or seen.add(s['id']))]
    songs.sort(key=lambda s: (s['year'], s['artist']))
    cat = {'id': cid, 'name': name, 'description': description, 'songs': songs}
    json.dump(cat, open(os.path.join(HERE, '..', 'data', f'{cid}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    unreviewed = [k for k in res if k not in year]
    dec = Counter(f"{s['year'] // 10 * 10}er" for s in songs)
    print(f'{name}: {len(songs)} Songs | Jahrzehnte: {sorted(dec.items())}')
    if missing or unreviewed:
        print('  fehlt:', missing, '| nicht geprüft:', unreviewed)
    return songs
