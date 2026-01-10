#!/usr/bin/env python3
"""
SessionStart Hook: Restores context from Planner and scratchpad.
This runs automatically when a session starts to load the current plan and working memory.
"""

import os
import glob
import json
import sys
from pathlib import Path
from datetime import datetime

import subprocess


def get_project_root():
    """Find the project root using git or environment variables."""
    try:
        return Path(
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], encoding="utf-8"
            ).strip()
        )
    except Exception:
        return Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))


def output(msg):
    """Output plain text for SessionStart hooks - stdout is injected as context."""
    print(msg)


def find_active_plan():
    """Finds the active PLAN.md from the planner plugin."""
    root = get_project_root()
    plans = root.glob(".cattoolkit/planning/**/*.md")
    plans = [str(p) for p in plans if "PLAN.md" in p.name]

    if not plans:
        return {"found": False, "content": "No active plan found.", "path": None}

    latest_plan = max(plans, key=os.path.getmtime)

    try:
        with open(latest_plan, "r") as f:
            content = f.read()
            # Extract meaningful section (first 800 chars to avoid overwhelming)
            preview = content[:800] + ("..." if len(content) > 800 else "")
            return {"found": True, "content": preview, "path": latest_plan}
    except Exception as e:
        return {
            "found": False,
            "content": f"Error reading active plan: {str(e)}",
            "path": latest_plan,
        }


def get_scratchpad():
    """Loads the scratchpad state."""
    path = get_project_root() / ".cattoolkit/context/scratchpad.md"
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                content = f.read()
                preview = content[:600] + ("..." if len(content) > 600 else "")
                return {"found": True, "content": preview, "size": len(content)}
        except Exception as e:
            return {
                "found": False,
                "content": f"Error reading scratchpad: {str(e)}",
                "size": 0,
            }
    return {"found": False, "content": "Scratchpad not yet initialized.", "size": 0}


def get_context_log():
    """Loads recent context log entries."""
    path = get_project_root() / ".cattoolkit/context/context.log"
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                lines = f.readlines()
                recent = lines[-10:] if len(lines) > 10 else lines
                return {
                    "found": True,
                    "content": "".join(recent),
                    "total_entries": len(lines),
                }
        except Exception as e:
            return {
                "found": False,
                "content": f"Error reading context log: {str(e)}",
                "total_entries": 0,
            }
    return {"found": False, "content": "No context log yet.", "total_entries": 0}


def get_todos():
    """Loads the todo list if it exists."""
    path = get_project_root() / ".cattoolkit/context/todos.md"
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                content = f.read()
                preview = content[:400] + ("..." if len(content) > 400 else "")
                return {"found": True, "content": preview, "size": len(content)}
        except Exception as e:
            return {
                "found": False,
                "content": f"Error reading todos: {str(e)}",
                "size": 0,
            }
    return {"found": False, "content": "No todos tracked yet.", "size": 0}


def main():
    """Main execution: loads all context and displays a comprehensive summary."""
    plan = find_active_plan()
    scratchpad = get_scratchpad()
    context_log = get_context_log()
    todos = get_todos()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"""# 🧠 MEMORY RESTORED - {timestamp}

## 📋 Current Plan (Source of Truth)
**Status**: {"✅ Active plan loaded" if plan["found"] else "⚠️ No active plan"}
**Source**: `{plan["path"] or "N/A"}`

{plan["content"]}

---

## 📝 Scratchpad (Working Memory)
**Status**: {"✅ Loaded" if scratchpad["found"] else "⚠️ Not initialized"}
**Size**: {scratchpad["size"]} characters

{scratchpad["content"]}

---

## ✅ Active Tasks (Todos)
**Status**: {"✅ Loaded" if todos["found"] else "ℹ️ Not tracking todos"}
**Size**: {todos["size"]} characters

{todos["content"]}

---

## 📊 Session History (Recent)
**Status**: {f"✅ {context_log['total_entries']} entries" if context_log["found"] else "ℹ️ No history yet"}

{context_log["content"]}

---

## 🔄 Auto-Memory System Active

This session is using **Passive Memory Hooks**:
- ✅ **SessionStart**: Plan and scratchpad auto-loaded
- ✅ **PostToolUse**: All edits/bash logged automatically
- ✅ **PreCompact**: Memory compaction before context overflow

> System ready. Context fully restored from persistent storage.
"""

    output(message)


if __name__ == "__main__":
    main()
