"""HUMAN TETRIS 14. video (REF-065 HumanWarmUp, 1v1, ~5 dk) - poz ADAY havuzu -> pozlar-14-aday.json.
Maskeler Actions'ta (tetris-varlik.yml, yalniz=poz, pozlar=03-motor/tetris-pvp/pozlar-14-aday.json), sonra poz-sec-14.py secer.

    python poz-aday-14.py

REF-065 dili: yoga + bale: yildiz, ucgen, arabesk, yan tekme, savasci, deve. Tam kopru alinmaz (TALIMATLAR §4).
Gruplar: 1 ayakta, 2 hamle/tek ayak/tekme, 3 yer. Adlar defterdeki hicbir pozla cakismaz (assert).
"""
import json, os, random

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]
rnd = random.Random(65)

EL = {1: [], 2: [], 3: []}


def el(tur, p):
    p["ad"] = "Duel " + p["ad"]
    EL[tur].append(p)


# ---- GRUP 1: ayakta (REF-065: yildiz, ucgen, yana uzanma, dansci kol)
el(1, on("Ribbon Side Reach", [-150, -140], "hip", "wide", "wide", govde=208))
el(1, on("Grand Star Lift", "up45", "up45", "wide", "wide", govde=180))
el(1, on("Crown Arms Plie", [-150, 150], [-150, 150], "goddess", "goddess"))
el(1, on("Sword Arm Open Stance", "up", "t", "wide", "wide", govde=176))
el(1, on("Ballet Fifth Tall", [-165, 165], [-165, 165], "tog", "tog"))
el(1, on("Archway Lean Right", [-160, -150], [-150, -130], "wide", "wide", govde=200))
el(1, on("Triangle Sky Reach", "up", "down", "wide", "wide", govde=232))
el(1, on("Trophy Lift Horse", [-150, -165], [-150, -165], "horse", "horse"))
el(1, on("Duel Guard Stance", [-40, 130], [-70, 110], "horse", "horse"))
el(1, on("Victory Fist Wide", "v", "hip", "wide", "wide", govde=186))
el(1, on("Propeller Arms Tap", "up45", "lowv", "sidetap", "tog", govde=176))
el(1, on("Bow Pull Stance", [-90, -90], [-90, 170], "wide", "wide"))
el(1, on("Sun Salute Open", [-140, -170], [-140, -170], "wide", "wide", govde=172))
el(1, on("Soft Knee Wing Beat", [-70, -130], [-70, -130], "softknee", "softknee"))
el(1, on("Side Tap Low Scoop", [-20, 40], "up45", "sidetap", "tog", govde=188))
el(1, on("Plie Elbows Low", "elbowdown", "elbowdown", "goddess", "goddess"))
el(1, on("Tilted Y Tiptoe", "v", "v", "tog", "tog", govde=196))
el(1, on("Reach Over Plie", [-140, -125], [-30, 40], "goddess", "goddess", govde=204))
el(1, profil("Half Bow Forward", 125, [110, 110], [-40, -40], [6, 6], [-6, -6]))
el(1, profil("Chest Lift Arms Back", 192, [-45, -45], [-42, -42], [6, 6], [-6, -6]))
el(1, profil("Long Stride Arms Forward", 180, [90, 90], [88, 88], [30, 30], [-30, -30]))
el(1, profil("Stride Back Arm Sky", 185, [170, 170], [-50, -50], [28, 28], [-32, -32]))
el(1, profil("Deep Bow Stride", 115, [100, 100], [98, 98], [25, 25], [-25, -25]))
el(1, profil("Lantern Reach Stride", 170, [150, 150], [-60, -60], [32, 20], [-28, -28]))
# ---- GRUP 2: hamle, tek ayak, tekme (REF-065: arabesk, yan tekme, savasci)
el(2, profil("Arabesque Long Line", 125, [120, 120], [-40, -40], [0, 0], [-70, -70]))
el(2, profil("Arabesque Arm High", 140, [160, 160], [150, 150], [0, 0], [-55, -55]))
el(2, profil("Attitude Back Knee", 160, [165, 150], [-70, -70], [0, 0], [-40, -95]))
el(2, profil("Scale Forward Palms", 95, [85, 85], [83, 83], [0, 0], [-80, -80]))
el(2, profil("Front Kick Reach Toes", 170, [80, 80], [78, 78], [70, 70], [0, 0]))
el(2, profil("Knee Lift Arms Crown", 180, [170, 150], [168, 148], [85, -80], [0, 0]))
el(2, profil("Warrior Two Hands Sky", 175, [175, 175], [172, 172], [70, -70], [-40, -40]))
el(2, profil("Warrior Arms Spread", 178, [90, 90], [-90, -90], [72, -72], [-42, -42]))
el(2, profil("Deep Lunge Palms Forward", 130, [95, 95], [93, 93], [85, -85], [-50, -50]))
el(2, profil("Lunge Twist Arm Back", 155, [100, 100], [-110, -110], [80, -80], [-48, -48]))
el(2, on("Side Kick Blade Arms", "up45", "lowv", "tog", [85, 85], govde=158))
el(2, on("Low Kick Guard Fists", [-40, 130], [-40, 130], "tog", [50, 50], govde=172))
el(2, on("Tall Kick Sky Arm", "up", "t", "tog", [70, 70], govde=160))
el(2, on("Side Lunge Hands Ground", [-5, -5], "t", "lunge", "straight", govde=168))
el(2, on("Side Lunge Cross Reach", [-150, -135], "lowv", "lunge", "straight", govde=212))
el(2, on("Lunge Diagonal Bolt", "up45", "lowv", "lunge", "straight", govde=196))
el(2, on("Lunge Crown Hands", [-150, 150], [-150, 150], "lunge", "straight"))
el(2, on("Tree Sky Palms", "up", "up", "tog", "kneein"))
el(2, on("Tree Open Wing", "t", "t", "tog", "kneein", govde=174))
el(2, on("Stork Knee Fist Pump", [-160, -170], "hip", "tog", "kneeup"))
el(2, on("Knee Lift Twin Flex", "flex", "flex", "tog", "kneeup", govde=176))
el(2, on("Skater Leg Behind Reach", "t", "lowv", "curtsy", "tog", govde=186))
el(2, on("Curtsy Crown", [-150, 150], [-150, 150], "curtsy", "tog"))
el(2, on("Wide Side Bend Hook", [-150, -120], [-30, 120], "lunge", "straight", govde=216))
# ---- GRUP 3: yer (REF-065: deve, diz; el / diz / ayak acikca yerde)
el(3, profil("Camel Reach Heels", 215, [-120, -120], [-118, -118], [0, -90], [0, -90]))
el(3, profil("Kneel Arms Sky Tall", 180, [175, 175], [172, 172], [0, -90], [0, -90]))
el(3, profil("Kneel Bow Forward", 125, [100, 100], [98, 98], [0, -90], [0, -90]))
el(3, profil("Half Kneel Sky Reach", 182, [172, 172], [-40, -40], [92, -2], [0, -90]))
el(3, profil("Half Kneel Arms Wide", 178, [90, 90], [-90, -90], [90, 0], [0, -90]))
el(3, profil("Low Lunge Back Knee", 165, [160, 160], [158, 158], [100, -90], [-20, -80]))
el(3, profil("Tabletop Arm Reach", 92, [90, 90], [0, 0], [-86, -86], [-82, -82]))
el(3, profil("Tabletop Leg Back", 92, [0, 0], [0, 0], [-85, -85], [-20, -20]))
el(3, profil("Bird Dog Long", 94, [88, 88], [0, 0], [-85, -85], [-5, -5]))
el(3, profil("Mountain Pike High", 55, [55, 55], [53, 53], [-30, -30], [-28, -28]))
el(3, profil("Plank Tall Hands", 96, [2, 2], [0, 0], [-80, -80], [-78, -78]))
el(3, profil("Squat Palms Floor", 120, [10, 10], [8, 8], [120, -120], [118, -118]))
el(3, profil("Crouch Arms Forward", 150, [90, 90], [88, 88], [115, -115], [113, -113]))
el(3, profil("Runner Fingertips", 125, [8, 8], [5, 5], [105, -85], [-62, -62]))
el(3, profil("Seated Fold Reach Toes", 130, [95, 95], [93, 93], [85, 85], [83, 83]))
el(3, on("Wide Kneel Goal Post", "cactus", "cactus", [-25, -90], [-25, -90]))
el(3, on("Kneel Side Bend Arc", [-150, -135], "hip", [-15, -90], [-15, -90], govde=204))
el(3, on("Kneel Star Arms", "v", "v", [-20, -90], [-20, -90]))

