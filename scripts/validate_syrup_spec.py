#!/usr/bin/env python3
"""Validate ALTERNATIVE™ syrup master system."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alt_syrup.compliance_loader import load_compliance
from alt_syrup.config_loader import load_brand, load_flavors


def main() -> int:
    brand = load_brand()
    flavors = load_flavors()
    checks: list[tuple[str, bool, str]] = []

    checks.append(("4 flavors locked", len(flavors) == 4, ""))
    names = {f["name"] for f in flavors}
    for n in ["ORIGINAL", "GRAPE", "STRAWBERRY", "MANGO"]:
        checks.append((f"Flavor {n}", n in names, ""))

    p = brand["product"]
    checks.append(("420mg total THC", p["total_thc_mg"] == 420, ""))
    checks.append(("5mg per serving", p["thc_per_serving_mg"] == 5, ""))
    checks.append(("84 servings", p["servings_per_container"] == 84, ""))
    checks.append(("5mL serving", p["serving_size"] == "5 mL", ""))
    checks.append(("4 FL OZ net", "4 FL OZ" in p["net_contents"], ""))

    checks.append(("Proleve manufacturer", brand["responsible_party"]["manufactured_by"] == "Proleve", ""))
    checks.append(("Invictus responsible party", "Invictus" in brand["responsible_party"]["manufactured_for"], ""))
    checks.append(("Syrup warnings include serving guidance", any("serving" in l.lower() for l in brand["warning_panel"]["lines"]), ""))

    for f in flavors:
        data = load_compliance(f["id"])
        checks.append((f"Compliance {f['id']}", data and data.get("verified"), ""))
        if data:
            sf = data["supplement_facts"]
            checks.append((f"SF servings {f['id']}", sf["servings_per_container"] == 84, ""))
            checks.append((f"SF THC {f['id']}", sf["amount_per_serving"] == "5 mg", ""))

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    print("ALTERNATIVE™ Syrup Master System — Validation")
    print("=" * 55)
    for name, ok, detail in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" ({detail})" if detail and not ok else ""))
    print("=" * 55)
    print(f"Score: {passed}/{total}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
