"""Front panel — LOCKED hierarchy, improved spacing."""

from reportlab.pdfgen.canvas import Canvas

from ..colors import ACCENT_MAP, CHAMPAGNE_GOLD, MATTE_BLACK, WARM_OFF_WHITE
from ..layout import SyrupLayout


def _center(c: Canvas, text: str, cx: float, y: float, font: str, size: float, color, lh: float = 1.35) -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    tw = c.stringWidth(text, font, size)
    c.drawString(cx - tw / 2, y, text)
    return y - size * lh


def render_front_panel(
    c: Canvas,
    layout: SyrupLayout,
    brand: dict,
    flavor: dict,
    typo: dict,
) -> None:
    panel = layout.front
    safe = layout.safe_front
    accent = ACCENT_MAP.get(flavor.get("accent_color", "champagne_gold"), CHAMPAGNE_GOLD)
    product = brand["product"]

    c.setFillColor(MATTE_BLACK)
    c.rect(panel.x, panel.y, panel.width, panel.height, fill=1, stroke=0)

    cx = safe.center_x
    y = safe.y + safe.height - 4

    # LOCKED HIERARCHY — do not alter order
    y = _center(c, brand["brand"]["name"], cx, y, "Helvetica-Bold", typo["brand_name"], accent, 1.5)
    y -= 2
    y = _center(c, flavor["name"], cx, y, "Helvetica-Bold", typo["flavor_name"], accent, 1.4)
    y -= 3
    y = _center(c, f"{product['total_thc_mg']} MG THC", cx, y, "Helvetica-Bold", typo["thc_total"], WARM_OFF_WHITE, 1.35)
    y = _center(c, f"{product['thc_per_serving_mg']} MG THC PER SERVING", cx, y, "Helvetica-Bold", typo["thc_per_serving"], accent, 1.3)
    y = _center(c, f"{product['servings_per_container']} SERVINGS", cx, y, "Helvetica", typo["servings"], WARM_OFF_WHITE, 1.3)
    _center(c, product["net_contents"], cx, safe.y + 6, "Helvetica", typo["net_contents"], WARM_OFF_WHITE, 1.2)

    # Age gate — secondary retail cue, text only
    age_gate = brand["brand"].get("age_gate", "21+")
    age_size = max(typo["net_contents"] - 1.5, 5.5)
    _center(c, age_gate, cx, safe.y + 15, "Helvetica", age_size, WARM_OFF_WHITE, 1.1)

    # Statement of identity — secondary, bottom area
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica", typo["net_contents"] - 1.5)
    stmt = brand["brand"]["statement_of_identity"]
    tw = c.stringWidth(stmt, "Helvetica", typo["net_contents"] - 1.5)
    c.drawString(cx - tw / 2, safe.y + 22, stmt)
