"""Back panel — standardized compliance sections, no filler."""

import io

import qrcode
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from ..colors import MATTE_BLACK, WARM_OFF_WHITE
from ..layout import SyrupLayout
from .supplement_facts import render_supplement_facts


def _body_size(typo: dict) -> float:
    return max(typo.get("panel_body", 6.0), 6.0)


def _lot_size(typo: dict) -> float:
    return max(typo.get("panel_body", 6.0) - 0.5, 5.5)


def render_back_panel(
    c: Canvas,
    layout: SyrupLayout,
    brand: dict,
    compliance: dict,
    typo: dict,
) -> None:
    panel = layout.back
    c.setFillColor(MATTE_BLACK)
    c.rect(panel.x, panel.y, panel.width, panel.height, fill=1, stroke=0)

    _render_qr(c, layout, brand, compliance, typo)
    _render_barcode(c, layout, compliance)
    _render_directions(c, layout, brand, typo)
    _render_ingredients(c, layout, compliance, typo)
    render_supplement_facts(c, layout.supplement_zone, compliance["supplement_facts"], typo)
    _render_warnings(c, layout, brand, compliance, typo)
    _render_responsible_party(c, layout, brand, typo)
    _render_lot(c, layout, compliance, typo)


def _render_qr(c: Canvas, layout: SyrupLayout, brand: dict, compliance: dict, typo: dict) -> None:
    zone = layout.qr_zone
    body = _body_size(typo)
    website_band = body * 1.6
    content_h = zone.height - website_band
    quiet_ratio = brand["qr_section"].get("quiet_zone_ratio", 0.12)
    qr_size = min(content_h * 0.82, zone.width * 0.44)
    quiet = qr_size * quiet_ratio
    qr_x = zone.x + quiet
    qr_y = zone.y + website_band + max((content_h - qr_size) / 2, quiet)

    url = compliance.get("qr_url", f"https://{brand['brand']['website']}")
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    c.drawImage(ImageReader(buf), qr_x, qr_y, qr_size, qr_size, mask="auto")

    tx = qr_x + qr_size + quiet
    ty = zone.y + zone.height - website_band - 2
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["panel_heading"] - 0.5)
    for line in brand["qr_section"]["heading_lines"]:
        c.drawString(tx, ty, line)
        ty -= typo["panel_heading"] * 0.95

    c.setFont("Helvetica", body)
    c.drawString(zone.x, zone.y + 1, brand["brand"]["website"])


def _render_barcode(c: Canvas, layout: SyrupLayout, compliance: dict) -> None:
    zone = layout.barcode_zone
    upc = compliance.get("barcode", {}).get("upc")
    if not upc:
        return
    bar_h = zone.height * 0.65
    bar_y = zone.y + (zone.height - bar_h) / 2
    bar_w = zone.width / 95
    pattern = _upc_pattern(upc.zfill(12))
    x = zone.x
    for bit in pattern:
        if bit == "1":
            c.setFillColor(WARM_OFF_WHITE)
            c.rect(x, bar_y, bar_w, bar_h, fill=1, stroke=0)
        x += bar_w
    c.setFont("Helvetica", 5.5)
    c.drawCentredString(zone.x + zone.width / 2, zone.y + 1, upc)


def _upc_pattern(digits: str) -> str:
    left = {
        "0": "0001101", "1": "0011001", "2": "0010011", "3": "0111101",
        "4": "0100011", "5": "0110001", "6": "0101111", "7": "0111011",
        "8": "0110111", "9": "0001011",
    }
    right = {k: "".join("1" if ch == "0" else "0" for ch in v) for k, v in left.items()}
    p = "101" + "".join(left[d] for d in digits[:6]) + "01010" + "".join(right[d] for d in digits[6:]) + "101"
    return p


def _render_directions(c: Canvas, layout: SyrupLayout, brand: dict, typo: dict) -> None:
    zone = layout.directions_zone
    body = _body_size(typo)
    y = zone.y + zone.height - typo["panel_heading"]
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["panel_heading"])
    c.drawString(zone.x, y, brand["directions"]["heading"])
    y -= typo["panel_heading"] * 1.15
    c.setFont("Helvetica", body)
    for line in brand["directions"]["lines"]:
        c.drawString(zone.x, y, line)
        y -= body * 1.05


def _render_ingredients(c: Canvas, layout: SyrupLayout, compliance: dict, typo: dict) -> None:
    zone = layout.ingredients_zone
    body = _body_size(typo)
    y = zone.y + zone.height - typo["panel_heading"]
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["panel_heading"])
    c.drawString(zone.x, y, "INGREDIENTS:")
    y -= typo["panel_heading"] * 1.05
    c.setFont("Helvetica", body)
    text = compliance.get("ingredients", "")
    if not text:
        text = ", ".join(compliance.get("ingredients_lines", []))
    for line in _wrap_to_width(c, text, "Helvetica", body, zone.width - 2):
        c.drawString(zone.x, y, line)
        y -= body * 1.08


def _render_warnings(c: Canvas, layout: SyrupLayout, brand: dict, compliance: dict, typo: dict) -> None:
    zone = layout.warning_zone
    body = _body_size(typo)
    y = zone.y + zone.height - typo["panel_heading"]
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["panel_heading"])
    c.drawString(zone.x, y, brand["warning_panel"]["heading"])
    y -= typo["panel_heading"] * 1.1
    c.setFont("Helvetica", body)
    for line in brand["warning_panel"]["lines"]:
        c.drawString(zone.x, y, line)
        y -= body * 1.02
    for sw in compliance.get("state_warnings", [])[:2]:
        for part in _wrap(sw, 36):
            c.drawString(zone.x, y, part)
            y -= body * 1.02


def _render_responsible_party(c: Canvas, layout: SyrupLayout, brand: dict, typo: dict) -> None:
    zone = layout.responsible_zone
    body = _body_size(typo)
    rp = brand["responsible_party"]
    y = zone.y + zone.height - body
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica", body)
    for line in [
        rp["manufactured_by_label"], rp["manufactured_by"],
        rp["manufactured_for_label"], rp["manufactured_for"],
        *rp["address_lines"],
    ]:
        c.drawString(zone.x, y, line)
        y -= body * 0.92


def _render_lot(c: Canvas, layout: SyrupLayout, compliance: dict, typo: dict) -> None:
    zone = layout.lot_zone
    size = _lot_size(typo)
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica", size)
    lot = compliance.get("lot_number", "")
    best = compliance.get("best_by", "")
    c.drawString(zone.x, zone.y + 2, f"Lot: {lot}" if lot else "Lot:")
    c.drawString(zone.x + 80, zone.y + 2, f"Best By: {best}" if best else "Best By:")


def _wrap(text: str, width: int) -> list[str]:
    words, lines, cur = text.split(), [], []
    for w in words:
        test = " ".join(cur + [w])
        if len(test) <= width:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def _wrap_to_width(c: Canvas, text: str, font: str, size: float, max_width: float) -> list[str]:
    words, lines, cur = text.split(), [], []
    for word in words:
        test = " ".join(cur + [word]) if cur else word
        if c.stringWidth(test, font, size) <= max_width:
            cur.append(word)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [word]
    if cur:
        lines.append(" ".join(cur))
    return lines
