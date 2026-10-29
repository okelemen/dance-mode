"""HUMAN TETRIS 11. video (REF-062 HumanWarmUp, CO-OP 2 oyuncu) - 25 ikili poz -> gruplar-11.json + duvar-listesi-11.json.

    python ikili-listesi-kur-11.py

REF-062 dili (HumanWarmUp "HUMAN TETRIS | ... | CO-OP 2 Players | THE NEXT PART"): TEK duvar, iki kisilik ortak delik;
pozlarin cogu AYNALI ve karsilikli (el ele), bir kismi yan yana temassiz (T kollu agac, dua comelmesi), bir kismi ASIMETRIK
(okcu + yan comelme, oturan + uzanan, kopru + ayakta). Kullanici 29 Eki 2026 listeyi onayladi ("Onayliyorum").
Uygulamada degisen (gerekce): 3 Standing Crescent Arch -> Extended Side Angle Feet Meet (7. videonun High Ten'iyle ayni siluet),
5 Eagle Arms -> Horse Stance Fist Bump (kartal kollari govdenin onunde, silüette okunmaz),
20 Cat-Cow Facing -> Kneeling Lunge Hand Link (masa duzeni 7. videonun Bird Dog'uyla ayni siluet).
Guvenlik (TALIMATLAR §4): kaldirma / tasima / agirlik verme yok, bas asagi yok (REF d06 omuz durusu ve d11 destekli split alinmadi);
her figur kendi ayagi/dizi/eli ile yerde. Aci dili poz-listesi-kur.py (on/profil). Temas [sol eklem, sag eklem], "yan" ya da
sayi = temassiz bosluk (m, varlik-cadi.py hizala). Sag figur verilmezse solun aynasi.
Maskeler Actions'ta: tetris-varlik.yml yalniz=grup, ek="--mod cadi --gruplar 03-motor/tetris-pvp/gruplar-11.json".
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


KNEEL = [0, -90]                 # profilde diz cokme (uyluk dik, baldir geride yerde)
TOPUK = [80, -95]                # profilde topuklar ustune oturma (uyluk one yatik, baldir geride yerde)
AYAKTA = [  # ayakta - herkes yapar
    ikili("T-Arm Tree", on("", "t", "t", "tog", "kneein"), on("", "t", "t", "tog", "kneein"), temas=0.35),       # REF d02
    ikili("Arabesque Low Hand Link", profil("", 155, [65, 65], [-120, -120], [0, 0], [-105, -105])),               # REF d01
    ikili("Extended Side Angle Feet Meet", on("", "down", [220, 225], "lunge", "straight", govde=215), temas=("ayak", "ayak")),
    ikili("Goddess Squat Prayer", on("", "chest", "chest", "goddess", "goddess"),
          on("", "chest", "chest", "goddess", "goddess"), temas=0.3),                                                   # REF d12
    ikili("Horse Stance Fist Bump", on("", "chest", [90, 90], "horse", "horse")),
    ikili("Wide Stance Palm Push", profil("", 145, [120, 120], [118, 118], [62, 0], [-45, -45])),
    ikili("Reverse Warrior Mirror", profil("", 200, [-160, -160], [-20, -20], [62, 0], [-40, -40]), temas=0.15),
    ikili("Fist Bump Front Lunge", profil("", 175, [90, 90], [-60, 60], [55, 0], [-35, -35])),
]

TEK_AYAK = [  # tek ayak denge / tekme / hamle
    ikili("High Side Kick Foot Meet", on("", "v", "v", "tog", [100, 100]), temas=("ayak", "ayak")),                  # REF d08
    ikili("Standing Quad Stretch Shoulder Link", profil("", 180, [70, 70], [-30, -30], [0, 0], [-10, -170]), temas=("el", "omuz")),
    ikili("Warrior Three Parallel", profil("", 92, [90, 90], [88, 88], [0, 0], [-90, -90]),
          profil("", 92, [90, 90], [88, 88], [0, 0], [-90, -90]), temas=0.3),                                            # REF d14
    ikili("Half Moon Facing Out", on("", [-5, -5], [180, 180], "tog", [90, 90], govde=270), temas=("ayak", "ayak")),
    ikili("Front Kick Mirror", profil("", 175, [40, 160], [38, 158], [90, 90], [0, 0]), temas=("ayak", "ayak")),
    ikili("Back Kick Hand Link", profil("", 115, [110, 110], [108, 108], [0, 0], [-125, -125])),
    ikili("Lateral Leg Raise Inner Hands", on("", "t", [45, 45], [-60, -60], "tog")),
    ikili("Archer Side Squat",                                                                                        # REF d10, asimetrik
          profil("", 175, [90, 90], [90, -90], [62, 0], [-40, -40]),
          on("", "chest", "chest", [-75, -80], [80, 5]), temas=0.15),
    ikili("Seated Helper Standing Reach",                                                                             # REF d07, asimetrik
          profil("", 200, [140, 140], [-30, -30], [90, 90], [70, -20]),
          ayna_poz(profil("", 130, [60, 60], [-60, -60], [0, 0], [-60, -60]))),
]

YER = [  # diz / yer (el-diz-ayak yerde)
    ikili("Camel Standing Reach",                                                                                     # REF d03 (kopru yerine deve)
          profil("", 220, [-20, -20], [-18, -18], KNEEL, KNEEL),
          ayna_poz(profil("", 190, [175, 175], [170, 170], [5, 5], [-5, -5])), temas=0.2),
    ikili("Kneeling Side Reach Palms Together", profil("", 180, [100, 100], [-150, -150], KNEEL, KNEEL)),             # REF d09
    ikili("Kneeling Lunge Hand Link", profil("", 175, [95, 95], [93, 93], [75, 0], [0, -90])),
    ikili("Downward Dog Facing", profil("", 40, [25, 25], [23, 23], [-25, -25], [-27, -27]), temas=0.1),
    ikili("Seated Wide Leg Hand Pull", profil("", 130, [95, 95], [93, 93], [90, 90], [88, 88]), temas=("ayak", "ayak")),
    ikili("Child Pose Hands Meet", profil("", 75, [85, 85], [83, 83], TOPUK, TOPUK)),
    ikili("Sphinx Facing", profil("", 125, [0, 90], [0, 88], [-90, -90], [-88, -88]), temas=0.1),
    ikili("Hero Sit Palms Up Touch", profil("", 180, [160, 160], [158, 158], TOPUK, TOPUK)),
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
json.dump({"_not": "11. video (REF-062) CO-OP ikili pozlar. Figurler soldan saga; temas [sol eklem, sag eklem], 'yan' ya da bosluk (m).",
           "gruplar": G}, open(os.path.join(BURA, "gruplar-11.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(duvar, open(os.path.join(BURA, "duvar-listesi-11.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"gruplar-11.json: {len(G)} ikili poz; duvar-listesi-11.json: {len(duvar)} duvar")
