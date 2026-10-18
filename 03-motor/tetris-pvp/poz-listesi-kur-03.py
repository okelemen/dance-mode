"""TETRIS MODE 3. video (REF-054) - 90 poz (45 duvar x 2 oyuncu) -> pozlar-03.json + duvar-listesi-03.json.

    python poz-listesi-kur-03.py

Liste kullanici onayli (18 Eki 2026, "Tamam, bu liste olsun"). REF-054 dili: ilk turdan yoga / esneklik, tur tur zorlasir.
Aci dili poz-listesi-kur.py ile ayni (pozlar.json _not). Defterdeki 208 poz (POSE WALL #1 80 + PVP #1 90 + ilk 38) tekrar edilmez.
Guvenlik: amuda kalkma, tam kopru, bas/omuz durusu, tam karga yok; zor pozlarin kolay surumu ("Prep", "Lite").
"""
import json, os
from importlib.util import spec_from_file_location, module_from_spec

BURA = os.path.dirname(os.path.abspath(__file__))
# yardimcilar (on, profil, K, B) PVP #1 ureticisinden; o dosya calistirilmadan alinir
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]

DIZ = [0, "geri"]          # onden diz cokme (baldir kameradan uzaga)
OTUR_L, OTUR_R = [-78, 75], [78, -75]   # onden bagdas

TUR1 = [  # ROUND 1 - isinma esnemeleri (yarisi ayakta, yarisi yerde)
    (on("Eagle Arms", [55, 170], [-55, -170], "softknee", "softknee"),
     profil("Sunrise Arch", 195, [-165, -160], [-160, -158], [3, 2], [-4, -3])),
    (on("Easy Seat Prayer Up", [-160, 165], [160, -165], OTUR_L, OTUR_R),
     on("Wide Leg Fold", [-10, -5], [10, 5], [-30, -30], [30, 30], govde=0)),
    (profil("Child's Pose", 75, [92, 90], [90, 88], [72, -90], [70, -90]),
     profil("Cat Back", 100, [0, 0], [0, 0], [0, -90], [0, -90], bas=-60)),
    (profil("Cow Lift", 85, [0, 0], [0, 0], [0, -90], [0, -90], bas=70),
     profil("Thread the Needle", 65, [-85, -90], [175, 178], [0, -90], [0, -90])),
    (on("Butterfly", [20, 5], [-20, -5], [-68, 62], [68, -62]),
     on("Seated Side Stretch", [-178, 135], [40, 15], OTUR_L, OTUR_R, govde=160)),
    (profil("Pyramid Fold", 35, [-150, -170], [-150, -170], [22, 22], [-28, -28]),
     profil("Standing Backbend", 205, [-30, 10], [-25, 10], [3, 3], [-3, -3], bas=20)),
    (profil("Humble Warrior", 45, [-160, -165], [-155, -160], [70, 0], [-45, -45]),
     on("Wide Leg Twist", [5, 0], [178, 178], [-32, -32], [32, 32], govde=5)),
    (profil("Lizard Lunge", 80, [0, 90], [0, 90], [88, 0], [-62, -90]),
     on("Mermaid Seat", [-40, -10], [175, -130], [60, 95], [80, 100], govde=195)),
    (profil("Happy Baby", -90, [-165, 175], [-160, 178], [-160, 178], [-155, 180]),
     profil("Supine Twist", -90, [-90, -90], [60, 90], [90, 90], [140, 40])),
    (profil("Legs Up", -90, [90, 90], [88, 88], [180, 180], [178, 178]),
     profil("Reclined Butterfly", -90, [-95, -95], [-92, -92], [135, 45], [130, 40])),
    (profil("Head to Knee", 100, [92, 95], [90, 93], [90, 90], [90, -90]),
     on("Wide Angle Fold", [-70, -80], [70, 80], [-88, -88], [88, 88])),
    (on("Crescent Moon Bend", [165, 140], [150, 135], "tog", "tog", govde=158),
     on("Tiptoe Prayer", [-160, 165], [160, -165], "tog", "tog")),
    (on("Toe Touch Twist", [20, 15], [178, 178], "wide", "wide", govde=35),
     profil("Clasp Fold", 15, [150, 150], [148, 148], [2, 2], [-2, -2])),
    (on("Cow Face Arms", [-175, 10], [15, -170], "tog", "tog"),
     profil("Heel Sit Reach Forward", 175, [90, 90], [88, 88], [88, -92], [88, -92])),
    (on("Side Lying Leg Lift", [-90, -170], [20, 0], [92, 90], [130, 128], govde=-90),
     profil("Kneeling Arm Sweep", 175, [130, 130], [-60, -60], [0, -90], [0, -90])),
]

