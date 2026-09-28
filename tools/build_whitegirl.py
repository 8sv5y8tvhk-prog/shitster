"""Baut data/whitegirl.json aus resolved-whitegirl.json mit von Hand geprüften Jahren.

Regel: Jahr der ERSTEN Veröffentlichung (Album oder Single, was zuerst kam), nie Remaster,
Neuauflagen, Compilations oder „Taylor's Version“.
None = bewusst nicht aufgenommen (zu wenig Banger, Doppelung oder keine saubere Version auf Deezer).
"""
import json, re
from collections import Counter

res = {f"{e['artist']}|{e['title']}": e for e in json.load(open('resolved-whitegirl.json', encoding='utf-8'))}

YEAR = {
 # Kult-Klassiker
 'Spice Girls|Wannabe': 1996, 'Britney Spears|...Baby One More Time': 1998, 'Christina Aguilera|Genie in a Bottle': 1999,
 'Backstreet Boys|I Want It That Way': 1999,
 # 2000–2004
 'Britney Spears|Oops!...I Did It Again': 2000, 'Britney Spears|Toxic': 2003, 'Christina Aguilera|Dirrty': 2002,
 "Destiny's Child|Survivor": 2001, "Destiny's Child|Bootylicious": 2001, 'Beyoncé|Crazy in Love': 2003,
 "Kylie Minogue|Can't Get You out of My Head": 2001, 'Shakira|Whenever, Wherever': 2001, 'Avril Lavigne|Complicated': 2002,
 'Avril Lavigne|Sk8er Boi': 2002, 'Vanessa Carlton|A Thousand Miles': 2002, "Nelly Furtado|I'm Like a Bird": 2000,
 'P!nk|Get the Party Started': 2001, 'Jennifer Lopez|Jenny from the Block': None, 'Kelly Clarkson|Since U Been Gone': 2004,
 'Hilary Duff|So Yesterday': None, 'Evanescence|Bring Me to Life': 2003, 'The Killers|Mr. Brightside': 2003,
 't.A.T.u.|All the Things She Said': 2002, 'Outkast|Hey Ya!': 2003, 'Usher|Yeah!': 2004, 'Natasha Bedingfield|Unwritten': 2004,
 # 2005–2009
 'Gwen Stefani|Hollaback Girl': 2004, 'Gwen Stefani|The Sweet Escape': 2006, 'Mariah Carey|We Belong Together': 2005,
 'Sugababes|Push the Button': None, 'Rihanna|Pon de Replay': 2005, 'Rihanna|SOS': 2006, 'Rihanna|Umbrella': 2007,
 "Rihanna|Don't Stop the Music": 2007, 'Rihanna|Disturbia': 2008, 'Beyoncé|Irreplaceable': 2006,
 'Beyoncé|Single Ladies (Put a Ring on It)': 2008, 'Beyoncé|Halo': 2008, "Shakira|Hips Don't Lie": 2006,
 'Nelly Furtado|Maneater': 2006, 'Nelly Furtado|Promiscuous': 2006, 'Fergie|Fergalicious': 2006, "Fergie|Big Girls Don't Cry": None,
 "The Pussycat Dolls|Don't Cha": 2005, 'The Pussycat Dolls|Buttons': None, 'Christina Aguilera|Candyman': None,
 'Avril Lavigne|Girlfriend': 2007, 'P!nk|So What': 2008, 'Katy Perry|I Kissed a Girl': 2008, 'Katy Perry|Hot N Cold': 2008,
 'Lady Gaga|Just Dance': 2008, 'Lady Gaga|Poker Face': 2008, 'Lady Gaga|Paparazzi': 2008, 'Lady Gaga|Bad Romance': 2009,
 'Lady Gaga|Telephone': 2009, 'Britney Spears|Womanizer': 2008, 'Britney Spears|Circus': None, 'Britney Spears|Gimme More': 2007,
 'Leona Lewis|Bleeding Love': 2007, 'Duffy|Mercy': None, 'Amy Winehouse|Rehab': 2006, 'Kesha|TiK ToK': 2009,
 'Miley Cyrus|Party in the U.S.A.': 2009, 'Miley Cyrus|The Climb': None, 'Taylor Swift|Love Story': 2008,
 'Taylor Swift|You Belong With Me': 2008, 'Paramore|Misery Business': 2007, 'Black Eyed Peas|I Gotta Feeling': 2009,
 'Sara Bareilles|Love Song': None, 'Colbie Caillat|Bubbly': None, "Plain White T's|Hey There Delilah": 2005,
 'Snow Patrol|Chasing Cars': 2006, 'Owl City|Fireflies': None, 'Cascada|Evacuate the Dancefloor': 2009, 'La Roux|Bulletproof': None,
 'Florence + The Machine|Dog Days Are Over': 2008,
 # 2010–2014
 'Kesha|Your Love Is My Drug': None, 'Kesha|Die Young': 2012, 'Katy Perry|California Gurls': 2010, 'Katy Perry|Teenage Dream': 2010,
 'Katy Perry|Firework': 2010, 'Katy Perry|Last Friday Night (T.G.I.F.)': 2010, 'Katy Perry|Roar': 2013, 'Katy Perry|Dark Horse': 2013,
 'Rihanna|Only Girl (In the World)': 2010, "Rihanna|What's My Name?": None, 'Rihanna|S&M': 2010, 'Rihanna|Rude Boy': 2009,
 'Rihanna|We Found Love': 2011, 'Rihanna|Diamonds': 2012, 'Lady Gaga|Born This Way': 2011, 'Lady Gaga|Alejandro': 2009,
 'Adele|Rolling in the Deep': 2010, 'Adele|Someone Like You': 2011, 'Adele|Set Fire to the Rain': None,
 'Taylor Swift|We Are Never Ever Getting Back Together': 2012, 'Taylor Swift|I Knew You Were Trouble': 2012, 'Taylor Swift|22': 2012,
 'Taylor Swift|Shake It Off': 2014, 'Taylor Swift|Blank Space': 2014, 'Carly Rae Jepsen|Call Me Maybe': 2011,
 'Ellie Goulding|Lights': None, 'Ellie Goulding|Burn': 2013, 'Jessie J|Price Tag': 2011,
 'Selena Gomez & The Scene|Love You Like a Love Song': 2011, 'Miley Cyrus|Wrecking Ball': 2013, "Miley Cyrus|We Can't Stop": None,
 'Icona Pop|I Love It': 2012, 'Lorde|Royals': 2012, 'Ariana Grande|Problem': 2014, 'Ariana Grande|Break Free': 2014,
 'Iggy Azalea|Fancy': 2014, 'Meghan Trainor|All About That Bass': 2014, 'Jessie J|Bang Bang': 2014, 'Nicki Minaj|Super Bass': 2010,
 'Nicki Minaj|Starships': 2012, 'Beyoncé|Run the World (Girls)': 2011, 'Beyoncé|Drunk in Love': None,
 'One Direction|What Makes You Beautiful': 2011, 'LMFAO|Party Rock Anthem': 2011, 'Avicii|Wake Me Up': None, 'Sia|Chandelier': 2014,
 'Lana Del Rey|Video Games': 2011, 'Lana Del Rey|Summertime Sadness': 2012, "Kelly Clarkson|Stronger (What Doesn't Kill You)": 2011,
 'Clean Bandit|Rather Be': None, 'Charli XCX|Boom Clap': None, 'Demi Lovato|Heart Attack': None,
 # 2015–2019
 'Ellie Goulding|Love Me Like You Do': 2015, 'Fifth Harmony|Worth It': 2015, 'Taylor Swift|Look What You Made Me Do': 2017,
 'Ariana Grande|Into You': 2016, 'Ariana Grande|Side to Side': 2016, 'Ariana Grande|no tears left to cry': None,
 'Ariana Grande|thank u, next': 2018, 'Ariana Grande|7 rings': 2019, 'Rihanna|Work': 2016,
 'Calvin Harris|This Is What You Came For': 2016, 'Lady Gaga|Shallow': 2018, 'Calvin Harris|One Kiss': 2018,
 'Camila Cabello|Havana': 2017, 'Selena Gomez|Hands to Myself': 2015, 'Selena Gomez|Bad Liar': None,
 'Demi Lovato|Cool for the Summer': 2015, 'Demi Lovato|Sorry Not Sorry': 2017, 'The Chainsmokers|Closer': 2016,
 'Zara Larsson|Lush Life': 2015, 'Little Mix|Shout Out to My Ex': 2016, 'Ava Max|Sweet but Psycho': 2018, 'Billie Eilish|bad guy': 2019,
 'Lizzo|Truth Hurts': 2017, 'Lizzo|Good as Hell': None, 'Harry Styles|Watermelon Sugar': 2019, 'Lorde|Green Light': 2017,
 'Doja Cat|Say So': 2019, 'Sia|Cheap Thrills': 2016, 'Beyoncé|Formation': 2016, 'Taylor Swift|Cruel Summer': 2019,
 # 2020–heute
 'Dua Lipa|Houdini': 2023, 'Olivia Rodrigo|drivers license': 2021, 'Olivia Rodrigo|good 4 u': 2021, 'Olivia Rodrigo|deja vu': None,
 'Olivia Rodrigo|vampire': 2023, 'Olivia Rodrigo|bad idea right?': None, 'Taylor Swift|cardigan': 2020, 'Taylor Swift|Anti-Hero': 2022,
 'Taylor Swift|The Fate of Ophelia': 2025, 'Miley Cyrus|Flowers': 2023, 'Miley Cyrus|Midnight Sky': None,
 'Sabrina Carpenter|Espresso': 2024, 'Sabrina Carpenter|Please Please Please': 2024, 'Sabrina Carpenter|Manchild': 2025,
 'Chappell Roan|Pink Pony Club': 2020, 'Chappell Roan|Good Luck, Babe!': 2024, 'Chappell Roan|HOT TO GO!': 2023,
 'Billie Eilish|BIRDS OF A FEATHER': 2024, 'Billie Eilish|What Was I Made For?': 2023, 'Harry Styles|As It Was': 2022,
 'Doja Cat|Kiss Me More': 2021, 'Ariana Grande|positions': None, 'Ariana Grande|yes, and?': 2024,
 'Lady Gaga|Die With A Smile': 2024, 'Lady Gaga|Abracadabra': 2025, 'ROSÉ|APT.': 2024, 'Charli xcx|360': 2024,
 'Charli xcx|Apple': None, 'Tate McRae|greedy': 2023, "Gracie Abrams|That's So True": 2024, 'Lizzo|About Damn Time': None,
 'Beyoncé|BREAK MY SOUL': 2022, 'Kylie Minogue|Padam Padam': None,
}

