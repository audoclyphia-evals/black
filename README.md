#Black

The uncompromising Python code formatter.

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

Black is a deterministic, opinionated Python code formatter that frees you from hand-formatting minutiae. By running Black on your code, you get consistent formatting across all projects, smaller diffs in code reviews, and zero time spent arguing about style. It supports Python 3.8+ and works beautifully in editors, CI pipelines, and pre-commit hooks.

[Chat on Discord](https://discord.gg/RtVdv86PrH) · [Documentation](https://black.readthedocs.io/en/stable/) · [Latest Release](https://github.com/psf/black/releases/latest)

> “Any color you like.” — Black is opinionated so you don't have to be.

---

## ✨ Features

- **Deterministic formatting** — Black always produces the same output for the same input, no configuration debates needed
- **Fast and stable** — Reformats files in-place with a guaranteed stable output (idempotent)
- **Preview mode** — Opt into the latest formatting styles with `--preview` to see upcoming changes
- **Line-range formatting** — Format only specific line ranges with `--line-ranges`, perfect for partial file formatting
- **Jupyter notebook support** — Formats `.ipynb` files, handling IPython magic commands transparently
- **`fmt: off` / `fmt: on` directives** — Exclude blocks of code from formatting with inline comments
- **CLI and HTTP API** — Use the `black` command-line tool or the `blackd` HTTP server for editor integration
- **GitHub Action** — Ready-to-use action for CI workflows that installs Black automatically
- **pyproject.toml configuration** — Configure Black's options like line length and target versions in your project's config file
- **Caching** — Avoids reformatting unchanged files by caching formatted file signatures

---

## Requirements

- **Python 3.8 or higher** — Black runs on CPython 3.8+
- **pip** (Python package manager) — for installation
- **Git** — recommended for version control integration and pre-commit hooks

## Installation

Install Black from PyPI using pip:

```bash
pip install black
```

To install with Jupyter notebook support:

```bash
pip install "black[jupyter]"
```

To install for development (from source):

```bash
git clone https://github.com/psf/black.git
cd black
pip install -e ".[dev]"
```

To verify the installation:

```bash
black --version
```

## 🚀 Quick Start

Format a single Python file or entire directory in seconds:

```bash
# Format a single file and check the diff
black --diff my_script.py

# Format a file in-place
black my_script.py

# Format an entire directory
black src/

# Check if files are formatted correctly (exit code only)
black --check src/
```

---

## Usage

### Format a single file

```bash
black my_script.py
```

### Format with a custom line length

```bash
black --line-length 100 my_script.py
```

### Preview upcoming formatting styles

```bash
black --preview src/
```

### Exclude specific files or patterns

```bash
black --exclude "/(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|_build|buck-out|build|dist)/" src/
```

### Use in pre-commit hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        language_version: python3.12
```

### Format via the blackd HTTP server

```bash
# Start the server
blackd --bind-host 127.0.0.1 --bind-port 45484

# Send code to format (example with curl)
curl --data 'x=1' http://127.0.0.1:45484
```

### Format specific line ranges

```bash
# Only format lines 10 through 20
black --line-ranges 10-20 my_script.py
```

### Use with IPython/Jupyter notebooks

```bash
black --jupyter notebook.ipynb
```

### Safe mode and stability

By default, Black runs in safe mode, which verifies that the formatted output is AST-equivalent to the original source. Use `--fast` to skip this check for faster formatting:

```bash
black --fast src/
```

---

## Overview

Black is a single-purpose tool: it reformats Python code to conform to a consistent, uncompromising style. The codebase is organized into three main packages under `src/`:

- **`black/`** — The core formatting engine, CLI, configuration, caching, and file handling. This is where the parsing, line generation, bracket tracking, comment normalization, string transformation, and numeric literal formatting logic lives. It also includes a Rust-inspired `Ok`/`Err` result type (`rusty.py`) for structured error handling.
- **`blackd/`** — An aiohttp-based HTTP server that exposes Black's formatting capabilities as a web API, complete with CORS middleware and a Python client for editor integration.
- **`blib2to3/`** — A vendored, modified version of Python's lib2to3 parser and tokenizer, which Black uses to parse source code into syntax trees.

Supporting these are scripts under `scripts/` for release automation (including calendar versioning from git tags), documentation validation, JSON schema generation for configuration, and fuzzing. A GitHub Action lives in `action/` for CI integration, with automatic version detection from git tags or pyproject.toml. The exhaustive test suite lives in `tests/` with hundreds of case files covering edge cases from docstrings and comments to pattern matching and f-strings.

### Architecture Diagram

```mermaid
flowchart TB
    %% Architecture diagram for Black code formatter
    %% Source: Context #2, #3, #4

    subgraph External_Entry_Points [External Entry Points]
        user([User / Developer]) -->|CLI command| cli[black CLI]
        user -->|HTTP request| blackd[blackd HTTP Server]
        gh_action[GitHub Action] -->|automated run| cli
    end

    subgraph Core_Formatting_Engine [Core Formatting Engine]
        cli[black CLI] -->|invokes| format_engine[Format Engine]
        blackd -->|invokes| format_engine
        format_engine -->|parses| parser[blib2to3 Parser]
        format_engine -->|line generation| linegen[Line Generator]
        format_engine -->|bracket tracking| brackets[Bracket Tracker]
        format_engine -->|comment handling| comments[Comment Handler]
        format_engine -->|string transforms| trans[String Transformer]
        format_engine -->|numeric formatting| numerics[Numeric Formatter]
        format_engine -->|ipynb support| ipynb[IPython Magics Handler]
        format_engine -->|range formatting| ranges[Range Formatter]
    end

    subgraph Supporting_Modules [Supporting Modules]
        format_engine -->|file ops| files[File Handler]
        format_engine -->|cache| cache[Cache Manager]
        format_engine -->|output| output[Output / Reporter]
        format_engine -->|config| mode[Mode Config]
        format_engine -->|parsing| parsing[Parsing Utilities]
        format_engine -->|concurrency| concurrency[Concurrency Handler]
    end

    subgraph Storage [Storage]
        cache -->|reads/writes| cache_db[(File System Cache)]
        files -->|reads| pyproject[(pyproject.toml)]
    end

    subgraph Testing_and_Scripts [Testing & Scripts]
        tests[Test Suites] -->|test| format_engine
        scripts[Utility Scripts] -->|automate| format_engine
    end
```

### Core Formatting Pipeline

```mermaid
classDiagram
    direction TB

    %% Group by module namespace (source files)
    
    namespace mode {
        class Mode {
        }
        class TargetVersion {
            <<Enumeration>>
        }
        class Feature {
            <<Enumeration>>
        }
        class Preview {
            <<Enumeration>>
        }
    }

    namespace lines {
        class Line {
        }
        class RHSResult {
        }
        class LinesBlock {
        }
        class EmptyLineTracker {
        }
    }

    namespace linegen {
        class LineGenerator {
        }
        class CannotSplit {
            <<Exception>>
        }
    }

    namespace brackets {
        class BracketTracker {
        }
        class BracketMatchError {
            <<Exception>>
        }
    }

    namespace trans {
        class CannotTransform {
            <<Exception>>
        }
        class CustomSplitMapMixin {
            <<Mixin>>
        }
        class StringTransformer {
            <<Abstract>>
        }
        class BaseStringSplitter {
            <<Abstract>>
        }
        class StringSplitter {
        }
        class StringMerger {
        }
        class StringParenStripper {
        }
    }

    %% Inheritance relationships (evidenced by hierarchy data)
    CannotSplit --|> CannotTransform
    StringMerger --|> StringTransformer
    StringMerger --|> CustomSplitMapMixin
    StringParenStripper --|> StringTransformer
    BaseStringSplitter --|> StringTransformer
    StringSplitter --|> BaseStringSplitter
    StringSplitter --|> CustomSplitMapMixin

    %% Association / usage relationships (inferred from purposes)
    LineGenerator --> Mode : configures formatting
    LineGenerator --> Line : generates
    Line --> BracketTracker : tracks brackets
    Line --> RHSResult : split result
    EmptyLineTracker --> LinesBlock : manages blocks
    EmptyLineTracker --> Line : processes
    LinesBlock --> Mode : stored config
    BracketTracker ..> BracketMatchError : raises
    LineGenerator ..> CannotSplit : raises
```

### Formatting a Python File Flow

```mermaid
sequenceDiagram
    autonumber
    %% Diagram: Formatting a Python File Flow in Black

    box "CLI Orchestration"
        participant Main as "main()"
        participant Sources as "get_sources()"
    end

    box "Per-File Processing"
        participant ReformatOne as "reformat_one()"
        participant FileInPlace as "format_file_in_place()"
        participant FileContents as "format_file_contents()"
    end

    box "Formatting Engine"
        participant FormatStr as "format_str()"
        participant FormatOnce as "_format_str_once()"
        participant Parser as "lib2to3_parse()"
    end

    Main->>Sources: get_sources(root, src, ...)
    Sources-->>Main: sources (set of Paths)
    note over Main,Sources: Compute file set using include/exclude patterns

    loop for each source path
        Main->>+ReformatOne: reformat_one(src, mode, report)
        ReformatOne->>+FileInPlace: format_file_in_place(src, mode, write_back)
        note over FileInPlace: Checks .pyi suffix, sets mode.is_pyi

        FileInPlace->>+FileContents: format_file_contents(contents, mode, fast)
        note over FileContents: Handles .ipynb vs .py#59; calls format_str for Python

        FileContents->>+FormatStr: format_str(contents, mode)
        note over FormatStr: Public entry point for string formatting

        FormatStr->>+FormatOnce: _format_str_once(contents, mode) [first pass]
        FormatOnce->>+Parser: lib2to3_parse(normalized)
        note over FormatOnce: Also calls decode_bytes() before parse
        Parser-->>-FormatOnce: CST (concrete syntax tree)
        FormatOnce->>FormatOnce: Generate lines from CST
        FormatOnce-->>-FormatStr: formatted string

        alt stability check (repeat if unstable)
            FormatStr->>+FormatOnce: _format_str_once(result, mode) [second pass]
            FormatOnce->>+Parser: lib2to3_parse(...)
            Parser-->>-FormatOnce: CST
            FormatOnce-->>-FormatStr: final string
        end

        FormatStr-->>-FileContents: formatted string
        FileContents-->>-FileInPlace: formatted string

        FileInPlace->>FileInPlace: Write back or produce diff (based on WriteBack)
        FileInPlace-->>-ReformatOne: changed (bool)
        ReformatOne-->>-Main: result
    end
```

### Blackd Server Request Handling

```mermaid
sequenceDiagram
    autonumber
    participant Client as "HTTP Client"
    participant BlackdServer as "Blackd Server"
    participant BlackCore as "black.format_str"

    %% Source: src/blackd/__init__.py defines handle and parse_mode (Context #4)
    %% Source: src/black/__init__.py contains format_str (Context #2)

    Client->>+BlackdServer: POST / (source code, headers)
    note over BlackdServer: Parse headers: X-Line-Length, X-Mode, X-Python-Variant, X-Fast, X-Diff
    BlackdServer->>BlackdServer: parse_mode(headers) → black.Mode
    BlackdServer->>+BlackCore: format_str(source, mode, line_range)
    BlackCore-->>-BlackdServer: formatted_code
    alt No formatting needed (input unchanged)
        BlackdServer-->>Client: 204 No Content
    else Formatting applied
        alt X-Diff header present
            BlackdServer->>BlackdServer: Compute unified diff
            BlackdServer-->>Client: 200 OK (diff)
        else
            BlackdServer-->>Client: 200 OK (formatted_code)
        end
    else Invalid request (e.g., bad header)
        BlackdServer-->>Client: 400 Bad Request
    end
```

### Cache Management

```mermaid
classDiagram
    direction TB

    %% Source: Context #5 (cache.py file details)
    namespace cache {
        class FileData {
            <<NamedTuple>>
        }
        class Cache {
            <<dataclass>>
        }
        class get_cache_dir {
            <<Function>>
        }
        class get_cache_file {
            <<Function>>
        }
    }

    %% Relationships grounded in context (Cache uses FileData, depends on helper functions)
    Cache --> FileData : uses
    Cache ..> get_cache_file : depends on
    Cache ..> get_cache_dir : depends on
```

### Configuration Loading

```mermaid
sequenceDiagram
    %% Configuration Loading Flow for Black
    %% Based on context #3 and #4: read_pyproject_toml, spellcheck_pyproject_toml_keys, validate_regex, parse_pyproject_toml, find_pyproject_toml, _load_toml, find_user_pyproject_toml
    
    autonumber
    
    participant Click as "Click CLI"
    participant Read as "read_pyproject_toml"
    participant Find as "find_pyproject_toml"
    participant Parse as "parse_pyproject_toml"
    participant Load as "_load_toml"
    participant Spell as "spellcheck_pyproject_toml_keys"
    participant Validate as "validate_regex"
    
    Click->>+Read: read_pyproject_toml(ctx, param, value)
    alt value is None
        Read->>+Find: find_pyproject_toml(src, stdin_filename)
        Find->>Find: find_project_root(path_search_start)
        alt pyproject.toml exists in project root
            Find-->>Read: path to pyproject.toml
        else not found
            Find->>Find: find_user_pyproject_toml()
            alt user config exists
                Find-->>Read: path to user config
            else not found
                Find-->>Read: None
            end
        end
    end
    opt value is not None
        Read->>+Parse: parse_pyproject_toml(value)
        Parse->>+Load: _load_toml(path)
        Load-->>-Parse: parsed TOML dict
        Parse->>Parse: extract tool.black config
        Parse->>Parse: infer target_version if missing
        Parse-->>-Read: config dict
        Read->>+Spell: spellcheck_pyproject_toml_keys(ctx, config_keys, path)
        Spell->>Spell: compare keys against ctx.command.params
        alt invalid keys found
            Spell-->>Read: print warning
        else all valid
            Spell-->>Read: no action
        end
        Read->>Read: inject config into ctx.default_map
    end
    Read-->>-Click: config file path or None
    
    Click->>+Validate: validate_regex(ctx, param, value)
    alt value is not None
        Validate->>Validate: re_compile_maybe_verbose(value)
        alt regex is valid
            Validate-->>Click: compiled Pattern
        else regex error
            Validate-->>Click: raise click.BadParameter
        end
    else value is None
        Validate-->>Click: None
    end
```

---

## 📚 Additional Documentation

For more detailed information, refer to the following resources:

- **Official documentation** – [Read the Docs](https://black.readthedocs.io/en/stable/) provides comprehensive guides, usage examples, and API reference.
- **Source code** – The repository itself contains inline comments and docstrings that explain module purposes, especially in `src/black/`, `src/blackd/`, and `src/blib2to3/`.
- **Contribution guidelines** – See [CONTRIBUTING.md](https://github.com/psf/black/blob/main/CONTRIBUTING.md) for setup, coding standards, and testing practices.
- **Command-line reference** – Run `black --help` or consult the CLI section of the official documentation for all options.