"""Label layout zones for 12oz sleek can — 182.22mm × 148mm."""

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
    width: float
    height: float
    safe: Rect
    front_panel: Rect
    info_panel: Rect
    barcode_zone: Rect
    qr_zone: Rect
    warning_zone: Rect
    nutrition_zone: Rect
    manufacturing_zone: Rect


def build_layout() -> LabelLayout:
    brand = load_brand()
    w = mm_to_pt(brand["canvas"]["width_mm"])
    h = mm_to_pt(brand["canvas"]["height_mm"])
    safe_inset = mm_to_pt(brand["canvas"]["safe_zone_mm"])

    safe = Rect(safe_inset, safe_inset, w - 2 * safe_inset, h - 2 * safe_inset)

    # Front hero panel — left 42% of safe area
    front_w = safe.width * 0.42
    front_panel = Rect(safe.x, safe.y, front_w, safe.height)

    # Information / compliance panel — right 58%
    info_x = safe.x + front_w + mm_to_pt(2)
    info_w = safe.x + safe.width - info_x
    info_panel = Rect(info_x, safe.y, info_w, safe.height)

    # Protected zones per spec
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

    return LabelLayout(
        width=w,
        height=h,
        safe=safe,
        front_panel=front_panel,
        info_panel=info_panel,
        barcode_zone=barcode_zone,
        qr_zone=qr_zone,
        warning_zone=warning_zone,
        nutrition_zone=nutrition_zone,
        manufacturing_zone=manufacturing_zone,
    )
