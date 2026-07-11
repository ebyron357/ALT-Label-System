#!/usr/bin/env python3
"""ALTERNATIVE™ Final Production Lock v3.0 — Launch Readiness Auditor."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alt_label.compliance_audit import run_full_audit as can_compliance
from alt_label.config_loader import load_brand as load_can_brand
from alt_label.prepress import audit_pdf, audit_hierarchy
from alt_syrup.compliance_audit import run_audit as syrup_compliance
from alt_syrup.config_loader import load_brand as load_syrup_brand
from alt_syrup.config_loader import load_flavors as load_syrup_flavors
from alt_label.config_loader import load_flavors as load_can_flavors, load_skus


def main() -> int:
    print("ALTERNATIVE™ FINAL PRODUCTION LOCK v3.0")
    print("=" * 60)

    can_brand = load_can_brand()
    syrup_brand = load_syrup_brand()
    can_c = can_compliance()
    syrup_c = syrup_compliance()

    # Brand consistency checks
    print("\nBRAND CONSISTENCY")
    checks = [
        ("Wordmark ALTERNATIVE™", can_brand["brand"]["name"] == syrup_brand["brand"]["name"]),
        ("Website URL", can_brand["brand"]["website"] == syrup_brand["brand"]["website"]),
        ("QR copy identical", can_brand["qr_section"]["heading_lines"] == syrup_brand["qr_section"]["heading_lines"]),
        ("Proleve manufacturer", can_brand["manufacturing"]["manufactured_by"] == syrup_brand["responsible_party"]["manufactured_by"]),
        ("Invictus responsible party", can_brand["manufacturing"]["manufactured_for"] == syrup_brand["responsible_party"]["manufactured_for"]),
        ("Tagline on beverage", can_brand["brand"].get("tagline") == "A NEW STATE OF MIND"),
        ("Tagline on syrup", False),  # documented gap
    ]
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'GAP '}] {name}")

    # Compliance summary
    print(f"\nCOMPLIANCE WARNINGS: {len(can_c.warnings)} beverage + {len(syrup_c.major()) + len(syrup_c.minor())} syrup")
    print(f"COMPLIANCE FAILURES: {len(can_c.failures)} beverage + {len(syrup_c.critical())} syrup critical")

    # Prepress
    print("\nPREPRESS (sample PDFs)")
    samples = list((ROOT / "output" / "production_v2").glob("*.pdf"))[:1]
    samples += list((ROOT / "output" / "syrup_production").glob("*.pdf"))[:1]
    rgb_risk = False
    for p in samples:
        for c in audit_pdf(p):
            if c.status == "warn" and "RGB" in c.name:
                rgb_risk = True
            if c.status != "pass":
                print(f"  [{c.status.upper()}] {p.name}: {c.name} — {c.detail}")
    if rgb_risk:
        print("  [CRITICAL] QR raster introduces RGB — PDF/X-1a risk")

    # Launch score
    critical_open = 5  # UPC, state, QR RGB, PDFX, legal sign-off
    score = max(0, 10 - critical_open * 0.5)
    print(f"\nFINAL LAUNCH READINESS SCORE: {score:.1f}/10")
    print("See docs/FINAL_PRODUCTION_LOCK_V3.md for full report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
