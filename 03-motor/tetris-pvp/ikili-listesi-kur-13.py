"""HUMAN TETRIS 13. video (REF-064 HumanWarmUp, CO-OP 2 oyuncu) - 25 ikili poz -> gruplar-13.json + duvar-listesi-13.json.

    python ikili-listesi-kur-13.py

REF-064 dili: TEK duvar, iki kisilik ortak delik; cogu AYNALI (bas arkasi eller, ayak bulusturan tekme, tepede birlesen eller,
sirt sirta comelme, karsilikli kol guresi). Guvenlik (TALIMATLAR §4): kaldirma / bas asagi yok (REF amuda kalkma alinmadi),
her figur kendi ayagi/dizi/eli ile yerde. Aci dili poz-listesi-kur.py. Temas [sol eklem, sag eklem], "yan" ya da sayi = bosluk (m).
Tekrar kontrolu: olc-poz-iou.py, 7. ve 11. videonun ikili maskelerine, esik 0,78.
Maskeler Actions'ta: tetris-varlik.yml yalniz=grup, ek="--mod cadi --gruplar 03-motor/tetris-pvp/gruplar-13.json".
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]


def ayna_poz(P):
    Q = {"ad": P["ad"], "yon": {"on": "on", "sag": "sol", "sol": "sag"}[P.get("yon", "on")]}
    neg = lambda v: [x if x == "geri" else -x for x in v]
    Q["govde"] = -P.get("govde", 180); Q["bas"] = -P.get("bas", 0)
    for a, b in (("sagKol", "solKol"), ("sagBacak", "solBacak")):
        if a in P: Q[b] = neg(P[a])
        if b in P: Q[a] = neg(P[b])
    return Q


def ikili(ad, sol, sag=None, temas=("el", "el")):
    """sol = ekranin solundaki oyuncu; sag verilmezse ayna; temas: eklem cifti, "yan" ya da bosluk (m)"""
    if sag is None:
        sag = ayna_poz(sol)
    t = temas if (temas == "yan" or isinstance(temas, (int, float))) else list(temas)
    return {"ad": "Duo " + ad, "figurler": [sol, sag], "temas": [t]}


KNEEL = [0, -90]                 # profilde diz cokme
AYAKTA = [  # ayakta - herkes yapar
    ikili("Hands Behind Head Wide Stance", on("", "head", "head", "wide", "wide"), on("", "head", "head", "wide", "wide"), temas=0.35),  # REF t32
    ikili("Peak Lean Palms Overhead", profil("", 158, [150, 150], [148, 148], [12, 12], [-22, -22])),                 # REF t78
    ikili("Cactus Arms Goddess", on("", "cactus", "cactus", "goddess", "goddess"), on("", "cactus", "cactus", "goddess", "goddess"), temas=0.3),
    ikili("Side Bend Arc Outer Arm Up", on("", [-155, -155], [60, 60], "tog", "straight", govde=165)),
    ikili("High Lunge Palm Press", profil("", 165, [145, 145], [-40, -40], [62, 0], [-42, -42])),
    ikili("Forward Fold Hand Link", profil("", 100, [90, 90], [88, 88], [0, 0], [-8, -8])),
    ikili("Star Stance Fingertip Touch", on("", "t", "t", "wide", "wide")),
    ikili("Y Arms Step Out", on("", "up45", "up45", "straight", "tog"), on("", "up45", "up45", "tog", "straight"), temas=0.3),
    ikili("Side Lunge Low Hand Link", on("", "lowv", [65, 65], "lunge", "straight")),
]

TEK_AYAK = [  # tek ayak denge / tekme
    ikili("Tree Pose Arms Overhead", on("", "up", "up", "tog", "kneein"), on("", "up", "up", "tog", "kneein"), temas=0.3),  # REF kapak
    ikili("Knee Raise Inner Hand Link", on("", "down", [90, 90], "tog", "kneeup")),
    ikili("Airplane Side Kick Feet Meet", on("", "t", "t", "tog", [72, 72]), temas=("ayak", "ayak")),                  # REF t40
    ikili("Flamingo Knee Up Hand Link", profil("", 178, [90, 90], [-30, -30], [85, -5], [0, 0])),
    ikili("Warrior Three Arms Back", profil("", 92, [-15, -15], [-13, -13], [0, 0], [-90, -90]),
          profil("", 92, [-15, -15], [-13, -13], [0, 0], [-90, -90]), temas=0.3),
    ikili("Dancer Pose Hand Link", profil("", 142, [112, 112], [-140, -140], [0, 0], [-60, -150])),
    ikili("Tilted T Leg Lift", on("", [-175, -175], "t", "tog", [62, 62], govde=200), temas=("ayak", "ayak")),
    ikili("Knee Tuck Arm Up Inner Link", on("", "up", [100, 100], "tog", [78, 20])),
]

YER = [  # diz / yer (el-diz-ayak yerde)
    ikili("Back To Back Squat", ayna_poz(profil("", 150, [90, 90], [88, 88], [100, -15], [98, -17])),
          profil("", 150, [90, 90], [88, 88], [100, -15], [98, -17]), temas=0.05),                                     # REF t112
    ikili("Kneeling Arm Wrestle", profil("", 185, [70, 100], [-20, -20], KNEEL, KNEEL)),                               # REF t185
    ikili("Seated Recline Bent Reach",                                                                                 # REF t104, asimetrik
          profil("", 205, [110, 110], [-140, -140], [90, 90], [70, -20]),
          ayna_poz(profil("", 130, [110, 110], [-70, -70], [30, -30], [-30, -30]))),
    ikili("Low Lunge Palms High", profil("", 185, [160, 160], [150, 150], [80, 0], [0, -90])),
    ikili("Boat Pose Feet Meet", profil("", 210, [90, 90], [88, 88], [50, 50], [48, 48]), temas=("ayak", "ayak")),
    ikili("Kneeling Chest Open", profil("", 200, [-50, -50], [-48, -48], KNEEL, KNEEL), temas=0.15),
    ikili("Plank Facing", profil("", 75, [0, 0], [2, 2], [-75, -75], [-73, -73]), temas=0.1),
    ikili("Garland Squat Side By Side", on("", "chest", "chest", [-80, 10], [80, -10]),
          on("", "chest", "chest", [-80, 10], [80, -10]), temas=0.15),
]

G, duvar = {}, []
for tur, liste in ((1, AYAKTA), (2, TEK_AYAK), (3, YER)):
    for g in liste:
        k = g["ad"].lower().replace(" ", "-")
        assert k not in G, k
        for i, f in enumerate(g["figurler"]):
            f["ad"] = f"{g['ad']} {'AB'[i]}"
        G[k] = g
        duvar.append({"tur": tur, "grup": k})
assert len(duvar) == 25
json.dump({"_not": "13. video (REF-064) CO-OP ikili pozlar. Figurler soldan saga; temas [sol eklem, sag eklem], 'yan' ya da bosluk (m).",
           "gruplar": G}, open(os.path.join(BURA, "gruplar-13.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvar, open(os.path.join(BURA, "duvar-listesi-13.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"gruplar-13.json: {len(G)} ikili poz; duvar-listesi-13.json: {len(duvar)} duvar")
