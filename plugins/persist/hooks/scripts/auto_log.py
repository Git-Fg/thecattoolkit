#!/usr/bin/env python3
"""
PostToolUse Hook: Automatically logs state-changing tool executions.
This runs after Edit, Write, and Bash operations to maintain session history.
"""

import sys
import os
import json
import datetime
import subprocess
from pathlib import Path

plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
if plugin_root and plugin_root not in sys.path:
    sys.path.insert(0, plugin_root)


def get_project_root():
    """Find the project root using git or environment variables."""
    try:
        # Try git first
        return Path(
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], encoding="utf-8"
            ).strip()
        )
    except Exception:
        # Fallback to current dir or environment variable
        return Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))


def main():
    """Log tool execution to context.log."""
    try:
        input_data = sys.stdin.read()

        if not input_data:
            sys.exit(0)

        data = json.loads(input_data)

        tool = data.get("tool_name", "Unknown")
        parameters = data.get("parameters", {})

        STATE_CHANGING_TOOLS = ["Edit", "Write", "Bash"]

        if tool not in STATE_CHANGING_TOOLS:
            print(json.dumps({"status": "success"}))
            sys.exit(0)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"[{timestamp}] Tool: {tool}\n"
        log_entry += "<forensics>\n"
        log_entry += f"  <raw_input>{json.dumps(parameters, default=str)}</raw_input>\n"

        if tool == "Edit":
            file_path = parameters.get("file_path", "unknown")
            log_entry += f"  <target>{file_path}</target>\n"

        elif tool == "Write":
            file_path = parameters.get("TargetFile", "unknown")
            log_entry += f"  <target>{file_path}</target>\n"

        elif tool == "Bash":
            command = parameters.get("command", "unknown")
            log_entry += f"  <command>{command[:200]}</command>\n"

        log_entry += "</forensics>\n\n"

        log_path = get_project_root() / ".cattoolkit/context/context.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        with open(log_path, "a") as f:
            f.write(log_entry)

        print(json.dumps({"status": "success"}))

    except json.JSONDecodeError:
        print(json.dumps({"status": "success"}))
    except Exception:
        print(json.dumps({"status": "success"}))


if __name__ == "__main__":
    main()
