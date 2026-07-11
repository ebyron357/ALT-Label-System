"""Master grid — identical structure for every syrup SKU."""

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


@dataclass
class SyrupLayout:
    width: float
    height: float
    bleed_pt: float
    front: Rect
    back: Rect
    safe_front: Rect
    safe_back: Rect
    supplement_zone: Rect
    barcode_zone: Rect
    qr_zone: Rect
    lot_zone: Rect
    warning_zone: Rect
    directions_zone: Rect
    ingredients_zone: Rect
    responsible_zone: Rect


def build_layout() -> SyrupLayout:
    brand = load_brand()
    bleed = mm_to_pt(brand["canvas"]["bleed_mm"])
    panel_w = mm_to_pt(brand["canvas"]["panel_width_mm"])
    panel_h = mm_to_pt(brand["canvas"]["panel_height_mm"])
    safe_inset = mm_to_pt(brand["canvas"]["safe_zone_mm"])

    full_w = 2 * panel_w + 2 * bleed
    full_h = panel_h + 2 * bleed

    front = Rect(bleed, bleed, panel_w, panel_h)
    back = Rect(bleed + panel_w, bleed, panel_w, panel_h)

    safe_front = Rect(
        front.x + safe_inset, front.y + safe_inset,
        front.width - 2 * safe_inset, front.height - 2 * safe_inset,
    )
    safe_back = Rect(
        back.x + safe_inset, back.y + safe_inset,
        back.width - 2 * safe_inset, back.height - 2 * safe_inset,
    )

    supplement_zone = Rect(
        safe_back.x, safe_back.y + safe_back.height * 0.42,
        safe_back.width * 0.48, safe_back.height * 0.38,
    )
    directions_zone = Rect(
        safe_back.x, safe_back.y + safe_back.height * 0.72,
        safe_back.width, safe_back.height * 0.26,
    )
    ingredients_zone = Rect(
        safe_back.x + safe_back.width * 0.50, safe_back.y + safe_back.height * 0.42,
        safe_back.width * 0.50, safe_back.height * 0.28,
    )
    warning_zone = Rect(
        safe_back.x, safe_back.y + safe_back.height * 0.08,
        safe_back.width, safe_back.height * 0.32,
    )
    responsible_zone = Rect(
        safe_back.x, safe_back.y + safe_back.height * 0.80,
        safe_back.width * 0.55, safe_back.height * 0.18,
    )
    qr_zone = Rect(
        safe_back.x, safe_back.y,
        safe_back.width * 0.42, safe_back.height * 0.10,
    )
    barcode_zone = Rect(
        safe_back.x + safe_back.width * 0.55, safe_back.y,
        safe_back.width * 0.45, safe_back.height * 0.10,
    )
    lot_zone = Rect(
        safe_back.x, safe_back.y + safe_back.height * 0.94,
        safe_back.width, safe_back.height * 0.06,
    )

    return SyrupLayout(
        width=full_w,
        height=full_h,
        bleed_pt=bleed,
        front=front,
        back=back,
        safe_front=safe_front,
        safe_back=safe_back,
        supplement_zone=supplement_zone,
        barcode_zone=barcode_zone,
        qr_zone=qr_zone,
        lot_zone=lot_zone,
        warning_zone=warning_zone,
        directions_zone=directions_zone,
        ingredients_zone=ingredients_zone,
        responsible_zone=responsible_zone,
    )
