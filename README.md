# Resume Builder with Role-Based Content

A robust resume builder that generates customized resumes for different roles using a Python preprocessor and LaTeX.

## How It Works

The system uses a **Python preprocessor** to filter LaTeX content based on role tags before compilation:

1. **Source Files**: Your LaTeX files in `tex-files/` contain role tags
2. **Python Preprocessor**: `scripts/resume_builder.py` processes the files and removes/excludes content based on the target role
3. **Clean LaTeX**: Generates role-specific LaTeX files in `build/artifacts/`
4. **PDF Generation**: LaTeX compiles the filtered files into PDFs in `build/pdfs/`

This approach is much more robust than complex LaTeX macros and allows for flexible, nested content filtering.

## Quick Start

### Build all roles
```bash
make all
```

### Build for specific role
```bash
make qr      # Build for quantitative research role
make qd      # Build for quantitative development role
make tech    # Build for technical role
make soleng  # Build for solutions engineering role
```

### Build for custom role
```bash
make build-customrole
```

### View available PDFs
```bash
make list-pdfs
```

## Directory Structure

```
resume-builder/
├── tex-files/              # Source LaTeX files (your content)
│   ├── main.tex           # Main document
│   ├── header.tex         # Header section
│   ├── experience.tex     # Experience section
│   └── ...                # Other sections
├── templates/             # LaTeX style files
├── scripts/              # Python preprocessor
│   └── resume_builder.py
├── build/                # Generated files
│   ├── artifacts/        # Processed LaTeX files (cleaned by 'make clean')
│   └── pdfs/            # Final PDFs (preserved by 'make clean')
└── Makefile             # Build system
```

## Tag System

### Block-level tagging
Wrap entire sections or experience blocks:

```latex
\begin{rolecontent}{qr,qd,tech}
\begin{experience}[City, ST]
                   {Company Name}
                   {2020 - 2023}
                   {Job Title}
    \item This entire experience block appears for qr, qd, and tech roles
\end{experience}
\end{rolecontent}
```

### Inline tagging
Tag individual bullets within experience blocks:

```latex
\begin{experience}[City, ST]
                   {Company Name}
                   {2020 - 2023}
                   {Job Title}
    \item This bullet appears for all roles
    \rolecontent{qr}{\item This bullet appears only for qr role}
    \rolecontent{qd,tech}{\item This bullet appears for qd and tech roles}
\end{experience}
```

### Content without tags
Content without any tags appears in all role builds.

## Build Commands

| Command | Description |
|---------|-------------|
| `make all` | Build PDFs for all roles |
| `make qr` | Build PDF for quantitative research role |
| `make qd` | Build PDF for quantitative development role |
| `make tech` | Build PDF for technical role |
| `make soleng` | Build PDF for solutions engineering role |
| `make build-rolename` | Build for custom role |
| `make clean` | Remove build artifacts (keeps PDFs) |
| `make clean-all` | Remove everything including PDFs |
| `make list-pdfs` | Show available PDFs |
| `make force` | Force rebuild all PDFs |

### Location Control

Control whether location appears in the header:

```bash
# Include location (Chicago, IL)
make qr INCLUDE_LOC=1
make all INCLUDE_LOC=1

# Exclude location (default)
make qr
make all
```

The location is automatically included/excluded based on the `INCLUDE_LOC` variable in the Makefile or when passed as a parameter.

## Adding New Roles

1. Add the role to the `ROLES` variable in `Makefile`
2. Use the role name in your content tags
3. Build with `make build-rolename`

## Benefits Over LaTeX-Only Solutions

- **No complex macros**: No need for recursive LaTeX macros
- **Order-independent**: Role lists work regardless of order
- **Nested support**: Tags can be nested at any level
- **Easy debugging**: Python errors are clearer than LaTeX errors
- **Extensible**: Easy to add new features or roles
- **Clean separation**: Build artifacts separate from final PDFs

## Example Usage

See `tex-files/example-tags.tex` for comprehensive examples of the tagging system.

## Requirements

- Python 3.6+
- LaTeX distribution (pdflatex)
- Make

## Troubleshooting

### Common Issues

1. **Python script not found**: Ensure `scripts/resume_builder.py` exists and is executable
2. **LaTeX compilation errors**: Check that your LaTeX syntax is correct in source files
3. **Missing content**: Verify your role tags match the roles defined in the Makefile

### Debug Mode

Run the Python preprocessor directly for debugging:

```bash
python3 scripts/resume_builder.py --source-dir tex-files --output-dir build/artifacts --role qr
```

### Understanding the Build Process

1. **Preprocessing**: Python script reads your LaTeX files and filters content based on role tags
2. **Artifacts**: Clean, role-specific LaTeX files are created in `build/artifacts/`
3. **Compilation**: LaTeX compiles the artifacts into PDFs in `build/pdfs/`
4. **Cleanup**: `make clean` removes artifacts but preserves PDFs

## Contributing

1. Add your content to the appropriate `.tex` files in `tex-files/`
2. Use the tagging system to specify which roles should see your content
3. Test with `make clean && make all`
4. Commit your changes 