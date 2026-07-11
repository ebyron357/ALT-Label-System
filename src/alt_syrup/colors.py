"""CMYK colors — shared ALTERNATIVE™ palette."""

from reportlab.lib.colors import CMYKColor


def cmyk(c: float, m: float, y: float, k: float) -> CMYKColor:
    return CMYKColor(c / 100, m / 100, y / 100, k / 100)


MATTE_BLACK = cmyk(0, 0, 0, 100)
WARM_OFF_WHITE = cmyk(0, 3, 8, 4)
CHAMPAGNE_GOLD = cmyk(0, 15, 35, 15)
DEEP_AMBER = cmyk(0, 45, 75, 25)
BERRY_ACCENT = cmyk(25, 55, 30, 10)
CITRUS_ACCENT = cmyk(0, 25, 55, 10)

ACCENT_MAP = {
    "champagne_gold": CHAMPAGNE_GOLD,
    "deep_amber": DEEP_AMBER,
    "berry_accent": BERRY_ACCENT,
    "citrus_accent": CITRUS_ACCENT,
}
