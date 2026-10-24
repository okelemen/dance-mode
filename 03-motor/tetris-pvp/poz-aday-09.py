"""HUMAN TETRIS 9. video (REF-060, 1v1, ~5 dk) - poz ADAY havuzu -> pozlar-09-aday.json.
Maskeler Actions'ta (tetris-varlik.yml, yalniz=poz, pozlar=03-motor/tetris-pvp/pozlar-09-aday.json), sonra poz-sec-09.py
olcumle (eski videolarin maskelerine + video icine aynali IoU) 46 poz secer: 3 tur 7 / 7 / 9 duvar (REF-060 yapisi).

    python poz-aday-09.py

REF-060 dili: yoga / denge / esneklik (agac, ucgen, dansci, one egilme, oturus); zorluk turla artar (tur 1 ayakta denge
ve uzanma, tur 2 tek ayak + derin hamle, tur 3 yer + esneklik finali). Once elle tasarlanmis pozlar (EL), sonra yedek
kombinasyon havuzu (HAVUZ). Guvenlik (TALIMATLAR §2): amuda kalkma, tam kopru, bas/omuz durusu, ayakta spagat, kaldirma yok.
Aci dili pozlar.json _not. Adlar defterdeki hicbir pozla cakismaz (assert).
"""
import json, os, random

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]
rnd = random.Random(60)

EL = {1: [], 2: [], 3: []}


def el(tur, p):
    p["ad"] = "Cosmic " + p["ad"]
    EL[tur].append(p)


