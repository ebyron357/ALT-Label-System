"""Compliance audit — flag missing items before prepress export."""

from dataclasses import dataclass, field

from .compliance_loader import load_compliance
from .config_loader import load_brand, load_flavors, load_skus


@dataclass
class AuditItem:
    category: str
    name: str
    status: str  # pass | warn | fail
    detail: str = ""


@dataclass
class ComplianceReport:
    items: list[AuditItem] = field(default_factory=list)

    @property
    def failures(self) -> list[AuditItem]:
        return [i for i in self.items if i.status == "fail"]

    @property
    def warnings(self) -> list[AuditItem]:
        return [i for i in self.items if i.status == "warn"]

    @property
    def passed(self) -> list[AuditItem]:
        return [i for i in self.items if i.status == "pass"]

    def ok_for_export(self) -> bool:
        return len(self.failures) == 0


def audit_variant(sku_id: str, flavor_id: str, sku: dict) -> list[AuditItem]:
    items: list[AuditItem] = []
    data = load_compliance(sku_id, flavor_id)
    label = f"{sku_id}/{flavor_id}"

    if not data or not data.get("verified"):
        items.append(AuditItem("compliance", f"Verified data [{label}]", "fail", "Missing or unverified"))
        return items

    items.append(AuditItem("compliance", f"Verified data [{label}]", "pass"))

    nf = data.get("nutrition_facts", {})
    if nf.get("calories") is not None and nf.get("serving_size"):
        items.append(AuditItem("nutrition", f"Nutrition Facts [{label}]", "pass"))
    else:
        items.append(AuditItem("nutrition", f"Nutrition Facts [{label}]", "fail", "Incomplete panel"))

    if data.get("ingredients"):
        items.append(AuditItem("ingredients", f"Ingredient statement [{label}]", "pass"))
    else:
        items.append(AuditItem("ingredients", f"Ingredient statement [{label}]", "fail"))

    thc_line = sku.get("thc_line", "")
    if thc_line and "20MG" not in thc_line.upper():
        items.append(AuditItem("thc", f"THC declaration [{label}]", "pass", thc_line))
    else:
        items.append(AuditItem("thc", f"THC declaration [{label}]", "fail", "Invalid or 20MG reference"))

    items.append(AuditItem("net_contents", f"Net contents [{label}]", "pass", "12 FL OZ (355 mL)"))

    brand = load_brand()
    mfg = brand["manufacturing"]
    if mfg["manufactured_by"] == "Proleve" and mfg["manufactured_for"] == "Invictus Wellness LLC":
        items.append(AuditItem("manufacturer", f"Manufacturer info [{label}]", "pass"))
    else:
        items.append(AuditItem("manufacturer", f"Manufacturer info [{label}]", "fail"))

    if brand["warning_panel"]["lines"]:
        items.append(AuditItem("warnings", f"Warning statements [{label}]", "pass"))
    else:
        items.append(AuditItem("warnings", f"Warning statements [{label}]", "fail"))

    if data.get("qr_url"):
        items.append(AuditItem("qr", f"QR URL [{label}]", "pass"))
    else:
        items.append(AuditItem("qr", f"QR URL [{label}]", "warn", "Using default URL"))

    if data.get("barcode", {}).get("upc"):
        items.append(AuditItem("barcode", f"Barcode UPC [{label}]", "pass"))
    else:
        items.append(AuditItem("barcode", f"Barcode UPC [{label}]", "warn", "Zone reserved — UPC not assigned"))

    for field_name, display in [("lot_number", "Lot"), ("batch_number", "Batch"), ("best_by", "Best By")]:
        if data.get(field_name):
            items.append(AuditItem("production", f"{display} [{label}]", "pass"))
        else:
            items.append(AuditItem("production", f"{display} area [{label}]", "warn", "Area preserved — value per run"))

    if data.get("state_warnings"):
        items.append(AuditItem("state", f"State warnings [{label}]", "pass"))
    else:
        items.append(AuditItem("state", f"State warnings [{label}]", "warn", "Verify target state requirements"))

    return items


def run_full_audit() -> ComplianceReport:
    report = ComplianceReport()
    for sku in load_skus():
        for flavor in load_flavors():
            report.items.extend(audit_variant(sku["id"], flavor["id"], sku))
    return report
