# Development Setup and Workflow

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

Welcome to the development guide for **Black**, the uncompromising Python code formatter. This document will get you from zero to a working development environment, explain the project's structure, and walk you through the common workflows you'll use as a contributor.

## Overview

Black is an opinionated code formatter that automatically formats Python code to a consistent style. By using it, you agree to cede control over minutiae of hand-formatting. In return, Black gives you speed, determinism, and freedom from `pycodestyle` nagging about formatting. You will save time and mental energy for more important matters.

Blackened code looks the same regardless of the project you're reading. Formatting becomes transparent after a while and you can focus on the content instead. Black makes code review faster by producing the smallest diffs possible.

## Installation

### Prerequisites

- **Python**: Black requires Python 3.8 or later.
- **Git**: You'll need Git to clone the repository and manage your changes.

### Setting Up Your Development Environment

1. **Clone the repository**

   ```bash
   git clone https://github.com/psf/black.git
   cd black
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Black in editable mode with development dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

   This installs Black itself plus all the tools you'll need for testing, linting, and development.

4. **Verify the installation**

   ```bash
   black --version
   ```

   You should see the version of Black you just installed.

## Development

### Project Structure

The Black codebase is organized into several key directories:

```
├── src/
│   ├── black/           # Core formatter logic
│   │   ├── __init__.py  # Main CLI and entry point
│   │   ├── brackets.py  # Bracket tracking for line splitting
│   │   ├── cache.py     # File system cache for formatted files
│   │   ├── comments.py  # Comment parsing and formatting directives
│   │   ├── concurrency.py # Parallel file formatting utilities
│   │   ├── debug.py     # Syntax tree inspection and debugging
│   │   ├── files.py     # File system operations and pyproject.toml parsing
│   │   ├── handle_ipynb_magics.py # Jupyter notebook magic command handling
│   │   ├── linegen.py   # Line generation from syntax trees
│   │   ├── lines.py     # Line manipulation utilities
│   │   ├── mode.py      # Configuration data structures
│   │   ├── nodes.py     # Syntax tree node utilities
│   │   ├── numerics.py  # Numeric literal formatting
│   │   ├── output.py    # Terminal output and diff generation
│   │   ├── parsing.py   # Source code parsing
│   │   ├── ranges.py    # Line range formatting
│   │   ├── report.py    # Formatting result reporting
│   │   ├── rusty.py     # Rust-inspired Result types (Ok/Err)
│   │   ├── schema.py    # JSON schema for configuration
│   │   ├── strings.py   # String manipulation utilities
│   │   └── trans.py     # String literal transformers
│   ├── blackd/          # HTTP server for formatting
│   │   ├── __init__.py  # Server entry point and request handling
│   │   ├── __main__.py  # CLI entry point for blackd
│   │   ├── client.py    # HTTP client for blackd
│   │   └── middlewares.py # CORS middleware
│   └── blib2to3/        # Python parser (forked from lib2to3)
│       ├── pgen2/       # Parser generator
│       └── pytree.py    # Syntax tree node structures
├── tests/               # Test suite
│   ├── conftest.py      # Pytest configuration
│   └── data/cases/      # Test case files
├── scripts/             # Utility scripts
│   ├── release.py       # Release automation
│   ├── fuzz.py          # Fuzzing tests
│   └── diff_shades_gha_helper.py # GitHub Actions helper
└── action/              # GitHub Action
    └── main.py
```

### Available Scripts and Commands

The project provides several utility scripts in the `scripts/` directory:

| Script | Purpose |
|--------|---------|
| `scripts/release.py` | Automates release versioning and changelog updates |
| `scripts/release_tests.py` | Tests for release versioning logic |
| `scripts/fuzz.py` | Property-based fuzzing tests for the formatter |
| `scripts/generate_schema.py` | Generates JSON schema for Black's configuration |
| `scripts/make_width_table.py` | Generates Unicode width table for character width calculations |
| `scripts/migrate-black.py` | Rewrites git history by applying Black to individual commits |
| `scripts/diff_shades_gha_helper.py` | GitHub Actions helper for analyzing Black's impact on PRs |
| `scripts/check_pre_commit_rev_in_example.py` | Validates pre-commit version references in docs |
| `scripts/check_version_in_basics_example.py` | Validates version consistency in documentation |

### Running Tests

Black uses pytest for testing. To run the full test suite:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_format.py
```

For more detailed test output, use the verbose flag:

```bash
pytest -v
```

You can also use pytest's built-in options for debugging, such as `--print-full-tree` and `--print-tree-diff` (configured in `tests/conftest.py`).

### Code Formatting and Linting

Since Black is itself a code formatter, the project enforces its own formatting. Before submitting changes, make sure your code is formatted with Black:

```bash
black src/ tests/
```

The project also uses type hints. You can check type correctness with mypy (if installed):

```bash
mypy src/
```

### Pre-commit Hooks

The project recommends using pre-commit hooks to automatically format code before commits. If you have pre-commit installed, you can set it up with:

```bash
pre-commit install
```

This will run Black and other checks on your staged files before each commit.

### Debugging

Black provides a `DebugVisitor` class in `src/black/debug.py` for inspecting and pretty-printing lib2to3 syntax trees. You can use it to understand how Black parses and transforms code:

```python
from black.debug import DebugVisitor
from blib2to3.pygram import python_grammar_no_print_statement
from blib2to3.pgen2 import driver as pgen2_driver

# Parse source code
d = pgen2_driver.Driver(python_grammar_no_print_statement)
tree = d.parse_string("x = 1 + 2")

# Pretty-print the syntax tree
DebugVisitor().visit(tree)
```

## Configuration

Black can be configured through a `pyproject.toml` file in your project root. Here are the available configuration options:

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BLACK_CACHE_DIR` | Override the cache directory location | Platform-specific cache dir | No |

### pyproject.toml Configuration

Create a `[tool.black]` section in your `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

### Key Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `line-length` | Maximum line length in characters | `88` |
| `target-version` | Python versions to target (e.g., `['py38', 'py39']`) | All supported versions |
| `include` | Regular expression for files to include | `\.pyi?$` |
| `exclude` | Regular expression for files to exclude | See above |
| `force-exclude` | Files to always exclude (even when passed explicitly) | Empty |
| `skip-magic-trailing-comma` | Skip adding trailing commas | `false` |
| `preview` | Enable preview style features | `false` |
| `required-version` | Specify required Black version | Empty |

### GitHub Action Configuration

Black also provides a GitHub Action in `action/main.py` that can be configured with:

| Input | Description | Default |
|-------|-------------|---------|
| `version` | Version of Black to install | Latest |
| `use_pyproject` | Read version from pyproject.toml | `false` |
| `options` | Command-line options for Black | Empty |
| `src` | Source files to format | Empty |
| `jupyter` | Enable Jupyter notebook support | `false` |
| `black_args` | Deprecated: use `options` and `src` instead | Empty |

## Contributing

We welcome contributions! Here's how you can help:

1. **Check existing issues**: Look for issues labeled "good first issue" or "help wanted" on GitHub.
2. **Fork the repository**: Create your own fork and work on a feature branch.
3. **Write tests**: Add test cases for your changes in the `tests/` directory.
4. **Run the test suite**: Make sure all tests pass before submitting.
5. **Submit a pull request**: Open a PR with a clear description of your changes.

For more detailed contribution guidelines, see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

Black is released under the MIT License. See the LICENSE file for details.