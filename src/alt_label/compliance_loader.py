"""Load and validate manufacturer-provided compliance data."""

import json
from pathlib import Path
from typing import Any

import jsonschema

from .config_loader import ROOT, load_flavors, load_skus

SCHEMA_PATH = ROOT / "data" / "compliance" / "schema.json"
PRODUCTS_DIR = ROOT / "data" / "compliance" / "products"
FLAVORS_DIR = ROOT / "data" / "compliance" / "flavors"


def load_schema() -> dict:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def compliance_path(sku_id: str, flavor_id: str) -> Path:
    return PRODUCTS_DIR / f"{sku_id}_{flavor_id}.json"


def _load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _merge_compliance(sku_id: str, flavor_id: str) -> dict[str, Any] | None:
    """Merge product override with flavor-level manufacturer data."""
    product_path = compliance_path(sku_id, flavor_id)
    flavor_path = FLAVORS_DIR / f"{flavor_id}.json"

    if product_path.exists():
        data = _load_json(product_path)
    elif flavor_path.exists():
        flavor_data = _load_json(flavor_path)
        data = {
            "verified": flavor_data.get("verified", False),
            "product_id": f"alternative_{sku_id}_{flavor_id}",
            "source": flavor_data.get("source", "manufacturer_provided"),
            "nutrition_facts": flavor_data["nutrition_facts"],
            "ingredients": flavor_data["ingredients"],
            "qr_url": "https://AlternativeBev.com/lab-results",
            "state_warnings": [],
        }
    else:
        return None

    schema = load_schema()
    jsonschema.validate(data, schema)
    return data


def load_compliance(sku_id: str, flavor_id: str) -> dict[str, Any] | None:
    return _merge_compliance(sku_id, flavor_id)


def validate_for_production(compliance: dict | None) -> tuple[bool, str]:
    if compliance is None:
        return False, "No compliance data found for this SKU/flavor"
    if not compliance.get("verified"):
        return False, "Compliance data not verified"
    return True, "OK"


def ensure_product_files() -> list[Path]:
    """Generate product compliance stubs from flavor manufacturer data."""
    PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for sku in load_skus():
        for flavor in load_flavors():
            path = compliance_path(sku["id"], flavor["id"])
            if path.exists():
                continue
            flavor_path = FLAVORS_DIR / f"{flavor['id']}.json"
            if not flavor_path.exists():
                continue
            flavor_data = _load_json(flavor_path)
            product = {
                "verified": True,
                "product_id": f"alternative_{sku['id']}_{flavor['id']}",
                "source": "manufacturer_provided",
                "nutrition_facts": flavor_data["nutrition_facts"],
                "ingredients": flavor_data["ingredients"],
                "qr_url": "https://AlternativeBev.com/lab-results",
                "state_warnings": [],
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(product, f, indent=2)
                f.write("\n")
            created.append(path)
    return created
