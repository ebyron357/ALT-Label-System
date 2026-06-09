# Compliance Data — Manufacturer Provided

Retail Master Lock v1.0 requires **exact manufacturer-provided** nutrition and ingredient data. No estimates.

## Flavor-Level Data (locked)

| Flavor | Calories | Ingredients |
|--------|----------|-------------|
| PASSION FRUIT | 0 | Carbonated Water, Natural Passion Fruit Flavor, Hemp-Derived THC |
| LYCHEE SWEET TEA | 20 | Water, Organic Cane Sugar, Natural Lychee Flavoring, Citric Acid, Malic Acid, Tartaric Acid, Tea Flavoring, Potassium Sorbate, Hemp-Derived Delta-9 THC |

Stored in `flavors/{flavor_id}.json`. Product files inherit this data automatically.

## Product Overrides

Optional per-SKU files in `products/{sku_id}_{flavor_id}.json` for:
- Assigned UPC barcode
- Lot / batch / best-by per production run
- State-specific warnings

## Generate Labels

```bash
python3 scripts/generate_labels.py --mode production
python3 scripts/validate_spec.py
```
