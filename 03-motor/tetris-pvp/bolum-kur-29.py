"""HUMAN TETRIS 29 bolum JSON'u (referanssiz, 1v1, cilali 3D orman tapinagi) - bolum-kur-26.py'den; ozel tur SPEED
(24 SPEED, 25 FREEZE, 26 MIRROR, 27 BLIND, 28 FREEZE -> 29 SPEED); giris TAS KAPI (kullanici 15 Kas 2026, yalniz 29; motor 26).

    python bolum-kur-29.py   ->  bolumler/tetris-mode-29.json

SURE 3:15-3:20 (TALIMATLAR §3) -> 106 olcu = 3:15,7 (130 BPM, vurus 0,4615 sn, olcu 1,846 sn):
  acilis (tas kapi + VS tablet + WHO WILL WIN?) 2 olcu (ilk duvar 3,69 sn; mobil paket md. 1)
  normal duvar 15 vurus = 6,92 sn: kart 2 / say 8 / buyu 3 / gec 2
  SPEED ROUND: ilk 2 duvar normal, son 4 duvar 12 vurus = 5,54 sn (kart 2 / say 6 / buyu 2 / gec 2), d.hiz -> FASTER!
  tur kartlari (ROUND 2, SPEED ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 31 vurus: kart 2 / say 14 / buyu 6 / gec 9
  sonuc 3 + RUTBE 3 + abone 3 olcu
Skor: son duvara kadar 20-20; BOSS WALL'da PINK OUT -> BLUE 21-20 (26'da PINK kazanmisti).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 130.0
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-29.json"), encoding="utf-8"))
assert len(DUVAR) == 24

# vurus cinsinden duvar dongusu: kart (kapi acilir) / say (3-2-1, maskot gosterir, karakterler poza girer) / buyu / gec (tam ekran panel)
Z_NORMAL = {"kart": 2, "say": 8, "buyu": 3, "gec": 2}
Z_HIZ = {"kart": 2, "say": 6, "buyu": 2, "gec": 2}          # SPEED: son 4 duvar
Z_BOSS = {"kart": 2, "say": 14, "buyu": 6, "gec": 9}
OUT = {"p1": {6, 14, 20}, "p2": {4, 11, 17, 24}}         # BLUE 21 - 20 PINK (son duvara kadar 20-20)
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):                                  # konum vurus cinsinden (duvarlar olcu ortasinda bitebilir)
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
skor = {"p1": 0, "p2": 0}
plan = [(1, None, 6, Z_NORMAL), (2, ("02", "ROUND 2"), 6, Z_NORMAL), (3, ("03", "SPEED ROUND", "FASTER AND FASTER!"), 6, Z_NORMAL),
        (4, ("04", "FINAL ROUND"), 5, Z_NORMAL), (5, ("!", "BOSS WALL", "WINNER TAKES IT ALL"), 1, Z_BOSS)]
no = 0
for tur, tk, n, Z in plan:
    if tk:
        kart(vur, 1, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        vur += 4
    for j in range(n):
        d = DUVAR[no]; no += 1
        hiz = tur == 3 and j >= 2
        if hiz: Z = Z_HIZ
        out = {o: no in OUT[o] for o in ("p1", "p2")}
        for o in ("p1", "p2"):
            if not out[o]:
                skor[o] += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(vur * V, 4), "z": z, "p1": d["p1"], "p2": d["p2"],
                         "out": out, "skor": dict(skor), "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "hiz": hiz,
                         "nasil": no <= 2})
        vur += sum(Z.values())
kazanan = "p2" if skor["p2"] > skor["p1"] else "p1"
assert skor == {"p1": 21, "p2": 20}, skor
assert vur % 4 == 0, vur                                     # kapanis kartlari olcu basinda
kart(vur, 3, tip="sonuc", kazanan=kazanan, skor=skor); vur += 12
kart(vur, 3, tip="rutbe"); vur += 12
kart(vur, 3, tip="abone"); vur += 12
TOPLAM = vur // 4
assert TOPLAM == 106, TOPLAM
assert 195 <= TOPLAM * O <= 200, TOPLAM * O                  # 3:15-3:20 kurali
assert duvarlar[0]["t0"] <= 5.0, duvarlar[0]["t0"]          # mobil paket md. 1

# SUBSCRIBE her ~15 sn (TALIMATLAR §4), tam ekran kartlarda yok, gec panelinde yok; 3,2 sn
SURE = TOPLAM * O
bos = lambda t: not any(k["t"] - 0.2 <= t <= k["t"] + k["sure"] + 0.2 or k["t"] <= t + 3.2 <= k["t"] + k["sure"] for k in kartlar) and \
    not any(d["t0"] + d["z"]["kart"] + d["z"]["say"] + d["z"]["buyu"] - 0.1 <= t + s <= d["t0"] + d["z"]["sure"] for d in duvarlar for s in (0, 3.2))
abone, t = [], 8.0
while t < SURE - 30:
    q = t
    while not bos(q) and q < t + 6:
        q += 0.1
    if bos(q):
        abone.append(round(q, 2)); t = q + 15
    else:
        t += 1
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-29", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Dark Groove.mp3 (Suno, kullanici; ilk kullanim) -> 01-muzik/human-tetris-29/dark-130.wav (130,0 BPM sabit)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-29.py. Motor 03-motor/sahne26.html (tas kapi girisi, SPEED). Referanssiz (kullanici 15 Kas 2026).",
         "tema": {"varlik": "/03-motor/tetris-pvp/varlik-29s2/tetris-varlik/", "karakter": "/03-motor/tetris-pvp/varlik-29-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-29s2/tetris-varlik/", "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "SPEED ROUND", "4": "FINAL ROUND"},
                  "acilis": "taskapi",
                  "aboneAlt": "NEW BATTLE EVERY DAY"}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-29.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.1f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"], "skor", skor)
