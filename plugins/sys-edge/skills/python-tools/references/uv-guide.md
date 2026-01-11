# UV Complete Guide

UV is an extremely fast Python package and project manager written in Rust. 10-100x faster than pip.

## Project Management

### Create and Initialize

```bash
uv init my-project           # New project
uv init .                    # Existing directory
```

**Generated structure:**
```
my-project/
├── .gitignore
├── .python-version
├── README.md
├── hello.py
└── pyproject.toml
```

### Run Commands

```bash
uv run python hello.py       # Run script
uv run pytest                # Run tool
uv run --python 3.12 python script.py  # Specific Python
```

## Dependency Management

### Adding Dependencies

```bash
uv add requests              # Production
uv add requests pandas numpy # Multiple
uv add "requests>=2.31.0"    # Version constraint
uv add --dev pytest ruff     # Development
uv add --group docs sphinx   # Named group
uv add git+https://github.com/user/repo.git  # From git
```

### Managing Dependencies

```bash
uv remove requests           # Remove
uv lock --upgrade            # Upgrade all
uv lock --upgrade-package requests  # Upgrade one
uv sync                      # Install from lockfile
uv sync --frozen             # Exact lockfile (CI)
```

### Dependency Groups

```toml
[project.optional-dependencies]
dev = ["pytest>=7.0.0", "ruff>=0.1.0"]
docs = ["sphinx>=5.0.0"]

[tool.uv]
dev-dependencies = ["black>=23.0.0"]
```

```bash
uv sync --group docs         # Include group
uv sync --only-group dev     # Only specific group
uv sync --no-group docs      # Exclude group
```

### Export

```bash
uv export -o requirements.txt
uv export --group dev -o requirements-dev.txt
```

## Python Version Management

```bash
uv python install 3.11 3.12 3.13  # Install versions
uv python list                     # List installed
uv python list --all-versions      # List available
uv python pin 3.12                 # Pin for project
```

## Tool Management

```bash
# Ephemeral execution (like npx)
uvx ruff check .
uvx black .

# Global install
uv tool install ruff
uv tool upgrade ruff
uv tool list
uv tool uninstall ruff
```

## The pip Interface

Drop-in replacement for pip commands:

```bash
uv pip install requests
uv pip install -r requirements.txt
uv pip install -e .
uv pip uninstall requests
uv pip freeze > requirements.txt
uv pip compile requirements.in -o requirements.txt
uv pip sync requirements.txt
```

### Virtual Environment

```bash
uv venv                      # Create .venv
uv venv --python 3.12        # Specific Python
uv venv .venv-custom         # Custom name
source .venv/bin/activate    # Activate (optional with uv run)
```

## Scripts with Inline Dependencies

```python
# script.py
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "pandas"]
# ///

import requests
import pandas as pd
# ...
```

```bash
uv add --script script.py requests pandas  # Add deps to script
uv run script.py                           # Auto-installs deps
```

## Building and Publishing

```bash
uv build                     # Build wheel + sdist
uv build --wheel             # Wheel only
uv publish                   # Publish to PyPI
uv publish --publish-url https://test.pypi.org/legacy/  # TestPyPI
```

## Configuration

### pyproject.toml

```toml
[tool.uv]
python = ">=3.11"
index-url = "https://pypi.org/simple"
extra-index-url = ["https://example.com/simple"]
resolution = "highest"  # or "lowest", "lowest-direct"

[tool.uv.sources]
my-package = { git = "https://github.com/user/repo.git" }
local-package = { path = "../local-package" }
```

### Environment Variables

```bash
UV_PYTHON_INSTALL_DIR="$HOME/.python"
UV_CACHE_DIR="$HOME/.cache/uv"
UV_NO_CACHE=1
UV_INDEX_URL="https://pypi.org/simple"
UV_OFFLINE=1
```

## Caching

```bash
uv cache dir                 # Show location
uv cache clean               # Clear all
uv cache clean requests      # Clear specific
uv cache prune               # Remove old entries
```

**Locations:**
- macOS/Linux: `~/.cache/uv`
- Windows: `%LOCALAPPDATA%\uv\cache`

## Workspaces (Monorepo)

**Root pyproject.toml:**
```toml
[tool.uv.workspace]
members = ["packages/*", "apps/*"]
```

**Package referencing workspace:**
```toml
[project]
dependencies = ["myproject-core"]

[tool.uv.sources]
myproject-core = { workspace = true }
```

```bash
uv sync                              # All packages
uv run --package myproject-api pytest  # Specific package
```

## Comparison

| Feature | uv | pip | poetry | conda |
|---------|-----|-----|--------|-------|
| Speed | 10-100x | 1x | 2-5x | 0.5x |
| Lockfiles |  |  |  |  |
| Python Management |  |  |  |  |
| Tool Running |  |  |  |  |
| Memory | Low | Med | Med | High |
