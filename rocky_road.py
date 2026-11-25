"""Shared, fixed ingredient layout for the slab, cross section and cut pieces.

Coordinates are relative to the chocolate centre.  The top inclusions are
partly embedded, so a knife cut through their x region removes them too.
"""
import numpy as np

# kind, centre (x,y,z), half size (x,y,z).  The camera looks from -Y.
INGREDIENTS = [
    ("marshmallow", -.93, -.24, .30, .15, .12, .13),
    ("biscuit", -.72, .17, .33, .13, .11, .09),
    ("hazelnut", -.51, -.34, .31, .095, .09, .09),
    ("marshmallow", -.31, .02, .32, .15, .14, .13),
    ("biscuit", -.03, -.27, .32, .16, .11, .09),
    ("hazelnut", .18, .28, .32, .10, .09, .09),
    ("biscuit", .45, -.05, .33, .16, .13, .09),
    ("hazelnut", .71, -.29, .32, .10, .10, .09),
    ("marshmallow", .94, .17, .30, .15, .13, .13),
    ("biscuit", -.96, .25, .32, .12, .10, .09),
    ("marshmallow", .10, .03, .31, .13, .12, .13),
    ("hazelnut", .59, .29, .33, .11, .09, .09),
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
        if name in ("biscuit", "marshmallow"):
            inside = (np.abs(x-px) <= sx) & (np.abs(y-py) <= sy) & (np.abs(z-pz) <= sz)
        else:
            inside = ((x-px)/sx)**2 + ((y-py)/sy)**2 + ((z-pz)/sz)**2 <= 1.0
        occupied |= inside
        kind[inside] = (1 if name == "marshmallow" else 2 if name == "biscuit" else 3)
    return occupied, kind
