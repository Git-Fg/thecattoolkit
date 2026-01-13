#!/usr/bin/env python3
"""
Verify Dependencies

Validates phase dependencies in ROADMAP.md for correctness.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple


def parse_roadmap(roadmap_path: Path) -> Dict[str, Dict]:
    """Parse ROADMAP.md and extract phase information."""
    phases = {}

    try:
        content = roadmap_path.read_text()
        lines = content.split('\n')

        in_phases_table = False

        for line in lines:
            # Start of phases table
            if '| Phase |' in line and 'Name' in line:
                in_phases_table = True
                continue

            # End of phases table (empty line or new section)
            if in_phases_table and (line.strip() == '' or line.startswith('#')):
                in_phases_table = False
                continue

            # Parse phase line
            if in_phases_table and '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 5:
                    phase_num = parts[1].strip()
                    phase_name = parts[2].strip()
                    status = parts[3].strip()
                    dependencies = parts[4].strip() if len(parts) > 4 else "none"

                    phases[phase_num] = {
                        'name': phase_name,
                        'status': status,
                        'dependencies': dependencies
                    }

    except Exception as e:
        print(f"Error parsing ROADMAP.md: {e}")
        return {}

    return phases


def validate_dependency_exists(phase_num: str, dep: str, all_phases: Set[str]) -> Tuple[bool, str]:
    """Check if a dependency phase exists."""
    if dep in all_phases:
        return True, f"Phase {dep} exists"
    else:
        return False, f"Phase {dep} does not exist"


def validate_dependency_status(phase_num: str, dep: str, dep_status: str) -> Tuple[bool, str]:
    """Check if a dependency is in a valid state."""
    if dep_status == '[x]':
        return True, f"Phase {dep} is complete"
    else:
        return False, f"Phase {dep} is not complete (status: {dep_status})"


def check_circular_dependency(phase_num: str, dep: str,
                            visited: Set[str],
                            recursion_stack: Set[str]) -> Tuple[bool, List[str]]:
    """Check for circular dependencies."""
    issues = []

    if dep in recursion_stack:
        issues.append(f"Circular dependency detected: {phase_num} -> {dep}")
        return False, issues

    if dep not in visited:
        visited.add(dep)
        recursion_stack.add(dep)

    return True, issues


def verify_dependencies(plan_dir: str) -> bool:
    """Verify all phase dependencies."""
    print(f"\n{'='*60}")
    print(f"Verifying Dependencies: {plan_dir}")
    print(f"{'='*60}\n")

    plan_path = Path(plan_dir)
    roadmap_path = plan_path / "ROADMAP.md"

    if not roadmap_path.exists():
        print(f"✗ ROADMAP.md not found: {roadmap_path}")
        return False

    # Parse roadmap
    phases = parse_roadmap(roadmap_path)

    if not phases:
        print("✗ No phases found in ROADMAP.md")
        return False

    print(f"Found {len(phases)} phases\n")

    all_valid = True
    all_phase_numbers = set(phases.keys())

    # Validate each phase
    for phase_num, phase_info in sorted(phases.items()):
        print(f"Phase {phase_num}: {phase_info['name']}")

        deps = phase_info['dependencies']
        if deps == "none" or not deps:
            print(f"  ✓ No dependencies")
            continue

        # Parse dependency list
        dep_list = [d.strip() for d in deps.split(',') if d.strip()]

        for dep in dep_list:
            # Check if dependency exists
            exists, msg = validate_dependency_exists(phase_num, dep, all_phase_numbers)
            print(f"  {'✓' if exists else '✗'} {msg}")
            all_valid = all_valid and exists

            if exists:
                # Check if dependency is complete
                dep_status = phases[dep]['status']
                complete, msg = validate_dependency_status(phase_num, dep, dep_status)
                print(f"    {'✓' if complete else '✗'} {msg}")
                all_valid = all_valid and complete

    # Check for circular dependencies
    print(f"\n{'='*60}")
    print("Checking for circular dependencies...")
    print(f"{'='*60}\n")

    visited = set()
    recursion_stack = set()

    def dfs(phase_num: str, path: List[str]) -> bool:
        if phase_num in recursion_stack:
            # Found circular dependency
            cycle = " -> ".join(path + [phase_num])
            print(f"✗ Circular dependency: {cycle}")
            return False

        if phase_num in visited:
            return True

        visited.add(phase_num)
        recursion_stack.add(phase_num)

        if phase_num in phases:
            deps = phases[phase_num]['dependencies']
            if deps != "none":
                for dep in deps.split(','):
                    dep = dep.strip()
                    if dep:
                        if not dfs(dep, path + [phase_num]):
                            return False

        recursion_stack.remove(phase_num)
        return True

    for phase_num in phases.keys():
        if phase_num not in visited:
            if not dfs(phase_num, []):
                all_valid = False

    # Dependency graph visualization
    print(f"\n{'='*60}")
    print("Dependency Graph:")
    print(f"{'='*60}\n")

    for phase_num in sorted(phases.keys()):
        phase_info = phases[phase_num]
        deps = phase_info['dependencies']
        status = phase_info['status']

        status_icon = {
            '[ ]': '⏳',
            '[~]': '🔄',
            '[x]': '✅',
            '[!]': '⛔'
        }.get(status, '?')

        print(f"{status_icon} Phase {phase_num}: {phase_info['name']}")

        if deps != "none" and deps:
            for dep in deps.split(','):
                dep = dep.strip()
                if dep:
                    dep_status = phases.get(dep, {}).get('status', '?')
                    print(f"    └─→ {dep} {dep_status}")

    # Summary
    print(f"\n{'='*60}")
    if all_valid:
        print("✅ Verification PASSED: All dependencies valid")
    else:
        print("❌ Verification FAILED: Dependency issues found")
    print(f"{'='*60}\n")

    return all_valid


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: verify-dependencies.py <plan-directory>")
        print("\nExample:")
        print("  python verify-dependencies.py .cattoolkit/plan/my-project")
        sys.exit(1)

    plan_dir = sys.argv[1]
    valid = verify_dependencies(plan_dir)

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
