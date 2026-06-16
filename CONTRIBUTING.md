# Contribution Guidelines

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

Welcome to Black — the uncompromising Python code formatter. We're thrilled you're considering contributing! Whether you're fixing a bug, adding a feature, improving documentation, or just asking a question, your help makes Black better for everyone. This guide will walk you through everything you need to know to get started.

## Development

Setting up your development environment for Black is straightforward. You'll need Python 3.8 or later.

### Quick Start

Clone the repository and install Black in editable mode with development dependencies:

```bash
git clone https://github.com/psf/black.git
cd black
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Available Scripts

Black includes several utility scripts in the `scripts/` directory to help with development and release tasks:

| Script | Purpose |
|--------|---------|
| `scripts/fuzz.py` | Property-based fuzzing tests for the formatter |
| `scripts/release.py` | Automates changes needed during and after releases |
| `scripts/release_tests.py` | Unit tests for the release versioning logic |
| `scripts/generate_schema.py` | Generates JSON schema for Black's configuration options |
| `scripts/make_width_table.py` | Generates Unicode width table for character width calculations |
| `scripts/migrate-black.py` | Rewrites git history by applying Black to individual commits |
| `scripts/diff_shades_gha_helper.py` | GitHub Actions helper for diff-shades PR analysis |
| `scripts/check_pre_commit_rev_in_example.py` | Validates pre-commit rev consistency in documentation |
| `scripts/check_version_in_basics_example.py` | Checks version consistency in "the_basics.md" documentation |

### Code Organization

The project is organized into three main source packages under `src/`:

- **`black/`** — The core formatting engine, CLI, and configuration
- **`blackd/`** — The HTTP daemon server for formatting code over HTTP
- **`blib2to3/`** — The Python parser (a modified lib2to3) used to parse source code

Key modules within `src/black/` include:

- `__init__.py` — Main CLI entry point and core formatting logic
- `mode.py` — Configuration data structures (`Mode`, `TargetVersion`, `Feature`, `Preview`)
- `linegen.py` — Generates reformatted `Line` objects from the syntax tree
- `lines.py` — Line manipulation utilities and data structures
- `brackets.py` — Tracks bracket depth and delimiter priorities for line splitting
- `comments.py` — Parses and normalizes comments and formatting directives
- `nodes.py` — Utility functions for syntax tree node manipulation
- `trans.py` — String transformers for splitting and merging string literals
- `strings.py` — String manipulation utilities
- `ranges.py` — Handles formatting of specific line ranges
- `cache.py` — Caching of formatted files for performance
- `parsing.py` — Parses source code into syntax trees and validates AST consistency
- `concurrency.py` — Utilities for formatting multiple files concurrently
- `handle_ipynb_magics.py` — Handles IPython magic commands in Jupyter notebooks
- `numerics.py` — Formats numeric literals (hex, octal, scientific notation)
- `output.py` — Styled terminal output and diff generation
- `report.py` — Tracks formatting statistics and reporting
- `files.py` — File system operations and pyproject.toml parsing
- `debug.py` — Debug utilities for inspecting syntax trees
- `rusty.py` — Rust-inspired `Result` types (`Ok`/`Err`)
- `schema.py` — JSON schema access for configuration validation

### Code Style and Linting

Black is itself a code formatter, so we expect all contributions to be formatted with Black! The project also uses:

- **Black** for code formatting (of course!)
- **pytest** for testing

There's no separate linting configuration — Black's formatting is the standard. Just run Black on your changes before committing.

## Testing

Testing is a critical part of contributing to Black. The project has an extensive test suite to ensure formatting correctness and stability.

### Running Tests

```bash
# Run the full test suite
pytest

# Run tests with verbose output
pytest -v

# Run a specific test file
pytest tests/test_black.py

