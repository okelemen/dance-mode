"""HUMAN TETRIS 10. video (REF-061 HumanWarmUp, 1 oyuncu, ~5 dk) - poz ADAY havuzu -> pozlar-10-aday.json.
Maskeler Actions'ta (tetris-varlik.yml, yalniz=poz, pozlar=03-motor/tetris-pvp/pozlar-10-aday.json), sonra poz-sec-10.py
olcumle (eski videolarin maskelerine + video icine aynali IoU) 29 poz secer (REF-061: 19 tur / 3:15 -> 29 tur x 10 sn).

    python poz-aday-10.py

REF-061 dili: yoga + esneme + dovus (yan tekme, yuksek tekme, hamle yumruk, sinav/plank, dansci, yan hamle, oturus burgu,
kayik, cocuk). Tur yok; siralama icin 3 grup: 1 ayakta, 2 hamle/tek ayak/tekme, 3 yer (el-ayak-diz yere acikca basan).
Guvenlik (TALIMATLAR §4): amuda kalkma, tam kopru, bas/omuz durusu, ayakta spagat, havada okunan poz yok.
Adlar defterdeki hicbir pozla cakismaz (assert).
"""
import json, os, random

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]
rnd = random.Random(61)

EL = {1: [], 2: [], 3: []}


def el(tur, p):
    p["ad"] = "Daily " + p["ad"]
    EL[tur].append(p)


# ---- GRUP 1: ayakta (isinma, uzanma, yana egilme, dovus durusu)
el(1, on("Sun Salute Reach", "up", "up", "softknee", "softknee", govde=186))
el(1, on("Side Stretch Arm Over", [-165, -150], "hip", "wide", "wide", govde=196))
el(1, on("Fighter Guard Wide", "chest", "chest", "horse", "horse"))
el(1, on("Cross Punch Stance", [-88, -88], "chest", "lunge", "straight", govde=176))
el(1, on("Uppercut Squat", [-160, 120], "chest", "horse", "horse"))
el(1, on("Hip Circle Hands Waist", "hip", "hip", "wide", "wide", govde=170))
el(1, on("Shoulder Roll Arms Back", [-20, -60], [-20, -60], "tog", "tog"))
el(1, on("Knee Lift Arms Down Push", "lowv", "lowv", "kneeup", "tog"))
el(1, on("Reach Up Toe Point", "up45", "t", "tog", "sidetap", govde=178))
el(1, profil("Forward Swing Arms", 170, [100, 100], [-40, -40], [5, 5], [-5, -5]))
el(1, profil("Standing Calf Stretch Hands Wall", 160, [110, 110], [108, 108], [20, 20], [-30, -30]))
el(1, on("Big Stretch Wide V", "v", "v", "goddess", "goddess"))
el(1, on("One Arm Sky Squat", "up", "hip", "horse", "horse"))
el(1, on("Lateral Reach Low Stance", [-110, -110], "down", "goddess", "goddess", govde=165))
# ---- GRUP 2: hamle, tek ayak, tekme
el(2, on("Side Kick Guard", "chest", "chest", "tog", [80, 80], govde=158))
el(2, profil("Front Kick High Guard", 172, [80, 150], [78, 148], [95, 95], [0, 0]))
el(2, profil("Back Kick Lean", 120, [60, 160], [58, 158], [0, 0], [-70, -70]))
el(2, on("Lunge Punch Forward", [-90, -90], [-30, -150], "lunge", "straight"))
el(2, profil("Dancer Hold Arm Forward", 120, [120, 120], [-150, -170], [0, 0], [-50, -150]))
el(2, on("Side Lunge Hands Prayer", [-20, 100], [-20, 100], "goddess", "straight"))
el(2, on("Warrior Two Gaze Up Arm", "up45", "t", "lunge", "straight"))
el(2, profil("Crescent Lunge Arms V", 185, [168, 168], [150, 150], [95, 0], [-40, -40]))
el(2, profil("Lunge Twist Arms T", 175, [90, 90], [-90, -90], [95, 0], [-40, -40]))
el(2, on("Flamingo Arms Up", "up", "up", "tog", "kneeup"))
el(2, profil("Warrior Three Arms Back", 95, [-20, -20], [-18, -18], [0, 0], [-85, -85]))
el(2, profil("Standing Quad Stretch Reach", 180, [160, 160], [-150, -170], [0, 0], [-10, -170]))
el(2, on("Low Side Lunge Arms Front", [-60, -60], [-60, -60], "goddess", "straight", govde=170))
el(2, profil("Deep Lunge Hands Floor", 120, [10, 10], [8, 8], [110, -10], [-50, -50]))
# ---- GRUP 3: yer (el / diz / ayak acikca yerde)
el(3, profil("Push Up High", 92, [0, 0], [0, 0], [-85, -85], [-87, -87]))
el(3, profil("Plank Forearms", 92, [0, 90], [0, 90], [-86, -86], [-88, -88]))
el(3, profil("Knee Push Up", 110, [0, 0], [0, 0], [0, -90], [0, -90]))
el(3, profil("Bear Crawl Hold", 100, [0, 0], [0, 0], [60, -60], [58, -62]))
el(3, profil("Sprinter Start", 95, [5, 5], [3, 3], [120, -40], [-60, -60]))
el(3, profil("Seated Twist Arm Back", 185, [-40, -40], [80, 80], [90, 90], [100, -60]))
el(3, profil("Boat Arms Up", 215, [160, 160], [158, 158], [130, 130], [128, 128]))
el(3, profil("Seated Side Reach", 195, [-165, -165], [-20, -20], [90, 90], [90, 90]))
el(3, profil("Child Pose Arms Back", 20, [-170, -170], [-168, -168], [120, -60], [118, -62]))
el(3, profil("Cat Back Round", 95, [0, 0], [0, 0], [0, -90], [0, -90]))
el(3, profil("Bird Dog Reach", 100, [90, 90], [0, 0], [0, -90], [-90, -90]))
el(3, profil("Kneeling Lunge Arms Up", 185, [175, 175], [173, 173], [95, 0], [0, -90]))
el(3, profil("Low Squat Hands Floor", 150, [30, 30], [28, 28], [120, -120], [118, -122]))
el(3, profil("Seated Butterfly Hands Feet", 175, [30, 30], [28, 28], [60, -90], [58, -92]))
el(3, profil("Down Dog Heels Up", 40, [40, 40], [38, 38], [-40, -40], [-42, -42]))
el(3, profil("Tabletop Arm Reach", 95, [90, 90], [0, 0], [0, -90], [0, -90]))
el(3, profil("Side Plank Knee Down Arm Up", 115, [0, 0], [178, 178], [0, -90], [-20, -20]))

