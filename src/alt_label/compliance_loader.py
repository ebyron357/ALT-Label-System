"""Load and validate Proleve-supplied compliance data."""

import json
from pathlib import Path
from typing import Any

import jsonschema

from .config_loader import ROOT

SCHEMA_PATH = ROOT / "data" / "compliance" / "schema.json"
PRODUCTS_DIR = ROOT / "data" / "compliance" / "products"


def load_schema() -> dict:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def compliance_path(sku_id: str, flavor_id: str) -> Path:
    return PRODUCTS_DIR / f"{sku_id}_{flavor_id}.json"


def load_compliance(sku_id: str, flavor_id: str) -> dict[str, Any] | None:
    path = compliance_path(sku_id, flavor_id)
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    schema = load_schema()
    jsonschema.validate(data, schema)
    return data


def validate_for_production(compliance: dict | None) -> tuple[bool, str]:
    if compliance is None:
        return False, "No compliance data file found"
    if not compliance.get("verified"):
        return False, "Compliance data not verified — set verified: true after Proleve approval"
    return True, "OK"