# kontak 1 (1 Kas 2026): grup 3 eledikten sonra yetmedi -> diz yere net basan yeni adaylar
el(3, on("Kneel T Wings", "t", "t", [-15, -90], [-15, -90]))
el(3, on("Kneel Hands Behind Head", "head", "head", [-22, -90], [-22, -90]))
el(3, on("Kneel Twin Flex", "flex", "flex", [-18, -90], [-18, -90]))
el(3, on("Kneel Diagonal Bolt", "up45", "lowv", [-20, -90], [-20, -90], govde=188))
el(3, on("Kneel Crown Hands", [-150, 150], [-150, 150], [-12, -90], [-12, -90]))
el(3, on("Kneel Sword Arm", "up", "t", [-22, -90], [-22, -90], govde=176))
el(3, on("Kneel Low V Open", "lowv", "lowv", [-28, -90], [-28, -90]))
el(3, profil("Half Kneel Bow", 140, [100, 100], [98, 98], [92, -2], [0, -90]))
el(3, profil("Half Kneel Arms Back", 190, [-40, -40], [-38, -38], [92, -2], [0, -90]))
el(3, profil("Kneel Arms Forward", 180, [90, 90], [88, 88], [0, -90], [0, -90]))
el(3, profil("Kneel Lean Back Open", 200, [150, 150], [-40, -40], [0, -90], [0, -90]))

