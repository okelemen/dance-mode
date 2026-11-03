"""HUMAN TETRIS 16. video (REF-067 TetrisBounce, 1v1, ~4:40) - poz ADAY havuzu -> pozlar-16-aday.json.
Maskeler Actions'ta (tetris-varlik.yml, yalniz=poz, pozlar=03-motor/tetris-pvp/pozlar-16-aday.json, ek=--mod sakura), sonra poz-sec-16.py secer.

    python poz-aday-16.py

REF-067 dili: 3 tur kolaydan zora. ROUND 1 ayakta (kol + genis durus, el belde, isaret), ROUND 2 MEDIUM comelme / hamle / tek ayak,
ROUND 3 HARD yer (diz, cocuk pozu, oturma) + zor denge. Her oyuncunun pozu ayri. Kapakta onaylanan 4 poz (pozlar-16-kapak.json) zorunlu.
Adlar defterdeki hicbir pozla cakismaz (assert).
"""
import json, os, random

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]
rnd = random.Random(67)

EL = {1: [], 2: [], 3: []}


def el(tur, p):
    p["ad"] = "Sakura " + p["ad"]
    EL[tur].append(p)


# ---- GRUP 1 (ROUND 1 EASY): ayakta, iki ayak yerde
el(1, on("Hands On Hips Tall", "hip", "hip", "wide", "wide"))
el(1, on("One Point Up Hip", [-160, -168], "hip", "tog", "tog", govde=178))
el(1, on("Shrug Palms Up", [-40, -95], [-40, -95], "tog", "tog"))
el(1, on("Wave Hello Wide", [-150, 170], "down", "wide", "wide"))
el(1, on("Muscle Pose Horse", "flex", "flex", "horse", "horse"))
el(1, on("Lean Left Arch", [-165, -150], [-165, -150], "wide", "wide", govde=158))
el(1, on("Lean Right Arch", [-150, -135], [-150, -135], "wide", "wide", govde=202))
el(1, on("Diagonal Dash Arms", "up45", "lowv", "wide", "wide", govde=184))
el(1, on("Elbows Out Head", "head", "head", "horse", "horse"))
el(1, on("Cross Arms Chest", "chest", "chest", "wide", "wide"))
el(1, on("Robot Arms Square", [-90, -180], [-90, 0], "wide", "wide"))
el(1, on("Pointing Forward Low", [-70, -70], "hip", "sidetap", "tog", govde=176))
el(1, on("Sky Clap Narrow", [-172, -178], [-172, -178], "tog", "tog"))
el(1, on("Penguin Arms Tiptoe", [-22, -22], [-22, -22], "tog", "tog"))
el(1, on("Side Reach Hip Lean", [-125, -135], "hip", "wide", "wide", govde=196))
el(1, on("Half W Half Down", "w", "down", "wide", "wide"))
el(1, on("Big Hug Open", [-60, 70], [-60, 70], "horse", "horse"))
el(1, on("Lasso Spin High", [-170, 120], "hip", "wide", "wide", govde=176))
el(1, profil("Bow Hello Forward", 140, [60, 60], [-10, -10], [4, 4], [-4, -4]))
el(1, profil("Stride Arms Swing", 182, [60, 60], [-60, -60], [24, 24], [-24, -24]))
# ---- GRUP 2 (ROUND 2 MEDIUM): comelme, hamle, tek ayak, tekme
el(2, on("Squat Prayer Hands", [-30, 100], [-30, 100], "goddess", "goddess"))
el(2, on("Sumo Arms Up", "up", "up", "goddess", "goddess"))
el(2, on("Low Squat Cactus", "cactus", "cactus", [-70, 10], [-70, 10]))
el(2, on("Side Lunge T Arms", "t", "t", "lunge", "straight"))
el(2, on("Side Lunge Sky Reach", "up", "hip", "straight", "lunge", govde=190))
el(2, on("Knee Up Hands Clap", [-30, 110], [-30, 110], "tog", "kneeup"))
el(2, on("Flamingo Wings", "t", "t", "tog", [-80, 60], govde=178))
el(2, on("Side Kick Hip Hand", "hip", "up45", "tog", [70, 70], govde=162))
el(2, on("Curtsy V Arms", "v", "v", "curtsy", "tog"))
el(2, on("Tree Prayer Tall", [-172, 178], [-172, 178], "tog", "kneein"))
el(2, on("Low Kick Arms Wide", "t", "lowv", "tog", [40, 40], govde=174))
el(2, on("Skater Reach Down", [-20, -10], "t", "curtsy", "tog", govde=170))
el(2, profil("Warrior Three Arms Back", 100, [-20, -20], [-18, -18], [0, 0], [-78, -78]))
el(2, profil("High Knee Run Arms", 185, [80, 140], [-50, -50], [90, 0], [-8, -8]))
el(2, profil("Lunge Prayer Twist", 175, [40, 140], [38, 140], [70, -70], [-45, -45]))
el(2, profil("Lunge Reach Forward", 150, [110, 110], [-60, -60], [75, -75], [-40, -40]))
el(2, profil("Arabesque Low Wings", 120, [80, 80], [-80, -80], [0, 0], [-50, -50]))
el(2, profil("Chair Pose Arms Up", 165, [165, 165], [163, 163], [80, -60], [78, -62]))
# ---- GRUP 3 (ROUND 3 HARD): yer (diz, el, kalca net yerde) + zor denge
el(3, profil("Child Pose Long", 70, [60, 60], [58, 58], [0, -90], [0, -90]))
el(3, profil("Kneel Lean Back Hands", 205, [-150, -150], [-148, -148], [0, -90], [0, -90]))
el(3, profil("Half Kneel Prayer", 180, [40, 140], [38, 140], [92, -2], [0, -90]))
el(3, profil("Half Kneel Point Forward", 170, [95, 95], [-30, -30], [92, -2], [0, -90]))
el(3, profil("Seated Arms Sky", 180, [170, 170], [168, 168], [88, 88], [86, 86]))
el(3, profil("Seated Knees Hug", 160, [70, 40], [68, 40], [60, -40], [58, -42]))
el(3, profil("Crawl Reach Arm", 92, [85, 85], [0, 0], [-85, -88], [-80, -88]))
el(3, profil("Side Kneel Leg Out", 175, [160, 160], [-50, -50], [0, -90], [-60, -60]))
el(3, on("Kneel V Arms Wide", "v", "v", [-24, -90], [-24, -90]))
el(3, on("Kneel Robot Arms", [-90, -180], [-90, 0], [-20, -90], [-20, -90]))
el(3, on("Kneel Hips Hands", "hip", "hip", [-18, -90], [-18, -90]))
el(3, on("Kneel Shrug Up", [-40, -95], [-40, -95], [-20, -90], [-20, -90]))
el(3, on("Kneel One Arm Sky", "up", "down", [-22, -90], [-22, -90], govde=184))
el(3, on("Kneel Lean Side Wave", [-150, 170], "hip", [-15, -90], [-15, -90], govde=200))
el(3, on("Deep Squat Elbows Knees", [-30, 160], [-30, 160], [-80, 20], [-80, 20]))
el(3, on("Star Balance One Leg", "v", "v", "tog", [-60, -60], govde=172))
el(3, on("Side Plank Sky Hand", "up", "down", "straight", "straight", govde=118))
# 1. secim: tur 3'te 10 kaldi (diz pozlari eski videolarla 0,79-0,94) -> farkli bacak sekilli yer pozlari
el(3, profil("Seated Lean Back Palms", 222, [-150, -150], [-148, -148], [88, 88], [86, 86]))
el(3, profil("Seated One Knee Reach", 150, [100, 100], [98, 98], [88, 88], [40, -95]))
el(3, profil("Seated Twist Arms Open", 182, [120, 120], [-120, -120], [88, 88], [86, 86]))
el(3, on("Gate Pose Over Reach", [-150, -128], "hip", [-20, -90], [45, 45], govde=212))
el(3, on("Gate Pose Low Hand", "t", [-10, -5], [-20, -90], [48, 48], govde=168))
el(3, on("Frog Squat Hands Floor", [-8, -4], [-8, -4], [-82, 24], [-82, 24]))
el(3, on("Frog Squat Arms Up", "v", "v", [-82, 24], [-82, 24]))
el(3, on("Kneel Arm Arc Over", [-160, 120], [-30, 40], [-16, -90], [-16, -90], govde=196))
el(3, profil("Half Kneel Hands Hips Tall", 180, [-40, 30], [-38, 30], [92, -2], [0, -90]))
el(3, profil("Kneel Sit Heels Arms Forward", 175, [90, 90], [88, 88], [-60, 60], [-62, 58]))