# Zweite Kürzungsrunde auf ~135 Songs: schwächere Titel und Doppelungen je Künstlerin
for k in ['Usher|Yeah!', 'Mariah Carey|We Belong Together', 'Rihanna|Pon de Replay', 'Lady Gaga|Paparazzi', 'Britney Spears|Gimme More',
          'Leona Lewis|Bleeding Love', 'Florence + The Machine|Dog Days Are Over', 'Katy Perry|Dark Horse', 'Rihanna|Rude Boy',
          'Lady Gaga|Alejandro', 'Taylor Swift|I Knew You Were Trouble', 'Ellie Goulding|Burn', 'Lana Del Rey|Video Games',
          'Fifth Harmony|Worth It', 'Ariana Grande|Into You', 'Selena Gomez|Hands to Myself', 'Demi Lovato|Sorry Not Sorry',
          'Zara Larsson|Lush Life', 'Little Mix|Shout Out to My Ex', 'Lorde|Green Light', 'Sia|Cheap Thrills', 'Beyoncé|Formation',
          'Taylor Swift|cardigan', 'Billie Eilish|What Was I Made For?', 'Charli xcx|360', "Nelly Furtado|I'm Like a Bird",
          'Dua Lipa|Levitating']:
    YEAR[k] = None

# Songs, die das Skript nicht gefunden hat (von Hand über die Top-Songs der Künstler gesucht)
EXTRA = [
 (1065583332, 'Dua Lipa', 'New Rules', 2017),
 (788708262, 'Dua Lipa', "Don't Start Now", 2019),
 (1122003492, 'Dua Lipa', 'Levitating', 2020),
]

