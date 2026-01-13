#!/usr/bin/env python3
"""
Lint Plan Files

Lints plan files for quality, consistency, and completeness.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple


def lint_brief(brief_path: Path) -> List[str]:
    """Lint BRIEF.md file."""
    issues = []

    try:
        content = brief_path.read_text()

        # Check required sections
        if '# Project:' not in content:
            issues.append("Missing '# Project:' header")

        if '## Objective' not in content:
            issues.append("Missing '## Objective' section")

        if '## Success Criteria' not in content:
            issues.append("Missing '## Success Criteria' section")

        # Check for success criteria format
        if '- [ ]' not in content and '- [x]' not in content:
            issues.append("Success criteria should use '- [ ]' format")

        # Check for empty sections
        if '## Objective' in content:
            obj_section = content.split('## Objective')[1].split('##')[0]
            if not obj_section.strip() or obj_section.strip() == '\n':
                issues.append("Objective section is empty")

        # Check for measurable success criteria
        if '## Success Criteria' in content:
            criteria_section = content.split('## Success Criteria')[1]
            criteria_lines = [line.strip() for line in criteria_section.split('\n')
                            if line.strip().startswith('- [')]

            for line in criteria_lines:
                criteria = line.lower()
                if any(word in criteria for word in ['better', 'good', 'nice', 'something']):
                    issues.append(f"Success criteria should be measurable: {line}")

    except Exception as e:
        issues.append(f"Error reading BRIEF.md: {e}")

    return issues


def lint_roadmap(roadmap_path: Path) -> List[str]:
    """Lint ROADMAP.md file."""
    issues = []

    try:
        content = roadmap_path.read_text()

        # Check required sections
        if '# Roadmap:' not in content:
            issues.append("Missing '# Roadmap:' header")

        if '## Phases' not in content:
            issues.append("Missing '## Phases' section")

        if '| Phase |' not in content:
            issues.append("Missing phases table")

        # Check table structure
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '| Phase |' in line:
                # Check header
                if 'Name' not in line or 'Status' not in line:
                    issues.append(f"Line {i+1}: Table header should include Name and Status")

                # Check separator
                if i+1 < len(lines):
                    sep_line = lines[i+1]
                    if not all(c in '|-: ' for c in sep_line):
                        issues.append(f"Line {i+2}: Invalid table separator format")

        # Validate status codes
        valid_statuses = ['[ ]', '[~]', '[x]', '[!]']
        for line in lines:
            if '|' in line and 'Phase' not in line:
                for status in valid_statuses:
                    if status in line:
                        break
                else:
                    # Check for invalid status
                    if any(s in line for s in ['[done]', '[complete]', '[in progress]', '[pending]']):
                        issues.append(f"Invalid status format: {line.strip()}")

        # Check for dependency column
        if 'Dependencies' not in content:
            issues.append("Missing 'Dependencies' column in table")

    except Exception as e:
        issues.append(f"Error reading ROADMAP.md: {e}")

    return issues


def lint_phase_plan(phase_plan_path: Path) -> List[str]:
    """Lint a phase plan file."""
    issues = []

    try:
        content = phase_plan_path.read_text()

        # Check required sections
        if '# Phase' not in content:
            issues.append("Missing '# Phase' header")

        if '## Tasks' not in content and '## Overview' not in content:
            issues.append("Missing '## Tasks' or '## Overview' section")

        # Check for task format
        if '### Task' in content:
            # Count tasks
            task_matches = re.findall(r'### Task \d+:', content)
            num_tasks = len(task_matches)

            if num_tasks == 0:
                issues.append("No tasks found")

            # Check each task for required fields
            for i, match in enumerate(re.finditer(r'### Task \d+:(.*?)(?=### Task|\Z)', content, re.DOTALL):
                task_content = match.group(1)

                # Check for required fields
                required_fields = ['Scope:', 'Action:', 'Verify:', 'Done:']
                for field in required_fields:
                    if field not in task_content:
                        issues.append(f"Task {i+1}: Missing '{field}' field")

                # Check for action verb
                action_match = re.search(r'Action:(.*?)(?:\n|$)', task_content)
                if action_match:
                    action_text = action_match.group(1).strip()
                    if action_text and not action_text[0].isupper():
                        issues.append(f"Task {i+1}: Action should start with capital letter")

        # Check handoff protocol
        if '## Handoff' not in content:
            issues.append("Missing '## Handoff' section")

        if 'HANDOFF.md' not in content:
            issues.append("Handoff section should mention HANDOFF.md")

    except Exception as e:
        issues.append(f"Error reading phase plan: {e}")

    return issues


def lint_summary(summary_path: Path) -> List[str]:
    """Lint a phase summary file."""
    issues = []

    try:
        content = summary_path.read_text()

        # Check required sections
        if '**Status:**' not in content:
            issues.append("Missing '**Status:**' field")

        if '**Date:**' not in content:
            issues.append("Missing '**Date:**' field")

        # Check for completed tasks
        if '- [x]' not in content:
            issues.append("Summary should list completed tasks with '- [x]'")

    except Exception as e:
        issues.append(f"Error reading summary: {e}")

    return issues


def lint_plan_directory(plan_dir: Path) -> bool:
    """Lint all files in a plan directory."""
    print(f"\n{'='*60}")
    print(f"Linting Plan Files: {plan_dir}")
    print(f"{'='*60}\n")

    all_valid = True

    # Lint BRIEF.md
    print("1. Linting BRIEF.md...")
    brief_path = plan_dir / "BRIEF.md"
    if brief_path.exists():
        issues = lint_brief(brief_path)
        if issues:
            for issue in issues:
                print(f"  ✗ {issue}")
            all_valid = False
        else:
            print(f"  ✅ BRIEF.md valid")
    else:
        print(f"  ⚠ BRIEF.md not found")

    # Lint ROADMAP.md
    print("\n2. Linting ROADMAP.md...")
    roadmap_path = plan_dir / "ROADMAP.md"
    if roadmap_path.exists():
        issues = lint_roadmap(roadmap_path)
        if issues:
            for issue in issues:
                print(f"  ✗ {issue}")
            all_valid = False
        else:
            print(f"  ✅ ROADMAP.md valid")
    else:
        print(f"  ⚠ ROADMAP.md not found")

    # Lint phase plans
    print("\n3. Linting phase plans...")
    phases_dir = plan_dir / "phases"
    if phases_dir.exists():
        phase_plans = list(phases_dir.glob("*/*-PLAN.md"))

        if not phase_plans:
            print(f"  ⚠ No phase plans found")
        else:
            for plan_file in sorted(phase_plans):
                print(f"\n  Linting {plan_file.relative_to(plan_dir)}...")
                issues = lint_phase_plan(plan_file)
                if issues:
                    for issue in issues:
                        print(f"    ✗ {issue}")
                    all_valid = False
                else:
                    print(f"    ✅ Valid")

    # Lint summaries
    print("\n4. Linting phase summaries...")
    if phases_dir.exists():
        summaries = list(phases_dir.glob("*/SUMMARY.md"))

        if not summaries:
            print(f"  ⚠ No summaries found")
        else:
            for summary_file in sorted(summaries):
                print(f"\n  Linting {summary_file.relative_to(plan_dir)}...")
                issues = lint_summary(summary_file)
                if issues:
                    for issue in issues:
                        print(f"    ✗ {issue}")
                    all_valid = False
                else:
                    print(f"    ✅ Valid")

    # Summary
    print(f"\n{'='*60}")
    if all_valid:
        print("✅ Linting PASSED: All files valid")
    else:
        print("❌ Linting FAILED: Issues found")
    print(f"{'='*60}\n")

    return all_valid


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: lint-plan-files.py <plan-directory>")
        print("\nExample:")
        print("  python lint-plan-files.py .cattoolkit/plan/my-project")
        sys.exit(1)

    plan_dir = Path(sys.argv[1])
    if not plan_dir.exists():
        print(f"Error: Plan directory not found: {plan_dir}")
        sys.exit(1)

    valid = lint_plan_directory(plan_dir)

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
