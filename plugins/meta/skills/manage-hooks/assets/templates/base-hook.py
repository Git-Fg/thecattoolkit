#!/usr/bin/env python3
"""
{hook-name}: {description}

Event: {event-type}
Matcher: {tool-pattern}
"""

import json
import logging
import os
import sys
from pathlib import Path

# Configure logging - hooks should be observable but not noisy
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def validate_path(file_path: str, base_dir: str = None) -> bool:
    """
    Prevent path traversal attacks.

    WHY: Malicious input could contain '../../../etc/passwd' to access files
    outside the project directory. This validation ensures all file operations
    stay within the allowed base directory.
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


def main():
    """
    Main hook execution with security and error handling.

    WHY: Failing loudly is better than silently corrupting state. Invalid JSON,
    missing input, or unexpected errors should be logged but not crash the hook.
    """
    try:
        # Read input from stdin
        # WHY: Claude passes context via stdin as JSON. Empty input means no context.
        input_data = sys.stdin.read()
        if not input_data:
            logger.debug(f"[{__name__}] No input received")
            return

        # Parse JSON input with error handling
        # WHY: Invalid JSON should fail gracefully, not block all operations
        hook_data = json.loads(input_data)

        # Security: Check for infinite loop prevention flag (Stop hooks)
        # WHY: Stop hooks can trigger themselves recursively. This flag prevents
        # infinite loops by detecting when a Stop hook is already active.
        if hook_data.get('stop_hook_active', False):
            logger.debug(f"[{__name__}] Stop hook already active, skipping")
            return

        # Extract tool input for validation
        # WHY: Different events provide different context. Extract consistently.
        tool_input = hook_data.get('tool_input', {})
        tool_name = hook_data.get('tool_name', '')

        # Path validation for file operations
        # WHY: Only validate paths when actually dealing with files to avoid false positives
        file_path = tool_input.get('file_path', '')
        if file_path and not validate_path(file_path):
            logger.error(f"[{__name__}] Path traversal attempt detected: {file_path}")
            return

        # {hook-logic}

        # For blocking hooks, output decision as JSON:
        # result = {
        #     "decision": "approve" | "block",
        #     "reason": "Explanation of decision"
        # }
        # print(json.dumps(result))

    except json.JSONDecodeError as e:
        # WHY: Don't block operations on malformed input, just log and continue
        logger.error(f"[{__name__}] Invalid JSON input: {e}")
        sys.exit(1)

    except Exception as e:
        # WHY: Catch-all for unexpected errors. Log with traceback for debugging.
        logger.error(f"[{__name__}] Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
