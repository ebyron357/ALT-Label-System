"""Front hero panel — brand hierarchy per Production Master v1."""

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
) -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    tw = c.stringWidth(text, font, size)
    c.drawString(cx - tw / 2, y, text)
    return y - size * 1.35


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

    # Matte black background for front panel
    c.setFillColor(MATTE_BLACK)
    c.rect(panel.x, panel.y, panel.width, panel.height, fill=1, stroke=0)

    cx = panel.center_x
    y = panel.y + panel.height - mm_to_pt_local(6)

    # 1. Tagline — TOP
    y = _draw_centered_text(
        c, brand["brand"]["tagline"], cx, y,
        "Helvetica", typo["tagline"], WARM_OFF_WHITE,
    )
    y -= typo["tagline"] * 0.5

    # 2. Hero A Symbol — reduced ~12.5%
    a_height = 52 * typo.get("a_symbol_scale", 0.875)
    y = draw_a_symbol(c, cx, y, a_height, WARM_OFF_WHITE)

    # 3. ALTERNATIVE™ — increased ~22.5%, primary recognition
    brand_size = 18 * typo.get("brand_name_scale", 1.225)
    y = _draw_centered_text(
        c, brand["brand"]["name"], cx, y,
        "Helvetica-Bold", brand_size, accent,
    )

    # 4. HEMP-DERIVED THC BEVERAGE
    y = _draw_centered_text(
        c, brand["brand"]["positioning"], cx, y,
        "Helvetica", typo["positioning"], WARM_OFF_WHITE,
    )
    y -= typo["positioning"] * 0.3

    # 5. SKU
    y = _draw_centered_text(
        c, sku["name"], cx, y,
        "Helvetica-Bold", typo["sku"], accent,
    )

    # 6. THC CONTENT — largest product-specific element
    y = _draw_centered_text(
        c, sku["thc_display"], cx, y,
        "Helvetica-Bold", typo["thc_content"], WARM_OFF_WHITE,
    )
    y = _draw_centered_text(
        c, sku["thc_subtext"], cx, y,
        "Helvetica", typo["thc_subtext"], WARM_OFF_WHITE,
    )
    y -= typo["thc_subtext"] * 0.4

    # 7. FLAVOR — increased ~35%
    flavor_size = typo["positioning"] * typo.get("flavor_scale", 1.35)
    y = _draw_centered_text(
        c, flavor["name"], cx, y,
        "Helvetica-Bold", flavor_size, accent,
    )

    # 8. Net contents
    _draw_centered_text(
        c, "12 FL OZ (355 mL)", cx, panel.y + mm_to_pt_local(8),
        "Helvetica", typo["net_contents"], WARM_OFF_WHITE,
    )


def mm_to_pt_local(mm: float) -> float:
    return mm * 72 / 25.4
