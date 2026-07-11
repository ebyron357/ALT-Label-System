#!/usr/bin/env python3
"""Validate ALTERNATIVE™ — Final Prepress + Retail Master Lock v2.0."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alt_label.compliance_audit import run_full_audit
from alt_label.compliance_loader import load_compliance
from alt_label.config_loader import load_brand, load_flavors, load_skus
from alt_label.prepress import audit_hierarchy


def main() -> int:
    brand = load_brand()
    skus = load_skus()
    flavors = load_flavors()
    checks: list[tuple[str, bool, str]] = []

    checks.append(("Version 2.0", brand.get("version") == "2.0", brand.get("version", "")))

    w, h = brand["canvas"]["width_mm"], brand["canvas"]["height_mm"]
    checks.append(("Trim 182.22mm × 148mm", abs(w - 182.22) < 0.01 and abs(h - 148.0) < 0.01, ""))
    checks.append(("Bleed defined", brand["canvas"].get("bleed_mm", 0) >= 3.0, ""))
    checks.append(("300 DPI", brand["canvas"]["dpi"] == 300, ""))

    thc_lines = {
        5: "5MG HEMP-DERIVED THC PER CAN",
        10: "10MG HEMP-DERIVED THC PER CAN",
        50: "50MG HEMP-DERIVED THC PER CAN",
        100: "100MG HEMP-DERIVED THC PER CAN",
    }
    for sku in skus:
        checks.append((
            f"No 20MG in {sku['id']}",
            sku["thc_mg"] != 20 and "20MG" not in sku.get("thc_line", "").upper(),
            "",
        ))
        checks.append((f"THC line {sku['thc_mg']}mg", sku.get("thc_line") == thc_lines[sku["thc_mg"]], ""))

    checks.append(("Exactly 4 SKUs", len(skus) == 4, ""))
    checks.append(("2 flavors locked", len(flavors) == 2, ""))

    checks.append(("Manufactured By Proleve", brand["manufacturing"]["manufactured_by"] == "Proleve", ""))
    checks.append(("USA in address", "USA" in brand["manufacturing"]["address_lines"][-1], ""))
    checks.append(("Website", brand["brand"]["website"] == "AlternativeBev.com", ""))
    checks.append(("QR quiet zone config", "quiet_zone_ratio" in brand.get("qr_section", {}), ""))

    typo = brand["typography"]
    checks.append(("A symbol -10%", abs(typo.get("a_symbol_scale", 1) - 0.90) < 0.01, ""))
    checks.append(("Brand +20%", typo.get("brand_name_scale", 1) >= 1.20, ""))
    checks.append(("Flavor +35%", typo.get("flavor_scale", 1) >= 1.35, ""))

    for flavor in flavors:
        for sku in skus:
            data = load_compliance(sku["id"], flavor["id"])
            ok = data is not None and data.get("verified")
            checks.append((f"Compliance {sku['id']}/{flavor['id']}", ok, ""))
            if data and flavor["id"] == "passion_fruit":
                checks.append((f"PF calories [{sku['id']}]", data["nutrition_facts"]["calories"] == "0", ""))
                lines = data.get("ingredients_lines", [])
                checks.append((f"PF ingredients lines [{sku['id']}]", len(lines) == 3, ""))
            if data and flavor["id"] == "lychee_sweet_tea":
                checks.append((f"LT calories [{sku['id']}]", data["nutrition_facts"]["calories"] == "20", ""))
                lines = data.get("ingredients_lines", [])
                checks.append((f"LT ingredients lines [{sku['id']}]", len(lines) == 9, ""))

    for check in audit_hierarchy():
        checks.append((check.name, check.status != "fail", check.detail))

    audit = run_full_audit()
    checks.append(("Compliance audit exportable", audit.ok_for_export(), ""))

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    score = min(10.0, round((passed / total) * 10, 2))

    print("ALTERNATIVE™ Final Prepress + Retail Master Lock v2.0")
    print("=" * 60)
    for name, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        extra = f" ({detail})" if detail and not ok else ""
        print(f"  [{status}] {name}{extra}")
    print("=" * 60)
    print(f"Score: {passed}/{total} — Retail readiness: {score}/10")
    if audit.warnings:
        print(f"Pre-press warnings: {len(audit.warnings)} (barcode, lot, state — expected pre-assignment)")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
