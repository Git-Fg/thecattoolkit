#!/usr/bin/env python3
"""
Hook Runner Script for thecattoolkit Guard Plugin

This script provides a unified interface for running hooks across different environments.
It handles environment detection (uv, poetry, python3) and executes the appropriate hook.

Usage:
    python3 hook_runner.py <hook_name>
    python3 hook_runner.py protect-files
    python3 hook_runner.py security-check
    python3 hook_runner.py type-check-on-edit
"""

import sys
import os
import subprocess
from pathlib import Path


def detect_python_interpreter() -> tuple[str, str] | tuple[None, None]:
    """
    Detect the best available Python interpreter.

    Returns:
        tuple: (interpreter_command, interpreter_type)
            - interpreter_command: str, the command to run
            - interpreter_type: str, type of interpreter (uv, poetry, python3)
    """
    # Check for uv (preferred for Python projects)
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return ("uv run", "uv")
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # Check for poetry
    try:
        result = subprocess.run(
            ["poetry", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return ("poetry run", "poetry")
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # Fall back to python3
    try:
        result = subprocess.run(
            ["python3", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return ("python3", "python3")
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return (None, None)


def run_hook(hook_name):
    """
    Run a specific hook script.

    Args:
        hook_name: str, name of the hook to run (e.g., 'protect-files', 'security-check')

    Returns:
        int: exit code (0 for success, non-zero for failure)
    """
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    hooks_dir = script_dir.parent  # Go up one level to hooks/

    # Construct the path to the hook script
    hook_script = script_dir / f"{hook_name}.py"

    # Check if the hook script exists
    if not hook_script.exists():
        print(f"Hook script not found: {hook_script}", file=sys.stderr)
        return 1

    # Check if hooks are deployed to .cattoolkit/hooks
    cattoolkit_hooks = Path(".cattoolkit/hooks")
    if not cattoolkit_hooks.exists():
        print("Hooks not deployed to .cattoolkit/hooks", file=sys.stderr)
        return 0

    # Detect the best Python interpreter
    interpreter_cmd, interpreter_type = detect_python_interpreter()

    if interpreter_cmd is None:
        print("No Python interpreter found (tried: uv, poetry, python3)", file=sys.stderr)
        return 1

    # Run the hook script
    try:
        # Use list-based subprocess call to avoid command injection
        cmd: list[str] = [interpreter_cmd, str(hook_script)]
        result = subprocess.run(
            cmd,
            shell=False,
            capture_output=False,  # Let the hook script output directly
            timeout=15,  # 5 minute timeout
        )
        return result.returncode

    except subprocess.TimeoutExpired:
        print(f"Hook '{hook_name}' timed out after 300 seconds", file=sys.stderr)
        return 1
    except subprocess.SubprocessError as e:
        print(f"Error running hook '{hook_name}': {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point for the hook runner."""
    if len(sys.argv) < 2:
        print("Usage: python3 hook_runner.py <hook_name>", file=sys.stderr)
        print("Available hooks: protect-files, security-check, type-check-on-edit", file=sys.stderr)
        return 1

    hook_name = sys.argv[1]
    exit_code = run_hook(hook_name)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
