#!/usr/bin/env python3
"""Generate ALTERNATIVE™ 12oz sleek can labels — Retail Master Lock v1.0."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alt_label.compliance_loader import ensure_product_files
from alt_label.pdfx_export import convert_to_pdfx1a, pdfx_available
from alt_label.renderer import render_all, render_label


def main() -> int:
    parser = argparse.ArgumentParser(description="ALTERNATIVE™ label generator")
    parser.add_argument(
        "--mode",
        choices=["preview", "production"],
        default="production",
        help="production requires verified manufacturer compliance data",
    )
    parser.add_argument("--output", type=Path, default=ROOT / "output" / "labels")
    parser.add_argument("--sku", help="Single SKU id")
    parser.add_argument("--flavor", help="Single flavor id")
    parser.add_argument("--pdfx", action="store_true", help="Export PDF/X-1a via Ghostscript")
    parser.add_argument("--bootstrap", action="store_true", help="Create product compliance files from flavor data")
    args = parser.parse_args()

    if args.bootstrap:
        created = ensure_product_files()
        print(f"Bootstrapped {len(created)} product compliance file(s)")

    args.output.mkdir(parents=True, exist_ok=True)

    if args.sku and args.flavor:
        filename = f"alternative_{args.sku}_{args.flavor}.pdf"
        paths = [render_label(args.output / filename, args.sku, args.flavor, mode=args.mode)]
    else:
        paths = render_all(args.output, mode=args.mode)

    print(f"Generated {len(paths)} label(s) → {args.output} [{args.mode}]")

    if args.pdfx and pdfx_available():
        pdfx_dir = args.output / "pdfx"
        pdfx_dir.mkdir(exist_ok=True)
        for p in paths:
            out = pdfx_dir / p.name.replace(".pdf", "_PDFX1a.pdf")
            convert_to_pdfx1a(p, out)
            print(f"  PDF/X-1a: {out}")
    elif args.pdfx:
        print("WARNING: Ghostscript not available — skipping PDF/X-1a", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
