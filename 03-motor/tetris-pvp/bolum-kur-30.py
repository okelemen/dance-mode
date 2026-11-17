"""HUMAN TETRIS 30 bolum JSON'u (REF-082 yapi, 1v1, cilali 3D yel degirmenli lale tarlasi) - bolum-kur-29.py'den; ozel tur MIRROR
(25 FREEZE, 26 MIRROR, 27 BLIND, 28 FREEZE, 29 SPEED -> 30 MIRROR); giris KANCA (17 Kas 2026, kullanici: boksor yok; BOSS WALL onizleme + geri sarma + lale acilisi, motor 27 TEMA.acilis='kanca').

    python bolum-kur-30.py   ->  bolumler/tetris-mode-30.json

SURE 3:15-3:20 (TALIMATLAR §3) -> 111 olcu = 3:15,9 (136 BPM, vurus 0,4412 sn, olcu 1,7647 sn):
  acilis (kanca 0-1,6 + geri sarma 1,6-2,0 + lale acilisi + WHO WILL WIN?) 2 olcu (ilk duvar 3,53 sn; mobil paket md. 1)
  normal duvar 15 vurus = 6,62 sn: kart 2 / say 8 / buyu 3 / gec 2
  MIRROR ROUND: 6 duvar d.ayna (siluet, panel, karakter, maskot aynalanir; ustte MIRROR!)
  tur kartlari (ROUND 2, MIRROR ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 31 vurus: kart 2 / say 14 / buyu 6 / gec 9
  sonuc 4 + RUTBE 4 + abone 3 olcu (136 BPM'de 3:15'e yetsin diye 29'dan +2 olcu)
Skor: son duvara kadar 20-20; BOSS WALL'da BLUE OUT -> PINK 21-20 (29'da BLUE kazanmisti).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 136.0
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-30.json"), encoding="utf-8"))
assert len(DUVAR) == 24

# vurus cinsinden duvar dongusu: kart (kapi acilir) / say (3-2-1, maskot gosterir, karakterler poza girer) / buyu / gec (tam ekran panel)
Z_NORMAL = {"kart": 2, "say": 8, "buyu": 3, "gec": 2}
Z_BOSS = {"kart": 2, "say": 14, "buyu": 6, "gec": 9}
OUT = {"p1": {4, 11, 18, 24}, "p2": {7, 15, 21}}         # PINK 21 - 20 BLUE (son duvara kadar 20-20)
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):                                  # konum vurus cinsinden (duvarlar olcu ortasinda bitebilir)
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
skor = {"p1": 0, "p2": 0}
plan = [(1, None, 6, Z_NORMAL), (2, ("02", "ROUND 2"), 6, Z_NORMAL), (3, ("03", "MIRROR ROUND", "LEFT IS RIGHT!"), 6, Z_NORMAL),
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
                         "out": out, "skor": dict(skor), "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "ayna": tur == 3,
                         "nasil": no <= 2})
        vur += sum(Z.values())
kazanan = "p2" if skor["p2"] > skor["p1"] else "p1"
assert skor == {"p1": 20, "p2": 21}, skor
assert vur % 4 == 0, vur                                     # kapanis kartlari olcu basinda
kart(vur, 4, tip="sonuc", kazanan=kazanan, skor=skor); vur += 16
kart(vur, 4, tip="rutbe"); vur += 16
kart(vur, 3, tip="abone"); vur += 12
TOPLAM = vur // 4
assert TOPLAM == 111, TOPLAM
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
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-30", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Neon Party Pulse.mp3 (Suno, kullanici; Human Tetris'te ilk kullanim) -> 01-muzik/human-tetris-30/neon-136.wav (136,0 BPM sabit)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-30.py. Motor 03-motor/sahne27.html (lale tarlasi, MIRROR). Referans REF-082 (yapi), mekan bizden (kullanici 17 Kas 2026).",
         "tema": {"acilis": "kanca", "varlik": "/03-motor/tetris-pvp/varlik-30s1/tetris-varlik/", "karakter": "/03-motor/tetris-pvp/varlik-30-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-30s1/tetris-varlik/", "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "MIRROR ROUND", "4": "FINAL ROUND"},
                  "aboneAlt": "NEW BATTLE EVERY DAY"}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-30.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.1f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"], "skor", skor)
