#!/usr/bin/env python3
"""
{hook-name}: {description}

Event: PreToolUse | Stop
Matcher: {tool-pattern}
Blocking: Yes

USE CASE: This template for hooks that need to approve/block actions before they execute.
Examples: Security checks, secret detection, dangerous command validation.
"""

import json
import logging
import os
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def validate_path(file_path: str, base_dir: str = None) -> bool:
    """
    Prevent path traversal attacks.

    WHY: Malicious input could contain '../../../etc/passwd' to access files
    outside the project directory.
    """
    if not file_path:
        return True

    if base_dir is None:
        base_dir = os.getcwd()

    try:
        base = Path(base_dir).resolve()
        target = Path(file_path).resolve()

        # Python 3.9+ has is_relative_to()
        if hasattr(target, 'is_relative_to'):
            return target.is_relative_to(base)

        # Fallback for Python < 3.9
        try:
            target.relative_to(base)
            return True
        except ValueError:
            return False
    except (ValueError, OSError):
        return False


def validate_operation(tool_input: dict, tool_name: str) -> tuple[bool, str]:
    """
    Validate the operation and return (approve: bool, reason: str).

    WHY: Centralized validation logic makes it easy to test and modify.
    Return True to allow, False to block with reason.
    """
    # {validation-logic}

    # Example: Check for secrets
    # content = tool_input.get('content', '')
    # if 'sk-' in content and 'openai' not in content.lower():
    #     return False, "Potential OpenAI API key detected in content"

    # Example: Check dangerous commands
    # command = tool_input.get('command', '')
    # if 'rm -rf' in command and '/ ' in command:
    #     return False, "Dangerous delete command detected"

    # Default: approve with reason
    return True, "Operation validated successfully"


def main():
    """Execute blocking hook validation with security checks."""
    try:
        input_data = sys.stdin.read()
        if not input_data:
            logger.debug(f"[{__name__}] No input received")
            return

        hook_data = json.loads(input_data)

        # Security: Prevent infinite loops in Stop hooks
        # WHY: Stop hooks can trigger themselves, this flag breaks the cycle
        if hook_data.get('stop_hook_active', False):
            result = {
                "decision": "approve",
                "reason": "Stop hook already active"
            }
            print(json.dumps(result))
            return

        tool_input = hook_data.get('tool_input', {})
        tool_name = hook_data.get('tool_name', '')

        # Path validation for file operations
        file_path = tool_input.get('file_path', '')
        if file_path and not validate_path(file_path):
            result = {
                "decision": "block",
                "reason": f"Path traversal attempt detected: {file_path}"
            }
            print(json.dumps(result))
            return

        # Execute validation logic
        approved, reason = validate_operation(tool_input, tool_name)

        # Output blocking decision as JSON
        # WHY: Claude reads this JSON to decide whether to proceed
        result = {
            "decision": "approve" if approved else "block",
            "reason": reason
        }
        print(json.dumps(result))

    except json.JSONDecodeError as e:
        logger.error(f"[{__name__}] Invalid JSON input: {e}")
        result = {
            "decision": "block",
            "reason": f"Invalid input format: {e}"
        }
        print(json.dumps(result))
        sys.exit(1)

    except Exception as e:
        logger.error(f"[{__name__}] Unexpected error: {e}", exc_info=True)
        # Block on unexpected errors for safety
        result = {
            "decision": "block",
            "reason": f"Hook execution failed: {e}"
        }
        print(json.dumps(result))
        sys.exit(1)


if __name__ == "__main__":
    main()
