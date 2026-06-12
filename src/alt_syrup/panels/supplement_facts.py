"""Supplement Facts — vector panel, no raster typography."""

from reportlab.pdfgen.canvas import Canvas

from ..colors import MATTE_BLACK, WARM_OFF_WHITE
from ..layout import Rect


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

    c.setFillColor(WARM_OFF_WHITE)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(MATTE_BLACK)

    ty = y + h - heading - 2
    c.setFont("Helvetica-Bold", heading + 0.5)
    c.drawString(x + 3, ty, "Supplement Facts")

    c.setLineWidth(2)
    c.line(x + 3, ty - 3, x + w - 3, ty - 3)

    ty -= heading + 1
    c.setFont("Helvetica", body)
    c.drawString(x + 3, ty, f"Serving Size {supplement['serving_size']}")
    ty -= body * 1.15
    c.drawString(x + 3, ty, f"Servings Per Container {supplement['servings_per_container']}")

    c.setLineWidth(3)
    c.line(x + 3, ty - 3, x + w - 3, ty - 3)
    ty -= body + 3

    c.setFont("Helvetica-Bold", body)
    c.drawString(x + 3, ty, "Amount Per Serving")
    ty -= body * 1.2

    c.setFont("Helvetica", body)
    ingredient = supplement["active_ingredient"]
    amount = supplement["amount_per_serving"]
    c.drawString(x + 3, ty, f"{ingredient}")
    c.drawRightString(x + w - 3, ty, amount)
    ty -= body * 1.1

    for other in supplement.get("other_ingredients", []):
        c.drawString(x + 3, ty, other["name"])
        c.drawRightString(x + w - 3, ty, other.get("amount", ""))
        ty -= body * 1.05

    c.setLineWidth(1)
    c.line(x + 3, y + 10, x + w - 3, y + 10)
    c.setFont("Helvetica", max(body - 0.5, 5.0))
    c.drawString(x + 3, y + 2, "† Daily Value not established.")
