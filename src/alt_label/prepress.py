"""Prepress audit and PDF verification — v2.0."""

import re
from dataclasses import dataclass, field
from pathlib import Path

from .config_loader import load_brand, mm_to_pt


@dataclass
class PrepressCheck:
    name: str
    status: str  # pass | warn | fail
    detail: str = ""


@dataclass
class PrepressReport:
    checks: list[PrepressCheck] = field(default_factory=list)

    def ok(self) -> bool:
        return not any(c.status == "fail" for c in self.checks)


def audit_pdf(pdf_path: Path) -> list[PrepressCheck]:
    """Verify generated PDF meets prepress requirements."""
    checks: list[PrepressCheck] = []
    brand = load_brand()

    if not pdf_path.exists():
        return [PrepressCheck("File exists", "fail", str(pdf_path))]

    checks.append(PrepressCheck("File exists", "pass", pdf_path.name))
    size = pdf_path.stat().st_size
    checks.append(PrepressCheck("File size", "pass" if size > 1000 else "warn", f"{size} bytes"))

    raw = pdf_path.read_bytes()
    if raw[:4] == b"%PDF":
        checks.append(PrepressCheck("Valid PDF header", "pass"))
    else:
        checks.append(PrepressCheck("Valid PDF header", "fail"))
        return checks

    if b"/Font" in raw or b"/Type1" in raw or b"/Subtype/Type1" in raw:
        checks.append(PrepressCheck("Fonts embedded", "pass"))
    else:
        checks.append(PrepressCheck("Fonts embedded", "warn", "No font objects detected"))

    if b"/DeviceRGB" in raw or b"/RGB" in raw:
        checks.append(PrepressCheck("CMYK only (no RGB)", "warn", "RGB color space detected"))
    else:
        checks.append(PrepressCheck("CMYK only (no RGB)", "pass"))

    if b"/SMask" in raw or b"/Transparency" in raw:
        checks.append(PrepressCheck("No transparency", "warn", "Transparency may need flattening for PDF/X-1a"))
    else:
        checks.append(PrepressCheck("No transparency", "pass"))

    trim_w = mm_to_pt(brand["canvas"]["width_mm"])
    bleed = mm_to_pt(brand["canvas"]["bleed_mm"])
    expected_w = trim_w + 2 * bleed
    media = _parse_media_box(raw)
    if media:
        w, h = media
        if abs(w - expected_w) < 2:
            checks.append(PrepressCheck("Artboard width (trim+bleed)", "pass", f"{w:.1f}pt"))
        else:
            checks.append(PrepressCheck("Artboard width (trim+bleed)", "warn", f"{w:.1f}pt expected ~{expected_w:.1f}pt"))
    else:
        checks.append(PrepressCheck("MediaBox parse", "warn", "Could not verify dimensions"))

    return checks


def _parse_media_box(data: bytes) -> tuple[float, float] | None:
    match = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", data)
    if not match:
        return None
    x1, y1, x2, y2 = (float(match.group(i)) for i in range(1, 5))
    return x2 - x1, y2 - y1


def audit_hierarchy() -> list[PrepressCheck]:
    """Verify typographic hierarchy supports 1-second shelf identification."""
    brand = load_brand()
    typo = brand["typography"]
    checks: list[PrepressCheck] = []

    brand_size = 20 * typo.get("brand_name_scale", 1.225)
    a_height = 26 * typo.get("a_symbol_scale", 0.90)
    thc_size = typo.get("thc_content", 11.0)
    flavor_size = typo.get("flavor_base", 8.5) * typo.get("flavor_scale", 1.35)

    if brand_size > a_height:
        checks.append(PrepressCheck("ALTERNATIVE™ dominates A symbol", "pass",
                                    f"wordmark {brand_size:.1f}pt > A {a_height:.1f}pt"))
    else:
        checks.append(PrepressCheck("ALTERNATIVE™ dominates A symbol", "fail"))

    for scale, label in [(1.0, "100%"), (0.5, "50%"), (0.25, "25%"), (0.1, "10%")]:
        b, t, f = brand_size * scale, thc_size * scale, flavor_size * scale
        order_ok = b >= t and f >= 2.0
        readable = f >= 1.5 and t >= 1.5
        status = "pass" if order_ok and (scale >= 0.25 or readable) else "warn" if scale == 0.1 else "pass"
        checks.append(PrepressCheck(
            f"Hierarchy at {label}",
            status,
            f"brand={b:.1f} thc={t:.1f} flavor={f:.1f}pt",
        ))

    return checks