KOL = {"V": "v", "W": "w", "Cactus": "cactus", "Reach": "up", "T": "t", "Head": "head", "Flex": "flex", "Low": "lowv",
       "Hip": "hip", "Diag": "up45", "Halo": [-160, 120], "Comet": [-110, -170], "Wave": [-70, -130], "Hug": [-40, 100]}
BAC = {"Wide": ("wide", "wide"), "Horse": ("horse", "horse"), "Knee": ("tog", "kneeup"), "Tree": ("tog", "kneein"),
       "Leg Out": ("straight", "tog"), "Kick": ("tog", [60, 60]), "Lunge": ("lunge", "straight"), "Tap": ("sidetap", "tog")}
KELIME = ["Golden", "Amber", "Rival", "Chevron", "Truss", "Duel", "Arena", "Blaze", "Crown", "Beam",
          "Rail", "Glow", "Clash", "Ember", "Copper", "Flare", "Ray", "Bold", "Charge", "Strike"]
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
          "pozlar-08.json", "pozlar-08-aday.json", "pozlar-09.json", "pozlar-09-aday.json", "pozlar-10.json", "pozlar-10-aday.json", "pozlar-12.json", "pozlar-12-aday.json"):
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
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "14. video ADAY (REF-065)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-14-aday.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(pozlar)} aday (el {sum(len(l) for l in EL.values())}: " + ", ".join(f"tur{t} {len(l)}" for t, l in EL.items()) + f"; havuz {len(HAVUZ)})")
