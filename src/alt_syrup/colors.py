"""CMYK colors — shared ALTERNATIVE™ palette."""

from reportlab.lib.colors import CMYKColor


def cmyk(c: float, m: float, y: float, k: float) -> CMYKColor:
    return CMYKColor(c / 100, m / 100, y / 100, k / 100)


MATTE_BLACK = cmyk(0, 0, 0, 100)
WARM_OFF_WHITE = cmyk(0, 3, 8, 4)
CHAMPAGNE_GOLD = cmyk(0, 15, 35, 15)
DEEP_AMBER = cmyk(0, 38, 62, 28)
BERRY_ACCENT = cmyk(25, 55, 30, 10)
STRAWBERRY_ACCENT = cmyk(18, 72, 48, 22)
CITRUS_ACCENT = cmyk(0, 25, 55, 10)
DIVIDER = cmyk(0, 2, 5, 35)

ACCENT_MAP = {
    "champagne_gold": CHAMPAGNE_GOLD,
    "deep_amber": DEEP_AMBER,
    "berry_accent": BERRY_ACCENT,
    "strawberry_accent": STRAWBERRY_ACCENT,
    "citrus_accent": CITRUS_ACCENT,
}
