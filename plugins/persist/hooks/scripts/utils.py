#!/usr/bin/env python3
"""Shared utilities for hook scripts."""

import os
import subprocess
from pathlib import Path


def get_project_root() -> Path:
    """Find the project root using CLAUDE_PROJECT_DIR or git."""
    if project_dir := os.environ.get("CLAUDE_PROJECT_DIR"):
        return Path(project_dir)
    try:
        return Path(
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                encoding="utf-8",
                stderr=subprocess.DEVNULL,
            ).strip()
        )
    except Exception:
        return Path.cwd()


def is_safe_path(file_path: str) -> bool:
    """Check path is within project root (prevents path traversal)."""
    try:
        project_root = os.getcwd()
        target_path = os.path.abspath(os.path.join(project_root, file_path))
        return os.path.commonpath([project_root, target_path]) == project_root
    except Exception:
        return False


def is_safe_write(file_path: str) -> bool:
    """Check if writing to a file is safe (blocks plugin cache and .git)."""
    try:
        abs_path = os.path.abspath(file_path)
        plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
        if plugin_root and abs_path.startswith(plugin_root):
            return False
        if ".git" in abs_path.split(os.sep):
            return False
        return is_safe_path(file_path)
    except Exception:
        return False
