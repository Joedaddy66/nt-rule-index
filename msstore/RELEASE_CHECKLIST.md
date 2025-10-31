# Microsoft Store Release Checklist

Use this checklist to ensure all requirements are met before submitting to the Microsoft Store.

## Pre-Release Checklist

### 1. Application Preparation
- [ ] FastAPI application is production-ready
- [ ] All dependencies are documented
- [ ] Application tested on Windows 10 and Windows 11
- [ ] Error handling and logging implemented
- [ ] Configuration management in place
- [ ] Health check endpoints functional
- [ ] API documentation complete

### 2. Package Configuration
- [ ] **Identity configured** in `msstore/manifest/app-manifest.xml`
  - [ ] Name (e.g., "RALongevity.NTRuleIndex")
  - [ ] Publisher (e.g., "CN=RALongevity")
  - [ ] Version (format: x.x.x.x)
  
- [ ] **Package metadata** complete in `msstore/manifest/package-metadata.json`
  - [ ] Display name
  - [ ] Description (compelling and clear)
  - [ ] Pricing model (free/paid)
  - [ ] Categories selected
  - [ ] Keywords/tags defined

- [ ] **Capabilities** declared in manifest
  - [ ] internetClient (if network access needed)
  - [ ] runFullTrust (for FastAPI service)
  - [ ] Other required capabilities

### 3. Visual Assets
- [ ] **Store Logo** (50x50 px) - `msstore/manifest/Assets/StoreLogo.png`
- [ ] **Square 150x150** (150x150 px) - `msstore/manifest/Assets/Square150x150Logo.png`
- [ ] **Square 44x44** (44x44 px) - `msstore/manifest/Assets/Square44x44Logo.png`
- [ ] **Wide 310x150** (310x150 px) - `msstore/manifest/Assets/Wide310x150Logo.png`
- [ ] All assets use transparent backgrounds
- [ ] Assets follow Microsoft design guidelines
- [ ] High-resolution variants provided (@2x, @4x)

### 4. Security & Compliance
- [ ] **Codex Guardrails** executed successfully
  ```bash
  make msstore-guardrails VERSION=x.x.x.x
  ```
- [ ] SARIF analysis reviewed (`msstore/guardrails/output/analysis.sarif`)
- [ ] No critical security findings
- [ ] CSV metrics generated (`msstore/guardrails/output/metrics.csv`)
- [ ] XLSX inventory complete (`msstore/guardrails/output/inventory.xlsx`)
- [ ] Summary report reviewed (`msstore/guardrails/output/summary.md`)

### 5. Code Signing
- [ ] **Development Certificate** obtained (for testing)
  - OR -
- [ ] **Production Certificate** obtained from trusted CA
  - [ ] Certificate valid for at least 12 months
  - [ ] Certificate includes code signing usage
  - [ ] Certificate password secured
  
- [ ] Certificate stored securely as GitHub Secret (if using CI/CD)
  - [ ] `SIGNING_CERTIFICATE` (base64-encoded)
  - [ ] `SIGNING_PASSWORD`

### 6. Partner Center Setup
- [ ] **Microsoft Partner Center account** created
  - [ ] Account verified and activated
  - [ ] Payment information configured (if paid app)
  - [ ] Tax information completed
  
- [ ] **App reserved** in Partner Center
  - [ ] App name available and reserved
  - [ ] App ID obtained
  
- [ ] **Azure AD app** registered (for automated submission)
  - [ ] `PARTNER_CENTER_TENANT_ID` documented
  - [ ] `PARTNER_CENTER_CLIENT_ID` documented
  - [ ] `PARTNER_CENTER_CLIENT_SECRET` created
  - [ ] App has Partner Center API permissions

### 7. Store Listing Content
- [ ] **App description**
  - [ ] Compelling introduction
  - [ ] Key features listed
  - [ ] Use cases explained
  - [ ] Minimum 200 characters
  
- [ ] **Screenshots** (at least 1, recommended 4-5)
  - [ ] 1366 x 768 or higher
  - [ ] Shows key features
  - [ ] Professional quality
  
- [ ] **Privacy policy** (if app collects data)
  - [ ] URL accessible
  - [ ] Complies with GDPR/privacy laws
  
- [ ] **Support contact**
  - [ ] Email address
  - [ ] Support website (optional)

### 8. Build & Package
- [ ] **Version number** updated consistently
  - [ ] `msstore/manifest/app-manifest.xml`
  - [ ] `msstore/manifest/package-metadata.json`
  - [ ] Git tag (e.g., v1.0.0)
  
- [ ] **MSIX package built** successfully
  ```powershell
  cd msstore\packaging
  .\build-msix.ps1 -Version "x.x.x.x"
  ```
  
- [ ] **Package signed** (for production)
  ```powershell
  signtool sign /fd SHA256 /f cert.pfx /p password output\*.msix
  ```
  
- [ ] **Attestation bundle** created
  - [ ] All guardrails outputs included
  - [ ] Package metadata included

### 9. Testing
- [ ] **Local installation test**
  ```powershell
  Add-AppxPackage -Path "path\to\package.msix"
  ```
  - [ ] Installs without errors
  - [ ] Application launches successfully
  - [ ] Core functionality works
  - [ ] No runtime errors
  
