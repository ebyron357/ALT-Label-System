"""Syrup label renderer — master system, all flavors."""

from pathlib import Path

from reportlab.pdfgen import canvas

from .colors import MATTE_BLACK
from .compliance_loader import load_compliance, validate_for_production
from .config_loader import load_brand, load_flavors
from .layout import build_layout
from .panels.back_panel import render_back_panel
from .panels.front_panel import render_front_panel


def render_syrup_label(
    output_path: Path,
    flavor_id: str,
    mode: str = "production",
) -> Path:
    brand = load_brand()
    flavors = {f["id"]: f for f in load_flavors()}
    if flavor_id not in flavors:
        raise ValueError(f"Unknown flavor: {flavor_id}")

    flavor = flavors[flavor_id]
    compliance = load_compliance(flavor_id)
    if mode == "production":
        ok, msg = validate_for_production(compliance)
        if not ok:
            raise ValueError(f"Production blocked: {msg}")

    layout = build_layout()
    typo = brand["typography"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=(layout.width, layout.height))
    c.setTitle(f"ALTERNATIVE Syrup {flavor['display_name']}")
    c.setAuthor("ALT-Syrup-System v1.0")

    c.setFillColor(MATTE_BLACK)
    c.rect(0, 0, layout.width, layout.height, fill=1, stroke=0)

    render_front_panel(c, layout, brand, flavor, typo)
    render_back_panel(c, layout, brand, compliance, typo)

    c.save()
    return output_path


def render_all(output_dir: Path, mode: str = "production") -> list[Path]:
    paths: list[Path] = []
    for flavor in load_flavors():
        name = f"alternative_syrup_{flavor['id']}.pdf"
        paths.append(render_syrup_label(output_dir / name, flavor["id"], mode=mode))
    return paths
