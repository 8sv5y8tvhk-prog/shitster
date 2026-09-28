"""Kategorie „EDM“ – Schwerpunkt EDM-Boom ab 2009, davor nur die ganz großen Klassiker, bekannte Remixe erlaubt."""
from catbuild import build

X = None  # bewusst nicht aufgenommen
YEAR = {
 # Klassiker vor 2009
 'Daft Punk|One More Time': 2000, 'Daft Punk|Around the World': 1997, 'Stardust|Music Sounds Better with You': 1998,
 "Gigi D'Agostino|L'amour toujours": 1999, 'Kernkraft 400|Zombie Nation': X, 'Robert Miles|Children': 1995,
 'Eric Prydz|Pjanoo': 2008, "Deadmau5|Ghosts 'n' Stuff": X, 'Fedde Le Grand|Put Your Hands Up for Detroit': 2006,
 'Bob Sinclar|World, Hold On (Children of the Sky)': 2006, 'David Guetta|Love Is Gone': 2007, 'Tiësto|Adagio for Strings': 2004,
 'Paul Kalkbrenner|Sky and Sand': 2008, 'Daft Punk|Harder, Better, Faster, Stronger': 2001,
 # EDM-Boom 2009–2016
 'Avicii|Levels': 2011, 'Avicii|Wake Me Up': 2013, 'Avicii|Hey Brother': 2013, 'Avicii|The Nights': 2014,
 'Avicii|Waiting for Love': 2015, 'Avicii|Silhouettes': 2012, 'Avicii|Without You': 2017,
 'Swedish House Mafia|One (Your Name)': 2010, 'Swedish House Mafia|Save the World': 2011,
 "Swedish House Mafia|Don't You Worry Child": 2012, 'Swedish House Mafia|Greyhound': 2012, 'Swedish House Mafia|Miami 2 Ibiza': 2010,
 'Axwell Λ Ingrosso|More Than You Know': 2017, 'Axwell Λ Ingrosso|Sun Is Shining': 2015, 'David Guetta|Titanium': 2011,
 'David Guetta|Without You': 2011, 'David Guetta|Sexy Bitch': 2009, 'David Guetta|Memories': 2009, 'David Guetta|Play Hard': X,
 'David Guetta|Hey Mama': 2014, 'David Guetta|Lovers on the Sun': 2014, 'David Guetta|Bad': 2014,
 'David Guetta|She Wolf (Falling to Pieces)': 2012, 'Calvin Harris|Feel So Close': 2011, 'Calvin Harris|Summer': 2014,
 'Calvin Harris|Blame': 2014, 'Calvin Harris|Sweet Nothing': 2012, 'Calvin Harris|Outside': 2014,
 'Calvin Harris|How Deep Is Your Love': 2015, 'Calvin Harris|I Need Your Love': 2012, 'Tiësto|Red Lights': 2013,
 'Tiësto|Wasted': 2014, 'Hardwell|Spaceman': 2012, 'Hardwell|Apollo': 2012, 'Afrojack|Take Over Control': 2010,
 'Alesso|Heroes (We Could Be)': 2014, 'Otto Knows|Million Voices': 2012, 'Zedd|Clarity': 2012, 'Zedd|Stay the Night': 2013,
 'Skrillex|Scary Monsters and Nice Sprites': 2010, 'Skrillex|Bangarang': 2011, 'Skrillex|Where Are Ü Now': X,
 'Knife Party|Bonfire': 2012, "Flux Pavilion|I Can't Stop": 2010, 'Major Lazer|Lean On': 2015,
 'Major Lazer|Light It Up (Remix)': 2015, 'Major Lazer|Cold Water': 2016, 'DJ Snake|Turn Down for What': 2013,
 'DJ Snake|Let Me Love You': 2016, 'Dimitri Vegas & Like Mike|Mammoth': X, 'Martin Garrix|Animals': 2013,
 'Martin Garrix|In the Name of Love': 2016, 'Martin Garrix|Scared to Be Lonely': 2017, 'Showtek|Booyah': X,
 'Nicky Romero|Toulouse': X, 'Deorro|Five Hours': 2014, 'Martin Solveig|Hello': 2010, 'Alan Walker|Faded': 2015,
 'Alan Walker|Alone': X, 'Alan Walker|The Spectre': 2017, 'Kygo|Firestone': 2014, 'Kygo|Stole the Show': 2015,
 "Kygo|It Ain't Me": 2017, 'The Chainsmokers|Roses': 2015, "The Chainsmokers|Don't Let Me Down": 2016,
 'Robin Schulz|Sugar': 2015, 'Robin Schulz|Headlights': 2015, 'OMI|Cheerleader (Felix Jaehn Remix)': 2014,
 "Felix Jaehn|Ain't Nobody (Loves Me Better)": 2015, 'Lost Frequencies|Are You With Me': 2014, 'Lost Frequencies|Reality': 2015,
 'Mike Posner|I Took a Pill in Ibiza (Seeb Remix)': 2015, 'Klingande|Jubel': 2013, 'Duke Dumont|Ocean Drive': 2015,
 'Disclosure|Latch': 2012, 'Clean Bandit|Rather Be': 2014, 'Armin van Buuren|This Is What It Feels Like': 2013,
 'Armin van Buuren|Blah Blah Blah': 2018, 'Timmy Trumpet|Freaks': 2014, 'Deadmau5|Strobe': 2009, 'Eric Prydz|Opus': 2015,
 'Kungs|This Girl': 2016, 'Sigala|Easy Love': 2015, 'Jonas Blue|Fast Car': 2015, 'Marshmello|Alone': 2016,
 'Porter Robinson|Language': X, 'Mako|Beam': X, 'Galantis|Runaway (U & I)': 2014, 'Galantis|Peanut Butter Jelly': X,
 'Sam Feldt|Show Me Love': X, 'Oliver Heldens|Gecko (Overdrive)': 2014, 'DVBBS|Tsunami': X, 'Sebastian Ingrosso|Reload': 2012,
 # 2017 bis heute
 'Marshmello|Happier': 2018, 'Marshmello|Friends': X, 'Meduza|Piece of Your Heart': 2019, 'Meduza|Lose Control': 2019,
 'Topic|Breaking Me': 2019, 'SAINt JHN|Roses (Imanbek Remix)': 2019, 'Joel Corry|Head & Heart': 2020, 'Acraze|Do It to It': 2021,
 'Regard|Ride It': 2019, 'Tiësto|The Business': 2020, 'Tiësto|10:35': 2022, "Fred again..|Marea (We've Lost Dancing)": 2021,
 'Fred again..|Turn On the Lights again..': 2022, 'Peggy Gou|(It Goes Like) Nanana': 2023, "David Guetta|I'm Good (Blue)": 2022,
 "David Guetta|Baby Don't Hurt Me": 2023, 'Calvin Harris|Miracle': 2023, 'Calvin Harris|Feels': 2017, 'Calvin Harris|Slide': X,
 'Fisher|Losing It': 2018, 'Mau P|Drugs From Amsterdam': 2022, 'Eliza Rose|B.O.T.A. (Baddest Of Them All)': 2022,
 'Kungs|Never Going Home': 2021, 'Lost Frequencies|Where Are You Now': 2021, 'Purple Disco Machine|Hypnotized': 2020,
 'Cassö|Prada': 2023, 'Alok|Hear Me Now': 2016, 'Swedish House Mafia|Moth to a Flame': 2021,
 'Martin Garrix|High on Life': 2018, 'Dom Dolla|Saving Up': 2023, 'Chris Lake|Turn Off the Lights': X,
 'John Summit|Where You Are': X, 'Anyma|Eternity': X, 'Kx5|Escape': 2022, 'Swedish House Mafia|It Gets Better': X,
 'Hugel|I Adore You': 2024,
}
ID_FIX = {
 'Avicii|Levels': 14383880, 'David Guetta|Lovers on the Sun': 90250609, 'David Guetta|Bad': 76520669,
 'Calvin Harris|Feel So Close': 61142285, 'Martin Solveig|Hello': 3803035232, 'Klingande|Jubel': 70322528,
 'Deadmau5|Strobe': 5150299, 'The Chainsmokers|Roses': 110148950, 'Kx5|Escape': 1899047597,
 'Calvin Harris|Feels': 374051471,
}
EXTRA = [
 (78527813, 'OneRepublic', 'If I Lose Myself (Alesso vs OneRepublic)', 2013),
 (1777963277, 'Dimitri Vegas & Like Mike & Martin Garrix', 'Tremor', 2014),
 (63017512, 'Avicii & Nicky Romero', 'I Could Be the One', 2012),
 (142706538, 'The Chainsmokers & Coldplay', 'Something Just Like This', 2017),
 (84908527, 'Lilly Wood & The Prick', 'Prayer in C (Robin Schulz Remix)', 2014),
 (1084861832, 'Mr. Probz', 'Waves (Robin Schulz Remix)', 2014),
 (73460627, 'Axwell, Ingrosso, Angello & Laidback Luke', 'Leave the World Behind', 2009),
 (1457025872, 'Elton John & Dua Lipa', 'Cold Heart (PNAU Remix)', 2021),
]
ARTIST = {'David Guetta|Bad': 'David Guetta & Showtek feat. Vassy', 'Kx5|Escape': 'Kx5 feat. Hayla'}

build('edm', 'EDM', 'Festival-Banger und Club-Hits – von Avicii und Swedish House Mafia bis Fred again.. und Peggy Gou.',
      YEAR, ID_FIX, EXTRA, artist=ARTIST)
