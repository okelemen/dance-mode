"""Blender'da sahne kurulduktan sonra her karede sap/topuk-meyve kesismesi denetimi.

Kullanim: blender -b sahne.blend -P denet_sap.py -- --son 300
"""
import sys

import bpy
from mathutils import Vector


def sinirlar(nesne, dg):
    n = nesne.evaluated_get(dg)
    noktalar = [n.matrix_world @ Vector(k) for k in n.bound_box]
    return [(min(v[i] for v in noktalar), max(v[i] for v in noktalar)) for i in range(3)]


son = int(sys.argv[sys.argv.index("--son") + 1]) if "--son" in sys.argv else bpy.context.scene.frame_end
sc = bpy.context.scene
meyve = bpy.data.objects["meyve"]
parcalar = [bpy.data.objects["bicak_sap"], bpy.data.objects["bicak_topuk"]]
hatalar = []
for f in range(1, son + 1):
    sc.frame_set(f)
    if meyve.hide_render:
        continue
    dg = bpy.context.evaluated_depsgraph_get()
    meyve_kutu = sinirlar(meyve, dg)
    for parca in parcalar:
        kutu = sinirlar(parca, dg)
        if all(kutu[i][0] < meyve_kutu[i][1] and meyve_kutu[i][0] < kutu[i][1] for i in range(3)):
            hatalar.append((f, parca.name))
if hatalar:
    print("SAP_KESISME_HATASI", hatalar[:30], "toplam", len(hatalar), flush=True)
    raise SystemExit(1)
print(f"SAP_KONTROL_TEMIZ 1..{son}: sap ve topuk meyvenin sinir kutusuna girmedi", flush=True)
