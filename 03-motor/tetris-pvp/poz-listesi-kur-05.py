"""TETRIS MODE 5. video (REF-056, 3 OYUNCU, HALLOWEEN) - 45 grup pozu (3 tur x 15) -> gruplar-05.json.

    python poz-listesi-kur-05.py

REF-056 dili (Glow Motion "HUMAN TETRIS x3 player"): her duvarda UC kisilik TEK siluet, uc oyuncu birbirine DEGER
(el ele, omuz omuza, dayanma, kollarla sekil, yerde yan yana). ROUND 1 BEGINNER -> ROUND 2 CHALLENGER -> ROUND 3 (final).
Kullanici 19 Eki 2026: "Hareketleri sen cikartacaksin" + Halloween temasi (yalniz bu video) -> grup sekilleri Halloween
nesnelerinden: yarasa, balkabagi, cadi sapkasi, mezar tasi, mumya, zombi, iskelet, orumcek, kara kedi, hayalet ...
Guvenlik (POZ-DUVARI/TALIMATLAR.md §2): KALDIRMA / TASIMA / UST USTE YOK (referanstaki kaldirma pozlari alinmadi),
amuda kalkma, kopru, bas durusu yok; her figur kendi ayagi/dizi/eli ile yerde.
Aci dili pozlar.json _not ile ayni (on/profil yardimcilari poz-listesi-kur.py'den).
Temas: varlik-cadi.py sag figuru x'te kaydirir; ["el","el"] = soldakinin en sagdaki eli ile sagdakinin en soldaki eli
bulusur; "yan" = silüetler yan yana deger. Dikey fark (dz) Actions logunda/yerlesim.json'da olculur.
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
_kaynak = open(os.path.join(BURA, "poz-listesi-kur.py"), encoding="utf-8").read().split("TUR1 = [")[0]
_g = {}
exec(compile(_kaynak, "poz-listesi-kur.py", "exec"), _g)
on, profil, K, B = _g["on"], _g["profil"], _g["K"], _g["B"]


def ayna_poz(P):
    Q = {"ad": P["ad"], "yon": {"on": "on", "sag": "sol", "sol": "sag"}[P.get("yon", "on")]}
    neg = lambda v: [x if x == "geri" else -x for x in v]
    Q["govde"] = -P.get("govde", 180); Q["bas"] = -P.get("bas", 0)
    for a, b in (("sagKol", "solKol"), ("sagBacak", "solBacak")):
        if a in P: Q[b] = neg(P[a])
        if b in P: Q[a] = neg(P[b])
    return Q


def grup(ad, sol, orta, sag=None, temas=("el", "el"), temas2=None, zincir=False):
    """sol = ekranin solundaki oyuncu, orta, sag (verilmezse solun aynasi; zincir=True ise solun kopyasi, ayni yone bakar)"""
    if sag is None:
        sag = dict(sol) if zincir else ayna_poz(sol)
    if temas2 is None:
        temas2 = temas if (zincir or temas == "yan") else list(reversed(temas))
    return {"ad": ad, "figurler": [sol, orta, sag], "temas": [temas if temas == "yan" else list(temas),
                                                            temas2 if temas2 == "yan" else list(temas2)]}


DUA_UST = ([-165, 170], [165, -170])          # eller basin ustunde birlesik (sapka ucu)
KNEEL = [0, -90]                               # profilde diz cokme
OTUR_L, OTUR_R = [-78, 75], [78, -75]          # onden bagdas

TUR1 = [  # ROUND 1 - BEGINNER: ayakta, onden, yumusak (herkes yapar)
    grup("Bat Trio", on("", "w", "up45", "wide", "wide"), on("", "w", "w", "goddess", "goddess")),
    grup("Pumpkin Ring", on("", "hip", "up45", "softknee", "softknee", govde=172), on("", "v", "v", "tog", "tog")),
    grup("Witch Hat", on("", "down", [110, 110], "tog", "tog", govde=160), on("", DUA_UST[0], DUA_UST[1], "tog", "tog"),
         temas=("el", "omuz")),
    grup("Haunted Gate", on("", "lowv", "t", "horse", "horse"), on("", "t", "t", "horse", "horse")),
    grup("Zombie Line", profil("", 175, [90, 90], [88, 88], [25, 10], [-20, -25]), profil("", 175, [90, 90], [88, 88], [-20, -25], [25, 10]),
         temas=("el", "omuz"), zincir=True),
    grup("Mummy Wrap", on("", "chest", "chest", "tog", "tog"), on("", "chest", "chest", "softknee", "softknee"), temas="yan"),
    grup("Skeleton Shake", on("", "up", "t", "kneeup", "tog"), on("", "t", "t", "tog", "kneeup")),
    grup("Ghost Float", on("", "lowv", "lowv", "tog", "curtsy"), on("", "lowv", "lowv", "tog", "tog")),
    grup("Cauldron Circle", on("", "lowv", [55, 20], "wide", "wide", govde=165), on("", [-55, -20], [55, 20], "goddess", "goddess")),
    grup("Haunted Tree", on("", "up", "t", "tog", "kneein"), on("", "up45", "v", "kneein", "tog")),
    grup("Scarecrow Row", on("", [-90, -20], [90, 20], "softknee", "tog", bas=15), on("", [-90, -20], [90, 20], "tog", "tog", bas=-15)),
    grup("Candle Trio", on("", DUA_UST[0], DUA_UST[1], "tog", "tog"), on("", DUA_UST[0], DUA_UST[1], "tog", "tog"), temas="yan"),
    grup("Vampire Cape", on("", "chest", [100, 60], "lunge", "tog", govde=172), on("", "v", "v", "wide", "wide"), temas=("el", "omuz")),
    grup("Monster Flex", on("", "flex", "flex", "wide", "wide"), on("", "flex", "flex", "horse", "horse"), temas="yan"),
    grup("Spooky Wave", on("", "cactus", "t", "tog", "sidetap"), on("", "up", "lowv", "tog", "tog")),
]

TUR2 = [  # ROUND 2 - CHALLENGER: hamle, diz cokme, denge, yer pozlari
    grup("Black Cat Stretch", profil("", 92, [0, 0], [0, 0], KNEEL, KNEEL), profil("", 80, [0, 0], [0, 0], KNEEL, KNEEL), temas="yan", zincir=True),
    grup("Werewolf Howl", profil("", 180, [120, 120], [118, 118], KNEEL, KNEEL), profil("", 195, [178, 178], [176, 176], [75, 0], [-42, -42], bas=25),
         sag=profil("", 180, [120, 120], [118, 118], KNEEL, KNEEL), temas="yan", temas2="yan"),
    grup("Gravestone Row", profil("", 180, [178, 178], [176, 176], KNEEL, KNEEL), on("", "up", "up", [0, "geri"], [0, "geri"]), temas="yan"),
    grup("Pumpkin Patch", profil("", 160, [110, -10], [108, -12], [135, -5], [133, -7]), on("", "chest", "chest", OTUR_L, OTUR_R), temas="yan"),
    grup("Broom Ride", profil("", 160, [60, 60], [58, 58], [70, 0], [-35, -35]), profil("", 160, [60, 60], [58, 58], [70, 0], [-35, -35]),
         temas=("el", "kalca"), zincir=True),
    grup("Witch Hat Lunge", on("", "lowv", [70, 70], "lunge", "tog", govde=170), on("", DUA_UST[0], DUA_UST[1], "goddess", "goddess"), temas=("el", "kalca")),
    grup("Ghost Glide", on("", "lowv", "t", "straight", "tog", govde=172), on("", "t", "t", "tog", "tog")),
    grup("Spider Crouch", on("", [-30, -10], [30, 10], "goddess", "goddess", govde=40), on("", "w", "w", "goddess", "goddess"), temas="yan"),
    grup("Bat Hang", profil("", 40, [-150, -150], [-148, -148], [0, 0], [-2, -2]), on("", "v", "v", "wide", "wide"),
         sag=None, temas="yan"),
    grup("Frankenstein Steps", on("", "t", "t", "kneeup", "tog"), on("", "t", "t", "tog", "kneeup")),
    grup("Haunted House", on("", "down", "up45", "tog", "tog", govde=168), on("", DUA_UST[0], DUA_UST[1], "wide", "wide")),
    grup("Candy Corn", profil("", 180, [140, 140], [138, 138], [80, 0], [0, -90]), on("", "up", "up", "tog", "tog"), temas=("el", "kalca")),
    grup("Mummy Bend", profil("", 25, [5, 5], [3, 3], [2, 2], [-2, -2]), profil("", 25, [5, 5], [3, 3], [2, 2], [-2, -2]), temas="yan", zincir=True),
    grup("Cauldron Squat", on("", "head", "head", "goddess", "goddess"), on("", "head", "head", "horse", "horse"), temas="yan"),
    grup("Skeleton Lunge", on("", "up", "t", "lunge", "tog", govde=172), on("", "t", "t", "lunge", "lunge")),
]

TUR3 = [  # ROUND 3 - FINAL: zor denge ve yer pozlari (guvenli surumler)
    grup("Raven Wings", profil("", 95, [-60, -60], [-58, -58], [0, 0], [-90, -90]), on("", "v", "v", "tog", "tog"), temas="yan"),
    grup("Dance of the Dead", profil("", 170, [150, 150], [-130, -160], [0, 0], [-40, -150]), on("", "up", "up", "tog", "kneein"), temas="yan"),
    grup("Coffin Bridge", profil("", -60, [180, 180], [178, 178], [60, 0], [58, -2]), on("", "v", "v", "goddess", "goddess"), temas="yan"),
    grup("Tombstone Plank", on("", "up", [-25, -25], "straight", "straight", govde=118), on("", "v", "v", [0, "geri"], [0, "geri"])),
    grup("Boat of Souls", profil("", 210, [90, 90], [88, 88], [125, 55], [123, 53]), on("", "up", "up", [-80, -80], [80, 80]), temas=("ayak", "ayak")),
    grup("Black Cat Balance", profil("", 95, [90, 90], [0, 0], [-90, -90], KNEEL), profil("", 95, [90, 90], [0, 0], [-90, -90], KNEEL),
         temas="yan", zincir=True),
    grup("Reaper Reach", profil("", 170, [135, 135], [133, 133], [80, 0], [-45, -45]), profil("", 170, [135, 135], [133, 133], [80, 0], [-45, -45]),
         temas=("el", "omuz"), zincir=True),
    grup("Ghost Tree", on("", "up", "up45", "tog", "kneein"), on("", "up45", "up45", "kneein", "tog")),
    grup("Coffin Candle", profil("", -90, [-10, -10], [-8, -8], [180, 180], [178, 178]), on("", "up", "up", "tog", "tog"), temas="yan"),
    grup("Hat Peak Fold", profil("", 20, [5, 5], [3, 3], [2, 2], [-150, -150]), on("", DUA_UST[0], DUA_UST[1], "tog", "tog"), temas="yan"),
    grup("Bat Swarm", on("", "w", "w", "goddess", "goddess", govde=165), on("", "v", "v", "wide", "wide"), temas="yan"),
    grup("Pumpkin Roll", profil("", 70, [100, 100], [98, 98], [100, -95], [98, -95]), on("", "chest", "chest", [0, "geri"], [0, "geri"]), temas="yan"),
    grup("Zombie Rise", profil("", 175, [150, 150], [-30, -30], KNEEL, [80, 0]), profil("", 175, [150, 150], [-30, -30], KNEEL, [80, 0]),
         temas=("el", "omuz"), zincir=True),
    grup("Spider Bridge", profil("", -80, [0, 0], [0, 0], [90, 0], [88, 0]), on("", "up", "up", "goddess", "goddess"), temas="yan"),
    grup("Final Fright", on("", "lowv", "up45", "lunge", "tog", govde=170), on("", "v", "v", "wide", "wide")),
]

gruplar, duvarlar = {}, []
for tur, liste in ((1, TUR1), (2, TUR2), (3, TUR3)):
    for G in liste:
        k = G["ad"].lower().replace(" ", "-").replace("'", "")
        assert k not in gruplar, k
        for i, f in enumerate(G["figurler"]):
            f["ad"] = f"{G['ad']} {'ABC'[i]}"
        gruplar[k] = G
        duvarlar.append({"tur": tur, "grup": k})
assert len(duvarlar) == 45, len(duvarlar)
json.dump({"_not": "TETRIS MODE 5. video (REF-056, 3 oyuncu, Halloween) grup pozlari. Figurler soldan saga A B C; aci dili pozlar.json _not. "
                   "temas: [sol eklem, sag eklem] ya da 'yan'.", "gruplar": gruplar},
          open(os.path.join(BURA, "gruplar-05.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvarlar, open(os.path.join(BURA, "duvar-listesi-05.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(gruplar)} grup ({3 * len(gruplar)} figur), {len(duvarlar)} duvar -> gruplar-05.json")
