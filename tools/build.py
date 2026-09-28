import json, re
res = {f"{e['artist']}|{e['title']}": e for e in json.load(open('resolved.json'))}
# Geprüfte Originaljahre (Deezer/MusicBrainz abgeglichen). None = raus (unsicherer Treffer).
YEAR = {
 'Fler|NDW 2005':2005,'Azad|Prison Break Anthem':2007,'K.I.Z|Walpurgisnacht':2007,'Kollegah|Mondfinsternis':None,
 'Kollegah|Du bist Boss':2014,'Bushido|Zeiten ändern dich':2010,'Haftbefehl|Azzlack Stereotyp':2010,
 'Kollegah|Jung Brutal Gutaussehend':None,'Kool Savas|Aura':2011,'Haftbefehl|Chabos wissen wer der Babo ist':2012,
 'Kollegah|Sturmmaske auf':None,'Bushido|Stress ohne Grund':2013,'SSIO|Nullkommaneun':2016,'SSIO|Nuttööö':2013,
 'Haftbefehl|Ihr Hurensöhne':2014,'Kontra K|Wölfe':2014,'Kollegah|King':None,'Kollegah|Mittelfinger hoch':2009,
 'Haftbefehl|069':2015,'Haftbefehl|Saudi Arabi Money Rich':2014,'Haftbefehl|Russisch Roulette':2014,'Shindy|Nautilus':2019,
 'Shindy|JFK':2014,"Genetikk|Lieb's oder lass es":2013,'AK Ausserkontrolle|Echte Berliner':2016,'Gzuz|Ebbe & Flut':2015,
 'Haftbefehl|Ich rolle mit meim Besten':2014,"Haftbefehl|Lass die Affen aus'm Zoo":2014,'K.I.Z|Hurra die Welt geht unter':2015,
 'Kontra K|Erfolg ist kein Glück':2015,'Xatar|Iz da':2015,'Celo & Abdi|Besuchstag':2012,'Bonez MC|Ohne mein Team':2016,
 'Bonez MC|Palmen aus Plastik':2016,'Kollegah|Alpha':None,'Olexesh|Magisch':2018,'Luciano|Jäger':2017,'Sun Diego|Eloah':2018,
 'Nimo|Heute mit mir':2017,'187 Strassenbande|Millionär':2017,'Summer Cem|Tamam Tamam':2018,'Capo|Alles auf Rot':2017,
 'Ufo361|Für die Gang':2017,'Ufo361|Emotions':2020,'RIN|Keine Liebe':2019,'Luciano|Meer':2018,'Veysel|Habibo':2018,
 'Azet|Fast Life':2016,'Gringo|Pink Panther':None,'Capital Bra|Neymar':2018,'Capital Bra|Berlin lebt':2018,'Capital Bra|Benzema':2018,
 'Bonez MC|Kokain':2018,'Bonez MC|500 PS':2018,'Mero|Baller los':2018,'Mero|Hobby Hobby':2019,'Eno|Mercedes':2018,
 'Loredana|Sonnenbrille':2018,'Summer Cem|Casanova':2018,'Xatar|Ich will alles':2008,'Kalazh44|Royal Rumble':2019,
 'Capital Bra|Tilidin':2019,'Samra|Wieder Lila':2019,'Samra|Cataleya':2018,'Capital Bra|110':2019,'Capital Bra|Cherry Lady':2019,
 'Shindy|DODI':2019,"Shindy|What's Luv":2020,'Apache 207|Roller':2019,'Apache 207|200 km/h':2019,'Luciano|La Haine':None,
 'Dardan|gENAuSo':2019,'Lucio101|6 Nullen':2019,'Fero47|NENENE':2019,'Pashanim|Airwaves':2020,'187 Strassenbande|Extasy':2021,
 'Luciano|SUVs':2021,'Azet|Fast Life 2':2020,'Gzuz|Wenn ich will':None,'Kontra K|Dreckig & Gemein':2025,'Bonez MC|Roadrunner':2020,
 'Pashanim|Sommergewitter':2021,'Pashanim|Kleiner Prinz':2022,'Luciano|Bamba':2023,'RIN|1994':None,'Farid Bang|BERETTA':2022,
 'Symba|Angels Sippen':None,'Nizi19|2wasser2sprite':2022,'Bonez MC|Taxi':2022,'Gzuz|Alles Black':None,
 'Pashanim|Shabab(e)s im VIP':2025,'Sira|9 bis 9':2023,'Kalazh44|Lichtblick':2024,'Kärdo|RACHE':2023,'Summer Cem|KILLY MANJARO':2026,
 'Pashanim|Mittelmeer':2024,'Olexesh|Bandog 2':2024,'Amo|Amo aller Amos':2024,'Sosa La M|Butcher':2024,'LACAZETTE|H&K':2024,
 'Ion Miles|iPhone 5s':2025,'Azet|Buscape':2025,'Dardan|Pablo':2024,'SSIO|Alles oder Nix':None,'Rap La Rue|Lamine Yamal':2024,
 'LACAZETTE|CDY':2026,'LACAZETTE|LID':2024,'AK Ausserkontrolle|Hin und Her':2026,'AK Ausserkontrolle|BLN':2026,'Yc|Xalaz':2026,
 "Summer Cem|MO' MONEY MO' HATERS":2026,'THIZZY52|BLOCKKIDS':2026,'THIZZY52|BALOTELLI':2026,'Capital Bra|Ghetto Superstars':2026,
 'Capital Bra|Sonne über Berlin':2026,'Olexesh|5 SKARABÄEN':2026,'Farid Bang|Requiem':2026,'SASHKO BRATE|Dejavu':2026,
 'Pajel|Blocckind':2023,'Luciano|THUG LIFE':2026,'Luciano|Pole Position':2025,'Kool Savas|AMG':2020,'Haftbefehl|Golden Brown':2015,
 'Kollegah|Pusher':None,'Sido|Masafaka':2016,'Bushido|Sonny Black':None,'KC Rebell|Mogli':2022,'RAF Camora|Blaues Licht':2021,
 'Pashanim|Prada Sport':2026,'Hanybal|Baller los':None,
}
EXTRA = [  # (deezer id, artist, title, year) – einzeln geprüft
 (1728324707,'Massiv','Wenn der Mond in mein Ghetto kracht',2006),(3802719952,'Sido','Strassenjunge',2006),
 (3786047722,'Sido','Mein Block',2004),(955106,'Bushido','Sonnenbank Flavour',2004),(356779151,'KC Rebell','Murcielago',2017),
 (120466438,'UFO361','Ich bin ein Berliner',2016),(709627962,'Samra','Zombie',2019),(138394773,'Bonez MC & RAF Camora','Mörder',2016),
 (761796682,'Gringo','Pink Panther',2019),(907183842,'Symba','Angels Sippen',2020),(685839992,'Luciano','La Haine',2019),
 (521607822,'Luciano','Ballin',2018),(142307035,'AK Ausserkontrolle','Kristall',2017),(82112822,'Haftbefehl','Crackküchenmukke',2012),
]
def clean(t):
    feat = re.search(r'\((?:feat\.|ft\.|with|mit) ([^)]*)\)', t, re.I)
    t = re.sub(r'\s*\((?:feat\.|ft\.|with|mit)[^)]*\)', '', t, flags=re.I)
    t = re.sub(r'\s*(Remastered|\(Single Version\)|\(Intro\))\s*$', '', t).strip()
    return t, (feat.group(1) if feat else None)
