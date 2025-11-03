# Microsoft Store Release Scaffold

## Overview

This directory contains the complete scaffold for publishing the **RA Longevity NT Rule Index** FastAPI microservice to the Microsoft Store. It includes manifest generation, MSIX bundling, Partner Center integration, and Codex Guardrails for security and compliance attestation.

## 📁 Directory Structure

```
msstore/
├── manifest/                      # Application manifest and metadata
│   ├── app-manifest.xml          # APPX/MSIX manifest
│   ├── package-metadata.json     # Extended metadata (pricing, categories, etc.)
│   └── Assets/                   # Logos and visual assets (to be added)
│       ├── StoreLogo.png
│       ├── Square150x150Logo.png
│       ├── Square44x44Logo.png
│       └── Wide310x150Logo.png
├── packaging/                     # Build and packaging scripts
│   ├── README.md                 # Detailed packaging documentation
│   ├── build-msix.ps1            # PowerShell build script
│   ├── build-msix.sh             # Bash build script (Linux/WSL)
│   ├── bundle-config.xml         # Multi-architecture bundle config
│   ├── output/                   # Build output directory
│   └── bundle/                   # Bundle output directory
└── guardrails/                    # Codex security and compliance
    ├── codex-config.json         # Guardrails configuration
    ├── run-guardrails.ps1        # PowerShell guardrails script
    ├── run-guardrails.sh         # Bash guardrails script
    └── output/                   # Attestation files (SARIF/CSV/XLSX)
        ├── analysis.sarif
        ├── metrics.csv
        ├── inventory.xlsx
        └── summary.md
```

## 🚀 Quick Start

### Prerequisites

- **Windows**: Windows 10/11 with Windows SDK 10.0.17763.0+
- **Linux/macOS**: WSL with Windows SDK or use scripts to prepare config
- **Tools**: PowerShell 5.1+ or Bash, Python 3.11+, Git

### Option 1: Using Makefile (Recommended)

```bash
# Build complete MSIX package with attestation
make msstore-package VERSION=1.0.0.0

# Run individual steps
make msstore-manifest          # Update manifest
make msstore-guardrails        # Run security checks
make msstore-build             # Build MSIX
make msstore-clean             # Clean artifacts
```

### Option 2: Using Build Scripts

**Windows (PowerShell):**
```powershell
cd msstore\packaging
.\build-msix.ps1 -Version "1.0.0.0"
```

**Linux/WSL/macOS (Bash):**
```bash
cd msstore/packaging
./build-msix.sh 1.0.0.0
```

### Option 3: GitHub Actions (Automated)

Push a tag to trigger automated build and submission:

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Or manually trigger the workflow:
1. Go to Actions → Microsoft Store Publish
2. Click "Run workflow"
3. Enter version and environment

## 📦 Package Configuration

### Manifest Metadata

Edit `manifest/package-metadata.json`:

```json
{
  "package": {
    "identity": {
      "name": "RALongevity.NTRuleIndex",
      "publisher": "CN=RALongevity",
      "version": "1.0.0.0"
    },
    "properties": {
      "displayName": "RA Longevity - NT Rule Index",
      "description": "FastAPI microservice for Number Theory...",
    },
    "pricing": {
      "model": "free",  // or "paid"
      "basePrice": "0.00"
    }
  }
}
```

### Visual Assets

Place the following in `manifest/Assets/`:

- **StoreLogo.png**: 50x50 px (Store listing)
- **Square150x150Logo.png**: 150x150 px (Medium tile)
- **Square44x44Logo.png**: 44x44 px (App list icon)
- **Wide310x150Logo.png**: 310x150 px (Wide tile)

