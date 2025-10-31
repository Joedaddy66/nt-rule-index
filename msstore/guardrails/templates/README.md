# Templates for Codex Guardrails Output

This directory contains templates for generating attestation documents.

## Available Templates

### SARIF Template
Located in the main configuration (`codex-config.json`), the SARIF output follows the OASIS SARIF 2.1.0 schema.

### CSV Template
Simple comma-separated values with headers:
- RuleID
- Severity
- Location
- Message
- Timestamp

### XLSX Template
Multi-sheet Excel workbook with:
- Package Inventory
- Security Findings
- Compliance Status
- Quality Metrics

## Customization

To customize output formats:

1. Edit `codex-config.json` emission section
2. Modify field lists for CSV
3. Add/remove sheets for XLSX
4. Adjust SARIF rule definitions

## Usage

Templates are automatically applied during guardrails execution:

```bash
./run-guardrails.sh 1.0.0.0
```

Output files are generated in `../output/` directory.

## Future Templates

Planned additions:
- PDF attestation reports
- HTML dashboards
- JSON compliance manifests
- Markdown summaries

---

**Note**: Template functionality is built into the guardrails scripts. This directory is reserved for future template file storage.
