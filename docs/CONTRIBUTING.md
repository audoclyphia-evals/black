# Contributing to Black

Contributions are accepted via pull requests and issues. This guide covers the development setup, testing procedures, and contribution workflow for the Black code formatter.

Black is an opinionated Python code formatter that applies a consistent style across codebases. Contributing to Black involves working with the formatting engine, parser (blib2to3), CLI interface, and extensive test suite. Familiarity with Python ASTs, code formatting concepts, and the project's modular architecture is helpful for meaningful contributions.

## Development

### Environment Setup

Black is a Python project using standard tooling. Set up a development environment with the following steps:

```bash
# Clone the repository
git clone https://github.com/psf/black.git
cd black

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install in editable mode with development dependencies
pip install -e ".[d]"
```

The project includes a `Dockerfile` for containerized builds. The Docker build compiles Black and its dependencies using a multi-stage approach:

```bash
# Build Docker image
docker build -t black .
```

### Available Scripts

The `scripts/` directory contains several utility scripts for development and release management:

| Script | Purpose |
|--------|---------|
| `scripts/generate_schema.py` | Generates JSON schema from the Click CLI command |
| `scripts/make_width_table.py` | Generates the Unicode width table |
| `scripts/fuzz.py` | Property-based fuzzing tests using Hypothesis |
| `scripts/migrate-black.py` | Migrates feature branches by applying Black to each commit |
| `scripts/release.py` | Release automation (versioning, changelog, git tags) |
| `scripts/release_tests.py` | Tests for the release scripts |
| `scripts/diff_shades_gha_helper.py` | GitHub Actions helper for diff-shades analysis |
| `scripts/check_pre_commit_rev_in_example.py` | Verifies pre-commit example version |
| `scripts/check_version_in_basics_example.py` | Verifies version in documentation examples |

### Code Organization

The project follows a structured layout:

- **`src/black/`** — Core formatting engine, CLI, and utilities
- **`src/blackd/`** — HTTP daemon server mode
- **`src/blib2to3/`** — Parser and grammar library (forked lib2to3)
- **`tests/`** — Test suite with extensive test data
- **`scripts/`** — Development and release utilities
- **`docs/`** — Sphinx documentation configuration

For a detailed breakdown of the architecture, refer to the [Architecture Overview](docs/ARCHITECTURE.md).

### Pre-commit Hooks

The repository includes pre-commit hook verification through `scripts/check_pre_commit_rev_in_example.py`, which ensures version references in documentation remain consistent. Configure pre-commit locally to run Black on staged files before committing.

## Testing

Black maintains an extensive test suite covering formatting correctness, parser behavior, edge cases, and regression scenarios. For comprehensive testing documentation, refer to the [Testing Guide](docs/TESTING.md).

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/black

# Run a specific test file
pytest tests/test_main.py

# Run tests for a specific formatting case
pytest -k "docstring"
```

### Test Structure

The test infrastructure is organized as follows:

- **`tests/conftest.py`** — Pytest configuration with custom options for syntax tree printing
- **`tests/__init__.py`** — Test package initialization
- **`tests/data/cases/`** — Formatting test cases (input/output pairs)

### Test Data Cases

The `tests/data/cases/` directory contains Python files that serve as both input and expected output for formatting tests. Each file typically contains code that exercises specific formatting rules. Key categories include:

- **Docstrings**: `docstring.py`, `docstring2.py`, `docstring_newline.py`, `f_docstring.py`
- **Comments**: `comments.py` through `comments9.py`, `comments_in_blocks.py`
- **Format directives**: `fmtonoff.py` through `fmtonoff6.py`, `fmtskip.py` through `fmtskip13.py`
- **String handling**: `multiline_strings.py`, `long_strings_flag_disabled.py`
- **Pattern matching**: `pattern_matching_simple.py` through `pattern_matching_trailing_comma.py`
- **Line ranges**: `line_ranges_basic.py` through `line_ranges_unwrapping.py`
- **PEP compliance**: `pep_570.py`, `pep_572.py`, `pep_604.py`, `pep_646.py`, `pep_654.py`, `pep_701.py`

### Writing New Tests

When adding a new formatting test:

1. Create a Python file in `tests/data/cases/` with descriptive naming
2. Include both the unformatted and expected formatted versions in the same file (separated by the standard test marker)
3. The test runner automatically compares input against expected output
4. Add corresponding pytest test functions that invoke the formatter with appropriate `Mode` settings

### Fuzzing

The project includes property-based testing via `scripts/fuzz.py`, which uses Hypothesis and Hypothesmith to test Black's idempotency property — applying Black twice to any valid Python source should produce identical output.

```bash
# Run fuzzing tests
python scripts/fuzz.py
```

## Contributing

### Workflow

1. Fork the repository and create a feature branch
2. Set up the development environment as described above
3. Make changes with corresponding tests
4. Run the full test suite to verify no regressions
5. Submit a pull request with a clear description of the change

### Code Style

Black enforces its own formatting style on its codebase. Run Black on all modified files before submitting:

```bash
black src/ tests/ scripts/
```

### Reporting Issues

Issues should be reported on the project's issue tracker. When reporting formatting bugs:

- Include the Python version and target version being used
- Provide the exact input code and the unexpected output
- Note whether `--preview` mode was enabled
- Check if the issue reproduces with the latest version

### Key Areas for Contributions

- **Formatting rules** in `src/black/linegen.py` and `src/black/lines.py`
- **String transformations** in `src/black/trans.py`
- **Comment handling** in `src/black/comments.py`
- **Parser improvements** in `src/blib2to3/`
- **CLI enhancements** in `src/black/__init__.py`
- **HTTP server features** in `src/blackd/`
- **Test coverage** in `tests/data/cases/`

For deeper understanding of specific subsystems, consult the dedicated documentation:

- [Core Formatting Engine Guide](docs/CORE_FORMATTER.md)
- [Parser & Grammar Library](docs/PARSER_LIBRARY.md)
- [Blackd HTTP Server Guide](docs/BLACKD_SERVER.md)
- [Architecture Overview](docs/ARCHITECTURE.md)