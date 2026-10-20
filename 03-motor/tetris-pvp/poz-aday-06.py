"""TETRIS MODE 6. video (REF-057, 2 oyuncu, ~5 dk) - poz ADAY havuzu -> pozlar-06-aday.json.
Maskeler Actions'ta (tetris-varlik.yml, yalniz=poz, pozlar=03-motor/tetris-pvp/pozlar-06-aday.json), sonra poz-sec-06.py
olcumle (eski 418 maskeye + video icine aynali IoU) 44 poz secer: tur 1 = 7 duvar, tur 2 = 7, tur 3 = 8 (REF-057 olcumu).

    python poz-aday-06.py

REF-057 dili: yoga / esneklik / denge / dans; zorluk turla artar (tur 1 ayakta yumusak, tur 2 tek ayak + derin hamle + yer,
tur 3 esneklik finali). Once elle tasarlanmis pozlar (EL), sonra asimetrik kombinasyon havuzu (HAVUZ) - basit pozlar onceki
5 videoda kullanildi. Guvenlik (TALIMATLAR §2): amuda kalkma, tam kopru, bas/omuz durusu, tam karga, kaldirma yok.
Aci dili pozlar.json _not. Adlar defterdeki hicbir pozla cakismaz (assert).
"""
import glob, json, os, random

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]
rnd = random.Random(57)

DUA = ([30, 160], [28, 158])               # profil: gogus hizasinda dua eli
UST = ([178, 178], [176, 176])             # profil: iki kol yukari
EL = {1: [], 2: [], 3: []}


def el(tur, p):
    p["ad"] = "Aurora " + p["ad"]
    EL[tur].append(p)


