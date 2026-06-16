# Command-Line Interface Reference

![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

> “Any color you like.”

Black is the uncompromising Python code formatter. By using it, you agree to cede control over minutiae of hand-formatting. In return, Black gives you speed, determinism, and freedom from `pycodestyle` nagging about formatting. You will save time and mental energy for more important matters.

## CLI Reference

Black is primarily used through its command-line interface. The `black` command formats Python code according to a deterministic set of rules, producing the smallest diffs possible and ensuring consistent style across your entire project.

### Basic Command

```bash
black [options] [FILE...]
```

Format one or more Python files, or read from stdin by passing `-` as the filename.

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `-l, --line-length` | How many characters per line to allow | `88` |
| `-t, --target-version` | Python versions that should be supported (e.g., `py39`, `py310`) | (inferred) |
| `--pyi` | Format as a `.pyi` stub file | `false` |
| `--ipynb` | Format Jupyter notebook files | `false` |
| `-S, --skip-string-normalization` | Don't normalize string quotes or prefixes | `false` |
| `-C, --skip-magic-trailing-comma` | Don't use trailing commas as a reason to split lines | `false` |
| `--preview` | Enable potentially disruptive style changes that may be added to Black's default style in the next major release | `false` |
| `--unstable` | Enable even more experimental features (use with caution) | `false` |
| `--check` | Don't write the files back, just return the status. Return code 0 means nothing changed, 1 means some files were changed | `false` |
| `--diff` | Don't write the files back, just output a diff for each file | `false` |
| `--color` | Show colored diff output | `false` |
| `--fast` / `--safe` | If `--fast`, skip AST safety checks after formatting | `--safe` |
| `--required-version` | Require a specific version of Black to be running | (none) |
| `--include` | A regular expression for files to include | `\.pyi?$` |
| `--exclude` | A regular expression for files to exclude | `/(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|\.svn|_build|buck-out|build|dist)/` |
| `--extend-exclude` | Like `--exclude`, but adds to the default regex | (none) |
| `--force-exclude` | Like `--exclude`, but files matching this regex are excluded even when passed explicitly | (none) |
| `--stdin-filename` | The name of the file when passing it through stdin. Useful for shebang lines | (none) |
| `-W, --workers` | Number of parallel workers | (auto-detected) |
| `-q, --quiet` | Don't emit non-error messages | `false` |
| `-v, --verbose` | Also emit messages about files that were not changed | `false` |
| `--version` | Show the version and exit | |
| `-h, --help` | Show help message and exit | |

**Line Ranges:**

| Flag | Description | Default |
|------|-------------|---------|
| `--line-ranges` | When specified, Black will try to only format lines in these ranges. Use as `--line-ranges START-END` (can be repeated) | (none) |

**Examples:**

```bash
# Format a single file
black my_script.py

# Format multiple files
black src/ tests/

# Check if files would be reformatted (exit code 1 if changes needed)
black --check .

# Show a diff of what would change
black --diff my_script.py

# Format with a custom line length
black --line-length 100 my_script.py

# Format for Python 3.10 and above
black --target-version py310 my_script.py

# Enable preview mode for upcoming style changes
black --preview my_script.py

# Format only specific line ranges
black --line-ranges 10-20 --line-ranges 30-40 my_script.py

# Format from stdin
echo "x = 1+2" | black -
```

### Configuration via `pyproject.toml`

Black reads configuration from a `[tool.black]` section in `pyproject.toml`. This is the recommended way to configure Black for your project.

```toml
[tool.black]
line-length = 88
target-version = ['py39', 'py310']
include = '\.pyi?$'
extend-exclude = '''
/(
    \.direnv
  | \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.nox
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

You can also specify a `required-version` to ensure a specific version of Black is used:

```toml
[tool.black]
required-version = "24.0"
```

### GitHub Action

Black provides a GitHub Action for CI/CD pipelines. The action installs Black and runs it on specified source files.

```yaml
- uses: psf/black@stable
  with:
    options: "--check --diff"
    src: "./src"
    version: "24.0"
```

The action supports the following inputs:

| Input | Description | Default |
|-------|-------------|---------|
| `options` | Command-line options for Black | `""` |
| `src` | Source files or directories to format | `""` |
| `version` | Version of Black to install | (auto-detected) |
| `use_pyproject` | Read version from `pyproject.toml` | `false` |
| `jupyter` | Also install Jupyter notebook support | `false` |
| `black_args` | (Deprecated) Alternative to `src` + `options` | `""` |
| `output_file` | Write Black's output to a file | `""` |

### Pre-commit Hook

Black can be used as a pre-commit hook. Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.0.0
    hooks:
      - id: black
        language_version: python3.11
```

## Usage

### Basic Usage

The simplest way to use Black is to point it at a file or directory:

```bash
black my_project/
```

Black will recursively find all Python files in `my_project/` and format them in place. If a file is already correctly formatted, Black will skip it.

### Checking Without Changing

To see which files would be changed without actually modifying them, use `--check`:

```bash
black --check .
```

This is useful in CI pipelines. The exit code will be:
- `0`: All files are already formatted correctly
- `1`: Some files would be reformatted
- `123`: An internal error occurred

### Viewing Diffs

To see exactly what Black would change, use `--diff`:

```bash
black --diff my_script.py
```

This outputs a unified diff showing the changes. Combine with `--color` for colored output:

```bash
black --diff --color my_script.py
```

### Formatting Specific Line Ranges

Black supports formatting only specific line ranges, which is useful for incremental adoption or focusing on recently changed code:

```bash
black --line-ranges 10-20 --line-ranges 30-40 my_script.py
```

This will only format lines 10-20 and 30-40 in `my_script.py`. Note that when using line ranges, the stable check (verifying that formatting is idempotent) is skipped for edge cases where the diff algorithm may produce incorrect new line ranges.

### Using Preview Mode

Preview mode enables style changes that are being considered for the next major release. These changes are stable and tested, but may not yet be part of the default style:

```bash
black --preview my_script.py
```

You can also enable specific preview features in your `pyproject.toml`:

```toml
[tool.black]
preview = true
```

### Formatting Jupyter Notebooks

Black can format code cells in Jupyter notebooks (`.ipynb` files). It handles IPython magic commands by masking them before formatting and restoring them afterward:

```bash
black --ipynb my_notebook.ipynb
```

### Using the Cache

Black caches formatted files to avoid reformatting unchanged files on subsequent runs. The cache is stored in a platform-appropriate cache directory and is invalidated when the Black version or mode changes. To bypass the cache, use `--no-cache` (if available) or run with `--check` which doesn't write to the cache.

### Parallel Formatting

Black can format multiple files in parallel using the `--workers` option:

```bash
black --workers 4 src/ tests/
```

By default, Black auto-detects the number of available CPU cores.

### Integration with Editors

Black can be integrated with most editors and IDEs. For example, to use Black with Visual Studio Code, add this to your `settings.json`:

```json
{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

For other editors, see the [Black documentation](https://black.readthedocs.io/en/stable/) for integration guides.

### Using the `blackd` HTTP Server

Black also ships with `blackd`, a daemon that provides formatting via HTTP. This is useful for editor integrations and CI pipelines that want to avoid the startup cost of running Black as a subprocess.

Start the daemon:

```bash
blackd
```

By default, it listens on `http://localhost:45484`. Send a POST request with the code to format:

```bash
curl -X POST -H "Content-Type: text/x-python" --data "x = 1+2" http://localhost:45484
```

The response will contain the formatted code. If no changes are needed, the server returns a `204 No Content` status.

For more details on `blackd`, see the [API documentation](API.md).

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All files formatted successfully (or no changes needed) |
| `1` | Some files would be reformatted (when using `--check`) |
| `123` | An internal error occurred (e.g., a file could not be parsed) |

## Additional Documentation

- [System Architecture](ARCHITECTURE.md) — Understand how Black's components work together
- [Contribution Guidelines](CONTRIBUTING.md) — Learn how to contribute to Black
- [Development Setup](DEVELOPMENT.md) — Set up your development environment
- [Testing Guide](TESTING.md) — Run and write tests for Black
- [API Documentation](API.md) — Use the `blackd` HTTP API

## License

MIT