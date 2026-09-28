"""Setzt die Interpreten-Anzeige aller Kategorien aus Deezers Mitwirkenden-Liste (Main + Featured).

Aufruf: python3 fix_artists.py            (alle Kategorien in data/)
        python3 fix_artists.py whitegirl  (nur eine Kategorie)

Format: „Haupt1 & Haupt2 feat. Gast1, Gast2 & Gast3“.
Steht schon eine vollständige Schreibweise in der Datei (alle Deezer-Namen enthalten), bleibt sie unverändert –
so bleiben bekannte Schreibweisen wie „Rihanna feat. Calvin Harris“ erhalten.
Nach jedem Neubau einer Kategorie (build_<id>.py) erneut ausführen.
"""
import json, os, re, sys, time, unicodedata, urllib.request

DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
UA = {'User-Agent': 'Shitster/0.2 (private music quiz)'}
# Deezer listet bei manchen Bands die Mitglieder/Produzenten als Haupt-Interpreten → ausblenden
BAND_MEMBERS = {'Eurythmics': {'Annie Lennox', 'Dave Stewart'}, 'Gnarls Barkley': {'CeeLo Green', 'Danger Mouse'},
                'Gala': {'Molella', 'Phil Jay'}}
# Einheitliche Schreibweisen (Deezer ist nicht konsistent)
NAME_FIX = {'JAY Z': 'JAY-Z', 'JAŸ-Z': 'JAY-Z', 'Charli xcx': 'Charli XCX', 'Charli Xcx': 'Charli XCX', 'ZEDD': 'Zedd', 'Volo': 'VOLO'}


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


def join(names):
    return names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' & ' + names[-1]


def unique(names):
    seen, out = set(), []
    for n in names:
        if norm(n) not in seen:
            seen.add(norm(n))
            out.append(n)
    return out


def artist_line(track):
    contrib = track.get('contributors') or []
    main = unique([NAME_FIX.get(c['name'], c['name']) for c in contrib if c.get('role') == 'Main'])
    feat = unique([NAME_FIX.get(c['name'], c['name']) for c in contrib if c.get('role') == 'Featured'])
    for band, members in BAND_MEMBERS.items():
        if band in main:
            main = [m for m in main if m not in members]
    # Wer als Gast geführt wird, ist kein Haupt-Interpret (Deezer listet manche doppelt)
    main = [m for m in main if norm(m) not in {norm(f) for f in feat}] or main[:1]
    if not main:
        main = [NAME_FIX.get(track['artist']['name'], track['artist']['name'])]
    return join(main) + (' feat. ' + join(feat) if feat else ''), main + feat


def main(only=None):
    changed = 0
    for fn in sorted(os.listdir(DATA)):
        cid = fn[:-5]
        if not fn.endswith('.json') or fn == 'categories.json' or (only and cid != only):
            continue
        path = os.path.join(DATA, fn)
        cat = json.load(open(path, encoding='utf-8'))
        for s in cat['songs']:
            t = get(f"https://api.deezer.com/track/{s['id']}")
            if not t:
                print('  FEHLER', s['id'], s['artist'], '-', s['title'])
                continue
            line, names = artist_line(t)
            cur = norm(s['artist'])
            if all(norm(n) in cur for n in names):
                continue  # vorhandene Schreibweise ist vollständig
            print(f"  {cid}: {s['artist']}  →  {line}   ({s['title']})")
            s['artist'] = line
            changed += 1
            time.sleep(0.1)
        json.dump(cat, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Geändert:', changed)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
