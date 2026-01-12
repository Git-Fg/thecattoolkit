#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""
Master validation script - runs all validation checks.

Usage:
    uv run scripts/validate-all.py <skill-directory>
"""

import sys
import os
import subprocess
import re
import yaml

# Import validation functions from other scripts
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def validate_name(skill_dir):
    """Validate skill name"""
    errors = []
    warnings = []

    # Extract name from frontmatter
    try:
        with open(f'{skill_dir}/SKILL.md', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        errors.append("SKILL.md not found")
        return errors, warnings

    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not frontmatter_match:
        errors.append("No frontmatter found")
        return errors, warnings

    try:
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML: {e}")
        return errors, warnings

    if 'name' not in frontmatter:
        errors.append("Missing 'name' field")
        return errors, warnings

    name = frontmatter['name']

    # Check format
    if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', name):
        errors.append(
            "Invalid format. Must be kebab-case: "
            "lowercase letters, numbers, hyphens only"
        )

    # Check length
    if len(name) < 3:
        errors.append(f"Too short: {len(name)} chars (minimum 3)")
    if len(name) > 50:
        errors.append(f"Too long: {len(name)} chars (maximum 50)")

    # Check matches directory
    dir_name = skill_dir.split('/')[-1]
    if name != dir_name:
        errors.append(f"Name '{name}' doesn't match directory '{dir_name}'")

    return errors, warnings

def validate_description(skill_dir):
    """Validate skill description"""
    errors = []
    warnings = []

    try:
        with open(f'{skill_dir}/SKILL.md', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return errors, warnings

    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not frontmatter_match:
        return errors, warnings

    try:
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
    except yaml.YAMLError:
        return errors, warnings

    if 'description' not in frontmatter:
        errors.append("Missing 'description' field")
        return errors, warnings

    description = frontmatter['description']

    # Check pattern
    if not re.match(r'^(MUST|SHOULD|PROACTIVELY)?\s*USE when\s+.+', description):
        errors.append(
            "Description must start with '(MODAL) USE when' pattern"
        )

    # Check length
    if len(description) < 10:
        errors.append(f"Description too short: {len(description)} chars")
    if len(description) > 1024:
        errors.append(f"Description too long: {len(description)} chars")

    return errors, warnings

def validate_structure(skill_dir):
    """Validate file structure"""
    errors = []
    warnings = []

    # Check SKILL.md exists
    if not os.path.exists(f'{skill_dir}/SKILL.md'):
        errors.append("Missing SKILL.md file")
        return errors, warnings

    # Check SKILL.md length
    try:
        with open(f'{skill_dir}/SKILL.md', 'r') as f:
            lines = f.readlines()
            line_count = len(lines)

            if line_count > 500:
                errors.append(
                    f"SKILL.md too long: {line_count} lines (should be < 400 for progressive disclosure)"
                )
    except FileNotFoundError:
        errors.append("SKILL.md not found")

    # Check optional directories
    optional_dirs = ['references', 'examples', 'workflows', 'scripts', 'assets']
    for dir_name in optional_dirs:
        dir_path = f'{skill_dir}/{dir_name}'
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            if not files:
                warnings.append(f"Empty directory: {dir_name}/")

    return errors, warnings

def validate_progressive_disclosure(skill_dir):
    """Validate progressive disclosure implementation"""
    errors = []
    warnings = []

    skill_md_path = f'{skill_dir}/SKILL.md'
    if not os.path.exists(skill_md_path):
        return errors, warnings

    with open(skill_md_path, 'r') as f:
        content = f.read()
        line_count = len(content.split('\n'))

        # Check if over 500 lines
        if line_count > 500:
            # Check if references directory exists
            if not os.path.exists(f'{skill_dir}/references'):
                errors.append(
                    "SKILL.md > 500 lines but no references/ directory found."
                    "Use progressive disclosure to move detailed content to references/"
                )

    return errors, warnings

def run_validation(skill_dir):
    """Run all validation checks"""
    print(f"\n{'='*70}")
    print(f"Validating: {skill_dir}")
    print(f"{'='*70}\n")

    all_errors = []
    all_warnings = []

    # Run each validation
    validations = [
        ('Name', validate_name),
        ('Description', validate_description),
        ('Structure', validate_structure),
        ('Progressive Disclosure', validate_progressive_disclosure),
    ]

    for name, validator in validations:
        errors, warnings = validator(skill_dir)

        if errors:
            print(f"\n❌ {name} Validation Failed:")
            for error in errors:
                print(f"   - {error}")
            all_errors.extend(errors)

        if warnings:
            print(f"\n⚠️  {name} Warnings:")
            for warning in warnings:
                print(f"   - {warning}")
            all_warnings.extend(warnings)

        if not errors and not warnings:
            print(f"\n✅ {name} validation passed")

    # Summary
    print(f"\n{'='*70}")
    print(f"Validation Summary")
    print(f"{'='*70}\n")

    if all_errors:
        print(f"❌ FAILED: {len(all_errors)} error(s) found")
        return False
    else:
        print(f"✅ PASSED: All validations successful")

    if all_warnings:
        print(f"⚠️  {len(all_warnings)} warning(s) - review recommended")

    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-all.py <skill-directory>")
        print("\nExample:")
        print("  python validate-all.py ./my-skill/")
        print("  python validate-all.py ./plugins/my-plugin/skills/my-skill/")
        sys.exit(1)

    skill_dir = sys.argv[1]
    if not os.path.exists(skill_dir):
        print(f"Error: Directory '{skill_dir}' not found")
        sys.exit(1)

    success = run_validation(skill_dir)

    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
