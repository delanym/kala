# -*- coding: UTF-8 -*-

""" Coding Convention:

CONSTANTS are all caps
Classes and DataTypes are capitalized
functions, methods and guiElements are camel case
locThrwAwayVars are contracted and camel case
global and local_variables are easily recognizable and joined with an underscore

4 space indent
Two open lines after a return statement
There is no limit to line length """

from collections import namedtuple, deque

# Types
Birth = namedtuple('Birth', ['name', 'place', 'era', 'lst', 'year', 'month', 'day', 'lst_delta', 'relation', 'dst_delta', 'julian_day_ut', 'comments'])
Date = namedtuple('Date', ['year', 'month', 'day'])
Point = namedtuple('Point', ['Date', 'hour', 'minute', 'delta', 'margin'])
Time = namedtuple('Time', ['default', 'calendar', 'zone', 'points', 'source'])
Event = namedtuple('Event', ['type', 'description', 'times', 'extent'])
Person = namedtuple('Person', ['name', 'notes', 'privacy', 'url', 'events'])

Sign = namedtuple('Sign', ['num', 'name', 'glyph', 'lord', 'element', 'mode'])
Nakshatra = namedtuple('Nakshatra', ['num', 'name', 'lord', 'deity', 'symbol'])
PlanetSolar = namedtuple('PlanetSolar', ['num', 'name', 'glyph', 'exalted', 'debility', 'weekday'])
PlanetLunar = namedtuple('PlanetLunar', ['num', 'name', 'glyph', 'dasa'])
Tithi = namedtuple('Tithi', ['num', 'name', 'omen', 'deity'])
Animal = namedtuple('Animal', ['num', 'name', 'trait', 'soulmate', 'inkind', 'combat', 'peach', 'steed', 'opposition', 'trine', 'karma'])

Mahadasa = namedtuple('Mahadasa', ['mahadasa', 'rise', 'antardasas'])
Dasa = namedtuple('Dasa', ['dasa', 'rise', 'end'])

Analysis = namedtuple('Analysis', ['source', 'category', 'key1', 'key2', 'key3', 'description'])


# Constants
SUN_YEAR = 365.2522
MOON_MONTH = 27.3217
SYNODIC_MONTH = 29.5306
MEAN_LUMINARY_SPEED = (360/MOON_MONTH) - (360/SUN_YEAR) # The mean speed at which the moon and sun pass each other ~12.190719339
NAKSHATRADEGREE = 360 / 27.0

PHASE_METHOD_FULL_BREATH = 0       # Amavasya ends when moon and sun conjunct. Tithis for whole month are equal in time.
PHASE_METHOD_HALF_BREATH = 1       # Amavasya ends when moon and sun conjunct. Tithis of each half are equal in time.
PHASE_METHOD_CRITICAL = 2          # Amavasya ends when moon and sun conjunct. Tithis of each half are equal in degrees.
PHASE_METHOD_NOBLE = 3             # Amavasya is at it's height when moon and sun conjunct.  Tithis are equal in degrees.
PHASE_METHOD_NAMES = ['Full Breath', 'Half Breath', 'Critical', 'Noble', 'Jaganatha Hora']


# Lists
SIGN_GLYPHS = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]
SIGN_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
SIGN_ELEMENTS = ["Fire", "Earth", "Air", "Water", "Fire", "Earth", "Air", "Water", "Fire", "Earth", "Air", "Water"]
SIGN_MODES = ["Cardinal", "Fixed", "Mutable", "Cardinal", "Fixed", "Mutable", "Cardinal", "Fixed", "Mutable", "Cardinal", "Fixed", "Mutable"]
SIGNS = []
SIGNS_HEADER = ["NUM", "SIGN", "LORD", "ELEMENT", "MODE"]
for i, (g, n, l, e, m) in enumerate(zip(SIGN_GLYPHS, SIGN_NAMES, SIGN_LORDS, SIGN_ELEMENTS, SIGN_MODES)):
    SIGNS.append(Sign(num=i+1, glyph=g, name=n, lord=l, element=e, mode=m))

