"""TETRIS MODE 5. video (REF-056, 3 OYUNCU, HALLOWEEN) - 135 tek kisilik poz (45 duvar x 3 oyuncu) -> pozlar-05.json + duvar-listesi-05.json.

    python poz-listesi-kur-05.py

Kullanici 19 Eki 2026: "Her karede tek bir siluet ... 3 tane yan yana" -> ekran uce bolunur (P1 | P2 | P3), her panelde TEK
siluet; 3 kisilik grup pozu yok (ilk deneme grup-listesi-kur-05.py iptal). "Hareketleri sen cikartacaksin" -> pozlar burada;
Halloween adlari (yalniz bu video). ROUND 1 BEGINNER: ayakta, onden · ROUND 2 CHALLENGER: hamle, diz cokme, denge ·
ROUND 3 FINAL: yer pozlari + zor denge. Guvenlik (TALIMATLAR §2): amuda kalkma, tam kopru, bas/omuz durusu, kaldirma yok.
Aci dili pozlar.json _not (on/profil poz-listesi-kur.py'den). Ad tekrari assert; sekil tekrari maskeler inince olc-poz-iou.py.
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil = _g["on"], _g["profil"]

KELIME = ["Pumpkin", "Bat", "Ghost", "Witch", "Zombie", "Skeleton", "Mummy", "Spider", "Vampire", "Goblin", "Cauldron", "Broom",
          "Raven", "Werewolf", "Haunted", "Phantom", "Candle", "Coffin", "Graveyard", "Moonlight", "Potion", "Lantern", "Cobweb",
          "Banshee", "Ghoul", "Spell", "Owl", "Black Cat", "Scarecrow", "Tombstone"]

# ---------------------------------------------------------------- ROUND 1: ayakta, onden
KOL1 = [("v", "v", "V"), ("w", "w", "W"), ("cactus", "cactus", "Cactus"), ("up", "up", "Reach"), ("t", "t", "T"), ("head", "head", "Hands Head"),
        ("flex", "flex", "Flex"), ("lowv", "lowv", "Low V"), ("hip", "hip", "Hips"), ("up", "hip", "One Up"), ("up45", "lowv", "Diagonal"),
        ("cactus", "t", "Half Cactus"), ("chest", "up", "Chest Reach"), ("elbowdown", "elbowdown", "Elbows Down"), ("w", "up", "W Reach"),
        ("v", "t", "V T"), ("head", "t", "Head T"), ("up45", "up45", "Wide Reach"), ("flex", "up", "Flex Reach")]
BAC1 = [("tog", "tog", "Stand"), ("wide", "wide", "Wide"), ("goddess", "goddess", "Goddess"), ("horse", "horse", "Horse"),
        ("tog", "kneeup", "Knee Up"), ("tog", "sidetap", "Side Tap"), ("curtsy", "softknee", "Curtsy"), ("tog", "kneein", "Tree"),
        ("softknee", "softknee", "Soft Knee"), ("straight", "tog", "Leg Out")]
TUR1, kul, i = [], set(), 0
while len(TUR1) < 45:
    a = KOL1[(i * 7) % len(KOL1)]; b = BAC1[(i * 3 + i // len(BAC1)) % len(BAC1)]
    i += 1
    if (a[2], b[2]) in kul:
        continue
    kul.add((a[2], b[2]))
    gv = (168 if len(TUR1) % 6 == 2 else 192 if len(TUR1) % 6 == 5 else 180) if b[0] == "tog" else 180
    TUR1.append(on(f"{KELIME[len(TUR1) % len(KELIME)]} {a[2]} {b[2]}", a[0], a[1], b[0], b[1], govde=gv))

# ---------------------------------------------------------------- ROUND 2: hamle, diz cokme, denge (profil) + onden hamle
BAC2 = [("Lunge", [75, 0], [-42, -42], 180), ("Kneel Lunge", [80, 0], [0, -90], 180), ("Kneel", [0, -90], [0, -90], 180),
        ("Chair", [60, -10], [58, -12], 150), ("Stork", [100, -90], [0, 0], 180), ("Knee Raise", [90, 0], [0, 0], 180),
        ("Split Stance", [25, 25], [-30, -30], 175), ("Heel Sit", [90, -90], [88, -90], 175), ("Warrior", [0, 0], [-90, -90], 95)]
KOL2 = [("Arms Up", [178, 178], [176, 176]), ("Arms Forward", [90, 90], [88, 88]), ("Arms Back", [-60, -60], [-58, -58]),
        ("Diagonal Reach", [135, 135], [133, 133]), ("Prayer", [30, 160], [28, 158]), ("Archer", [150, 150], [-60, -60]),
        ("Hands Hips", [-40, 60], [-38, 62]), ("Airplane", [90, 90], [-90, -90]), ("Arms Down", [5, 5], [3, 3])]
UYAR = {"Warrior": {"Arms Forward", "Arms Back", "Airplane", "Arms Down"}, "Chair": {"Arms Up", "Arms Forward", "Prayer", "Diagonal Reach"}}
ON2 = [("Side Lunge", "lunge", "tog", 172), ("Deep Goddess", [-70, 20], [70, -20], 180), ("Wide Lunge", "lunge", "lunge", 180)]
KOLON2 = [("V", "v", "v"), ("T", "t", "t"), ("Cactus", "cactus", "cactus"), ("Reach", "up", "up"), ("W", "w", "w")]
TUR2, govdeler = [], set()
for j in range(400):
    if len(TUR2) >= 45:
        break
    if j % 4 == 3:
        bb = ON2[(j // 4) % len(ON2)]; kk = KOLON2[(j // 4 + j // 12) % len(KOLON2)]
        govde = f"{bb[0]} {kk[0]}"
        if govde in govdeler:
            continue
        govdeler.add(govde)
        TUR2.append(on(f"{KELIME[(len(TUR2) + 7) % len(KELIME)]} {govde}", kk[1], kk[2], bb[1], bb[2], govde=bb[3]))
        continue
    bb = BAC2[j % len(BAC2)]; kk = KOL2[(j * 5 + j // len(BAC2)) % len(KOL2)]
    if bb[0] in UYAR and kk[0] not in UYAR[bb[0]]:
        continue
    govde = f"{bb[0]} {kk[0]}"
    if govde in govdeler:
        continue
    govdeler.add(govde)
    TUR2.append(profil(f"{KELIME[(len(TUR2) + 7) % len(KELIME)]} {govde}", bb[3], kk[1], kk[2], bb[1], bb[2]))

# ---------------------------------------------------------------- ROUND 3: yer pozlari + zor denge (guvenli surumler)
DIZ2 = [0, "geri"]
B3 = [
    ("Seated Staff Arms Up", lambda a: profil(a, 175, [178, 178], [176, 176], [90, 90], [88, 88])),
    ("Seated Staff Hands Back", lambda a: profil(a, 160, [-25, -25], [-23, -23], [90, 90], [88, 88])),
    ("Boat Arms Forward", lambda a: profil(a, 210, [90, 90], [88, 88], [125, 55], [123, 53])),
    ("Boat Arms Up", lambda a: profil(a, 210, [175, 175], [173, 173], [125, 55], [123, 53])),
    ("Tabletop", lambda a: profil(a, 90, [0, 0], [0, 0], [0, -90], [0, -90])),
    ("Bird Dog", lambda a: profil(a, 92, [90, 90], [0, 0], [-90, -90], [0, -90])),
    ("Tabletop Leg Back", lambda a: profil(a, 90, [0, 0], [0, 0], [-90, -90], [0, -90])),
    ("High Plank", lambda a: profil(a, 98, [0, 0], [0, 0], [-82, -82], [-84, -84])),
    ("Forearm Plank", lambda a: profil(a, 95, [0, 90], [0, 90], [-85, -85], [-87, -87])),
    ("Plank Leg Lift", lambda a: profil(a, 98, [0, 0], [0, 0], [-120, -120], [-84, -84])),
    ("Knee Plank", lambda a: profil(a, 110, [0, 0], [0, 0], [-40, -130], [-42, -132])),
    ("Glute Bridge", lambda a: profil(a, -60, [-10, -10], [-8, -8], [60, 0], [58, -2])),
    ("Bridge Arms Up", lambda a: profil(a, -60, [180, 180], [178, 178], [60, 0], [58, -2])),
    ("Bridge Leg Up", lambda a: profil(a, -60, [-10, -10], [-8, -8], [150, 150], [58, -2])),
    ("Crab", lambda a: profil(a, -80, [0, 0], [0, 0], [90, 0], [88, 0])),
    ("Crab Kick", lambda a: profil(a, -80, [0, 0], [0, 0], [150, 150], [88, 0])),
    ("Lying Arms Up", lambda a: profil(a, -90, [180, 180], [178, 178], [90, 90], [88, 88])),
    ("Lying Knees Tuck", lambda a: profil(a, -90, [150, 90], [148, 88], [150, 70], [148, 68])),
    ("Dead Bug Reach", lambda a: profil(a, -90, [180, 180], [90, 90], [180, 90], [90, 90])),
    ("Child Arms Forward", lambda a: profil(a, 70, [100, 100], [98, 98], [100, -95], [98, -95])),
    ("Child Arms Back", lambda a: profil(a, 70, [-20, -20], [-18, -18], [100, -95], [98, -95])),
    ("Cobra", lambda a: profil(a, 130, [0, 0], [0, 0], [-90, -90], [-88, -88])),
    ("Superman Lite", lambda a: profil(a, 100, [100, 100], [98, 98], [-95, -95], [-93, -93])),
    ("Side Kneel Reach", lambda a: on(a, "up", [40, 40], [0, "geri"], [60, -10], govde=160)),
    ("Kneel V", lambda a: on(a, "v", "v", DIZ2, DIZ2)),
    ("Kneel W", lambda a: on(a, "w", "w", DIZ2, DIZ2)),
    ("Kneel Cactus", lambda a: on(a, "cactus", "cactus", DIZ2, DIZ2)),
    ("Kneel Hands Head", lambda a: on(a, "head", "head", DIZ2, DIZ2)),
    ("Kneel One Up", lambda a: on(a, "up", "hip", DIZ2, DIZ2, govde=190)),
    ("Seated Straddle Reach", lambda a: on(a, "up", "up", [-80, -80], [80, 80])),
    ("Seated Straddle T", lambda a: on(a, "t", "t", [-80, -80], [80, 80])),
    ("Seated Straddle Lean", lambda a: on(a, "down", [140, 140], [-80, -80], [80, 80], govde=200)),
    ("Cross Legged Cactus", lambda a: on(a, "cactus", "cactus", [-78, 75], [78, -75])),
    ("Cross Legged V", lambda a: on(a, "v", "v", [-78, 75], [78, -75])),
    ("Low Squat Prayer", lambda a: on(a, "chest", "chest", [-70, 25], [70, -25])),
    ("Low Squat Reach", lambda a: on(a, "up", "up", [-70, 25], [70, -25])),
    ("Frog Hands Floor", lambda a: on(a, [-12, -5], [12, 5], [-70, 25], [70, -25], govde=150)),
    ("Standing Split Lite", lambda a: profil(a, 30, [5, 5], [3, 3], [2, 2], [-120, -120])),
    ("Warrior Three Arms Up", lambda a: profil(a, 95, [95, 95], [93, 93], [0, 0], [-90, -90])),
    ("Dancer Lite", lambda a: profil(a, 160, [150, 150], [-130, -160], [0, 0], [-40, -150])),
    ("Half Moon Lite", lambda a: on(a, [-5, -5], [170, 170], "tog", [80, 80], govde=105)),
    ("Side Lunge Fold", lambda a: profil(a, 35, [5, 5], [3, 3], [40, -40], [-40, -40])),
    ("Pistol Prep", lambda a: profil(a, 165, [90, 90], [88, 88], [90, 90], [80, -60])),
    ("Reverse Tabletop", lambda a: profil(a, -85, [0, 0], [0, 0], [90, 0], [88, 0])),
    ("Seated Twist Reach", lambda a: on(a, [-80, -80], [170, 170], [-85, -85], [85, 85], govde=200)),
]
TUR3 = [f(f"{KELIME[(n + 13) % len(KELIME)]} {ad}") for n, (ad, f) in enumerate(B3)]
assert len(TUR1) == 45 and len(TUR2) == 45 and len(TUR3) == 45, (len(TUR1), len(TUR2), len(TUR3))

# ---------------------------------------------------------------- duvarlar: her duvar 3 farkli poz (P1 | P2 | P3)
anah = lambda p: p["ad"].lower().replace(" ", "-").replace("'", "")
pozlar, duvarlar, adlar = {}, [], set()
for tur, liste in ((1, TUR1), (2, TUR2), (3, TUR3)):
    for w in range(15):            # liste aile aile ilerliyor: ayni duvara w, w+15, w+30 (benzer pozlar yan yana gelmez)
        uc = [liste[w], liste[w + 15], liste[w + 30]]
        for p in uc:
            assert p["ad"] not in adlar, p["ad"]
            adlar.add(p["ad"]); pozlar[anah(p)] = p
        duvarlar.append({"tur": tur, "p1": anah(uc[0]), "p2": anah(uc[1]), "p3": anah(uc[2])})
assert len(duvarlar) == 45 and len(pozlar) == 135, (len(duvarlar), len(pozlar))

eski = set()
for f in ("pozlar.json", "pozlar-03.json", "pozlar-04.json"):
    eski |= {p["ad"].lower() for p in json.load(open(os.path.join(BURA, f), encoding="utf-8"))["pozlar"].values()}
_kul = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("KULLANILMIS = ")[1].split("}")[0] + "}"
eski |= eval(_kul)
cakisan = sorted(a for a in adlar if a.lower() in eski)
assert not cakisan, cakisan

not_ = json.load(open(os.path.join(BURA, "pozlar.json"), encoding="utf-8"))["_not"].replace("(REF-053)", "5. video (REF-056, 3 oyuncu, Halloween)")
json.dump({"_not": not_, "pozlar": pozlar}, open(os.path.join(BURA, "pozlar-05.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvarlar, open(os.path.join(BURA, "duvar-listesi-05.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(pozlar)} poz, {len(duvarlar)} duvar -> pozlar-05.json")