- [ ] **Windows App Certification Kit** (WACK) passed
  ```powershell
  # Run WACK
  appcert.exe reset
  appcert.exe test -appxpackagepath "path\to\package.msix" -reportoutputpath "wack-report.xml"
  ```
  - [ ] All tests passed
  - [ ] No crashes detected
  - [ ] Performance requirements met
  
- [ ] **Different Windows versions tested**
  - [ ] Windows 10 (minimum version)
  - [ ] Windows 11
  
- [ ] **Clean installation test**
  - [ ] Tested on fresh Windows installation
  - [ ] All dependencies available
  - [ ] No missing system components

### 10. Documentation
- [ ] **README.md** updated
  - [ ] Installation instructions
  - [ ] Usage examples
  - [ ] API documentation
  
- [ ] **Release notes** prepared
  - [ ] New features listed
  - [ ] Bug fixes documented
  - [ ] Breaking changes noted
  
- [ ] **User guide** available
  - [ ] Getting started
  - [ ] Configuration options
  - [ ] Troubleshooting section

### 11. CI/CD Setup (Optional but Recommended)
- [ ] **GitHub Secrets** configured
  - [ ] `PARTNER_CENTER_TENANT_ID`
  - [ ] `PARTNER_CENTER_CLIENT_ID`
  - [ ] `PARTNER_CENTER_CLIENT_SECRET`
  - [ ] `PARTNER_CENTER_APP_ID`
  - [ ] `SIGNING_CERTIFICATE`
  - [ ] `SIGNING_PASSWORD`
  
- [ ] **Workflow tested**
  - [ ] Manual workflow trigger works
  - [ ] Release tag trigger works
  - [ ] Build succeeds
  - [ ] Artifacts uploaded
  
- [ ] **Notifications configured**
  - [ ] Build status alerts
  - [ ] Submission status tracking

### 12. Legal & Compliance
- [ ] **License** appropriate for distribution
  - [ ] Open source license compatible with Microsoft Store
  - OR
  - [ ] Proprietary license terms acceptable
  
- [ ] **Third-party licenses** acknowledged
  - [ ] All dependencies documented
  - [ ] License files included
  
- [ ] **Terms of service** prepared (if applicable)
- [ ] **Age rating** determined
  - [ ] Content reviewed
  - [ ] Appropriate rating selected

## Submission Checklist

### 1. Pre-Submission
- [ ] All items in Pre-Release Checklist completed
- [ ] Final testing completed
- [ ] All documentation reviewed
- [ ] Team approval obtained

### 2. Submission Process
- [ ] Login to [Partner Center](https://partner.microsoft.com/dashboard)
- [ ] Navigate to app submission
- [ ] Upload MSIX package
- [ ] Upload attestation bundle (in notes/files section)
- [ ] Complete all store listing fields
- [ ] Upload screenshots and assets
- [ ] Set pricing and availability
- [ ] Select markets/regions
- [ ] Configure age ratings
- [ ] Submit for certification

### 3. Post-Submission
- [ ] **Certification tracking**
  - [ ] Monitor certification status
  - [ ] Respond to feedback within 24 hours
  - [ ] Address any issues found
  
- [ ] **Publication monitoring**
  - [ ] Verify app appears in store
  - [ ] Test store listing page
  - [ ] Check download functionality
  
- [ ] **User feedback monitoring**
  - [ ] Watch for initial reviews
  - [ ] Respond to user questions
  - [ ] Track reported issues

## Update Checklist (For Subsequent Releases)

- [ ] Version number incremented
- [ ] Release notes documented
- [ ] Breaking changes communicated
- [ ] Guardrails executed for new version
- [ ] Package rebuilt and signed
- [ ] Testing completed
- [ ] Submission notes explain changes
- [ ] Update timeline communicated to users

## Emergency Rollback Checklist

If critical issues are discovered after release:

- [ ] Identify the issue and impact
- [ ] Prepare fix or rollback plan
- [ ] Submit hotfix version or revert to previous
- [ ] Notify users through store listing
- [ ] Update documentation
- [ ] Post-mortem analysis

## Automation Status

Track automation of release process:

| Task | Manual | Automated | Notes |
|------|--------|-----------|-------|
| Guardrails | ⬜ | ☑️ | Via `make msstore-guardrails` |
| MSIX Build | ⬜ | ☑️ | Via `make msstore-build` |
| Package Signing | ☑️ | ☑️ | Manual cert or GitHub Action |
| Partner Center Submission | ☑️ | ☑️ | Manual or GitHub Action |
| Testing | ☑️ | ⬜ | Manual WACK execution |
| Documentation | ☑️ | ⬜ | Manual updates |

## Timeline Estimates

| Phase | Time Required |
|-------|---------------|
| Initial setup (first release) | 2-4 hours |
| Package preparation | 30 minutes |
| Testing | 1-2 hours |
| Submission | 30 minutes |
| Microsoft certification | 1-3 business days |
| Store publication | 1-24 hours |
| **Total (first release)** | **4-7 days** |
| **Subsequent releases** | **2-5 days** |

## Resources

- [Microsoft Store Policies](https://docs.microsoft.com/windows/uwp/publish/store-policies)
- [App Certification Requirements](https://docs.microsoft.com/windows/uwp/publish/the-app-certification-process)
- [MSIX Packaging](https://docs.microsoft.com/windows/msix/)
- [Partner Center Guide](https://docs.microsoft.com/windows/uwp/publish/)

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-31  
**Next Review**: Before each major release
