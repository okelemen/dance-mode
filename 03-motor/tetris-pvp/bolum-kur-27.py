"""HUMAN TETRIS 27 bolum JSON'u (referanssiz, CO-OP 2 oyuncu, cilali 3D karli dag zirvesi) - bolum-kur-26.py'den; ozel tur BLIND
(24 SPEED, 25 FREEZE, 26 MIRROR -> 27 BLIND, seride ilk).

    python bolum-kur-27.py   ->  bolumler/tetris-mode-27.json

Olcu cizelgesi (126 BPM, olcu 1,905 sn):
  0-2     acilis CO-OP karti + "CAN YOU CLEAR ALL 24 WALLS?" (ilk duvar 3,81 sn; mobil paket md. 1)
  2-38    ROUND 1: 6 duvar x 6 olcu (ilk iki duvarda HOW TO PLAY seridi)
  38-40   ROUND 2 karti; 40-76 6 duvar x 6
  76-78   BLIND ROUND karti ("WHITEOUT!"); 78-114 6 duvar x 6 (siluet kar firtinasinin arkasinda, son 1,5 sn'de belirir - motor 24)
  114-116 FINAL ROUND karti; 116-146 5 duvar x 6
  146-148 BOSS WALL karti; 148-156 son duvar 8 olcu
  156-159 sonuc (TEAM 21/24 + SILVER); 159-162 RUTBE; 162-166 abone + LIKE/COMMENT/SHARE
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

Z_NORMAL = {"kart": 4, "say": 12, "buyu": 4, "gec": 4}
Z_BOSS = {"kart": 4, "say": 16, "buyu": 6, "gec": 6}
OUT = {5: "p2", 11: "p1", 16: "p2"}
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(olcu, sure_olcu, **k):
    kartlar.append(dict(t=round(olcu * O, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
olcu = 2
temiz = 0
plan = [(1, None, 6, Z_NORMAL), (2, ("02", "ROUND 2"), 6, Z_NORMAL), (3, ("03", "BLIND ROUND", "WHITEOUT!"), 6, Z_NORMAL),
        (4, ("04", "FINAL ROUND"), 5, Z_NORMAL), (5, ("!", "BOSS WALL", "CLEAR IT TOGETHER"), 1, Z_BOSS)]
no = 0
for tur, tk, n, Z in plan:
    if tk:
        kart(olcu, 2, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        olcu += 2
    for _ in range(n):
        d = DUVAR[no]; no += 1
        assert d["tur"] == {1: "ROUND 1", 2: "ROUND 2", 3: "BLIND ROUND", 4: "FINAL ROUND", 5: "FINAL ROUND"}[tur], (no, d["tur"])
        out = {o: OUT.get(no) == o for o in ("p1", "p2")}
        if not any(out.values()):
            temiz += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(olcu * O, 4), "z": z, "grup": d["grup"], "video": d["video"],
                         "out": out, "skor": temiz, "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "blind": tur == 3,
                         "nasil": no <= 2})
        olcu += sum(Z.values()) // 4
assert temiz == 21, temiz
rutbe = "GOLD" if temiz == 24 else "SILVER" if temiz >= 18 else "BRONZE"
kart(olcu, 3, tip="sonuc", skor=temiz, toplam=len(duvarlar), rutbe=rutbe); olcu += 3
kart(olcu, 3, tip="rutbe"); olcu += 3
kart(olcu, 4, tip="abone"); olcu += 4
TOPLAM = olcu
assert TOPLAM == 166, TOPLAM
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