TUR2 = [  # ROUND 2 - denge ve guc
    (profil("Eagle Pose", 165, [95, 175], [95, 175], [50, -15], [40, -10]),
     on("Standing Figure Four", "chest", "chest", [-8, 10], [80, -100])),
    (profil("Revolved Triangle", 90, [0, 0], [180, 180], [25, 25], [-30, -30]),
     on("Bound Side Angle", [-20, 30], [-120, -40], "lunge", "straight", govde=-130)),
    (profil("Pigeon Upright", 175, [10, 0], [8, 0], [85, -95], [-90, -90]),
     profil("Sage Twist", 180, [110, 170], [-35, -25], [140, 2], [90, 90])),
    (profil("Forearm Plank", 95, [0, 90], [0, 90], [-85, -85], [-85, -85]),
     profil("Reverse Tabletop", -90, [0, 0], [0, 0], [90, 0], [90, 0])),
    (profil("Single Leg Bridge", -65, [85, 90], [85, 90], [150, 150], [100, 5]),
     profil("Locust", 105, [-100, -100], [-98, -98], [-100, -100], [-98, -98])),
    (on("Kneeling Side Plank", [178, 178], [0, 0], [-55, -55], [-35, -100], govde=125),
     profil("Dolphin", 45, [30, 90], [30, 90], [-35, -35], [-33, -33])),
    (profil("Stork Fold", 60, [10, 10], [8, 8], [0, 0], [-45, -120]),
     profil("Arabesque Reach", 150, [170, 170], [-90, -90], [0, 0], [-100, -100])),
    (profil("Reverse Plank", -105, [0, 0], [0, 0], [75, 75], [75, 75]),
     on("Wild Thing Lite", [-20, -10], [120, 100], [-45, -100], [-20, -5], govde=140)),
    (on("Fire Log Seat", [-60, -20], [60, 20], [-85, 85], [85, -85]),
     on("Compass Prep", [-30, -10], [130, 140], [-80, 80], [135, 150], govde=190)),
    (on("Gate Lift", [-10, 0], [170, 175], [-20, "geri"], [90, 92], govde=-140),
     profil("Low Boat", 215, [95, 95], [93, 93], [105, 105], [103, 103])),
    (on("Hand to Toe Side", "t", [100, 100], "tog", [100, 100]),
     profil("Tiptoe Squat", 180, [90, 90], [88, 88], [92, -25], [90, -25])),
    (profil("Plank Leg Lift", 95, [0, 0], [0, 0], [-85, -85], [-110, -110]),
     profil("Down Dog Split", 40, [38, 38], [38, 38], [-35, -35], [-150, -150])),
    (profil("Half Bow", 100, [100, 100], [-110, -120], [-92, -92], [-95, -170]),
     profil("Floor Swimmer", 95, [100, 100], [95, 90], [-100, -100], [-90, -90])),
    (profil("Heron Seat", 175, [140, 140], [138, 138], [150, 150], [88, -92]),
     profil("Seated Leg Cradle", 180, [60, 120], [60, 120], [110, -100], [85, -95])),
    (profil("Half Split", 105, [10, 5], [8, 3], [80, 80], [0, -90]),
     on("Wide Squat Twist", [-40, -20], [150, 170], "goddess", "goddess", govde=170)),
]

