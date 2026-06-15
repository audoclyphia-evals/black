# Testing Guide

Your guide to Black's test suite — from running your first test to contributing new test cases.

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

Black's test suite ensures the formatter produces consistent, correct output across a wide range of Python syntax, edge cases, and formatting scenarios. The tests are organized around data-driven test cases located in `tests/data/cases/`, covering everything from basic formatting to complex preview-mode behaviors. This guide will help you understand the testing infrastructure, run existing tests, and write new ones.

---

## Overview

Black uses a **data-driven testing approach**: each test case is a Python file in `tests/data/cases/` that contains both the input code and the expected formatted output. The test runner applies Black to the input, then compares the result against the expected output. This makes it straightforward to add regression tests for specific formatting scenarios — just drop a new `.py` file into the cases directory.

The test suite covers several distinct areas:

- **Formatting correctness** — verifying Black's output matches expectations for hundreds of Python syntax patterns
- **Preview mode features** — testing new formatting behaviors that are gated behind the `preview` flag
- **Edge cases** — boundary conditions like `fmt: skip` directives, line range formatting, and unusual syntax
- **Fuzzing** — property-based tests that catch unexpected formatter crashes or inconsistencies

---

## Test Structure

### Directory Layout

```
tests/
├── __init__.py
├── conftest.py                    # pytest configuration and custom options
└── data/
    └── cases/                     # Data-driven formatting test cases
        ├── annotations.py
        ├── comments.py
        ├── fmtskip.py
        ├── line_ranges_basic.py
        ├── pep_604.py
        ├── preview_long_strings.py
        ├── numeric_literals.py
        └── ...                    # 100+ test case files
```

### Key Test Case Categories

| Category | Example Files | Description |
|----------|--------------|-------------|
| `fmt: skip` handling | `fmtskip.py` through `fmtskip13.py`, `fmtskip_after_bracket_with_comment.py`, `fmtskip_in_parens.py` | Tests that code marked with `# fmt: skip` is left unchanged |
| Redundant parentheses | `pep_572_remove_parens.py`, `pep_572_do_not_remove_parens.py` | Tests removal of unnecessary parentheses in various Python constructs |
| Docstring formatting | `docstring.py`, `docstring2.py`, `docstring_tabs.py`, `no_blank_line_before_docstring.py` | Tests docstring formatting, blank line handling, and style rules |
| Import formatting | `import_line_collapse.py`, `import_spacing.py` | Tests import statement formatting and collapsing behavior |
| Numeric literals | `numeric_literals.py`, `numeric_literals_skip_underscores.py` | Tests formatting of hex, scientific notation, and other numeric formats |
| Line ranges | `line_ranges_basic.py`, `line_ranges_fmt_off.py`, `line_ranges_unwrapping.py` | Tests partial formatting with line range selection |
| Preview mode | `preview_long_strings.py`, `preview_comments7.py`, `preview_hug_parens_with_braces_and_square_brackets.py` | Tests features gated behind the `--preview` flag |
| PEP compliance | `pep_570.py`, `pep_572.py`, `pep_604.py`, `pep_654.py`, `pep_701.py` | Tests formatting of specific PEP syntax features |

### `conftest.py`

The test configuration file at `tests/conftest.py` provides custom pytest command-line options for debugging the AST (Abstract Syntax Tree):

- **`--print-full-tree`** — Prints the complete lib2to3 syntax tree for test cases, useful for understanding how Black parses input
- **`--print-tree-diff`** — Prints a diff of the syntax tree before and after formatting

---

## Running Tests

```bash
# Run the full test suite
pytest

# Run tests for a specific test case
pytest tests/data/cases/comments.py

# Run with verbose output to see individual test names
pytest -v

# Print the AST for a test case (useful for debugging)
pytest --print-full-tree tests/data/cases/numeric_literals.py

# Print the AST diff for a test case
pytest --print-tree-diff tests/data/cases/annotations.py
```

### Fuzzing

Black includes property-based fuzzing tests in `scripts/fuzz.py` that use tools like Hypothesis to generate random inputs and verify the formatter doesn't crash or produce invalid output. These are especially valuable for catching edge cases that hand-written test cases might miss.

---

## How Data-Driven Tests Work

Each file in `tests/data/cases/` is a self-contained test case. The file contains Python code that Black will format, and the test infrastructure verifies the output matches expectations.

For example, a test case for numeric literal formatting might contain:

```python
# Input (what goes in the file)
x = 1000000
y = 0x1A2B3C
z = 1.23e-4

# Black reformats this to...
x = 1_000_000
y = 0x1A2B3C
z = 1.23e-4
```

The test runner applies Black to the source and compares the result against the expected output embedded in the file.

---

## Writing New Tests

To add a new test case for a formatting scenario:

1. **Create a new `.py` file** in `tests/data/cases/` with a descriptive name (e.g., `my_new_feature.py`).

2. **Include both input and expected output** in the file, following the conventions of existing test cases.

3. **Run the test** to verify it passes:

   ```bash
   pytest tests/data/cases/my_new_feature.py -v
   ```

4. **Use the `--print-tree-diff` flag** if your test involves complex syntax structures:

   ```bash
   pytest --print-tree-diff tests/data/cases/my_new_feature.py
   ```

### Naming Conventions

- **`preview_*.py`** — Test cases that exercise preview-mode features
- **`fmtskip*.py`** — Test cases for `# fmt: skip` directive handling
- **`pep_*.py`** — Test cases for PEP-specific syntax formatting
- **`line_ranges_*.py`** — Test cases for line-range formatting
- **`comments*.py`** — Test cases for comment placement and formatting

### Tips for Good Test Cases

- **Keep test cases focused** — each file should test one specific formatting scenario
- **Use realistic code** — while minimal examples are fine, real-world-like code helps catch practical issues
- **Cover edge cases** — test boundary conditions like maximum line length, deeply nested structures, and unusual syntax combinations
- **Name files descriptively** — future contributors should understand what a test covers from its filename

---

## Release Tests

The release automation logic has its own dedicated test suite in `scripts/release_tests.py`. This uses a `TestRelease` class with mocked git tag data to verify version determination logic:

```bash
# Run release-specific tests
pytest scripts/release_tests.py -v
```

These tests mock git tag data using a `FakeDateTime` class to verify:
- Current version extraction from git tags
- Next calendar version calculation
- Handling of edge cases like missing or empty tag lists

---

## Debugging Failing Tests

When a test fails, the test runner will show the difference between Black's actual output and the expected output. To dig deeper:

1. **Inspect the AST** using `--print-full-tree` to understand how Black parsed the input
2. **Compare ASTs** using `--print-tree-diff` to see what changed during formatting
3. **Run Black directly** on the test file with specific options to reproduce the issue

For more details on Black's overall architecture and how the formatting pipeline works, see the [Architecture Guide](ARCHITECTURE.md). For development environment setup, see the [Development Setup Guide](DEVELOPMENT.md).