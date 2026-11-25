"""Shared, fixed ingredient layout for the slab, cross section and cut pieces.

Coordinates are relative to the chocolate centre.  The top inclusions are
partly embedded, so a knife cut through their x region removes them too.
"""
import numpy as np

# kind, centre (x,y,z), half size (x,y,z).  The camera looks from -Y.
INGREDIENTS = [
    ("marshmallow", -.88, -.31, .30, .17, .13, .17),
    ("biscuit", -.53, -.19, .34, .18, .13, .105),
    ("hazelnut", -.24, -.35, .32, .115, .105, .11),
    ("marshmallow", .12, -.18, .34, .17, .14, .16),
    ("biscuit", .48, -.32, .32, .19, .12, .105),
    ("hazelnut", .84, -.20, .33, .12, .11, .105),
    ("biscuit", -.96, .21, .32, .15, .14, .10),
    ("hazelnut", -.67, .26, .33, .12, .11, .10),
    ("marshmallow", -.29, .18, .32, .17, .14, .17),
    ("biscuit", .16, .27, .34, .17, .14, .10),
    ("hazelnut", .56, .19, .32, .11, .11, .10),
    ("marshmallow", .91, .19, .32, .15, .13, .15),
    # Pieces buried in the dark chocolate appear on the real cut face.
    ("marshmallow", -.71, .04, -.04, .13, .13, .12),
    ("biscuit", -.38, -.08, -.13, .12, .13, .075),
    ("hazelnut", -.05, .14, .02, .095, .09, .09),
    ("biscuit", .34, -.04, -.07, .14, .11, .075),
    ("marshmallow", .68, .04, -.04, .13, .12, .12),
]

COLORS = {
    "marshmallow": "#f8eee0",
    "biscuit": "#c99c61",
    "hazelnut": "#a46a37",
}


def ingredient_masks(x, y, z):
    """Return the occupied mask and last matching ingredient kind."""
    shape = np.broadcast_shapes(np.shape(x), np.shape(y), np.shape(z))
    occupied = np.zeros(shape, dtype=bool)
    kind = np.zeros(shape, dtype=np.uint8)
    for name, px, py, pz, sx, sy, sz in INGREDIENTS:
        if name == "biscuit":
            inside = (np.abs(x-px) <= sx) & (np.abs(y-py) <= sy) & (np.abs(z-pz) <= sz)
        else:
            inside = ((x-px)/sx)**2 + ((y-py)/sy)**2 + ((z-pz)/sz)**2 <= 1.0
        occupied |= inside
        kind[inside] = (1 if name == "marshmallow" else 2 if name == "biscuit" else 3)
    return occupied, kind
