#!/usr/bin/env python3
"""
Check Frontmatter

Validates YAML frontmatter in skill and command files for compliance.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict


# Valid frontmatter fields for skills
SKILL_FIELDS = {
    'required': ['name', 'description'],
    'optional': [
        'allowed-tools', 'user-invocable', 'context', 'agent',
        'disable-model-invocation'
    ]
}

# Valid frontmatter fields for commands
COMMAND_FIELDS = {
    'required': ['description'],
    'optional': [
        'argument-hint', 'allowed-tools', 'disable-model-invocation'
    ]
}

# Valid tool names
VALID_TOOLS = {
    'Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep',
    'Skill', 'Task', 'AskUserQuestion', 'TodoWrite',
    'WebFetch', 'WebSearch', 'ListMcpResourcesTool',
    'ReadMcpResourceTool'
}


def parse_frontmatter(file_path: Path) -> Tuple[Dict, str, bool]:
    """Parse YAML frontmatter from a markdown file."""
    try:
        content = file_path.read_text()

        # Check for frontmatter
        if not content.startswith('---'):
            return {}, content, False

        # Extract frontmatter
        end_yaml = content.find('\n---', 3)
        if end_yaml == -1:
            return {}, content, False

        yaml_content = content[3:end_yaml]

        # Parse YAML (simple implementation)
        frontmatter = {}
        for line in yaml_content.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Handle arrays
                if value.startswith('[') and value.endswith(']'):
                    # Parse array
                    items = value[1:-1].split(',')
                    value = [item.strip().strip('"') for item in items]

                frontmatter[key] = value

        return frontmatter, content, True

    except Exception as e:
        print(f"Error parsing frontmatter in {file_path}: {e}")
        return {}, content, False


def validate_name(field_name: str, value: str) -> Tuple[bool, List[str]]:
    """Validate the 'name' field."""
    issues = []

    # Skill name validation
    if not value:
        issues.append("'name' is required")
    elif not re.match(r'^[a-z][a-z0-9-]{2,49}$', value):
        issues.append(
            "'name' must match pattern: ^[a-z][a-z0-9-]{2,49}$"
        )

    return len(issues) == 0, issues


def validate_description(field_name: str, value: str) -> Tuple[bool, List[str]]:
    """Validate the 'description' field."""
    issues = []

    if not value:
        issues.append("'description' is required")
    elif len(value) < 10:
        issues.append("'description' should be at least 10 characters")

    # Check for 3rd person (no "I/me/you")
    if any(word in value.lower() for word in ['i ', 'me ', 'my ', 'you ', 'your ']):
        issues.append("'description' should use 3rd person (no I/me/you)")

    return len(issues) == 0, issues


def validate_allowed_tools(field_name: str, value: List[str]) -> Tuple[bool, List[str]]:
    """Validate the 'allowed-tools' field."""
    issues = []

    if not value:
        return True, []

    if not isinstance(value, list):
        issues.append("'allowed-tools' must be a list")
        return False, issues

    for tool in value:
        # Check for Skill(tool) format
        if tool.startswith('Skill(') and tool.endswith(')'):
            skill_name = tool[6:-1]
            if not skill_name:
                issues.append(f"Invalid skill format: {tool}")
        elif tool.startswith('Bash('):
            # Bash tools are OK
            pass
        elif tool not in VALID_TOOLS:
            # Check if it's a valid Skill reference
            if not (tool.startswith('Skill(') or tool.startswith('Bash(')):
                issues.append(f"Unknown tool: {tool}")

    return len(issues) == 0, issues


def validate_user_invocable(field_name: str, value: any) -> Tuple[bool, List[str]]:
    """Validate the 'user-invocable' field."""
    issues = []

    if value is not None and not isinstance(value, bool):
        issues.append("'user-invocable' must be a boolean (true/false)")

    return len(issues) == 0, issues


def validate_context(field_name: str, value: str) -> Tuple[bool, List[str]]:
    """Validate the 'context' field."""
    issues = []

    if value and value not in ['fork', 'clone']:
        issues.append("'context' must be 'fork' or 'clone'")

    return len(issues) == 0, issues


def validate_field(field_name: str, value: any, field_type: str) -> Tuple[bool, List[str]]:
    """Validate a single frontmatter field."""
    validators = {
        'name': validate_name,
        'description': validate_description,
        'allowed-tools': validate_allowed_tools,
        'user-invocable': validate_user_invocable,
        'context': validate_context,
    }

    if field_name in validators:
        return validators[field_name](field_name, value)

    # Unknown field
    return True, []


def check_frontmatter(file_path: Path, file_type: str) -> bool:
    """Check frontmatter for a single file."""
    frontmatter, content, has_frontmatter = parse_frontmatter(file_path)

    print(f"\n{file_path}")

    # Determine valid fields based on file type
    if file_path.name == 'SKILL.md':
        valid_fields = SKILL_FIELDS['required'] + SKILL_FIELDS['optional']
    elif file_path.suffix == '.md' and 'commands' in file_path.parts:
        valid_fields = COMMAND_FIELDS['required'] + COMMAND_FIELDS['optional']
    else:
        # Unknown file type
        return True

    all_valid = True

    # Check for required fields
    if file_type == 'skill':
        required = SKILL_FIELDS['required']
    else:
        required = COMMAND_FIELDS['required']

    for field in required:
        if field not in frontmatter:
            print(f"  ✗ Missing required field: {field}")
            all_valid = False

    # Validate all present fields
    for field_name, value in frontmatter.items():
        if field_name in valid_fields:
            valid, issues = validate_field(field_name, value, file_type)
            if issues:
                for issue in issues:
                    print(f"  ✗ {field_name}: {issue}")
                all_valid = False
            else:
                print(f"  ✓ {field_name}: valid")
        else:
            print(f"  ⚠ Unknown field: {field_name}")

    # Check for disallowed fields
    forbidden = ['permissionMode', 'model']
    for field in frontmatter.keys():
        if field in forbidden:
            print(f"  ✗ Forbidden field: {field}")
            all_valid = False

    if not has_frontmatter:
        print(f"  ⚠ No frontmatter found")

    if all_valid and has_frontmatter:
        print(f"  ✅ Frontmatter valid")

    return all_valid


def find_skills_and_commands(root_dir: Path) -> List[Tuple[Path, str]]:
    """Find all skill and command files."""
    results = []

    # Find SKILL.md files
    for skill_dir in root_dir.glob('skills/*'):
        skill_file = skill_dir / 'SKILL.md'
        if skill_file.exists():
            results.append((skill_file, 'skill'))

    # Find command files
    for cmd_file in root_dir.glob('commands/*.md'):
        results.append((cmd_file, 'command'))

    return results


def main():
    """Main entry point."""
    plugin_root = Path(__file__).parent.parent.parent

    print(f"{'='*60}")
    print(f"Checking Frontmatter Compliance")
    print(f"{'='*60}\n")

    files_to_check = find_skills_and_commands(plugin_root)

    if not files_to_check:
        print("No skill or command files found")
        sys.exit(0)

    all_valid = True
    stats = defaultdict(int)

    for file_path, file_type in files_to_check:
        valid = check_frontmatter(file_path, file_type)
        all_valid = all_valid and valid
        stats[file_type] += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Skills checked: {stats['skill']}")
    print(f"  Commands checked: {stats['command']}")

    if all_valid:
        print(f"\n✅ All frontmatter valid")
    else:
        print(f"\n❌ Some frontmatter has issues")

    print(f"{'='*60}\n")

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
