"""HUMAN TETRIS 35. video (REF-087 HumanWarmUp _J_wvFI8y_0, 2P CO-OP eş poz) - ikili poz ADAYLARI -> gruplar-35-aday.json.

    python ikili-listesi-kur-35.py

Neden: 7/11/13/15/18 ikili havuzundan 23, 27, 28 kullanıldı; kalan 9 aday (poz-sec-35 sayımı, 20 Kas 2026) 24 duvara yetmiyor.
REF-087 dili: iki kişi TEK eş poz; çoğu AYNA simetrik (iç kollar yukarıda birleşir + geniş çömelme / hamle, eğilip baş başa
elmas, omuz omuza, sırt sırta), bir kısmı karşılıklı (yüz yüze sandalye / savaşçı avuç avuca), zor olanlarda biri yarım diz
çökük öbürü ayakta. Kullanıcı kararı (5 Kas 2026, 18): KALDIRMA / TAŞIMA YOK, kimse havaya kalkmaz; her figür kendi
ayağı / dizi ile yerde. Açı dili poz-listesi-kur.py (ikili-listesi-kur-15/18 yardımcıları).
Aday sayısı 24'ten fazla: maskeler kontakta havada / tekrar elemesinden sonra poz-sec-35.py seçer (eski ikililere IoU < 0,78).
Maskeler Actions'ta: tetris-varlik.yml yalniz=grup, ek="--mod cadi --gruplar 03-motor/tetris-pvp/gruplar-35-aday.json".
"""
import glob, json, os

BURA = os.path.dirname(os.path.abspath(__file__))
_g = {"__file__": os.path.join(BURA, "ikili-listesi-kur-15.py")}
exec(compile(open(os.path.join(BURA, "ikili-listesi-kur-15.py"), encoding="utf-8").read().split("KNEEL = [")[0],
             "ikili-listesi-kur-15.py", "exec"), _g)
on, profil, ayna_poz, ikili = _g["on"], _g["profil"], _g["ayna_poz"], _g["ikili"]
KNEEL = [0, -90]
YARIM_DIZ = ([0, "geri"], [70, 0])          # on(): ekran-solu bacak dizde, ekran-sagi bacak onde (poz-listesi-kur Half Kneel)


def sirt(ad, P, temas=0.0):
    """sirt sirta: soldaki ekran soluna, sagdaki ekran sagina bakar"""
    return ikili(ad, ayna_poz(P), P, temas=temas)


def karsi(ad, P, Q=None, temas=("el", "el")):
    """karsilikli: soldaki saga, sagdaki sola bakar"""
    return ikili(ad, P, ayna_poz(Q or P), temas=temas)


# on(ad, sagKol=ekran-solu kol, solKol=ekran-sagi kol, ...): soldaki figur icin solKol = IC kol (esine yakin)
EASY = [  # ayakta, ayna
    ikili("Inner Hands High Outer Hip", on("", "hip", "up", "tog", "tog")),
    ikili("Palm Press Chest Height", on("", "down", "t", "tog", "tog")),
    ikili("Outer V Inner Low Link", on("", "up45", "lowv", "wide", "wide")),
    ikili("Shoulder To Shoulder Cactus", on("", "cactus", "down", "tog", "tog"), temas="yan"),
    ikili("Inner Elbow Hook Outer Up", on("", "up", "flex", "tog", "tog"), temas=0.05),
    ikili("Joined Arch Horse Stance", on("", "head", "up", "horse", "horse")),
    ikili("Side Step Outer T Inner Up", on("", "t", "up45", "sidetap", "tog")),
    sirt("Back To Back Prayer Reach", profil("", 178, [176, 178], [176, 178], [0, 0], [-4, -4])),
    ikili("Outer Hand Head Inner Low Link", on("", "head", "lowv", "tog", "softknee")),
    ikili("Wide Stance Outer Flex Link", on("", "flex", "t", "wide", "wide")),
]

