"""Kategorie „80er, 90er & 2000er“ – je ~45 Songs pro Jahrzehnt, international mit wenigen deutschen Klassikern."""
from catbuild import build

X = None  # bewusst nicht aufgenommen
YEAR = {
 # 80er
 'Michael Jackson|Billie Jean': 1982, 'Michael Jackson|Beat It': 1982, 'Michael Jackson|Thriller': 1982,
 'Michael Jackson|Smooth Criminal': 1987, 'Madonna|Like a Virgin': 1984, 'Madonna|Like a Prayer': 1989, 'Madonna|La Isla Bonita': X,
 'Whitney Houston|I Wanna Dance with Somebody (Who Loves Me)': 1987, 'Cyndi Lauper|Girls Just Want to Have Fun': 1983,
 'a-ha|Take On Me': 1985, 'Toto|Africa': 1982, "Journey|Don't Stop Believin'": 1981, 'Europe|The Final Countdown': 1986,
 'Survivor|Eye of the Tiger': 1982, 'Wham!|Wake Me Up Before You Go-Go': 1984, 'George Michael|Careless Whisper': 1984,
 'Duran Duran|Hungry Like the Wolf': X, 'Tears for Fears|Everybody Wants to Rule the World': 1985,
 'Eurythmics|Sweet Dreams (Are Made of This)': 1983, 'Soft Cell|Tainted Love': 1981, "The Human League|Don't You Want Me": 1981,
 "Depeche Mode|Just Can't Get Enough": 1981, 'Kim Wilde|Kids in America': X, 'Rick Astley|Never Gonna Give You Up': 1987,
 'Prince|Purple Rain': 1984, 'Prince|Kiss': 1986, 'Lionel Richie|All Night Long (All Night)': 1983, 'Kenny Loggins|Footloose': X,
 'Irene Cara|Flashdance... What a Feeling': 1983, 'Dexys Midnight Runners|Come On Eileen': 1982,
 "Simple Minds|Don't You (Forget About Me)": 1985, 'The Police|Every Breath You Take': 1983, 'Phil Collins|In the Air Tonight': 1981,
 'Bonnie Tyler|Total Eclipse of the Heart': 1983, "Modern Talking|You're My Heart, You're My Soul": 1984, 'Nena|99 Luftballons': 1983,
 'Falco|Rock Me Amadeus': 1985, 'Peter Schilling|Major Tom (völlig losgelöst)': 1983, 'Opus|Live Is Life': 1984,
 'Baltimora|Tarzan Boy': X, 'Men at Work|Down Under': 1981, 'Bananarama|Venus': X,
 'Dead or Alive|You Spin Me Round (Like a Record)': 1984, 'Culture Club|Karma Chameleon': 1983, 'Spandau Ballet|True': X,
 "Bobby McFerrin|Don't Worry Be Happy": 1988, 'UB40|Red Red Wine': X, "Tina Turner|What's Love Got to Do with It": 1984,
 'Tina Turner|The Best': 1989, "Starship|Nothing's Gonna Stop Us Now": X, 'Belinda Carlisle|Heaven Is a Place on Earth': X,
 'Roxette|The Look': 1988, 'Salt-N-Pepa|Push It': X, 'Paula Abdul|Straight Up': X, 'Queen|Another One Bites the Dust': 1980,
 'Kate Bush|Running Up That Hill (A Deal with God)': 1985, 'Pet Shop Boys|West End Girls': 1985, 'Frankie Goes to Hollywood|Relax': X,
 # 90er
 "Backstreet Boys|Everybody (Backstreet's Back)": 1997, 'Spice Girls|Spice Up Your Life': 1997, 'Haddaway|What Is Love': 1993,
 "Dr. Alban|It's My Life": X, 'Scatman John|Scatman (Ski-Ba-Bop-Ba-Dop-Bop)': 1994, 'Captain Hollywood Project|More and More': X,
 '2 Unlimited|No Limit': 1993, 'Snap!|Rhythm Is a Dancer': 1992, 'Culture Beat|Mr. Vain': 1993, 'La Bouche|Be My Lover': X,
 'Vengaboys|Boom, Boom, Boom, Boom!!': 1998, "Vengaboys|We're Going to Ibiza": X, 'Aqua|Barbie Girl': 1997,
 'Eiffel 65|Blue (Da Ba Dee)': 1998, 'Lou Bega|Mambo No. 5 (A Little Bit of...)': 1999, "Ricky Martin|Livin' la Vida Loca": 1999,
 'Los Del Rio|Macarena': 1995, "Coolio|Gangsta's Paradise": 1995, 'Fugees|Killing Me Softly': 1996, 'TLC|No Scrubs': 1999,
 'TLC|Waterfalls': X, 'Mariah Carey|Fantasy': X, 'Whitney Houston|I Will Always Love You': 1992,
 'Celine Dion|My Heart Will Go On': 1997, 'Oasis|Wonderwall': 1995, 'Alanis Morissette|Ironic': 1995, "No Doubt|Don't Speak": 1995,
 'Robbie Williams|Angels': 1997, 'Take That|Back for Good': 1995, 'Chumbawamba|Tubthumping': 1997, 'Mr. President|Coco Jamboo': X,
 'Sash!|Ecuador': X, 'DJ BoBo|Somebody Dance with Me': X, 'Die Fantastischen Vier|Die Da!?!': 1992,
 'Scooter|How Much Is the Fish?': 1998, 'Ace of Base|All That She Wants': 1992, 'Ace of Base|The Sign': X,
 'Roxette|It Must Have Been Love': 1990, 'Vanilla Ice|Ice Ice Baby': 1990, "MC Hammer|U Can't Touch This": 1990,
 'Will Smith|Men in Black': X, "Will Smith|Gettin' Jiggy Wit It": X, 'Dr. Dre|Still D.R.E.': 1999, '2Pac|California Love': 1995,
 'The Notorious B.I.G.|Hypnotize': X, "Puff Daddy|I'll Be Missing You": X, 'Eminem|My Name Is': 1999, 'Madonna|Vogue': 1990,
 'Michael Jackson|Black or White': 1991, 'Seal|Kiss from a Rose': X, 'Bryan Adams|(Everything I Do) I Do It for You': 1991,
 'Faithless|Insomnia': X, 'ATB|9 PM (Till I Come)': 1998, 'Darude|Sandstorm': 1999, 'Alice Deejay|Better Off Alone': X,
 'Rednex|Cotton Eye Joe': 1994, 'Gala|Freed from Desire': 1996, 'Corona|The Rhythm of the Night': 1993,
 'Sixpence None the Richer|Kiss Me': X, 'Savage Garden|Truly Madly Deeply': 1997, 'Hanson|MMMBop': 1997,
 'The Verve|Bitter Sweet Symphony': 1997, 'Natalie Imbruglia|Torn': 1997, "Des'ree|You Gotta Be": X,
 'Depeche Mode|Enjoy the Silence': 1990, 'The Prodigy|Firestarter': 1996, "Destiny's Child|Say My Name": 1999,
 # 2000er
 'Eminem|The Real Slim Shady': 2000, 'Eminem|Without Me': 2002, 'Eminem|Lose Yourself': 2002, '50 Cent|In da Club': 2003,
 'Nelly|Hot in Herre': 2002, 'Black Eyed Peas|Where Is the Love?': 2003, 'Black Eyed Peas|Pump It': X, 'Usher|Yeah!': 2004,
 'Sean Paul|Get Busy': 2002, 'Sean Paul|Temperature': X, "Shaggy|It Wasn't Me": 2000, 'Daniel Powter|Bad Day': 2005,
 "James Blunt|You're Beautiful": 2004, 'Coldplay|Viva la Vida': 2008, 'Coldplay|Clocks': X,
 'Las Ketchup|The Ketchup Song (Aserejé)': 2002, 'Eric Prydz|Call on Me': 2004, 'Bob Sinclar|Love Generation': 2005,
 'Benny Benassi|Satisfaction': 2002, 'David Guetta|When Love Takes Over': 2009, 'Kanye West|Stronger': 2007,
 'Kanye West|Gold Digger': 2005, 'Timbaland|The Way I Are': 2007, 'Akon|Smack That': 2006, 'Akon|Lonely': X,
 'Justin Timberlake|SexyBack': 2006, 'Justin Timberlake|Cry Me a River': X, 'Gnarls Barkley|Crazy': 2006, 'Mika|Grace Kelly': 2007,
 'Gorillaz|Feel Good Inc.': 2005, 'Robbie Williams|Feel': X, 'Crazy Frog|Axel F': 2005, "Snoop Dogg|Drop It Like It's Hot": 2004,
 'Missy Elliott|Get Ur Freak On': 2001, 'Missy Elliott|Work It': X, 'Flo Rida|Low': 2007, 'Jay-Z|Empire State of Mind': 2009,
 "Alicia Keys|Fallin'": 2001, 'Craig David|7 Days': 2000, 'Modjo|Lady (Hear Me Tonight)': 2000,
 "Spiller|Groovejet (If This Ain't Love)": X, 'Tokio Hotel|Durch den Monsun': 2005, 'Peter Fox|Haus am See': 2008,
 'Leona Lewis|Bleeding Love': 2007, 'Duffy|Mercy': X, 'MGMT|Kids': X, 'Keane|Somewhere Only We Know': X,
 'The Fray|How to Save a Life': 2005, 'Timbaland|Apologize': X, 'Maroon 5|This Love': 2002,
 'Pitbull|I Know You Want Me (Calle Ocho)': 2009, "Basshunter|Now You're Gone": 2007, 'Mariah Carey|We Belong Together': 2005,
 'Rihanna|Pon de Replay': 2005, 'Nelly Furtado|Say It Right': X, 'Amy Winehouse|Valerie': X, 'Kelis|Milkshake': 2003,
 'OneRepublic|Stop and Stare': X, 'Train|Hey, Soul Sister': X,
}
ID_FIX = {
 'Michael Jackson|Smooth Criminal': 4603400, 'Haddaway|What Is Love': 3801648492, 'Take That|Back for Good': 848836952,
 'The Verve|Bitter Sweet Symphony': 432946922, 'The Prodigy|Firestarter': 62126191, 'Coldplay|Viva la Vida': 13444256,
 'Las Ketchup|The Ketchup Song (Aserejé)': 476739482, 'Benny Benassi|Satisfaction': 13839055,
 'Tokio Hotel|Durch den Monsun': 7718640, "The Human League|Don't You Want Me": 3152080, 'Los Del Rio|Macarena': 990761,
}
EXTRA = [(7923756, 'Mark Ronson feat. Amy Winehouse', 'Valerie', 2007)]
TITLE = {'Die Fantastischen Vier|Die Da!?!': 'Die Da!?!', 'Fugees|Killing Me Softly': 'Killing Me Softly with His Song'}

build('dekaden', '80er, 90er & 2000er', 'Die größten Hits aus drei Jahrzehnten – von Michael Jackson über Eurodance bis Eminem.',
      YEAR, ID_FIX, EXTRA, title=TITLE)
