"""Information panel — compliance, QR, barcode, warnings."""

import io
from typing import Any

import qrcode
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from ..colors import CHAMPAGNE_GOLD, MATTE_BLACK, WARM_OFF_WHITE
from ..layout import LabelLayout
from .nutrition_facts import render_nutrition_facts


def render_compliance_panel(
    c: Canvas,
    layout: LabelLayout,
    brand: dict,
    sku: dict,
    compliance: dict | None,
    typo: dict,
) -> None:
    panel = layout.info_panel
    c.setFillColor(MATTE_BLACK)
    c.rect(panel.x, panel.y, panel.width, panel.height, fill=1, stroke=0)

    _render_qr_section(c, layout, brand, compliance, typo)
    _render_barcode_zone(c, layout, compliance, typo)
    _render_website(c, layout, brand, typo)

    if compliance and compliance.get("verified"):
        render_nutrition_facts(c, layout.nutrition_zone, compliance["nutrition_facts"], typo)
        _render_ingredients(c, layout, compliance, typo)
        _render_active_ingredient(c, layout, brand, sku, typo)
        _render_manufacturing(c, layout, brand, typo)
        _render_warning(c, layout, brand, typo)
        if compliance.get("state_warnings"):
            _render_state_warnings(c, layout, compliance["state_warnings"], typo)
        _render_lot_areas(c, layout, compliance, typo)
    else:
        _render_compliance_placeholder(c, layout, typo)


def _render_qr_section(
    c: Canvas,
    layout: LabelLayout,
    brand: dict,
    compliance: dict | None,
    typo: dict,
) -> None:
    zone = layout.qr_zone
    qr_size = min(zone.height * 0.65, zone.width * 0.45)
    quiet = qr_size * 0.12  # preserve quiet zone

    url = (compliance or {}).get("qr_url", f"https://{brand['brand']['website']}")
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    qr_x = zone.x + quiet
    qr_y = zone.y + zone.height - qr_size - quiet
    c.drawImage(ImageReader(buf), qr_x, qr_y, qr_size, qr_size, mask="auto")

    text_x = qr_x + qr_size + quiet * 1.5
    text_y = zone.y + zone.height - typo["compliance_heading"] * 1.2
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["compliance_heading"])
    for line in brand["qr_section"]["heading_lines"]:
        c.drawString(text_x, text_y, line)
        text_y -= typo["compliance_heading"] * 1.25


def _render_barcode_zone(
    c: Canvas,
    layout: LabelLayout,
    compliance: dict | None,
    typo: dict,
) -> None:
    zone = layout.barcode_zone
    c.setStrokeColor(WARM_OFF_WHITE)
    c.setLineWidth(0.5)

    if compliance and compliance.get("verified") and compliance.get("barcode"):
        upc = compliance["barcode"]["upc"]
        _draw_upc_bars(c, zone, upc)
        c.setFillColor(WARM_OFF_WHITE)
        c.setFont("Helvetica", 6)
        c.drawCentredString(zone.center_x, zone.y + 2, upc)
    else:
        c.setFillColor(WARM_OFF_WHITE)
        c.setFont("Helvetica", typo["compliance_body"] - 1)
        c.drawCentredString(
            zone.center_x, zone.center_y,
            "BARCODE ZONE — PROTECTED",
        )
        c.rect(zone.x, zone.y, zone.width, zone.height, fill=0, stroke=1)


def _draw_upc_bars(c: Canvas, zone, upc: str) -> None:
    """Render simplified UPC-A barcode representation."""
    digits = upc.zfill(12)
    bar_h = zone.height * 0.7
    bar_y = zone.y + (zone.height - bar_h) / 2
    total_bars = 95
    bar_w = zone.width / total_bars
    patterns = _upc_patterns(digits)
    x = zone.x
    for bit in patterns:
        if bit == "1":
            c.setFillColor(WARM_OFF_WHITE)
            c.rect(x, bar_y, bar_w, bar_h, fill=1, stroke=0)
        x += bar_w


def _upc_patterns(digits: str) -> str:
    """Generate UPC-A bar pattern from 12-digit code."""
    left_patterns = {
        "0": "0001101", "1": "0011001", "2": "0010011", "3": "0111101",
        "4": "0100011", "5": "0110001", "6": "0101111", "7": "0111011",
        "8": "0110111", "9": "0001011",
    }
    right_patterns = {k: "".join("1" if ch == "0" else "0" for ch in v)
                      for k, v in left_patterns.items()}

    pattern = "101"
    for d in digits[:6]:
        pattern += left_patterns.get(d, "0001101")
    pattern += "01010"
    for d in digits[6:]:
        pattern += right_patterns.get(d, "1110010")
    pattern += "101"
    return pattern


def _render_website(c: Canvas, layout: LabelLayout, brand: dict, typo: dict) -> None:
    zone = layout.qr_zone
    c.setFillColor(CHAMPAGNE_GOLD)
    c.setFont("Helvetica-Bold", typo["compliance_body"])
    c.drawString(zone.x, zone.y + 2, brand["brand"]["website"])


