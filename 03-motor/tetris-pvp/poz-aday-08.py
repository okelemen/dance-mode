"""HUMAN TETRIS 8. video (REF-059, 1v1 PvP, ~5 dk) - poz ADAY havuzu -> pozlar-08-aday.json.
Maskeler Actions'ta (tetris-varlik.yml, yalniz=poz, pozlar=03-motor/tetris-pvp/pozlar-08-aday.json), sonra poz-sec-08.py
olcumle (eski 6 videonun maskelerine + video icine aynali IoU) 44 poz secer: 4 tur 5 / 7 / 4 / 6 duvar (REF-059 oraniyla 5 dk).

    python poz-aday-08.py

REF-059 dili: esneklik / denge / dans (disko); zorluk turla artar (tur 1 ayakta disko-dans pozlari, tur 2 tek ayak + derin
hamle, tur 3 yer + diz, tur 4 esneklik finali). Once elle tasarlanmis pozlar (EL), sonra yedek kombinasyon havuzu (HAVUZ).
Guvenlik (TALIMATLAR §2): amuda kalkma, tam kopru, bas/omuz durusu, ayakta spagat, kaldirma yok.
Aci dili pozlar.json _not. Adlar defterdeki hicbir pozla cakismaz (assert).
"""
import json, os, random

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]
rnd = random.Random(59)

EL = {1: [], 2: [], 3: [], 4: []}


def el(tur, p):
    p["ad"] = "Disco " + p["ad"]
    EL[tur].append(p)


