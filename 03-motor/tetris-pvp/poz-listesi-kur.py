"""TETRIS MODE PVP #1 - 90 poz (45 duvar x 2 oyuncu) -> pozlar.json.

    python poz-listesi-kur.py

Kural (POZ-DUVARI/TALIMATLAR.md §2, poz-defteri.md): her poz gercek ve guvenli, videoda tekrar yok, defterdeki
(POSE WALL #1, 80 poz) pozlar tekrar edilmez. REF-053 dili: yoga / esneklik / denge; tur tur zorlasir.
Acilar ekran duzleminde (pozlar.json _not). Kol/bacak sekilleri EKRAN-SOLU uzuv icin yazilir, ekran-sagi aynalanir.
Karakter kameraya donukken sagKol/sagBacak = ekran SOLU, solKol/solBacak = ekran SAGI.
"""
import json, os

def ayna(v):
    return [-v[0], -v[1]]

# kol sekilleri (ekran-solu kol)
K = {
    "up": [-174, -176], "v": [-148, -148], "t": [-90, -90], "cactus": [-90, 180], "w": [-55, -160],
    "head": [-128, 62], "behind": [-152, 38], "lowv": [-35, -35], "down": [-8, -5], "hip": [-45, 20],
    "chest": [-22, 95], "up45": [-122, -122], "flex": [-95, 150], "elbowdown": [-30, -150],
}
# bacak sekilleri (ekran-solu bacak)
B = {
    "tog": [-3, -1], "wide": [-22, -22], "goddess": [-62, -4], "horse": [-38, 4], "kneeup": [-80, -8],
    "lunge": [-62, -2], "straight": [-45, -45], "sidetap": [-30, -30], "curtsy": [18, -12], "softknee": [-12, 6],
    "kneein": [-60, 40],
}

def on(ad, sagKol, solKol, sagBacak, solBacak, govde=180, bas=0):
    """kameraya donuk poz; sag* = ekran solu, sol* = ekran sagi (sekil adlari ya da aci listesi)"""
    g = lambda x, D: (D[x] if isinstance(x, str) else x)
    sk = g(sagKol, K); so = g(solKol, K); sb = g(sagBacak, B); sl = g(solBacak, B)
    if isinstance(solKol, str): so = ayna(so)
    if isinstance(solBacak, str): sl = ayna(sl)
    return {"ad": ad, "yon": "on", "govde": govde, "bas": bas, "sagKol": sk, "solKol": so, "sagBacak": sb, "solBacak": sl}

def profil(ad, govde, onKol, arkaKol, onBacak, arkaBacak, bas=0):
    """profil (yuzu ekran sagina): pozitif aci = ileri. onKol/onBacak = kameraya yakin uzuv (karakterin solu)"""
    return {"ad": ad, "yon": "sag", "govde": govde, "bas": bas, "solKol": onKol, "sagKol": arkaKol, "solBacak": onBacak, "sagBacak": arkaBacak}

TUR1 = [  # ayakta, onden - herkes yapar (15 duvar: P1, P2)
    (on("Big V", "v", "v", "tog", "tog"), on("Cactus", "cactus", "cactus", "tog", "tog")),
    (on("W Arms", "w", "w", "softknee", "softknee"), on("Hands on Head", "head", "head", "wide", "wide")),
    (on("Goddess Squat", "cactus", "cactus", "goddess", "goddess"), on("Low V Stance", "lowv", "lowv", "wide", "wide")),
    (on("Knee Lift Cactus", "cactus", "cactus", "tog", "kneeup"), on("Elbows Back Stretch", "behind", "behind", "tog", "tog")),
    (on("Goddess V", "v", "v", "goddess", "goddess"), on("Reach and Tap", "up", "t", "tog", "sidetap")),
    (on("Horse Stance", "chest", "chest", "horse", "horse"), on("Knee Lift V", "v", "v", "kneeup", "tog")),
    (on("Curtsy Reach", "up", "up", "softknee", "curtsy"), on("Side Tap T", "t", "t", "sidetap", "tog")),
    (on("Wide W", "w", "w", "wide", "wide"), on("Banana Reach", [150, 150], [140, 140], "tog", "tog", govde=162)),
    (on("Diagonal Line", "up45", [55, 55], "straight", "tog"), on("Goddess Hands on Head", "head", "head", "goddess", "goddess")),
    (on("One Arm Up Knee Lift", "up", "hip", "tog", "kneeup"), on("Wide Cactus", "cactus", "cactus", "wide", "wide")),
    (on("Horse W", "w", "w", "horse", "horse"), on("Tall Reach", "up", "up", "tog", "tog")),
    (on("Lean Left Reach", "down", [205, 235], "tog", "sidetap", govde=205), on("Lean Right Reach", [-205, -235], "down", "sidetap", "tog", govde=155)),
    (on("Knee In Twist", "head", "head", "tog", "kneein"), on("Flexed Arms Wide", "flex", "flex", "straight", "straight")),
    (on("Low Horse Reach", "up45", "up45", "horse", "horse"), on("Curtsy Cactus", "cactus", "cactus", "curtsy", "softknee")),
    (on("Side Lean Squat", "v", [40, 40], "goddess", "goddess", govde=168), on("Elbows Down Knee Lift", "elbowdown", "elbowdown", "kneeup", "tog")),
]

