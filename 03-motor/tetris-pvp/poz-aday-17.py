"""HUMAN TETRIS 17. video (REF-068 TetrisBounce, SOLO, ~5 dk) - poz ADAY havuzu -> pozlar-17-aday.json.
Maskeler Actions'ta (tetris-varlik.yml, yalniz=poz, pozlar=03-motor/tetris-pvp/pozlar-17-aday.json, ek=--mod galaksi), sonra secim.

    python poz-aday-17.py

REF-068 dili: yoga / jimnastik, 3 level. EASY ayakta (agac, kollar, genis durus), NORMAL hamle / savasci / tek ayak denge,
HARD yer (diz, oturma, kobra benzeri yer pozlari) + zor denge. Kullanici karari (3 Kas 2026): ters poz YOK (amut, bas ustu),
ziplama yok, hepsi yere basar. Tek oyuncu: her duvar bir poz, 24 duvar. Adlar defterdeki hicbir pozla cakismaz (assert).
"""
import json, os, random

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]
rnd = random.Random(68)

EL = {1: [], 2: [], 3: []}


def el(tur, p):
    p["ad"] = "Nebula " + p["ad"]
    EL[tur].append(p)


# ---- LEVEL 1 EASY: ayakta, iki ayak yerde ya da hafif tek ayak (agac)
el(1, on("Tree Hands Sky", "up", "up", "tog", "kneein"))
el(1, on("Tree Hands Chest", "chest", "chest", "tog", "kneein"))
el(1, on("Mountain Arms V", "v", "v", "tog", "tog"))
el(1, on("Crescent Lean Left", "up", "up", "tog", "tog", govde=160))
el(1, on("Crescent Lean Right", "up", "up", "tog", "tog", govde=200))
el(1, on("Wide Stand Arms Low V", "lowv", "lowv", "wide", "wide"))
el(1, on("Wide Stand Cactus", "cactus", "cactus", "wide", "wide"))
el(1, on("Star Arms Diagonal", "up45", "lowv", "straight", "straight", govde=184))
el(1, on("Side Bend Arm Over Wide", [-150, -125], "hip", "wide", "wide", govde=196))
el(1, on("Hands Behind Head Wide", "head", "head", "wide", "wide"))
el(1, on("Toe Tap Side Reach", [-120, -130], "down", "sidetap", "tog", govde=188))
el(1, on("Eagle Arms Tall", [-60, 120], [-60, 120], "tog", "tog"))
el(1, on("Goal Post Arms Tall", [-90, -178], [-90, -178], "tog", "tog"))
el(1, on("One Arm Sky One Hip", "up", "hip", "wide", "wide"))
el(1, on("Half Moon Stand Left", [-170, -150], [-170, -150], "wide", "wide", govde=150))
el(1, profil("Forward Fold Half", 120, [90, 90], [88, 88], [0, 0], [-2, -2]))
el(1, profil("Standing Reach Back", 195, [175, 175], [173, 173], [2, 2], [-2, -2]))
# ---- LEVEL 2 NORMAL: hamle, savasci, tek ayak denge, comelme
el(2, on("Warrior Two Wide", "t", "t", "lunge", "straight"))
el(2, on("Reverse Warrior Reach", [-160, -140], [-20, 10], "lunge", "straight", govde=200))
el(2, on("Goddess Cactus Low", "cactus", "cactus", "goddess", "goddess"))
el(2, on("Goddess Prayer", "chest", "chest", "goddess", "goddess"))
el(2, on("Side Lunge Prayer", "chest", "chest", "lunge", "straight", govde=176))
el(2, on("Standing Split Side", "up45", "down", "tog", [75, 75], govde=150))
el(2, on("Knee Up Arms Sky", "up", "up", "tog", "kneeup"))
el(2, on("Knee Up Eagle Arms", [-60, 120], [-60, 120], "tog", "kneeup"))
el(2, on("Curtsy Arms V", "v", "v", "curtsy", "tog"))
el(2, on("Chair Twist Arms", "up45", "lowv", "softknee", "softknee", govde=188))
el(2, on("Low Squat Prayer", "chest", "chest", [-78, 22], [-78, 22]))
el(2, profil("Warrior One Sky", 178, [172, 172], [170, 170], [70, -70], [-40, -40]))
el(2, profil("Warrior Three Low", 102, [80, 80], [78, 78], [0, 0], [-70, -70]))
el(2, profil("Airplane Wings", 108, [100, 100], [-100, -100], [0, 0], [-75, -75]))
el(2, profil("Lunge Arms Back Wings", 160, [-40, -40], [-60, -60], [72, -72], [-42, -42]))
el(2, profil("Pyramid Reach Down", 110, [30, 30], [28, 28], [25, 25], [-25, -25]))
el(2, profil("Chair Arms Forward", 160, [90, 90], [88, 88], [75, -55], [73, -57]))
el(2, profil("Standing Knee Hug", 178, [40, 120], [38, 120], [85, -85], [-2, -2]))
# ---- LEVEL 3 HARD: yer pozlari (diz, oturma, el yerde) + zor denge; ters poz yok
el(3, profil("Cobra Low", 245, [-30, -30], [-28, -28], [-88, -90], [-88, -90]))
el(3, profil("Low Lunge Sky", 175, [170, 170], [168, 168], [88, -5], [0, -90]))
el(3, profil("Low Lunge Twist Open", 180, [130, 130], [-110, -110], [88, -5], [0, -90]))
el(3, profil("Pigeon Rise", 195, [175, 175], [173, 173], [60, -150], [-88, -90]))
el(3, profil("Camel Hands Back", 210, [-150, -150], [-148, -148], [0, -90], [0, -90]))
el(3, profil("Seated Forward Reach", 120, [85, 85], [83, 83], [88, 88], [86, 86]))
el(3, profil("Seated Boat Arms", 210, [95, 95], [93, 93], [130, 130], [128, 128]))
el(3, profil("Table Top Leg Back", 92, [90, 90], [0, 0], [-85, -88], [-90, -90]))
el(3, profil("Bird Dog Reach", 92, [90, 90], [0, 0], [-88, -90], [-90, -90]))
el(3, profil("Kneeling Side Arch", 200, [-160, -160], [20, 20], [0, -90], [0, -90]))
el(3, on("Lotus Prayer Sit", "chest", "chest", [-80, 120], [-80, 120]))
el(3, on("Lotus Arms Sky", "up", "up", [-80, 120], [-80, 120]))
el(3, on("Butterfly Sit Wings", "t", "t", [-75, 135], [-75, 135]))
el(3, on("Kneel Gate Reach", [-155, -130], "hip", [-20, -90], [48, 48], govde=214))
el(3, on("Kneel Arms V Tall", "v", "v", [-22, -90], [-22, -90]))
el(3, on("Wide Seat Arms Up", "up", "up", [-70, -70], [-70, -70]))
el(3, on("Frog Hands Down", [-10, -4], [-10, -4], [-82, 26], [-82, 26]))
el(3, on("Dancer Side Reach", "up45", "down", "tog", [60, 140], govde=160))
el(3, on("Standing Split Wide Arms", "t", "t", "tog", [88, 88], govde=146))
el(3, on("Tree Arms Wide Low", "lowv", "lowv", "tog", "kneein", govde=176))
el(3, on("Side Lunge Deep Twist", "up45", "lowv", "lunge", "straight", govde=166))
el(3, profil("Dancer Long Reach", 145, [150, 150], [-40, -120], [0, 0], [-60, -130]))
el(3, profil("Half Moon Side Hand", 100, [-170, -170], [10, 10], [0, 0], [-88, -88]))

