#!/usr/bin/env python3
"""
Evaluate Stop Hook
Deterministic safety check before allowing session stop.

Checks for:
- Uncommitted git changes (dirty working tree)
- Active HANDOFF.md files (blocked work in progress)

Returns 'block' if session is dirty, 'allow' otherwise.
"""

import sys
import os
import json
import subprocess
from pathlib import Path

plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
if plugin_root and plugin_root not in sys.path:
    sys.path.insert(0, plugin_root)


def get_project_root():
    """Find the project root using git or environment variables."""
    try:
        return Path(
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                encoding="utf-8",
                stderr=subprocess.DEVNULL,
            ).strip()
        )
    except Exception:
        return Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))


def check_uncommitted_changes():
    """Check if there are uncommitted git changes."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=get_project_root(),
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def check_active_handoffs():
    """Check for active HANDOFF.md files indicating blocked work."""
    project_root = get_project_root()
    planning_dir = project_root / ".cattoolkit" / "planning"

    if not planning_dir.exists():
        return []

    handoffs = list(planning_dir.rglob("HANDOFF.md"))
    return [str(h.relative_to(project_root)) for h in handoffs]


def main():
    """Evaluate if session stop is safe."""
    blockers = []

    if check_uncommitted_changes():
        blockers.append("Uncommitted git changes detected")

    active_handoffs = check_active_handoffs()
    if active_handoffs:
        blockers.append(f"Active HANDOFF.md files: {', '.join(active_handoffs)}")

    if blockers:
        result = {
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "ok": False,
                "reason": f"Session stop blocked: {'; '.join(blockers)}. Commit changes or resolve handoffs before stopping.",
            }
        }
    else:
        result = {
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "ok": True,
                "reason": "Session stop approved - no uncommitted changes or active handoffs",
            }
        }

    print(json.dumps(result))


if __name__ == "__main__":
    main()
