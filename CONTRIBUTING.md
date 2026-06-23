# Contributing to Black

Guidelines for developing, testing, and contributing to the Black code formatter.

Black is the uncompromising Python code formatter. This document covers the development workflow, testing procedures, and contribution process for developers working on Black itself.

## Development

### Environment Setup

Black requires Python 3.13 or later. The project uses a `src/` layout with the following package structure:

- `src/black/` — Core formatting engine
- `src/blackd/` — HTTP formatting server
- `src/blib2to3/` — Python syntax parser

The build system uses Hatch. To set up a development environment:

```bash
python -m venv venv
source venv/bin/activate

# Install build dependencies and the package in development mode
pip install --upgrade pip
pip install --group hatch
pip install -e ".[d,uvloop,colorama]"
```

Alternatively, a Docker-based setup is available:

```bash
docker build -t black .
```

This produces a container with Black installed at `/opt/venv/bin/black`.

### Project Structure

The repository is organized as follows:

| Directory | Purpose |
|---|---|
| `src/black/` | Core formatter modules (line generation, parsing, string transformation, etc.) |
| `src/blackd/` | HTTP server (`blackd`) and client for remote formatting |
| `src/blib2to3/` | Forked lib2to3 parser used for Python syntax tree generation |
| `scripts/` | Release automation, schema generation, fuzzing, and documentation checks |
| `tests/` | Test suite including formatting case files |
| `action/` | GitHub Action entrypoint for running Black in CI |
| `docs/` | Sphinx documentation configuration |
| `profiling/` | Profiling test data |

### Key Scripts

The `scripts/` directory contains development utilities:

| Script | Purpose |
|---|---|
| `scripts/release.py` | Automates release versioning and changelog updates |
| `scripts/release_tests.py` | Tests for release versioning logic |
| `scripts/generate_schema.py` | Generates JSON schema for Black's configuration options |
| `scripts/make_width_table.py` | Generates Unicode width table for character display calculations |
| `scripts/fuzz.py` | Property-based fuzzing tests |
| `scripts/migrate-black.py` | Rewrites git history by applying Black to individual commits |
| `scripts/diff_shades_gha_helper.py` | GitHub Actions helper for diff-shades PR analysis |
| `scripts/check_pre_commit_rev_in_example.py` | Validates pre-commit version references in documentation |
| `scripts/check_version_in_basics_example.py` | Validates version consistency in documentation examples |

## Testing

Black uses pytest as its test framework. The test suite includes both standard unit tests and formatting case files that verify Black's output against expected results.

### Running Tests

```bash
# Run the full test suite
pytest

# Run tests for a specific module
pytest tests/

# Run a specific test file
pytest tests/conftest.py
```

### Custom Pytest Options

The test configuration in `tests/conftest.py` provides additional options for debugging parser output:

- `--print-full-tree` — Prints the full syntax tree for test cases
- `--print-tree-diff` — Prints syntax tree diffs between input and formatted output

### Test Structure

Test case files live in `tests/data/cases/`. Each file typically contains a Python source snippet that exercises a specific formatting behavior. Tests compare Black's formatted output against expected results embedded in or derived from these files.

Categories of test cases include:

- **Formatting directives** — `fmtonoff*.py`, `fmtskip*.py` files testing `# fmt: off` / `# fmt: skip` behavior
- **Line ranges** — `line_ranges_*.py` files testing partial formatting by line range
- **Python syntax** — Files for specific PEPs (e.g., `pep_572.py`, `pep_604.py`, `pep_654.py`, `pep_701.py`)
- **Preview features** — Files prefixed with `preview_` testing upcoming formatting changes
- **Edge cases** — Files testing boundary conditions such as bracket matching, comment handling, and string transformations

### Fuzz Testing

Property-based fuzz testing is available via:

```bash
python scripts/fuzz.py
```

This exercises Black against randomly generated Python code to surface formatting crashes or inconsistencies.

## Contributing

Contributions to Black are accepted via pull requests against the repository.

### Workflow

1. Fork the repository and create a feature branch.
2. Make changes, following the existing code style and conventions.
3. Add or update tests in `tests/data/cases/` for any formatting behavior changes.
4. Ensure the full test suite passes before submitting.
5. Open a pull request with a clear description of the change and its motivation.

### Code Style

Black is itself formatted by Black. All source code should conform to Black's own formatting standards. The core formatter modules in `src/black/` follow standard Python conventions with type annotations throughout.

### Reporting Issues

Issues and feature requests should be reported through the project's issue tracker. When reporting formatting bugs, include the input code, the actual Black output, and the expected output when possible.

### Release Process

The release process is managed through `scripts/release.py`, which handles version tracking via git tags, calendar version generation, and source file updates. Release-related tests are in `scripts/release_tests.py`.