Use transparent backgrounds and follow [Microsoft's design guidelines](https://docs.microsoft.com/windows/apps/design/style/app-icons-and-logos).

## 🛡️ Codex Guardrails

### Running Security Analysis

```bash
# Run guardrails independently
cd msstore/guardrails
./run-guardrails.sh 1.0.0.0

# Review output
cat output/summary.md
```

### Output Files

- **SARIF** (`analysis.sarif`): Machine-readable security findings
- **CSV** (`metrics.csv`): Compliance metrics for reporting
- **XLSX** (`inventory.xlsx`): Complete package inventory with findings
- **Summary** (`summary.md`): Executive summary and recommendations

### Configuration

Customize security rules in `guardrails/codex-config.json`:

```json
{
  "guardrails": {
    "security": {
      "enabled": true,
      "rules": [
        {
          "id": "SEC-001",
          "name": "NoHardcodedSecrets",
          "severity": "error"
        }
      ]
    }
  }
}
```

See [Codex Guardrails Specification](../../docs/codex-guardrails.md) for details.

## 🔐 Code Signing

### Development/Testing

For local testing, signing is optional. Windows will show "Unknown publisher" warning.

### Production Release

Required for Microsoft Store submission:

1. **Obtain a certificate**:
   - Purchase from a trusted CA (DigiCert, GlobalSign, etc.)
   - Or use Microsoft Store-provided certificate

2. **Sign during build**:
   ```powershell
   .\build-msix.ps1 -Version "1.0.0.0" -Sign -CertPath "cert.pfx" -CertPassword "pass"
   ```

3. **Or sign separately**:
   ```powershell
   signtool sign /fd SHA256 /f cert.pfx /p password output\NTRuleIndex.msix
   ```

### GitHub Actions Signing

Store certificate as base64 in GitHub Secrets:

```powershell
# Convert certificate to base64
$bytes = [System.IO.File]::ReadAllBytes("cert.pfx")
$base64 = [System.Convert]::ToBase64String($bytes)
echo $base64
```

Add to repository secrets:
- `SIGNING_CERTIFICATE`: Base64-encoded certificate
- `SIGNING_PASSWORD`: Certificate password

## 📤 Submission to Partner Center

### Prerequisites

1. **Partner Center Account**: [Register here](https://partner.microsoft.com/dashboard)
2. **App Reservation**: Reserve your app name
3. **API Credentials**: Create Azure AD app for automated submission

### Manual Submission

1. Login to [Partner Center](https://partner.microsoft.com/dashboard)
2. Navigate to "Apps and games" → "New app"
3. Upload MSIX package from `packaging/output/`
4. Complete store listing (description, screenshots, etc.)
5. Upload attestation bundle from `guardrails/output/`
6. Submit for certification

### Automated Submission (GitHub Actions)

Configure GitHub Secrets:
- `PARTNER_CENTER_TENANT_ID`
- `PARTNER_CENTER_CLIENT_ID`
- `PARTNER_CENTER_CLIENT_SECRET`
- `PARTNER_CENTER_APP_ID`

The workflow will automatically submit on release.

See [GitHub workflow documentation](.github/workflows/msstore-publish.yml) for details.

## 🧪 Testing

### Local Installation

```powershell
# Install package
Add-AppxPackage -Path "msstore\packaging\output\NTRuleIndex_1.0.0.0_x64.msix"

# Verify installation
Get-AppxPackage -Name "RALongevity.NTRuleIndex"

# Launch app
# (Method depends on your FastAPI service startup configuration)

# Uninstall
Remove-AppxPackage -Package "RALongevity.NTRuleIndex_1.0.0.0_x64__<publisher_hash>"
```

### Troubleshooting Installation

**Error: "App package signature not valid"**
- Solution: Sign the package or enable developer mode

**Error: "Deployment failed"**
- Check Event Viewer → Applications and Services Logs → Microsoft → Windows → AppXDeployment-Server
- Verify all dependencies are listed in manifest

## 🔄 Version Management

Update version in three locations:

1. **Manifest**: `manifest/app-manifest.xml`
   ```xml
   <Identity Version="1.0.0.0" />
   ```

2. **Metadata**: `manifest/package-metadata.json`
   ```json
   "version": "1.0.0.0"
   ```

3. **Git Tag**: `v1.0.0`
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   ```

Or use the build script which updates all automatically:
```bash
make msstore-manifest VERSION=1.2.3.0
```

## 📋 Checklist for First Release

- [ ] Configure manifest metadata (`manifest/package-metadata.json`)
- [ ] Add visual assets to `manifest/Assets/`
- [ ] Test build script locally
- [ ] Run guardrails and review output
- [ ] Build MSIX package
- [ ] Test installation on clean Windows system
- [ ] Obtain code signing certificate (for production)
- [ ] Sign package
- [ ] Create Partner Center account and reserve app name
- [ ] Configure GitHub secrets for automated submission
- [ ] Create first release tag
- [ ] Verify automated workflow runs successfully
- [ ] Complete store listing in Partner Center
- [ ] Submit for certification

## 📚 Documentation

- **Packaging Details**: [packaging/README.md](packaging/README.md)
- **Codex Guardrails**: [docs/codex-guardrails.md](../../docs/codex-guardrails.md)
- **GitHub Workflow**: [.github/workflows/msstore-publish.yml](../../.github/workflows/msstore-publish.yml)
- **Makefile Targets**: Run `make help` for available commands

## 🔗 Resources

### Microsoft Documentation
- [MSIX Package Format](https://docs.microsoft.com/windows/msix/)
- [App Manifest Schema](https://docs.microsoft.com/uwp/schemas/appxpackage/appx-package-manifest)
- [Partner Center Submission API](https://docs.microsoft.com/windows/uwp/monetize/create-and-manage-submissions-using-windows-store-services)
- [Windows App Certification Kit](https://developer.microsoft.com/windows/downloads/app-certification-kit/)

### Tools
- [MSIX Packaging Tool](https://www.microsoft.com/store/productId/9N5LW3JBCXKF)
- [Windows SDK](https://developer.microsoft.com/windows/downloads/windows-sdk/)
- [StoreBroker PowerShell Module](https://github.com/Microsoft/StoreBroker)

### Standards
- [SARIF Specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)
- [NIST Guidelines](https://www.nist.gov/cyberframework)
- [CIS Controls](https://www.cisecurity.org/controls)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## 🐛 Troubleshooting

### Build Issues

**"makeappx.exe not found"**
- Install Windows SDK
- Add SDK bin directory to PATH
- Or use Windows machine for building

**"Version format invalid"**
- Use format: Major.Minor.Build.Revision (e.g., 1.0.0.0)
- All components must be numeric

### Submission Issues

**"Package validation failed"**
- Run Windows App Certification Kit (WACK)
- Review manifest for missing fields
- Ensure all capabilities are justified

**"Authentication failed with Partner Center"**
- Verify Azure AD app registration
- Check client ID and secret
- Ensure app has necessary permissions

## 📞 Support

For issues with this scaffold:
1. Check [troubleshooting section](#-troubleshooting) above
2. Review [packaging documentation](packaging/README.md)
3. Consult [Microsoft Store docs](https://docs.microsoft.com/windows/apps/publish/)
4. Open issue in repository with:
   - Build logs
   - Error messages
   - Environment details (OS, SDK version)

## 📝 License

This scaffold is part of the RA Longevity NT Rule Index project.
See [LICENSE](../../LICENSE) for details.

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-31  
**Maintained By**: RA Longevity Team
