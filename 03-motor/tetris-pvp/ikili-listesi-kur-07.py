"""TETRIS MODE 7. video (REF-058, 2 oyunculu CO-OP) - 24 ikili poz (3 tur x 8) -> gruplar-07.json + duvar-listesi-07.json.

    python ikili-listesi-kur-07.py

REF-058 dili (Glow Motion "Can You Two Fit? | HUMAN TETRIS x 2 player"): TEK duvar, iki kisilik ORTAK delik, iki oyuncu
birbirine DEGER (kalp eli, el ele kemer, sirt sirta, dans yaslanmasi, ayna diz). Kullanici 23 Eki 2026: "Referanstaki gibi
CO-OP olsun (tek duvar, iki kisilik ortak delik), ~5 dk, 24 duvar." -> tur 1 ayakta, tur 2 hamle/denge/diz, tur 3 yer + esneklik.
Guvenlik (POZ-DUVARI/TALIMATLAR.md §2): KALDIRMA / TASIMA / UST USTE YOK (referanstaki plank-ustunde pozu alinmadi),
amuda kalkma, kopru, bas durusu yok; her figur kendi ayagi/dizi/eli ile yerde, cekme/agirlik verme yok.
Aci dili pozlar.json _not ile ayni (on/profil poz-listesi-kur.py'den). Figurler soldan saga; temas [sol figurun eklemi,
sag figurun eklemi] ya da "yan" (varlik-cadi.py hizala). Sag figur verilmezse solun aynasi.
Maskeler Actions'ta: tetris-varlik.yml yalniz=grup, ek="--mod cadi --gruplar 03-motor/tetris-pvp/gruplar-07.json".
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
    """sol = ekranin solundaki oyuncu (on: ic uzuv = solKol/solBacak; profil sag: partnere bakar); sag verilmezse ayna"""
    if sag is None:
        sag = ayna_poz(sol)
    return {"ad": "Duo " + ad, "figurler": [sol, sag], "temas": [temas if temas == "yan" else list(temas)]}


KNEEL = [0, -90]                           # profilde diz cokme
OTUR_L, OTUR_R = [-78, 75], [78, -75]      # onden bagdas
SIRT = lambda P: ayna_poz(P)               # profil sag'in aynasi: sola bakar (sirti saga) -> sirt sirta

TUR1 = [  # IN SYNC - ayakta, temasli, herkes yapar
    ikili("Heart Hands", on("", "hip", [140, 110], "tog", "tog")),
    ikili("High Ten", on("", [150, 150], [140, 140], "softknee", "tog", govde=170)),
    ikili("Side Lean Arch", on("", "hip", [165, 140], "wide", "tog", govde=160)),
    ikili("Back to Back Reach Up", SIRT(profil("", 180, [178, 178], [176, 176], [0, 0], [-2, -2])),
          profil("", 180, [178, 178], [176, 176], [0, 0], [-2, -2]), temas="yan"),
    ikili("Mirror Knee Hold", on("", "t", [60, 60], "tog", "kneeup")),
    ikili("Shoulder Hug Tree", on("", "up45", [75, 80], "kneein", "tog"), temas=("el", "omuz")),
    ikili("Star Link", on("", "v", [120, 120], "wide", "wide")),
    ikili("Cactus Elbow Link", on("", "cactus", "cactus", "goddess", "goddess"), temas="yan"),
]

TUR2 = [  # TRUST TEST - hamle, tek ayak denge, diz cokme
    ikili("Lunge Arch Bridge", on("", "hip", [160, 130], "lunge", "tog", govde=165)),
    ikili("Warrior Three Hand Link", profil("", 92, [90, 90], [88, 88], [0, 0], [-90, -90])),
    ikili("Kneeling Heart", profil("", 180, [150, 110], [-20, -20], KNEEL, KNEEL)),
    ikili("Tree Palm Press", on("", "up", [90, 90], "kneein", "tog")),
    ikili("Chair Squat Hand Link", profil("", 160, [90, 90], [88, 88], [90, -10], [88, -12])),
    ikili("Side Lunge Shoulder Reach", on("", "t", [70, 60], "lunge", [40, 40]), temas=("el", "omuz")),
    ikili("Dance Dip", profil("", 205, [120, 100], [-130, -130], [20, 10], [-25, -25]),
          ayna_poz(profil("", 160, [100, 60], [60, 30], [35, 0], [-30, -30]))),
    ikili("Knee Up Elbow Touch", on("", "up", "flex", "tog", "kneeup"), temas="yan"),
]

TUR3 = [  # MAX POWER - yer pozlari + esneklik (guvenli surumler)
    ikili("Seated Feet Together Arms Up", profil("", 180, [178, 178], [176, 176], [90, 90], [88, 88]), temas=("ayak", "ayak")),
    ikili("Boat Feet Touch", profil("", 215, [90, 90], [88, 88], [130, 130], [128, 128]), temas=("ayak", "ayak")),
    ikili("Back to Back Chair", SIRT(profil("", 190, [40, 140], [38, 138], [90, 0], [88, -2])),
          profil("", 190, [40, 140], [38, 138], [90, 0], [88, -2]), temas="yan"),
    ikili("Plank Hand Touch", profil("", 100, [90, 90], [0, 0], [-80, -80], [-78, -78])),
    ikili("Kneeling Gate Arch", on("", [-30, -30], [150, 120], [-60, -60], [0, "geri"], govde=155)),
    ikili("Low Lunge Crescent Arch", profil("", 175, [165, 140], [163, 138], [95, 0], [-55, -150])),
    ikili("Seated Side Bend Overhead", on("", [150, 110], [40, 30], OTUR_L, OTUR_R, govde=150)),
    ikili("Pyramid Fold Hand Link", profil("", 80, [60, 60], [58, 58], [25, 25], [-25, -25])),
]

G, duvar = {}, []
for tur, liste in ((1, TUR1), (2, TUR2), (3, TUR3)):
    for g in liste:
        k = g["ad"].lower().replace(" ", "-")
        assert k not in G, k
        for i, f in enumerate(g["figurler"]):
            f["ad"] = f"{g['ad']} {'AB'[i]}"
        G[k] = g
        duvar.append({"tur": tur, "grup": k})
assert len(duvar) == 24 and all(sum(d["tur"] == t for d in duvar) == 8 for t in (1, 2, 3))
json.dump({"_not": "7. video (REF-058) CO-OP ikili pozlar. Figurler soldan saga; temas [sol eklem, sag eklem] ya da 'yan'.",
           "gruplar": G}, open(os.path.join(BURA, "gruplar-07.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvar, open(os.path.join(BURA, "duvar-listesi-07.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"gruplar-07.json: {len(G)} ikili poz; duvar-listesi-07.json: {len(duvar)} duvar")
