import json, urllib.request, urllib.parse, time, sys
def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20) as r: return json.load(r)
        except Exception as e: time.sleep(1)
    return {}
pls = {11533942424,11622388144,10578289242,9989614662,8459098642,6850110164,9662479942,10793863422,14512684983,146820791}
for y in range(2012, 2026):
    d = get("https://api.deezer.com/search/playlist?q="+urllib.parse.quote(f"best of deutschrap {y}")+"&limit=10")
    for p in d.get('data',[]):
        if 'Deezer' in p['user']['name'] and str(y) in p['title']: pls.add(p['id']); print(y, p['id'], p['title'], file=sys.stderr)
pool = {}
for pid in pls:
    url = f"https://api.deezer.com/playlist/{pid}/tracks?limit=500"
    while url:
        d = get(url)
        for t in d.get('data',[]):
            k = t['id']
            e = pool.setdefault(k, {'id':k,'title':t['title_short'],'artist':t['artist']['name'],'rank':t['rank'],'album':t['album']['id'],'n':0})
            e['n'] += 1
        url = d.get('next')
json.dump(list(pool.values()), open('pool.json','w'), ensure_ascii=False)
print(len(pool))
