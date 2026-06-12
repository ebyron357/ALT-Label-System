"""Supplement Facts — vector panel, aligned dividers."""

from reportlab.pdfgen.canvas import Canvas

from ..colors import MATTE_BLACK, WARM_OFF_WHITE
from ..layout import Rect

_PAD = 4


def render_supplement_facts(
    c: Canvas,
    zone: Rect,
    supplement: dict,
    typo: dict,
) -> None:
    """FDA Supplement Facts format — vector lines and text only."""
    x, y, w, h = zone.x, zone.y, zone.width, zone.height
    body = max(typo.get("supplement_body", 5.5), 5.5)
    heading = typo.get("supplement_heading", 6.0)
    inner_l = x + _PAD
    inner_r = x + w - _PAD

    c.setFillColor(WARM_OFF_WHITE)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(MATTE_BLACK)
    c.setStrokeColor(MATTE_BLACK)

    ty = y + h - heading - 2
    c.setFont("Helvetica-Bold", heading + 0.5)
    c.drawString(inner_l, ty, "Supplement Facts")

    c.setLineWidth(1.5)
    c.line(inner_l, ty - 3, inner_r, ty - 3)

    ty -= heading + 1
    c.setFont("Helvetica", body)
    c.drawString(inner_l, ty, f"Serving Size {supplement['serving_size']}")
    ty -= body * 1.12
    c.drawString(inner_l, ty, f"Servings Per Container {supplement['servings_per_container']}")

    c.setLineWidth(2.5)
    c.line(inner_l, ty - 3, inner_r, ty - 3)
    ty -= body + 3

    c.setFont("Helvetica-Bold", body)
    c.drawString(inner_l, ty, "Amount Per Serving")
    ty -= body * 1.15

    c.setFont("Helvetica", body)
    ingredient = supplement["active_ingredient"]
    amount = supplement["amount_per_serving"]
    c.drawString(inner_l, ty, f"{ingredient}")
    c.drawRightString(inner_r, ty, amount)
    ty -= body * 1.08

    for other in supplement.get("other_ingredients", []):
        c.drawString(inner_l, ty, other["name"])
        c.drawRightString(inner_r, ty, other.get("amount", ""))
        ty -= body * 1.04

    c.setLineWidth(0.75)
    c.line(inner_l, y + 12, inner_r, y + 12)
    c.setFont("Helvetica", max(body - 0.5, 5.0))
    c.drawString(inner_l, y + 3, "† Daily Value not established.")
