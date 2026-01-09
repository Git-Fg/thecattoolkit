# @cattoolkit/guard

Consolidated safety plugin (formerly guard-python, guard-ts).

## Hooks

- **protect-files.py** - Warns about editing sensitive files (lock files, .env, secrets, git internals)
- **security-check.py** - Detects potential secrets in code (API keys, tokens, passwords)
- **type-check-python.py** - Runs pyrefly/mypy on Python files
- **type-check-ts.js** - Runs tsc on TypeScript files

## Design Philosophy

All hooks run non-blocking (warn-only mode). Type checkers auto-detect project configuration and skip if not applicable.
