import json, urllib.request, urllib.parse, time, re, unicodedata
UA = {'User-Agent': 'Shitster/0.1 (private music quiz)'}
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r: return json.load(r)
        except Exception as e: time.sleep(1.5)
    return {}
def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    s = re.sub(r'\(.*?\)|\[.*?\]|feat\..*', '', s)
    return re.sub(r'[^a-z0-9]', '', s)
out = []
for line in open('songs.txt'):
    artist, title = line.strip().split('|')
    d = get("https://api.deezer.com/search?limit=50&q=" + urllib.parse.quote(f'artist:"{artist}" track:"{title}"'))
    hits = [t for t in d.get('data', []) if norm(title) in norm(t['title']) or norm(t['title_short']) == norm(title)]
    if not hits:
        d = get("https://api.deezer.com/search?limit=50&q=" + urllib.parse.quote(f'{artist} {title}'))
        hits = [t for t in d.get('data', []) if norm(title) in norm(t['title'])]
    if not hits:
        print('MISSING', artist, title); continue
    hits = [t for t in hits if 'remix' not in t['title'].lower() and 'live' not in t['title'].lower() and 'instrumental' not in t['title'].lower()] or hits
    best = max(hits, key=lambda t: t['rank'])
    # earliest deezer album date among matching versions
    dz = []
    for t in hits[:12]:
        a = get(f"https://api.deezer.com/album/{t['album']['id']}")
        if a.get('release_date'): dz.append(a['release_date'])
    mb = get("https://musicbrainz.org/ws/2/recording?fmt=json&limit=25&query=" + urllib.parse.quote(f'recording:"{title}" AND artist:"{artist}"'))
    time.sleep(1.1)
    mbd = [r.get('first-release-date') for r in mb.get('recordings', []) if r.get('score', 0) >= 90 and r.get('first-release-date')]
    e = {'artist': artist, 'title': title, 'id': best['id'], 'dzTitle': best['title'], 'dzArtist': best['artist']['name'],
         'rank': best['rank'], 'dzMin': min(dz) if dz else None, 'mbMin': min(mbd) if mbd else None}
    print(e['dzMin'], e['mbMin'], artist, '-', title, '|', e['dzArtist'], '-', e['dzTitle'], e['rank']//1000, flush=True)
    out.append(e)
json.dump(out, open('resolved.json', 'w'), ensure_ascii=False, indent=1)
