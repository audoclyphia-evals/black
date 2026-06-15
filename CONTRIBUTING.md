# Contribution Guidelines

Welcome to Black — we're thrilled you want to contribute! 🎉

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

Black is the uncompromising Python code formatter. This guide will help you navigate the codebase, set up your development environment, run tests, and submit high-quality pull requests. Whether you're fixing a bug, adding a formatting feature, or improving test coverage, this document points you in the right direction.

## Overview

The Black codebase is organized around three main packages:

- **`src/black/`** — The core formatting engine, including parsing, line generation, string transformation, bracket tracking, and configuration handling.
- **`src/blackd/`** — An optional HTTP server (`blackd`) and client (`BlackDClient`) that exposes Black's formatting over HTTP.
- **`src/blib2to3/`** — A forked lib2to3 parser infrastructure (including `pgen2/` for grammar, tokenization, and parsing) that powers Black's syntax analysis.

Supporting directories include `scripts/` (release automation, schema generation, fuzzing, and documentation validation), `action/` (GitHub Actions integration), `tests/` (test suite and test case data), and `docs/` (Sphinx configuration).

For a detailed breakdown of how these components interact, see [Architecture](ARCHITECTURE.md).

## Development

### Setting Up Your Environment

1. **Clone the repository** and create a virtual environment:

```bash
git clone https://github.com/psf/black.git
cd black
python -m venv venv
source venv/bin/activate
```

2. **Install Black in editable mode** with development dependencies:

```bash
pip install -e ".[dev]"
```

3. **Verify your setup** by running a quick format check:

```bash
python -m black --check src/
```

### Project Layout at a Glance

| Directory | Purpose |
|---|---|
| `src/black/` | Core formatter logic (linegen, brackets, strings, trans, etc.) |
| `src/blackd/` | HTTP server and client for remote formatting |
| `src/blib2to3/` | Python parser and grammar infrastructure |
| `tests/` | Test suite and test configuration |
| `tests/data/cases/` | Formatting test case input/output files |
| `scripts/` | Release, schema generation, fuzzing, and doc validation scripts |
| `action/` | GitHub Actions entry point |
| `profiling/` | Profiling utilities |

### Key Source Modules

The core formatter lives in `src/black/`. Here are the most important modules you'll likely interact with:

- **`__init__.py`** — Main entry point and core formatting orchestration.
- **`linegen.py`** — Generates reformatted `Line` objects from the syntax tree.
- **`lines.py`** — `Line`, `LinesBlock`, `EmptyLineTracker`, and related data structures.
- **`brackets.py`** — `BracketTracker` for tracking bracket depth and delimiter priorities.
- **`trans.py`** — String transformers (merging, splitting, paren stripping).
- **`strings.py`** — String manipulation utilities.
- **`mode.py`** — `Mode`, `TargetVersion`, `Preview`, and `Feature` enumerations for configuration.
- **`parsing.py`** — Source code parsing and AST safety validation.
- **`comments.py`** — Comment parsing and `fmt:off`/`fmt:on`/`fmt:skip` directive handling.
- **`ranges.py`** — Line-range formatting support.
- **`numerics.py`** — Numeric literal formatting and normalization.
- **`files.py`** — File discovery, root detection, and configuration parsing.
- **`cache.py`** — File caching to skip unchanged files.
- **`report.py`** — Formatting result reporting (`Report`, `Changed`, `NothingChanged`).

### Scripts

The `scripts/` directory contains several useful utilities:

| Script | Purpose |
|---|---|
| `scripts/release.py` | Automates release versioning and changelog updates |
| `scripts/release_tests.py` | Tests for the release versioning logic |
| `scripts/generate_schema.py` | Generates the JSON configuration schema for Black |
| `scripts/make_width_table.py` | Generates Unicode character width tables |
| `scripts/fuzz.py` | Property-based fuzzing tests |
| `scripts/diff_shades_gha_helper.py` | GitHub Actions helper for diff-shades analysis |
| `scripts/migrate-black.py` | Rewrites git history applying Black to individual commits |
| `scripts/check_version_in_basics_example.py` | Validates version references in documentation |
| `scripts/check_pre_commit_rev_in_example.py` | Validates pre-commit configuration in documentation |

## Testing

