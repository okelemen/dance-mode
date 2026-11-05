"""HUMAN TETRIS 18. video (REF-069 TetrisBounce, 2 oyuncu cift / CO-OP) - ikili poz ADAYLARI -> gruplar-18-aday.json.

    python ikili-listesi-kur-18.py

REF-069 dili: TEK duvar, iki kisilik ortak siluet; EASY ayakta ayna pozlar (sirt sirta, kollar havada, iceri kol bagli),
MEDIUM temasli / farkli figurler (kalp, cerceve, karsilikli hamle), HARD biri yerde (diz, plank, oturus) oburu ayakta.
Kullanici karari (5 Kas 2026, B): KALDIRMA / TASIMA YOK, kimse havaya kalkmaz; her figur kendi ayagi/dizi/eli ile yerde.
Yer pozlari 15. videoda onaylanmis acilardan (havada okunmamis) turetildi. Aci dili poz-listesi-kur.py.
Aday sayisi 24'ten fazla: maskeler kontakta "havada" / tekrar elemesinden sonra 24 secilir (olc-poz-iou.py, 7/11/13/15 ikililerine, esik 0,78).
Maskeler Actions'ta: tetris-varlik.yml yalniz=grup, ek="--mod cadi --gruplar 03-motor/tetris-pvp/gruplar-18-aday.json".
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
_g = {"__file__": os.path.join(BURA, "ikili-listesi-kur-15.py")}
exec(compile(open(os.path.join(BURA, "ikili-listesi-kur-15.py"), encoding="utf-8").read().split("KNEEL = [")[0],
             "ikili-listesi-kur-15.py", "exec"), _g)
on, profil, ayna_poz, ikili = _g["on"], _g["profil"], _g["ayna_poz"], _g["ikili"]
KNEEL = [0, -90]


def sirt(ad, P, temas=0.0):
    """sirt sirta: soldaki ekran soluna, sagdaki ekran sagina bakar"""
    return ikili(ad, ayna_poz(P), P, temas=temas)


def karsi(ad, P, Q=None, temas=("el", "el")):
    """karsilikli: soldaki saga, sagdaki sola bakar"""
    return ikili(ad, P, ayna_poz(Q or P), temas=temas)


EASY = [  # ayakta, ayna
    sirt("Back To Back Peace Up", profil("", 178, [160, 175], [-15, -15], [0, 0], [-4, -4])),
    ikili("Outer Arm Up Hand Link", on("", "up", [12, 8], "tog", "sidetap")),
    ikili("Butterfly Lean Out", on("", [-100, -100], [60, 60], "sidetap", "tog", govde=200)),
    ikili("Roof Hands Wide Stance", on("", "lowv", [150, 150], "wide", "wide")),
    ikili("Shoulder Hug Hip Hand", on("", "hip", [100, 100], "tog", "softknee", govde=172), temas=0.0),
    ikili("Inner Knee Lift Arms Up", on("", "up", "up", "tog", "kneeup"), temas=0.3),
    ikili("Outer Tree Joined Palms", on("", [-150, -150], [160, 165], [-85, -20], "tog")),
    ikili("Star Outer Low Link", on("", "up45", [30, 30], "wide", "wide")),
    # kontak 1 elemesinden sonra (6 ve 7 havada oturuyor gibi okundu)
    sirt("Back To Back Arms T", profil("", 178, [90, 90], [-90, -90], [0, 0], [-4, -4])),
    ikili("Twin Wide V Low Link", on("", "v", [20, 15], "wide", "wide")),
    ikili("Side Bend Toward Arch", on("", [-150, -120], "down", "tog", "sidetap", govde=160), temas=0.1),
]

MEDIUM = [  # temasli / farkli figurler
    ikili("Heart Lunge Outer T", on("", "t", [150, 105], "lunge", "tog", govde=168)),
    sirt("Back To Back Wall Sit", profil("", 180, [80, 80], [70, 70], [85, 0], [85, 0])),
    karsi("Warrior Three Fingertips", profil("", 95, [95, 95], [-20, -20], [0, 0], [-88, -88])),
    karsi("Facing Lunge High Five", profil("", 178, [150, 150], [-30, -30], [62, 0], [-40, -40])),
    ikili("Bow And Cheer", profil("", 100, [30, 30], [20, 20], [5, 5], [-5, -5]), on("", "up", "up", "tog", "tog"), temas=0.2),
    ikili("Frame Arms Cactus Link", on("", "cactus", "t", "wide", "tog")),
    sirt("Back To Back Side Lunge", profil("", 178, [176, 180], [-20, -20], [62, 0], [-40, -40])),
    ikili("Crossed Reach Wide V", on("", "v", [140, 140], "wide", "goddess")),
    ikili("Outer Side Lunge Inner Palms Up", on("", [-30, -30], [160, 165], [-70, -5], "tog")),   # kontak 1 sonrasi
]

HARD = [  # biri yerde (diz / plank / oturus), oburu ayakta
    ikili("Half Kneel Crown And Star", profil("", 180, [175, 178], [170, 175], [85, 0], KNEEL), on("", "v", "v", "wide", "wide"), temas=0.1),
    ikili("Plank And Standing Star", profil("", 80, [85, 85], [0, 0], [-80, -80], [-78, -78]), on("", "up45", "up45", "wide", "wide"), temas=0.15),
    ikili("Seated Lean And Bow Link", profil("", 215, [-30, -30], [-28, -28], [85, 85], [83, 83]),
          ayna_poz(profil("", 120, [60, 60], [58, 58], [15, 15], [-15, -15]))),
    ikili("Kneel Stretch And Side Bend", profil("", 175, [130, 100], [-30, -30], KNEEL, KNEEL),
          on("", [-205, -235], "down", "sidetap", "tog", govde=155), temas=0.1),
    ikili("Low Squat And Tall Reach", on("", "w", "w", [-80, 10], [80, -10]), on("", "up", "up", "tog", "tog"), temas=0.15),
    ikili("Side Lunge And Kneel T", on("", [-170, -170], [150, 90], [-75, -75], [72, -5]),
          ayna_poz(profil("", 178, [90, 90], [-90, -90], KNEEL, KNEEL)), temas=0.1),
    karsi("Half Kneel Offer Hand", profil("", 180, [70, 70], [-20, -20], [85, 0], KNEEL),
          profil("", 168, [40, 40], [-10, -10], [0, 0], [-5, -5])),
    sirt("Back To Back Half Kneel Arms Up", profil("", 180, [175, 178], [168, 175], [85, 0], KNEEL)),
    ikili("Kneel T And Warrior Two", profil("", 178, [90, 90], [-90, -90], KNEEL, KNEEL), on("", "t", "t", "straight", "lunge"), temas=0.1),
    ikili("Wide Lunge Down And Tree", on("", [-172, -172], [10, 10], [-50, -50], [50, 50], govde=150),
          on("", [160, 165], [-150, -150], "tog", [85, 20]), temas=0.15),
    # kontak 1 sonrasi (19 ve 21 havada okundu)
    karsi("Half Kneel Facing Arch", profil("", 175, [150, 150], [-20, -20], [85, 0], KNEEL)),
    ikili("Kneel Arms Up And Standing Bow", profil("", 178, [175, 178], [170, 175], KNEEL, KNEEL),
          ayna_poz(profil("", 120, [60, 60], [58, 58], [15, 15], [-15, -15])), temas=0.2),
]

G = {}
for tur, liste in ((1, EASY), (2, MEDIUM), (3, HARD)):
    for g in liste:
        k = g["ad"].lower().replace(" ", "-")
        assert k not in G, k
        for i, f in enumerate(g["figurler"]):
            f["ad"] = f"{g['ad']} {'AB'[i]}"
        g["tur"] = tur
        G[k] = g
json.dump({"_not": "18. video (REF-069) CO-OP ikili poz ADAYLARI, kaldirma yok. Figurler soldan saga; temas [sol eklem, sag eklem], 'yan' ya da bosluk (m).",
           "gruplar": G}, open(os.path.join(BURA, "gruplar-18-aday.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"gruplar-18-aday.json: {len(G)} aday (EASY {len(EASY)}, MEDIUM {len(MEDIUM)}, HARD {len(HARD)})")
