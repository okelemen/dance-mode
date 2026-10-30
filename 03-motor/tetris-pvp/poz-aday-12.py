"""HUMAN TETRIS 12. video (REF-063 HumanWarmUp, 1 oyuncu, ~5 dk) - poz ADAY havuzu -> pozlar-12-aday.json.
Maskeler Actions'ta (tetris-varlik.yml, yalniz=poz, pozlar=03-motor/tetris-pvp/pozlar-12-aday.json), sonra poz-sec-12.py secer.

    python poz-aday-12.py

REF-063 dili: yana esneme hamlesi, savasci, yuksek yan tekme, cok genis durus, yere inen hamleler. Tam kopru alinmaz (TALIMATLAR §4).
Gruplar: 1 ayakta, 2 hamle/tek ayak/tekme, 3 yer. Adlar defterdeki hicbir pozla cakismaz (assert).
"""
import json, os, random

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]
rnd = random.Random(63)

EL = {1: [], 2: [], 3: []}


def el(tur, p):
    p["ad"] = "Solo " + p["ad"]
    EL[tur].append(p)


# ---- GRUP 1: ayakta
el(1, on("Neon Side Bend Over", [-150, -135], "hip", "wide", "wide", govde=205))
el(1, on("Arc Reach Wide", [-140, -170], [-20, -40], "goddess", "goddess", govde=195))
el(1, on("Goal Post Lean", "cactus", "cactus", "wide", "wide", govde=188))
el(1, on("Star Tilt", "t", "up45", "wide", "wide", govde=172))
el(1, on("Sky Punch Horse", [-170, -170], "chest", "horse", "horse"))
el(1, on("Elbow Out Squat", "head", "head", "horse", "horse"))
el(1, on("Flex Goddess", "flex", "flex", "goddess", "goddess"))
el(1, on("Low Arms Wide Tap", "lowv", "t", "sidetap", "tog", govde=184))
el(1, on("Diagonal Line Stretch", "up45", "lowv", "straight", "tog", govde=194))
el(1, on("Comet Arm Tip Toe", [-115, -165], [-70, -20], "tog", "sidetap"))
el(1, on("Hug Arms Wide Knees", [-40, 110], [-40, 110], "goddess", "goddess"))
el(1, profil("Forward Fold Half Reach", 118, [100, 100], [98, 98], [8, 8], [-8, -8]))
el(1, profil("Lean Back Arms Up", 198, [170, 170], [168, 168], [10, 10], [-10, -10]))
el(1, on("W Arms Wide Stance", "w", "w", "wide", "wide", govde=180))
el(1, on("Halo Side Tap", [-160, 120], "hip", "sidetap", "tog"))
el(1, on("V Arm Lean Goddess", "v", "lowv", "goddess", "goddess", govde=170))
# ---- GRUP 2: hamle, tek ayak, tekme
el(2, on("High Side Kick T", "t", "t", "tog", [100, 100], govde=150))
el(2, on("Low Side Kick Arms Up", "up", "up", "tog", [55, 55], govde=170))
el(2, on("Side Bend Lunge Arm Over", [-145, -130], [-60, -60], "lunge", "straight", govde=205))
el(2, on("Reverse Warrior Reach", "up", "lowv", "lunge", "straight", govde=195))
el(2, on("Warrior Cactus", "cactus", "cactus", "lunge", "straight"))
el(2, on("Lunge Flex Double", "flex", "flex", "lunge", "straight"))
el(2, on("Lunge Hands Head", "head", "head", "lunge", "straight"))
el(2, on("Knee Up T Arms", "t", "t", "tog", "kneeup"))
el(2, on("Tree Hands Head", "head", "head", "tog", "kneein"))
el(2, on("Tree Wide V", "v", "v", "tog", "kneein"))
el(2, profil("Airplane Arms Wide", 100, [90, 90], [-90, -90], [0, 0], [-75, -75]))
el(2, profil("Skater Reach", 130, [130, 130], [-40, -40], [60, -20], [-50, -80]))
el(2, profil("Front Kick Low Arms Back", 175, [-40, -40], [-38, -38], [65, 65], [0, 0]))
el(2, profil("Runner Lunge Arm Up", 150, [170, 170], [40, 40], [100, -5], [-55, -55]))
el(2, profil("Pyramid Reach", 105, [160, 160], [158, 158], [25, 25], [-30, -30]))
el(2, profil("Back Leg Lift Reach", 140, [150, 150], [150, 150], [0, 0], [-40, -40]))
# ---- GRUP 3: yer (el / diz / ayak acikca yerde)
el(3, profil("Three Leg Plank", 92, [0, 0], [0, 0], [-86, -86], [-65, -65]))
el(3, profil("Wide Plank Arm Forward", 95, [85, 85], [0, 0], [-82, -82], [-88, -88]))
el(3, profil("Kneeling Upright Arms Wide", 180, [90, 90], [-90, -90], [0, -90], [0, -90]))
el(3, profil("Kneeling Side Lean", 195, [175, 175], [-30, -30], [0, -90], [0, -90]))
el(3, profil("Half Kneel Forward Reach", 170, [90, 90], [88, 88], [95, 0], [0, -90]))
el(3, profil("Half Kneel Twist Back", 175, [-50, -50], [95, 95], [95, 0], [0, -90]))
el(3, profil("Crawl Knee Forward", 100, [0, 0], [0, 0], [100, -90], [-70, -70]))
el(3, profil("Spider Lunge Arm Up", 110, [0, 0], [150, 150], [110, -80], [-70, -70]))
el(3, profil("Seated Wide Lean Reach", 165, [100, 100], [98, 98], [85, 85], [83, 83]))
el(3, profil("Seated Arms Back Legs Long", 215, [-150, -150], [-148, -148], [80, 80], [78, 78]))
el(3, profil("Seated Knees Up Arms Forward", 195, [90, 90], [88, 88], [120, 20], [118, 18]))
el(3, profil("Tall Sit Heels Arm Up", 180, [175, 175], [-20, -20], [0, -150], [0, -150]))
el(3, profil("Reverse Tabletop Lift", 250, [-170, -170], [-168, -168], [95, -90], [93, -92]))
el(3, profil("Hands Feet Pike Low", 45, [50, 50], [48, 48], [-30, -30], [-32, -32]))
el(3, profil("Lizard Hold", 105, [5, 5], [3, 3], [115, -95], [-72, -72]))
el(3, profil("Gate Kneel Leg Side", 180, [170, 170], [-30, -30], [0, -90], [70, 70]))

