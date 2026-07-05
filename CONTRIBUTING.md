# Contributing to Black

Guidelines and instructions for contributing to the Black code formatter.

Black is an opinionated Python code formatter that provides a deterministic and consistent style. Contributions help maintain and extend its formatting capabilities across the Python ecosystem. This guide covers development setup, testing procedures, and the contribution workflow.

## Development

### Prerequisites

Black requires Python 3.8 or later. The project uses [Hatch](https://hatch.pypa.io/) as its build system.

### Setting Up the Development Environment

```bash
# Clone the repository
git clone https://github.com/psf/black.git
cd black

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install build dependencies and the package in development mode
pip install --upgrade pip
pip install --group hatch

# Build and install Black in development mode
hatch build -t wheel
pip install dist/*-cp*
```

Alternatively, using the Dockerfile for a containerized environment:

```bash
docker build -t black-dev .
docker run -v $(pwd):/code black-dev /opt/venv/bin/black --check /code
```

### Project Structure

The codebase is organized as follows:

| Directory | Purpose |
|---|---|
| `src/black/` | Core formatting engine — CLI, mode configuration, line generation, string transformation, and bracket tracking |
| `src/blackd/` | HTTP server (`blackd`) and client (`BlackDClient`) for remote formatting |
| `src/blib2to3/` | Forked `lib2to3` parser — grammar, tokenizer, and syntax tree definitions |
| `scripts/` | Release automation, schema generation, fuzz testing, and documentation validation |
| `tests/` | Test suites, fixtures, and formatting test cases |
| `action/` | GitHub Action entrypoint for CI/CD integration |

### Key Source Modules

| Module | Responsibility |
|---|---|
| `src/black/__init__.py` | Main CLI entry point and top-level formatting functions |
| `src/black/mode.py` | Configuration data structures (`Mode`, `TargetVersion`, `Preview`) |
| `src/black/linegen.py` | Line generation from syntax trees |
| `src/black/lines.py` | Line and block data structures |
| `src/black/trans.py` | String transformers for merging and splitting |
| `src/black/brackets.py` | Bracket depth tracking and delimiter priority |
| `src/black/comments.py` | Comment parsing and `fmt:off` directive handling |
| `src/black/nodes.py` | Syntax tree node utilities |
| `src/black/parsing.py` | Source code parsing and AST safety validation |
| `src/black/ranges.py` | Line range formatting support |
| `src/black/cache.py` | File system cache for avoiding redundant reformatting |
| `src/black/concurrency.py` | Parallel file formatting utilities |
| `src/black/files.py` | File system operations, project root detection, and `pyproject.toml` parsing |

### Utility Scripts

The `scripts/` directory contains maintenance and release tooling:

| Script | Purpose |
|---|---|
| `scripts/release.py` | Automates release versioning and changelog updates |
| `scripts/generate_schema.py` | Generates JSON schema for Black's configuration options |
| `scripts/make_width_table.py` | Generates the Unicode character width table |
| `scripts/fuzz.py` | Property-based fuzzing tests |
| `scripts/diff_shades_gha_helper.py` | GitHub Actions helper for diff-shades analysis |
| `scripts/migrate-black.py` | Rewrites git history applying Black to individual commits |

## Testing

Black uses [pytest](https://docs.pytest.org/) as its test framework. The test suite validates formatting correctness across a wide range of Python syntax patterns.

### Running Tests

```bash
# Run the full test suite
pytest

# Run tests for a specific module
pytest tests/test_format.py

# Run a single test case
pytest tests/test_format.py -k "test_expression"

# Run with verbose output
pytest -v
```

### Test Configuration

The `tests/conftest.py` file defines shared pytest fixtures and custom command-line options:

- `--print-full-tree`: Prints the full lib2to3 syntax tree for debugging
- `--print-tree-diff`: Prints the diff between syntax trees before and after formatting

### Test Structure

The test suite is organized into two main categories:

**Functional Tests** — Located in `tests/`, these test the formatter's behavior end-to-end. Tests verify that input code produces expected formatted output.

**Formatting Test Cases** — Located in `tests/data/cases/`, these are Python source files that serve as input/output pairs for the formatter. Each file contains code that Black should format deterministically. Notable categories include:

| Case File Pattern | Tests |
|---|---|
| `comments*.py` | Comment placement, spacing, and preservation |
| `fmtonoff*.py` / `fmtskip*.py` | `# fmt: off` / `# fmt: skip` directive behavior |
| `line_ranges_*.py` | Line range formatting and boundary conditions |
| `pep_*.py` | PEP-specific syntax formatting (walrus operator, union types, etc.) |
| `preview_*.py` | Preview-mode formatting features |
| `docstring*.py` | Docstring formatting and normalization |
| `pattern_matching_*.py` | `match`/`case` statement formatting |

### Writing New Tests

When adding a new formatting feature or fixing a formatting bug:

1. Add a test case file in `tests/data/cases/` with the unformatted input
2. Ensure the file demonstrates the specific formatting behavior
3. Add corresponding test functions in the appropriate test module under `tests/`
4. Run the full test suite to verify no regressions

### Fuzz Testing

Black includes property-based fuzz testing via `scripts/fuzz.py`, which generates random Python code and verifies that formatting is idempotent (formatting twice produces the same result as formatting once).

```bash
# Run fuzz tests
python scripts/fuzz.py
```

## Contributing

### Contribution Workflow

1. **Fork** the repository on GitHub
2. **Clone** your fork and set up the development environment (see [Development](#development))
3. **Create a branch** for your change:
   ```bash
   git checkout -b feature/my-change
   ```
4. **Make your changes** with corresponding tests
5. **Run the test suite** to ensure nothing is broken:
   ```bash
   pytest
   ```
6. **Commit** with a clear, descriptive message
7. **Push** your branch and open a pull request

### Code Style

Black is its own primary user — the codebase is formatted with Black. Contributors should ensure all code is formatted with the version of Black specified in the project's configuration.

### Commit Messages

Write clear, descriptive commit messages that explain the purpose of the change. Reference relevant issue numbers where applicable.

### Reporting Issues

Issues should be reported on the GitHub issue tracker. When reporting formatting bugs, include:

- The Python source code that demonstrates the issue
- The expected formatted output
- The actual formatted output produced by Black
- The Python version and Black version being used

### Pre-commit Integration

Black supports integration via [pre-commit](https://pre-commit.com/). The repository includes validation scripts to ensure documentation examples stay consistent with pre-commit configuration:

- `scripts/check_pre_commit_rev_in_example.py` — Validates pre-commit `rev` references in documentation
- `scripts/check_version_in_basics_example.py` — Validates version consistency in basic usage examples