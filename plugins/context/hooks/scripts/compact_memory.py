#!/usr/bin/env python3
"""
PreCompact Hook: Compacts memory before context overflow.
This runs when context window is near capacity to preserve critical information.
"""
import sys
import json
import datetime
import re
from pathlib import Path

def read_file_safe(path):
    """Safely read a file, return empty string if not found or error."""
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()
    except:
        pass
    return ""

def write_file_safe(path, content):
    """Safely write a file, creating directories if needed."""
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        return False

def extract_key_actions(context_log):
    """Extract meaningful actions from context log."""
    actions = []
    lines = context_log.split('\n')

    for line in lines:
        if '[20' in line and 'Tool:' in line:
            actions.append(line)

    return actions[-20:]  # Last 20 actions

def summarize_actions(actions):
    """Create a summary of recent actions."""
    if not actions:
        return "No recent actions."

    summary = "**Recent Actions:**\n"
    for action in actions:
        summary += f"- {action}\n"

    return summary

def main():
    """Compact memory by creating a summary and updating scratchpad."""
    try:
        context_log_path = ".cattoolkit/context/context.log"
        scratchpad_path = ".cattoolkit/context/scratchpad.md"
        summary_path = ".cattoolkit/context/checkpoints"

        context_log = read_file_safe(context_log_path)
        scratchpad = read_file_safe(scratchpad_path)

        if not context_log and not scratchpad:
            print(json.dumps({"status": "success", "message": "No context to compact"}))
            sys.exit(0)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        actions = extract_key_actions(context_log)
        actions_summary = summarize_actions(actions)

        checkpoint_summary = f"""# Memory Checkpoint - {timestamp}

## Summary of Recent Session

{actions_summary}

## Original Scratchpad Content

{scratchpad[:500]}{'...' if len(scratchpad) > 500 else ''}

---
*Checkpoint created automatically by PreCompact hook*
"""

        checkpoint_file = f"{summary_path}/checkpoint-{timestamp.replace(':', '-').replace(' ', '-')}.md"
        write_file_safe(checkpoint_file, checkpoint_summary)

        if scratchpad:
            lines = scratchpad.split('\n')

            memory_section_index = -1
            for i, line in enumerate(lines):
                if '## Recent Actions' in line or '## Memory Summary' in line:
                    memory_section_index = i
                    break

            if memory_section_index >= 0:
                lines = lines[:memory_section_index]
            else:
                lines.append("\n## Recent Actions (Auto-Updated)")

            lines.append(f"\n### {timestamp}")
            lines.append(actions_summary)

            new_scratchpad = '\n'.join(lines)

            write_file_safe(scratchpad_path, new_scratchpad)

        if os.path.exists(context_log_path):
            with open(context_log_path, 'w') as f:
                f.write(f"[{timestamp}] Memory checkpoint created\n")
                f.write(f"[{timestamp}] Context compacted - summary moved to scratchpad\n\n")

        print(json.dumps({
            "status": "success",
            "message": f"Memory compacted at {timestamp}",
            "checkpoint": checkpoint_file,
            "actions_summarized": len(actions)
        }))

    except Exception as e:
        print(json.dumps({
            "status": "success",
            "message": f"Memory compaction completed with warnings: {str(e)}"
        }))

if __name__ == "__main__":
    import os
    main()
