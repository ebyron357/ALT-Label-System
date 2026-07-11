#!/usr/bin/env python3
"""ALTERNATIVE™ Final Manufacturing Readiness Review — audit dashboard."""

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "manufacturing" / "checklists.csv"

# Ranked blockers for first production order (highest risk first)
PRODUCTION_BLOCKERS = [
    ("1", "Proleve signed label approval not complete", "CRITICAL", "Proleve QA", "3-7 days", "HIGH",
     "Labels under review — no manufacturing release without written QA/legal sign-off"),
    ("2", "No GS1 UPC on 8 beverage SKUs", "CRITICAL", "Invictus", "5 days / $750", "HIGH",
     "Printing labels without UPC forces full reprint; blocks case codes and POS"),
    ("3", "Print files not converter-approved (PDF/X-1a / QR RGB)", "CRITICAL", "Proleve Prepress", "5-10 days", "HIGH",
     "RGB QR raster in CMYK workflow — converter rejection risk documented in v3 gate"),
    ("4", "No physical press proof on can substrate", "CRITICAL", "Proleve + Converter", "7-14 days", "HIGH",
     "Matte black ink adhesion and barcode scan unverified on actual can"),
    ("5", "Master formula not locked per THC tier (5/10/50/100 mg)", "CRITICAL", "Proleve R&D", "7-14 days", "HIGH",
     "Four potency tiers require separate formula records and dosing validation"),
    ("6", "No ISO 17025 lab under contract for batch release", "CRITICAL", "Proleve QA", "7-14 days", "HIGH",
     "Cannot release inventory without potency/homogeneity COA per batch"),
    ("7", "Shelf-life / stability study incomplete", "CRITICAL", "Proleve QA", "30-90 days", "HIGH",
     "Best-by date cannot be set; retail and distributor will reject undated claims"),
    ("8", "THC homogeneity not validated on fill line", "CRITICAL", "Proleve QA", "7-14 days", "HIGH",
     "Potency variance across cans creates regulatory and label-accuracy liability"),
    ("9", "12oz sleek can + end supply not PO'd", "CRITICAL", "Proleve Procurement", "14-28 days", "HIGH",
     "Can MOQ and lead time gate production slot regardless of label readiness"),
    ("10", "Batch record SOP (lot/batch/best-by) undefined", "CRITICAL", "Proleve Production", "3-5 days", "HIGH",
     "Label zones exist but encoding system not operationalized for run 1"),
    ("11", "Label converter PO not issued", "CRITICAL", "Proleve Procurement", "14-21 days", "HIGH",
     "Depends on UPC + PDF/X-1a + press proof — 2-3 week converter lead time"),
    ("12", "cGMP / HACCP plan not documented for THC beverages", "IMPORTANT", "Proleve QA", "14-30 days", "MEDIUM",
     "Distributor due diligence and recall readiness require documented food safety"),
    ("13", "Co-manufacturing agreement Invictus-Proleve unsigned", "IMPORTANT", "Invictus Legal", "7-14 days", "MEDIUM",
     "Liability allocation and spec ownership undefined"),
    ("14", "Product liability insurance not bound", "IMPORTANT", "Invictus", "7 days / $3-8K", "MEDIUM",
     "Does not block pilot run at Proleve but blocks inventory transfer to Invictus"),
    ("15", "Quarantine / hold-release procedure undefined", "IMPORTANT", "Proleve QA", "3 days", "MEDIUM",
     "Failed COA batches need documented disposition before scale"),
]


def load_items() -> list[dict]:
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    items = load_items()
    by_checklist = defaultdict(list)
    for row in items:
        by_checklist[row["checklist"]].append(row)

    open_items = [r for r in items if r["status"] == "OPEN"]
    critical_open = [r for r in open_items if r["classification"] == "CRITICAL"]
    prod_blockers = [r for r in open_items if "PRODUCTION_ORDER" in r.get("blocks", "")]

    print("ALTERNATIVE™ FINAL MANUFACTURING READINESS REVIEW")
    print("=" * 60)
    print()
    print("FIRST PRODUCTION ORDER TOMORROW?  NO")
    print()
    print("RANKED BLOCKERS (highest risk → lowest)")
    print("-" * 60)
    for row in PRODUCTION_BLOCKERS:
        print(f"  #{row[0]} [{row[2]}] {row[1]}")
        print(f"      Owner: {row[3]} | Timeline: {row[4]} | Risk: {row[5]}")
        print(f"      → {row[6]}")
        print()

    print("CHECKLIST SUMMARY")
    print("-" * 60)
    for name in ("MANUFACTURING", "PRODUCTION", "LAUNCH", "WHOLESALE", "RETAIL", "DTC"):
        rows = by_checklist[name]
        crit = sum(1 for r in rows if r["classification"] == "CRITICAL" and r["status"] == "OPEN")
        imp = sum(1 for r in rows if r["classification"] == "IMPORTANT" and r["status"] == "OPEN")
        opt = sum(1 for r in rows if r["classification"] == "OPTIONAL" and r["status"] == "OPEN")
        print(f"  {name:14} {len(rows):2} items | OPEN critical: {crit} | important: {imp} | optional: {opt}")

    print()
    print("CHANNEL READINESS (open CRITICAL items)")
    print("-" * 60)
    channels = {
        "Production Order": prod_blockers,
        "Inventory Creation": [r for r in open_items if "INVENTORY" in r.get("blocks", "")],
        "DTC Launch": [r for r in open_items if "DTC" in r.get("blocks", "")],
        "Wholesale Launch": [r for r in open_items if "WHOLESALE" in r.get("blocks", "")],
        "Retail Launch": [r for r in open_items if "RETAIL" in r.get("blocks", "")],
    }
    for ch, rows in channels.items():
        crit = sum(1 for r in rows if r["classification"] == "CRITICAL")
        print(f"  {ch:22} {crit:2} critical open / {len(rows):2} total open")

    print()
    print("SCORES")
    print("-" * 60)
    total = len(items)
    complete = sum(1 for r in items if r["status"] != "OPEN")
    mfg_score = round((1 - len([r for r in by_checklist["MANUFACTURING"] if r["status"] == "OPEN"]) / max(1, len(by_checklist["MANUFACTURING"]))) * 10, 1)
    prod_score = round((1 - len(prod_blockers) / max(1, len([r for r in items if "PRODUCTION_ORDER" in r.get("blocks", "")]))) * 10, 1)

    scores = [
        ("Manufacturing Readiness", mfg_score, "YELLOW" if mfg_score >= 5 else "RED"),
        ("Production File Readiness", 6.5, "YELLOW"),
        ("Formula / QA Readiness", 3.5, "RED"),
        ("Packaging Supply Readiness", 4.0, "RED"),
        ("Inventory Readiness", 5.0, "YELLOW"),
        ("DTC Launch Readiness", 4.5, "RED"),
        ("Wholesale Launch Readiness", 3.5, "RED"),
        ("Retail Launch Readiness", 4.0, "RED"),
    ]
    for label, score, status in scores:
        flag = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}[status]
        print(f"  [{flag} {status:6}] {label}: {score}/10")

    print()
    print(f"Checklist database: {CSV_PATH}")
    print(f"Full report: docs/FINAL_MANUFACTURING_READINESS_REVIEW.md")
    print(f"Open items: {len(open_items)}/{total} | Critical open: {len(critical_open)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
