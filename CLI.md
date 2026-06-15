# Command-Line Interface Reference

> The uncompromising Python code formatter

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

Black is a Python code formatter that enforces a consistent style by parsing and re-formatting your code. It provides two primary CLI commands: `black` for formatting Python files directly, and `blackd` for running an HTTP formatting server. Configuration is managed through command-line options or a `pyproject.toml` file, and Black supports targeting specific Python versions, line range formatting, preview-mode features, and more.

---

## Overview

Black's CLI offers two entry points:

| Command | Module | Purpose |
|---------|--------|---------|
| `black` | `src/black/__main__.py` | Formats Python source files in-place, as a diff, or in check mode |
| `blackd` | `src/blackd/__main__.py` | Runs an HTTP server that accepts Python code and returns formatted output |

At its core, the `black` command uses the [`Mode`](src/black/mode.py) class to store all formatting configuration — target Python versions, line length, preview features, and more. Output behavior is controlled by the [`WriteBack`](src/black/__init__.py) enum, which determines whether formatted code is written back to files, displayed as a diff, or checked without modifying files.

For a deeper understanding of how the formatting pipeline works end-to-end, see [Architecture](ARCHITECTURE.md). For configuration file setup, see [Development Setup](DEVELOPMENT.md).

---

## CLI Reference

### `black`

The primary command for formatting Python source code. Black parses your source into a syntax tree using its bundled [`blib2to3`](src/blib2to3/) parser, applies formatting rules, and writes the result back.

```bash
black [OPTIONS] [SRC ...]
```

**Core Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `SRC` | One or more files or directories to format | — |
| `--check` | Don't write changes, just return the exit code. Exit code 0 means no changes needed. | Off |
| `--diff` | Don't write changes, print a diff showing what would change | Off |
| `--color` / `--no-color` | Show colored output (when supported by terminal) | Auto-detected |

**Configuration Options** (also settable via [`pyproject.toml`](src/black/files.py)):

| Option | Description | Default |
|--------|-------------|---------|
| `--line-length` / `-l` | Maximum characters per line | Defined in [`src/black/const.py`](src/black/const.py) |
| `--target-version` / `-t` | Target Python version(s). Can be specified multiple times. Values from [`TargetVersion`](src/black/mode.py) enum | All supported versions |
| `--preview` | Enable preview style features as defined in the [`Preview`](src/black/mode.py) enum | Off |
| `--no-preview` | Disable preview style features | — |

**Line Range Formatting** (implemented in [`src/black/ranges.py`](src/black/ranges.py)):

| Option | Description |
|--------|-------------|
| `--line-ranges` | Format only the specified line ranges (e.g., `--line-ranges 10-20`) |

**Caching** (managed by [`Cache`](src/black/cache.py)):

| Option | Description | Default |
|--------|-------------|---------|
| `--cache-dir` | Directory for the cache used to avoid reformatting unchanged files | Platform-dependent |
| `--no-cache` | Do not use the cache | Off |

**Output Control:**

| Option | Description | Default |
|--------|-------------|---------|
| `--output-file` | Write output to this file instead of stdout (when not formatting in-place) | — |
| `--force-exclude` | Exclude paths even if they match patterns from config | Off |

**`--check` and `--diff`** are mutually useful for CI pipelines — `--check` gates whether Black would make changes, and `--diff` shows exactly what would change without modifying files.

---

### `blackd`

An HTTP server that provides Black formatting as a service. Powered by [`aiohttp`](src/blackd/__init__.py), with CORS support via [`middlewares.py`](src/blackd/middlewares.py) and a corresponding [`BlackDClient`](src/blackd/client.py).

