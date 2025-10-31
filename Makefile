# Makefile for RA Longevity NT Rule Index - Microsoft Store Release

.PHONY: help build-docs msstore-manifest msstore-build msstore-guardrails msstore-package msstore-test msstore-clean all

# Variables
VERSION ?= 1.0.0.0
PYTHON := python3
MSSTORE_DIR := msstore
MANIFEST_DIR := $(MSSTORE_DIR)/manifest
PACKAGING_DIR := $(MSSTORE_DIR)/packaging
GUARDRAILS_DIR := $(MSSTORE_DIR)/guardrails
OUTPUT_DIR := $(PACKAGING_DIR)/output

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(CYAN)RA Longevity NT Rule Index - Build Targets$(NC)"
	@echo ""
	@echo "$(YELLOW)Documentation:$(NC)"
	@echo "  make build-docs              - Build MkDocs documentation site"
	@echo "  make serve-docs              - Serve documentation locally"
	@echo ""
	@echo "$(YELLOW)Microsoft Store Release:$(NC)"
	@echo "  make msstore-manifest        - Generate/update Microsoft Store manifest"
	@echo "  make msstore-guardrails      - Run Codex guardrails analysis"
	@echo "  make msstore-build           - Build MSIX package"
	@echo "  make msstore-package         - Complete package (guardrails + build)"
	@echo "  make msstore-test            - Test MSIX package locally"
	@echo "  make msstore-clean           - Clean build artifacts"
	@echo ""
	@echo "$(YELLOW)All-in-One:$(NC)"
	@echo "  make all                     - Build docs and prepare MSIX package"
	@echo ""
	@echo "$(YELLOW)Variables:$(NC)"
	@echo "  VERSION=$(VERSION)            - Package version (override with VERSION=x.x.x.x)"
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make msstore-package VERSION=1.2.3.0"
	@echo "  make msstore-build"
	@echo "  make all"

# Documentation targets
build-docs: ## Build documentation index and site
	@echo "$(CYAN)Building documentation...$(NC)"
	@if [ -f scripts/build_index.py ]; then \
		$(PYTHON) scripts/build_index.py; \
	fi
	@pip install -q -r requirements.txt
	@mkdocs build --strict
	@echo "$(GREEN)✓ Documentation built in site/$(NC)"

serve-docs: ## Serve documentation locally
	@echo "$(CYAN)Starting documentation server...$(NC)"
	@if [ -f scripts/build_index.py ]; then \
		$(PYTHON) scripts/build_index.py; \
	fi
	@mkdocs serve

# Microsoft Store targets
msstore-manifest: ## Generate/update Microsoft Store manifest
	@echo "$(CYAN)Updating Microsoft Store manifest...$(NC)"
	@mkdir -p $(MANIFEST_DIR)/Assets
	@if [ "$(VERSION)" != "1.0.0.0" ]; then \
		echo "$(YELLOW)Updating version to $(VERSION)...$(NC)"; \
		if command -v sed >/dev/null 2>&1; then \
			sed -i.bak 's/Version="[0-9.]*"/Version="$(VERSION)"/' $(MANIFEST_DIR)/app-manifest.xml; \
			rm -f $(MANIFEST_DIR)/app-manifest.xml.bak; \
		fi; \
		if command -v jq >/dev/null 2>&1; then \
			jq '.package.identity.version = "$(VERSION)"' $(MANIFEST_DIR)/package-metadata.json > $(MANIFEST_DIR)/package-metadata.json.tmp; \
			mv $(MANIFEST_DIR)/package-metadata.json.tmp $(MANIFEST_DIR)/package-metadata.json; \
		fi; \
	fi
	@echo "$(GREEN)✓ Manifest ready at $(MANIFEST_DIR)/$(NC)"

msstore-guardrails: ## Run Codex guardrails analysis
	@echo "$(CYAN)Running Codex guardrails analysis...$(NC)"
	@mkdir -p $(GUARDRAILS_DIR)/output
	@if [ -f $(GUARDRAILS_DIR)/run-guardrails.sh ]; then \
		cd $(GUARDRAILS_DIR) && ./run-guardrails.sh $(VERSION); \
	else \
		echo "$(YELLOW)⚠ Guardrails script not found$(NC)"; \
	fi
	@echo "$(GREEN)✓ Guardrails analysis complete$(NC)"
	@echo "$(GREEN)  - SARIF: $(GUARDRAILS_DIR)/output/analysis.sarif$(NC)"
	@echo "$(GREEN)  - CSV: $(GUARDRAILS_DIR)/output/metrics.csv$(NC)"
	@echo "$(GREEN)  - XLSX: $(GUARDRAILS_DIR)/output/inventory.xlsx$(NC)"