# Run tests with coverage
pytest --cov=src
```

### Test Structure

Tests are located in the `tests/` directory and follow this structure:

- **`tests/conftest.py`** — Pytest configuration, custom command-line options (like `--print-full-tree` and `--print-tree-diff`)
- **`tests/data/cases/`** — Test case files that demonstrate specific formatting scenarios. These are Python files that are formatted and compared against expected output.

The test cases cover a wide range of Python features and edge cases, including:

| Category | Example Files |
|----------|---------------|
| Comments | `comments.py`, `comments2.py`–`comments9.py`, `comments_in_blocks.py`, `comments_in_comprehensions.py` |
| Formatting directives | `fmtonoff.py`–`fmtonoff6.py`, `fmtskip.py`–`fmtskip13.py` |
| String formatting | `fstring.py`, `fstring_quotations.py`, `long_strings__type_annotations.py` |
| Pattern matching | `pattern_matching_simple.py`, `pattern_matching_complex.py`, `pattern_matching_generic.py` |
| PEP features | `pep_572.py`, `pep_604.py`, `pep_646.py`, `pep_654.py`, `pep_701.py` |
| Line ranges | `line_ranges_basic.py`, `line_ranges_diff_edge_case.py`, `line_ranges_fmt_off.py` |
| Docstrings | `docstring.py`, `docstring2.py`, `docstring_newline.py`, `module_docstring_1.py`–`module_docstring_4.py` |
| Context managers | `context_managers_38.py`, `context_managers_39.py`, `context_managers_autodetect_38.py`–`context_managers_autodetect_311.py` |
| Preview mode | `preview_comments7.py`, `preview_long_strings.py`, `preview_hug_parens_with_braces_and_square_brackets.py` |

### Writing New Tests

When adding a new feature or fixing a bug:

1. **Create a test case file** in `tests/data/cases/` with the input code you want to format
2. The test framework will automatically format it and compare against expected output
3. For formatting directive tests (like `# fmt: off`), see existing files like `fmtskip.py` for patterns
4. For preview mode features, use the `preview_` prefix in your test file name

### Testing Best Practices

- Write tests that demonstrate the specific behavior you're adding or fixing
- Include edge cases (empty input, extreme nesting, unusual spacing)
- Test both the "before" and "after" formatting states
- For bug fixes, add a regression test that would have failed before your fix
- Use descriptive test file names that indicate what's being tested

## Contributing

We'd love your help! Here's how you can contribute to Black.

### Where to Start

Not sure where to begin? Here are some ideas:

- **Report bugs** — Open an issue on GitHub with a minimal reproduction case
- **Improve documentation** — Fix typos, clarify explanations, add examples
- **Add test cases** — Cover edge cases that aren't currently tested
- **Fix known issues** — Check the issue tracker for open bugs
- **Implement features** — Look for feature requests and discuss your approach first

### Pull Request Workflow

1. **Fork the repository** on GitHub
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b my-feature-branch
   ```
3. **Make your changes** — follow the code style and add tests
4. **Run tests** to make sure everything passes:
   ```bash
   pytest
   ```
5. **Format your code** with Black:
   ```bash
   black src/ tests/
   ```
6. **Commit your changes** with a clear, descriptive commit message
7. **Push to your fork** and open a pull request against the `main` branch

### Commit Message Conventions

We follow conventional commit style:

- `fix:` — Bug fixes
- `feat:` — New features
- `docs:` — Documentation changes
- `test:` — Adding or modifying tests
- `refactor:` — Code refactoring
- `style:` — Formatting changes
- `chore:` — Maintenance tasks

Example: `fix: handle edge case in bracket matching with nested parentheses`

### Code Review Process

Once you open a pull request:

1. **Automated checks** will run (tests, formatting validation)
2. **Maintainers will review** your code within a few days
3. **Address feedback** by pushing additional commits to your branch
4. **Once approved**, a maintainer will merge your PR

### Reporting Issues

When reporting a bug, please include:

- A minimal, reproducible example of the code that causes the issue
- The expected formatting output
- The actual formatting output (or error message)
- Your Black version (`black --version`)
- Your Python version
- Any relevant configuration (pyproject.toml, etc.)

### Need Help?

- **Chat on Discord** — [Join our Discord server](https://discord.gg/RtVdv86PrH) for real-time help
- **Open a Discussion** — Use GitHub Discussions for questions and ideas
- **Read the docs** — Visit [black.readthedocs.io](https://black.readthedocs.io/en/stable/) for comprehensive documentation

### License

Black is licensed under the MIT License. By contributing, you agree that your contributions will be licensed under the same license.