"""Label layout — trim + bleed zones for 12oz sleek can."""

from dataclasses import dataclass

from .config_loader import load_brand, mm_to_pt


@dataclass
class Rect:
    x: float
    y: float
    width: float
    height: float

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2


@dataclass
class LabelLayout:
    """Full artboard including bleed; trim_box is the finished label size."""
    width: float
    height: float
    bleed_pt: float
    trim_box: Rect
    safe: Rect
    front_panel: Rect
    info_panel: Rect
    barcode_zone: Rect
    qr_zone: Rect
    warning_zone: Rect
    nutrition_zone: Rect
    manufacturing_zone: Rect
    lot_zone: Rect


def build_layout() -> LabelLayout:
    brand = load_brand()
    trim_w = mm_to_pt(brand["canvas"]["width_mm"])
    trim_h = mm_to_pt(brand["canvas"]["height_mm"])
    bleed_pt = mm_to_pt(brand["canvas"]["bleed_mm"])
    safe_inset = mm_to_pt(brand["canvas"]["safe_zone_mm"])

    full_w = trim_w + 2 * bleed_pt
    full_h = trim_h + 2 * bleed_pt
    trim_box = Rect(bleed_pt, bleed_pt, trim_w, trim_h)

    safe = Rect(
        trim_box.x + safe_inset,
        trim_box.y + safe_inset,
        trim_w - 2 * safe_inset,
        trim_h - 2 * safe_inset,
    )

    front_w = safe.width * 0.42
    front_panel = Rect(safe.x, safe.y, front_w, safe.height)

    info_x = safe.x + front_w + mm_to_pt(2)
    info_w = safe.x + safe.width - info_x
    info_panel = Rect(info_x, safe.y, info_w, safe.height)

    barcode_zone = Rect(
        info_panel.x + info_panel.width * 0.55,
        safe.y + safe.height * 0.02,
        info_panel.width * 0.42,
        safe.height * 0.14,
    )
    qr_zone = Rect(
        info_panel.x,
        safe.y + safe.height * 0.02,
        info_panel.width * 0.48,
        safe.height * 0.22,
    )
    warning_zone = Rect(
        info_panel.x,
        safe.y + safe.height * 0.58,
        info_panel.width,
        safe.height * 0.38,
    )
    nutrition_zone = Rect(
        info_panel.x,
        safe.y + safe.height * 0.26,
        info_panel.width * 0.52,
        safe.height * 0.30,
    )
    manufacturing_zone = Rect(
        info_panel.x,
        safe.y + safe.height * 0.50,
        info_panel.width * 0.55,
        safe.height * 0.08,
    )
    lot_zone = Rect(
        info_panel.x,
        safe.y - safe_inset + 2,
        info_panel.width,
        mm_to_pt(6),
    )

    return LabelLayout(
        width=full_w,
        height=full_h,
        bleed_pt=bleed_pt,
        trim_box=trim_box,
        safe=safe,
        front_panel=front_panel,
        info_panel=info_panel,
        barcode_zone=barcode_zone,
        qr_zone=qr_zone,
        warning_zone=warning_zone,
        nutrition_zone=nutrition_zone,
        manufacturing_zone=manufacturing_zone,
        lot_zone=lot_zone,
    )
