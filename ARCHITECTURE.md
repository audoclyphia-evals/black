# System Architecture Documentation

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

The uncompromising Python code formatter. Black is an opinionated, deterministic formatter that reformats entire files in place, freeing developers from formatting debates and producing consistent, readable code across any project.

## Architecture

Black's architecture is organized around a multi-stage formatting pipeline that transforms raw Python source code into a consistently formatted output. The system is composed of several collaborating modules, each with a distinct responsibility.

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

The formatting pipeline processes source code through three major phases:

1. **Parsing** — Raw source is tokenized and parsed into a concrete syntax tree (CST) using a custom fork of lib2to3 (`blib2to3`). This CST preserves whitespace and comments, unlike an AST.
2. **Line Generation** — The CST is walked by a `LineGenerator` visitor that produces `Line` objects. Each `Line` represents a logical line of formatted output, with leaves and attached comments. During this phase, the generator makes decisions about line splitting, bracket handling, and comment placement.
3. **Line Splitting and Output** — Lines that exceed the configured line length are split. String transformers (`StringMerger`, `StringSplitter`, `StringParenStripper`) handle string literal merging and splitting. The final lines are concatenated into the formatted output.

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

```text
┌──────────┐    ┌──────────────┐    ┌───────────┐    ┌──────────┐
│  Source  │───▶│   blib2to3   │───▶│  LineGen  │───▶│  Lines   │
│  Code    │    │   (parse)    │    │ (walk)    │    │ (split)  │
└──────────┘    └──────────────┘    └───────────┘    └──────────┘
                                                           │
                                                    ┌──────▼──────┐
                                                    │  Formatted  │
                                                    │   Output    │
                                                    └─────────────┘
```

### Key Components and Their Responsibilities

| Component | Module | Responsibility |
|-----------|--------|----------------|
| **BracketTracker** | `src/black/brackets.py` | Tracks bracket depth and delimiter priorities for line splitting decisions |
| **BracketMatchError** | `src/black/brackets.py` | Exception raised when bracket matching fails |
| **ProtoComment** | `src/black/comments.py` | Represents a comment in the syntax tree, storing type, value, whitespace, and newline information |
| **LineGenerator** | `src/black/linegen.py` | Generates reformatted `Line` objects from the CST, handling various Python constructs |
| **Line** | `src/black/lines.py` | Holds leaves and comments for a single line of code |
| **EmptyLineTracker** | `src/black/lines.py` | Calculates extra empty lines needed before and after each processed line |
| **Mode** | `src/black/mode.py` | Stores configuration settings: target versions, line length, feature flags |
| **TargetVersion** | `src/black/mode.py` | Defines supported Python versions for formatting |
| **Feature** | `src/black/mode.py` | Enumeration of Python language features supported by the formatter |
| **Preview** | `src/black/mode.py` | Individual preview style features for gradual opt-in |
| **Cache** | `src/black/cache.py` | Manages file system cache to avoid reformatting unchanged files |
| **StringTransformer** | `src/black/trans.py` | Abstract base for string merging, splitting, and parenthesis stripping |
| **StringMerger** | `src/black/trans.py` | Merges adjacent strings or removes backslash continuations |
| **StringSplitter** | `src/black/trans.py` | Splits atom strings to fit within line length |
| **DebugVisitor** | `src/black/debug.py` | Pretty-prints CST with indentation and color coding for debugging |
| **Report** | `src/black/report.py` | Tracks reformatting statistics and provides reporting |
| **Visitor** | `src/black/nodes.py` | Base visitor class for traversing lib2to3 syntax trees |
| **Ok / Err** | `src/black/rusty.py` | Result types inspired by Rust error handling |
| **BlackDClient** | `src/blackd/client.py` | HTTP client for the blackd server |
| **FileData** | `src/black/cache.py` | Stores metadata about a file for caching purposes |

### Formatting a Single File

When Black formats a file, the following sequence occurs:

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

1. The `reformat_one` function (in `src/black/__init__.py`) is called with the file path, mode, and options.
2. It checks the cache (if enabled and not in diff mode) to skip unchanged files.
3. The source is read, parsed by `blib2to3`, and fed through `_format_str_once`.
4. The formatted output is validated for stability (a second pass produces identical output) and, in safe mode, AST equivalence.
5. The result is written back according to the `WriteBack` strategy (in-place, diff, check, or color-diff).

### Configuration Loading

Black discovers configuration from `pyproject.toml`, a user-level config file, or command-line arguments. The `Mode` dataclass consolidates all formatting settings.

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

### Blackd HTTP Server

The `src/blackd/` package provides a lightweight aiohttp-based HTTP server that formats code on demand. It supports protocol version 1, configurable Python variants via headers, and CORS middleware for cross-origin requests from web clients.

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

The server's `handle` coroutine (in `src/blackd/__init__.py`) reads the request body, parses formatting options from headers, invokes the core formatting engine, and returns the result. Errors produce appropriate HTTP status codes (204 for no change, 400 for invalid input, 501 for unsupported protocol versions).

### Cache Management

The `Cache` class in `src/black/cache.py` avoids reformatting files whose content hasn't changed. It uses a hash of the file contents combined with the formatting mode to detect staleness.

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

### Safety Guarantees

Black provides two levels of safety:
- **Stable formatting** — The `assert_stable` function runs a second formatting pass to verify the output doesn't change.
- **AST equivalence** — In safe mode (`--safe`), `assert_equivalent` parses both the original and formatted code into ASTs and compares their stringified forms, ensuring no semantic changes.

## Project Structure

