# Black

The uncompromising Python code formatter

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

Black is a Python code formatter that automatically reformats your code to follow a consistent style, so you can stop arguing about formatting and focus on what matters. It parses your code into an AST, applies formatting transformations, and outputs code that is deterministic and reproducible — no configuration needed.

---

## Features

- **Zero-configuration formatting** — Black makes opinionated style decisions so you don't have to, producing consistent output across your entire codebase.
- **Preview mode** — Opt-in to upcoming style changes including long string splitting, dictionary value formatting, power operator hugging, and parenthesized context managers.
- **Line range formatting** — Format only specific line ranges within a file, useful for formatting changes in version control diffs without touching the rest of the file.
- **`fmt: skip` directive handling** — Exclude specific lines or blocks from formatting using `# fmt: skip` comments, giving you control over edge cases.
- **Redundant parentheses removal** — Automatically strips unnecessary parentheses from expressions, assignments, return annotations, and except clauses.
- **Docstring blank line handling** — Enforces consistent blank line rules inside docstrings, with special handling for `.pyi` stub files.
- **Import line collapse** — Collapses or preserves import formatting based on line length and style preferences.
- **Numeric literal formatting** — Normalizes numeric literals including hex, scientific notation, and underscore separators for readability.
- **Python 3.12+ type parameter support** — Formats the new generic class and function type parameter syntax with proper line breaking and trailing comma handling.
- **blackd HTTP server** — Run Black as an HTTP service for integration with editors, CI pipelines, and other tools that need on-demand formatting.
- **Concurrent formatting** — Formats multiple files in parallel for speed on large codebases.
- **Jupyter notebook support** — Formats code cells within `.ipynb` notebooks, including handling of IPython magic commands.

---

## Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository and development workflows)

---

## Installation

Install Black from PyPI using pip:

```bash
pip install black
```

To install from source, clone the repository and install in development mode:

```bash
git clone https://github.com/psf/black.git
cd black
pip install -e .
```

Verify your installation:

```bash
black --version
```

---

## Quick Start

After installation, you can immediately begin formatting your Python code. Here are some common operations:

Format a single file:

```bash
black my_script.py
```

Format an entire directory:

```bash
black src/
```

Check formatting without making changes (useful in CI):

```bash
black --check src/
```

Format inline from Python:

```python
import black

source = """
x  =  1
y   =    2
z =     3
"""

mode = black.Mode(target_versions={black.TargetVersion.PY312})
formatted = black.format_str(source, mode=mode)
print(formatted)
# x = 1
# y = 2
# z = 3
```

---

## Usage

### Command-Line Interface

The `black` command formats files in place and prints a summary of changes.

```bash
black src/ tests/
```

To generate a diff without modifying files, use the `--diff` flag:

```bash
black --diff my_module.py
```

### Targeting Specific Python Versions

Black can optimize formatting for specific Python versions. Use the `--target-version` flag:

```bash
black --target-version py312 src/
```

Supported versions include `py27`, `py38`, `py39`, `py310`, `py311`, and `py312`.

### Using Preview Features

Enable preview mode to access upcoming style changes, such as long string splitting and dictionary value formatting. These features may become the default in future releases.

```bash
black --preview src/
```

### Using Line Ranges

Format only specific lines within a file with the `--lines` flag:

```bash
black --lines 10-20 my_file.py
```

This is particularly useful when formatting code sections identified by a linter or version control diff.

### Running the HTTP Server (blackd)

The `blackd` server exposes Black's formatting capabilities as a web service, which is useful for editor integrations and CI pipelines. Start the server with:

```bash
python -m blackd
```

Then format code via HTTP requests. For more details, see the [Blackd HTTP API Conceptual Guide](API.md).

---

## Project Overview

Black is organized into three main packages under `src/`:

- **`black`** — The core formatting engine, including parsing, line generation, bracket tracking, string transformations, caching, and configuration management.
- **`blackd`** — An HTTP server that exposes Black's formatting capabilities as a web service, along with a client library.
- **`blib2to3`** — A fork of Python's `lib2to3` parser, providing the grammar definitions, tokenizer, and syntax tree infrastructure that Black uses to parse Python source code.

Supporting directories include `scripts/` for release automation, `action/` for the GitHub Action integration, and `tests/` with an extensive suite of formatting test cases.

---

## 📚 Additional Documentation

For more detailed information, see the following documentation:

- [System Architecture Documentation](ARCHITECTURE.md) — Provides a comprehensive overview of the system's components, their relationships, and data flow.
- [Contribution Guidelines](CONTRIBUTING.md) — Essential for new contributors to understand how to participate in the project.
- [Blackd HTTP API Conceptual Guide](API.md) — Explains how to use the blackd HTTP API at a high level, including request/response patterns and usage examples.
- [Command-Line Interface Reference](CLI.md) — Offers detailed reference for the `black` command-line options and usage patterns.
- [Testing Guide](TESTING.md) — Documents how to run tests, understand test structure, and write new tests.
- [Development Setup and Workflow](DEVELOPMENT.md) — Guides developers through setting up the development environment and workflow for working on the project.

The following diagrams provide visual overviews of Black's architecture and internals:

- [System Architecture](docs/architecture_black_code_formatter_system_architecture.mmd) — High-level component overview.
- [Core Formatting Engine Classes](docs/class_core_formatting_engine_classes.mmd) — Class diagram for core formatting structures.
- [Parser and AST Infrastructure](docs/class_parser_and_ast_infrastructure.mmd) — Class diagram for the `blib2to3` parser.
- [File Formatting Pipeline](docs/sequence_file_formatting_pipeline.mmd) — End-to-end formatting flow sequence.
- [Blackd HTTP Server Flow](docs/sequence_blackd_http_server_flow.mmd) — Request processing flow for the blackd server.