KOL = {"V": "v", "W": "w", "Cactus": "cactus", "Reach": "up", "T": "t", "Head": "head", "Flex": "flex", "Low": "lowv",
       "Hip": "hip", "Diag": "up45", "Halo": [-160, 120], "Comet": [-110, -170], "Wave": [-70, -130], "Hug": [-40, 100]}
BAC = {"Wide": ("wide", "wide"), "Horse": ("horse", "horse"), "Knee": ("tog", "kneeup"), "Tree": ("tog", "kneein"),
       "Leg Out": ("straight", "tog"), "Kick": ("tog", [60, 60]), "Lunge": ("lunge", "straight"), "Tap": ("sidetap", "tog")}
KELIME = ["Bridge", "Laser", "Pink", "Chevron", "Truss", "Solo", "Night", "Strobe", "Runner", "Beam",
          "Rail", "Neon", "Step", "Violet", "Magenta", "Shine", "Ray", "Vivid", "Charge", "Dash"]
HAVUZ, adlar = [], set()


def ekle(tur, p):
    k = p["ad"].lower()
    if k not in adlar:
        adlar.add(k); p["tur"] = tur; HAVUZ.append(p)


kk, bb = list(KOL), list(BAC)
while len(HAVUZ) < 90:
    a, b, c = rnd.choice(kk), rnd.choice(kk), rnd.choice(bb)
    if a == b:
        continue
    p = on(f"{rnd.choice(KELIME)} {a} {b} {c}", KOL[a], KOL[b], BAC[c][0], BAC[c][1], govde=rnd.choice([160, 168, 176, 184, 192, 200]))
    ekle(1 if c in ("Wide", "Horse", "Tap", "Leg Out") else 2, p)

eski = set()
for f in ("pozlar.json", "pozlar-03.json", "pozlar-04.json", "pozlar-05.json", "pozlar-05-aday.json", "pozlar-06.json", "pozlar-06-aday.json",
          "pozlar-08.json", "pozlar-08-aday.json", "pozlar-09.json", "pozlar-09-aday.json", "pozlar-10.json", "pozlar-10-aday.json"):
    yol = os.path.join(BURA, f)
    if os.path.exists(yol):
        eski |= {p["ad"].lower() for p in json.load(open(yol, encoding="utf-8"))["pozlar"].values()}
_kul = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("KULLANILMIS = ")[1].split("}")[0] + "}"
eski |= eval(_kul)

pozlar = {}
for tur, liste in EL.items():
    for p in liste:
        p["tur"] = tur; p["el"] = True
for p in [x for l in EL.values() for x in l] + HAVUZ:
    assert p["ad"].lower() not in eski, p["ad"]
    k = p["ad"].lower().replace(" ", "-").replace("'", "")
    assert k not in pozlar, k
    pozlar[k] = p
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "12. video ADAY (REF-063)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-12-aday.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(pozlar)} aday (el {sum(len(l) for l in EL.values())}: " + ", ".join(f"tur{t} {len(l)}" for t, l in EL.items()) + f"; havuz {len(HAVUZ)})")