TUR2 = [  # SKILL CHECK: denge, hamle, profil
    (profil("Warrior One", 178, [176, 180], [174, 178], [62, 0], [-40, -40]), on("Standing Knee Out", "t", "t", "tog", [85, 20])),
    (profil("Crescent Lunge", 178, [176, 180], [174, 178], [82, 2], [-42, -80]), profil("Split Stance Fold", 70, [20, 20], [15, 15], [25, 25], [-30, -30])),
    (profil("Flat Back", 92, [10, 10], [8, 8], [3, 3], [-3, -3]), profil("Standing Knee Hold", 180, [60, 10], [-20, -10], [100, 10], [-2, 0])),
    (profil("Lunge Arms Back", 150, [-150, -150], [-140, -140], [70, 0], [-40, -45]), on("Goddess Side Bend", "down", [200, 230], "goddess", "goddess", govde=200)),
    (profil("Reverse Warrior", 200, [-160, -160], [-20, -20], [62, 0], [-40, -40]), on("Wide Side Reach", [-215, -240], "down", "wide", "wide", govde=160)),
    (profil("Garland Squat", 160, [80, 140], [85, 145], [110, -15], [105, -15]), on("Gate Pose", [170, 140], [60, 60], [0, "geri"], [65, 65], govde=160)),
    (profil("Runner Lunge Low", 125, [5, 5], [3, 3], [80, 2], [-75, -82]), on("Extended Side Angle", "down", [220, 225], "lunge", "straight", govde=215)),
    (profil("Standing Split Low", 40, [5, 5], [3, 3], [2, 2], [-130, -130]), on("Balance T Knee", "t", "t", "kneeup", "tog")),
    (profil("Kick Back Reach", 140, [100, 100], [-60, -60], [3, 3], [-70, -70]), on("Wide Elbow Stretch", "behind", "behind", "wide", "wide")),
    (profil("Quad Stretch Reach", 180, [140, 140], [-30, -30], [2, 2], [-28, -150]), on("Hip Shift Reach", "up", "hip", [10, 10], [-15, -15], govde=190)),
    (profil("Chair Reach Back", 145, [-170, -170], [-165, -165], [55, -20], [55, -20]), on("Squat Cross Arms", "chest", "chest", "goddess", "goddess")),
    (profil("Lunge Prayer Twist", 160, [80, 150], [100, 150], [70, 0], [-40, -45]), on("Knee Up Diagonal", "up45", [55, 55], "tog", "kneeup")),
    (profil("Front Leg Reach", 178, [140, 140], [135, 135], [45, 45], [-3, -2]), on("Low V Curtsy", "lowv", "lowv", "curtsy", "softknee")),
    (profil("Single Leg Reach Forward", 150, [100, 100], [95, 95], [2, 2], [-60, -60]), on("Squat Diagonal Reach", [150, 150], [140, 140], "goddess", "goddess", govde=170)),
    (profil("Deep Lunge Hands Down", 95, [5, 5], [3, 3], [80, 2], [-60, -60]), on("Squat Elbows Down", "elbowdown", "elbowdown", "goddess", "goddess")),
]

