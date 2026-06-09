# ALT-Label-System

Code-driven packaging and label generation for **ALTERNATIVE™** products.

## Product Lines

| Line | System | Export |
|------|--------|--------|
| **12oz Sleek Cans** | `alt_label` v2.0 | `python3 scripts/export_production.py` |
| **THC Syrup 4oz** | `alt_syrup` v1.0 | `python3 scripts/export_syrup_production.py` |

```bash
pip install -r requirements.txt
```

---

## Can Labels (Retail Master Lock v2.0)

8 PDFs — 4 SKUs × 2 flavors (Lychee Sweet Tea, Passion Fruit)

```bash
python3 scripts/export_production.py
python3 scripts/validate_spec.py
```

Output: `output/production_v2/`

---

## Syrup Labels (Master Compliance + Production Rebuild)

4 PDFs — Original · Grape · Strawberry · Mango

```bash
python3 scripts/export_syrup_production.py
python3 scripts/validate_syrup_spec.py
```

Output: `output/syrup_production/`

### Syrup Product Facts (locked)
- 420mg THC · 5mg per 5mL serving · 84 servings · 4 FL OZ (120mL)

### Documentation
- [Compliance Audit Report](docs/syrup/COMPLIANCE_AUDIT_REPORT.md)
- [Master Label Standard](docs/syrup/MASTER_LABEL_STANDARD.md)
- [Change Log](docs/syrup/CHANGELOG.md)
- [Future Expansion Guide](docs/syrup/FUTURE_EXPANSION_GUIDE.md)

### Illustrator Masters
- `assets/syrup/masters/front_panel_master.svg`
- `assets/syrup/masters/back_panel_master.svg`

---

## Design Principles (all lines)

- **Not a redesign** — refine, validate, productionize
- Matte black · warm off-white · gold/amber accents
- No AI artifacts · no decorative filler · no fruit/cannabis imagery
- Manufacturer data only — no estimated compliance values
