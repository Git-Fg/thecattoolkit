# @cattoolkit/verify

**Validation Phase** - Verifying correctness of file changes and code safety.

## Purpose

The immune system of the toolkit. Shifts focus from "blocking" to "verifying correctness" - all hooks run in warn-only mode.

## Hooks

- **protect-files.py** - Warns about editing sensitive files (lock files, .env, secrets, git internals)
- **security-check.py** - Detects potential secrets in code (API keys, tokens, passwords)
- **type-check-python.py** - Runs pyrefly/mypy on Python files after edits
- **type-check-ts.js** - Runs tsc on TypeScript files after edits

## Design Philosophy

All hooks run non-blocking (warn-only). Type checkers auto-detect project configuration and skip if not applicable.
