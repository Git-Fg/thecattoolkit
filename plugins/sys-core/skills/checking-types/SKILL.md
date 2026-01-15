---
name: checking-types
description: "Runs configured type checkers (pyrefly, mypy) on files after editing. MUST USE when validating Python type safety (Internal-only passive hook)."
user-invocable: false
allowed-tools: [Read, Bash(pyrefly), Bash(mypy), Bash(python3:-m pyrefly), Bash(python3:-m mypy)]
---

# Type Checking Standards

## Active Hooks


### Automatic Type Check
**Trigger:** `PostToolUse` (Edit/Write on .py files)
**Action:** Runs type checker on the modified file.
**Priority:**
1. `tool.pyrefly` in pyproject.toml -> `uv run pyrefly`
2. `tool.mypy` in pyproject.toml -> `uv run mypy`



## Configuration

To enable type checking for a project, assume the presence of `pyproject.toml` with `[tool.pyrefly]` or `[tool.mypy]`.

**Scripts:**
- `plugins/verify/hooks/scripts/type-check-python.py`
