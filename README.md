# ALT-Label-System

Code-driven packaging and label generation system for **ALTERNATIVE™** — Production Master v1.

Generates retail-ready, compliance-ready 12oz sleek can labels (182.22mm × 148mm, CMYK, 300 DPI) while preserving the existing premium brand aesthetic.

## Specification

This system implements the **ALTERNATIVE™ Master Label Rebuild & Compliance Optimization** spec:

- **Not a redesign** — refinement of existing hierarchy, typography, and color system
- Locked SKU system: SESSION™ (5mg), SOCIAL™ (10mg), RESERVE™ (50mg / 100mg)
- Flavors: LYCHEE SWEET TEA, PASSION FRUIT (accent colors only — no fruit graphics)
- Matte black + warm off-white + flavor-specific gold/amber accents
- Manufacturing: Proleve Brands / Invictus Wellness LLC
- QR, warning panel, active ingredient, and protected barcode zones

## Quick Start

```bash
pip install -r requirements.txt
python scripts/generate_labels.py --mode preview
```

Output: `output/labels/alternative_{sku}_{flavor}.pdf` (8 variants)

### PDF/X-1a Export

Requires [Ghostscript](https://ghostscript.com/):

```bash
python scripts/generate_labels.py --mode preview --pdfx
```

### Production Labels

1. Add Proleve-verified compliance JSON per variant in `data/compliance/products/`
2. Set `"verified": true` in each file
3. Generate:

```bash
python scripts/generate_labels.py --mode production --pdfx
```

See [data/compliance/README.md](data/compliance/README.md) for the data schema.

## Label Hierarchy

| Priority | Element |
|----------|---------|
| 1 | A NEW STATE OF MIND |
| 2 | Hero A Symbol (reduced ~12%) |
| 3 | ALTERNATIVE™ (increased ~22%) |
| 4 | HEMP-DERIVED THC BEVERAGE |
| 5 | SKU (SESSION™ / SOCIAL™ / RESERVE™) |
| 6 | THC content (largest product element) |
| 7 | Flavor (increased ~35%) |
| 8 | 12 FL OZ (355 mL) |

## Project Structure

```
config/           Brand, SKU, and flavor definitions
data/compliance/  Proleve-supplied product data (schema + products/)
src/alt_label/    Label renderer, panels, PDF/X export
scripts/          CLI generator
assets/           Brand assets (A symbol reference)
output/           Generated PDFs (gitignored)
```

## Single Variant

```bash
python scripts/generate_labels.py --sku session_5mg --flavor lychee_sweet_tea
```

## Compliance Policy

**No placeholder compliance data.** Nutrition facts, ingredients, barcodes, and lot information render only from verified Proleve JSON files. Preview mode shows panel structure without fabricated values.