Black has an extensive test suite. For a comprehensive guide on running tests, understanding test structure, and writing new tests, see [Testing Guide](TESTING.md).

### Running Tests

```bash
# Run the full test suite
pytest

# Run a specific test file
pytest tests/test_format.py

# Run tests matching a pattern
pytest -k "test_black"
```

### Test Structure

Tests live in the `tests/` directory. The file `tests/conftest.py` provides pytest configuration and custom command-line options:

- `--print-full-tree` — Prints the full syntax tree for debugging.
- `--print-tree-diff` — Prints diffs between syntax trees.

### Test Cases

Formatting test cases are stored in `tests/data/cases/` as Python files. Each file typically contains both the input and expected output, separated by markers. The test cases cover a wide range of formatting scenarios:

- **`fmt:skip` directive handling** — Files like `fmtskip.py`, `fmtskip_after_bracket_with_comment.py`, `fmtskip_class_header.py`, and others test that `fmt: skip` annotations correctly exclude code from formatting.
- **Redundant parentheses removal** — Test cases verify that unnecessary parentheses are stripped from assignments, return type annotations, except clauses, and more.
- **Docstring blank line handling** — Files like `pyi_docstring_blank_lines_no_preview.py` test blank line rules in `.pyi` stub files and standard Python files.
- **Import line collapse** — `import_line_collapse.py` tests formatting of import statements.
- **Numeric literal formatting** — `numeric_literals.py` and `numeric_literals_skip_underscores.py` test hex, scientific notation, and underscore handling.
- **Comment handling** — Multiple `comments*.py` files cover inline comments, bracket comments, and `type: ignore` directives.
- **Line range formatting** — `line_ranges_basic.py`, `line_ranges_fmt_off.py`, and others test selective formatting by line range.
- **Pattern matching** — Several `pattern_matching_*.py` files test Python 3.10+ `match`/`case` syntax.
- **Preview features** — Files prefixed with `preview_` test upcoming formatting behaviors.

### Writing New Tests

When adding a new formatting feature or fixing a bug:

1. **Create a test case file** in `tests/data/cases/` with both input and expected output.
2. **Register it** in the appropriate test module so it gets picked up by the test runner.
3. **Run the test suite** to verify your change doesn't regress existing behavior.

Property-based fuzzing tests in `scripts/fuzz.py` can also help catch edge cases.

## Contributing

We'd love your help making Black better! Here's how to get started.

### Workflow

1. **Fork** the repository on GitHub.
2. **Create a feature branch** from `main`:

```bash
git checkout -b your-feature-branch
```

3. **Make your changes** — keep commits focused and well-described.
4. **Run the test suite** to make sure everything passes.
5. **Submit a pull request** against `main`.

### Pull Request Guidelines

- **One change per PR** — keep pull requests focused and reviewable.
- **Include test cases** — every formatting change should come with a test case in `tests/data/cases/`.
- **Follow existing code style** — the project obviously uses Black itself for formatting.
- **Describe what changed and why** — include context in your PR description about the problem you're solving.

### Reporting Issues

Issues can be reported on the GitHub issue tracker. When reporting:

- Include the version of Black you're using (`black --version`).
- Provide a minimal code example that reproduces the issue.
- Show the expected vs. actual formatting output.

### Code Areas Needing Contribution

Based on the codebase, here are areas where contributions are especially welcome:

- **Test coverage** — The `tests/data/cases/` directory is extensive but there are always edge cases to cover, particularly around line-range formatting, preview features, and complex bracket expressions.
- **Preview features** — The `Preview` enumeration in `src/black/mode.py` defines individual preview-style features. These are a great place to contribute new formatting behaviors.
- **Documentation** — Improving docstrings, adding examples, and enhancing the contributor experience.

### Additional Documentation

For deeper dives into specific areas, check out these companion guides:

- [Architecture](ARCHITECTURE.md) — System components, relationships, and data flow.
- [Blackd HTTP API Conceptual Guide](API.md) — How to use the blackd HTTP API.
- [Command-Line Interface Reference](CLI.md) — Detailed CLI options and usage patterns.
- [Testing Guide](TESTING.md) — Running tests, test structure, and writing new tests.
- [Development Setup and Workflow](DEVELOPMENT.md) — Environment setup, tools, and workflow details.