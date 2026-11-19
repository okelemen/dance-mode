"""HUMAN TETRIS 33: Actions karakter artifact'lerini (p1, p2, maskot) tek klasorde birlestirir -> varlik-33-karakter/
(karakter/<oyuncu>/*.png + yerlesim.json["karakter"][oyuncu]); motor TEMA.karakter bu klasoru okur."""
import json, os, shutil

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = {"p1": "varlik-33-k-p1", "p2": "varlik-33-k-p2", "maskot": "varlik-33-k-maskot"}
HEDEF = os.path.join(BURA, "varlik-33-karakter")
Y = {"karakter": {}}
for o, d in KAYNAK.items():
    k = os.path.join(BURA, d)
    y = json.load(open(os.path.join(k, "yerlesim.json"), encoding="utf-8"))["karakter"][o]
    Y["karakter"][o] = y
    hedef = os.path.join(HEDEF, "karakter", o); os.makedirs(hedef, exist_ok=True)
    n = 0
    for f in os.listdir(os.path.join(k, "karakter", o)):
        shutil.copy(os.path.join(k, "karakter", o, f), os.path.join(hedef, f)); n += 1
    print(o, n, "kare")
json.dump(Y, open(os.path.join(HEDEF, "yerlesim.json"), "w", encoding="utf-8"), indent=1)
D = json.load(open(os.path.join(BURA, "duvar-listesi-33.json"), encoding="utf-8"))
for o in ("p1", "p2"):
    eksik = [w[o] for w in D if not os.path.exists(os.path.join(HEDEF, "karakter", o, w[o] + "-00.png"))]
    assert not eksik, (o, eksik[:3])
eksik = [w[o] for w in D for o in ("p1", "p2") if not os.path.exists(os.path.join(HEDEF, "karakter", "maskot", w[o] + "-00.png"))]
assert not eksik, ("maskot", eksik[:3])
print("->", HEDEF, "tamam")
