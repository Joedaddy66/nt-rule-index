# Microsoft Store Release - Quick Start Guide

This guide will help you quickly set up and execute your first Microsoft Store release.

## Prerequisites Checklist

- [ ] Windows 10/11 with Windows SDK installed
- [ ] Code signing certificate (for production)
- [ ] Microsoft Partner Center account
- [ ] Visual assets prepared (logos, icons)
- [ ] FastAPI application ready for packaging

## Quick Release Steps

### 1. Configure Package Metadata (5 minutes)

Edit `msstore/manifest/package-metadata.json`:

```json
{
  "package": {
    "identity": {
      "name": "YourCompany.YourApp",
      "publisher": "CN=YourCompany",
      "version": "1.0.0.0"
    },
    "properties": {
      "displayName": "Your App Name",
      "description": "Your app description"
    }
  }
}
```

### 2. Add Visual Assets (10 minutes)

Place these files in `msstore/manifest/Assets/`:
- `StoreLogo.png` (50x50)
- `Square150x150Logo.png` (150x150)
- `Square44x44Logo.png` (44x44)
- `Wide310x150Logo.png` (310x150)

### 3. Run Guardrails Analysis (2 minutes)

```bash
make msstore-guardrails VERSION=1.0.0.0
```

Review the output in `msstore/guardrails/output/summary.md`.

### 4. Build MSIX Package (5 minutes)

**On Windows:**
```powershell
cd msstore\packaging
.\build-msix.ps1 -Version "1.0.0.0"
```

**On Linux/macOS:**
```bash
make msstore-package VERSION=1.0.0.0
```

### 5. Test Locally (5 minutes)

On Windows:
```powershell
Add-AppxPackage -Path "msstore\packaging\output\NTRuleIndex_1.0.0.0_x64.msix"
```

### 6. Sign Package (For Production) (2 minutes)

```powershell
signtool sign /fd SHA256 /f certificate.pfx /p password output\NTRuleIndex.msix
```

### 7. Submit to Microsoft Store

**Option A: Manual Submission**
1. Go to [Partner Center](https://partner.microsoft.com/dashboard)
2. Upload the MSIX package
3. Complete store listing
4. Submit for certification

**Option B: Automated via GitHub Actions**
1. Configure GitHub Secrets (see below)
2. Push a release tag:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

## GitHub Secrets Configuration

For automated submission, add these secrets to your repository:

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `PARTNER_CENTER_TENANT_ID` | Azure AD Tenant ID | Partner Center → Account settings |
| `PARTNER_CENTER_CLIENT_ID` | Application Client ID | Azure AD app registration |
| `PARTNER_CENTER_CLIENT_SECRET` | Application Secret | Azure AD app registration |
| `PARTNER_CENTER_APP_ID` | Store App ID | Partner Center → Your app |
| `SIGNING_CERTIFICATE` | Base64-encoded PFX | `[Convert]::ToBase64String([IO.File]::ReadAllBytes("cert.pfx"))` |
| `SIGNING_PASSWORD` | Certificate password | Your cert password |

## Troubleshooting

### Build fails with "makeappx.exe not found"
- **Solution**: Install Windows SDK or run on Windows machine

### "Package signature not valid" on installation
- **Solution**: Sign the package or enable Developer Mode in Windows Settings

### Guardrails script fails
- **Solution**: Ensure scripts are executable: `chmod +x msstore/guardrails/run-guardrails.sh`

## Next Steps After First Release

1. Monitor certification status in Partner Center
2. Respond to any certification feedback
3. Plan updates and versioning strategy
4. Set up automated builds for continuous delivery

## Common Workflows

### Update Version
```bash
make msstore-manifest VERSION=1.1.0.0
make msstore-package VERSION=1.1.0.0
```

### Clean and Rebuild
```bash
make msstore-clean
make msstore-package VERSION=1.0.0.0
```

### CI/CD Integration
The workflow at `.github/workflows/msstore-publish.yml` handles:
- Building MSIX package
- Running guardrails
- Signing package
- Submitting to Partner Center
- Creating release artifacts

## Support Resources

- [Complete Documentation](README.md) - Full Microsoft Store scaffold guide
- [Codex Guardrails](../../docs/codex-guardrails.md) - Security and compliance details
- [Packaging Guide](packaging/README.md) - Detailed packaging instructions
- [Microsoft Docs](https://docs.microsoft.com/windows/msix/) - Official MSIX documentation

## Estimated Timeline

| Task | Time Required |
|------|---------------|
| Initial setup (first time) | 30-60 minutes |
| Subsequent builds | 5-10 minutes |
| Certification review | 1-3 business days |
| Store publication | 1-24 hours after approval |

---

**Ready to release?** Start with step 1 above or run `make help` for available commands.
