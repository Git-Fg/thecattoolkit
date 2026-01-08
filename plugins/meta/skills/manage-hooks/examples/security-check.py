#!/usr/bin/env python3
"""
Security check hook for potential secrets.
Warns about API keys, passwords, and tokens in code.
"""

import json
import logging
import re
import sys

logger = logging.getLogger(__name__)

# Patterns that might indicate secrets
SECRET_PATTERNS = [
    r'api[_-]?key["\s]*[:=]["\s]*[a-zA-Z0-9]{20,}',
    r'secret[_-]?key["\s]*[:=]["\s]*[a-zA-Z0-9]{20,}',
    r'password["\s]*[:=]["\s]*[^\s"\']+',
    r'token["\s]*[:=]["\s]*[a-zA-Z0-9]{20,}',
]


def check_for_secrets(file_path: str, content: str) -> bool:
    """Check if content contains potential secrets"""
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False


def main():
    """Main hook execution"""
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return

        hook_data = json.loads(input_data)
        tool_input = hook_data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")

        if check_for_secrets(file_path, content):
            logger.warning(f"⚠️ Warning: Potential secrets detected in {file_path}")

    except Exception as e:
        logger.error(f"Hook error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