# ---- HAVUZ: yedek kombinasyonlar (secici --havuz ile kullanir; once EL)
KOL = {"V": "v", "W": "w", "Cactus": "cactus", "Reach": "up", "T": "t", "Head": "head", "Flex": "flex", "Low": "lowv",
       "Hip": "hip", "Diag": "up45", "Halo": [-160, 120], "Comet": [-110, -170], "Wave": [-70, -130], "Hug": [-40, 100]}
BAC = {"Wide": ("wide", "wide"), "Horse": ("horse", "horse"), "Knee": ("tog", "kneeup"), "Tree": ("tog", "kneein"),
       "Leg Out": ("straight", "tog"), "Kick": ("tog", [60, 60]), "Lunge": ("lunge", "straight"), "Tap": ("sidetap", "tog")}
KELIME = ["Morning", "Sunrise", "Fresh", "Easy", "Calm", "Bright", "Breeze", "Flow", "Spark", "Steady",
          "Light", "Wake", "Glow", "Smooth", "Balance", "Daily", "Rise", "Pulse", "Lift", "Ready"]
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
          "pozlar-06.json", "pozlar-06-aday.json", "pozlar-08.json", "pozlar-08-aday.json", "pozlar-09.json", "pozlar-09-aday.json"):
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
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "10. video ADAY (REF-061)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-10-aday.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"{len(pozlar)} aday (el {sum(len(l) for l in EL.values())}: " + ", ".join(f"tur{t} {len(l)}" for t, l in EL.items())
      + f"; havuz {len(HAVUZ)}) -> pozlar-10-aday.json")
