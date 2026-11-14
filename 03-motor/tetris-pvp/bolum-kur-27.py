"""HUMAN TETRIS 27 bolum JSON'u (referanssiz, CO-OP 2 oyuncu, cilali 3D karli dag zirvesi) - bolum-kur-26.py'den; ozel tur BLIND
(24 SPEED, 25 FREEZE, 26 MIRROR -> 27 BLIND, seride ilk).

    python bolum-kur-27.py   ->  bolumler/tetris-mode-27.json

SURE 3:15-3:20 (kullanici 14 Kas 2026: "bu video ve bundan sonraki videolar 3 dakika 15 saniye ya da 3 dakika 20 saniye") ->
104 olcu = 3:18,1 (ilk hal 166 olcu = 5:16 idi). 24 duvar / 24 poz / turlar / OUT'lar ayni; dongu kisaldi.
Vurus cizelgesi (126 BPM, vurus 0,476 sn, olcu 1,905 sn):
  acilis 2 olcu (ilk duvar 3,81 sn; mobil paket md. 1)
  normal duvar 15 vurus = 7,14 sn: kart 2 (0,95) / say 8 (3,81; BLIND'da son 1,5 sn siluet) / buyu 3 (1,43) / gec 2 (0,95)
  tur kartlari (ROUND 2, BLIND ROUND, FINAL ROUND, BOSS WALL) 1'er olcu
  BOSS WALL 23 vurus: kart 2 / say 12 / buyu 5 / gec 4
  sonuc 2 + RUTBE 2 + abone 2 olcu
CO-OP: tek duvar, iki oyuncu ayni ikili pozu birlikte yapar. Biri gec kalirsa duvar ikisini birden kar yiginlarina iter (OUT),
o duvar sayilmaz. Sayac WALLS CLEARED n/24. OUT: 5 (PINK gec), 11 (BLUE gec), 16 (BLIND, PINK gec) -> 21/24 = SILVER.
BOSS WALL gecilir (son duvar zafer).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 126.0
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-27.json"), encoding="utf-8"))
assert len(DUVAR) == 24

Z_NORMAL = {"kart": 2, "say": 8, "buyu": 3, "gec": 2}       # 3:15-3:20 kurali (14 Kas 2026)
Z_BOSS = {"kart": 2, "say": 12, "buyu": 5, "gec": 4}
OUT = {5: "p2", 11: "p1", 16: "p2"}
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):                                  # konum vurus cinsinden (duvarlar olcu ortasinda bitebilir)
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
temiz = 0
plan = [(1, None, 6, Z_NORMAL), (2, ("02", "ROUND 2"), 6, Z_NORMAL), (3, ("03", "BLIND ROUND", "WHITEOUT!"), 6, Z_NORMAL),
        (4, ("04", "FINAL ROUND"), 5, Z_NORMAL), (5, ("!", "BOSS WALL", "CLEAR IT TOGETHER"), 1, Z_BOSS)]
no = 0
for tur, tk, n, Z in plan:
    if tk:
        kart(vur, 1, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        vur += 4
    for _ in range(n):
        d = DUVAR[no]; no += 1
        assert d["tur"] == {1: "ROUND 1", 2: "ROUND 2", 3: "BLIND ROUND", 4: "FINAL ROUND", 5: "FINAL ROUND"}[tur], (no, d["tur"])
        out = {o: OUT.get(no) == o for o in ("p1", "p2")}
        if not any(out.values()):
            temiz += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(vur * V, 4), "z": z, "grup": d["grup"], "video": d["video"],
                         "out": out, "skor": temiz, "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "blind": tur == 3,
                         "nasil": no <= 2})
        vur += sum(Z.values())
assert temiz == 21, temiz
rutbe = "GOLD" if temiz == 24 else "SILVER" if temiz >= 18 else "BRONZE"
assert vur % 4 == 0, vur                                     # kapanis kartlari olcu basinda
kart(vur, 2, tip="sonuc", skor=temiz, toplam=len(duvarlar), rutbe=rutbe); vur += 8
kart(vur, 2, tip="rutbe"); vur += 8
kart(vur, 2, tip="abone"); vur += 8
TOPLAM = vur // 4
assert TOPLAM == 104, TOPLAM
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
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-27", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Frostbite Knockout.wav (Suno, kullanici, 21 Eki 2026; TETRIS MODE 6da da) -> 01-muzik/human-tetris-27/frost-126.wav (123->129 kayiyordu, 126 BPM sabit, sapma 0,34)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-27.py. Motor 03-motor/sahne24.html (CO-OP). Referanssiz (kullanici 14 Kas 2026).",
         "tema": {"varlik": "/03-motor/tetris-pvp/varlik-27s2/tetris-varlik/", "karakter": "/03-motor/tetris-pvp/varlik-27-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-27-grup/", "maskeKlasor": "",
                  "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "BLIND ROUND", "4": "FINAL ROUND"},
                  "aboneAlt": "NEW BATTLE EVERY DAY"}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-27.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.1f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"],
      "temiz", temiz, rutbe)
