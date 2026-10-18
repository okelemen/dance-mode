"""TETRIS MODE 4. video (REF-055) - 90 poz (45 duvar x 2 oyuncu) -> pozlar-04.json + duvar-listesi-04.json.

    python poz-listesi-kur-04.py

REF-055 dili (Glow Motion "HUMAN TETRIS PVP BATTLE#1"): LEVEL 1 EASY -> MEDIUM -> LEVEL 3 HARD, ilk duvar lotus,
yoga/esneklik, oyunculara farkli poz, zorluk turla artar. Kullanici 18 Eki 2026: "onay beklemene gerek yok ... zayif
gordugun yerleri duzelt". Aci dili poz-listesi-kur.py ile ayni (pozlar.json _not).
Defterdeki 260 poz (POSE WALL #1 80 + PVP #1 90 + 3. video 90) adla tekrar edilmez (assert); sekil benzerligi
Actions maskeleri inince olc-poz-iou.py ile olculur (eski 180 maskeye en yuksek IoU).
Guvenlik: amuda kalkma, tam kopru, bas/omuz durusu, tam karga, plug yok; zor pozlarin kolay surumu ("Prep", "Lite").
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]

DIZ = [0, "geri"]                        # onden diz cokme
OTUR_L, OTUR_R = [-78, 75], [78, -75]    # onden bagdas
DUA_L, DUA_R = [-20, 150], [20, -150]    # onden gogus hizasinda dua eli

TUR1 = [  # LEVEL 1 - EASY: ayakta + oturma, yumusak yoga
    (on("Lotus Prayer", DUA_L, DUA_R, OTUR_L, OTUR_R),
     on("Lotus Arms Wide", "t", "t", OTUR_L, OTUR_R)),
    (profil("Crescent Prayer", 180, [30, 160], [28, 158], [75, 0], [-42, -42]),
     on("Skandasana Prayer", DUA_L, DUA_R, [-75, -5], [52, 52], govde=172)),
    (on("Elbow to Knee", "head", [-35, -15], "kneein", "tog", govde=192),
     on("Knee Out Steeple", [-165, 170], [165, -170], [-80, -8], "tog")),
    (profil("Front Kick Hold", 175, [90, 90], [-60, -60], [70, 70], [0, 0]),
     on("Starfish Lean", "v", "v", "wide", "wide", govde=160)),
    (profil("Half Lift Hands Shins", 50, [5, 5], [3, 3], [2, 2], [-2, -2]),
     profil("Chair Prayer", 150, [30, 160], [28, 158], [60, -10], [58, -12])),
    (profil("Kneeling Hands on Hips", 180, [-40, 60], [-38, 62], [0, -90], [0, -90]),
     profil("Kneeling Clasp Behind Lift", 160, [-150, -150], [-148, -148], [0, -90], [0, -90])),
    (profil("Staff Arms Up", 180, [178, 178], [176, 176], [90, 90], [88, 88]),
     profil("Kneeling Lunge Hands on Knee", 180, [45, 10], [43, 8], [85, 0], [0, -90])),
    (profil("Standing Clasp Behind Lift", 150, [-140, -140], [-138, -138], [0, 0], [-2, -2]),
     on("Lateral Lunge Reach Across", [130, 120], [130, 120], [-75, -5], [52, 52], govde=165)),
    (profil("Knee Raise Arms Up", 180, [178, 178], [176, 176], [90, 0], [0, 0]),
     on("Side Leg Lift Arms Up", "up", "up", "tog", [45, 45], govde=170)),
    (profil("Kneeling Diagonal Reach", 160, [140, 140], [138, 138], [0, -90], [0, -90]),
     profil("Child Arms Back", 70, [-80, -80], [-78, -78], [100, -95], [98, -95])),
    (profil("Seated Toe Point Arms Forward", 175, [90, 90], [88, 88], [80, 80], [78, 78]),
     profil("Seated Leg Hold Up", 185, [120, 120], [118, 118], [140, 140], [90, 90])),
    (profil("Kneeling Arms Up Back", 195, [-175, -175], [-172, -172], [0, -90], [0, -90]),
     profil("Heel Sit Clasp Behind", 165, [-140, -140], [-138, -138], [90, -90], [88, -90])),
    (profil("Standing Arms Forward Tiptoe Lean", 160, [100, 100], [98, 98], [-15, -15], [-17, -17]),
     on("Wide Stance Punch Up", "up", "chest", "wide", "wide")),
    (on("Seated Arms Up Twist Lean", [-170, -150], [140, 120], OTUR_L, OTUR_R, govde=168),
     profil("Seated Lean Back Arms Forward", 210, [90, 90], [88, 88], [125, 55], [123, 53])),
    (profil("Low Lunge Arms Wide Back", 180, [-120, -120], [-60, -60], [85, 0], [0, -90]),
     on("Seated Straddle Arms T", "t", "t", [-80, -80], [80, 80])),
]

TUR2 = [  # MEDIUM - denge, hamle, yer pozlari ("BUT WHO'S GOT THE EDGE?" turuna bizim karsiligimiz)
    (profil("Plank Shoulder Tap", 95, [40, 160], [0, 0], [-85, -85], [-85, -85]),
     profil("Knee Plank Feet Up", 115, [0, 0], [0, 0], [-45, -130], [-47, -132])),
    (profil("Dead Bug", -90, [180, 180], [178, 178], [180, 90], [178, 88]),
     profil("Bicycle Hold", -105, [-140, 60], [-138, 62], [150, 90], [95, 95])),
    (profil("Scissor Legs", -90, [90, 90], [88, 88], [180, 180], [100, 100]),
     profil("Glute Bridge Arms Up", -60, [180, 180], [178, 178], [60, 0], [58, -2])),
    (profil("Crab Kick", -80, [0, 0], [0, 0], [150, 150], [90, 0]),
     profil("Prone Arms Forward Lift", 100, [100, 100], [98, 98], [-90, -90], [-88, -88])),
    (profil("Warrior Lunge Arms Back", 150, [-40, -40], [-38, -38], [75, 0], [-42, -42]),
     on("Goddess Arms Crossed Up", [140, 170], [-140, -170], "goddess", "goddess")),
    (profil("Standing Leg Back Arms Up", 175, [178, 178], [176, 176], [0, 0], [-35, -35]),
     on("One Leg Hug Knee Side", "chest", "t", "tog", [60, -10])),
    (profil("Tabletop Knee Tuck", 90, [0, 0], [0, 0], [0, -90], [60, -40]),
     profil("Kneeling Arm Swing Back", 175, [150, 150], [-60, -60], [0, -90], [0, -90])),
    (profil("Side Lunge Fold Hands Floor", 35, [5, 5], [3, 3], [40, -40], [-40, -40]),
     on("Wide Stance Toe Reach", [-20, -20], [130, 140], "wide", "wide", govde=30)),
    (profil("Pistol Squat Prep", 165, [90, 90], [88, 88], [90, 90], [80, -60]),
     on("Cossack Reach", "t", "t", [-80, -5], [70, 70], govde=175)),
    (profil("Hands Down Lunge Knee Up", 60, [10, 10], [8, 8], [95, -10], [-50, -50]),
     profil("Fallen Lunge Arms Up", 170, [178, 178], [176, 176], [60, -20], [-40, -40])),
    (profil("Seated Leg Raise Hold", 185, [-20, -20], [-18, -18], [120, 120], [90, 90]),
     on("V Sit Hands Floor", [-30, -10], [30, 10], [-140, -150], [140, 150])),
    (profil("Inchworm Walk Out", 105, [30, 30], [28, 28], [-60, -60], [-62, -62]),
     profil("Squat Hands Behind Head", 160, [150, -130], [148, -128], [85, -20], [83, -22])),
    (profil("Toe Touch Kick", 120, [130, 130], [-30, -30], [100, 100], [0, 0]),
     on("Side Bend Leg Out", [-20, -10], [175, -150], [-38, -38], "tog", govde=200)),
    (profil("Kneel One Leg Forward Arms Up", 180, [178, 178], [176, 176], [70, 70], [0, -90]),
     on("Side Lunge Arms Up", "up", "up", [-75, -5], [52, 52], govde=172)),
    (profil("Reverse Lunge Reach Up", 185, [175, 175], [173, 173], [60, 0], [-20, -110]),
     profil("Prone Snow Angel", 100, [180, 180], [178, 178], [-90, -90], [-88, -88])),
]

TUR3 = [  # LEVEL 3 - HARD: esneklik + denge finali (guvenli surumler)
    (profil("Full Bow", 100, [-120, -120], [-118, -118], [-80, -170], [-78, -168]),
     profil("Kneeling Backbend Hands Heels", 230, [-30, -30], [-28, -28], [0, -90], [0, -90])),
    (profil("Standing Bow Pull", 120, [100, 100], [-120, -150], [0, 0], [-120, -175]),
     on("Side Plank Leg Lift", [0, 0], [178, 178], [-70, -70], [-120, -120], govde=115)),
    (profil("Seated Forward Fold Arms Long", 120, [110, 110], [108, 108], [90, 90], [88, 88]),
     on("Straddle Side Reach", [-80, -85], [175, -120], [-88, -88], [88, 88], govde=-145)),
    (profil("Splits Prep Arms Wide", 180, [-90, -90], [90, 90], [85, 85], [-80, -80]),
     profil("Lunge Backbend Arms Up", 200, [-160, -160], [-158, -158], [70, 0], [-40, -90])),
    (profil("Boat Twist Arms", 215, [-60, -60], [120, 120], [110, 110], [108, 108]),
     profil("Seated Leg Lift Arms Up", 190, [178, 178], [176, 176], [130, 130], [90, 90])),
    (profil("Standing Split Hands Floor", 20, [5, 5], [3, 3], [2, 2], [-150, -150]),
     profil("Warrior Three Hands Prayer", 95, [30, 160], [28, 158], [0, 0], [-90, -90])),
    (profil("Kneeling Lunge Quad Pull", 185, [175, 175], [-120, -160], [80, 0], [-10, -150]),
     profil("Half Kneel Arms Back Lift", 185, [-140, -140], [-138, -138], [80, 0], [0, -90])),
    (profil("Lying Reach Up", -90, [180, 180], [178, 178], [180, 180], [178, 178]),
     profil("Lying Leg Hug", -90, [150, 90], [148, 88], [150, 70], [92, 92])),
    (profil("Low Squat Prayer Twist", 140, [40, 170], [-60, -60], [80, -20], [78, -22]),
     on("Wide Squat Arms Up", "up", "up", "goddess", "goddess", govde=180)),
    (profil("Plank Knee to Elbow", 95, [0, 0], [0, 0], [120, -40], [-85, -85]),
     profil("Side Lunge Hands Prayer Deep", 180, [30, 160], [28, 158], [95, -5], [-35, -35])),
    (profil("Seated Lean Back Leg Up", 215, [-35, -35], [-33, -33], [140, 140], [125, 55]),
     on("Seated Wide Twist Reach", [-80, -80], [170, 170], [-85, -85], [85, 85], govde=200)),
    (profil("Kneeling Arch One Arm", 220, [-175, -175], [-40, -40], [0, -90], [0, -90]),
     profil("Low Lunge Hands on Back Knee", 180, [-30, -30], [-28, -28], [85, 0], [0, -150])),
    (profil("Forearm Plank Leg Up", 100, [10, 90], [10, 90], [-85, -85], [-130, -130]),
     profil("Kneeling Airplane Arms", 165, [90, 90], [-90, -90], [0, -90], [0, -90])),
    (profil("Stork Arms Up", 180, [178, 178], [176, 176], [100, -90], [0, 0]),
     profil("Deep Lunge Arms Forward Low", 120, [100, 100], [98, 98], [100, 0], [-60, -60])),
    (profil("Seated Splits Lean", 200, [-170, -170], [-168, -168], [88, 88], [-88, -88]),
     profil("Lunge Victory Reach", 180, [150, 150], [-160, -160], [75, 0], [-42, -42])),
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

# defterdeki adlarla cakisma: PVP #1 + 3. video + POSE WALL #1
eski = set()
for f in ("pozlar.json", "pozlar-03.json"):
    eski |= {p["ad"].lower() for p in json.load(open(os.path.join(BURA, f), encoding="utf-8"))["pozlar"].values()}
_kul = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("KULLANILMIS = ")[1].split("}")[0] + "}"
eski |= eval(_kul)
cakisan = sorted(a for a in adlar if a.lower() in eski)
assert not cakisan, cakisan

not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "4. video (REF-055)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-04.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvarlar, open(os.path.join(BURA, "duvar-listesi-04.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(pozlar)} poz, {len(duvarlar)} duvar -> pozlar-04.json")
