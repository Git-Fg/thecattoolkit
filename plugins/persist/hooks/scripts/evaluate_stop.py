#!/usr/bin/env python3
"""
Stop Hook: Evaluates if the session should stop or continue.
Checks for uncommitted git changes and active HANDOFF.md files.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def get_project_root() -> Path:
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


def check_uncommitted_changes() -> bool:
    """Returns True if there are uncommitted git changes."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            encoding="utf-8",
            timeout=5,
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def check_handoff_exists() -> bool:
    """Returns True if HANDOFF.md exists in planning directory."""
    root = get_project_root()
    handoff = root / ".cattoolkit/planning/HANDOFF.md"
    return handoff.exists()


def main():
    try:
        input_data = json.load(sys.stdin)
        stop_hook_active = input_data.get("stop_hook_active", False)

        if stop_hook_active:
            sys.exit(0)

        blockers = []

        if check_uncommitted_changes():
            blockers.append("uncommitted git changes")

        if check_handoff_exists():
            blockers.append("active HANDOFF.md")

        if blockers:
            reason = f"Blockers detected: {', '.join(blockers)}. Commit changes or resolve handoff before stopping."
            print(json.dumps({"decision": "block", "reason": reason}))
        else:
            print(json.dumps({"decision": None}))

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
