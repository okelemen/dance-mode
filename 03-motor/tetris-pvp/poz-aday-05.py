"""TETRIS MODE 5. video - poz ADAY havuzu (~450) -> pozlar-05-aday.json. Maskeler Actions'ta (varlik.py --mod cadi --yalniz poz),
sonra poz-sec-05.py olcumle (eski maskelere + video icine IoU < 0,80) her turdan 45 poz secer.

    python poz-aday-05.py

Neden: ilk 135 pozun 42'si eski 278 maskeye ya da video icinde birbirine IoU >= 0,80 cikti (iou-d1.txt). Basit pozlar onceki
4 videoda kullanildi; yeni pozlar asimetrik kol/bacak + govde egimi + profil kombinasyonlarindan gelir. Guvenlik kurallari ayni
(amuda kalkma, tam kopru, bas durusu, kaldirma yok). Aci dili pozlar.json _not.
"""
import json, os, random

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]
rnd = random.Random(56)

KELIME = ["Pumpkin", "Bat", "Ghost", "Witch", "Zombie", "Skeleton", "Mummy", "Spider", "Vampire", "Goblin", "Cauldron", "Broom",
          "Raven", "Werewolf", "Haunted", "Phantom", "Candle", "Coffin", "Graveyard", "Moonlight", "Potion", "Lantern", "Cobweb",
          "Banshee", "Ghoul", "Spell", "Owl", "Black Cat", "Scarecrow", "Tombstone", "Wizard", "Shadow", "Crypt", "Fog", "Hex"]
aday, adlar = [], set()


def ekle(tur, p):
    k = p["ad"].lower()
    if k in adlar:
        return
    adlar.add(k); p["tur"] = tur; aday.append(p)


# ROUND 1 - ayakta onden: ekran-solu ve ekran-sagi kol AYRI secilir (asimetri), govde egimi
KOL = {"V": "v", "W": "w", "Cactus": "cactus", "Reach": "up", "T": "t", "Head": "head", "Flex": "flex", "Low": "lowv", "Hip": "hip",
       "Chest": "chest", "Diag": "up45", "Down": "down", "Elbow": "elbowdown", "Back": "behind",
       "Cross": [-20, 110], "Salute": [-100, 140], "Swing": [-150, -110], "Point": [-60, -60], "Hook": [-130, -40]}
BAC = {"Stand": ("tog", "tog"), "Wide": ("wide", "wide"), "Goddess": ("goddess", "goddess"), "Horse": ("horse", "horse"),
       "Knee": ("tog", "kneeup"), "Tap": ("tog", "sidetap"), "Curtsy": ("curtsy", "softknee"), "Tree": ("tog", "kneein"),
       "Leg Out": ("straight", "tog"), "Half Goddess": ("goddess", "tog"), "Kick": ("tog", [55, 55]), "Hop": ("tog", [30, -60])}
kk, bb = list(KOL), list(BAC)
while sum(1 for p in aday if p["tur"] == 1) < 170:
    a, b, l = rnd.choice(kk), rnd.choice(kk), rnd.choice(bb)
    gv = rnd.choice([180, 180, 180, 165, 195, 155, 205])
    sag = KOL[a]; sol = KOL[b]
    sol = sol if isinstance(sol, str) else [-sol[0], -sol[1]]       # ozel aci listeleri ekran-solu icin yazildi -> ekran-sagina ayna
    ad = f"{rnd.choice(KELIME)} {a} {b} {l}" + ("" if gv == 180 else f" Lean {'R' if gv < 180 else 'L'}")
    ekle(1, on(ad, sag, sol, BAC[l][0], BAC[l][1], govde=gv))

# ROUND 2 - profil hamle/diz/denge: on kol ve arka kol AYRI + onden derin hamleler
BAC2 = {"Lunge": ([75, 0], [-42, -42], 180), "Kneel Lunge": ([80, 0], [0, -90], 180), "Kneel": ([0, -90], [0, -90], 180),
        "Chair": ([60, -10], [58, -12], 150), "Stork": ([100, -90], [0, 0], 180), "Knee Raise": ([90, 0], [0, 0], 180),
        "Split Stance": ([25, 25], [-30, -30], 175), "Heel Sit": ([90, -90], [88, -90], 175), "Warrior": ([0, 0], [-90, -90], 95),
        "Low Lunge": ([95, -5], [-55, -55], 165), "Kick Back": ([0, 0], [-60, -60], 165), "Quad Hold": ([0, 0], [-10, -150], 180)}
KOL2 = {"Up": [178, 178], "Forward": [90, 90], "Back": [-60, -60], "Diag": [135, 135], "Prayer": [30, 160], "Down": [5, 5],
        "Hip": [-40, 60], "High Back": [-150, -150], "Low Forward": [50, 50], "Bent Up": [90, 170]}
