"""Phase 1 compliance audit for syrup labels."""

from dataclasses import dataclass, field

from .compliance_loader import load_compliance
from .config_loader import load_brand, load_flavors


@dataclass
class Finding:
    severity: str  # CRITICAL | MAJOR | MINOR
    category: str
    issue: str
    recommendation: str


@dataclass
class AuditReport:
    findings: list[Finding] = field(default_factory=list)

    def critical(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "CRITICAL"]

    def major(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "MAJOR"]

    def minor(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "MINOR"]


def run_audit() -> AuditReport:
    report = AuditReport()
    brand = load_brand()

    # Pre-system baseline findings (greenfield audit)
    report.findings.append(Finding(
        "CRITICAL", "System",
        "No unified syrup label system existed prior to this build",
        "Deploy master system architecture with locked grid and panel structure",
    ))

    for flavor in load_flavors():
        fid = flavor["id"]
        data = load_compliance(fid)
        label = flavor["display_name"]

        if not data or not data.get("verified"):
            report.findings.append(Finding(
                "CRITICAL", "Compliance", f"{label}: Missing verified compliance data",
                "Add manufacturer-verified JSON to data/compliance/syrup/flavors/",
            ))
            continue

        sf = data["supplement_facts"]
        if sf["servings_per_container"] != 84 or sf["amount_per_serving"] != "5 mg":
            report.findings.append(Finding(
                "CRITICAL", "Supplement Facts", f"{label}: Serving/THC mismatch",
                "Lock to 5mL serving, 5mg THC, 84 servings per container",
            ))

        if not data.get("ingredients_lines"):
            report.findings.append(Finding(
                "MAJOR", "Ingredients", f"{label}: No line-format ingredient declaration",
                "Use manufacturer ingredients_lines array",
            ))

        if not data.get("barcode", {}).get("upc"):
            report.findings.append(Finding(
                "MAJOR", "UPC", f"{label}: No UPC assigned",
                "Assign UPC before retail distribution; barcode zone is reserved",
            ))

        if not data.get("lot_number"):
            report.findings.append(Finding(
                "MINOR", "Lot Coding", f"{label}: Lot number per-run not set",
                "Populate at production; lot area preserved on label",
            ))

        if not data.get("best_by"):
            report.findings.append(Finding(
                "MINOR", "Best By", f"{label}: Best-by date per-run not set",
                "Populate at production; area preserved on label",
            ))

        if not data.get("state_warnings"):
            report.findings.append(Finding(
                "MAJOR", "State THC Disclosure", f"{label}: No state-specific warnings",
                "Add state_warnings per target distribution markets before national rollout",
            ))

    if brand["warning_panel"]["lines"]:
        report.findings.append(Finding(
            "MINOR", "Warnings",
            "Warning panel strengthened with syrup-specific serving guidance",
            "Legal review recommended for target states before national distribution",
        ))

    return report
