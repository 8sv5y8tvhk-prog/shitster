import json, urllib.request, urllib.parse, sys, time
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Shitster/0.1'}), timeout=20) as r: return json.load(r)
for q in sys.argv[1:]:
    if q.startswith('id:'):
        t = get('https://api.deezer.com/track/'+q[3:]); a = get('https://api.deezer.com/album/%d' % t['album']['id'])
        print('ID', q[3:], t['artist']['name'], '-', t['title'], '|', a['release_date'], a['title']); continue
    d = get('https://api.deezer.com/search?limit=6&q='+urllib.parse.quote(q))
    print('==', q)
    for t in d.get('data', [])[:4]:
        a = get('https://api.deezer.com/album/%d' % t['album']['id'])
        print('  ', t['id'], t['rank']//1000, t['artist']['name'], '-', t['title'], '|', a.get('release_date'), a.get('title'))
