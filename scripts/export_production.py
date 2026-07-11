#!/usr/bin/env python3
"""
ALTERNATIVE™ Final Prepress + Retail Master Lock v2.0
Generate 8 production PDFs with compliance and prepress audits.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alt_label.compliance_audit import run_full_audit
from alt_label.pdfx_export import convert_to_pdfx1a, pdfx_available
from alt_label.prepress import audit_hierarchy, audit_pdf
from alt_label.renderer import render_all


DELIVERABLES = [
    ("lychee_sweet_tea", "session_5mg", "Lychee Sweet Tea — Session 5mg"),
    ("lychee_sweet_tea", "social_10mg", "Lychee Sweet Tea — Social 10mg"),
    ("lychee_sweet_tea", "reserve_50mg", "Lychee Sweet Tea — Reserve 50mg"),
    ("lychee_sweet_tea", "reserve_100mg", "Lychee Sweet Tea — Reserve 100mg"),
    ("passion_fruit", "session_5mg", "Passion Fruit — Session 5mg"),
    ("passion_fruit", "social_10mg", "Passion Fruit — Social 10mg"),
    ("passion_fruit", "reserve_50mg", "Passion Fruit — Reserve 50mg"),
    ("passion_fruit", "reserve_100mg", "Passion Fruit — Reserve 100mg"),
]


def main() -> int:
    output_dir = ROOT / "output" / "production_v2"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("ALTERNATIVE™ — Final Prepress + Retail Master Lock v2.0")
    print("=" * 60)

    # Compliance audit
    print("\n[1/4] Compliance Audit")
    compliance = run_full_audit()
    for item in compliance.items:
        icon = {"pass": "✓", "warn": "!", "fail": "✗"}[item.status]
        detail = f" — {item.detail}" if item.detail else ""
        print(f"  [{icon}] {item.name}{detail}")

    if not compliance.ok_for_export():
        print("\nABORT: Compliance failures detected.")
        return 1

    warns = len(compliance.warnings)
    if warns:
        print(f"\n  {warns} warning(s) flagged — review before press (barcode, lot, state)")

    # Hierarchy QC
    print("\n[2/4] Hierarchy QC (100% / 50% / 25% / 10%)")
    for check in audit_hierarchy():
        icon = "✓" if check.status == "pass" else "!"
        print(f"  [{icon}] {check.name}: {check.detail}")

    # Generate PDFs
    print("\n[3/4] Generating 8 Production PDFs")
    paths = render_all(output_dir, mode="production")
    for p in paths:
        print(f"  → {p.name}")

    # Prepress audit per file
    print("\n[4/4] Prepress Audit")
    all_prepress_ok = True
    for p in paths:
        checks = audit_pdf(p)
        fails = [c for c in checks if c.status == "fail"]
        if fails:
            all_prepress_ok = False
            print(f"  ✗ {p.name}: {fails[0].name}")
        else:
            print(f"  ✓ {p.name}")

    # PDF/X-1a if available
    pdfx_paths: list[Path] = []
    if pdfx_available():
        pdfx_dir = output_dir / "pdfx"
        pdfx_dir.mkdir(exist_ok=True)
        print("\n[PDF/X-1a Export]")
        for p in paths:
            out = pdfx_dir / p.name.replace(".pdf", "_PDFX1a.pdf")
            try:
                convert_to_pdfx1a(p, out)
                pdfx_paths.append(out)
                print(f"  → {out.name}")
            except Exception as e:
                print(f"  ! {p.name}: {e}")

    # Manifest
    manifest = {
        "version": "2.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "deliverables": [
            {
                "flavor": flavor,
                "sku": sku,
                "label": label,
                "pdf": f"alternative_{sku}_{flavor}.pdf",
            }
            for flavor, sku, label in DELIVERABLES
        ],
        "compliance_warnings": len(compliance.warnings),
        "pdfx_exported": len(pdfx_paths),
        "retail_readiness_target": "9.5+/10",
    }
    manifest_path = output_dir / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"\nManifest: {manifest_path}")
    print(f"\nDelivered {len(paths)} production PDFs → {output_dir}")

    return 0 if all_prepress_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
