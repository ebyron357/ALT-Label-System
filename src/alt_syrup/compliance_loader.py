"""Load manufacturer syrup compliance data."""

import json
from pathlib import Path
from typing import Any

import jsonschema

from .config_loader import ROOT

SCHEMA_PATH = ROOT / "data" / "compliance" / "syrup" / "schema.json"
FLAVORS_DIR = ROOT / "data" / "compliance" / "syrup" / "flavors"
PRODUCTS_DIR = ROOT / "data" / "compliance" / "syrup" / "products"


def load_schema() -> dict:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_compliance(flavor_id: str) -> dict[str, Any] | None:
    product_path = PRODUCTS_DIR / f"{flavor_id}.json"
    flavor_path = FLAVORS_DIR / f"{flavor_id}.json"

    if product_path.exists():
        data = _load_json(product_path)
    elif flavor_path.exists():
        flavor_data = _load_json(flavor_path)
        data = {
            "verified": flavor_data.get("verified", False),
            "product_id": f"alternative_syrup_{flavor_id}",
            "source": flavor_data.get("source", "manufacturer_provided"),
            "supplement_facts": flavor_data["supplement_facts"],
            "ingredients": flavor_data["ingredients"],
            "ingredients_lines": flavor_data["ingredients_lines"],
            "qr_url": "https://AlternativeBev.com/lab-results",
            "state_warnings": [],
        }
    else:
        return None

    jsonschema.validate(data, load_schema())
    return data


def validate_for_production(compliance: dict | None) -> tuple[bool, str]:
    if not compliance or not compliance.get("verified"):
        return False, "Missing or unverified compliance data"
    return True, "OK"