KOL = {"V": "v", "W": "w", "Cactus": "cactus", "Reach": "up", "T": "t", "Head": "head", "Low": "lowv", "Hip": "hip",
       "Diag": "up45", "Halo": [-160, 120], "Eagle": [-60, 120], "Chest": "chest", "Goal": [-90, -178]}
BAC = {"Wide": ("wide", "wide"), "Horse": ("horse", "horse"), "Goddess": ("goddess", "goddess"), "Knee": ("tog", "kneeup"),
       "Tree": ("tog", "kneein"), "Lunge": ("lunge", "straight"), "Tap": ("sidetap", "tog"), "Curtsy": ("curtsy", "tog"),
       "Split": ("tog", [72, 72])}
KELIME = ["Nebula", "Galaxy", "Star", "Comet", "Orbit", "Neon", "Grid", "Cosmic", "Nova", "Astro", "Laser", "Pulse",
          "Synth", "Retro", "Meteor", "Stellar", "Lunar", "Solar", "Vapor", "Prism"]
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
    p = on(f"{rnd.choice(KELIME)} {a} {b} {c}", KOL[a], KOL[b], BAC[c][0], BAC[c][1], govde=rnd.choice([164, 172, 180, 188, 196]))
    ekle(1 if c in ("Wide", "Horse", "Tap") else 2 if c in ("Goddess", "Lunge", "Curtsy", "Knee") else 3, p)

eski = set()
for f in sorted(os.listdir(BURA)):
    if f.startswith("pozlar") and f.endswith(".json") and not f.startswith("pozlar-17"):
        eski |= {p["ad"].lower() for p in json.load(open(os.path.join(BURA, f), encoding="utf-8"))["pozlar"].values()}
_kul = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("KULLANILMIS = ")[1].split("}")[0] + "}"
eski |= eval(_kul)
DEFTER = os.path.join(os.path.expanduser("~"), "OneDrive", "Masaüstü", "POZ-DUVARI", "poz-defteri.md")   # yerelde calisir
_def = open(DEFTER, encoding="utf-8").read().lower() if os.path.exists(DEFTER) else ""

pozlar = {}
for tur, liste in EL.items():
    for p in liste:
        p["tur"] = tur; p["el"] = True
for p in [x for l in EL.values() for x in l] + HAVUZ:
    assert p["ad"].lower() not in eski, p["ad"]
    assert not _def or p["ad"].lower() not in _def, "defterde var: " + p["ad"]
    k = p["ad"].lower().replace(" ", "-").replace("'", "")
    assert k not in pozlar, k
    pozlar[k] = p
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "17. video ADAY (REF-068)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-17-aday.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(pozlar)} aday (el {sum(len(l) for l in EL.values())}: " + ", ".join(f"level{t} {len(l)}" for t, l in EL.items()) + f"; havuz {len(HAVUZ)}); defter {'okundu' if _def else 'YOK'}")
