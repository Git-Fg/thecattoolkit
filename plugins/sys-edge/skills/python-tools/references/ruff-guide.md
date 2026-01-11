# Ruff Complete Guide

Ruff is an extremely fast Python linter and formatter written in Rust. 10-100x faster than Flake8/Black.

## Linting

### Basic Commands

```bash
ruff check .                 # Check directory
ruff check src/main.py       # Check files
ruff check --fix .           # Auto-fix
ruff check --diff .          # Preview fixes
ruff check --watch           # Continuous mode
```

### Output Formats

```bash
ruff check --output-format json .     # JSON
ruff check --output-format github .   # GitHub Actions
ruff check --output-format gitlab .   # GitLab
ruff check --output-format junit .    # JUnit XML
```

### Advanced Options

```bash
ruff check --unsafe-fixes .           # Include unsafe fixes
ruff check --fix-only .               # Fix without reporting
ruff check --statistics .             # Show rule stats
ruff check --show-settings .          # Debug config
ruff check --show-files .             # Show files to check
```

## Formatting

```bash
ruff format .                # Format all
ruff format src/main.py      # Format specific
ruff format --check .        # Check only
ruff format --diff .         # Preview changes
ruff format --preview .      # Enable preview features
```

### Combined Workflow

```bash
ruff check --fix . && ruff format .
```

## Configuration

### pyproject.toml

```toml
[tool.ruff]
line-length = 88
indent-width = 4
target-version = "py311"

exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "UP",  # pyupgrade
]

ignore = ["E501"]  # Line too long (formatter handles)

fixable = ["ALL"]
unfixable = []

dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["S101"]
"scripts/*" = ["T201"]

[tool.ruff.lint.isort]
known-first-party = ["myproject"]
combine-as-imports = true

[tool.ruff.lint.pydocstyle]
convention = "google"  # or "numpy", "pep257"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
docstring-code-format = true
```

## Rule Sets

| Code | Name | Purpose |
|:-----|:-----|:--------|
| E | pycodestyle errors | PEP 8 errors |
| W | pycodestyle warnings | PEP 8 warnings |
| F | Pyflakes | Logic errors |
| I | isort | Import sorting |
| N | pep8-naming | Naming conventions |
| D | pydocstyle | Docstring style |
| UP | pyupgrade | Modern Python |
| B | flake8-bugbear | Common bugs |
| A | flake8-builtins | Builtin shadowing |
| C4 | flake8-comprehensions | Comprehensions |
| T20 | flake8-print | Print statements |
| PT | flake8-pytest-style | Pytest style |
| S | flake8-bandit | Security |
| Q | flake8-quotes | Quote style |
| RUF | Ruff-specific | Custom rules |

### Selecting Rules

```bash
ruff check --select E,W,F .          # Specific sets
ruff check --select ALL .            # All rules
ruff check --extend-select B,I .     # Add to defaults
ruff check --ignore E501 .           # Ignore specific
```

### Recommended Combinations

**Minimal:**
```toml
select = ["E4", "E7", "E9", "F"]
```

**Standard:**
```toml
select = ["E", "W", "F", "I"]
```

**Strict:**
```toml
select = ["E", "W", "F", "I", "N", "D", "UP", "B", "C4", "S", "T20", "PT"]
```

## Error Suppression

### Inline Comments

```python
import os  # noqa: F401              # Specific rule
import sys, os  # noqa: F401, E401   # Multiple rules
x = 1  # noqa                        # All rules
```

### File-Level

```python
# ruff: noqa: F401, E402
import os
```

### Auto-Add noqa

```bash
ruff check --add-noqa .
```

## Rule Explainer

```bash
ruff rule E501                       # Explain rule
ruff rule --all                      # List all rules
```

## Common Rules Explained

### F (Pyflakes)
- **F401**: Imported but unused
- **F841**: Variable assigned but never used
- **F821**: Undefined name

### B (flake8-bugbear)
- **B006**: Mutable default argument
- **B008**: Function call in default argument
- **B011**: Don't use assert False

### UP (pyupgrade)
- **UP006**: Use `list` instead of `typing.List`
- **UP032**: Use f-string instead of `.format()`

## Editor Integration

### VS Code

```json
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

### Pre-commit

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Cache Management

```bash
ruff clean                           # Clear cache
ruff check --no-cache .              # Disable cache
```

## Migration from Other Tools

### From Flake8

```ini
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503
```

Becomes:

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
ignore = ["E203", "W503"]
```

### From Black

```bash
# Replace
black .
# With
ruff format .
```

### From isort

```bash
# Replace
isort .
# With
ruff check --select I --fix .
```

### Complete Migration

**Before (multiple tools):**
```bash
isort . && black . && flake8 .
```

**After (single tool):**
```bash
ruff check --fix . && ruff format .
```