# ---- TUR 1: ayakta, disko / dans pozlari
el(1, on("Saturday Point", "up45", "hip", "lunge", "softknee"))
el(1, on("Point Diagonal Hip Pop", "up45", "lowv", "softknee", "tog", govde=172))
el(1, on("Hip Bump Arms Up", "up", "up", "softknee", "sidetap", govde=168))
el(1, profil("Runner Arms Swing", 175, [90, 90], [-60, -60], [70, -20], [-30, -60]))
el(1, on("Star Tiptoe Arm Flag", "v", "t", "straight", "tog"))
el(1, on("Lasso Overhead", [-150, -60], "hip", "tog", "softknee"))
el(1, profil("Reach Forward Lunge", 165, [120, 120], [118, 118], [75, 0], [-35, -35]))
el(1, on("Wide Lean Arms Over Right", [150, 140], [148, 138], "wide", "wide", govde=158))
el(1, profil("Heel Kick Back Arms Swing", 178, [60, 60], [-50, -50], [0, 0], [-5, -150]))
el(1, on("Elbow Pump Goddess", "elbowdown", "w", "goddess", "goddess"))
el(1, profil("Back Lean Arms Open", 195, [150, 150], [-130, -130], [10, 10], [-10, -10]))
el(1, on("Side Lunge Reach Over", [-165, -160], "hip", "softknee", "straight", govde=195))
el(1, on("Cross Step Arms T", "t", "t", "curtsy", "softknee"))
el(1, profil("Mini Squat Arms Back", 150, [-70, -70], [-68, -68], [90, -10], [88, -12]))
el(1, on("Knee Up Clap High", "up", "up", "kneeup", "tog"))
el(1, on("Frame Wide Chest", "chest", "chest", "wide", "wide"))
# ---- TUR 2: tek ayak denge, derin hamle
el(2, profil("Standing Knee Lift Tall Arms", 185, [178, 178], [176, 176], [100, -40], [0, 0]))
el(2, profil("Warrior Lean Arms Forward", 110, [100, 100], [98, 98], [60, 0], [-35, -35]))
el(2, profil("Half Lever One Arm", 120, [130, 130], [-20, -20], [0, 0], [-60, -60]))
el(2, on("Tree Arms Low V", "lowv", "lowv", "tog", "kneein"))
el(2, on("Side Leg Lift Arms Up", "up", "up", "tog", [70, 70], govde=165))
el(2, profil("Deep Lunge Arms Back Up", 150, [-150, -150], [-148, -148], [95, 0], [-60, -60]))
el(2, profil("Skater Balance", 120, [80, 80], [-80, -80], [30, -60], [-60, -90]))
el(2, on("Goddess Twist Elbows", "flex", "cactus", "goddess", "goddess", govde=172))
el(2, profil("Kneel One Knee Arms Up", 180, [178, 178], [176, 176], [90, 0], [0, -90]))
el(2, profil("Kneel Lean Back Hands Hips", 205, [-40, -100], [-38, -98], [0, -90], [0, -90]))
el(2, on("Low Squat Hands Chest", "chest", "chest", "goddess", "goddess"))
el(2, profil("Chair Arms Up", 160, [170, 170], [168, 168], [70, -10], [68, -12]))
el(2, profil("Runner Lunge Hands Low", 110, [20, 20], [18, 18], [100, 0], [-60, -60]))
el(2, on("Star Tilt One Leg", [-120, -120], [120, 120], [-5, -5], [50, 50], govde=160))
el(2, profil("Kick Forward Arms Back", 170, [-50, -50], [-48, -48], [80, 80], [0, 0]))
el(2, profil("Long Lunge Arms Forward Back", 165, [100, 100], [-80, -80], [85, 0], [-45, -45]))
# ---- TUR 3: yer, diz, plank
el(3, profil("High Plank", 100, [0, 0], [0, 0], [-85, -85], [-87, -87]))
el(3, profil("Down Dog", 40, [35, 35], [33, 33], [-30, -30], [-32, -32]))
el(3, profil("Seated Boat Arms Up", 205, [178, 178], [176, 176], [130, 130], [128, 128]))
el(3, profil("Seated Fold Arms Forward", 120, [95, 95], [93, 93], [90, 90], [88, 88]))
el(3, profil("Cobra Arms Straight", 140, [5, 5], [3, 3], [-90, -90], [-88, -88]))
el(3, profil("Table Top Arm Leg Reach", 95, [90, 90], [0, 0], [0, -90], [-90, -90]))
el(3, profil("Camel Prep Hands Back", 220, [-40, -40], [-38, -38], [0, -90], [0, -90]))
el(3, profil("Low Lunge Arms Up Arch", 200, [175, 175], [173, 173], [95, 0], [-60, -150]))
el(3, profil("Seated One Leg Hold Up", 180, [150, 150], [0, 0], [160, 160], [90, 90]))
el(3, profil("Kneel Leg Forward Fold", 120, [100, 100], [98, 98], [90, 90], [0, -90]))
el(3, profil("Crescent Kneel Back Arch", 210, [-150, -150], [-148, -148], [95, 0], [0, -90]))
el(3, profil("Seated Twist Arm Back", 185, [60, 60], [-120, -120], [90, 90], [88, 88]))
el(3, profil("Kneel Hands Floor Leg Back Up", 100, [0, 0], [0, 0], [0, -90], [-110, -160]))
el(3, profil("Crouch Hands Ankles", 70, [5, 5], [3, 3], [100, -60], [98, -62]))
# ---- TUR 4: esneklik finali
el(4, profil("Bow Pull Tall", 130, [110, 110], [-150, -170], [0, 0], [-100, -170]))
el(4, profil("Arabesque Low Arms Forward", 120, [110, 110], [108, 108], [0, 0], [-60, -60]))
el(4, profil("Kneeling Leg Hold Behind", 175, [178, 178], [-160, -170], [0, -90], [-20, -170]))
el(4, profil("Lunge Back Foot Hold", 190, [-160, -160], [-150, -160], [95, 0], [0, -170]))
el(4, on("Side Leg Hold High", "up", [95, 95], "tog", [100, 100], govde=165))
el(4, profil("Warrior Three Arms Back", 92, [-80, -80], [-78, -78], [0, 0], [-90, -90]))
el(4, profil("Seated Boat One Leg", 210, [100, 100], [98, 98], [140, 140], [60, 0]))
el(4, profil("Front Lunge Twist Arms Wide", 180, [90, 90], [-90, -90], [90, 0], [-50, -50]))
el(4, profil("Standing Toe Grab Forward", 175, [95, 95], [-40, -40], [95, 95], [0, 0]))
el(4, profil("Lunge Arms Up Back Heel Up", 185, [170, 170], [168, 168], [90, 0], [-60, -160]))
el(4, profil("Archer Lunge", 175, [90, 90], [-90, 90], [90, 0], [-45, -45]))
el(4, profil("Dancer Arms Up Leg Back", 160, [178, 178], [176, 176], [0, 0], [-40, -150]))
el(4, profil("High Kick Leg Hold", 185, [150, 150], [-60, -60], [130, 130], [0, 0]))
el(4, profil("Low Lunge Hands Floor Back Arm Up", 120, [0, 0], [-150, -150], [100, 0], [-60, -60]))

