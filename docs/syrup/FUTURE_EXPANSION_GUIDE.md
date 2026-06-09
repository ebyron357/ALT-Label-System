# ALTERNATIVE™ Syrup — Future Flavor Expansion Guide

## Add a New Flavor (5 minutes)

### 1. Register flavor
Edit `config/syrup/flavors.yaml`:
```yaml
  - id: peach
    name: "PEACH"
    display_name: "Peach"
    accent_color: citrus_accent
```

### 2. Add manufacturer compliance data
Create `data/compliance/syrup/flavors/peach.json`:
```json
{
  "verified": true,
  "source": "manufacturer_provided",
  "supplement_facts": {
    "serving_size": "5 mL",
    "servings_per_container": 84,
    "active_ingredient": "Hemp-Derived Delta-9 THC",
    "amount_per_serving": "5 mg",
    "other_ingredients": []
  },
  "ingredients": "...",
  "ingredients_lines": ["...", "Hemp-Derived Delta-9 THC", "..."]
}
```

### 3. Generate
```bash
python3 scripts/export_syrup_production.py
```

No grid, typography, or panel changes required.

---

## Add a New Strength

Edit `config/syrup/brand.yaml` `product` block:
```yaml
product:
  total_thc_mg: 840        # example
  thc_per_serving_mg: 10
  servings_per_container: 84
```

Front panel hierarchy auto-updates. Supplement Facts pulls from compliance JSON.

---

## Add a New Bottle Size

Edit `config/syrup/brand.yaml`:
```yaml
canvas:
  panel_width_mm: 60.0     # example larger bottle
  panel_height_mm: 100.0
product:
  net_contents: "8 FL OZ (237 mL)"
```

Re-export all flavors. Panel structure unchanged.

---

## Add State Warnings

Per flavor or globally in product override `data/compliance/syrup/products/{flavor}.json`:
```json
{
  "state_warnings": [
    "CALIFORNIA: This product contains THC..."
  ]
}
```

---

## Illustrator Workflow

1. Open `assets/syrup/masters/front_panel_master.svg` or `back_panel_master.svg`
2. Import generated PDF for reference positioning
3. All production text should remain driven by `alt_syrup` renderer for consistency
4. Use masters for manual prepress adjustments only — regenerate PDF after config changes
