# ALT-Label-System

Code-driven packaging and label generation for **ALTERNATIVE™** — Retail Master Lock v1.0.

Refines existing can artwork into a production-ready, nationally scalable 12oz sleek label. **Not a redesign.**

## Shelf Priority (1-second recognition)

1. **ALTERNATIVE™** — dominant wordmark
2. **THC strength** — single-line callout (`5MG HEMP-DERIVED THC PER CAN`)
3. **Flavor** — LYCHEE SWEET TEA / PASSION FRUIT

## Quick Start

```bash
pip install -r requirements.txt
python3 scripts/generate_labels.py --mode production
python3 scripts/validate_spec.py
```

Generates 8 PDFs (4 SKUs × 2 flavors) at `output/labels/`.

### PDF/X-1a

```bash
python3 scripts/generate_labels.py --mode production --pdfx
```

## Locked Systems

| SKUs | SESSION™ 5mg · SOCIAL™ 10mg · RESERVE™ 50mg · RESERVE™ 100mg |
| Flavors | LYCHEE SWEET TEA · PASSION FRUIT |
| No 20MG | Permanently excluded |

## Manufacturer Data

Nutrition and ingredients use **exact manufacturer-provided values** per flavor. See [data/compliance/README.md](data/compliance/README.md).

## Cleanup Pass

No decorative diamonds, dots, borders, separators, or filler graphics. Functional elements only.

## Spec

- Canvas: 182.22mm × 148mm · CMYK · 300 DPI
- Matte black · warm off-white · flavor accent (gold/amber reduced to brand + THC + highlights)
- Manufactured By: Proleve · Manufactured For: Invictus Wellness LLC
