"""Load syrup brand and flavor configuration."""

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
SYRUP_CONFIG = ROOT / "config" / "syrup"

__all__ = ["ROOT", "load_brand", "load_flavors", "mm_to_pt", "load_yaml"]


def load_yaml(name: str) -> dict[str, Any]:
    with open(SYRUP_CONFIG / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_brand() -> dict[str, Any]:
    return load_yaml("brand.yaml")


def load_flavors() -> list[dict[str, Any]]:
    return load_yaml("flavors.yaml")["flavors"]


def mm_to_pt(mm: float) -> float:
    return mm * 72 / 25.4
