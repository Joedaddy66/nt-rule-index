# NT Rule Index
Local-first repository linking Drive artifacts to **Number-Theory Rule Packs** and publishing a MkDocs site.

## Quick start

### Documentation
- Build index: `python scripts/build_index.py`
- Install docs deps: `pip install -r requirements.txt`
- Serve locally: `mkdocs serve` → http://127.0.0.1:8000

### Microsoft Store Release
- Build MSIX package: `make msstore-package VERSION=1.0.0.0`
- Run guardrails: `make msstore-guardrails`
- See [Microsoft Store Release Scaffold](msstore/README.md) for details

## Features

### Documentation Site
- MkDocs-based documentation with Material theme
- Automated index generation from CSV data
- GitHub Pages deployment

### Microsoft Store Scaffold
- **Manifest Generation**: APPX/MSIX manifest with metadata
- **MSIX Packaging**: Build scripts for Windows Store distribution
- **Codex Guardrails**: Security and compliance attestation (SARIF/CSV/XLSX)
- **CI/CD Integration**: GitHub Actions workflow for automated submission
- **Partner Center**: Automated submission to Microsoft Store

See [msstore/README.md](msstore/README.md) for comprehensive Microsoft Store deployment documentation.