songs, seen = [], set()
for key, e in res.items():
    if key not in YEAR: print('UNREVIEWED', key); continue
    y = YEAR[key]
    if not y: continue
    title, feat = clean(e['dzTitle'])
    artist = e['dzArtist'] + (f' feat. {feat}' if feat else '')
    if key == 'Bushido|Stress ohne Grund': artist = 'Shindy feat. Bushido'
    if key == 'Azad|Prison Break Anthem': title = 'Prison Break Anthem (Ich glaub an Dich)'
    songs.append({'id': e['id'], 'artist': artist, 'title': title, 'year': y})
for i, a, t, y in EXTRA: songs.append({'id': i, 'artist': a, 'title': t, 'year': y})
songs = [s for s in songs if not (s['id'] in seen or seen.add(s['id']))]
songs.sort(key=lambda s: (s['year'], s['artist']))
cat = {'id': 'deutschrap', 'name': 'Deutschrap', 'description': 'Straße, Gangsta-Rap & Klassiker – Schwerpunkt 2013 bis heute.', 'songs': songs}
json.dump(cat, open('../data/deutschrap.json', 'w'), ensure_ascii=False, indent=1)
years = [s['year'] for s in songs]
idx = [{'id': 'deutschrap', 'name': 'Deutschrap', 'description': cat['description'], 'file': 'deutschrap.json', 'icon': 'mic',
        'colors': ['#ff375f', '#5e5ce6'], 'count': len(songs), 'from': min(years), 'to': max(years)}]
json.dump(idx, open('../data/categories.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(songs), 'Songs'); print(sorted(Counter(years).items()))
print('ab 2013:', sum(y >= 2013 for y in years))
