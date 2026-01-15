---
description: "Migrate legacy Python (pip/conda/poetry) to modern UV standards. Auto-detects project type and converts configuration to UV with Ruff linting."
argument-hint: "no args (detects automatically)"
allowed-tools: [Skill(managing-python), Bash]
disable-model-invocation: true
---

# Python Migration Assistant

Modernize your Python project with UV and Ruff for faster, cleaner development.

**This command automatically:**
1. Detects legacy configs (`requirements.txt`, `setup.py`, `environment.yml`, `pyproject.toml`)
2. Initializes UV project structure
3. Imports dependencies
4. Sets up Ruff for linting
5. Deletes legacy artifacts (with confirmation)

Invoke `Skill(managing-python)` to perform the migration workflow.
