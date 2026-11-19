"""HUMAN TETRIS 32 bolum JSON'u (REF-084 yapi, 3 PLAYER BATTLE, cilali 3D Noel oyuncak atolyesi) - bolum-kur-31.py'den; ozel tur SPEED
(27 BLIND, 28 FREEZE, 29 SPEED, 30 MIRROR, 31 FREEZE -> 32 SPEED). Giris KANCA (motor TEMA.acilis='kanca').
SURE 3:15-3:20 (TALIMATLAR §3) -> 110 olcu = 3:16,8 (134,14 BPM, vurus 0,4473 sn, olcu 1,7892 sn; Golden Groove):
  acilis (kanca + geri sarma + hediye kutusu acilisi + WHO WILL WIN?) 2 olcu (ilk duvar 3,58 sn; mobil paket md. 1)
  normal duvar 16 vurus = 7,16 sn: kart 2 / say 8 / buyu 3 / gec 3   (3 oyuncu: hakem uc pozu sirayla gosterir)
  SPEED turu: ilk 2 duvar normal, son 4 duvar 12 vurus (kart 2 / say 6 / buyu 2 / gec 2) + FASTER!
  tur kartlari (ROUND 2, SPEED ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 28 vurus: kart 2 / say 12 / buyu 6 / gec 8
  sonuc 3 + RUTBE 3 + abone 3 olcu
Skor: son duvara kadar 20-20-20; BOSS WALL'da BLUE ve PINK OUT -> GREEN 21 (30 PINK, 31 BLUE kazanmisti).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 134.14
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-32.json"), encoding="utf-8"))
assert len(DUVAR) == 24

Z_NORMAL = {"kart": 2, "say": 8, "buyu": 3, "gec": 3}
Z_SPEED = {"kart": 2, "say": 6, "buyu": 2, "gec": 2}
Z_BOSS = {"kart": 2, "say": 12, "buyu": 6, "gec": 8}
OY = ("p1", "p2", "p3")
OUT = {"p1": {4, 11, 18, 24}, "p2": {7, 14, 21, 24}, "p3": {2, 9, 16}}   # 23. duvar sonunda 20-20-20; BOSS: BLUE & PINK OUT -> GREEN 21
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
skor = {o: 0 for o in OY}
plan = [(1, None, 6), (2, ("02", "ROUND 2"), 6), (3, ("03", "SPEED ROUND", "FASTER AND FASTER!"), 6),
        (4, ("04", "FINAL ROUND"), 5), (5, ("!", "BOSS WALL", "WINNER TAKES IT ALL"), 1)]
no = 0
for tur, tk, n in plan:
    if tk:
        kart(vur, 1, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        vur += 4
    for j in range(n):
        d = DUVAR[no]; no += 1
        hiz = tur == 3 and j >= 2
        Z = Z_BOSS if tur == 5 else Z_SPEED if hiz else Z_NORMAL
        out = {o: no in OUT[o] for o in OY}
        for o in OY:
            if not out[o]:
                skor[o] += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(vur * V, 4), "z": z, "p1": d["p1"], "p2": d["p2"], "p3": d["p3"],
                         "out": out, "skor": dict(skor), "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "hiz": hiz,
                         "nasil": no <= 2})
        vur += sum(Z.values())
assert [duvarlar[22]["skor"][o] for o in OY] == [20, 20, 20], duvarlar[22]["skor"]
assert skor == {"p1": 20, "p2": 20, "p3": 21}, skor
kazanan = max(OY, key=lambda o: skor[o])
assert vur % 4 == 0, vur
kart(vur, 3, tip="sonuc", kazanan=kazanan, skor=skor); vur += 12
kart(vur, 3, tip="rutbe"); vur += 12
kart(vur, 3, tip="abone"); vur += 12
TOPLAM = vur // 4
assert TOPLAM == 110, TOPLAM
assert 195 <= TOPLAM * O <= 200, TOPLAM * O
assert duvarlar[0]["t0"] <= 5.0, duvarlar[0]["t0"]

SURE = TOPLAM * O
bos = lambda t: not any(k["t"] - 0.2 <= t <= k["t"] + k["sure"] + 0.2 or k["t"] <= t + 3.2 <= k["t"] + k["sure"] for k in kartlar) and \
    not any(d["t0"] + d["z"]["kart"] + d["z"]["say"] + d["z"]["buyu"] - 0.1 <= t + s <= d["t0"] + d["z"]["sure"] for d in duvarlar for s in (0, 3.2))
abone, t = [], 18.0                     # motor 29: abone satiri ustte, HOW TO PLAY seridiyle (ilk 2 duvar) cakismasin
while t < SURE - 30:
    q = t
    while not bos(q) and q < t + 6:
        q += 0.1
    if bos(q):
        abone.append(round(q, 2)); t = q + 15
    else:
        t += 1
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-32", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Golden Groove.mp3 (Suno; Human Tetris'te ilk kullanim, kullanici 19 Kas) -> 01-muzik/human-tetris-32/golden-32-dizili.wav (134,14 BPM sabit, 110 olcu)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-32.py. Motor 03-motor/sahne29.html (uc serit Noel oyuncak atolyesi, SPEED, panda hakem). Referans REF-084 (yapi), mekan bizden (kullanici 19 Kas 2026).",
         "tema": {"acilis": "kanca", "varlik": "/03-motor/tetris-pvp/varlik-32s1/", "karakter": "/03-motor/tetris-pvp/varlik-32-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-32s1/", "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "SPEED ROUND", "4": "FINAL ROUND"},
                  "renk": ["#1ad2ff", "#ff2ad2", "#2ee860"], "acik": ["#d6f6ff", "#ffd6f4", "#d6ffe0"], "koyu": ["#0a5ad8", "#b0108c", "#0a8a2a"],
                  "ad": ["BLUE", "PINK", "GREEN"], "aboneAlt": "NEW BATTLE EVERY DAY"}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-32.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.1f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"], "skor", skor)
