# Resume Builder

A LaTeX-based resume builder that generates different versions of your resume for different job roles using conditional content.

## Features

- **Role-based customization**: Generate different resume versions for different job types (QR, QD, Tech, SE)
- **Modular content**: Content is split into separate `.tex` files for easy editing
- **Conditional content**: Use `\qronly{}`, `\qdonly{}`, `\techonly{}`, and `\solengonly{}` macros to include role-specific content
- **Location control**: Optionally include or exclude location from the header
- **Automated builds**: Makefile handles compilation and dependency tracking

## Quick Start

1. **Install LaTeX** (if not already installed):
   ```bash
   brew install --cask mactex
   ```

2. **Build all resume versions**:
   ```bash
   make all
   ```

3. **Build specific role**:
   ```bash
   make qr    # Quantitative Research
   make qd    # Quantitative Development
   make tech  # Technology
   make soleng # Software Engineering
   ```

4. **Include location in header**:
   ```bash
   make qr INCLUDE_LOCATION=1
   make qd INCLUDE_LOCATION=1
   ```

## Usage

### Role-based Content

Wrap content in role-specific macros to include it only for certain roles:

```latex
\qronly{\item This only appears in QR resumes}
\qdonly{\item This only appears in QD resumes}
\techonly{\item This only appears in Tech resumes}
\solengonly{\item This only appears in Software Engineering resumes}
```

### Location Control

- **Default behavior**: Location is omitted from the header
- **Include location**: Pass `INCLUDE_LOCATION=1` to include "Chicago, IL" in the header
- **Example**: `make qr INCLUDE_LOCATION=1` generates a QR resume with location included

### File Structure

```
resume-builder/
├── tex-files/           # LaTeX source files
│   ├── main.tex        # Main document with role macros
│   ├── header.tex      # Header with conditional location
│   ├── education.tex   # Education section
│   ├── experience.tex  # Experience section
│   ├── skills.tex      # Skills section
│   └── projects.tex    # Projects section
├── templates/          # Style files
│   └── resume-layout.sty
├── build/             # Generated PDFs
└── Makefile          # Build automation
```

## Commands

- `make all` - Build all role versions
- `make qr` - Build Quantitative Research version
- `make qd` - Build Quantitative Development version
- `make tech` - Build Technology version
- `make soleng` - Build Software Engineering version
- `make clean` - Remove all generated files
- `make force` - Force rebuild all versions

## Overleaf Compatibility

This project works with Overleaf! Simply upload the `tex-files/` directory and `templates/` directory to Overleaf, then compile `main.tex`. The role-based content will work as expected.

## Troubleshooting

- **"resume is up to date"**: Use `make force` to force a rebuild
- **LaTeX errors**: Check for typos in macro names (e.g., `\QDOnly` vs `\QDonly`)
- **Missing files**: Ensure all `.tex` files are in the `tex-files/` directory 