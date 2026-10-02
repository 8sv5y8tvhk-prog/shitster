"""Baut data/categories.json aus allen Kategorie-Dateien in data/.

Aufruf: python3 make_index.py
Reihenfolge und Aussehen der Kategorien stehen in META.
"""
import json, os

DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
META = {
    'deutschrap': {'icon': 'mic', 'colors': ['#ff375f', '#5e5ce6']},
    'whitegirl': {'icon': 'heart', 'colors': ['#ff6fb5', '#a855f7']},
    'dekaden': {'icon': 'cassette', 'colors': ['#40c8e0', '#5e5ce6']},
    'rock': {'icon': 'flame', 'colors': ['#ff453a', '#3a0a0a']},
    'edm': {'icon': 'eq', 'colors': ['#00d4ff', '#bf5af2']},
    'serien': {'icon': 'tv', 'colors': ['#ffd60a', '#ff6b35']},
}

index = []
for cid, meta in META.items():
    path = os.path.join(DATA, f'{cid}.json')
    if not os.path.exists(path):
        continue
    cat = json.load(open(path, encoding='utf-8'))
    years = [s['year'] for s in cat['songs']]
    index.append({'id': cid, 'name': cat['name'], 'description': cat['description'], 'file': f'{cid}.json',
                  'icon': meta['icon'], 'colors': meta['colors'], 'count': len(years), 'from': min(years), 'to': max(years)})
json.dump(index, open(os.path.join(DATA, 'categories.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for c in index:
    print(f"{c['name']}: {c['count']} Songs, {c['from']}–{c['to']}")
