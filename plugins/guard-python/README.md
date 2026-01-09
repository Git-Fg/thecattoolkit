# @cattoolkit/guard-python

**The Immune System: File safety warnings, security checks, and type-checking hooks for Vibecoding safety.**

**License:** MIT

## Purpose

Provides passive safety and quality hooks that run automatically to protect against common mistakes and security issues. These hooks represent the **Immune System** of the toolkit—always running, never blocking, keeping your development environment safe.

## Target Users

- **All Users** - Anyone who wants automatic safety checks during development
- **Security-Conscious Developers** - Teams that want to prevent accidental secret commits
- **Type-Safe Projects** - Python projects using pyrefly or mypy

## How It Works

The guard plugin uses **hooks**—scripts that run automatically before and after tool operations:

### Pre-Tool Hooks (Before Edit/Write)
1. **protect-files.py** - Warns about editing sensitive files
2. **security-check.py** - Warns about potential secrets in content

### Post-Tool Hooks (After Edit/Write)
1. **type-check-on-edit.py** - Runs type checking on Python files

## Features

### File Protection (`protect-files.py`)

Warns before editing protected file types:

**Protected Patterns (warns):**
- Lock files: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`
- Secrets: `.env`, `.env.*`, `secrets/*`, `credentials/*`
- Git internals: `.git/*`

**Warning Patterns (note):**
- CI/CD: `.github/workflows/*`
- Production: `docker-compose.yml`, `Dockerfile`, `production/*`

**Behavior:** All edits are **allowed** with helpful warnings shown to Claude.

### Security Check (`security-check.py`)

Detects potential secrets in file content:

**Secret Patterns:**
- API keys: `api_key`, `apikey`
- Passwords: `password`, `secret`, `pwd`
- Tokens: `Bearer` tokens, GitHub PATs, OpenAI/Anthropic keys
- Keys: AWS keys, private keys

**Behavior:** Shows warnings if patterns are detected. Skips test files and lock files.

### Type Check (`type-check-on-edit.py`)

Runs type checking on Python files after edits:

**Supported Type Checkers:**
- **pyrefly** (preferred) - Modern, fast Python type checker
- **mypy** - Traditional Python type checker

**Configuration Detection:**
- Checks `pyproject.toml` for `[tool.pyrefly]` or `[tool.mypy]`
- Skips silently if no type checker is configured
- Prioritizes `uv run` commands, falls back to global executables

**Excluded Paths:**
- `.venv`, `venv`, `__pycache__`, `.attic`, `node_modules`, `.git`, `build`, `dist`

## Installation

The guard plugin is lightweight and can be installed alongside any other plugin:

```bash
# Add to your marketplace.json or install directly
claude plugin install @cat-toolkit/guard
```

### Setup Protocol (Recommended)

Hooks are deployed to `.cattoolkit/hooks/` for project-specific customization:

```bash
# Deploy hooks using the setup-py command (recommended)
cd your-project
/setup-py
```

**Benefits of .cattoolkit/hooks/ deployment:**
- Project-specific hook customization
- Version-controlled hook configurations
- Portable hook setup
- Centralized runtime environment
- **No environment variables required** - Uses absolute paths

**Configuration:**
Hooks automatically check for `.cattoolkit/hooks/scripts/` before running. If hooks are not deployed, they skip silently.

## Usage

### Automatic Operation
Hooks run automatically—no commands needed. Just edit files as usual:

```bash
# Edit a file - hooks run automatically
claude-code "Update the auth module"

# protect-files.py: Warns if editing .env
# security-check.py: Warns if content looks like a secret
# type-check-on-edit.py: Runs mypy/pyrefly on .py files
```

### Configuration

**Type Checking:**
Add to your `pyproject.toml`:

```toml
[tool.pyrefly]
# For pyrefly (preferred)

[tool.mypy]
# For mypy
python_version = "3.11"
warn_return_any = true
```

**Secret Patterns:**
Edit `.cattoolkit/hooks/scripts/security-check.py` to customize `SECRET_PATTERNS` or `SKIP_FILES`.

**Protected Files:**
Edit `.cattoolkit/hooks/scripts/protect-files.py` to customize `PROTECTED_PATTERNS` or `WARN_PATTERNS`.

## Integration

The guard plugin integrates seamlessly with all other Cat Toolkit plugins:

- **With @cat-toolkit/engineer** - Automatic type checking during development
- **With @cat-toolkit/planner** - File protection during project setup
- **With @cat-toolkit/context** - Security awareness during context management

## Best Practices

1. **Keep It Installed** - Guard is lightweight and benefits every session
2. **Configure Type Checking** - Add `[tool.pyrefly]` or `[tool.mypy]` to your `pyproject.toml`
3. **Review Warnings** - Hooks show warnings for a reason—review before committing
4. **Customize Patterns** - Adjust secret patterns for your specific needs

## Troubleshooting

### Type Check Not Running
1. Check `pyproject.toml` has `[tool.pyrefly]` or `[tool.mypy]`
2. Verify type checker is installed: `uv run pyrefly --version` or `mypy --version`
3. Ensure file is not in excluded paths (`.venv`, `__pycache__`, etc.)

### False Positive Warnings
1. Edit patterns in `security-check.py` or `protect-files.py`
2. Add files to `SKIP_FILES` set in `security-check.py`
3. Test changes: `claude-code "Edit test file"`

### Hook Timeout
- Hooks have aggressive timeouts (e.g. 2s for type checking) to prevent blocking workflow
- If type checking is slow/timing out, consider:
  - Running type checker on save instead of every edit
  - Excluding large files from type checking
  - Using faster type checker (pyrefly vs mypy)

## Architecture

**Why Separate from Meta?**
- Hooks are **passive** (they observe and warn)
- Meta tools are **active** (they create and build)
- Users benefit from guard hooks without needing meta's complex toolkit builder features

**The Immune System Analogy:**
- Hooks = White blood cells (always present, detecting threats)
- Meta tools = Bone marrow (creates new cells/tools)
- Both important, but serve different purposes

## License

MIT License - see plugin directory for full license text.
