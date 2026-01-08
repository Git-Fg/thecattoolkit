#!/usr/bin/env python3
"""
Run type checker on Python files after Claude edits them.
Only runs when pyproject.toml is configured with type checking support.

Type checker priority order:
- uv run pyrefly -> pyrefly (global) -> uv run mypy -> mypy (global)

Configuration detection:
- Checks for [tool.pyrefly] in pyproject.toml (uses pyrefly)
- Checks for [tool.mypy] in pyproject.toml (uses mypy)
- Skips silently if no type checker is configured

Results are reported to stderr for AI visibility.

SAFETY: If this is the 3rd consecutive attempt to fix the same type error, stop and ask the user for guidance.
"""
import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Literal, Optional, Tuple

logger = logging.getLogger(__name__)

TypeChecker = Literal["pyrefly", "mypy"]


def check_command_available(cmd: str) -> bool:
    """Check if a command is available on the system."""
    return shutil.which(cmd) is not None


def try_command(cmd: list[str], timeout: int = 5) -> bool:
    """Try running a command to check availability. Returns True if successful."""
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=timeout)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def is_safe_path(file_path: str) -> bool:
    """
    Verify file_path resolves to a location within the current working directory.
    Uses os.path.commonpath to prevent path traversal attacks.
    """
    try:
        project_root = os.getcwd()
        target_path = os.path.abspath(os.path.join(project_root, file_path))
        return os.path.commonpath([project_root, target_path]) == project_root
    except Exception:
        return False


def find_pyproject_toml(file_path: str) -> Optional[Path]:
    """Find pyproject.toml by searching upward from file_path."""
    path = Path(file_path).resolve()
    seen = set()

    while path != path.parent and str(path) not in seen:
        seen.add(str(path))
        pyproject = path / "pyproject.toml"
        if pyproject.exists():
            return pyproject
        path = path.parent

    return None


def detect_configured_type_checker(pyproject_path: Path) -> Optional[TypeChecker]:
    """Detect which type checker is configured in pyproject.toml."""
    try:
        content = pyproject_path.read_text()
        if "[tool.pyrefly]" in content:
            return "pyrefly"
        if "[tool.mypy]" in content:
            return "mypy"
    except Exception:
        pass
    return None


def get_type_checker_command(checker: TypeChecker, project_root: Path) -> tuple[list[str], str] | None:
    """
    Return the type checker command for the given checker type.
    Returns (command, description) tuple or None if unavailable.
    """
    if checker == "pyrefly":
        # Try uv run pyrefly first
        if check_command_available("uv"):
            if try_command(["uv", "run", "pyrefly", "--version"], timeout=3):
                return (["uv", "run", "pyrefly", "check"], "uv run pyrefly")
        # Fallback to global pyrefly
        if check_command_available("pyrefly"):
            return (["pyrefly", "check"], "pyrefly")
        return None

    if checker == "mypy":
        # Try uv run mypy first
        if check_command_available("uv"):
            if try_command(["uv", "run", "mypy", "--version"], timeout=3):
                return (["uv", "run", "mypy"], "uv run mypy")
        # Fallback to global mypy
        if check_command_available("mypy"):
            return (["mypy"], "mypy")
        return None

    return None


def should_check_file(file_path: str, project_root: Path) -> bool:
    """Check if file should be type checked based on common exclusion patterns."""
    path = Path(file_path).resolve()

    # Skip if file is not under project root
    try:
        path.relative_to(project_root)
    except ValueError:
        return False

    # Common exclusion patterns
    exclude_parts = {".venv", "venv", "__pycache__", ".attic", "node_modules", ".git", "build", "dist"}
    if any(part in path.parts for part in exclude_parts):
        return False

    # Skip test files if desired (optional - uncomment to enable)

    return True


def main() -> None:
    try:
        input_data = json.load(sys.stdin)
        file_path = input_data.get("tool_input", {}).get("file_path", "")

        # Input validation
        if not file_path or not os.path.exists(file_path):
            sys.exit(0)

        # Security: Check for path traversal attempts
        if not is_safe_path(file_path):
            logger.debug("[type-check-on-edit] Path traversal detected: %s", file_path)
            sys.exit(0)

        # Only check Python files
        if not file_path.endswith(".py"):
            sys.exit(0)

        # Find pyproject.toml
        pyproject_path = find_pyproject_toml(file_path)
        if not pyproject_path:
            sys.exit(0)  # No pyproject.toml found, skip

        # Detect configured type checker
        checker = detect_configured_type_checker(pyproject_path)
        if not checker:
            sys.exit(0)  # No type checker configured, skip

        project_root = pyproject_path.parent

        # Check if file should be type checked
        if not should_check_file(file_path, project_root):
            sys.exit(0)

        # Get type checker command
        cmd_info = get_type_checker_command(checker, project_root)
        if not cmd_info:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": f"[{checker}] not available"
                }
            }))
            sys.exit(0)

        cmd, checker_name = cmd_info

        # Run type checker on the file
        full_cmd = cmd + [file_path]
        try:
            result = subprocess.run(full_cmd, capture_output=True, timeout=3)

            # Concise output: basename only
            name = checker_name.replace("uv run ", "")
            if result.returncode != 0:
                output = result.stdout.decode("utf-8", errors="ignore").strip()
                # First meaningful line
                error_line = ""
                for line in output.split("\n"):
                    line = line.strip()
                    if line and not line.startswith(("Success", "Found")):
                        error_line = f" — {line[:100]}"
                        break

                print(json.dumps({
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": f"[{name}] type-check failed{error_line}"
                    }
                }))
            else:
                print(json.dumps({
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": f"[{name}] type-checked {os.path.basename(file_path)}"
                    }
                }))

        except subprocess.TimeoutExpired:
            name = checker_name.replace("uv run ", "")
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": f"[{name}] timed out"
                }
            }))
        except FileNotFoundError:
            name = checker_name.replace("uv run ", "")
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": f"[{name}] not found"
                }
            }))

    except json.JSONDecodeError:
        # Invalid JSON input, skip silently
        sys.exit(0)
    except Exception as e:
        # Log error for debugging
        logger.debug("[type-check-on-edit] Unexpected error: %s", e, exc_info=True)
        sys.exit(0)


if __name__ == "__main__":
    main()
