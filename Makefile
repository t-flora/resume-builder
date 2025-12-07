# ---------- CONFIG ---------------------------------------------------
SRC_DIR     := tex-files
TEX_MAIN    := $(SRC_DIR)/main.tex
TEX_FILES   := $(SRC_DIR)/header.tex $(SRC_DIR)/education.tex $(SRC_DIR)/skills.tex $(SRC_DIR)/experience.tex $(SRC_DIR)/projects.tex $(SRC_DIR)/additional-info.tex
STYLE       := templates/resume-layout.sty
BUILD_DIR   := build
ARTIFACTS_DIR := $(BUILD_DIR)/artifacts
PDFS_DIR    := $(BUILD_DIR)/pdfs
ROLES       := qr qd tech soleng de ds        # add more tags here
PDFS        := $(addprefix $(PDFS_DIR)/resume-,$(addsuffix .pdf,$(ROLES)))
INCLUDE_LOC :=  # set to any value to include location
INCLUDE_LANGS :=  # set to any value to include languages
PYTHON_SCRIPT := scripts/resume_builder.py
# ---------------------------------------------------------------------

.PHONY: all $(ROLES) clean clean-all force preprocess

all: preprocess $(PDFS)

# Preprocess LaTeX files for all roles
preprocess: $(ARTIFACTS_DIR)
	@echo "Preprocessing LaTeX files for all roles..."
	python3 $(PYTHON_SCRIPT) --source-dir $(SRC_DIR) --output-dir $(ARTIFACTS_DIR) --roles $(ROLES) $(if $(INCLUDE_LOC),--include-location,) $(if $(INCLUDE_LANGS),--include-languages,)

# Generic rule: resume-qr.pdf, resume-qd.pdf, ...
$(PDFS_DIR)/resume-%.pdf: $(ARTIFACTS_DIR)/%/main.tex $(ARTIFACTS_DIR)/%/resume-layout.sty $(ARTIFACTS_DIR)/%/role-def.tex | $(PDFS_DIR)
	@echo "Building PDF for role: $*"
	cd $(ARTIFACTS_DIR)/$* && \
	pdflatex -jobname=resume-$* -interaction=nonstopmode main.tex && \
	pdflatex -jobname=resume-$* -interaction=nonstopmode main.tex && \
	mv resume-$*.pdf ../../pdfs/

# Convenience phony targets (qr, qd, tech, soleng)
$(ROLES): preprocess
	$(MAKE) $(PDFS_DIR)/resume-$@.pdf

# Force rebuild all
force:
	$(MAKE) clean
	$(MAKE) all

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(ARTIFACTS_DIR): $(BUILD_DIR)
	mkdir -p $(ARTIFACTS_DIR)

$(PDFS_DIR): $(BUILD_DIR)
	mkdir -p $(PDFS_DIR)

# Clean only build artifacts, keep PDFs
clean:
	@echo "Cleaning build artifacts (keeping PDFs)..."
	rm -rf $(ARTIFACTS_DIR)

# Clean everything including PDFs
clean-all:
	@echo "Cleaning everything including PDFs..."
	rm -rf $(BUILD_DIR)

# Build for a specific role only
build-%: $(ARTIFACTS_DIR) $(PDFS_DIR)
	@echo "Building for role: $*"
	python3 $(PYTHON_SCRIPT) --source-dir $(SRC_DIR) --output-dir $(ARTIFACTS_DIR) --role $* $(if $(INCLUDE_LOC),--include-location,) $(if $(INCLUDE_LANGS),--include-languages,)
	$(MAKE) $(PDFS_DIR)/resume-$*.pdf

# Show available PDFs
list-pdfs:
	@echo "Available PDFs:"
	@ls -la $(PDFS_DIR)/*.pdf 2>/dev/null || echo "No PDFs found. Run 'make all' to build them."