KAPAK = json.load(open(os.path.join(BURA, "pozlar-16-kapak.json"), encoding="utf-8"))["pozlar"]
KAPAK_TUR = {"petal-sky-point": 1, "blossom-wide-star": 1, "petal-hip-side-kick": 2, "lantern-lunge-v-reach": 2}

KOL = {"V": "v", "W": "w", "Cactus": "cactus", "Reach": "up", "T": "t", "Head": "head", "Flex": "flex", "Low": "lowv",
       "Hip": "hip", "Diag": "up45", "Halo": [-160, 120], "Comet": [-110, -170], "Wave": [-70, -130], "Hug": [-40, 100], "Chest": "chest"}
BAC = {"Wide": ("wide", "wide"), "Horse": ("horse", "horse"), "Goddess": ("goddess", "goddess"), "Knee": ("tog", "kneeup"),
       "Tree": ("tog", "kneein"), "Leg Out": ("straight", "tog"), "Kick": ("tog", [60, 60]), "Lunge": ("lunge", "straight"),
       "Tap": ("sidetap", "tog"), "Curtsy": ("curtsy", "tog")}
KELIME = ["Petal", "Blossom", "Lantern", "Bloom", "Sakura", "Pink", "Blue", "Bridge", "Breeze", "Spring",
          "Twilight", "Glow", "Sweet", "Swing", "Branch", "Pastel", "Kawaii", "Sunset", "Ribbon", "Lotus"]
