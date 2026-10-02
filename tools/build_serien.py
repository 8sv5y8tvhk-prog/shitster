"""Kategorie „Serien & Filme“ – nur Kinderserien und Filme von 1995 bis 2010 (Wunsch des Nutzers, 02.10.2026).

Besonderheit: Jeder Song hat ein Feld `show` (Serie bzw. Film). Die App zeigt es als Haupttitel,
der Bonus heißt dort „Serie erkannt“. Jahr = Start der Serie bzw. Erscheinungsjahr des Films (Wunsch des Nutzers).
Kinderserien/Anime auf Deutsch, wo das Original auf Deezer verfügbar ist, sonst Original; Erwachsenen-Serien und Filme im Original.
Nur Originalaufnahmen – Cover-Bands (TV Sounds Unlimited, Dominik Hauser, Kontrollverlust, Anime Allstars ohne Originalsänger …) sind raus.
Danach: python3 fix_artists.py serien && python3 verify.py serien && python3 make_index.py
"""
import json, os

# (Serie/Film, Jahr, Deezer-ID, Songtitel, Interpret)
SONGS = [
 # Kinderserien & Anime
 ('Pokémon', 1997, 3504033041, 'Pokémon Theme', 'Pokémon'),
 ('Teletubbies', 1997, 3256172991, 'Teletubbies Theme', 'Teletubbies'),
 ('Bob der Baumeister', 1998, 952358072, 'Can We Fix It? Yes We Can!', 'Bob the Builder'),
 ('Digimon', 1999, 603896, 'Leb deinen Traum', 'Frank Schindel'),
 ('SpongeBob Schwammkopf', 1999, 4173198372, 'Titelsong', 'SpongeBob Schwammkopf'),
 ('Lizzie McGuire', 2001, 677779022, 'Theme to Lizzie McGuire', 'Angie Jaree'),
 ('Kim Possible', 2002, 3153721, 'Call Me, Beep Me!', 'Christina Milian'),
 ('Teen Titans', 2003, 976699292, 'Teen Titans Theme', 'Puffy AmiYumi'),
 ('LazyTown', 2004, 79494752, 'Bing Bang', 'LazyTown'),
 ('Avatar – Der Herr der Elemente', 2005, 3466172801, 'Main Title', 'Jeremy Zuckerman'),
 ('H2O – Plötzlich Meerjungfrau', 2006, 1766399697, 'No Ordinary Girl', 'Kate Alexa'),
 ('Phineas und Ferb', 2007, 3725658642, 'Titelsong', 'Manuel Straube'),
 # Disney Channel & Nickelodeon
 ('Raven blickt durch', 2003, 1165064092, "That's So Raven", 'Raven-Symoné'),
 ('Drake & Josh', 2004, 914388672, 'Found a Way', 'Drake Bell'),
 ('Zoey 101', 2005, 1109501502, 'Follow Me', 'Jamie Lynn Spears'),
 ('Hannah Montana', 2006, 13275871, 'The Best of Both Worlds', 'Hannah Montana'),
 ('iCarly', 2007, 13161512, 'Leave It All to Me', 'Miranda Cosgrove feat. Drake Bell'),
 ('Die Zauberer vom Waverly Place', 2007, 5323464, 'Everything Is Not What It Seems', 'Selena Gomez'),
 ('Big Time Rush', 2009, 10391894, 'Big Time Rush', 'Big Time Rush'),
 ('Sonny Munroe', 2009, 4231648, 'So Far So Great', 'Demi Lovato'),
 ('Jonas', 2009, 5323457, 'Live to Party', 'Jonas Brothers'),
 ('Victorious', 2010, 4069964191, 'Make It Shine', 'Victorious Cast'),
 # Disney-, Pixar- & Familienfilme
 ('Pocahontas', 1995, 3118641, 'Colors of the Wind', 'Judy Kuhn'),
 ('Toy Story', 1995, 696962792, "You've Got a Friend in Me", 'Randy Newman'),
 ('Space Jam', 1996, 135872772, 'Space Jam', "Quad City DJ's"),
 ('Hercules', 1997, 531228911, "I Won't Say (I'm in Love)", 'Susan Egan'),
 ('Mulan', 1998, 1377537512, "I'll Make a Man Out of You", 'Donny Osmond'),
 ('Tarzan', 1999, 561875132, "You'll Be in My Heart", 'Phil Collins'),
 ('Die Monster AG', 2001, 128946464, "If I Didn't Have You", 'Billy Crystal & John Goodman'),
 ('Shrek', 2001, 917717, 'All Star', 'Smash Mouth'),
 ('Shrek', 2001, 917741, "I'm a Believer", 'Smash Mouth'),
 ('Plötzlich Prinzessin', 2001, 3117907, 'Miracles Happen', 'Myra'),
 ('Lilo & Stitch', 2002, 3118019, 'Hawaiian Roller Coaster Ride', "Mark Keali'i Ho'omalu"),
 ('Findet Nemo', 2003, 16162672, 'Beyond the Sea', 'Robbie Williams'),
 ('Popstar auf Umwegen', 2003, 1386338302, 'What Dreams Are Made Of', 'Hilary Duff'),
 ('Die Wilden Kerle', 2003, 635038, 'Es ist geil ein wilder Kerl zu sein', 'Bananafishbones'),
 ('Shrek 2', 2004, 145425722, 'Accidentally in Love', 'Counting Crows'),
 ('Die Unglaublichen', 2004, 24185421, 'The Incredits', 'Michael Giacchino'),
 ('Cars', 2006, 128948754, 'Life Is a Highway', 'Rascal Flatts'),
 ('High School Musical', 2006, 4242713, 'Breaking Free', 'Zac Efron & Vanessa Hudgens'),
 ('High School Musical', 2006, 4242714, "We're All in This Together", 'High School Musical Cast'),
 ('High School Musical 2', 2007, 3058861, 'What Time Is It', 'High School Musical Cast'),
 ('Ratatouille', 2007, 3107455, 'Le Festin', 'Camille'),
 ('Camp Rock', 2008, 24394231, 'This Is Me', 'Demi Lovato & Joe Jonas'),
 ('High School Musical 3', 2008, 3070711, 'Now or Never', 'High School Musical Cast'),
 ('Kung Fu Panda', 2008, 623727802, 'Kung Fu Fighting', 'Cee-Lo Green & Jack Black'),
 ('Madagascar 2', 2008, 630829962, 'I Like to Move It', 'will.i.am'),
 ('WALL·E', 2008, 668947072, 'Down to Earth', 'Peter Gabriel'),
 ('Hannah Montana – Der Film', 2009, 4307896, 'The Climb', 'Miley Cyrus'),
 ('Oben', 2009, 3852711, 'Married Life', 'Michael Giacchino'),
 ('Camp Rock 2', 2010, 6970226, "Can't Back Down", 'Demi Lovato'),
 ('Ich – Einfach unverbesserlich', 2010, 373915541, 'Despicable Me', 'Pharrell Williams'),
 ('Rapunzel – Neu verföhnt', 2010, 7599985, 'I See the Light', 'Mandy Moore'),
 ('Toy Story 3', 2010, 887427682, 'We Belong Together', 'Randy Newman'),
 # Große Filme
 ('Titanic', 1997, 17000055, 'My Heart Will Go On', 'Céline Dion'),
 ('Armageddon', 1998, 624823, "I Don't Want to Miss a Thing", 'Aerosmith'),
 ('Gladiator', 2000, 3055975, 'Now We Are Free', 'Lisa Gerrard & Hans Zimmer'),
 ('Harry Potter und der Stein der Weisen', 2001, 661779, "Hedwig's Theme", 'John Williams'),
 ('Der Herr der Ringe: Die Gefährten', 2001, 14628816, 'Concerning Hobbits', 'Howard Shore'),
 ('Spider-Man', 2002, 15220573, 'Main Title', 'Danny Elfman'),
 ('Fluch der Karibik', 2003, 3117931, "He's a Pirate", 'Klaus Badelt'),
 ('Twilight', 2008, 2723257, 'Decode', 'Paramore'),
 ('Inception', 2010, 6524423, 'Time', 'Hans Zimmer'),
]

songs = [{'id': i, 'artist': a, 'title': t, 'year': y, 'show': show} for show, y, i, t, a in SONGS]
ids = [s['id'] for s in songs]
assert len(ids) == len(set(ids)), 'doppelte Deezer-ID'
songs.sort(key=lambda s: (s['year'], s['show']))
cat = {'id': 'serien', 'name': 'Serien & Filme',
       'description': 'Kinderserien, Disney Channel und Filme von 1995 bis 2010 – erkennst du die Serie oder den Film?', 'songs': songs}
json.dump(cat, open(os.path.join(os.path.dirname(__file__), '..', 'data', 'serien.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(songs), 'Songs |', sorted(Counter(f"{s['year'] // 10 * 10}er" for s in songs).items()))
