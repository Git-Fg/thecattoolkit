#!/usr/bin/env python3
"""
Mark Complete

Marks tasks or phases as complete.
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def mark_task_complete(plan_file: Path, task_index: int) -> bool:
    """Mark a specific task as complete."""
    try:
        content = plan_file.read_text()
        lines = content.split('\n')

        task_count = 0

        for i, line in enumerate(lines):
            if line.strip().startswith('### Task'):
                if task_count == task_index:
                    # Update status in this task
                    for j in range(i, min(i+20, len(lines))):
                        if '**Status:**' in lines[j]:
                            lines[j] = "**Status:** [x]"
                            break
                    else:
                        # Add status if not present
                        lines.insert(i+1, "**Status:** [x]")

                    plan_file.write_text('\n'.join(lines))
                    print(f"GOOD Task {task_index + 1} marked as complete")
                    return True

                task_count += 1

        print(f"✗ Task {task_index + 1} not found")
        return False

    except Exception as e:
        print(f"✗ Error updating task: {e}")
        return False


def mark_phase_complete(roadmap_path: Path, phase_num: str) -> bool:
    """Mark a phase as complete in ROADMAP.md."""
    try:
        if not roadmap_path.exists():
            print(f"✗ ROADMAP.md not found: {roadmap_path}")
            return False

        content = roadmap_path.read_text()
        lines = content.split('\n')

        for i, line in enumerate(lines):
            # Find phase in table
            if '|' in line and phase_num in line:
                parts = line.split('|')
                if len(parts) >= 4:
                    # Update status
                    parts[3] = ' [x] '
                    lines[i] = '|'.join(parts)

                    roadmap_path.write_text('\n'.join(lines))
                    print(f"GOOD Phase {phase_num} marked as complete")
                    return True

        print(f"✗ Phase {phase_num} not found in ROADMAP.md")
        return False

    except Exception as e:
        print(f"✗ Error updating phase: {e}")
        return False


def mark_all_tasks_complete(phase_dir: Path) -> bool:
    """Mark all tasks in a phase as complete."""
    plan_files = list(phase_dir.glob("*-PLAN.md"))

    if not plan_files:
        print(f"✗ No plan file found in {phase_dir}")
        return False

    plan_file = plan_files[0]

    try:
        content = plan_file.read_text()
        lines = content.split('\n')

        updated = False

        for i, line in enumerate(lines):
            if '**Status:**' in line:
                if line.strip() != '**Status:** [x]':
                    lines[i] = "**Status:** [x]"
                    updated = True

        if updated:
            plan_file.write_text('\n'.join(lines))
            print(f"GOOD All tasks marked as complete in {plan_file.name}")
            return True
        else:
            print(f"ℹ All tasks already complete")
            return True

    except Exception as e:
        print(f"✗ Error updating tasks: {e}")
        return False


def find_phase(phases_dir: Path, phase_num: str) -> Path:
    """Find a phase directory by number."""
    for dir_path in phases_dir.iterdir():
        if dir_path.is_dir() and dir_path.name.startswith(f"{phase_num}-"):
            return dir_path
    return None


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  mark-complete.py <plan-directory> phase <phase-number>")
        print("  mark-complete.py <plan-directory> task <phase-number> <task-index>")
        print("  mark-complete.py <plan-directory> all-tasks <phase-number>")
        print("\nExamples:")
        print("  python mark-complete.py .cattoolkit/plan/my-project phase 02")
        print("  python mark-complete.py .cattoolkit/plan/my-project task 02 0")
        print("  python mark-complete.py .cattoolkit/plan/my-project all-tasks 02")
        sys.exit(1)

    plan_dir = sys.argv[1]
    action = sys.argv[2]

    plan_path = Path(plan_dir)
    roadmap_path = plan_path / "ROADMAP.md"

    if action == "phase":
        if len(sys.argv) < 4:
            print("Error: Phase number required")
            sys.exit(1)

        phase_num = sys.argv[3]
        valid = mark_phase_complete(roadmap_path, phase_num)
        sys.exit(0 if valid else 1)

    elif action == "task":
        if len(sys.argv) < 5:
            print("Error: Phase number and task index required")
            sys.exit(1)

        phase_num = sys.argv[3]
        try:
            task_index = int(sys.argv[4])
        except ValueError:
            print("Error: Task index must be a number")
            sys.exit(1)

        phases_dir = plan_path / "phases"
        phase_dir = find_phase(phases_dir, phase_num)

        if not phase_dir:
            print(f"✗ Phase {phase_num} not found")
            sys.exit(1)

        plan_files = list(phase_dir.glob("*-PLAN.md"))
        if not plan_files:
            print(f"✗ No plan file found in {phase_dir}")
            sys.exit(1)

        valid = mark_task_complete(plan_files[0], task_index)
        sys.exit(0 if valid else 1)

    elif action == "all-tasks":
        if len(sys.argv) < 4:
            print("Error: Phase number required")
            sys.exit(1)

        phase_num = sys.argv[3]

        phases_dir = plan_path / "phases"
        phase_dir = find_phase(phases_dir, phase_num)

        if not phase_dir:
            print(f"✗ Phase {phase_num} not found")
            sys.exit(1)

        valid = mark_all_tasks_complete(phase_dir)
        sys.exit(0 if valid else 1)

    else:
        print(f"Error: Unknown action '{action}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
