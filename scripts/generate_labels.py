#!/usr/bin/env python3
"""Generate ALTERNATIVE™ 12oz sleek can labels — Production Master v1."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alt_label.pdfx_export import convert_to_pdfx1a, pdfx_available
from alt_label.renderer import render_all, render_label


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ALTERNATIVE™ label generator — 182.22mm × 148mm, CMYK, print-ready"
    )
    parser.add_argument(
        "--mode",
        choices=["preview", "production"],
        default="preview",
        help="preview: layout without unverified compliance data; production: requires verified JSON",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "output" / "labels",
        help="Output directory for PDF files",
    )
    parser.add_argument("--sku", help="Generate single SKU (e.g. session_5mg)")
    parser.add_argument("--flavor", help="Generate single flavor (e.g. lychee_sweet_tea)")
    parser.add_argument(
        "--pdfx",
        action="store_true",
        help="Also export PDF/X-1a via Ghostscript (requires gs)",
    )
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    if args.sku and args.flavor:
        filename = f"alternative_{args.sku}_{args.flavor}.pdf"
        path = render_label(args.output / filename, args.sku, args.flavor, mode=args.mode)
        paths = [path]
    else:
        paths = render_all(args.output, mode=args.mode)

    print(f"Generated {len(paths)} label(s) in {args.output} [{args.mode} mode]")

    if args.pdfx:
        if not pdfx_available():
            print("WARNING: Ghostscript not available — skipping PDF/X-1a export", file=sys.stderr)
        else:
            pdfx_dir = args.output / "pdfx"
            pdfx_dir.mkdir(exist_ok=True)
            for p in paths:
                out = pdfx_dir / p.name.replace(".pdf", "_PDFX1a.pdf")
                convert_to_pdfx1a(p, out)
                print(f"  PDF/X-1a: {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
