# AGENTS.md

## Cursor Cloud specific instructions

### Repository layout (important)
- The `main` branch contains only `README.md` and `.gitattributes` — **no application code**. The actual product code lives on feature branches (e.g. `cursor/manufacturing-readiness-971b`, which is the most complete superset). If `main` is checked out and you need to run the product, check out / merge a feature branch first.
- This is a Python CLI/batch toolchain (`ALT-Label-System`) that renders print-ready product label PDFs. There are **no long-running services, servers, databases, or network/secret dependencies** — it is pure file-in (YAML/JSON config under `config/` and `data/`) → file-out (PDFs under the git-ignored `output/`).

### Environment
- Python 3.12 (3.10+ required; the code uses `X | None` annotations evaluated at runtime).
- Dependencies are declared in `requirements.txt` and install to the user site (`~/.local`) via `pip install -r requirements.txt`. The startup update script runs this automatically when `requirements.txt` is present.
- **Ghostscript (`gs`) is optional** — only used for PDF/X-1a prepress export (`src/alt_label/pdfx_export.py`). It is not installed by default and the code degrades gracefully (`shutil.which("gs")`) when absent; normal PDF output does not need it.

### Running / building / testing
- Standard commands are documented in `README.md` (feature branch). Two product lines:
  - Cans: `python3 scripts/export_production.py` → `output/production_v2/` (8 PDFs)
  - Syrup: `python3 scripts/export_syrup_production.py` → `output/syrup_production/` (4 PDFs)
- Scripts self-bootstrap `sys.path` to `src/`, so no editable install or venv activation is needed — run from the repo root.
- **There is no lint config and no pytest/test suite.** The de-facto test gates are the validation scripts, which print a readiness score and exit non-zero on failure:
  - `python3 scripts/validate_spec.py` (cans)
  - `python3 scripts/validate_syrup_spec.py` (syrup)
  - For a quick syntax check, `python3 -m compileall -q src scripts`.
- Optional audit/report scripts: `scripts/manufacturing_readiness_audit.py`, `scripts/launch_readiness_audit.py`, `scripts/launch_war_room_audit.py`.