TUR3 = [  # ROUND 3 - esneklik finali
    (profil("King Pigeon Reach", 190, [150, 150], [-120, -150], [85, -95], [-90, -170]),
     profil("Fish Pose", -115, [60, 90], [60, 90], [90, 90], [90, 90], bas=70)),
    (profil("Front Split Prep", 175, [0, 0], [0, 0], [85, 85], [-80, -80]),
     on("Hurdler Stretch", [-85, -88], [-110, -95], [-88, -88], [80, -100], govde=-135)),
    (profil("Low Lunge Arms Forward", 180, [90, 90], [88, 88], [85, 0], [-15, -90]),
     on("Forearm Side Plank", [5, 95], "hip", [-70, -70], [-72, -72], govde=110)),
    (profil("Hollow Hold", -100, [-110, -110], [-108, -108], [100, 100], [98, 98]),
     profil("Upward Plank Leg Lift", -105, [0, 0], [0, 0], [75, 75], [120, 120])),
    (profil("Mermaid Pigeon", 185, [-175, -115], [-170, -120], [85, -95], [-90, -175]),
     on("Tortoise Prep", [-88, -92], [88, 92], [-105, -15], [105, 15])),
    (profil("Toe Stand Prep", 150, [20, 0], [18, 0], [95, -20], [80, 80]),
     profil("Revolved Side Angle", 100, [0, 0], [180, 180], [75, 0], [-45, -45])),
    (profil("L-Sit Prep", 185, [0, 0], [0, 0], [100, 100], [98, 98]),
     profil("Tabletop Twist Reach", 90, [0, 0], [180, 180], [0, -90], [0, -90])),
    (profil("Lizard Twist", 100, [0, 0], [178, 178], [88, 0], [-62, -90]),
     profil("Humble Pigeon", 80, [95, 90], [93, 88], [85, -95], [-90, -90])),
    (profil("Crane Stand", 180, [-130, -130], [-125, -125], [100, 0], [2, 2]),
     profil("Bear Hold", 90, [0, 0], [0, 0], [10, -70], [10, -70])),
    (on("Open Wide Boat", [-150, -150], [150, 150], [-140, -140], [140, 140]),
     profil("Cross Leg Fold", 100, [95, 90], [93, 88], [85, -80], [85, -80])),
    (profil("Tiger Pose", 90, [0, 0], [-100, -130], [0, -90], [-100, -150]),
     on("Side Plank Tree", [0, 0], [178, 178], [-65, -65], [-150, -30], govde=115)),
    (on("Wide Angle Side Bend", [-85, -88], [175, -140], [-88, -88], [88, 88], govde=-150),
     profil("Kneeling Quad Hold", 180, [140, 140], [-150, -170], [85, 0], [-45, -170])),
    (on("Side Split Prep", [0, 0], [0, 0], [-80, -80], [80, 80]),
     profil("Reverse Prayer Fold", 60, [-130, -60], [-125, -55], [2, 2], [-2, -2])),
    (on("Side Lying Quad Hold", [-90, -170], [60, 90], [92, 90], [90, -120], govde=-90),
     profil("Knee to Nose", 95, [0, 0], [0, 0], [70, 10], [0, -90], bas=-50)),
    (profil("Bound Lunge", 180, [-25, -25], [-22, -22], [70, 0], [-45, -45]),
     on("Seated Straddle Reach Up", "v", "v", [-88, -88], [88, 88])),
]

pozlar, duvarlar, adlar = {}, [], set()
for tur, liste in ((1, TUR1), (2, TUR2), (3, TUR3)):
    for p1, p2 in liste:
        for p in (p1, p2):
            assert p["ad"] not in adlar, p["ad"]
            adlar.add(p["ad"])
        k1 = p1["ad"].lower().replace(" ", "-").replace("'", ""); k2 = p2["ad"].lower().replace(" ", "-").replace("'", "")
        pozlar[k1] = p1; pozlar[k2] = p2
        duvarlar.append({"tur": tur, "p1": k1, "p2": k2})
assert len(duvarlar) == 45 and len(pozlar) == 90, (len(duvarlar), len(pozlar))

# defterdeki adlarla cakisma: PVP #1 (pozlar.json) + POSE WALL #1 (poz-listesi-kur.py KULLANILMIS)
eski = {p["ad"].lower() for p in json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["pozlar"].values()}
_kul = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("KULLANILMIS = ")[1].split("}")[0] + "}"
eski |= eval(_kul)
cakisan = sorted(a for a in adlar if a.lower() in eski)
assert not cakisan, cakisan

not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "3. video (REF-054)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-03.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvarlar, open(os.path.join(BURA, "duvar-listesi-03.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(pozlar)} poz, {len(duvarlar)} duvar -> pozlar-03.json")
