#!/usr/bin/env python3
"""
Resume Execution

Resumes execution from a handoff.
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def check_handoff_resolved(handoff_path: Path) -> Tuple[bool, str]:
    """Check if a handoff has been resolved."""
    if not handoff_path.exists():
        return False, "Handoff file not found"

    content = handoff_path.read_text()

    # Check for resolution markers
    if '**Resolution:**' in content:
        resolution = content.split('**Resolution:**')[1].split('\n')[0].strip()
        if resolution:
            return True, resolution

    return False, "No resolution found"


def verify_handoff_actions(handoff_path: Path) -> Tuple[bool, List[str]]:
    """Verify all handoff actions have been completed."""
    content = handoff_path.read_text()
    issues = []

    # Extract action items
    action_section = None
    if '## What You Need to Do' in content:
        action_section = content.split('## What You Need to Do')[1]

    if action_section:
        # Look for numbered actions
        actions = [line.strip() for line in action_section.split('\n')
                  if line.strip().startswith(('1.', '2.', '3.', '4.', '5.'))]

        for action in actions:
            # Check if action appears completed (simplified check)
            if not any(marker in content.lower() for marker in
                      ['completed', 'done', 'fixed', 'resolved', 'GOOD']):
                issues.append(f"Action may not be completed: {action}")

    return len(issues) == 0, issues


def update_phase_status(roadmap_path: Path, phase_num: str, new_status: str) -> None:
    """Update phase status in ROADMAP.md."""
    if not roadmap_path.exists():
        return

    content = roadmap_path.read_text()
    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Find phase in table
        if '|' in line and phase_num in line:
            parts = line.split('|')
            if len(parts) >= 4:
                # Update status
                parts[3] = f' {new_status} '
                lines[i] = '|'.join(parts)

    roadmap_path.write_text('\n'.join(lines))


def remove_handoff_file(handoff_path: Path) -> None:
    """Remove or rename handoff file after resolution."""
    if handoff_path.exists():
        # Rename to indicate it's resolved
        resolved_path = handoff_path.parent / f"RESOLVED-{handoff_path.name}"
        handoff_path.rename(resolved_path)
        print(f"Handoff moved to: {resolved_path}")


def resume_execution(plan_dir: str) -> bool:
    """Resume execution from handoff."""
    print(f"\n{'='*60}")
    print(f"Resuming Execution: {plan_dir}")
    print(f"{'='*60}\n")

    plan_path = Path(plan_dir)
    roadmap_path = plan_path / "ROADMAP.md"

    if not roadmap_path.exists():
        print(f"✗ ROADMAP.md not found: {roadmap_path}")
        return False

    # Find blocked phases
    content = roadmap_path.read_text()
    blocked_phases = []

    lines = content.split('\n')
    for line in lines:
        if '|' in line and '[!]' in line:
            # Extract phase number
            parts = line.split('|')
            if len(parts) >= 2:
                phase_info = parts[1].strip()
                if '-' in phase_info:
                    phase_num = phase_info.split('-')[0].strip()
                    phase_name = '-'.join(phase_info.split('-')[1:]).strip()
                    blocked_phases.append((phase_num, phase_name, line))

    if not blocked_phases:
        print("✓ No blocked phases found")
        return True

    print(f"Found {len(blocked_phases)} blocked phase(s)\n")

    all_resolved = True

    for phase_num, phase_name, table_line in blocked_phases:
        print(f"Phase {phase_num}: {phase_name}")

        # Find handoff file
        phases_dir = plan_path / "phases"
        handoff_path = None

        for dir_path in phases_dir.iterdir():
            if dir_path.is_dir() and dir_path.name.startswith(f"{phase_num}-"):
                potential_handoff = dir_path / "HANDOFF.md"
                if potential_handoff.exists():
                    handoff_path = potential_handoff
                    break

        if not handoff_path:
            print(f"  ⚠ Handoff file not found")
            all_resolved = False
            continue

        # Check if resolved
        resolved, resolution_msg = check_handoff_resolved(handoff_path)

        if resolved:
            print(f"  ✓ {resolution_msg}")

            # Verify actions
            actions_valid, issues = verify_handoff_actions(handoff_path)

            if not actions_valid:
                print(f"  ⚠ Some actions may not be completed:")
                for issue in issues:
                    print(f"    - {issue}")
                all_resolved = False
                continue

            # Update phase status
            update_phase_status(roadmap_path, phase_num, '[~]')
            print(f"  ✓ Phase status updated to [~]")

            # Remove handoff file
            remove_handoff_file(handoff_path)
            print(f"  ✓ Handoff resolved")

        else:
            print(f"  ✗ {resolution_msg}")
            all_resolved = False

        print()

    # Summary
    print(f"{'='*60}")
    if all_resolved:
        print("GOOD All handoffs resolved - execution can continue")
    else:
        print("BAD Some handoffs not resolved - execution blocked")
    print(f"{'='*60}\n")

    return all_resolved


def list_handoffs(plan_dir: str) -> None:
    """List all handoffs in the plan."""
    print(f"\n{'='*60}")
    print(f"Handoffs in: {plan_dir}")
    print(f"{'='*60}\n")

    plan_path = Path(plan_dir)
    phases_dir = plan_path / "phases"

    if not phases_dir.exists():
        print("No phases directory found")
        return

    handoffs = list(phases_dir.glob("*/HANDOFF.md"))

    if not handoffs:
        print("No handoffs found")
        return

    for handoff in sorted(handoffs):
        print(f"\n{handoff.relative_to(plan_path)}")
        print(f"  Modified: {handoff.stat().st_mtime}")

        content = handoff.read_text()

        # Extract reason
        if '**Reason:**' in content:
            reason = content.split('**Reason:**')[1].split('\n')[0].strip()
            print(f"  Reason: {reason}")

        # Extract date
        if '**Date:**' in content:
            date = content.split('**Date:**')[1].split('\n')[0].strip()
            print(f"  Date: {date}")

        # Check if resolved
        if '**Resolution:**' in content:
            resolution = content.split('**Resolution:**')[1].split('\n')[0].strip()
            if resolution:
                print(f"  GOOD Resolved: {resolution}")
            else:
                print(f"  ⚠ Resolution noted but no details")
        else:
            print(f"  ⛔ Not resolved")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: resume-execution.py <plan-directory> [--list]")
        print("\nExamples:")
        print("  python resume-execution.py .cattoolkit/plan/my-project")
        print("  python resume-execution.py .cattoolkit/plan/my-project --list")
        sys.exit(1)

    plan_dir = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == '--list':
        list_handoffs(plan_dir)
        sys.exit(0)

    valid = resume_execution(plan_dir)

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
