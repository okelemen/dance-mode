"""HUMAN TETRIS 15. video (REF-066 HumanWarmUp, CO-OP 2 oyuncu) - 25 ikili poz -> gruplar-15.json + duvar-listesi-15.json.

    python ikili-listesi-kur-15.py

REF-066 dili: TEK duvar, iki kisilik ortak delik; cogu AYNALI ve bagli (kalp kemeri, ayak bulusturan, plank, yan hamle).
Guvenlik (TALIMATLAR §4): kaldirma / bas asagi yok, her figur kendi ayagi/dizi/eli ile yerde. Aci dili poz-listesi-kur.py.
Temas [sol eklem, sag eklem], "yan" ya da sayi = bosluk (m).
Tekrar kontrolu: olc-poz-iou.py, 7., 11. ve 13. videonun ikili maskelerine, esik 0,78.
Maskeler Actions'ta: tetris-varlik.yml yalniz=grup, ek="--mod cadi --gruplar 03-motor/tetris-pvp/gruplar-15.json".
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
    ikili("Heart Arch Hands On Hips", on("", "hip", [170, 110], "straight", "straight", govde=165)),                 # REF kapak
    ikili("Arc Bend And Side Kick", on("", "lowv", [165, 120], "wide", "wide", govde=160),
          on("", [-90, -90], "up", [-70, -70], "tog"), temas=0.2),                                       # REF t18
    ikili("Warrior Two Fingertip Line", on("", "t", "t", "straight", "lunge")),                                     # REF t50
    ikili("Reverse Warrior Low Link", on("", "up45", "lowv", "straight", "lunge", govde=190)),
    ikili("Bow Forward Hands Clasp", profil("", 120, [60, 60], [58, 58], [15, 15], [-15, -15])),
    ikili("Pike V And Knee Drive", profil("", 45, [40, 40], [38, 38], [-30, -30], [-28, -28]),
          ayna_poz(profil("", 178, [100, 30], [-40, 100], [85, -5], [-5, -5])), temas=0.3),                          # REF t155
    ikili("Guard Step Punch Link", profil("", 178, [90, 90], [-40, 100], [30, -5], [-25, -25]),
          ayna_poz(profil("", 172, [120, 40], [-40, 100], [80, -10], [-5, -5])), temas=0.05),                        # REF t190
    ikili("Wide Horse V Arms", on("", "v", "v", "horse", "horse"), temas=0.3),   # kontak 1: Goddess IoU 0,79
    ikili("Wide Side Stretch Low Link", on("", "up", [45, 45], "wide", "lunge")),
]

TEK_AYAK = [  # tek ayak denge / tekme
    ikili("Side Angle Kick Hand Link", on("", "up45", [80, 80], "tog", [60, 60], govde=195)),
    ikili("Crescent Tiptoe Arms High", on("", "up", "up", "tog", [25, 25], govde=170), temas=0.25),
    ikili("Inner Knee Open Link", on("", [-120, -120], [100, 100], "tog", "kneein")),   # kontak 1: IoU 0,81
    ikili("Stork Side Reach", profil("", 160, [70, 70], [-60, -60], [90, 0], [-5, -5])),
    ikili("Back Kick Front Reach", profil("", 110, [100, 100], [-20, -20], [0, 0], [-70, -70])),
    ikili("Hip Hinge Foot Back Link", profil("", 125, [80, 80], [-30, -30], [5, 5], [-45, -45])),
    ikili("Heel Lift Side Arch", on("", "v", [170, 100], "tog", [45, 45], govde=170)),
    ikili("Outer Leg Swing T Tilt", on("", "t", "t", [-55, -55], "tog", govde=165), temas=0.3),
]

YER = [  # diz / yer (el-diz-ayak yerde)
    ikili("Wide Lunge Hand Down Arm Up", on("", [-172, -172], [10, 10], [-50, -50], [50, 50], govde=150), temas=("ayak", "ayak")),   # REF t44
    ikili("Seated Lean Back Feet Meet", profil("", 215, [-30, -30], [-28, -28], [85, 85], [83, 83]), temas=("ayak", "ayak")),         # REF t62
    ikili("Low Plank Reach Hand Link", profil("", 80, [85, 85], [0, 0], [-80, -80], [-78, -78])),                                    # REF t105
    ikili("Kneeling Side Stretch Link", profil("", 175, [130, 100], [-30, -30], KNEEL, KNEEL)),
    ikili("Half Kneel Forward Reach", profil("", 180, [60, 60], [-60, -60], [85, 0], KNEEL)),
    ikili("Deep Side Lunge Arch Link", on("", [-170, -170], [150, 90], [-75, -75], [72, -5])),                                       # REF t115
    ikili("Long Side Lunge Low Link", on("", [-60, -60], [75, 75], [-75, -75], [55, 0], govde=150)),                                  # REF t130
    ikili("Low Squat W Arms", on("", "w", "w", [-80, 10], [80, -10]), temas=0.2),
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
json.dump({"_not": "15. video (REF-066) CO-OP ikili pozlar. Figurler soldan saga; temas [sol eklem, sag eklem], 'yan' ya da bosluk (m).",
           "gruplar": G}, open(os.path.join(BURA, "gruplar-15.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvar, open(os.path.join(BURA, "duvar-listesi-15.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"gruplar-15.json: {len(G)} ikili poz; duvar-listesi-15.json: {len(duvar)} duvar")
