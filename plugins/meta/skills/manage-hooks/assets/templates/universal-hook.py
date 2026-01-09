#!/usr/bin/env python3
import sys
import json
import os
import logging
import re

# Configuration: HOOK_MODE = "blocking" | "observer"
HOOK_MODE = "blocking"


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stderr,
    )


def validate_path(path):
    """Basic safety check for paths."""
    if not path or path.startswith("..") or "/../" in path:
        return False
    return True


def handle_operation(op_data):
    """
    Main logic for processing the tool invocation.
    In BLOCKING mode: Return {"status": "approve" | "block", "reason": "...", "message": "..."}
    In OBSERVER mode: Perform side effect and return optional data.
    """
    tool_name = op_data.get("tool")
    arguments = op_data.get("arguments", {})

    logging.info(f"Processing {tool_name} in {HOOK_MODE} mode")

    # EXAMPLE LOGIC: Block any 'Read' tool that targets .env files
    if HOOK_MODE == "blocking" and tool_name == "Read":
        path = arguments.get("path")
        if path and path.endswith(".env"):
            return {
                "status": "block",
                "reason": "security_policy",
                "message": "Direct access to .env files is restricted.",
            }

    # Default approval for blocking mode
    if HOOK_MODE == "blocking":
        return {"status": "approve"}

    # Observer mode just finishes
    return {"status": "success"}


def main():
    setup_logging()

    try:
        # Hooks receive tool data via STDIN as JSON
        input_data = sys.stdin.read()
        if not input_data:
            logging.error("No input data received")
            sys.exit(1)

        op_data = json.loads(input_data)
        result = handle_operation(op_data)

        # Hooks MUST output JSON to STDOUT
        print(json.dumps(result))

        # Exit code reflects success of the hook itself, not the approval
        sys.exit(0)

    except Exception as e:
        logging.error(f"Hook failed: {str(e)}")
        # In blocking mode, you might want to block on error for safety
        if HOOK_MODE == "blocking":
            print(
                json.dumps(
                    {
                        "status": "block",
                        "reason": "hook_error",
                        "message": f"Security hook failure: {str(e)}",
                    }
                )
            )
        sys.exit(0)  # Exit 0 so the supervisor handles the JSON block


if __name__ == "__main__":
    main()