HAVUZ, adlar = [], set()


def ekle(tur, p):
    k = p["ad"].lower()
    if k not in adlar:
        adlar.add(k); p["tur"] = tur; HAVUZ.append(p)


kk, bb = list(KOL), list(BAC)
while len(HAVUZ) < 110:
    a, b, c = rnd.choice(kk), rnd.choice(kk), rnd.choice(bb)
    if a == b:
        continue
    p = on(f"{rnd.choice(KELIME)} {a} {b} {c}", KOL[a], KOL[b], BAC[c][0], BAC[c][1], govde=rnd.choice([164, 172, 180, 188, 196]))
    ekle(1 if c in ("Wide", "Horse", "Tap", "Leg Out") else 2, p)

eski = set()
for f in sorted(os.listdir(BURA)):
    if f.startswith("pozlar") and f.endswith(".json") and not f.startswith("pozlar-16"):
        eski |= {p["ad"].lower() for p in json.load(open(os.path.join(BURA, f), encoding="utf-8"))["pozlar"].values()}
_kul = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("KULLANILMIS = ")[1].split("}")[0] + "}"
eski |= eval(_kul)
DEFTER = os.path.join(os.path.expanduser("~"), "OneDrive", "Masaüstü", "POZ-DUVARI", "poz-defteri.md")   # yerelde calisir
_def = open(DEFTER, encoding="utf-8").read().lower() if os.path.exists(DEFTER) else ""

pozlar = {}
for k, p in KAPAK.items():
    q = dict(p); q["tur"] = KAPAK_TUR[k]; q["el"] = True; q["kapak"] = True
    pozlar[k] = q
for tur, liste in EL.items():
    for p in liste:
        p["tur"] = tur; p["el"] = True
for p in [x for l in EL.values() for x in l] + HAVUZ:
    assert p["ad"].lower() not in eski, p["ad"]
    assert not _def or p["ad"].lower() not in _def, "defterde var: " + p["ad"]
    k = p["ad"].lower().replace(" ", "-").replace("'", "")
    assert k not in pozlar, k
    pozlar[k] = p
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "16. video ADAY (REF-067)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-16-aday.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(pozlar)} aday (kapak 4; el {sum(len(l) for l in EL.values())}: " + ", ".join(f"tur{t} {len(l)}" for t, l in EL.items()) + f"; havuz {len(HAVUZ)}); defter {'okundu' if _def else 'YOK'}")