def _render_ingredients(
    c: Canvas,
    layout: LabelLayout,
    compliance: dict,
    typo: dict,
) -> None:
    y = layout.nutrition_zone.y - typo["compliance_body"] * 1.5
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["compliance_body"])
    c.drawString(layout.info_panel.x, y, "Ingredients:")
    y -= typo["compliance_body"] * 1.2
    c.setFont("Helvetica", typo["compliance_body"] - 0.5)
    ingredients = compliance["ingredients"]
    lines = _wrap_text(ingredients, 52)
    for line in lines[:4]:
        c.drawString(layout.info_panel.x, y, line)
        y -= typo["compliance_body"] * 1.1


def _render_active_ingredient(
    c: Canvas,
    layout: LabelLayout,
    brand: dict,
    sku: dict,
    typo: dict,
) -> None:
    y = layout.manufacturing_zone.y + layout.manufacturing_zone.height + 4
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["compliance_body"])
    c.drawString(layout.info_panel.x, y, brand["active_ingredient"]["label"])
    c.setFont("Helvetica", typo["compliance_body"])
    text = f"{brand['active_ingredient']['substance']} — {sku['active_ingredient_amount']}"
    c.drawString(layout.info_panel.x, y - typo["compliance_body"] * 1.2, text)


def _render_manufacturing(
    c: Canvas,
    layout: LabelLayout,
    brand: dict,
    typo: dict,
) -> None:
    mfg = brand["manufacturing"]
    y = layout.manufacturing_zone.y + layout.manufacturing_zone.height
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica", typo["compliance_body"] - 0.5)
    lines = [
        f"Manufactured By: {mfg['manufactured_by']}",
        f"Manufactured For: {mfg['manufactured_for']}",
        *mfg["address"],
    ]
    for line in lines:
        c.drawString(layout.info_panel.x, y, line)
        y -= typo["compliance_body"]


def _render_warning(
    c: Canvas,
    layout: LabelLayout,
    brand: dict,
    typo: dict,
) -> None:
    zone = layout.warning_zone
    y = zone.y + zone.height - typo["compliance_heading"]
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["compliance_heading"])
    c.drawString(zone.x, y, brand["warning_panel"]["heading"])
    y -= typo["compliance_heading"] * 1.3
    c.setFont("Helvetica", typo["compliance_body"] - 0.5)
    for line in brand["warning_panel"]["lines"]:
        c.drawString(zone.x, y, line)
        y -= typo["compliance_body"] * 1.15


def _render_state_warnings(
    c: Canvas,
    layout: LabelLayout,
    warnings: list[str],
    typo: dict,
) -> None:
    y = layout.warning_zone.y + 4
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["compliance_body"] - 0.5)
    for w in warnings[:3]:
        lines = _wrap_text(w, 48)
        for line in lines:
            c.drawString(layout.info_panel.x, y, line)
            y += typo["compliance_body"]


def _render_lot_areas(
    c: Canvas,
    layout: LabelLayout,
    compliance: dict,
    typo: dict,
) -> None:
    y = layout.info_panel.y + 4
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica", typo["compliance_body"] - 1)
    fields = []
    if compliance.get("lot_number"):
        fields.append(f"Lot: {compliance['lot_number']}")
    if compliance.get("batch_number"):
        fields.append(f"Batch: {compliance['batch_number']}")
    if compliance.get("best_by"):
        fields.append(f"Best By: {compliance['best_by']}")
    if fields:
        c.drawString(layout.info_panel.x, y, "  |  ".join(fields))


def _render_compliance_placeholder(c: Canvas, layout: LabelLayout, typo: dict) -> None:
    """Non-production state — compliance data not yet verified."""
    zone = layout.nutrition_zone
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["compliance_heading"])
    c.drawString(zone.x, zone.y + zone.height - 12, "COMPLIANCE DATA REQUIRED")
    c.setFont("Helvetica", typo["compliance_body"])
    msg = (
        "Production labels require verified Proleve-supplied data. "
        "Add JSON to data/compliance/products/ with verified: true."
    )
    for i, line in enumerate(_wrap_text(msg, 42)):
        c.drawString(zone.x, zone.y + zone.height - 28 - i * 10, line)

    _render_active_ingredient(c, layout, {"active_ingredient": {
        "label": "Active Ingredient:",
        "substance": "Hemp-Derived Delta-9 THC",
    }}, {"active_ingredient_amount": "—"}, typo)
    _render_manufacturing(c, layout, _load_brand_minimal(), typo)
    _render_warning(c, layout, _load_brand_minimal(), typo)


def _load_brand_minimal() -> dict:
    from ..config_loader import load_brand
    return load_brand()


def _wrap_text(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        test = " ".join(current + [word])
        if len(test) <= width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines
