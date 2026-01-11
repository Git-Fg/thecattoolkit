---
name: check-types
description: "MUST USE when validating Python type safety. Runs configured type checkers (pyrefly, mypy) on files after editing (Internal-only passive hook)."
allowed-tools: [Read, Bash(pyrefly), Bash(mypy), Bash(python3:-m pyrefly), Bash(python3:-m mypy)]
---

# Type Checking Standards

## Capabilities

This skill provides automatic type checking via hooks:

### Automatic Type Check
**Trigger:** `PostToolUse` (Edit/Write on .py files)
**Action:** Runs type checker on the modified file.
**Priority:**
1. `tool.pyrefly` in pyproject.toml -> `uv run pyrefly`
2. `tool.mypy` in pyproject.toml -> `uv run mypy`

## Usage

This skill functions **passively** via the runtime hook system. It communicates results back to the agent via hook output.

## Configuration

To enable type checking for a project, assume the presence of `pyproject.toml` with `[tool.pyrefly]` or `[tool.mypy]`.

**Scripts:**
- `plugins/verify/hooks/scripts/type-check-python.py`
