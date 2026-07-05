# Black

> The uncompromising Python code formatter

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg?logo=python&logoColor=white)
![CLI](https://img.shields.io/badge/CLI-available-brightgreen.svg)
![API](https://img.shields.io/badge/API-blackd-orange.svg)

Black is an opinionated Python code formatter that enforces a consistent style across a codebase. It parses Python source code into an AST and reformats it according to a deterministic set of rules, removing the need for developers to argue about style. The formatter supports both a command-line interface and an HTTP daemon (`blackd`) for programmatic access.

---

## Project Overview

Black eliminates style debates by enforcing a single, opinionated formatting standard. It operates by parsing source code into an abstract syntax tree and reformatting it according to a deterministic set of rules.

The project consists of several core components:

- **`src/black/`** — The main formatter engine, including the CLI entry point, code parsing, line generation, string transformations, caching, and configuration management.
- **`src/blackd/`** — An HTTP daemon (`blackd`) that exposes formatting as a web service, along with a client library for interacting with it.
- **`src/blib2to3/`** — A fork of Python's `lib2to3` parser used for parsing Python source into syntax trees.
- **`action/`** — A GitHub Action entrypoint that installs Black and runs it on specified source files for CI/CD integration.
- **`scripts/`** — Utility scripts for release automation, documentation validation, schema generation, and testing.
- **`tests/`** — Comprehensive test suite with numerous test case files covering formatting scenarios.

---

## Features

- **Deterministic formatting** — Produces identical output regardless of the input's original style, ensuring consistency across projects.
- **CLI interface** — Full command-line tool for formatting files, directories, and stdin input.
- **HTTP daemon (`blackd`)** — An HTTP server that accepts code via requests and returns formatted output, enabling integration with editors and CI systems.
- **GitHub Action support** — A ready-to-use GitHub Action (`action/main.py`) that installs Black and runs it on specified source files.
- **Preview mode** — An opt-in mode that enables upcoming formatting features before they become the default.
- **Jupyter notebook support** — Handles IPython magic commands in Jupyter notebook cells for formatting.
- **Caching** — A file system cache (`src/black/cache.py`) avoids reformatting unchanged files.
- **Line range formatting** — Support for formatting specific line ranges within source files.
- **Configuration via `pyproject.toml`** — Reads formatting options from `pyproject.toml` for project-level configuration.
- **Multiple Python version targeting** — Supports targeting specific Python versions (`TargetVersion` enum) to ensure compatibility.

---

## Requirements

- **Python 3.8** or higher
- **pip** (Python package manager)
- **Git** (for cloning the repository and release tooling)
- **build-essential** (on Linux, for compiling dependencies from source)
- **python3-dev** (on Linux, required for building native extensions)

Optional tools:

- **Docker** — A `Dockerfile` is provided for containerized usage.
- **pre-commit** — Black can be integrated as a pre-commit hook.

---

## Installation

### From PyPI

```bash
pip install black
```

### From Source

```bash
git clone https://github.com/psf/black.git
cd black
pip install -e .
```

### With Optional Extras

```bash
# With colorama support
pip install black[colorama]

# With d (diff) and uvloop support
pip install black[d,uvloop]

# With Jupyter notebook support
pip install black[colorama,jupyter]
```

### Docker

```bash
docker build -t black .
docker run --rm -v $(pwd):/code black /code
```

The Docker image is built from `python:3.13-slim` and includes Black with `colorama`, `d`, and `uvloop` extras.

---

## Quick Start

1. **Install Black**:

```bash
pip install black
```

2. **Format a file**:

```bash
black my_script.py
```

3. **Check formatting without modifying files**:

```bash
black --check my_script.py
```

4. **Format a directory**:

```bash
black src/
```

5. **Format from stdin**:

```bash
echo "x  =  1" | black -
```

---

## Usage

### Basic Formatting

Format a single Python file in place:

```bash
black my_module.py
```

Format an entire directory:

```bash
black src/
```

### Check Mode

Verify that files are formatted without making changes (useful in CI):

```bash
black --check src/
```

### Preview Mode

Enable preview features that are not yet part of the default style:

```bash
black --preview my_module.py
```

Preview mode enables experimental formatting behaviors such as long string splitting, dictionary value formatting, and power operator hugging.

### Line Length

Set a custom line length (default is 88):

```bash
black --line-length 100 my_module.py
```

### Target Python Version

Format code targeting a specific Python version:

```bash
black --target-version py38 my_module.py
```

### Formatting Specific Line Ranges

Format only a specific range of lines:

```bash
black --line-ranges 10-20 my_module.py
```

### Using the HTTP Daemon (`blackd`)

Start the `blackd` server:

```bash
python -m blackd
```

Send code for formatting via HTTP:

```bash
curl -X POST http://localhost:4548/ -d 'x  =  1'
```

For detailed API reference, refer to the [`api_documentation.yaml`](api_documentation.yaml) file.

### GitHub Action

The repository includes a GitHub Action (`action/main.py`) for CI/CD integration. It installs Black and runs it on specified source files. Configuration is done via action inputs:

- `with.version` — Specify the Black version to install.
- `with.use_pyproject` — Read the version from `pyproject.toml` (requires Python 3.11+).
- `with.src` — Source files or directories to format.
- `with.options` — Additional Black options.
- `with.jupyter` — Enable Jupyter notebook support.