NAKSHATRA_NAMES = ["Asvini", "Bharani", "Krttika", "Rohini", "Mrgasirsa", "Ardra", "Punarvasu", "Pusya", "Aslesa", "Magha", "Purvaphalguni", "Uttaraphalguni", "Hasta", "Citra", "Svati", "Visakha", "Anuradha", "Jyestha", "Mula", "Purvashadha", "Uttarashadha", "Sravana", "Dhanistha", "Satabhisak", "Purvabhadrapada", "Uttarabhadrapada", "Revati"]
NAKSHATRA_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
NAKSHATRA_DEITIES = ["Asvini Kumars", "Yama", "Agni", "Brahma/Prajapati", "Soma/Chandra", "Rudra", "Aditi", "Brihaspati", "Sarpas/Nagas", "Pitris/Manes", "Bhaga", "Aryaman", "Savitri", "Tvastar/Visvakarma", "Yavu", "Indra-Agni", "Mitra", "Indra", "Nirriti", "Apah", "Visvadeva", "Visnu", "Vasus", "Varuna", "Ajaikapada", "Ahirbudhanya", "Pushan"]
NAKSHATRA_SYMBOLS = ["Horse Head", "Yoni", "Razor", "Chariot/Temple/Banyan", "Deer Head", "Diamond/Tear/Human Head", "Bow & Quiver", "Udder/Lotus/Arrow", "Serpent", "Throne", "Bedhead/Fig Tree", "Foot of bed", "Hand/Palm", "Bright/Pearl", "Sapling/Corel", "Potter's wheel", "Lotus", "Earing/Amulet/Parasol", "Root/Goad", "Tusk/Fan/Winnowing basket", "Small cot", "Ear/Footprints", "Drum/Flute", "100 flowers or stars/Empty circle", "Sword/Front of coffin/Janus", "Twins/Front of coffin/Leviathan", "Fish"]
NAKSHATRAS = []
NAKSHATRAS_HEADER = ["NUM", "NAKSHATRA", "LORD", "DEITY", "SYMBOL"]
for i, (n, d, l, s) in enumerate(zip(NAKSHATRA_NAMES, NAKSHATRA_LORDS, NAKSHATRA_DEITIES, NAKSHATRA_SYMBOLS)):
    NAKSHATRAS.append(Nakshatra(num=i+1, name=n, lord=l, deity=d, symbol=s))

PLANET_NAMES_SOLAR = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
PLANET_GLYPHS_SOLAR = ["☼", "☾", "♂", "☿", "♃", "♀", "♄"]
PLANET_EXALTED = ["Aries", "Taurus", "Capricorn", "Virgo", "Cancer", "Pisces", "Libra"]
PLANET_DEBILITY = ["Libra", "Scorpio", "Cancer", "Pisces", "Capricorn", "Virgo", "Aries"]
WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
PLANETS_SOLAR = []
PLANETS_SOLAR_HEADER = ["NUM", "PLANET", "GLYPH", "EXALTATION", "DEBILITY", "WEEKDAY"]
for i, (n, g, e, d, w) in enumerate(zip(PLANET_NAMES_SOLAR, PLANET_GLYPHS_SOLAR, PLANET_EXALTED, PLANET_DEBILITY, WEEKDAYS)):
    PLANETS_SOLAR.append(PlanetSolar(num=i+1, name=n, glyph=g, exalted=e, debility=d, weekday=w))

PLANET_NAMES_LUNAR = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
PLANET_GLYPHS_LUNAR = ["☋", "♀", "☼", "☾", "♂", "☊", "♃", "♄", "☿"]
PLANET_DASAS = [7, 20, 6, 10, 7, 18, 16, 19, 17]
PLANETS_LUNAR = []
for i, (n, g, d) in enumerate(zip(PLANET_NAMES_LUNAR, PLANET_GLYPHS_LUNAR, PLANET_DASAS)):
    PLANETS_LUNAR.append(PlanetLunar(num=i+1, name=n, glyph=g, dasa=d))
DASAS = deque(PLANETS_LUNAR)

