#!/usr/bin/env python3
"""
PreCompact Hook: Creates memory checkpoints before context compaction.
Simplified version using shared utilities.
"""

import sys
import os
import datetime
import json
from pathlib import Path

# Import shared utilities
try:
    from utils import get_project_root, is_safe_path, is_safe_write
except ImportError:
    # Inline fallbacks if utils not found
    import subprocess

    def get_project_root():
        if d := os.environ.get("CLAUDE_PROJECT_DIR"):
            return Path(d)
        try:
            return Path(
                subprocess.check_output(
                    ["git", "rev-parse", "--show-toplevel"],
                    encoding="utf-8",
                    stderr=subprocess.DEVNULL,
                ).strip()
            )
        except:
            return Path.cwd()

    def is_safe_path(p):
        try:
            return os.path.commonpath([os.getcwd(), os.path.abspath(p)]) == os.getcwd()
        except:
            return False

    def is_safe_write(p):
        plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
        abs_p = os.path.abspath(p)
        return (
            is_safe_path(p)
            and not (plugin_root and abs_p.startswith(plugin_root))
            and ".git" not in abs_p.split(os.sep)
        )


def read_file_safe(path):
    """Safely read a file."""
    try:
        if not is_safe_path(str(path)):
            return ""
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
    except Exception:
        pass
    return ""


def write_file_safe(path, content):
    """Safely write a file."""
    try:
        if not is_safe_write(str(path)):
            return False
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return True
    except Exception:
        return False


def extract_key_actions(context_log):
    """Extract last 20 tool actions from log."""
    return [line for line in context_log.split("\n") if "[20" in line][-20:]


def main():
    """Compact memory by creating checkpoint and updating scratchpad."""
    try:
        root = get_project_root()
        context_log_path = root / ".cattoolkit/context/context.log"
        scratchpad_path = root / ".cattoolkit/context/scratchpad.md"
        checkpoints_path = root / ".cattoolkit/context/checkpoints"

        context_log = read_file_safe(context_log_path)
        scratchpad = read_file_safe(scratchpad_path)

        if not context_log and not scratchpad:
            print(
                json.dumps({"continue": True, "systemMessage": "No context to compact"})
            )
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        actions = extract_key_actions(context_log)
        actions_summary = (
            "\n".join(f"- {a}" for a in actions) if actions else "No recent actions."
        )

        # Create checkpoint
        checkpoint = f"# Checkpoint - {timestamp}\n\n## Actions\n{actions_summary}\n\n## Scratchpad\n{scratchpad[:500]}{'...' if len(scratchpad) > 500 else ''}\n"
        checkpoint_file = (
            checkpoints_path
            / f"checkpoint-{timestamp.replace(':', '-').replace(' ', '-')}.md"
        )
        write_file_safe(checkpoint_file, checkpoint)

        # Update scratchpad with summary
        if scratchpad:
            lines = scratchpad.split("\n")
            for i, line in enumerate(lines):
                if "## Recent Actions" in line or "## Memory Summary" in line:
                    lines = lines[:i]
                    break
            lines.extend([f"\n## Recent Actions ({timestamp})", actions_summary])
            write_file_safe(scratchpad_path, "\n".join(lines))

        # Clear context log
        if os.path.exists(context_log_path) and is_safe_write(str(context_log_path)):
            with open(context_log_path, "w") as f:
                f.write(f"[{timestamp}] Memory compacted\n")

        print(
            json.dumps(
                {
                    "continue": True,
                    "systemMessage": f"Memory compacted. Checkpoint: {checkpoint_file.name}",
                }
            )
        )

    except Exception as e:
        print(
            json.dumps({"continue": True, "systemMessage": f"Compaction warning: {e}"})
        )


if __name__ == "__main__":
    main()
