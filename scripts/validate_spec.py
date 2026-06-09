#!/usr/bin/env python3
"""Validate ALTERNATIVE™ label system — Retail Master Lock v1.0."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alt_label.compliance_loader import load_compliance
from alt_label.config_loader import load_brand, load_flavors, load_skus


def main() -> int:
    brand = load_brand()
    skus = load_skus()
    flavors = load_flavors()
    checks: list[tuple[str, bool, str]] = []

    w = brand["canvas"]["width_mm"]
    h = brand["canvas"]["height_mm"]
    checks.append(("Canvas 182.22mm × 148mm", abs(w - 182.22) < 0.01 and abs(h - 148.0) < 0.01, ""))
    checks.append(("300 DPI documented", brand["canvas"]["dpi"] == 300, ""))

    expected = {5: "SESSION™", 10: "SOCIAL™", 50: "RESERVE™", 100: "RESERVE™"}
    thc_lines = {
        5: "5MG HEMP-DERIVED THC PER CAN",
        10: "10MG HEMP-DERIVED THC PER CAN",
        50: "50MG HEMP-DERIVED THC PER CAN",
        100: "100MG HEMP-DERIVED THC PER CAN",
    }
    for sku in skus:
        mg = sku["thc_mg"]
        checks.append((f"SKU {mg}mg", sku["name"] == expected[mg], sku["name"]))
        checks.append((f"THC line {mg}mg", sku.get("thc_line") == thc_lines[mg], sku.get("thc_line", "")))

    checks.append(("No 20MG SKU", not any(s["thc_mg"] == 20 for s in skus), ""))
    checks.append(("Exactly 4 SKUs", len(skus) == 4, str(len(skus))))

    flavor_names = {f["name"] for f in flavors}
    checks.append(("LYCHEE SWEET TEA", "LYCHEE SWEET TEA" in flavor_names, ""))
    checks.append(("PASSION FRUIT", "PASSION FRUIT" in flavor_names, ""))

    checks.append(("Manufactured By Proleve", brand["manufacturing"]["manufactured_by"] == "Proleve", ""))
    checks.append(("Invictus as Manufactured For only", brand["manufacturing"]["manufactured_for"] == "Invictus Wellness LLC", ""))
    checks.append(("Address includes USA", "USA" in brand["manufacturing"]["address_lines"][-1], ""))

    checks.append(("Website AlternativeBev.com", brand["brand"]["website"] == "AlternativeBev.com", ""))
    checks.append(("QR copy", brand["qr_section"]["heading_lines"] == [
        "SCAN FOR", "LAB RESULTS", "INGREDIENTS", "PRODUCT INFO"
    ], ""))
    checks.append(("Active Ingredient label", brand["active_ingredient"]["label"] == "Active Ingredient", ""))
    checks.append(("Warning pregnancy copy", any(
        "while pregnant" in line for line in brand["warning_panel"]["lines"]
    ), ""))

    typo = brand["typography"]
    checks.append(("A symbol reduced 10%", abs(typo.get("a_symbol_scale", 1) - 0.90) < 0.01, ""))
    checks.append(("Brand name increased", typo.get("brand_name_scale", 1) >= 1.20, ""))
    checks.append(("Flavor increased 35%", typo.get("flavor_scale", 1) >= 1.35, ""))

    for flavor in flavors:
        for sku in skus:
            data = load_compliance(sku["id"], flavor["id"])
            ok = data is not None and data.get("verified")
            checks.append((
                f"Compliance {sku['id']}/{flavor['id']}",
                ok,
                "missing" if not ok else "",
            ))
            if data:
                cal = data["nutrition_facts"]["calories"]
                if flavor["id"] == "passion_fruit":
                    checks.append(("Passion Fruit calories 0", cal == "0", cal))
                if flavor["id"] == "lychee_sweet_tea":
                    checks.append(("Lychee calories 20", cal == "20", cal))

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    score = round((passed / total) * 10, 1)

    print("ALTERNATIVE™ Retail Master Lock v1.0 — Validation")
    print("=" * 55)
    for name, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        extra = f" ({detail})" if detail and not ok else ""
        print(f"  [{status}] {name}{extra}")
    print("=" * 55)
    print(f"Score: {passed}/{total} — Retail readiness: {score}/10")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
