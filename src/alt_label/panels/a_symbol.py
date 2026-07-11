"""Geometric hero A mark — vector rendering, no external graphics."""

from reportlab.pdfgen.canvas import Canvas


def draw_a_symbol(c: Canvas, cx: float, top_y: float, height: float, color) -> float:
    """
    Draw refined geometric A mark centered at cx.
    Returns bottom y coordinate after drawing.
    """
    w = height * 0.83
    left = cx - w / 2
    bottom = top_y - height

    c.setFillColor(color)
    c.setStrokeColor(color)

    # Outer A shape
    path = c.beginPath()
    path.moveTo(cx, top_y)
    path.lineTo(left + w, bottom)
    path.lineTo(left + w * 0.78, bottom)
    path.lineTo(left + w * 0.58, bottom + height * 0.35)
    path.lineTo(left + w * 0.42, bottom + height * 0.35)
    path.lineTo(left + w * 0.22, bottom)
    path.lineTo(left, bottom)
    path.close()
    c.drawPath(path, fill=1, stroke=0)

    # Inner counter — negative space cutout
    from ..colors import MATTE_BLACK

    inner_w = w * 0.28
    inner_h = height * 0.18
    inner_y = bottom + height * 0.32
    c.setFillColor(MATTE_BLACK)
    path2 = c.beginPath()
    path2.moveTo(cx, inner_y + inner_h)
    path2.lineTo(cx - inner_w / 2, inner_y)
    path2.lineTo(cx + inner_w / 2, inner_y)
    path2.close()
    c.drawPath(path2, fill=1, stroke=0)

    return bottom - 8