TUR3 = [  # TIME TO GO ALL OUT: diz cokme, oturma, yer
    (profil("Kneeling Reach", 180, [176, 180], [174, 178], [0, -90], [0, -90]), profil("Camel", 210, [-25, -25], [-20, -20], [0, -90], [0, -90])),
    (profil("Kneeling Lunge Arms Up", 180, [176, 180], [174, 178], [85, 0], [-15, -90]), profil("Seated Staff", 180, [5, 5], [3, 3], [90, 90], [90, 90])),
    (profil("Seated Forward Reach", 125, [90, 95], [88, 92], [90, 90], [90, 90]), profil("High Plank", 75, [2, 2], [0, 0], [-105, -105], [-105, -105])),
    (profil("Cobra", 125, [3, 3], [0, 0], [-92, -92], [-92, -92]), profil("Kneeling Side Arm", 180, [90, 90], [-90, -90], [0, -90], [0, -90])),
    (profil("Hero Seat Arms Up", 180, [176, 180], [174, 178], [88, -92], [88, -92]), profil("Tabletop Leg Lift", 90, [0, 0], [0, 0], [0, -90], [-90, -90])),
    (profil("Seated Knees Up", 175, [60, 60], [55, 55], [125, 0], [125, 0]), profil("Kneeling Camel Reach", 205, [-170, -170], [-25, -25], [0, -90], [0, -90])),
    (profil("Plank Knee Drive", 75, [2, 2], [0, 0], [60, -40], [-105, -105]), profil("Seated Reach Back", 200, [-150, -150], [-140, -140], [90, 90], [90, 90])),
    (on("Half Kneel V", "v", "v", [0, "geri"], [70, 0]), on("Half Kneel Cactus", "cactus", "cactus", [-70, 0], [0, "geri"])),
    (profil("Low Lunge Twist Back", 175, [90, 90], [-90, -90], [80, 2], [-75, -82]), profil("Seated Leg Lift", 175, [-30, -20], [-25, -15], [130, 130], [90, 90])),
    (profil("Puppy Stretch", 55, [85, 85], [83, 83], [0, -90], [0, -90]), profil("Kneeling Lean Back", 200, [-60, -60], [-55, -55], [0, -90], [0, -90])),
    (on("Half Kneel W", "w", "w", [0, "geri"], [70, 0]), on("Half Kneel Lean", "down", [205, 230], [-70, 0], [0, "geri"], govde=205)),
    (profil("Sphinx Lift", 110, [0, 90], [0, 90], [-92, -92], [-92, -92]), profil("Seated Twist Arms", 180, [90, 90], [-90, -90], [125, 0], [90, 90])),
    (profil("Plank Arm Reach", 75, [100, 100], [0, 0], [-105, -105], [-105, -105]), profil("Hero Seat Lean Back", 205, [-20, -20], [-15, -15], [88, -92], [88, -92])),
    (profil("Kneeling Lunge Reach Back", 200, [-160, -160], [-150, -150], [85, 0], [-15, -90]), profil("Seated Wide Arms", 180, [130, 130], [-130, -130], [90, 90], [90, 90])),
    (profil("Kneel Torch Up", 178, [176, 180], [90, 90], [80, 0], [-15, -90]), profil("Tabletop Reach", 90, [90, 90], [0, 0], [0, -90], [0, -90])),
]

pozlar, duvarlar, adlar = {}, [], set()
for tur, liste in ((1, TUR1), (2, TUR2), (3, TUR3)):
    for p1, p2 in liste:
        for p in (p1, p2):
            assert p["ad"] not in adlar, p["ad"]
            adlar.add(p["ad"])
        k1 = p1["ad"].lower().replace(" ", "-"); k2 = p2["ad"].lower().replace(" ", "-")
        pozlar[k1] = p1; pozlar[k2] = p2
        duvarlar.append({"tur": tur, "p1": k1, "p2": k2})

# defterde (POSE WALL #1) kullanilmis adlarla cakisma kontrolu
KULLANILMIS = {"airplane", "archer", "back to back", "big arch", "boat", "bridge hands", "champions", "crab pair", "dancer hold", "flamingo",
               "hands on knees", "heart", "high five", "leaning tower", "lightning", "low and high", "lunge twins", "mirror wave",
               "point the way", "pyramid", "robot", "rocket", "scarecrow", "seesaw", "side bend", "side plank star", "skater",
               "ski jumper", "star", "statue", "superhero", "table and chair", "tea pot", "thinker pair", "tree", "tunnel",
               "wall sit pair", "warrior three", "warrior two", "triangle", "low lunge", "down dog", "fold down", "chair", "half moon",
               "knee hug", "side lunge", "superman", "hips up", "mountain climber", "lunge twist", "frog", "lunge punch", "hero kneel",
               "hand to toe", "squat arms up", "toe touch sit", "bird dog", "rock star", "victory lunge", "big hug", "dancer", "windmill",
               "surfer", "runner", "zombie", "penguin", "cross legs", "floor reach", "fists up", "side kick", "muscles", "salute",
               "disco", "lean", "goalkeeper", "dino arms", "wave hello", "hand on chin", "step out", "hands on hips", "teapot", "bow"}
cakisan = [a for a in adlar if a.lower() in KULLANILMIS]
assert not cakisan, cakisan

yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pozlar.json")
json.dump({"_not": json.load(open(yol, encoding="utf-8"))["_not"], "pozlar": pozlar}, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvarlar, open(os.path.join(os.path.dirname(yol), "duvar-listesi.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(pozlar)} poz, {len(duvarlar)} duvar -> {yol}")
