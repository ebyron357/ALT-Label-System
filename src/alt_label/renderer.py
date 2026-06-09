"""Main label PDF renderer."""

from pathlib import Path

from reportlab.pdfgen import canvas

from .compliance_loader import load_compliance
from .config_loader import load_brand, load_flavors, load_skus
from .layout import build_layout
from .panels.compliance_panel import render_compliance_panel
from .panels.front_panel import render_front_panel


def render_label(
    output_path: Path,
    sku_id: str,
    flavor_id: str,
    mode: str = "preview",
) -> Path:
    """
    Render a single label PDF.

    mode:
      - preview: brand layout with compliance placeholders (no fake data)
      - production: requires verified Proleve compliance JSON
    """
    brand = load_brand()
    skus = {s["id"]: s for s in load_skus()}
    flavors = {f["id"]: f for f in load_flavors()}

    if sku_id not in skus:
        raise ValueError(f"Unknown SKU: {sku_id}")
    if flavor_id not in flavors:
        raise ValueError(f"Unknown flavor: {flavor_id}")

    sku = skus[sku_id]
    flavor = flavors[flavor_id]
    flavor["accent_color"] = flavor.get("accent_color", "champagne_gold")

    compliance = load_compliance(sku_id, flavor_id)
    if mode == "production":
        from .compliance_loader import validate_for_production
        ok, msg = validate_for_production(compliance)
        if not ok:
            raise ValueError(f"Production mode blocked: {msg}")

    layout = build_layout()
    typo = brand["typography"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=(layout.width, layout.height))
    c.setTitle(f"ALTERNATIVE {sku['name']} {flavor['name']}")
    c.setAuthor("ALT-Label-System v1")

    # Full canvas matte black base
    from .colors import MATTE_BLACK
    c.setFillColor(MATTE_BLACK)
    c.rect(0, 0, layout.width, layout.height, fill=1, stroke=0)

    render_front_panel(c, layout, brand, sku, flavor, typo)
    render_compliance_panel(c, layout, brand, sku, compliance, typo)

    # Safe zone guide (non-printing metadata — omitted in production export)
    if mode == "preview":
        c.setStrokeColorRGB(0.3, 0.3, 0.3)
        c.setLineWidth(0.25)
        c.rect(layout.safe.x, layout.safe.y, layout.safe.width, layout.safe.height, fill=0, stroke=1)

    c.save()
    return output_path


def render_all(output_dir: Path, mode: str = "preview") -> list[Path]:
    """Generate all SKU × flavor combinations."""
    skus = load_skus()
    flavors = load_flavors()
    paths: list[Path] = []
    for sku in skus:
        for flavor in flavors:
            filename = f"alternative_{sku['id']}_{flavor['id']}.pdf"
            path = render_label(output_dir / filename, sku["id"], flavor["id"], mode=mode)
            paths.append(path)
    return paths
