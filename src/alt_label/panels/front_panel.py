"""Front hero panel — Retail Master Lock v2.0 hierarchy."""

from reportlab.pdfgen.canvas import Canvas

from ..colors import ACCENT_MAP, CHAMPAGNE_GOLD, MATTE_BLACK, WARM_OFF_WHITE
from ..layout import LabelLayout
from .a_symbol import draw_a_symbol


def _draw_centered_text(
    c: Canvas,
    text: str,
    cx: float,
    y: float,
    font: str,
    size: float,
    color,
    line_height: float = 1.35,
) -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    tw = c.stringWidth(text, font, size)
    c.drawString(cx - tw / 2, y, text)
    return y - size * line_height


def render_front_panel(
    c: Canvas,
    layout: LabelLayout,
    brand: dict,
    sku: dict,
    flavor: dict,
    typo: dict,
) -> None:
    panel = layout.front_panel
    accent_key = flavor.get("accent_color", "champagne_gold")
    accent = ACCENT_MAP.get(accent_key, CHAMPAGNE_GOLD)

    c.setFillColor(MATTE_BLACK)
    c.rect(panel.x, panel.y, panel.width, panel.height, fill=1, stroke=0)

    cx = panel.center_x
    y = panel.y + panel.height - mm_to_pt(6)

    # 1. Tagline
    y = _draw_centered_text(
        c, brand["brand"]["tagline"], cx, y,
        "Helvetica", typo["tagline"], WARM_OFF_WHITE,
    )
    y -= typo["tagline"] * 0.4

    # 2. Hero A Symbol — reduced 10%, supports wordmark (does not compete)
    a_height = 26 * typo.get("a_symbol_scale", 0.90)
    y = draw_a_symbol(c, cx, y, a_height, WARM_OFF_WHITE)
    y -= typo.get("brand_name_spacing", 1.5) * 4

    # 3. ALTERNATIVE™ — dominant brand asset (+22.5%)
    brand_size = 20 * typo.get("brand_name_scale", 1.225)
    y = _draw_centered_text(
        c, brand["brand"]["name"], cx, y,
        "Helvetica-Bold", brand_size, accent,
        line_height=typo.get("brand_name_spacing", 1.6),
    )

    # 4. Positioning — secondary, off-white
    y = _draw_centered_text(
        c, brand["brand"]["positioning"], cx, y,
        "Helvetica", typo["positioning"], WARM_OFF_WHITE,
    )
    y -= typo["positioning"] * 0.25

    # 5. SKU — secondary, off-white
    y = _draw_centered_text(
        c, sku["name"], cx, y,
        "Helvetica-Bold", typo["sku"], WARM_OFF_WHITE,
    )

    # 6. THC strength — single-line callout, accent (shelf priority #2)
    thc_line = sku.get("thc_line") or f"{sku['thc_mg']}MG HEMP-DERIVED THC PER CAN"
    y = _draw_centered_text(
        c, thc_line, cx, y,
        "Helvetica-Bold", typo["thc_content"], accent,
        line_height=1.4,
    )
    y -= typo["thc_content"] * 0.2

    # 7. Flavor — increased 35%, accent (shelf priority #3)
    flavor_size = typo.get("flavor_base", 8.5) * typo.get("flavor_scale", 1.35)
    y = _draw_centered_text(
        c, flavor["name"], cx, y,
        "Helvetica-Bold", flavor_size, accent,
    )

    # 8. Net contents
    net = brand.get("net_contents", "12 FL OZ (355 mL)")
    _draw_centered_text(
        c, net, cx, panel.y + mm_to_pt(8),
        "Helvetica", typo["net_contents"], WARM_OFF_WHITE,
    )


def mm_to_pt(mm: float) -> float:
    return mm * 72 / 25.4
