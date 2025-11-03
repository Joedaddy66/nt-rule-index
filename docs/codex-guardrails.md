# Codex Guardrails Specification

## Overview

The Codex Guardrails framework provides automated security, compliance, and quality checks for the RA Longevity NT Rule Index Microsoft Store submission. It ensures that packages meet security standards, comply with regulations, and maintain high quality before distribution.

## Framework Components

### 1. Security Analysis

#### Secret Detection (SEC-001)
- **Severity**: Error
- **Description**: Scans code and configuration files for hardcoded secrets, API keys, passwords, and credentials
- **Detection Patterns**:
  - Password variables and constants
  - API key patterns
  - AWS/Azure/GCP credentials
  - Private keys and certificates
  - Authentication tokens

#### Secure Connections (SEC-002)
- **Severity**: Warning
- **Description**: Ensures all network connections use TLS/SSL encryption
- **Checks**:
  - HTTP URLs should be HTTPS
  - Database connections use SSL
  - API endpoints are secured
  - Certificate validation is enabled

#### Input Validation (SEC-003)
- **Severity**: Error
- **Description**: Validates that all user inputs are properly sanitized
- **Checks**:
  - SQL injection prevention
  - XSS attack prevention
  - Path traversal protection
  - Command injection prevention

### 2. Compliance Checks

#### NIST Compliance
- **Standards**: NIST SP 800-53, 800-171
- **Controls**:
  - Access control (AC)
  - Audit and accountability (AU)
  - Identification and authentication (IA)
  - System and communications protection (SC)

#### CIS Controls
- **Standards**: CIS Critical Security Controls
- **Focus Areas**:
  - Inventory and control of software assets
  - Secure configuration
  - Data protection
  - Controlled access based on need to know

#### OWASP Guidelines
- **Standards**: OWASP Top 10
- **Checks**:
  - Injection flaws
  - Broken authentication
  - Sensitive data exposure
  - Security misconfiguration
  - Cross-site scripting (XSS)

### 3. Quality Metrics

#### Code Complexity
- **Maximum Cyclomatic Complexity**: 10
- **Maximum Nesting Depth**: 4
- **Rationale**: Maintains readability and testability

#### Test Coverage
- **Minimum Line Coverage**: 80%
- **Minimum Branch Coverage**: 75%
- **Exception**: Infrastructure and scaffold code

#### Documentation
- **Requirements**:
  - Public APIs documented
  - Configuration options explained
  - Usage examples provided
  - Architecture decisions recorded

## Emission Formats

### SARIF (Static Analysis Results Interchange Format)

**Purpose**: Machine-readable security findings

**Schema Version**: 2.1.0

**Contents**:
- Tool information and version
- Rule definitions with severity levels
- Analysis results with locations
- Code flows for complex issues
- Remediation guidance

**Example**:
```json
{
  "version": "2.1.0",
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "Codex Guardrails",
          "version": "1.0"
        }
      },
      "results": [...]
    }
  ]
}
```

**Use Cases**:
- Integration with CI/CD pipelines
- GitHub Security tab
- IDE security extensions
- Security dashboards

### CSV (Comma-Separated Values)

**Purpose**: Human-readable metrics and findings

**Columns**:
- RuleID: Unique identifier for the rule
- Severity: error, warning, info, note
- Location: File path and line number
- Message: Human-readable description
- Timestamp: ISO 8601 format

**Example**:
```csv
RuleID,Severity,Location,Message,Timestamp
SEC-001,info,Package structure,No hardcoded secrets detected,2025-10-31T18:00:00Z
SEC-002,info,Network configuration,TLS/SSL configuration verified,2025-10-31T18:00:00Z
```

**Use Cases**:
- Quick review in spreadsheet software
- Compliance reporting
- Historical tracking
- Management dashboards

### XLSX (Excel Workbook)

**Purpose**: Comprehensive attestation document

**Sheets**:

1. **Package Inventory**
   - Component name
   - Version number
   - License type
   - Known vulnerabilities
   - Dependency tree

2. **Security Findings**
   - Rule ID and name
   - Severity level
   - File location
   - Line numbers
   - Detailed description
   - Remediation steps

3. **Compliance Status**
   - Standard name (NIST, CIS, OWASP)
   - Control ID
   - Status (Pass/Fail/N/A)
   - Evidence location
   - Last assessment date

