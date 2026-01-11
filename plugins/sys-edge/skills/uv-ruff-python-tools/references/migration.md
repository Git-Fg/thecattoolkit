# Migration Guide: UV and Ruff

## From pip + virtualenv → UV

### Before

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### After

```bash
uv init .
uv add $(cat requirements.txt | grep -v '^#' | tr '\n' ' ')
uv run python main.py
```

### Convert requirements.txt → pyproject.toml

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
    "pandas>=2.0.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]
```

### Maintain requirements.txt (Optional)

```bash
uv export -o requirements.txt
uv export --group dev -o requirements-dev.txt
```

## From conda → UV

### Key Differences

| Feature | conda | UV |
|---------|-------|-----|
| Speed | Slow | Fast |
| Non-Python packages | ✅ | ❌ |
| PyPI packages | Limited | Full |
| Memory | High | Low |

### Migration Steps

1. **Export conda packages:**
```bash
conda env export --from-history > environment.yml
```

2. **Convert to pyproject.toml:**
```yaml
# environment.yml
dependencies:
  - python=3.11
  - numpy=1.24.0
  - pip:
    - requests==2.31.0
```

Becomes:

```toml
[project]
requires-python = ">=3.11"
dependencies = [
    "numpy>=1.24.0",
    "requests>=2.31.0",
]
```

3. **Remove conda environment:**
```bash
conda deactivate
conda env remove -n myenv
```

### When to Keep Conda

Keep conda if you need:
- Non-Python packages (R, Julia, C libraries)
- Specific binary distributions
- Legacy scientific computing workflows

## From poetry → UV

### Convert pyproject.toml

**Poetry:**
```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.31.0"

[tool.poetry.dev-dependencies]
pytest = "^7.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**UV:**
```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["requests>=2.31.0"]

[tool.uv]
dev-dependencies = ["pytest>=7.0.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Version Constraints

| Poetry | UV/pip |
|--------|--------|
| `^2.31.0` | `>=2.31.0,<3.0.0` |
| `~2.31.0` | `>=2.31.0,<2.32.0` |
| `*` | (no constraint) |

### Migration Steps

```bash
rm poetry.lock
rm -rf .venv
poetry env remove --all
uv lock && uv sync
```

## From pipx → UV Tool

### Migration

```bash
# List pipx tools
pipx list

# Install with UV
uv tool install ruff
uv tool install black

# Remove pipx tools
pipx uninstall-all
```

### Ephemeral Execution

```bash
# pipx run equivalent
uvx ruff check .
uvx black .
```

## From Flake8/Black/isort → Ruff

### Configuration Migration

**From .flake8:**
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__
per-file-ignores =
    __init__.py:F401
```

**From pyproject.toml (Black + isort):**
```toml
[tool.black]
line-length = 88

[tool.isort]
profile = "black"
known_first_party = ["myproject"]
```

**To unified Ruff:**
```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
ignore = ["E203", "W503"]
exclude = [".git", "__pycache__"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]

[tool.ruff.lint.isort]
known-first-party = ["myproject"]
```

### Command Migration

| Before | After |
|--------|-------|
| `isort .` | `ruff check --select I --fix .` |
| `black .` | `ruff format .` |
| `flake8 .` | `ruff check .` |
| All three | `ruff check --fix . && ruff format .` |

### Remove Old Tools

```bash
uv remove --dev black isort flake8
uv add --dev ruff
```

### Update pre-commit

**Before:**
```yaml
repos:
  - repo: https://github.com/PyCQA/isort
    hooks: [id: isort]
  - repo: https://github.com/psf/black
    hooks: [id: black]
  - repo: https://github.com/PyCQA/flake8
    hooks: [id: flake8]
```

**After:**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Complete Migration Checklist

- [ ] Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Convert requirements.txt → pyproject.toml
- [ ] Generate lockfile: `uv lock`
- [ ] Install dependencies: `uv sync`
- [ ] Add Ruff: `uv add --dev ruff`
- [ ] Convert linter/formatter config to `[tool.ruff]`
- [ ] Test: `ruff check . && ruff format .`
- [ ] Update CI/CD pipelines
- [ ] Update pre-commit hooks
- [ ] Remove old tools
- [ ] Update team documentation

## Typical Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Install time | 5 min | 30 sec | 10x faster |
| Lint time | 15 sec | 0.5 sec | 30x faster |
| CI/CD time | 10 min | 2 min | 5x faster |
| Tools to manage | 7 | 2 | 3.5x fewer |
| Config files | 4 | 1 | 4x simpler |
