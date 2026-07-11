"""Load brand, SKU, and flavor configuration."""

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"


def load_yaml(name: str) -> dict[str, Any]:
    with open(CONFIG_DIR / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_brand() -> dict[str, Any]:
    return load_yaml("brand.yaml")


def load_skus() -> list[dict[str, Any]]:
    return load_yaml("skus.yaml")["skus"]


def load_flavors() -> list[dict[str, Any]]:
    return load_yaml("flavors.yaml")["flavors"]


def mm_to_pt(mm: float) -> float:
    return mm * 72 / 25.4
