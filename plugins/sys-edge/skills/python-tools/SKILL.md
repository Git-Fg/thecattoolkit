---
name: python-tools
description: "Covers uv (10-100x faster package manager) and ruff (extremely fast linter/formatter). Use when managing Python projects, dependencies, virtual environments, linting, or formatting."
user-invocable: false
allowed-tools: [Bash, Read, Write, Edit]
---

# UV & Ruff: Modern Python Development

Astral's blazing-fast Python tooling: **uv** for package management, **ruff** for code quality.

## Quick Decision Tree

```
Need to install/manage Python packages?
  → uv add <package>          # Add dependency
  → uv sync                   # Install from lockfile
  → uv run <command>          # Run in project env

Need to lint or format Python code?
  → ruff check .              # Lint
  → ruff check --fix .        # Lint + auto-fix
  → ruff format .             # Format

Need to manage Python versions?
  → uv python install 3.12    # Install Python
  → uv python pin 3.12        # Pin for project

Need to run a CLI tool once?
  → uvx <tool>                # e.g., uvx black .
```

## Installation

```bash
# UV (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# UV (Windows PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Ruff (via uv - recommended)
uv tool install ruff

# Verify
uv version && ruff version
```

## Essential Commands

### UV Project Management

```bash
# Initialize project
uv init my-project && cd my-project

# Dependencies
uv add requests pandas           # Production deps
uv add --dev pytest ruff         # Dev deps
uv remove requests               # Remove dep
uv lock --upgrade                # Update lockfile

# Run commands (no activation needed)
uv run python main.py
uv run pytest
uv run ruff check .

# Python versions
uv python install 3.11 3.12
uv python pin 3.12
uv run --python 3.11 python script.py
```

### Ruff Linting & Formatting

```bash
# Lint
ruff check .                     # Check errors
ruff check --fix .               # Auto-fix
ruff check --diff .              # Preview fixes
ruff check --watch               # Continuous mode

# Format
ruff format .                    # Format files
ruff format --check .            # Check only
ruff format --diff .             # Preview changes

# Combined workflow
ruff check --fix . && ruff format .
```

## Configuration

### pyproject.toml (Minimal)

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP"]
ignore = ["E501"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["S101"]
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Rule Sets Quick Reference

| Code | Name | Purpose |
|:-----|:-----|:--------|
| E/W | pycodestyle | PEP 8 style |
| F | Pyflakes | Logic errors |
| I | isort | Import sorting |
| B | flake8-bugbear | Common bugs |
| UP | pyupgrade | Modern syntax |
| S | flake8-bandit | Security |
| T20 | flake8-print | Print statements |

**Recommended starter set:** `select = ["E", "W", "F", "I", "B", "UP"]`

## Suppress Errors

```python
import os  # noqa: F401           # Ignore specific rule
import sys  # noqa                # Ignore all rules
# ruff: noqa: E501               # File-level ignore
```

## CI/CD Snippet (GitHub Actions)

```yaml
- name: Install uv
  run: curl -LsSf https://astral.sh/uv/install.sh | sh

- name: Install and lint
  run: |
    uv sync --frozen
    uv run ruff check .
    uv run ruff format --check .
    uv run pytest
```

## Troubleshooting

```bash
# Clear caches
uv cache clean
ruff clean

# Debug configuration
ruff check --show-settings .

# Reinstall Python
rm -r "$(uv python dir)" && uv python install 3.12

# Reset lockfile
rm uv.lock && uv lock
```

## Detailed References

Load these for comprehensive guidance:

| Reference | Content |
|:----------|:--------|
| `references/uv-guide.md` | Complete uv documentation: projects, Python versions, building, publishing |
| `references/ruff-guide.md` | All 800+ rules, formatting options, editor integration |
| `references/migration.md` | Migrating from pip, conda, poetry, Flake8, Black, isort |
| `references/workflows.md` | Monorepos, Docker, CI/CD, production deployments |

## Resources

- [uv docs](https://docs.astral.sh/uv/) | [ruff docs](https://docs.astral.sh/ruff/)
- [astral-sh/uv](https://github.com/astral-sh/uv) | [astral-sh/ruff](https://github.com/astral-sh/ruff)