# ---- TUR 1: ayakta, yumusak yoga + dans
el(1, profil("Crescent Arms Wide", 185, [120, 120], [-120, -120], [70, 0], [-38, -38]))
el(1, on("Tree Arms Crown", [-150, 120], [150, -120], "tog", "kneein"))
el(1, profil("Airplane Lean Back Arms", 150, [-40, -40], [-38, -38], [60, -5], [-30, -30]))
el(1, on("Half Moon Side Reach", [-10, -10], [160, 130], [-8, -6], [10, 10], govde=205))
el(1, profil("Standing Hug Knee", 180, [60, -40], [58, -42], [110, -30], [0, 0]))
el(1, on("Victory Lunge Side", "v", "v", [-60, -5], [30, 30], govde=172))
el(1, profil("Gate Reach Up", 180, [170, 170], [168, 168], [0, -90], [45, 45]))
el(1, on("Dancer Arms Fan", [-120, -60], [120, 60], [-10, 10], [70, -110]))
el(1, profil("Heel Raise Reach Forward", 175, [110, 120], [108, 118], [-6, -6], [-8, -8]))
el(1, on("Side Step Reach Diagonal", [-160, -165], [40, 20], [-30, -30], "tog", govde=172))
el(1, profil("Kneeling Prayer Up", 180, [178, 178], [176, 176], [0, -90], [0, -90]))
el(1, on("Wide Stance Elbow Frame", [-60, 170], [60, -170], "wide", "wide"))
el(1, profil("Mountain Lean Arms Back", 170, [-60, -60], [-58, -58], [0, 0], [-2, -2]))
el(1, on("Goddess One Arm Up", "up", "hip", "goddess", "goddess"))
el(1, profil("Tiptoe Arms Forward Bend", 135, [120, 120], [118, 118], [-4, -4], [-6, -6]))
el(1, on("Hip Sway Arms Wave", [-110, -170], [110, -10], "softknee", [8, 8], govde=172))
# ---- TUR 2: tek ayak denge, derin hamle, yer pozlari
el(2, profil("Warrior Lean Forward Arms Back", 125, [-60, -60], [-58, -58], [70, 0], [-38, -38]))
el(2, on("Tree Hands Overhead Tilt", [-165, -170], [170, 165], "tog", "kneein", govde=170))
el(2, profil("Knee Pull Lean", 160, [90, -10], [88, -12], [120, -20], [0, 0]))
el(2, profil("Leg Back Arms Forward", 110, [110, 110], [108, 108], [5, 5], [-70, -70]))
el(2, profil("Side Kneel Arch", 200, [175, 175], [-40, -40], [0, -90], [30, -60]))
el(2, on("Deep Goddess Prayer Up", [-175, -178], [175, 178], "goddess", "goddess", govde=180))
el(2, profil("Low Lunge Twist Open", 175, [90, 90], [-90, -90], [95, 0], [-60, -150]))
el(2, profil("Pyramid Hands Back", 70, [-150, -150], [-148, -148], [25, 25], [-25, -25]))
el(2, on("Kneeling Side Stretch Leg Out", [-30, -10], [160, -160], [0, -90], [60, 60], govde=200))
el(2, profil("Seated Hug Knees", 165, [70, 0], [68, -2], [130, -20], [128, -22]))
el(2, profil("Single Leg Squat Prep", 150, [100, 100], [98, 98], [80, -10], [45, 45]))
el(2, on("Star Balance Lean", [-120, -120], [120, 120], [-5, -5], [70, 70], govde=165))
el(2, profil("Table Top Leg Lift", 95, [0, 0], [-2, -2], [0, -90], [-90, -90]))
el(2, profil("Squat Arms Up Lean", 165, [170, 170], [168, 168], [90, -10], [88, -12]))
el(2, on("Lunge Cross Reach", [-30, 30], [-150, -150], [-60, -5], [30, 30], govde=165))
el(2, profil("Kneeling One Leg Side Arms Up", 180, [175, 175], [173, 173], [0, -90], [90, 0]))
# ---- TUR 3: esneklik finali
el(3, profil("Dancer Deep Reach", 115, [115, 115], [-120, -170], [0, 0], [-110, -170]))
el(3, profil("Warrior Three Arms Wide", 92, [180, 180], [0, 0], [0, 0], [-90, -90]))
el(3, profil("Standing Split Hand Ankle", 15, [-5, -5], [-3, -3], [2, 2], [-160, -160]))
el(3, profil("Half Split Arms Up", 180, [178, 178], [176, 176], [90, 90], [0, -90]))
el(3, profil("Camel Prep One Hand Heel", 215, [-30, -30], [175, 175], [0, -90], [0, -90]))
el(3, profil("King Pigeon Prep", 175, [-150, -150], [-148, -148], [90, -5], [-90, -160]))
el(3, on("Side Plank Star", [0, 0], [175, 175], [-70, -70], [-30, -30], govde=118))
el(3, profil("Boat Arms Back", 215, [-80, -80], [-78, -78], [130, 130], [128, 128]))
el(3, profil("Seated Leg Hold Stretch", 180, [150, 150], [148, 148], [150, 150], [90, 90]))
el(3, profil("Bow Kneeling Reach", 185, [175, 175], [-150, -170], [0, -90], [-10, -170]))
el(3, profil("Extended Side Angle Bind", 125, [-20, -20], [-150, -150], [85, 0], [-42, -42]))
el(3, profil("Front Split Prep Hands Floor", 120, [45, 45], [43, 43], [90, 90], [-85, -85]))
el(3, on("Wide Straddle Fold Arms Out", [-100, -100], [100, 100], [-88, -88], [88, 88], govde=125))
el(3, profil("Low Lunge Back Bind Lift", 195, [-150, -150], [-148, -148], [95, 0], [-55, -150]))
el(3, profil("Standing Leg Hold Forward", 180, [100, 100], [-30, -30], [90, 90], [0, 0]))
el(3, profil("Mermaid Seated Arch", 205, [178, 178], [176, 176], [90, -90], [-90, -150]))
el(3, profil("Arabesque Arms Up", 165, [178, 178], [176, 176], [0, 0], [-80, -80]))
el(3, profil("Tiger Kneel Leg Up", 95, [90, 90], [0, 0], [0, -90], [-120, -170]))

