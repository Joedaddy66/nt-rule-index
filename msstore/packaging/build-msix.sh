#!/bin/bash
# Bash Script for Building MSIX Package (Linux/WSL/macOS)
# Usage: ./build-msix.sh <version> [sign]

set -e

VERSION="${1:-1.0.0.0}"
SIGN="${2:-false}"

# Paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
MANIFEST_DIR="$SCRIPT_DIR/../manifest"
OUTPUT_DIR="$SCRIPT_DIR/output"
BUNDLE_DIR="$SCRIPT_DIR/bundle"
GUARDRAILS_DIR="$SCRIPT_DIR/../guardrails"

echo "=== RA Longevity MSIX Build Script ==="
echo "Version: $VERSION"
echo ""

# Create output directories
echo "Creating output directories..."
mkdir -p "$OUTPUT_DIR"
mkdir -p "$BUNDLE_DIR"

# Update version in manifest
echo "Updating manifest version to $VERSION..."
MANIFEST_PATH="$MANIFEST_DIR/app-manifest.xml"
if [ -f "$MANIFEST_PATH" ]; then
    # Use sed to update version (basic implementation)
    sed -i.bak "s/Version=\"[0-9.]*\"/Version=\"$VERSION\"/" "$MANIFEST_PATH"
    echo "✓ Manifest version updated"
else
    echo "⚠ Warning: Manifest not found at $MANIFEST_PATH"
fi

# Update version in package metadata
METADATA_PATH="$MANIFEST_DIR/package-metadata.json"
if [ -f "$METADATA_PATH" ]; then
    # Use sed or jq to update version
    if command -v jq &> /dev/null; then
        jq ".package.identity.version = \"$VERSION\"" "$METADATA_PATH" > "$METADATA_PATH.tmp"
        mv "$METADATA_PATH.tmp" "$METADATA_PATH"
    else
        sed -i.bak "s/\"version\": \"[0-9.]*\"/\"version\": \"$VERSION\"/" "$METADATA_PATH"
    fi
    echo "✓ Package metadata updated"
fi

# Run Codex Guardrails
echo ""
echo "Running Codex Guardrails..."
GUARDRAILS_SCRIPT="$GUARDRAILS_DIR/run-guardrails.sh"
if [ -f "$GUARDRAILS_SCRIPT" ]; then
    bash "$GUARDRAILS_SCRIPT" "$VERSION"
    echo "✓ Guardrails completed"
else
    echo "⚠ Guardrails script not found (continuing)"
fi

# Check for MSIX packaging tools
echo ""
echo "Checking for MSIX packaging tools..."
if command -v makeappx &> /dev/null || command -v makeappx.exe &> /dev/null; then
    echo "✓ makeappx found"
    MAKEAPPX_CMD="makeappx"
    if ! command -v makeappx &> /dev/null; then
        MAKEAPPX_CMD="makeappx.exe"
    fi
elif [ -n "$WSLENV" ]; then
    # Running in WSL, try Windows makeappx
    MAKEAPPX_CMD="/mnt/c/Program Files (x86)/Windows Kits/10/bin/10.0.22621.0/x64/makeappx.exe"
    if [ ! -f "$MAKEAPPX_CMD" ]; then
        echo "⚠ Warning: makeappx not found. Install Windows SDK or use PowerShell script on Windows"
        echo "Skipping MSIX build (manifest and configuration are ready)"
        exit 0
    fi
else
    echo "⚠ Warning: makeappx not found. This script requires Windows SDK or WSL."
    echo "Please use build-msix.ps1 on Windows or install Windows SDK."
    echo "Manifest and configuration files are ready for building."
    exit 0
fi

# Build MSIX package
echo ""
echo "Building MSIX package..."
MSIX_PATH="$OUTPUT_DIR/NTRuleIndex_${VERSION}_x64.msix"

"$MAKEAPPX_CMD" pack /d "$MANIFEST_DIR" /p "$MSIX_PATH" /o

if [ $? -eq 0 ]; then
    echo "✓ MSIX package built successfully: $MSIX_PATH"
else
    echo "✗ Failed to build MSIX package"
    exit 1
fi

# Sign package if requested
if [ "$SIGN" = "true" ] || [ "$SIGN" = "sign" ]; then
    echo ""
    echo "Signing MSIX package..."
    
    if command -v signtool &> /dev/null || command -v signtool.exe &> /dev/null; then
        SIGNTOOL_CMD="signtool"
        if ! command -v signtool &> /dev/null; then
            SIGNTOOL_CMD="signtool.exe"
        fi
        
        if [ -n "$CERT_PATH" ]; then
            "$SIGNTOOL_CMD" sign /fd SHA256 /f "$CERT_PATH" "$MSIX_PATH"
            echo "✓ Package signed successfully"
        else
            echo "⚠ CERT_PATH environment variable not set, skipping signing"
        fi
    else
        echo "⚠ signtool not found, skipping signing"
    fi
fi

# Generate attestation bundle
echo ""
echo "Generating attestation bundle..."
ATTESTATION_DIR="$OUTPUT_DIR/attestation"
mkdir -p "$ATTESTATION_DIR"

# Copy guardrails outputs
SARIF_PATH="$GUARDRAILS_DIR/output/analysis.sarif"
CSV_PATH="$GUARDRAILS_DIR/output/metrics.csv"
XLSX_PATH="$GUARDRAILS_DIR/output/inventory.xlsx"

[ -f "$SARIF_PATH" ] && cp "$SARIF_PATH" "$ATTESTATION_DIR/"
[ -f "$CSV_PATH" ] && cp "$CSV_PATH" "$ATTESTATION_DIR/"
[ -f "$XLSX_PATH" ] && cp "$XLSX_PATH" "$ATTESTATION_DIR/"

echo "✓ Attestation bundle created"

# Summary
echo ""
echo "=== Build Summary ==="
echo "Package: $MSIX_PATH"
echo "Version: $VERSION"
echo "Signed: $SIGN"
echo "Attestation: $ATTESTATION_DIR"
echo ""
echo "✓ Build completed successfully!"
echo ""
echo "Next steps:"
echo "  1. Test package on Windows: Add-AppxPackage -Path '$MSIX_PATH'"
echo "  2. Upload to Partner Center or use GitHub Action for automated submission"
