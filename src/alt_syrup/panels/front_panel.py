"""Front panel — LOCKED hierarchy, master footer alignment."""

from reportlab.pdfgen.canvas import Canvas

from ..colors import ACCENT_MAP, CHAMPAGNE_GOLD, DIVIDER, MATTE_BLACK, WARM_OFF_WHITE
from ..layout import SyrupLayout


def _center(c: Canvas, text: str, cx: float, y: float, font: str, size: float, color, lh: float = 1.35) -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    tw = c.stringWidth(text, font, size)
    c.drawString(cx - tw / 2, y, text)
    return y - size * lh


def _render_master_footer(
    c: Canvas,
    safe,
    cx: float,
    brand: dict,
    product: dict,
    typo: dict,
) -> None:
    """Shared footer structure — ALT ORIGINAL master alignment for all SKUs."""
    net_y = safe.y + 6
    age_y = safe.y + 14
    stmt_y = safe.y + 22
    divider_y = safe.y + 28

    c.setStrokeColor(DIVIDER)
    c.setLineWidth(0.4)
    inset = 10
    c.line(safe.x + inset, divider_y, safe.x + safe.width - inset, divider_y)

    _center(c, product["net_contents"], cx, net_y, "Helvetica", typo["net_contents"], WARM_OFF_WHITE, 1.2)

    age_gate = brand["brand"].get("age_gate", "21+")
    age_size = typo.get("age_gate", 5.0)
    _center(c, age_gate, cx, age_y, "Helvetica", age_size, WARM_OFF_WHITE, 1.0)

    stmt = brand["brand"]["statement_of_identity"]
    stmt_size = typo.get("statement_of_identity", 6.6)
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica", stmt_size)
    tw = c.stringWidth(stmt, "Helvetica", stmt_size)
    c.drawString(cx - tw / 2, stmt_y, stmt)


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

    _render_master_footer(c, safe, cx, brand, product, typo)
