#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""
Validate skill description follows Standard OR Enhanced pattern.

Standard Pattern: {CAPABILITY}. Use when {TRIGGERS}.
Enhanced Pattern: {CAPABILITY}. {MODAL} Use when {TRIGGERS}.

Usage:
    uv run scripts/validate-description.py <skill-directory>
"""

import sys
import re
import yaml

def validate_description(skill_dir):
    """Validate skill description against Standard OR Enhanced pattern"""
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

    # Check description exists
    if 'description' not in frontmatter:
        errors.append("Missing 'description' field in frontmatter")
        return errors, warnings

    description = frontmatter['description']

    # Check length
    if len(description) < 50:
        errors.append(f"Description too short: {len(description)} chars (minimum 50)")
    if len(description) > 1024:
        errors.append(f"Description too long: {len(description)} chars (maximum 1024)")

    # Detect pattern type
    modal_pattern = r'(MUST|PROACTIVELY|SHOULD)\s+Use when'
    standard_pattern = r'Use when'
    old_pattern = r'^USE when'  # Old Cat Toolkit style

    has_modal = bool(re.search(modal_pattern, description))
    has_standard = bool(re.search(standard_pattern, description, re.IGNORECASE))
    has_old_style = bool(re.match(old_pattern, description))

    # Check for old style (starting with "USE when")
    if has_old_style:
        errors.append(
            "Description starts with 'USE when' (old style). "
            "Should start with capability statement. "
            "Format: '{CAPABILITY}. Use when {TRIGGERS}.'"
        )

    # Check for "Use when" pattern
    if not has_modal and not has_standard:
        errors.append("Missing 'Use when' trigger pattern")

    # Pattern-specific validation
    if has_modal:
        # Enhanced pattern - check capability comes first
        parts = description.split('.')
        if len(parts) < 2:
            errors.append("Missing capability statement before modal")
        else:
            capability_part = parts[0].strip()
            if len(capability_part) < 10:
                errors.append("Capability statement too short (before modal)")

        # CRITICAL: Check if using Enhanced pattern in non-infrastructure context
        is_infrastructure = 'sys-core' in skill_dir or 'sys-meta' in skill_dir or 'sys-builder' in skill_dir
        if not is_infrastructure:
            warnings.append(
                "WARNING: Enhanced pattern (MUST/PROACTIVELY/SHOULD) should be used for "
                "internal infrastructure only. Consider Standard pattern for portability."
            )
    else:
        # Standard pattern validation
        if description.startswith('Use when') or description.startswith('use when'):
            errors.append(
                "Description should start with capability, not 'Use when'. "
                "Format: '{CAPABILITY}. Use when {TRIGGERS}.'"
            )

        # CRITICAL: Check if using Standard pattern in infrastructure context
        is_infrastructure = 'sys-core' in skill_dir or 'sys-meta' in skill_dir or 'sys-builder' in skill_dir
        if is_infrastructure:
            warnings.append(
                "WARNING: Using Standard pattern in infrastructure context. "
                "Consider Enhanced pattern (MUST/PROACTIVELY/SHOULD) for internal toolkit standards."
            )

    # Check for trigger specificity
    use_when_parts = re.split(r'Use when', description, flags=re.IGNORECASE)
    if len(use_when_parts) > 1:
        triggers = use_when_parts[1].strip()
        if len(triggers) < 20:
            warnings.append("Triggers seem vague. Add specific user phrases.")
        if ',' not in triggers and ' or ' not in triggers:
            warnings.append("Consider adding multiple trigger phrases (comma or 'or' separated)")

    # Check for vague language
    vague_phrases = [
        'helps with',
        'assists with',
        'useful for',
        'tool for',
        'skill for',
        'a skill that',
        'a tool that'
    ]
    has_vague = any(phrase in description.lower() for phrase in vague_phrases)
    if has_vague:
        warnings.append(
            "Description contains vague language. Be specific about capabilities. "
            "Avoid: 'helps with', 'assists with', 'useful for', 'tool for'"
        )

    # Check 3rd person
    first_person = ['I ', 'I\'m', 'We ', 'We\'re', 'my ', 'our ']
    has_first_person = any(fp in description for fp in first_person)
    if has_first_person:
        errors.append("Description should be in 3rd person (avoid 'I', 'We', 'my', 'our')")

    return errors, warnings

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/validate-description.py <skill-directory>")
        print("\nPatterns supported:")
        print("  Standard: {CAPABILITY}. Use when {TRIGGERS}.")
        print("  Enhanced: {CAPABILITY}. {MODAL} Use when {TRIGGERS}.")
        sys.exit(1)

    skill_dir = sys.argv[1]
    errors, warnings = validate_description(skill_dir)

    if errors:
        print("✗ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    if warnings:
        print("⚠ Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    print("✓ Description validation passed")
