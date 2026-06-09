"""FDA Nutrition Facts panel renderer."""

from reportlab.pdfgen.canvas import Canvas

from ..colors import MATTE_BLACK, WARM_OFF_WHITE
from ..layout import Rect


def render_nutrition_facts(
    c: Canvas,
    zone: Rect,
    nutrition: dict,
    typo: dict,
) -> None:
    """Render standard Nutrition Facts box from Proleve-supplied data."""
    x, y, w, h = zone.x, zone.y, zone.width, zone.height
    body = typo["compliance_body"] - 0.5
    heading = typo["compliance_heading"]

    # White panel on black background
    c.setFillColor(WARM_OFF_WHITE)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(MATTE_BLACK)

    ty = y + h - heading - 2
    c.setFont("Helvetica-Black", heading + 1)
    c.drawString(x + 4, ty, "Nutrition Facts")

    c.setLineWidth(2)
    c.line(x + 4, ty - 4, x + w - 4, ty - 4)

    ty -= heading + 2
    c.setFont("Helvetica", body)
    c.drawString(x + 4, ty, f"Serving Size {nutrition['serving_size']}")
    ty -= body * 1.2
    c.drawString(x + 4, ty, f"Servings Per Container {nutrition['servings_per_container']}")

    c.setLineWidth(4)
    c.line(x + 4, ty - 4, x + w - 4, ty - 4)
    ty -= body + 4

    c.setFont("Helvetica-Bold", body + 1)
    c.drawString(x + 4, ty, f"Calories {nutrition['calories']}")
    ty -= body * 1.5

    c.setLineWidth(1)
    c.line(x + 4, ty, x + w - 4, ty)
    ty -= body * 1.2

    c.setFont("Helvetica-Bold", body - 0.5)
    c.drawString(x + 4, ty, "Amount Per Serving")
    dv_x = x + w - 50
    c.drawString(dv_x, ty, "% Daily Value*")
    ty -= body * 1.1

    c.setFont("Helvetica", body - 0.5)
    for nutrient in nutrition.get("nutrients", []):
        name = nutrient["name"]
        amount = nutrient["amount"]
        dv = nutrient.get("daily_value") or ""
        line = f"{name} {amount}"
        c.drawString(x + 4, ty, line)
        if dv:
            c.drawRightString(x + w - 4, ty, dv)
        ty -= body * 1.05
        if ty < y + 8:
            break

    c.setLineWidth(1)
    c.line(x + 4, y + 14, x + w - 4, y + 14)
    c.setFont("Helvetica", body - 1.5)
    c.drawString(x + 4, y + 4, "* Percent Daily Values based on a 2,000 calorie diet.")
