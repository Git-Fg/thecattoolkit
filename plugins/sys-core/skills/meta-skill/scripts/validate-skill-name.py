#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Validate skill name follows naming conventions.

Usage:
    uv run scripts/validate-skill-name.py <skill-name>
"""

import sys
import re

def validate_name(name):
    """Validate skill name"""
    errors = []
    warnings = []

    # Check length
    if len(name) < 3:
        errors.append(f"Too short: {len(name)} chars (minimum 3)")
    if len(name) > 50:
        errors.append(f"Too long: {len(name)} chars (maximum 50)")

    # Check pattern
    pattern = r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$'
    if not re.match(pattern, name):
        errors.append(
            "Invalid format. Must be kebab-case: "
            "lowercase letters, numbers, hyphens only. "
            "Must start with letter, no consecutive hyphens, "
            "no hyphens at start/end"
        )

    return errors, warnings

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate-skill-name.py <skill-name>")
        sys.exit(1)

    name = sys.argv[1]
    errors, warnings = validate_name(name)

    if errors:
        print("✗ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    if warnings:
        print("⚠ Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    print(f"✓ Valid skill name: {name}")