# ---- TUR 1: ayakta denge, uzanma, yana egilme
el(1, on("Crescent Moon Side Bend", [-170, -165], [-160, -150], "tog", "tog", govde=200))
el(1, on("Tree Hands Prayer High", [-178, 170], [-178, 170], "tog", "kneein"))
el(1, on("Tree Arms Sky V", "v", "v", "kneein", "tog"))
el(1, on("Orbit Arm Circle", [-120, -60], [-60, -120], "softknee", "tog", govde=175))
el(1, on("Star Reach Side Tilt", [-130, -130], [-30, -30], "wide", "wide", govde=165))
el(1, on("Wide Stance Arms Diagonal", [-140, -140], [-40, -40], "straight", "straight"))
el(1, on("Toe Tap Side Arms Up", "up", "up", "tog", [-40, -40], govde=172))
el(1, on("Half Moon Reach Tall", [-170, -170], "down", "tog", [-35, -35], govde=190))
el(1, profil("Mountain Lean Forward Reach", 160, [130, 130], [128, 128], [0, 0], [0, 0]))
el(1, profil("Standing Back Arch Arms Up", 205, [-170, -170], [-168, -168], [5, 5], [-5, -5]))
el(1, profil("Heel Raise Arms Forward High", 180, [140, 140], [138, 138], [5, -5], [0, 0]))
el(1, profil("Step Forward Reach Up", 175, [165, 165], [-30, -30], [40, 0], [-25, -25]))
el(1, on("Side Lunge Arms Low Out", "lowv", "lowv", "lunge", "straight"))
el(1, on("Hands On Head Wide Squat", "head", "head", "horse", "horse"))
el(1, on("Cactus Knee Lift", "cactus", "cactus", "kneeup", "tog"))
el(1, on("Lean Side Arm Over Hip Hand", [-160, -150], "hip", "softknee", "straight", govde=192))
el(1, profil("Quarter Squat Arms Up", 165, [175, 175], [173, 173], [55, -5], [53, -7]))
el(1, on("Diagonal Line Long", [-150, -150], "down", "tog", [-30, -30], govde=168))
el(1, on("Goddess Arms Down Out", "lowv", "lowv", "goddess", "goddess"))
el(1, profil("Knee Hug Standing", 178, [70, -60], [68, -62], [110, -30], [0, 0]))
# ---- TUR 2: tek ayak denge, derin hamle, savasci
el(2, on("Triangle Reach Floor Sky", "up", "down", "straight", "straight", govde=120))
el(2, on("Extended Side Angle", [-155, -155], "down", "lunge", "straight", govde=130))
el(2, profil("Warrior One Arms Up", 182, [178, 178], [176, 176], [95, 0], [-35, -35]))
el(2, on("Warrior Two Arms T", "t", "t", "lunge", "straight"))
el(2, profil("Reverse Warrior Lean", 200, [-160, -160], [-20, -20], [95, 0], [-35, -35]))
el(2, profil("Dancer Reach Forward", 115, [110, 110], [-140, -175], [0, 0], [-60, -160]))
el(2, on("Tree Arms T", "t", "t", "kneein", "tog"))
el(2, profil("Eagle Arms Knee Up", 170, [90, 150], [92, 152], [80, -30], [0, 0]))
el(2, profil("Standing Knee To Chest Arms Up", 180, [175, 175], [173, 173], [130, -20], [0, 0]))
el(2, on("Side Kick Hold Arms Wide", "t", "t", "tog", [70, 70], govde=162))
el(2, profil("Crescent Lunge Hands Prayer", 175, [60, 160], [58, 158], [100, 0], [-55, -55]))
el(2, profil("Pyramid Fold Hands Floor", 95, [5, 5], [3, 3], [20, 20], [-25, -25]))
el(2, profil("Airplane Arms Back", 100, [-50, -50], [-48, -48], [0, 0], [-80, -80]))
el(2, profil("Low Lunge Hands Knee", 175, [40, 40], [38, 38], [100, -5], [-70, -150]))
el(2, profil("Chair Twist Hands Prayer", 150, [70, 170], [68, 168], [70, -10], [68, -12]))
el(2, on("Wide Fold Hands Floor", "down", "down", "straight", "straight", govde=95))
el(2, profil("Standing Leg Forward Hold", 175, [80, 80], [-60, -60], [85, 85], [0, 0]))
el(2, on("Half Moon Arms Wide", [-160, -160], [-20, -20], "tog", [80, 80], govde=105))
el(2, profil("Skandasana Prep", 175, [90, 90], [88, 88], [70, -20], [-45, -45]))
el(2, profil("Revolved Lunge Arm Up", 140, [178, 178], [0, 0], [95, 0], [-45, -45]))
# ---- TUR 3: yer, diz, esneklik finali
el(3, profil("Kneeling Side Lean", 200, [-170, -170], [-20, -20], [0, -90], [0, -90]))
el(3, profil("Child Arms Reach", 20, [170, 170], [168, 168], [110, -60], [108, -62]))
el(3, profil("Seated Forward Fold Toes", 90, [70, 70], [68, 68], [90, 90], [88, 88]))
el(3, profil("Boat Arms Forward", 220, [90, 90], [88, 88], [140, 140], [138, 138]))
el(3, profil("Pigeon Upright Arms Up", 180, [175, 175], [173, 173], [90, -60], [-90, -90]))
el(3, profil("Seated Spinal Twist", 180, [90, 90], [-100, -100], [100, 0], [90, 90]))
el(3, profil("Side Plank Prep Knee", 120, [0, 0], [178, 178], [0, -90], [-20, -20]))
el(3, profil("Gate Pose Side Reach", 190, [-160, -160], [-10, -10], [0, -90], [-40, -40]))
el(3, profil("Plank Knee To Chest", 100, [0, 0], [0, 0], [-40, -130], [-87, -87]))
el(3, profil("Three Leg Down Dog", 40, [35, 35], [33, 33], [-30, -30], [-120, -150]))
el(3, profil("Seated Wide Arms Up", 180, [178, 178], [176, 176], [90, 90], [70, 70]))
el(3, profil("Low Lunge Arch Hands Hips", 210, [-40, -100], [-38, -98], [100, 0], [-60, -150]))
el(3, profil("Kneel Arms Back Chest Open", 190, [-60, -60], [-58, -58], [0, -90], [0, -90]))
el(3, profil("Seated Leg Up Hand Shin", 190, [130, 130], [0, 0], [150, 150], [90, -90]))
el(3, profil("Reclined Hero Prep", 220, [-30, -30], [-28, -28], [0, -90], [0, -90]))
el(3, profil("Lizard Hands Floor", 80, [0, 0], [0, 0], [110, 0], [-60, -60]))
el(3, profil("Tabletop Leg Kick Back", 95, [90, 90], [0, 0], [0, -90], [-100, -100]))
el(3, profil("Kneeling Lunge Back Reach", 200, [178, 178], [-150, -160], [95, 0], [0, -90]))
el(3, profil("Seated Bound Angle Arms Up", 180, [175, 175], [173, 173], [60, -60], [58, -62]))
el(3, profil("Puppy Stretch", 60, [160, 160], [158, 158], [0, -90], [0, -90]))
el(3, profil("Side Seated Mermaid", 195, [-170, -170], [-10, -10], [90, -90], [-80, -150]))
el(3, profil("Half Boat Hands Knees", 210, [60, 60], [58, 58], [130, 30], [128, 28]))
el(3, profil("Kneel Thread Arm Up", 90, [178, 178], [0, 0], [0, -90], [0, -90]))
el(3, profil("Seated One Leg Stretch Reach", 110, [100, 100], [98, 98], [90, 90], [60, -60]))