```bash
blackd [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | Host address to bind to | `127.0.0.1` |
| `--port` | Port number to listen on | `4548` |
| `--bind` | Alternative way to specify host and port | — |

The server accepts Python source code via HTTP requests and returns the formatted output. It supports configuration through HTTP headers corresponding to the formatting options available in the `black` command. For a detailed conceptual guide, see [Blackd HTTP API](API.md).

---

## Usage

### Basic Formatting

Format a single file in-place:

```bash
black my_script.py
```

Format all Python files in a directory:

```bash
black src/
```

### Check Without Modifying

Use `--check` in CI pipelines to verify code is already formatted:

```bash
black --check src/
# Exit code 0 = all files formatted
# Exit code 1 = some files need formatting
```

Preview what Black would change without writing:

```bash
black --diff my_script.py
```

### Line Range Formatting

Format only a specific range of lines — useful when you've changed only part of a file:

```bash
black --line-ranges 10-25 my_script.py
```

This is implemented in [`src/black/ranges.py`](src/black/ranges.py) and converts unchanged top-level statements to `STANDALONE_COMMENT` nodes to speed up processing. Test cases covering edge cases like decorators, fmt:off overlap, and exceeding ranges are in the [`tests/data/cases/line_ranges_*.py`](tests/data/cases/) files.

### Targeting Specific Python Versions

Restrict formatting to syntax compatible with specific Python versions:

```bash
black --target-version py38 --target-version py39 src/
```

The `TargetVersion` enum in [`src/black/mode.py`](src/black/mode.py) defines all supported versions.

### Using Preview Mode

Enable preview-style formatting features for access to newer style changes:

```bash
black --preview src/
```

Preview features — including long string splitting, dictionary value formatting, and power operator hugging — are individually controlled via the [`Preview`](src/black/mode.py) enum. Test cases for preview features live in `tests/data/cases/preview_*.py`.

### Configuration via `pyproject.toml`

Black reads configuration from `pyproject.toml` automatically, handled by [`src/black/files.py`](src/black/files.py). Example:

```toml
[tool.black]
line-length = 88
target-version = ["py38", "py39"]
preview = true
```

A JSON schema for all configuration options is available via [`src/black/schema.py`](src/black/schema.py) and can be generated with [`scripts/generate_schema.py`](scripts/generate_schema.py).

### Running the blackd HTTP Server

Start the formatting server:

```bash
blackd
# or with options:
blackd --host 0.0.0.0 --port 8080
```

The server supports CORS requests through the middleware in [`src/blackd/middlewares.py`](src/blackd/middlewares.py). A Python client is available in [`src/blackd/client.py`](src/blackd/client.py) for programmatic access.

---

## Formatting Features

Black handles a wide range of formatting scenarios. Key capabilities include:

- **`fmt: skip` directives** — Exclude specific lines or blocks from formatting (tested extensively in [`tests/data/cases/fmtskip*.py`](tests/data/cases/)).
- **Redundant parentheses removal** — Strips unnecessary parentheses from assignments, conditionals, and function returns (see [`tests/data/cases/pep_572_remove_parens.py`](tests/data/cases/pep_572_remove_parens.py)).
- **Docstring blank line handling** — Normalizes blank lines within docstrings, including `.pyi` files (see [`tests/data/cases/pyi_docstring_blank_lines_no_preview.py`](tests/data/cases/pyi_docstring_blank_lines_no_preview.py)).
- **Import line collapse** — Collapses import lines where appropriate (see [`tests/data/cases/import_line_collapse.py`](tests/data/cases/import_line_collapse.py)).
- **Numeric literal formatting** — Normalizes numeric literals (hex, scientific notation, underscores) (see [`tests/data/cases/numeric_literals.py`](tests/data/cases/numeric_literals.py)).
- **Long string splitting** — Intelligent splitting of long string literals to fit within line length (see [`tests/data/cases/preview_long_strings.py`](tests/data/cases/preview_long_strings.py)).
- **Line range formatting** — Format only specific lines, with edge-case handling for decorators, fmt:off blocks, and indentation (see [`tests/data/cases/line_ranges_*.py`](tests/data/cases/)).

---

## Additional Documentation

For more details on related topics, check out these companion guides:

- [Architecture](ARCHITECTURE.md) — System components, data flow, and module relationships
- [Contributing](CONTRIBUTING.md) — Development workflow, coding standards, and PR process
- [Blackd HTTP API](API.md) — Conceptual guide to the HTTP formatting server
- [Testing Guide](TESTING.md) — How to run and write tests
- [Development Setup](DEVELOPMENT.md) — Environment setup and common tasks