msstore-build: msstore-manifest msstore-guardrails ## Build MSIX package
	@echo "$(CYAN)Building MSIX package...$(NC)"
	@mkdir -p $(OUTPUT_DIR)
	@if [ -f $(PACKAGING_DIR)/build-msix.sh ]; then \
		cd $(PACKAGING_DIR) && ./build-msix.sh $(VERSION); \
	else \
		echo "$(YELLOW)⚠ Build script not found$(NC)"; \
		echo "$(YELLOW)Note: MSIX building requires Windows SDK (makeappx.exe)$(NC)"; \
		echo "$(YELLOW)Manifest and configurations are ready for building on Windows$(NC)"; \
	fi

msstore-package: msstore-build ## Complete MSIX package with attestation
	@echo "$(CYAN)Creating attestation bundle...$(NC)"
	@mkdir -p $(OUTPUT_DIR)/attestation
	@if [ -d $(GUARDRAILS_DIR)/output ]; then \
		cp -r $(GUARDRAILS_DIR)/output/* $(OUTPUT_DIR)/attestation/ 2>/dev/null || true; \
	fi
	@if [ -f $(MANIFEST_DIR)/package-metadata.json ]; then \
		cp $(MANIFEST_DIR)/package-metadata.json $(OUTPUT_DIR)/attestation/; \
	fi
	@echo "$(GREEN)✓ Package ready for distribution$(NC)"
	@echo "$(GREEN)  Output: $(OUTPUT_DIR)/$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Test locally: make msstore-test"
	@echo "  2. Submit to Partner Center or use GitHub Action"

msstore-test: ## Test MSIX package installation (Windows only)
	@echo "$(CYAN)Testing MSIX package...$(NC)"
	@if command -v powershell.exe >/dev/null 2>&1; then \
		echo "$(YELLOW)On Windows, run:$(NC)"; \
		echo "  Add-AppxPackage -Path '$(OUTPUT_DIR)/NTRuleIndex_$(VERSION)_x64.msix'"; \
	else \
		echo "$(YELLOW)⚠ MSIX testing requires Windows with PowerShell$(NC)"; \
		echo "$(YELLOW)Package validation can be done on Windows system$(NC)"; \
	fi

msstore-clean: ## Clean build artifacts
	@echo "$(CYAN)Cleaning Microsoft Store build artifacts...$(NC)"
	@rm -rf $(OUTPUT_DIR)
	@rm -rf $(PACKAGING_DIR)/bundle
	@rm -rf $(GUARDRAILS_DIR)/output
	@echo "$(GREEN)✓ Clean complete$(NC)"

# Combined targets
all: build-docs msstore-package ## Build everything
	@echo "$(GREEN)✓ All targets completed$(NC)"

# Development helpers
install-deps: ## Install Python dependencies
	@echo "$(CYAN)Installing dependencies...$(NC)"
	@pip install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

check-tools: ## Check required tools availability
	@echo "$(CYAN)Checking required tools...$(NC)"
	@echo -n "Python: "; command -v python3 >/dev/null && echo "$(GREEN)✓$(NC)" || echo "$(YELLOW)✗$(NC)"
	@echo -n "MkDocs: "; command -v mkdocs >/dev/null && echo "$(GREEN)✓$(NC)" || echo "$(YELLOW)✗$(NC)"
	@echo -n "jq: "; command -v jq >/dev/null && echo "$(GREEN)✓$(NC)" || echo "$(YELLOW)✗ (optional)$(NC)"
	@if command -v powershell.exe >/dev/null 2>&1 || command -v makeappx.exe >/dev/null 2>&1; then \
		echo -n "Windows SDK: $(GREEN)✓$(NC)"; \
	else \
		echo -n "Windows SDK: $(YELLOW)✗ (required for MSIX build)$(NC)"; \
	fi
	@echo ""

# Archive and release
archive: msstore-package ## Create release archive
	@echo "$(CYAN)Creating release archive...$(NC)"
	@ARCHIVE_NAME="nt-rule-index-msstore-$(VERSION).tar.gz"; \
	tar -czf $$ARCHIVE_NAME \
		$(MSSTORE_DIR)/ \
		README.md \
		LICENSE \
		NOTICE; \
	echo "$(GREEN)✓ Archive created: $$ARCHIVE_NAME$(NC)"

# Default target
.DEFAULT_GOAL := help