# ---- kontak 1 duzeltmesi (20 Eki 2026): havada/dusuyor gibi okunan ve tam yer spagati gibi gorunen pozlarin yerine
# YERE SAGLAM BASAN yedekler (secici HARIC listesiyle eskileri atar)
el(1, profil("Walking Stance Arms Up", 185, [178, 178], [176, 176], [25, 25], [-25, -25]))
el(1, profil("Split Stance Arms Forward Back", 180, [90, 90], [-60, -60], [28, 28], [-28, -28]))
el(1, on("Wide Stance Side Bend Arm Over", [-150, -110], [20, 10], "wide", "wide", govde=200))
el(2, profil("Kneeling Hands Behind Head Lean", 160, [150, -130], [148, -128], [0, -90], [0, -90]))
el(2, profil("Low Squat Arms Forward", 150, [95, 95], [93, 93], [110, -60], [108, -62]))
el(2, profil("Lunge Arms Back Wings", 175, [-100, -100], [-98, -98], [80, 0], [-40, -40]))
el(2, on("Horse Stance Arms Diagonal", [-140, -140], [40, 40], "horse", "horse"))
el(3, profil("Lizard Lunge Arms Up", 160, [178, 178], [176, 176], [100, -10], [-70, -70]))
el(3, profil("Seated Forward Reach Toes", 110, [100, 100], [98, 98], [90, 90], [88, 88]))
el(3, on("Gate Side Bend Over", [-150, -110], [20, 10], [0, -90], [60, 60], govde=205))
el(3, profil("Kneeling Lunge Prayer Twist", 175, [40, 170], [-60, -60], [95, 0], [0, -90]))
el(3, profil("Warrior Reverse Reach", 200, [160, 160], [-30, -30], [70, 0], [-38, -38]))

# ---- HAVUZ: asimetrik kombinasyonlar (seciciye yedek; once EL kullanilir)
KOL = {"V": "v", "W": "w", "Cactus": "cactus", "Reach": "up", "T": "t", "Head": "head", "Flex": "flex", "Low": "lowv",
       "Hip": "hip", "Diag": "up45", "Swing": [-150, -110], "Hook": [-130, -40], "Salute": [-100, 140], "Cross": [-20, 110]}
BAC = {"Wide": ("wide", "wide"), "Goddess": ("goddess", "goddess"), "Knee": ("tog", "kneeup"), "Tree": ("tog", "kneein"),
       "Leg Out": ("straight", "tog"), "Kick": ("tog", [55, 55]), "Lunge": ("lunge", [30, 30]), "Curtsy": ("curtsy", "softknee")}
KELIME = ["Polar", "Glacier", "Frost", "Comet", "Nova", "Orbit", "Crystal", "Iceberg", "Snowflake", "Northern", "Zenith",
          "Prism", "Halo", "Meteor", "Tundra", "Fjord", "Pulsar", "Lumen", "Boreal", "Stardust"]
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
    g = rnd.choice([165, 172, 180, 188, 195])
    p = on(f"{rnd.choice(KELIME)} {a} {b} {c}", KOL[a], KOL[b], BAC[c][0], BAC[c][1], govde=g)
    ekle(1 if c in ("Wide", "Goddess", "Curtsy", "Lunge") else 2, p)
while len(HAVUZ) < 140:    # tur 2-3: profil denge/esneklik
    gv = rnd.choice([60, 90, 110, 130, 160, 185, 205])
    ok = [rnd.choice([178, 150, 120, 90, 45, -40, -90, -150]) for _ in range(2)]
    on_b = rnd.choice([[0, 0], [90, -10], [110, -40], [70, 0], [0, -90], [45, 45], [95, 95]])
    ar_b = rnd.choice([[0, 0], [-70, -70], [-90, -90], [-40, -40], [-110, -170], [0, -90], [-60, -150]])
    if on_b == [0, -90] and ar_b == [0, -90]:
        continue
    zor = gv < 120 or ar_b[0] <= -70
    p = profil(f"{rnd.choice(KELIME)} Flow {len(HAVUZ)}", gv, [ok[0], ok[0] - 2], [ok[1], ok[1] - 2], on_b, ar_b)
    ekle(3 if zor else 2, p)

# ---- ad cakisma kontrolu: defterdeki tum videolar
eski = set()
for f in ("pozlar.json", "pozlar-03.json", "pozlar-04.json", "pozlar-05.json", "pozlar-05-aday.json"):
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
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "6. video ADAY (REF-057)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-06-aday.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"{len(pozlar)} aday (el {sum(len(l) for l in EL.values())}: " + ", ".join(f"tur{t} {len(l)}" for t, l in EL.items())
      + f"; havuz {len(HAVUZ)}) -> pozlar-06-aday.json")
