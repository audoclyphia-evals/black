# Testing Guide

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

> *The uncompromising Python code formatter — tested to stay that way.*

Black's test suite is the backbone of its reliability. With hundreds of test cases covering formatting edge cases, comment handling, line ranges, Jupyter notebook support, and the blackd HTTP server, the suite ensures that every release produces deterministic, stable, and AST-equivalent output. Whether you're fixing a bug or adding a new preview style, the tests are your safety net.

## Testing

### Running the Test Suite

Black uses `pytest` as its test runner. To get started, install the development dependencies and run the full suite:

```bash
# Install Black in editable mode with test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_format.py

# Run tests matching a keyword
pytest -k "preview"
```

### Test Structure and Conventions

The test suite lives in the `tests/` directory and follows a clear structure:

| Path | Purpose |
|------|---------|
| `tests/conftest.py` | Pytest configuration, custom options (`--print-full-tree`, `--print-tree-diff`) |
| `tests/data/cases/` | Input/output test cases for formatting (one file per feature or edge case) |
| `tests/__init__.py` | Package marker |

**Key conventions:**

- **Case files** in `tests/data/cases/` are the primary way formatting behavior is tested. Each file contains Python code that Black formats, and the test framework compares the output against expected results.
- **Test file names** match the feature they cover (e.g., `preview_long_strings.py`, `fmtskip.py`, `line_ranges_basic.py`).
- **Regression tests** are added as new case files when bugs are reported — this ensures the fix stays fixed.
- **Cluster-based testing**: The codebase organizes tests around functional clusters. For example, `Cluster_0` focuses on line range diff edge cases, while `Cluster_1` covers the blackd HTTP server and client functionality.

### Writing New Tests

Adding a new test is straightforward:

1. **Create a case file** in `tests/data/cases/` with a descriptive name, e.g., `my_new_feature.py`.
2. **Write the input code** — the unformatted Python you want Black to process.
3. **Run Black on it** to generate the expected output (the test framework will do this automatically on first run).
4. **Commit both** the input file and the expected output.

For more complex scenarios, you can also write traditional pytest functions in the test modules. The `conftest.py` provides helpful fixtures and options for debugging AST trees during test development.

### Coverage and Quality

While there is no strict coverage percentage threshold enforced by CI, the project maintains a high bar:

- Every formatting feature and preview style has dedicated case files.
- Edge cases (comments in brackets, `fmt: skip` directives, line ranges, etc.) are extensively covered.
- The `assert_stable` function in `src/black/__init__.py` verifies that formatted output doesn't change on a second pass — a core stability guarantee.
- The `assert_equivalent` function ensures that formatted code produces the same AST as the original, preventing semantic changes.

### Debugging Tests

When a test fails, you have several tools at your disposal:

```bash
# Print the full syntax tree for debugging
pytest --print-full-tree tests/data/cases/my_test.py

# Print only the diff between trees
pytest --print-tree-diff tests/data/cases/my_test.py

# Run with very verbose output to see formatting decisions
pytest -vv -k "my_feature"
```

The `DebugVisitor` class in `src/black/debug.py` is also available for programmatic AST inspection during development.

### Fuzzing and Property-Based Testing

For extra rigor, the project includes a fuzzing script at `scripts/fuzz.py`. This runs property-based tests that generate random Python code and verify that Black handles it without crashing and produces stable output. Run it with:

```bash
python scripts/fuzz.py
```

This is especially useful when adding new syntax support or preview features that interact with many language constructs.