TITHI_NAMES = ["Sukla Pratipad", "Sukla Dvitiya", "Sukla Tritiya", "Sukla Caturthi", "Sukla Pancami", "Sukla Sasti", "Sukla Saptami", "Sukla Astami", "Sukla Navami", "Sukla Dasami", "Sukla Ekadasi", "Sukla Dvadasi", "Sukla Trayodasi", "Sukla Caturdasi", "Purnima", "Krsna Pratipad", "Krsna Dvitiya", "Krsna Tritiya", "Krsna Caturthi", "Krsna Pancami", "Krsna Sasti", "Krsna Saptami", "Krsna Astami", "Krsna Navami", "Krsna Dasami", "Krsna Ekadasi", "Krsna Dvadasi", "Krsna Trayodasi", "Krsna Caturdasi", "Amavasya"]
TITHI_OMENS = ["One giving rise", "Auspicious", "Strength and Power", "Negative", "Wealth", "Fame", "Friendly", "Conflict", "Aggressive", "Soft", "Happiness", "Fame", "Victory", "Aggressive", "Soft", "One giving rise", "Auspicious", "Strength and Power", "Negative", "Wealth", "Fame", "Friendly", "Conflict", "Aggressive", "Soft", "Happiness", "Fame", "Victory", "Aggressive", "Inauspicious"]
TITHI_DEITIES = ["Agni", "Asvini Kumar/Brahma", "Gauri", "Ganapati", "Naga", "Mangala", "Surya", "Siva/Matrgana", "Durga", "Yama/Diks", "Vayu/Kubera", "Visnu", "Kamadeva/Dharma", "Rudra", "Soma", "Agni", "Asvini Kumar/Brahma", "Gauri", "Ganapati", "Naga", "Mangala", "Surya", "Siva", "Durga", "Yama/Diks", "Vayu/Kubera", "Visnu", "Kamadeva/Dharma", "Rudra", "Pitris"]
TITHIS = []
TITHIS_HEADER = ["NUM", "NAME", "OMEN", "DEITY"]
for i, (n, o, d) in enumerate(zip(TITHI_NAMES, TITHI_OMENS, TITHI_DEITIES)):
    TITHIS.append(Tithi(num=i+1, name=n, omen=o, deity=d))

ANIMAL_NAMES = deque(["Rat", "Ox", "Tiger", "Hare", "Dragon", "Snake", "Horse", "Sheep", "Monkey", "Rooster", "Dog", "Pig"])
ANIMAL_TRAITS = ["Concealment", "Endurance", "Watchfulness", "Detachment", "Unpredictability", "Accumulation", "Decisiveness", "Propriety", "Irrepressibility", "Application", "Nobility", "Resignation"]
ANIMAL_SOULMATES = ["Ox", "Rat", "Pig", "Dog", "Rooster", "Monkey", "Sheep", "Horse", "Snake", "Dragon", "Rabbit", "Tiger"]
#ANIMAL_TRINE = Make a deque and rotate(4), rotate(-4)
ANIMAL_INKIND = ["Ox", "Rat", "Hare", "Tiger", "Snake", "Dragon", "Sheep", "Horse", "Rooster", "Monkey", "Pig", "Dog"]
#ANIMAL_KARMA = Make a deque and rotate(3), rotate(-3)
#ANIMAL_OPPOSITION = Make a deque and rotate(6)
ANIMAL_COMBAT = ["Sheep", "Horse", "Snake", "Dragon", "Hare", "Tiger", "Ox", "Rat", "Pig", "Dog", "Rooster", "Monkey"]
ANIMAL_PEACH = ["Rooster", "Horse", "Rabbit", "Rat", "Rooster", "Horse", "Rabbit", "Rat", "Rooster", "Horse", "Rabbit", "Rat"]
ANIMAL_STEED = ["Tiger", "Pig", "Monkey", "Snake", "Tiger", "Pig", "Monkey", "Snake", "Tiger", "Pig", "Monkey", "Snake"]
ANIMALS = []
ANIMALS_HEADER = ["NUM", "NAME", "TRAIT", "SOULMATE", "INKIND", "COMBAT", "PEACH", "STEED", "OPPOSITION", "TRINE, TRINE", "KARMA, KARMA"]
for i, (n, t, so, ik, c, p, st, o, tr, k) in enumerate(zip(ANIMAL_NAMES, ANIMAL_TRAITS, ANIMAL_SOULMATES, ANIMAL_INKIND, ANIMAL_COMBAT, ANIMAL_PEACH, ANIMAL_STEED, ANIMAL_NAMES, ANIMAL_NAMES, ANIMAL_NAMES)):
    ANIMALS.append(Animal(num=i+1, name=n, trait=t, soulmate=so, inkind=ik, combat=c, peach=p, steed=st, opposition=o, trine=tr, karma=k))

