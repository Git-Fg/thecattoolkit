#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""
Validate YAML frontmatter in SKILL.md.

Usage:
    uv run scripts/validate-frontmatter.py <skill-directory>
"""

import sys
import re
import yaml

def validate_frontmatter(skill_dir):
    """Validate frontmatter structure and content"""
    errors = []
    warnings = []

    # Read SKILL.md
    try:
        with open(f'{skill_dir}/SKILL.md', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        errors.append("SKILL.md not found")
        return errors, warnings

    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not frontmatter_match:
        errors.append("No frontmatter found (must start with ---)")
        return errors, warnings

    try:
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML in frontmatter: {e}")
        return errors, warnings

    # Check required fields
    if 'name' not in frontmatter:
        errors.append("Missing required field: 'name'")
    if 'description' not in frontmatter:
        errors.append("Missing required field: 'description'")

    # Validate name field
    if 'name' in frontmatter:
        name = frontmatter['name']

        # Check format (kebab-case)
        if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', name):
            errors.append(
                f"Invalid name format: '{name}'. Must be kebab-case: "
                "lowercase letters, numbers, hyphens only. "
                "Must start with letter, no consecutive hyphens, no hyphens at start/end"
            )

        # Check length (3-50 chars)
        if len(name) < 3:
            errors.append(f"Name too short: '{name}' ({len(name)} chars, minimum 3)")
        if len(name) > 50:
            errors.append(f"Name too long: '{name}' ({len(name)} chars, maximum 50)")

        # Check matches directory name
        dir_name = skill_dir.split('/')[-1]
        if name != dir_name:
            errors.append(
                f"Name '{name}' doesn't match directory name '{dir_name}'. "
                "Skill name must match directory name."
            )

    # Validate description field
    if 'description' in frontmatter:
        description = frontmatter['description']

        # Check type (must be string, not list or dict)
        if not isinstance(description, str):
            errors.append(
                f"Description must be a string, not {type(description).__name__}"
            )

        # Check for multiline (should be single line)
        if '\n' in description:
            warnings.append(
                "Description should be single line. Multi-line descriptions may cause issues."
            )

    # Validate optional fields
    optional_fields = ['allowed-tools', 'user-invocable', 'context', 'disable-model-invocation', 'license', 'compatibility', 'version', 'author']

    for field in optional_fields:
        if field in frontmatter:
            value = frontmatter[field]

            # Validate allowed-tools
            if field == 'allowed-tools':
                if not isinstance(value, list):
                    errors.append(f"'allowed-tools' must be a list, not {type(value).__name__}")
                else:
                    for tool in value:
                        if not isinstance(tool, str):
                            errors.append(f"Tool '{tool}' must be a string")
                        elif '(' in tool and ')' not in tool:
                            errors.append(
                                f"Tool '{tool}' has invalid syntax. "
                                "Use 'Tool' or 'Tool(args)' format"
                            )

            # Validate user-invocable
            if field == 'user-invocable':
                if not isinstance(value, bool):
                    errors.append(
                        f"'user-invocable' must be boolean (true/false), not {type(value).__name__}"
                    )

            # Validate context
            if field == 'context':
                valid_contexts = ['fork']
                if value not in valid_contexts:
                    errors.append(
                        f"'context' must be one of {valid_contexts}, not '{value}'"
                    )

            # Validate disable-model-invocation
            if field == 'disable-model-invocation':
                if not isinstance(value, bool):
                    errors.append(
                        f"'disable-model-invocation' must be boolean (true/false), not {type(value).__name__}"
                    )

    # Check for unknown fields
    known_fields = ['name', 'description', 'allowed-tools', 'user-invocable', 'context', 'disable-model-invocation', 'license', 'compatibility', 'version', 'author']
    for field in frontmatter:
        if field not in known_fields:
            warnings.append(f"Unknown field: '{field}'. Is this intentional?")

    return errors, warnings

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate-frontmatter.py <skill-directory>")
        sys.exit(1)

    skill_dir = sys.argv[1]
    errors, warnings = validate_frontmatter(skill_dir)

    if errors:
        print("✗ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    if warnings:
        print("⚠ Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    print("✓ Frontmatter validation passed")
