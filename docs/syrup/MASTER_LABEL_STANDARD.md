# ALTERNATIVE™ Syrup — Master Label Standard

## System Version
Syrup Master System v1.0

## Canvas (Identical for Every SKU)

| Spec | Value |
|------|-------|
| Panel (each) | 52mm × 90mm |
| Combined (front + back) | 104mm × 90mm |
| Bleed | 3.175mm all sides |
| Safe zone | 3mm inset |
| DPI | 300 |
| Color | CMYK only |

## Locked Front Panel Hierarchy

```
1. ALTERNATIVE™
2. [FLAVOR NAME]
3. 420 MG THC
4. 5 MG THC PER SERVING
5. 84 SERVINGS
6. 4 FL OZ (120mL)
   + Statement of Identity (secondary)
```

**Do not alter order.** Adjust spacing only.

## Locked Back Panel Sections

```
QR + Website
Barcode (protected zone)
WARNINGS
SUPPLEMENT FACTS (left)
INGREDIENTS (right)
DIRECTIONS
RESPONSIBLE PARTY
LOT / BEST BY
```

## Typography Scale (pt)

| Element | Size |
|---------|------|
| Brand name | 14.0 |
| Flavor | 11.0 |
| 420 MG THC | 13.0 |
| 5 MG per serving | 8.0 |
| Servings | 7.5 |
| Net contents | 7.0 |
| Panel headings | 6.5 |
| Panel body | 5.5 |

## Color Rules

- **Matte black** — background
- **Warm off-white** — secondary text, supplement panel body
- **Accent (gold/berry/citrus)** — brand name, THC per serving only
- No gradients, chrome, metallic, glow

## Scalability

| Change | Method |
|--------|--------|
| New flavor | Add entry to `config/syrup/flavors.yaml` + `data/compliance/syrup/flavors/{id}.json` |
| New strength | Update `config/syrup/brand.yaml` product block |
| New bottle size | Update canvas dimensions in brand.yaml — grid logic unchanged |
| State warnings | Add to compliance JSON `state_warnings` array |

## File Naming

```
alternative_syrup_{flavor_id}.pdf
```

Examples: `alternative_syrup_grape.pdf`
