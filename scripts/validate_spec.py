#!/usr/bin/env python3
"""Validate ALTERNATIVE™ label system against Production Master v1 spec."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alt_label.config_loader import load_brand, load_flavors, load_skus, mm_to_pt


def main() -> int:
    brand = load_brand()
    skus = load_skus()
    flavors = load_flavors()
    checks: list[tuple[str, bool, str]] = []

    # Canvas
    w = brand["canvas"]["width_mm"]
    h = brand["canvas"]["height_mm"]
    checks.append(("Canvas width 182.22mm", abs(w - 182.22) < 0.01, f"got {w}"))
    checks.append(("Canvas height 148mm", abs(h - 148.0) < 0.01, f"got {h}"))
    checks.append(("300 DPI spec documented", brand["canvas"]["dpi"] == 300, ""))

    # SKU lock
    expected = {5: "SESSION™", 10: "SOCIAL™", 50: "RESERVE™", 100: "RESERVE™"}
    for sku in skus:
        mg = sku["thc_mg"]
        checks.append((
            f"SKU {mg}mg naming",
            sku["name"] == expected[mg],
            sku["name"],
        ))
    checks.append(("Exactly 4 SKUs", len(skus) == 4, str(len(skus))))

    # Flavors
    flavor_names = {f["name"] for f in flavors}
    checks.append((
        "LYCHEE SWEET TEA flavor",
        "LYCHEE SWEET TEA" in flavor_names,
        "",
    ))
    checks.append((
        "PASSION FRUIT flavor",
        "PASSION FRUIT" in flavor_names,
        "",
    ))

    # Brand copy
    checks.append((
        "Tagline",
        brand["brand"]["tagline"] == "A NEW STATE OF MIND",
        brand["brand"]["tagline"],
    ))
    checks.append((
        "Website",
        brand["brand"]["website"] == "AlternativeBev.com",
        "",
    ))
    checks.append((
        "Manufactured By Proleve",
        brand["manufacturing"]["manufactured_by"] == "Proleve Brands",
        "",
    ))
    checks.append((
        "Manufactured For Invictus (not as manufacturer)",
        brand["manufacturing"]["manufactured_for"] == "Invictus Wellness LLC",
        "",
    ))

    # QR copy
    qr = brand["qr_section"]["heading_lines"]
    checks.append((
        "QR section copy",
        qr == ["SCAN FOR", "LAB RESULTS", "INGREDIENTS", "PRODUCT INFO"],
        str(qr),
    ))

    # Typography hierarchy
    typo = brand["typography"]
    checks.append((
        "A symbol reduced",
        typo.get("a_symbol_scale", 1) < 1,
        str(typo.get("a_symbol_scale")),
    ))
    checks.append((
        "Brand name increased",
        typo.get("brand_name_scale", 1) > 1,
        str(typo.get("brand_name_scale")),
    ))
    checks.append((
        "Flavor size increased",
        typo.get("flavor_scale", 1) > 1,
        str(typo.get("flavor_scale")),
    ))

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    score = round((passed / total) * 10, 1)

    print("ALTERNATIVE™ Production Master v1 — Spec Validation")
    print("=" * 55)
    for name, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        extra = f" ({detail})" if detail and not ok else ""
        print(f"  [{status}] {name}{extra}")

    print("=" * 55)
    print(f"Score: {passed}/{total} checks — Retail readiness index: {score}/10")

    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