```
black/
├── action/                   # GitHub Action entrypoint
│   └── main.py               # Installs Black and runs it on specified sources
├── docs/                     # Sphinx documentation configuration
│   └── conf.py
├── profiling/                # Profiling test data
│   └── mix_small.py
├── scripts/                  # Development and release utilities
│   ├── diff_shades_gha_helper.py   # GitHub Actions integration with diff-shades
│   ├── release.py                  # Release automation (version bumping, changelog)
│   ├── release_tests.py            # Tests for release logic
│   ├── fuzz.py                     # Property-based fuzzing tests
│   ├── generate_schema.py          # JSON schema generation for config
│   ├── make_width_table.py         # Unicode width table generation
│   ├── migrate-black.py            # Git history rewriting tool
│   └── check_*.py                  # Documentation version consistency checks
├── src/
│   ├── black/                # Core formatter library
│   │   ├── __init__.py       # Main CLI and public API (format_str, format_file_in_place)
│   │   ├── __main__.py       # Entry point for `python -m black`
│   │   ├── brackets.py       # Bracket depth tracking and delimiter priority
│   │   ├── cache.py          # File system cache (FileData, Cache)
│   │   ├── comments.py       # Comment parsing and normalization (ProtoComment)
│   │   ├── concurrency.py    # Parallel file formatting (multiprocessing)
│   │   ├── const.py          # Default configuration constants
│   │   ├── debug.py          # CST pretty-printing (DebugVisitor)
│   │   ├── files.py          # File system operations, pyproject.toml parsing
│   │   ├── handle_ipynb_magics.py  # IPython magic masking for Jupyter cells
│   │   ├── linegen.py        # Line generation from CST (LineGenerator)
│   │   ├── lines.py          # Line data structures (Line, EmptyLineTracker, LinesBlock)
│   │   ├── mode.py           # Configuration (Mode, TargetVersion, Feature, Preview)
│   │   ├── nodes.py          # AST node transformation utilities (Visitor)
│   │   ├── numerics.py       # Numeric literal formatting (hex, octal, scientific)
│   │   ├── output.py         # Terminal output, diffs, file dumping
│   │   ├── parsing.py        # Source parsing and AST validation
│   │   ├── ranges.py         # Line range formatting (_LinesMapping, _TopLevelStatementsVisitor)
│   │   ├── report.py         # Formatting statistics and reporting (Report, Changed)
│   │   ├── resources/        # Static resources
│   │   ├── rusty.py          # Result types (Ok, Err)
│   │   ├── schema.py         # JSON configuration schema access
│   │   ├── strings.py        # String utility functions
│   │   ├── trans.py          # String transformers (StringMerger, StringSplitter, etc.)
│   │   └── _width_table.py   # Unicode character width table
│   ├── blackd/               # HTTP formatting server
│   │   ├── __init__.py       # Request handling, header parsing (HeaderError, InvalidVariantHeader)
│   │   ├── __main__.py       # Server CLI entry point
│   │   ├── client.py         # HTTP client (BlackDClient)
│   │   └── middlewares.py    # CORS middleware
│   └── blib2to3/             # Fork of lib2to3 parser
│       ├── pygram.py         # Python grammar export
│       ├── pytree.py         # Syntax tree node structures
│       └── pgen2/            # Parser generator engine
│           ├── driver.py     # High-level parsing interface
│           ├── grammar.py    # Grammar data structures
│           ├── parse.py      # Parser engine
│           ├── token.py      # Token constants
│           ├── tokenize.py   # Tokenizer
│           ├── conv.py       # C grammar conversion
│           └── literals.py   # String literal evaluation
├── tests/                    # Test suite
│   ├── conftest.py           # Pytest configuration
│   ├── data/cases/           # Hundreds of formatted/unformatted test cases
│   │   ├── preview_*         # Preview mode formatting tests
│   │   ├── fmtonoff*.py      # fmt: on/off directive tests
│   │   ├── fmtskip*.py       # fmt: skip directive tests
│   │   ├── line_ranges_*.py  # Line range formatting tests
│   │   ├── pep_*.py          # PEP-specific feature tests
│   │   ├── pattern_matching_*.py
│   │   ├── comments*.py      # Comment handling tests
│   │   └── ...               # Many more feature-specific test files
│   └── data/line_ranges_formatted/  # Expected outputs for line range tests
└── Dockerfile                # Container definition
```

### Key Directories Explained

- **`src/black/`** — The heart of the formatter. Contains the main formatting pipeline, configuration, caching, and all formatting logic from bracket tracking to string splitting.
- **`src/blackd/`** — A companion HTTP server that exposes Black's formatting capabilities over HTTP. Useful for editor integrations, web services, and CI pipelines.
- **`src/blib2to3/`** — A maintained fork of Python's `lib2to3` parser. Provides the CST parser that preserves whitespace and comments, which is essential for a formatter that must reproduce semantically identical code.
- **`tests/data/cases/`** — A comprehensive collection of test cases covering every formatting feature, edge case, and preview mode option. Each file is formatted and compared against a known-good output.
- **`scripts/`** — Developer utilities for release management, schema generation, documentation validation, and fuzzing.
- **`action/`** — A GitHub Action wrapper that installs Black and runs it on user-specified source files, with optional Jupyter support and version pinning.

For detailed information on setting up a development environment, running tests, and contributing, see the [Development Setup](DEVELOPMENT.md) and [Contributing Guidelines](CONTRIBUTING.md). The [Testing Guide](TESTING.md) provides comprehensive information about the test suite and how to write new tests.

## License

MIT