# ---- HAVUZ: yedek kombinasyonlar (secici --havuz ile kullanir; once EL)
KOL = {"V": "v", "W": "w", "Cactus": "cactus", "Reach": "up", "T": "t", "Head": "head", "Flex": "flex", "Low": "lowv",
       "Hip": "hip", "Diag": "up45", "Halo": [-160, 120], "Comet": [-110, -170], "Wave": [-70, -130], "Hug": [-40, 100]}
BAC = {"Wide": ("wide", "wide"), "Horse": ("horse", "horse"), "Knee": ("tog", "kneeup"), "Tree": ("tog", "kneein"),
       "Leg Out": ("straight", "tog"), "Kick": ("tog", [60, 60]), "Lunge": ("lunge", "straight"), "Tap": ("sidetap", "tog")}
KELIME = ["Nebula", "Comet", "Orbit", "Galaxy", "Stardust", "Meteor", "Pulsar", "Quasar", "Aurora", "Lunar",
          "Solar", "Rocket", "Zenith", "Vortex", "Starlight", "Eclipse", "Halo", "Nova", "Planet", "Saturn"]
HAVUZ, adlar = [], set()


def ekle(tur, p):
    k = p["ad"].lower()
    if k not in adlar:
        adlar.add(k); p["tur"] = tur; HAVUZ.append(p)


kk, bb = list(KOL), list(BAC)
while len(HAVUZ) < 70:     # tur 1-2: onden ayakta asimetrik
    a, b, c = rnd.choice(kk), rnd.choice(kk), rnd.choice(bb)
    if a == b:
        continue
    g = rnd.choice([160, 168, 176, 184, 192, 200])
    p = on(f"{rnd.choice(KELIME)} {a} {b} {c}", KOL[a], KOL[b], BAC[c][0], BAC[c][1], govde=g)
    ekle(1 if c in ("Wide", "Horse", "Tap", "Leg Out") else 2, p)
while len(HAVUZ) < 160:    # tur 2-3: profil denge/esneklik
    gv = rnd.choice([50, 80, 100, 125, 150, 175, 195, 215])
    ok = [rnd.choice([178, 155, 130, 100, 60, 20, -50, -100, -150]) for _ in range(2)]
    on_b = rnd.choice([[0, 0], [100, -10], [120, -50], [60, 0], [0, -90], [90, 90], [140, 140]])
    ar_b = rnd.choice([[0, 0], [-60, -60], [-90, -90], [-30, -30], [-100, -160], [0, -90], [-50, -140]])
    if on_b == [0, -90] and ar_b == [0, -90] and gv < 150:
        continue
    yer = on_b in ([0, -90], [90, 90], [140, 140]) or ar_b == [0, -90] or gv < 80
    p = profil(f"{rnd.choice(KELIME)} Drift {len(HAVUZ)}", gv, [ok[0], ok[0] - 2], [ok[1], ok[1] - 2], on_b, ar_b)
    ekle(3 if yer else 2, p)

# ---- ad cakisma kontrolu: defterdeki tum videolar
eski = set()
for f in ("pozlar.json", "pozlar-03.json", "pozlar-04.json", "pozlar-05.json", "pozlar-05-aday.json",
          "pozlar-06.json", "pozlar-06-aday.json", "pozlar-08.json", "pozlar-08-aday.json"):
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
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "9. video ADAY (REF-060)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-09-aday.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"{len(pozlar)} aday (el {sum(len(l) for l in EL.values())}: " + ", ".join(f"tur{t} {len(l)}" for t, l in EL.items())
      + f"; havuz {len(HAVUZ)}) -> pozlar-09-aday.json")
