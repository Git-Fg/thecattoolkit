#!/usr/bin/env python3
"""
Protect sensitive files from modification.
Warns about edits to production configs, lock files, and sensitive directories.
"""

import fnmatch
import json
import logging
import os
import sys
from typing import Optional

logger = logging.getLogger(__name__)

# Files/patterns to warn about
PROTECTED_PATTERNS = [
    # Lock files
    'package-lock.json',
    'yarn.lock',
    'pnpm-lock.yaml',
    'Gemfile.lock',
    'poetry.lock',
    'Cargo.lock',

    # Sensitive files
    '.env',
    '.env.local',
    '.env.production',
    'secrets/*',
    '*/secrets/*',
]

def check_file_protection(file_path: str) -> bool:
    """Check if file should be protected"""
    for pattern in PROTECTED_PATTERNS:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def main():
    """Main hook execution"""
    try:
        # Read input from stdin
        input_data = sys.stdin.read()
        if not input_data:
            return

        hook_data = json.loads(input_data)

        # Extract file path
        tool_input = hook_data.get('tool_input', {})
        file_path = tool_input.get('file_path', '')

        # Check if file should be protected
        if check_file_protection(file_path):
            logger.warning(f"⚠️ Warning: Editing protected file: {file_path}")

    except Exception as e:
        logger.error(f"Hook error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
