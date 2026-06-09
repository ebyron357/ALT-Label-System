"""Back panel — standardized compliance sections, no filler."""

import io

import qrcode
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from ..colors import MATTE_BLACK, WARM_OFF_WHITE
from ..layout import SyrupLayout
from .supplement_facts import render_supplement_facts


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
    qr_size = min(zone.height * 0.85, zone.width * 0.55)
    quiet = qr_size * brand["qr_section"].get("quiet_zone_ratio", 0.12)
    url = compliance.get("qr_url", f"https://{brand['brand']['website']}")
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    c.drawImage(ImageReader(buf), zone.x + quiet, zone.y + quiet, qr_size, qr_size, mask="auto")
    tx = zone.x + quiet + qr_size + quiet
    ty = zone.y + zone.height - typo["panel_heading"]
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["panel_heading"] - 1)
    for line in brand["qr_section"]["heading_lines"]:
        c.drawString(tx, ty, line)
        ty -= typo["panel_heading"]
    c.setFont("Helvetica", typo["panel_body"] - 0.5)
    c.drawString(zone.x, zone.y, brand["brand"]["website"])


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
    c.setFont("Helvetica", 5)
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
    y = zone.y + zone.height - typo["panel_heading"]
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["panel_heading"])
    c.drawString(zone.x, y, brand["directions"]["heading"])
    y -= typo["panel_heading"] * 1.2
    c.setFont("Helvetica", typo["panel_body"] - 0.5)
    for line in brand["directions"]["lines"]:
        c.drawString(zone.x, y, line)
        y -= typo["panel_body"] * 1.1


def _render_ingredients(c: Canvas, layout: SyrupLayout, compliance: dict, typo: dict) -> None:
    zone = layout.ingredients_zone
    y = zone.y + zone.height - typo["panel_heading"]
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["panel_heading"])
    c.drawString(zone.x, y, "INGREDIENTS:")
    y -= typo["panel_heading"] * 1.1
    c.setFont("Helvetica", typo["panel_body"] - 0.5)
    for line in compliance.get("ingredients_lines", []):
        c.drawString(zone.x, y, line)
        y -= typo["panel_body"] * 1.05


def _render_warnings(c: Canvas, layout: SyrupLayout, brand: dict, compliance: dict, typo: dict) -> None:
    zone = layout.warning_zone
    y = zone.y + zone.height - typo["panel_heading"]
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica-Bold", typo["panel_heading"])
    c.drawString(zone.x, y, brand["warning_panel"]["heading"])
    y -= typo["panel_heading"] * 1.2
    c.setFont("Helvetica", typo["panel_body"] - 0.6)
    for line in brand["warning_panel"]["lines"]:
        c.drawString(zone.x, y, line)
        y -= typo["panel_body"] * 1.05
    for sw in compliance.get("state_warnings", [])[:2]:
        for part in _wrap(sw, 38):
            c.drawString(zone.x, y, part)
            y -= typo["panel_body"]


def _render_responsible_party(c: Canvas, layout: SyrupLayout, brand: dict, typo: dict) -> None:
    zone = layout.responsible_zone
    rp = brand["responsible_party"]
    y = zone.y + zone.height - typo["panel_body"]
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica", typo["panel_body"] - 0.6)
    for line in [
        rp["manufactured_by_label"], rp["manufactured_by"],
        rp["manufactured_for_label"], rp["manufactured_for"],
        *rp["address_lines"],
    ]:
        c.drawString(zone.x, y, line)
        y -= typo["panel_body"] * 0.95


def _render_lot(c: Canvas, layout: SyrupLayout, compliance: dict, typo: dict) -> None:
    zone = layout.lot_zone
    c.setFillColor(WARM_OFF_WHITE)
    c.setFont("Helvetica", typo["panel_body"] - 1)
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
