#!/usr/bin/env python3
"""ALTERNATIVE™ Syrup — Master production export (4 flavors)."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alt_syrup.compliance_audit import run_audit
from alt_syrup.compliance_loader import validate_for_production, load_compliance
from alt_syrup.config_loader import load_flavors
from alt_syrup.renderer import render_all

try:
    from alt_label.pdfx_export import convert_to_pdfx1a, pdfx_available
except ImportError:
    pdfx_available = lambda: False
    convert_to_pdfx1a = None


def main() -> int:
    out = ROOT / "output" / "syrup_production"
    out.mkdir(parents=True, exist_ok=True)

    print("ALTERNATIVE™ Syrup Master System — Production Export")
    print("=" * 60)

    audit = run_audit()
    print(f"\nCompliance Audit: {len(audit.critical())} critical, "
          f"{len(audit.major())} major, {len(audit.minor())} minor")

    for flavor in load_flavors():
        ok, msg = validate_for_production(load_compliance(flavor["id"]))
        if not ok:
            print(f"ABORT {flavor['id']}: {msg}")
            return 1

    paths = render_all(out, mode="production")
    for p in paths:
        print(f"  → {p.name}")

    if pdfx_available() and convert_to_pdfx1a:
        pdfx_dir = out / "pdfx"
        pdfx_dir.mkdir(exist_ok=True)
        for p in paths:
            try:
                convert_to_pdfx1a(p, pdfx_dir / p.name.replace(".pdf", "_PDFX1a.pdf"))
            except Exception as e:
                print(f"  ! PDF/X {p.name}: {e}")

    manifest = {
        "system": "ALTERNATIVE Syrup Master v1.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "deliverables": [p.name for p in paths],
        "flavors": [f["display_name"] for f in load_flavors()],
        "audit_summary": {
            "critical": len(audit.critical()),
            "major": len(audit.major()),
            "minor": len(audit.minor()),
        },
    }
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"\nDelivered {len(paths)} labels → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
