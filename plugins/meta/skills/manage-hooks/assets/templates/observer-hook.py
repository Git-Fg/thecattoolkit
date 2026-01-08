#!/usr/bin/env python3
"""
{hook-name}: {description}

Event: PostToolUse | SessionStart | Notification
Matcher: {tool-pattern}
Blocking: No

USE CASE: This template for hooks that observe/report without blocking actions.
Examples: Type checking, formatting, logging, notifications.
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


def observe_operation(tool_input: dict, tool_name: str, hook_data: dict) -> dict:
    """
    Observe and process the operation.

    WHY: Observer hooks don't block, they report. Return any output
    as additional context or warnings.
    """
    # {observation-logic}

    # Example: Run type checker on Python files
    # file_path = tool_input.get('file_path', '')
    # if file_path.endswith('.py'):
    #     result = run_type_checker(file_path)
    #     return {"warning": result} if result else {}

    # Example: Format code after edits
    # file_path = tool_input.get('file_path', '')
    # if should_format(file_path):
    #     run_formatter(file_path)

    # Default: no output
    return {}


def main():
    """Execute observer hook without blocking."""
    try:
        input_data = sys.stdin.read()
        if not input_data:
            logger.debug(f"[{__name__}] No input received")
            return

        hook_data = json.loads(input_data)

        tool_input = hook_data.get('tool_input', {})
        tool_name = hook_data.get('tool_name', '')

        # Path validation for file operations
        file_path = tool_input.get('file_path', '')
        if file_path and not validate_path(file_path):
            logger.error(f"[{__name__}] Path traversal attempt detected: {file_path}")
            return

        # Execute observation logic
        output = observe_operation(tool_input, tool_name, hook_data)

        # Observer hooks don't output blocking decisions
        # They can output additional context if needed
        if output:
            print(json.dumps(output))

    except json.JSONDecodeError as e:
        logger.error(f"[{__name__}] Invalid JSON input: {e}")
        # Observer hooks fail gracefully, don't block
        sys.exit(1)

    except Exception as e:
        logger.error(f"[{__name__}] Unexpected error: {e}", exc_info=True)
        # Observer hooks fail gracefully, don't block
        sys.exit(1)


if __name__ == "__main__":
    main()
