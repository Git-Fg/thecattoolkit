#!/usr/bin/env python3
"""
Validate Plan Structure

Validates BRIEF, ROADMAP, and PHASE files against project-lifecycle standards.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple


def validate_file_exists(file_path: Path, file_type: str) -> Tuple[bool, str]:
    """Check if a required file exists."""
    if file_path.exists():
        return True, f"✓ {file_type} exists"
    else:
        return False, f"✗ {file_type} missing: {file_path}"


def validate_roadmap_structure(roadmap_path: Path) -> Tuple[bool, List[str]]:
    """Validate ROADMAP.md structure."""
    issues = []
    valid_statuses = ['[ ]', '[~]', '[x]', '[!]']

    try:
        content = roadmap_path.read_text()

        # Check for required sections
        if '# Roadmap:' not in content:
            issues.append("Missing 'Roadmap:' header")

        if '## Phases' not in content:
            issues.append("Missing '## Phases' section")

        # Check for table
        if '| Phase |' not in content:
            issues.append("Missing phases table")

        # Validate status codes
        for line in content.split('\n'):
            if '|' in line and 'Phase' not in line:
                for status in valid_statuses:
                    if status in line:
                        break
                else:
                    if any(s in line for s in ['[done]', '[complete]', '[in progress]']):
                        issues.append(f"Invalid status format: {line.strip()}")

    except Exception as e:
        issues.append(f"Error reading ROADMAP.md: {e}")

    return len(issues) == 0, issues


def validate_phase_structure(phase_dir: Path, phase_num: str) -> Tuple[bool, List[str]]:
    """Validate a phase directory and plan file."""
    issues = []

    # Check directory naming
    if not phase_dir.name.startswith(f"{phase_num}-"):
        issues.append(f"Phase directory should start with '{phase_num}-'")

    # Check for plan file
    plan_files = list(phase_dir.glob("*-PLAN.md"))
    if not plan_files:
        issues.append(f"No *-PLAN.md file found in {phase_dir}")
    elif len(plan_files) > 1:
        issues.append(f"Multiple plan files found: {plan_files}")

    return len(issues) == 0, issues


def validate_dependencies(roadmap_path: Path) -> Tuple[bool, List[str]]:
    """Validate phase dependencies."""
    issues = []

    try:
        content = roadmap_path.read_text()
        phases = []

        # Extract phase information
        lines = content.split('\n')
        for line in lines:
            if '|' in line and 'Phase' not in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4:
                    phase_num = parts[1].strip()
                    dependencies = parts[4].strip() if len(parts) > 4 else "none"
                    phases.append((phase_num, dependencies))

        # Check dependencies
        phase_dict = {num: deps for num, deps in phases}

        for phase_num, deps in phase_dict.items():
            if deps and deps != "none":
                # Parse dependencies
                dep_list = [d.strip() for d in deps.split(',')]

                for dep in dep_list:
                    # Check if dependency exists
                    if dep not in phase_dict:
                        issues.append(f"Phase {phase_num} depends on non-existent phase {dep}")

                    # Check for circular dependency (simplified)
                    if dep == phase_num:
                        issues.append(f"Phase {phase_num} cannot depend on itself")

    except Exception as e:
        issues.append(f"Error validating dependencies: {e}")

    return len(issues) == 0, issues


def validate_plan_structure(plan_dir: str) -> bool:
    """Validate complete plan structure."""
    print(f"\n{'='*60}")
    print(f"Validating Plan Structure: {plan_dir}")
    print(f"{'='*60}\n")

    plan_path = Path(plan_dir)
    all_valid = True

    # Check if plan directory exists
    if not plan_path.exists():
        print(f"✗ Plan directory not found: {plan_path}")
        return False

    # Validate BRIEF.md
    print("1. Validating BRIEF.md...")
    brief_path = plan_path / "BRIEF.md"
    valid, msg = validate_file_exists(brief_path, "BRIEF.md")
    print(f"   {msg}")
    all_valid = all_valid and valid

    # Validate ROADMAP.md
    print("\n2. Validating ROADMAP.md...")
    roadmap_path = plan_path / "ROADMAP.md"
    valid, msg = validate_file_exists(roadmap_path, "ROADMAP.md")
    print(f"   {msg}")
    all_valid = all_valid and valid

    if valid:
        print("\n3. Validating ROADMAP structure...")
        valid, issues = validate_roadmap_structure(roadmap_path)
        if issues:
            for issue in issues:
                print(f"   ✗ {issue}")
            all_valid = False
        else:
            print("   ✓ ROADMAP structure valid")

        print("\n4. Validating dependencies...")
        valid, issues = validate_dependencies(roadmap_path)
        if issues:
            for issue in issues:
                print(f"   ✗ {issue}")
            all_valid = False
        else:
            print("   ✓ Dependencies valid")

    # Validate phases directory
    print("\n5. Validating phases directory...")
    phases_dir = plan_path / "phases"
    if phases_dir.exists():
        print(f"   ✓ Phases directory exists")

        # Validate each phase
        phase_dirs = [d for d in phases_dir.iterdir() if d.is_dir()]
        if not phase_dirs:
            print(f"   ⚠ No phase directories found")

        for phase_dir in sorted(phase_dirs):
            print(f"\n   Validating {phase_dir.name}...")
            # Extract phase number
            phase_num = phase_dir.name.split('-')[0]
            valid, issues = validate_phase_structure(phase_dir, phase_num)
            if issues:
                for issue in issues:
                    print(f"      ✗ {issue}")
                all_valid = False
            else:
                print(f"      ✓ {phase_dir.name} valid")
    else:
        print(f"   ⚠ Phases directory not found")

    # Summary
    print(f"\n{'='*60}")
    if all_valid:
        print("GOOD Validation PASSED: Plan structure is valid")
    else:
        print("BAD Validation FAILED: Plan structure has issues")
    print(f"{'='*60}\n")

    return all_valid


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: validate-plan-structure.py <plan-directory>")
        print("\nExample:")
        print("  python validate-plan-structure.py .cattoolkit/plan/my-project")
        sys.exit(1)

    plan_dir = sys.argv[1]
    valid = validate_plan_structure(plan_dir)

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