# Falsche Deezer-Version erwischt (Remix/Live/Cover/Übersetzung) → Original-ID
ID_FIX = {
 'Shakira|Whenever, Wherever': 15211178, 'Rihanna|SOS': 1574660, 'Beyoncé|Irreplaceable': 4264585742,
 'Snow Patrol|Chasing Cars': 1576190, 'Kesha|Die Young': 62710229, 'Carly Rae Jepsen|Call Me Maybe': 60726419,
 'Ellie Goulding|Burn': 78176590, 'Icona Pop|I Love It': 69959333, 'Lana Del Rey|Summertime Sadness': 16047072,
 'Lana Del Rey|Video Games': 16047065, 'Beyoncé|Formation': 669486732, 'Gwen Stefani|Hollaback Girl': 983450,
 'Katy Perry|Firework': 13460186,
}

# Anzeige der Interpreten (Features sauber ausgeschrieben)
ARTIST = {
 'Beyoncé|Crazy in Love': 'Beyoncé feat. JAY-Z', 'Rihanna|Umbrella': 'Rihanna feat. JAY-Z',
 "Shakira|Hips Don't Lie": 'Shakira feat. Wyclef Jean', 'Usher|Yeah!': 'Usher feat. Lil Jon & Ludacris',
 'Christina Aguilera|Dirrty': 'Christina Aguilera feat. Redman', 'Nelly Furtado|Promiscuous': 'Nelly Furtado feat. Timbaland',
 "The Pussycat Dolls|Don't Cha": 'The Pussycat Dolls feat. Busta Rhymes', 'Lady Gaga|Just Dance': 'Lady Gaga feat. Colby O’Donis',
 'Lady Gaga|Telephone': 'Lady Gaga feat. Beyoncé', 'Rihanna|We Found Love': 'Rihanna feat. Calvin Harris',
 'Rihanna|Work': 'Rihanna feat. Drake', 'Katy Perry|California Gurls': 'Katy Perry feat. Snoop Dogg',
 'Katy Perry|Dark Horse': 'Katy Perry feat. Juicy J', 'Icona Pop|I Love It': 'Icona Pop feat. Charli XCX',
 'Ariana Grande|Problem': 'Ariana Grande feat. Iggy Azalea', 'Iggy Azalea|Fancy': 'Iggy Azalea feat. Charli XCX',
 'Jessie J|Bang Bang': 'Jessie J, Ariana Grande & Nicki Minaj', 'Jessie J|Price Tag': 'Jessie J feat. B.o.B',
 'Ariana Grande|Side to Side': 'Ariana Grande feat. Nicki Minaj', 'Fifth Harmony|Worth It': 'Fifth Harmony feat. Kid Ink',
 'Calvin Harris|This Is What You Came For': 'Calvin Harris feat. Rihanna', 'Calvin Harris|One Kiss': 'Calvin Harris & Dua Lipa',
 'Lady Gaga|Shallow': 'Lady Gaga & Bradley Cooper', 'Camila Cabello|Havana': 'Camila Cabello feat. Young Thug',
 'The Chainsmokers|Closer': 'The Chainsmokers feat. Halsey', 'Sia|Cheap Thrills': 'Sia feat. Sean Paul',
 'Doja Cat|Kiss Me More': 'Doja Cat feat. SZA', 'Lady Gaga|Die With A Smile': 'Lady Gaga & Bruno Mars',
 'ROSÉ|APT.': 'ROSÉ & Bruno Mars', 'Charli xcx|360': 'Charli XCX', 'Kelly Clarkson|Stronger (What Doesn\'t Kill You)': 'Kelly Clarkson',
}
TITLE = {'Billie Eilish|BIRDS OF A FEATHER': 'Birds of a Feather', 'Beyoncé|BREAK MY SOUL': 'Break My Soul'}

