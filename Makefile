# ============================================================
# Aluminum OS — Unified Makefile
# All CLIs: aluminum-boot · tucker · forge
# ============================================================
# Usage:
#   make           → build all Rust binaries (release)
#   make forge     → build forge only (zero external deps, instant)
#   make tucker    → build tucker (requires cargo update first)
#   make boot      → build aluminum-boot kernel binary
#   make check     → cargo check (fast, no linking)
#   make test      → run all tests (Rust + Python)
#   make install   → install all binaries to ~/.local/bin
#   make clean     → remove build artifacts
#   make status    → show versions of all installed CLIs
# ============================================================

CARGO        := cargo
RELEASE_DIR  := target/release
DEBUG_DIR    := target/debug
INSTALL_DIR  := $(HOME)/.local/bin

# Detect platform
UNAME := $(shell uname -s 2>/dev/null || echo Windows)
ifeq ($(UNAME), Windows_NT)
  EXE := .exe
  CP  := copy
else
  EXE :=
  CP  := cp
endif

.PHONY: all forge tucker boot check test install install-forge clean status python-test

# ── Build targets ──────────────────────────────────────────────────────────

## Build all Rust binaries (release)
all: forge boot
	@echo ""
	@echo "✓ All binaries built in $(RELEASE_DIR)/"
	@echo "  forge$(EXE)         — unified 51% native AI CLI"
	@echo "  aluminum-boot$(EXE) — constitutional kernel boot"
	@echo ""
	@echo "Run 'make tucker' after 'cargo update' to build Tucker V4 CLI"

## Build forge only — zero external deps, instant build
forge:
	$(CARGO) build -p forge --release
	@echo "✓ forge built: $(RELEASE_DIR)/forge$(EXE)"

## Build Tucker V4 CLI — requires external deps (run cargo update first)
tucker:
	@echo "Building Tucker V4 CLI (full async council mode)…"
	@echo "Note: run 'cargo update' first if this is the first build"
	$(CARGO) build -p tucker --release
	@echo "✓ tucker built: $(RELEASE_DIR)/tucker$(EXE)"

## Build aluminum-boot kernel binary
boot:
	$(CARGO) build -p aluminum-os --release
	@echo "✓ aluminum-boot built: $(RELEASE_DIR)/aluminum-boot$(EXE)"

## Fast type-check without linking
check:
	$(CARGO) check -p aluminum-os
	$(CARGO) check -p forge
	@echo "✓ cargo check passed for aluminum-os + forge"

# ── Test targets ───────────────────────────────────────────────────────────

## Run all tests (Rust + Python)
test: rust-test python-test
	@echo ""
	@echo "✓ All tests passed"

## Rust tests
rust-test:
	$(CARGO) test
	@echo "✓ Rust tests passed"

## Python tests (Manus Core + Kintsugi + Health + uws CLI + Provenance)
python-test:
	cd python && python3 -m unittest tests.test_all -v

# ── Install targets ────────────────────────────────────────────────────────

## Install all built binaries to INSTALL_DIR
install: all
	mkdir -p $(INSTALL_DIR)
	$(CP) $(RELEASE_DIR)/forge$(EXE)         $(INSTALL_DIR)/
	$(CP) $(RELEASE_DIR)/aluminum-boot$(EXE) $(INSTALL_DIR)/
	@echo "✓ forge and aluminum-boot installed to $(INSTALL_DIR)"
	@echo "  Add to PATH: export PATH=\"$$PATH:$(INSTALL_DIR)\""

## Install forge only (fast — zero external deps)
install-forge: forge
	mkdir -p $(INSTALL_DIR)
	$(CP) $(RELEASE_DIR)/forge$(EXE) $(INSTALL_DIR)/
	@echo "✓ forge installed to $(INSTALL_DIR)/forge$(EXE)"

# ── Status ────────────────────────────────────────────────────────────────

## Show installed CLI versions
status:
	@echo "=== Aluminum OS CLI Status ==="
	@forge --version 2>/dev/null && echo "  forge: installed" || echo "  forge: not installed (run: make install-forge)"
	@tucker --version 2>/dev/null && echo "  tucker: installed" || echo "  tucker: not installed (run: make tucker && make install)"
	@aluminum-boot 2>/dev/null | head -1 || echo "  aluminum-boot: not installed"
	@python3 janus/janus_boot.py --version 2>/dev/null || echo "  janus: available (python3 janus/janus_boot.py)"
	@echo ""
	@echo "Governance check (native, no deps):"
	@forge govern "constitutional sovereignty audit"

# ── Maintenance ───────────────────────────────────────────────────────────

## Remove build artifacts
clean:
	$(CARGO) clean
	find python -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ build artifacts removed"