ANIMAL_EPHEMERIS = []

ZONES_todo = [(-12, ""), (-11.5, ""), (-11, ""), (-10.5, ""), (-10, ""), (-9.5, ""), (-9, ""), (-8.5, ""), (-8, "Western Pacific"), (-7.5, ""), (-7, "Edmonton"), (-6.5, ""), (-6, "Chicago, Texas, Guatamala, Mexico City"), (-5.5, ""), (-5, "Eastern Standard, Toronto, Cuba, Colombia"), (-4.5, ""), (-4, "Venezuela"), (-3.5, ""), (-3, "Rio de Janeiro"), (-2.5, ""), (-2, ""), (-1.5, ""), (-1, ""), (-0.5, ""), (0, "UK, Portugal"), (0.5, ""), (1, "Germany, Italy"), (1.5, ""), (2, "South Africa, Greece. Israel"), (2.5, ""), (3, "Moscow"), (3.5, ""), (4, ""), (4.5, ""), (5, ""), (5.5, "India, Sri Lanka"), (5.75, "Nepal"), (6, ""), (6.5, ""), (7, "Thailand"), (7.5, ""), (8, "China, Singapore, Taiwan, Malaysia"), (8.5, ""), (9, "Japan"), (9.5, "Adelaide"), (10, "Sydney"), (10.5, ""), (11, ""), (11.5, ""), (12, "Petropavlovsk-Kamchatsky")]

ZONES_ints = [-12 , -11.5 , -11 , -10.5 , -10 , -9.5 , -9 , -8.5 , -8 , -7.5 , -7 , -6.5 , -6 , -5.5 , -5 , -4.5 , -4 , -3.5 , -3 , -2.5 , -2 , -1.5 , -1 , -0.5 , 0 , 0.5 , 1 , 1.5 , 2 , 2.5 , 3 , 3.5 , 4 , 4.5 , 5 , 5.5 , 5.75 , 6 , 6.5 , 7 , 7.5 , 8 , 8.5 , 9 , 9.5 , 10 , 10.5 , 11 , 11.5 , 12]


ZONES = ["-12",  "-11.5",  "-11",  "-10.5",  "-10",  "-9.5",  "-9",  "-8.5",  "-8",  "-7.5",  "-7",  "-6.5",  "-6",  "-5.5",  "-5",  "-4.5",  "-4",  "-3.5",  "-3",  "-2.5",  "-2",  "-1.5",  "-1",  "-0.5",  "0",  "0.5",  "1",  "1.5",  "2",  "2.5",  "3",  "3.5",  "4",  "4.5",  "5",  "5.5",  "5.75",  "6",  "6.5",  "7",  "7.5",  "8",  "8.5",  "9",  "9.5",  "10",  "10.5",  "11",  "11.5",  "12"]



PLANETS_DICT = {"Sun":0, "Moon":1, "Mercury":2, "Venus":3, "Mars":4, "Jupiter":5, "Saturn":6}

births = []

NAKSHATRA_DEITIES_LURKER = ["Pūṣan (‘the prosperer’) Old Indian god, who is described as radiant and toothless. He is married to the sun-maiden, and confers growth and prosperity through light. He watches over roads, protects travellers and guides the dead. His car is drawn by goats."]



















