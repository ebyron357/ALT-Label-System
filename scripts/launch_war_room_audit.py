#!/usr/bin/env python3
"""ALTERNATIVE™ National Launch War Room v1.0 — Executive Dashboard."""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "launch" / "state_matrix.csv"


def main() -> int:
    print("ALTERNATIVE™ NATIONAL LAUNCH WAR ROOM v1.0")
    print("=" * 60)
    print("GO/NO-GO: NO nationwide | CONDITIONAL GO phased regional\n")

    tiers = {"TIER1": 0, "TIER2": 0, "TIER3": 0}
    sku_5_states = 0
    blocked_states = []

    with open(MATRIX, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tiers[row["tier"]] = tiers.get(row["tier"], 0) + 1
            if row["sku_5mg"] == "YES":
                sku_5_states += 1
            if row["tier"] == "TIER3":
                blocked_states.append(row["state"])

    print("STATE TIERS")
    print(f"  TIER 1 (launch now):  {tiers.get('TIER1', 0)}")
    print(f"  TIER 2 (conditions):  {tiers.get('TIER2', 0)}")
    print(f"  TIER 3 (do not enter): {tiers.get('TIER3', 0)}")
    print(f"  States where 5mg SKU legal: {sku_5_states}")
    print(f"  Hard-blocked: {', '.join(blocked_states)}")

    scores = {
        "National Launch": ("4.2/10", "RED"),
        "Compliance": ("6.5/10", "YELLOW"),
        "Distributor": ("4.0/10", "RED"),
        "Retail": ("5.5/10", "YELLOW"),
        "Operational": ("6.0/10", "YELLOW"),
        "Website": ("8.0/10", "GREEN"),
        "Manufacturing": ("7.5/10", "GREEN"),
        "Revenue": ("7.0/10", "YELLOW"),
    }
    print("\nEXECUTIVE DASHBOARD")
    for k, (v, status) in scores.items():
        print(f"  [{status:6}] {k}: {v}")

    print("\n$250K INVENTORY: NO-GO national | GO $85K phased (5/10mg, Tier1+TN+PA)")
    print("Full report: docs/NATIONAL_LAUNCH_WAR_ROOM_V1.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
