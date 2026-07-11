# ALT-Label-System

**ALTERNATIVE™ Final Prepress + Retail Master Lock v2.0**

Code-driven label generation for 12oz sleek cans. Refinement and production preparation — **not a redesign**.

## Shelf Priority (1-second test)

1. **ALTERNATIVE™** — dominant wordmark
2. **THC strength** — single-line SKU callout
3. **Flavor** — LYCHEE SWEET TEA / PASSION FRUIT

## Production Export (8 PDFs)

```bash
pip install -r requirements.txt
python3 scripts/export_production.py
python3 scripts/validate_spec.py
```

Output: `output/production_v2/` + `MANIFEST.json`

### Deliverables

| Flavor | SKUs |
|--------|------|
| Lychee Sweet Tea | Session 5mg · Social 10mg · Reserve 50mg · Reserve 100mg |
| Passion Fruit | Session 5mg · Social 10mg · Reserve 50mg · Reserve 100mg |

## Audits (v2.0)

- **Compliance audit** — nutrition, ingredients, THC, warnings, QR, barcode/lot flags
- **Prepress audit** — bleed, CMYK, fonts, artboard dimensions
- **Hierarchy QC** — readability at 100% / 50% / 25% / 10%

## Manufacturer Data (exact)

| Flavor | Calories | Ingredients |
|--------|----------|-------------|
| Passion Fruit | 0 | 3 lines — manufacturer format |
| Lychee Sweet Tea | 20 | 9 lines — manufacturer format |

## Print Spec

- Trim: 182.22mm × 148mm + 3.175mm bleed
- CMYK · 300 DPI · PDF/X-1a (`--pdfx` or via export script)
- No decorative elements · No AI artifacts · No 20MG

## Pre-Press Warnings (expected)

UPC barcodes, lot/batch/best-by values, and state-specific warnings are flagged but do not block export — zones are preserved for production run assignment.
