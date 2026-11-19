"""HUMAN TETRIS 33 bolum JSON'u (REF-085 yapi, 1v1, cilali 3D antik kum arenasi) - bolum-kur-31.py'den; ozel tur BLIND
(27 BLIND, 28 FREEZE, 29 SPEED, 30 MIRROR, 31 FREEZE, 32 SPEED -> 33 BLIND). Giris KANCA (motor TEMA.acilis='kanca').
SURE 3:15-3:20 (TALIMATLAR §3) -> 106 olcu = 3:16,3 (129,58 BPM, vurus 0,4630 sn, olcu 1,8521 sn; Stardust Crown):
  acilis (kanca + geri sarma + arena kapisi acilisi + WHO WILL WIN?) 2 olcu (ilk duvar 3,70 sn; mobil paket md. 1)
  normal duvar 14 vurus = 6,48 sn: kart 2 / say 7 / buyu 3 / gec 2
  BLIND duvari 16 vurus: kart 2 / say 9 (4,17 sn; siluet son 1,5 sn'de belirir) / buyu 3 / gec 2
  tur kartlari (ROUND 2, BLIND ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 30 vurus: kart 2 / say 12 / buyu 6 / gec 10
  sonuc 3 + RUTBE 3 + abone 3 olcu
Skor: son duvara kadar 20-20; BOSS WALL'da BLUE OUT -> PINK 21-20 (31'de BLUE kazanmisti).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 129.58
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-33.json"), encoding="utf-8"))
assert len(DUVAR) == 24

# vurus cinsinden duvar dongusu: kart (kapi acilir) / say (3-2-1, maskot gosterir, karakterler poza girer) / buyu / gec (tam ekran panel)
Z_NORMAL = {"kart": 2, "say": 7, "buyu": 3, "gec": 2}
Z_BLIND = {"kart": 2, "say": 9, "buyu": 3, "gec": 2}
Z_BOSS = {"kart": 2, "say": 12, "buyu": 6, "gec": 10}
OUT = {"p1": {3, 10, 17, 24}, "p2": {6, 13, 20}}         # PINK 21 - 20 BLUE (son duvara kadar 20-20; 13 ve 17 BLIND turunda)
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):                                  # konum vurus cinsinden (duvarlar olcu ortasinda bitebilir)
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
skor = {"p1": 0, "p2": 0}
plan = [(1, None, 6, Z_NORMAL), (2, ("02", "ROUND 2"), 6, Z_NORMAL), (3, ("03", "BLIND ROUND", "SANDSTORM!"), 6, Z_BLIND),
        (4, ("04", "FINAL ROUND"), 5, Z_NORMAL), (5, ("!", "BOSS WALL", "WINNER TAKES IT ALL"), 1, Z_BOSS)]
no = 0
for tur, tk, n, Z in plan:
    if tk:
        kart(vur, 1, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        vur += 4
    for j in range(n):
        d = DUVAR[no]; no += 1
        out = {o: no in OUT[o] for o in ("p1", "p2")}
        for o in ("p1", "p2"):
            if not out[o]:
                skor[o] += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(vur * V, 4), "z": z, "p1": d["p1"], "p2": d["p2"],
                         "out": out, "skor": dict(skor), "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "blind": tur == 3,
                         "nasil": no <= 2})
        vur += sum(Z.values())
kazanan = "p2" if skor["p2"] > skor["p1"] else "p1"
assert skor == {"p1": 20, "p2": 21}, skor
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
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-33", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Stardust Crown.wav (Suno; HT 9'dan beri ilk, kullanici 19 Kas) -> 01-muzik/human-tetris-33/stardust-33-dizili.wav (129,58 BPM sabit, 106 olcu)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-33.py. Motor 03-motor/sahne30.html (antik kum arenasi, BLIND, ejderha hakem). Referans REF-085 (yapi), mekan bizden (kullanici 19 Kas 2026).",
         "tema": {"acilis": "kanca", "varlik": "/03-motor/tetris-pvp/varlik-33s1/", "karakter": "/03-motor/tetris-pvp/varlik-33-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-33s1/", "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "BLIND ROUND", "4": "FINAL ROUND"},
                  "aboneAlt": "NEW BATTLE EVERY DAY"}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-33.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.1f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"], "skor", skor)