4. **Quality Metrics**
   - Code complexity scores
   - Test coverage percentages
   - Documentation completeness
   - Technical debt indicators

**Formatting**:
- Color-coded severity (red=error, yellow=warning, green=pass)
- Conditional formatting for metrics
- Charts and graphs for visualization
- Hyperlinks to detailed documentation

**Use Cases**:
- Compliance audits
- Management reviews
- Partner Center submissions
- Historical record keeping

## Attestation Bundle

### Contents

The attestation bundle is a ZIP archive containing:

```
attestation-bundle-<version>.zip
├── analysis.sarif          # Security analysis results
├── metrics.csv             # Compliance metrics
├── inventory.xlsx          # Complete package inventory
├── summary.md              # Executive summary
└── package-metadata.json   # Package configuration
```

### Generation

Automatically created during the build process:

```powershell
# PowerShell
.\msstore\packaging\build-msix.ps1 -Version "1.0.0.0"

# Bash
./msstore/packaging/build-msix.sh 1.0.0.0
```

### Usage

1. **Microsoft Partner Center**: Upload with MSIX package
2. **Internal Review**: Share with security and compliance teams
3. **Audit Trail**: Archive for regulatory requirements
4. **Customer Transparency**: Optional disclosure for enterprise customers

## Integration Points

### Build Pipeline

```yaml
# GitHub Actions
- name: Run Codex Guardrails
  run: |
    cd msstore/guardrails
    ./run-guardrails.sh ${{ env.VERSION }}

- name: Upload Attestation
  uses: actions/upload-artifact@v4
  with:
    name: attestation-bundle
    path: msstore/guardrails/output/
```

### Makefile

```bash
# Run guardrails
make msstore-guardrails VERSION=1.0.0.0

# Complete package with attestation
make msstore-package VERSION=1.0.0.0
```

### Manual Execution

```bash
# Linux/macOS/WSL
cd msstore/guardrails
./run-guardrails.sh 1.0.0.0

# Windows PowerShell
cd msstore\guardrails
.\run-guardrails.ps1 -Version "1.0.0.0"
```

## Configuration

### Customization

Edit `msstore/guardrails/codex-config.json`:

```json
{
  "guardrails": {
    "security": {
      "enabled": true,
      "rules": [...]
    },
    "compliance": {
      "enabled": true,
      "standards": ["NIST", "CIS", "OWASP"]
    }
  }
}
```

### Adding Custom Rules

```json
{
  "id": "CUSTOM-001",
  "name": "CustomRuleName",
  "severity": "warning",
  "description": "Custom rule description",
  "pattern": "regex-pattern-here"
}
```

## Troubleshooting

### Issue: SARIF validation fails

**Solution**: Ensure JSON is well-formed and follows SARIF 2.1.0 schema

### Issue: CSV encoding problems

**Solution**: Use UTF-8 encoding for all output files

### Issue: XLSX generation requires additional tools

**Solution**: 
- Windows: Install Excel or OpenXML SDK
- Linux: Install Python `openpyxl` library
- Fallback: Text-based placeholder is created automatically

### Issue: Large attestation bundle size

**Solution**: 
- Exclude test data from scans
- Compress with maximum compression
- Archive older versions separately

## Best Practices

1. **Run guardrails before every submission**
2. **Review all findings, even "info" level**
3. **Archive attestation bundles with releases**
4. **Update rules for new security threats**
5. **Document false positives with justification**
6. **Integrate with code review process**
7. **Train team on interpreting results**

## Versioning

Guardrails framework follows semantic versioning:
- **Major**: Breaking changes to output format
- **Minor**: New rules or features
- **Patch**: Bug fixes and improvements

Current version: **1.0.0**

## Support

For issues with Codex Guardrails:
1. Check configuration in `codex-config.json`
2. Review output in `guardrails/output/summary.md`
3. Consult this specification
4. Open issue in repository with logs

## Future Enhancements

- [ ] Integration with external security scanners
- [ ] Machine learning-based anomaly detection
- [ ] Real-time monitoring dashboard
- [ ] Automated remediation suggestions
- [ ] Integration with issue tracking systems
- [ ] Custom policy templates by industry

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-31  
**Maintained By**: RA Longevity Team