MEDIUM = [  # temasli / farkli figurler (REF-087 kapagi: genis comelme + ic eller yukarida)
    ikili("Wide Squat Inner High Five", on("", "hip", "up", "goddess", "goddess")),
    ikili("Leaning Diamond Hands", on("", "hip", "up", "straight", "tog", govde=165)),
    ikili("Side Lunge Inner High Five", on("", "lowv", "up", "lunge", "tog")),
    ikili("Wide Squat Crossed Diagonal", on("", "w", "up45", "goddess", "goddess")),
    ikili("Outer Knee Lift Inner Link", on("", "v", "t", "kneeup", "tog")),
    ikili("Lunge Cactus Frame", on("", "cactus", "up", "lunge", "softknee")),
    ikili("Side Bend Away Inner Link", on("", [-150, -150], "t", "tog", "sidetap", govde=200)),
    karsi("Facing Chair Palms", profil("", 160, [90, 90], [85, 85], [40, -30], [40, -30])),
    karsi("Facing Warrior Reach", profil("", 170, [100, 100], [-60, -60], [60, 0], [-40, -40])),
    ikili("Mirror Warrior Two Inner Up", on("", "t", "up", "lunge", "straight")),
    ikili("Horse Stance Outer Up Inner Elbow", on("", "up", "elbowdown", "horse", "horse"), temas=0.05),
]

HARD = [  # biri yarim diz / derin comelme, obuu ayakta ya da ikisi de alcak; kimse havada degil
    ikili("Half Kneel And Lunge Link", on("", "t", "t", *YARIM_DIZ), on("", "up", "t", "lunge", "tog"), temas=0.1),
    ikili("Wide Squat And Side Lunge", on("", "cactus", "cactus", "goddess", "goddess"), on("", "t", "up45", "tog", "lunge"), temas=0.1),
    ikili("Deep Squat Twin Reach Up", on("", "up", "up", "goddess", "goddess"), temas=0.1),
    karsi("Half Kneel Facing Palms", profil("", 178, [90, 90], [-20, -20], [85, 0], KNEEL)),
    sirt("Back To Back Half Kneel T", profil("", 178, [90, 90], [-90, -90], [85, 0], KNEEL)),
    ikili("Half Kneel V And Standing Diagonal", on("", "v", "v", *YARIM_DIZ), on("", "up45", [55, 55], "straight", "tog"), temas=0.15),
    ikili("Low Lunge And Tall Diagonal", profil("", 150, [150, 150], [140, 140], [70, 0], [-40, -45]),
          on("", "up45", [55, 55], "straight", "tog"), temas=0.15),
    ikili("Twin Wide Lunge Arms Up", on("", "up", "up", "lunge", "straight"), temas=0.1),
    ikili("Half Kneel Cactus And Wide Squat", on("", "cactus", "cactus", *YARIM_DIZ), on("", "w", "w", "goddess", "goddess"), temas=0.15),
    karsi("Facing Low Lunge Palms", profil("", 160, [110, 110], [-30, -30], [70, 0], [-40, -45])),
]

ESKI = set()
for f in glob.glob(os.path.join(BURA, "gruplar-*.json")):
    if "35" in os.path.basename(f):
        continue
    ESKI |= set(json.load(open(f, encoding="utf-8"))["gruplar"])
G = {}
for tur, liste in ((1, EASY), (2, MEDIUM), (3, HARD)):
    for g in liste:
        k = g["ad"].lower().replace(" ", "-")
        assert k not in G and k not in ESKI, k
        for i, f in enumerate(g["figurler"]):
            f["ad"] = f"{g['ad']} {'AB'[i]}"
        g["tur"] = tur
        G[k] = g
assert len(ESKI) > 100, len(ESKI)          # bos sayim = kirik komut
json.dump({"_not": "35. video (REF-087) CO-OP ikili es poz ADAYLARI, kaldirma yok. Figurler soldan saga; temas [sol eklem, sag eklem], 'yan' ya da bosluk (m).",
           "gruplar": G}, open(os.path.join(BURA, "gruplar-35-aday.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"gruplar-35-aday.json: {len(G)} aday (EASY {len(EASY)}, MEDIUM {len(MEDIUM)}, HARD {len(HARD)}), eski ad {len(ESKI)}")
