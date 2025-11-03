# MSIX Packaging Configuration for Microsoft Store

## Overview
This configuration bundles the RA Longevity FastAPI microservice into an MSIX package for Microsoft Store distribution.

## Prerequisites
- Windows SDK 10.0.17763.0 or higher
- MSIX Packaging Tool or makeappx.exe
- Code signing certificate (for production)
- Partner Center account and credentials

## Package Structure
```
msstore/
├── manifest/
│   ├── app-manifest.xml          # APPX manifest
│   ├── package-metadata.json      # Extended metadata with Codex info
│   └── Assets/                    # Logo and visual assets (placeholder)
├── packaging/
│   ├── build-msix.ps1            # PowerShell build script
│   ├── build-msix.sh             # Bash build script (WSL/Linux)
│   ├── bundle-config.xml         # Bundle configuration
│   └── output/                   # Build output directory
└── guardrails/
    ├── codex-config.json         # Codex guardrails configuration
    └── templates/                # SARIF/CSV/XLSX templates
```

## Build Process

### Step 1: Prepare Application Files
Ensure your FastAPI service and all dependencies are ready:
- Application executable or entry point
- Required DLLs and dependencies
- Configuration files
- Assets (icons, images)

### Step 2: Build MSIX Package
```powershell
# Windows (PowerShell)
cd msstore/packaging
.\build-msix.ps1 -Version "1.0.0.0"

# Or using makeappx directly
makeappx pack /d "..\manifest" /p "output\NTRuleIndex.msix"
```

```bash
# Linux/WSL
cd msstore/packaging
./build-msix.sh 1.0.0.0
```

### Step 3: Sign Package (Production Only)
```powershell
signtool sign /fd SHA256 /f certificate.pfx /p password output\NTRuleIndex.msix
```

### Step 4: Create Bundle (Optional - for multiple architectures)
```powershell
makeappx bundle /d "output" /p "bundle\NTRuleIndex.msixbundle"
```

## Codex Guardrails Integration

The package includes Codex guardrails for compliance and security:

1. **SARIF Emission**: Security findings in SARIF format
2. **CSV Reports**: Compliance metrics and attestation data
3. **XLSX Manifests**: Human-readable package inventory

These are generated automatically during the build process and included in the attestation bundle.

## Testing

### Local Installation
```powershell
# Install locally for testing
Add-AppxPackage -Path "output\NTRuleIndex.msix"

# Test the application
# Access at: ms-windows-store://pdp/?productid=<your-product-id>

# Uninstall
Remove-AppxPackage -Package "RALongevity.NTRuleIndex_1.0.0.0_x64__<hash>"
```

## Submission to Partner Center

See the GitHub Action workflow at `.github/workflows/msstore-publish.yml` for automated submission.

Manual submission steps:
1. Login to [Partner Center](https://partner.microsoft.com/dashboard)
2. Navigate to Apps and games > Create new app
3. Upload the MSIX package or bundle
4. Complete store listing details
5. Submit for certification

## Version Management

Update version in three places:
1. `manifest/app-manifest.xml` - `Identity/@Version`
2. `manifest/package-metadata.json` - `package.identity.version`
3. GitHub release tag - `v1.0.0`

## Pricing Configuration

Current: **Free**
To change pricing, update `manifest/package-metadata.json`:
```json
{
  "pricing": {
    "model": "paid",
    "basePrice": "4.99",
    "currency": "USD"
  }
}
```

## Troubleshooting

### Package Validation Errors
- Verify manifest schema compliance
- Check all asset files exist
- Ensure version format is correct (Major.Minor.Build.Revision)

### Signing Issues
- Certificate must be trusted on target system
- Verify certificate hasn't expired
- Use SHA256 signing algorithm

### Runtime Issues
- Check dependencies are included
- Verify capability declarations match requirements
- Test on clean Windows installation

## References
- [MSIX Documentation](https://docs.microsoft.com/windows/msix/)
- [Partner Center Submission Guide](https://docs.microsoft.com/windows/uwp/publish/)
- [Codex Guardrails Specification](../../docs/codex-guardrails.md)