b2, k2 = list(BAC2), list(KOL2)
while sum(1 for p in aday if p["tur"] == 2) < 140:
    l, a, b = rnd.choice(b2), rnd.choice(k2), rnd.choice(k2)
    lg = BAC2[l]
    gv = lg[2] + rnd.choice([0, 0, -10, 10])
    if l == "Warrior" and a in ("Up", "Bent Up"):
        continue
    if l == "Quad Hold":
        b = "Quad"
        p = profil(f"{rnd.choice(KELIME)} {l} {a}", gv, KOL2[a], [-120, -160], lg[0], lg[1])
    else:
        p = profil(f"{rnd.choice(KELIME)} {l} {a} {b}", gv, KOL2[a], KOL2[b], lg[0], lg[1])
    ekle(2, p)
ON2 = {"Side Lunge": ("lunge", "tog", 172), "Deep Goddess": ([-70, 20], [70, -20], 180), "Wide Lunge": ("lunge", "lunge", 180),
       "Skater": ([-30, 40], [20, -70], 170)}
while sum(1 for p in aday if p["tur"] == 2) < 175:
    l, a, b = rnd.choice(list(ON2)), rnd.choice(kk), rnd.choice(kk)
    sol = KOL[b] if isinstance(KOL[b], str) else [-KOL[b][0], -KOL[b][1]]
    ekle(2, on(f"{rnd.choice(KELIME)} {l} {a} {b}", KOL[a], sol, ON2[l][0], ON2[l][1], govde=ON2[l][2]))

# ROUND 3 - yer pozlari + zor denge: tabanlar x kol varyantlari
DIZ2 = [0, "geri"]
TABAN = {  # ad: (tip, govde, bacak1, bacak2)  tip: p = profil, o = onden
    "Seated Staff": ("p", 175, [90, 90], [88, 88]), "Boat": ("p", 210, [125, 55], [123, 53]), "Tabletop": ("p", 90, [0, -90], [0, -90]),
    "Bird Dog": ("p", 92, [-90, -90], [0, -90]), "High Plank": ("p", 98, [-82, -82], [-84, -84]), "Knee Plank": ("p", 110, [-40, -130], [-42, -132]),
    "Bridge": ("p", -60, [60, 0], [58, -2]), "Crab": ("p", -80, [90, 0], [88, 0]), "Lying": ("p", -90, [90, 90], [88, 88]),
    "Child": ("p", 70, [100, -95], [98, -95]), "Cobra": ("p", 130, [-90, -90], [-88, -88]), "Seated Knees Up": ("p", 165, [135, -5], [133, -7]),
    "Warrior Three": ("p", 95, [0, 0], [-90, -90]), "Standing Split": ("p", 30, [2, 2], [-120, -120]),
    "Kneel": ("o", 180, DIZ2, DIZ2), "Straddle": ("o", 180, [-80, -80], [80, 80]), "Cross Legged": ("o", 180, [-78, 75], [78, -75]),
    "Low Squat": ("o", 180, [-70, 25], [70, -25]), "Half Kneel Side": ("o", 175, [0, "geri"], [60, -10]), "Side Sit": ("o", 170, [-80, 60], [70, -100])}
PK = {"Up": [178, 178], "Forward": [90, 90], "Back Floor": [-25, -25], "Floor": [0, 0], "Diag": [135, 135], "Wide": [90, -90], "Hug": [110, -10]}
OK = ["v", "w", "cactus", "up", "t", "head", "flex", "hip", "chest", "up45", "lowv"]
TAB = list(TABAN)
while sum(1 for p in aday if p["tur"] == 3) < 150:
    t = rnd.choice(TAB); tip, gv, b1, b2_ = TABAN[t]
    if tip == "p":
        a, b = rnd.choice(list(PK)), rnd.choice(list(PK))
        if t in ("Tabletop", "Bird Dog", "High Plank", "Knee Plank", "Crab") and b != "Floor":
            b = "Floor"                                     # yerde dayanak kol sart (guvenlik)
        if t == "Child" and a in ("Hug",):
            continue
        ekle(3, profil(f"{rnd.choice(KELIME)} {t} {a} {b}", gv, PK[a], PK[b], b1, b2_))
    else:
        a, b = rnd.choice(OK), rnd.choice(OK)
        ekle(3, on(f"{rnd.choice(KELIME)} {t} {a.title()} {b.title()}", a, b, b1, b2_, govde=gv + rnd.choice([0, 0, 12, -12])))

# eski adlarla cakisma yok
eski = set()
for f in ("pozlar.json", "pozlar-03.json", "pozlar-04.json"):
    eski |= {p["ad"].lower() for p in json.load(open(os.path.join(BURA, f), encoding="utf-8"))["pozlar"].values()}
aday = [p for p in aday if p["ad"].lower() not in eski]
anah = lambda p: p["ad"].lower().replace(" ", "-").replace("'", "")
pozlar = {anah(p): p for p in aday}
assert len(pozlar) == len(aday)
not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "5. video ADAY havuzu (REF-056)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-05-aday.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({t: sum(1 for p in aday if p["tur"] == t) for t in (1, 2, 3)}, "->", len(aday), "aday")
