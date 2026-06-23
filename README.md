# Black

The uncompromising Python code formatter.

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.9+-3776AB.svg?logo=python&logoColor=white)

## Project Overview

Black is a Python code formatter that enforces a consistent style across projects. It provides both a command-line tool for local use and an HTTP server (`blackd`) for remote formatting. The formatter operates on Python source files and Jupyter notebooks, applying opinionated formatting rules with minimal configuration. It parses source code into a syntax tree, applies formatting transformations, and produces standardized output.

The codebase is organized into three main packages:

- **`src/black`** — Core formatting engine, CLI interface, configuration, and output utilities
- **`src/blackd`** — HTTP server and client for remote formatting via REST API
- **`src/blib2to3`** — Python parser (parser generator and syntax tree) used to parse source code before formatting

Supporting infrastructure includes GitHub Actions integration (`action/`), release and schema generation scripts (`scripts/`), and a comprehensive test suite (`tests/`).

## Features

- **Deterministic formatting** — Produces the same output regardless of input style
- **Bracket and comment tracking** — Manages bracket depth and formatting directives like `fmt:off` and `fmt:skip`
- **String transformations** — Merges, splits, and normalizes string literals to fit line length limits
- **Line range formatting** — Formats specific line ranges within source files
- **Jupyter notebook support** — Masks and unmasks IPython magic commands during formatting
- **Concurrent formatting** — Formats multiple files in parallel using multiprocessing
- **File caching** — Avoids reformatting unchanged files by tracking file metadata
- **Preview mode** — Provides access to upcoming style changes before they become default
- **Multiple Python version targeting** — Configurable target versions for version-specific syntax
- **HTTP API server** — Remote formatting via the `blackd` daemon with CORS support (see [HTTP Server Usage](#format-using-the-http-server) below)

## Requirements

- Python 3.9 or higher
- pip (Python package manager)

Optional dependencies for enhanced functionality:

- `colorama` — Colored terminal output
- `d` — Daemon mode for `blackd`
- `uvloop` — Faster event loop for `blackd`

## Installation

Install Black from PyPI using pip:

```bash
pip install black
```

To include optional extras:

```bash
pip install "black[colorama,d,uvloop]"
```

### Docker

A Docker image is available for containerized usage:

```bash
docker build -t black .
docker run black --help
```

The Dockerfile builds from `python:3.13-slim` and installs Black with colorama, daemon, and uvloop extras.

### Verify Installation

```bash
black --version
```

## Quickstart

Here are some common commands to get you started.

Format a single file:

```bash
black my_script.py
```

Format a directory recursively:

```bash
black src/
```

Check formatting without making changes:

```bash
black --check src/
```

Preview changes without applying them:

```bash
black --diff src/
```

For more detailed options and use cases, see the [Usage](#usage) section below.

## Usage

This section covers the primary ways to use Black.

### Format Files In-Place

```bash
black my_module.py utils.py
```

### Specify Line Length

```bash
black --line-length 100 src/
```

### Target a Specific Python Version

```bash
black --target-version py39 src/
```

### Format Using the HTTP Server

Start the `blackd` server:

```bash
python -m blackd --bind 0.0.0.0 --port 45484
```

Format code remotely using the client:

```python
from blackd.client import BlackDClient

client = BlackDClient("http://localhost:45484")
result = client.format_code("x  =  1")
print(result)
```

### Format Jupyter Notebooks

```bash
black --ipynb notebooks/
```

Black handles IPython magic commands by masking them during formatting and restoring them afterward.

### Skip Formatting for Specific Lines

Add `# fmt: off` and `# fmt: on` directives to exclude code sections:

```python
# fmt: off
x = [1,2,3,4,5]
y = {"a": 1,"b": 2}
# fmt: on

# This line will be formatted normally
z = [1, 2, 3]
```

Single-line skips use `# fmt: skip`:

```python
result = some_function(arg1, arg2)  # fmt: skip
```

### Format Specific Line Ranges

```bash
black --line-ranges 10-20 my_script.py
```

## API Documentation

The following is the auto-generated API reference for Black's internal and HTTP interfaces.

openapi: 3.0.3
info:
  title: API Documentation
  description: Auto-generated API documentation
  version: 1.0.0
paths:
  release.get_git_tags:
    patch:
      summary: Tests the logic for determining the next calendar version based on
        git tags.
      description: Documentation generation skipped due to LLM timeout (120s limit
        exceeded)
      operationId: ''
      tags: []
      responses:
        '200':
          description: Success
  /path/:
    get:
      summary: API endpoint with union type query parameter
      description: Documentation generation skipped due to LLM timeout (120s limit
        exceeded)
      operationId: ''
      tags: []
      responses:
        '200':
          description: Success
tags:
- name: Release

## Additional Documentation

For more detailed information, see the following documentation:

- [System Architecture](ARCHITECTURE.md) — Overview of Black's components, their interactions, and design principles
- [Contributing to Black](CONTRIBUTING.md) — Guidelines for setting up the development environment, running tests, and submitting contributions