# ---- HAVUZ: yedek kombinasyonlar (secici --havuz ile kullanir; once EL)
KOL = {"V": "v", "W": "w", "Cactus": "cactus", "Reach": "up", "T": "t", "Head": "head", "Flex": "flex", "Low": "lowv",
       "Hip": "hip", "Diag": "up45", "Swing": [-150, -110], "Hook": [-130, -40], "Salute": [-100, 140], "Cross": [-20, 110]}
BAC = {"Wide": ("wide", "wide"), "Goddess": ("goddess", "goddess"), "Knee": ("tog", "kneeup"), "Tree": ("tog", "kneein"),
       "Leg Out": ("straight", "tog"), "Kick": ("tog", [55, 55]), "Lunge": ("lunge", [30, 30]), "Curtsy": ("curtsy", "softknee")}
KELIME = ["Mirrorball", "Glitter", "Groove", "Boogie", "Funk", "Spotlight", "Velvet", "Sequin", "Neon", "Dancefloor",
          "Strobe", "Plush", "Fever", "Shimmy", "Hustle", "Bassline", "Sparkle", "Roller", "Jukebox", "Vinyl"]
HAVUZ, adlar = [], set()


def ekle(tur, p):
    k = p["ad"].lower()
    if k not in adlar:
        adlar.add(k); p["tur"] = tur; HAVUZ.append(p)


kk, bb = list(KOL), list(BAC)
while len(HAVUZ) < 60:     # tur 1-2: onden ayakta asimetrik
    a, b, c = rnd.choice(kk), rnd.choice(kk), rnd.choice(bb)
    if a == b:
        continue
    g = rnd.choice([165, 172, 180, 188, 195])
    p = on(f"{rnd.choice(KELIME)} {a} {b} {c}", KOL[a], KOL[b], BAC[c][0], BAC[c][1], govde=g)
    ekle(1 if c in ("Wide", "Goddess", "Curtsy", "Lunge") else 2, p)
while len(HAVUZ) < 130:    # tur 2-4: profil denge/esneklik
    gv = rnd.choice([60, 90, 110, 130, 160, 185, 205])
    ok = [rnd.choice([178, 150, 120, 90, 45, -40, -90, -150]) for _ in range(2)]
    on_b = rnd.choice([[0, 0], [90, -10], [110, -40], [70, 0], [0, -90], [45, 45], [95, 95]])
    ar_b = rnd.choice([[0, 0], [-70, -70], [-90, -90], [-40, -40], [-110, -170], [0, -90], [-60, -150]])
    if on_b == [0, -90] and ar_b == [0, -90]:
        continue
    yer = on_b in ([0, -90], [95, 95]) or ar_b == [0, -90]
    zor = gv < 120 or ar_b[0] <= -70
    p = profil(f"{rnd.choice(KELIME)} Flow {len(HAVUZ)}", gv, [ok[0], ok[0] - 2], [ok[1], ok[1] - 2], on_b, ar_b)
    ekle(3 if yer else (4 if zor else 2), p)

# ---- ad cakisma kontrolu: defterdeki tum videolar
eski = set()
for f in ("pozlar.json", "pozlar-03.json", "pozlar-04.json", "pozlar-05.json", "pozlar-05-aday.json",
          "pozlar-06.json", "pozlar-06-aday.json"):
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
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "8. video ADAY (REF-059)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-08-aday.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"{len(pozlar)} aday (el {sum(len(l) for l in EL.values())}: " + ", ".join(f"tur{t} {len(l)}" for t, l in EL.items())
      + f"; havuz {len(HAVUZ)}) -> pozlar-08-aday.json")
