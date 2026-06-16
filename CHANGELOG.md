# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add `is_ok()` and `is_err()` predicate methods to `Ok` and `Err` result types for checking operation success or failure (black/numerics.py:format_octal, black/cache.py:Cache.clear())

### Changed

- Update the Ok.__init__ and Ok.ok methods, and Err.__init__ and Err.err methods in rusty.py to refine the Result type implementation for more consistent error handling. (black/__init__.py:WriteBack class, black/__init__.py:WriteBack.from_configuration method)

### Removed

- Remove the parse_req_python_version and parse_req_python_specifier helper functions from files.py and the FileMode alias from __init__. (black/files.py:parse_req_python_version, black/files.py:parse_req_python_specifier)