songs, missing = [], []
for key, y in YEAR.items():
    if not y:
        continue
    e = res.get(key)
    if not e and key not in ID_FIX:
        missing.append(key)
        continue
    artist, title = key.split('|')
    songs.append({'id': ID_FIX.get(key) or e['id'], 'artist': ARTIST.get(key, artist), 'title': TITLE.get(key, title), 'year': y})
unreviewed = [k for k in res if k not in YEAR]
for i, a, t, y in EXTRA:
    songs.append({'id': i, 'artist': a, 'title': t, 'year': y})

seen = set()
songs = [s for s in songs if not (s['id'] in seen or seen.add(s['id']))]
songs.sort(key=lambda s: (s['year'], s['artist']))
cat = {'id': 'whitegirl', 'name': 'White Girl Music',
       'description': 'Pop-Banger zum Mitgrölen – Rihanna, Gaga, Britney, Taylor & Co. Schwerpunkt ab 2000.', 'songs': songs}
json.dump(cat, open('../data/whitegirl.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

years = [s['year'] for s in songs]
print(len(songs), 'Songs'); print(sorted(Counter(years).items()))
print('ab 2000:', sum(y >= 2000 for y in years), '| fehlt:', missing, '| nicht geprüft:', unreviewed)
EOF_MARKER = None
