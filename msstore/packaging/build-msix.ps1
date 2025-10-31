# PowerShell Script for Building MSIX Package
# Usage: .\build-msix.ps1 -Version "1.0.0.0" [-Sign]

param(
    [Parameter(Mandatory=$true)]
    [string]$Version,
    
    [Parameter(Mandatory=$false)]
    [switch]$Sign = $false,
    
    [Parameter(Mandatory=$false)]
    [string]$CertPath = "",
    
    [Parameter(Mandatory=$false)]
    [string]$CertPassword = ""
)

$ErrorActionPreference = "Stop"

# Paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)
$manifestDir = Join-Path $scriptDir "..\manifest"
$outputDir = Join-Path $scriptDir "output"
$bundleDir = Join-Path $scriptDir "bundle"
$guardrailsDir = Join-Path $scriptDir "..\guardrails"

Write-Host "=== RA Longevity MSIX Build Script ===" -ForegroundColor Cyan
Write-Host "Version: $Version" -ForegroundColor Green

# Create output directories
Write-Host "`nCreating output directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
New-Item -ItemType Directory -Force -Path $bundleDir | Out-Null

# Update version in manifest
Write-Host "Updating manifest version to $Version..." -ForegroundColor Yellow
$manifestPath = Join-Path $manifestDir "app-manifest.xml"
if (Test-Path $manifestPath) {
    $xml = [xml](Get-Content $manifestPath)
    $xml.Package.Identity.Version = $Version
    $xml.Save($manifestPath)
    Write-Host "✓ Manifest version updated" -ForegroundColor Green
} else {
    Write-Warning "Manifest not found at $manifestPath"
}

# Run Codex Guardrails
Write-Host "`nRunning Codex Guardrails..." -ForegroundColor Yellow
$guardrailsScript = Join-Path $guardrailsDir "run-guardrails.ps1"
if (Test-Path $guardrailsScript) {
    & $guardrailsScript -Version $Version
    Write-Host "✓ Guardrails completed" -ForegroundColor Green
} else {
    Write-Host "⚠ Guardrails script not found (continuing)" -ForegroundColor Yellow
}

# Build MSIX package
Write-Host "`nBuilding MSIX package..." -ForegroundColor Yellow
$msixPath = Join-Path $outputDir "NTRuleIndex_${Version}_x64.msix"

try {
    # Note: This assumes makeappx.exe is in PATH or Windows SDK is installed
    $makeappx = Get-Command makeappx.exe -ErrorAction Stop
    
    & $makeappx pack /d $manifestDir /p $msixPath /o
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ MSIX package built successfully: $msixPath" -ForegroundColor Green
    } else {
        throw "makeappx.exe failed with exit code $LASTEXITCODE"
    }
} catch {
    Write-Error "Failed to build MSIX package: $_"
    Write-Host "`nNote: Ensure Windows SDK is installed and makeappx.exe is in PATH" -ForegroundColor Yellow
    exit 1
}

# Sign package if requested
if ($Sign) {
    Write-Host "`nSigning MSIX package..." -ForegroundColor Yellow
    
    if (-not $CertPath) {
        Write-Error "Certificate path is required when -Sign is specified"
        exit 1
    }
    
    try {
        $signtool = Get-Command signtool.exe -ErrorAction Stop
        
        if ($CertPassword) {
            & $signtool sign /fd SHA256 /f $CertPath /p $CertPassword $msixPath
        } else {
            & $signtool sign /fd SHA256 /f $CertPath $msixPath
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Package signed successfully" -ForegroundColor Green
        } else {
            throw "signtool.exe failed with exit code $LASTEXITCODE"
        }
    } catch {
        Write-Error "Failed to sign package: $_"
        exit 1
    }
}

# Generate attestation bundle
Write-Host "`nGenerating attestation bundle..." -ForegroundColor Yellow
$attestationDir = Join-Path $outputDir "attestation"
New-Item -ItemType Directory -Force -Path $attestationDir | Out-Null

# Copy guardrails outputs
$sarifPath = Join-Path $guardrailsDir "output\analysis.sarif"
$csvPath = Join-Path $guardrailsDir "output\metrics.csv"
$xlsxPath = Join-Path $guardrailsDir "output\inventory.xlsx"

if (Test-Path $sarifPath) { Copy-Item $sarifPath $attestationDir }
if (Test-Path $csvPath) { Copy-Item $csvPath $attestationDir }
if (Test-Path $xlsxPath) { Copy-Item $xlsxPath $attestationDir }

Write-Host "✓ Attestation bundle created" -ForegroundColor Green

# Summary
Write-Host "`n=== Build Summary ===" -ForegroundColor Cyan
Write-Host "Package: $msixPath" -ForegroundColor White
Write-Host "Version: $Version" -ForegroundColor White
Write-Host "Signed: $(if ($Sign) { 'Yes' } else { 'No' })" -ForegroundColor White
Write-Host "Attestation: $attestationDir" -ForegroundColor White

Write-Host "`n✓ Build completed successfully!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Test package: Add-AppxPackage -Path '$msixPath'" -ForegroundColor White
Write-Host "  2. Upload to Partner Center or use GitHub Action for automated submission" -ForegroundColor White
