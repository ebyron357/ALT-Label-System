# Compliance Data — Proleve Supplied Only

Production label generation requires verified compliance JSON per product variant.

## File Naming

```
data/compliance/products/{sku_id}_{flavor_id}.json
```

Examples:
- `session_5mg_lychee_sweet_tea.json`
- `reserve_100mg_passion_fruit.json`

## Required Fields

See `schema.json` for the full JSON Schema. All fields must contain **actual Proleve-supplied data** — no estimates or placeholders.

| Field | Source |
|-------|--------|
| `verified` | Must be `true` after Proleve QA approval |
| `nutrition_facts` | Proleve formulation / lab analysis |
| `ingredients` | Proleve ingredient statement |
| `barcode` | Assigned UPC from Invictus / Proleve |
| `qr_url` | COA / lab results landing page |
| `state_warnings` | Jurisdiction-specific legal copy |
| `lot_number`, `batch_number`, `best_by` | Per production run |

## Generate Production Labels

```bash
# After adding verified JSON files:
python scripts/generate_labels.py --mode production --pdfx
```

## Preview Labels (No Compliance Data)

```bash
python scripts/generate_labels.py --mode preview
```

Preview mode renders the full brand hierarchy and compliance panel structure without fabricated nutrition, ingredient, or barcode values.
