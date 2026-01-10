import sys
import os
import datetime
import json
import subprocess
from pathlib import Path

# Bootstrap: Detect CLAUDE_PLUGIN_ROOT from environment
CLAUDE_PLUGIN_ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT")
if not CLAUDE_PLUGIN_ROOT:
    # Fallback: try to detect from script location
    current_script = Path(__file__).resolve()
    for parent in current_script.parents:
        if (parent / "plugins").exists():
            CLAUDE_PLUGIN_ROOT = str(parent)
            break

# Import path_validator for security
try:
    from path_validator import validate_path
except ImportError:
    # Fail closed - block unsafe operations
    sys.stderr.write("CRITICAL: path_validator not found. Blocking unsafe operations.\n")

    def validate_path(path):
        return False

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))


def is_safe_write(file_path: str) -> bool:
    """
    Check if writing to a file is safe.
    BLOCKS writes to the Plugin Root (cache) to prevent tampering.
    BLOCKS writes to .git directories.
    ALLOWS writes to Project Root.
    """
    try:
        abs_path = os.path.abspath(file_path)

        # Block Plugin Root
        if CLAUDE_PLUGIN_ROOT and abs_path.startswith(CLAUDE_PLUGIN_ROOT):
            return False

        # Block .git
        if ".git" in abs_path.split(os.sep):
            return False

        return True
    except Exception:
        return False


def read_file_safe(path):
    """Safely read a file, return empty string if not found or error."""
    try:
        if not validate_path(path):
            return ""
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
    except Exception:
        pass
    return ""


def write_file_safe(path, content):
    """Safely write a file, creating directories if needed."""
    try:
        if not validate_path(path):
            return False

        if not is_safe_write(path):
            return False

        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return True
    except Exception as e:
        return False


def extract_key_actions(context_log):
    """Extract meaningful actions from context log."""
    actions = []
    lines = context_log.split("\n")

    for line in lines:
        if "[20" in line and "Tool:" in line:
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


def get_project_root():
    """Find the project root using git or environment variables."""
    try:
        result = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            encoding="utf-8"
        ).strip()
        return Path(result)
    except Exception:
        return Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))


def main():
    """Compact memory by creating a summary and updating scratchpad."""
    try:
        root = get_project_root()
        context_log_path = root / ".cattoolkit/context/context.log"
        scratchpad_path = root / ".cattoolkit/context/scratchpad.md"
        summary_path = root / ".cattoolkit/context/checkpoints"

        context_log = read_file_safe(context_log_path)
        scratchpad = read_file_safe(scratchpad_path)

        if not context_log and not scratchpad:
            print(
                json.dumps(
                    {
                        "continue": True,
                        "systemMessage": "Memory compaction: No context to compact",
                    }
                )
            )
            sys.exit(0)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        actions = extract_key_actions(context_log)
        actions_summary = summarize_actions(actions)

        checkpoint_summary = f"""# Memory Checkpoint - {timestamp}

## Summary of Recent Session

{actions_summary}

## Original Scratchpad Content

{scratchpad[:500]}{"..." if len(scratchpad) > 500 else ""}

---
*Checkpoint created automatically by PreCompact hook*
"""

        checkpoint_file = f"{summary_path}/checkpoint-{timestamp.replace(':', '-').replace(' ', '-')}.md"
        write_file_safe(checkpoint_file, checkpoint_summary)

        if scratchpad:
            lines = scratchpad.split("\n")

            memory_section_index = -1
            for i, line in enumerate(lines):
                if "## Recent Actions" in line or "## Memory Summary" in line:
                    memory_section_index = i
                    break

            if memory_section_index >= 0:
                lines = lines[:memory_section_index]
            else:
                lines.append("\n## Recent Actions (Auto-Updated)")

            lines.append(f"\n### {timestamp}")
            lines.append(actions_summary)

            new_scratchpad = "\n".join(lines)

            write_file_safe(scratchpad_path, new_scratchpad)

        if (
            os.path.exists(context_log_path)
            and validate_path(context_log_path)
            and is_safe_write(str(context_log_path))
        ):
            with open(context_log_path, "w") as f:
                f.write(f"[{timestamp}] Memory checkpoint created\n")
                f.write(
                    f"[{timestamp}] Context compacted - summary moved to scratchpad\n\n"
                )

        print(
            json.dumps(
                {
                    "continue": True,
                    "systemMessage": f"Memory compacted at {timestamp}. Checkpoint created.",
                    "hookSpecificOutput": {
                        "checkpoint": str(checkpoint_file),
                        "actions_summarized": len(actions),
                    },
                }
            )
        )

    except Exception as e:
        print(
            json.dumps(
                {
                    "continue": True,
                    "systemMessage": f"Memory compaction warning: {str(e)}",
                }
            )
        )


if __name__ == "__main__":
    main()
