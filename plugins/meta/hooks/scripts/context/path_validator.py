#!/usr/bin/env python3
"""
Path Validator Utility

Shared utility for validating file paths in hooks.
Prevents path traversal attacks by ensuring all paths stay within the project directory.

Usage:
    from path_validator import validate_path, safe_read, safe_write, is_safe_write

    if not validate_path(file_path):
        logger.error("Path traversal attempt")
        return
"""

import os
from pathlib import Path
from typing import Optional

# Security: Detect Plugin Root to prevent self-modification
CLAUDE_PLUGIN_ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT")


def is_safe_write(file_path: str) -> bool:
    """
    Check if writing to a file is safe.
    BLOCKS writes to the Plugin Root (cache) to prevent tampering.
    ALLOWS writes to Project Root.

    Args:
        file_path: Path to check

    Returns:
        True if safe to write, False if target is inside Plugin Root
    """
    try:
        if not CLAUDE_PLUGIN_ROOT:
            return True

        abs_path = os.path.abspath(file_path)
        return not abs_path.startswith(CLAUDE_PLUGIN_ROOT)
    except Exception:
        return False


SYSTEM_DIRS = {"/etc", "/usr", "/bin", "/sbin", "/var", "/opt", "/lib", "/System"}


def validate_path(file_path: str, base_dir: Optional[str] = None) -> bool:
    """
    Validate that a file path is within the allowed base directory.

    WHY: Prevents path traversal attacks where malicious input contains
    '../../../etc/passwd' to access files outside the project.

    Args:
        file_path: The path to validate
        base_dir: Base directory (defaults to current working directory)

    Returns:
        True if path is safe, False otherwise

    Examples:
        >>> validate_path("src/app.py")
        True
        >>> validate_path("../../../etc/passwd")
        False
        >>> validate_path("/tmp/secret.txt")
        False
    """
    # First, block system directories
    try:
        abs_path = os.path.abspath(file_path)
        for sys_dir in SYSTEM_DIRS:
            if abs_path.startswith(sys_dir):
                return False
    except Exception:
        pass

    if not file_path:
        return True

    if base_dir is None:
        base_dir = os.getcwd()

    try:
        base = Path(base_dir).resolve()
        target = Path(file_path).resolve()

        # Python 3.9+ has is_relative_to()
        if hasattr(target, "is_relative_to"):
            return target.is_relative_to(base)

        # Fallback for Python < 3.9
        try:
            target.relative_to(base)
            return True
        except ValueError:
            return False
    except (ValueError, OSError):
        return False


def get_safe_path(file_path: str, base_dir: Optional[str] = None) -> Optional[str]:
    """
    Get the safe, absolute path if valid, None otherwise.

    WHY: Sometimes you need the absolute path for operations while
    still validating safety.

    Args:
        file_path: The path to convert
        base_dir: Base directory (defaults to current working directory)

    Returns:
        Absolute path if safe, None if unsafe
    """
    if not validate_path(file_path, base_dir):
        return None

    try:
        return str(Path(file_path).resolve())
    except (ValueError, OSError):
        return None


def safe_read(file_path: str, base_dir: Optional[str] = None) -> Optional[str]:
    """
    Safely read a file only if it's within the base directory.

    WHY: Combines path validation with file reading for convenience.

    Args:
        file_path: Path to the file to read
        base_dir: Base directory (defaults to current working directory)

    Returns:
        File contents if safe and readable, None otherwise
    """
    safe_path = get_safe_path(file_path, base_dir)
    if not safe_path:
        return None

    try:
        with open(safe_path, "r") as f:
            return f.read()
    except (OSError, IOError):
        return None


def safe_write(file_path: str, content: str, base_dir: Optional[str] = None) -> bool:
    """
    Safely write to a file only if it's within the base directory.

    WHY: Combines path validation with file writing for convenience.

    Args:
        file_path: Path to the file to write
        content: Content to write
        base_dir: Base directory (defaults to current working directory)

    Returns:
        True if successful, False otherwise
    """
    safe_path = get_safe_path(file_path, base_dir)
    if not safe_path:
        return False

    try:
        with open(safe_path, "w") as f:
            f.write(content)
        return True
    except (OSError, IOError):
        return False


def is_safe_project_path(file_path: str) -> bool:
    """
    Check if path is within common project directories.

    WHY: Some hooks may want to be extra restrictive and only allow
    paths within src/, lib/, tests/, etc.

    Args:
        file_path: Path to check

    Returns:
        True if in safe project directory, False otherwise
    """
    safe_dirs = {"src", "lib", "tests", "docs", "scripts", "assets", "public", "config"}

    try:
        path = Path(file_path)
        if path.is_absolute():
            path = path.relative_to(Path.cwd())

        # Check if any parent directory is a safe directory
        for parent in path.parents:
            if parent.name in safe_dirs:
                return True

        return False
    except (ValueError, OSError):
        return False


if __name__ == "__main__":
    # Test cases
    import sys

    test_paths = [
        ("src/app.py", True),
        ("../../../etc/passwd", False),
        ("/tmp/secret.txt", False),
        ("tests/test.py", True),
        ("./relative/path.py", True),
    ]

    print("Path Validation Tests:")
    print("-" * 50)
    for path, expected in test_paths:
        result = validate_path(path)
        status = "✓" if result == expected else "✗"
        print(f"{status} {path}: {result} (expected: {expected})")

    print("\nSafe Path Examples:")
    print("-" * 50)
    safe = get_safe_path("src/app.py")
    print(f"src/app.py -> {safe}")
