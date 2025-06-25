# ---------- CONFIG ---------------------------------------------------
SRC_DIR     := tex-files
TEX_MAIN    := $(SRC_DIR)/main.tex
TEX_FILES   := $(SRC_DIR)/header.tex $(SRC_DIR)/education.tex $(SRC_DIR)/skills.tex $(SRC_DIR)/experience.tex $(SRC_DIR)/projects.tex $(SRC_DIR)/additional-info.tex
STYLE       := templates/resume-layout.sty
BUILD_DIR   := build
ROLES       := qr qd tech soleng              # add more tags here
PDFS        := $(addprefix $(BUILD_DIR)/resume-,$(addsuffix .pdf,$(ROLES)))
INCLUDE_LOC :=                           # set to any value to include location
# ---------------------------------------------------------------------

.PHONY: all $(ROLES) clean force

all: $(PDFS)

# Generic rule: resume-qr.pdf, resume-qd.pdf, ...
$(BUILD_DIR)/resume-%.pdf: $(TEX_MAIN) $(TEX_FILES) $(STYLE) | $(BUILD_DIR)
	cp $(SRC_DIR)/*.tex $(BUILD_DIR)/
	cd $(BUILD_DIR) && \
	cp ../$(STYLE) . && \
	echo '\def\buildrole{$*}' > temp.tex && \
	$(if $(INCLUDE_LOC),echo '\def\includelocation{true}',echo '\def\includelocation{false}') >> temp.tex && \
	cat main.tex >> temp.tex && \
	pdflatex -jobname=resume-$* -interaction=nonstopmode temp.tex && \
	pdflatex -jobname=resume-$* -interaction=nonstopmode temp.tex && \
	rm temp.tex resume-layout.sty *.tex

# Convenience phony targets (qr, qd, tech, soleng)
$(ROLES):
	$(MAKE) $(BUILD_DIR)/resume-$@.pdf

# Force rebuild all
force:
	$(MAKE) clean
	$(MAKE) all

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR)
