#!/usr/bin/env python3
"""
Run Phase

Executes a single phase of a plan.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


def load_phase_plan(phase_dir: Path) -> Dict:
    """Load a phase plan from file."""
    plan_files = list(phase_dir.glob("*-PLAN.md"))

    if not plan_files:
        raise FileNotFoundError(f"No plan file found in {phase_dir}")

    if len(plan_files) > 1:
        raise ValueError(f"Multiple plan files found: {plan_files}")

    plan_file = plan_files[0]
    content = plan_file.read_text()

    # Parse tasks from markdown
    tasks = []
    task_sections = content.split('### Task')

    for section in task_sections[1:]:  # Skip first split (before first task)
        lines = section.split('\n')
        task_name = lines[0].strip() if lines else ""

        task = {
            'name': task_name,
            'content': '\n'.join(lines[1:]).strip(),
            'status': '[ ]'  # Default
        }

        # Check for status in content
        if '**Status:**' in task['content']:
            # Extract status
            status_match = task['content'].split('**Status:**')[1].split('\n')[0].strip()
            task['status'] = status_match

        tasks.append(task)

    return {
        'name': phase_dir.name,
        'plan_file': plan_file,
        'content': content,
        'tasks': tasks
    }


def get_task_status(task: Dict) -> str:
    """Extract task status from task content."""
    if '**Status:**' in task['content']:
        status = task['content'].split('**Status:**')[1].split('\n')[0].strip()
        return status
    return '[ ]'


def execute_task(task: Dict) -> bool:
    """Execute a single task."""
    print(f"\nExecuting: {task['name']}")
    print(f"Status: {get_task_status(task)}")

    # This is a placeholder for task execution
    # In a real implementation, this would:
    # 1. Create execution context
    # 2. Dispatch to worker agent
    # 3. Monitor execution
    # 4. Verify completion

    print(f"  (Task execution placeholder)")
    print(f"  This would execute the task in a real implementation")

    return True


def verify_task(task: Dict) -> bool:
    """Verify task completion."""
    print(f"\nVerifying: {task['name']}")

    # Placeholder for verification
    # Would check:
    # - Files created/modified
    # - Tests passing
    # - Success criteria met

    print(f"  (Task verification placeholder)")
    print(f"  This would verify task completion in a real implementation")

    return True


def update_task_status(plan_file: Path, task_index: int, new_status: str) -> None:
    """Update task status in plan file."""
    content = plan_file.read_text()

    # Find and replace task status
    lines = content.split('\n')
    task_count = 0

    for i, line in enumerate(lines):
        if line.strip().startswith('### Task'):
            if task_count == task_index:
                # Update status in this task
                for j in range(i, min(i+20, len(lines))):
                    if '**Status:**' in lines[j]:
                        lines[j] = f"**Status:** {new_status}"
                        break
                break
            task_count += 1

    plan_file.write_text('\n'.join(lines))


def run_phase(plan_dir: str, phase_num: str) -> bool:
    """Run a single phase."""
    print(f"\n{'='*60}")
    print(f"Running Phase: {phase_num}")
    print(f"{'='*60}\n")

    plan_path = Path(plan_dir)
    phases_dir = plan_path / "phases"

    if not phases_dir.exists():
        print(f"✗ Phases directory not found: {phases_dir}")
        return False

    # Find phase directory
    phase_dir = None
    for dir_path in phases_dir.iterdir():
        if dir_path.is_dir() and dir_path.name.startswith(f"{phase_num}-"):
            phase_dir = dir_path
            break

    if not phase_dir:
        print(f"✗ Phase directory not found: {phase_num}-*")
        return False

    print(f"Found phase: {phase_dir.name}\n")

    try:
        # Load phase plan
        phase_plan = load_phase_plan(phase_dir)

        print(f"Phase: {phase_plan['name']}")
        print(f"Tasks: {len(phase_plan['tasks'])}\n")

        # Execute tasks
        for i, task in enumerate(phase_plan['tasks']):
            status = get_task_status(task)

            if status == '[x]':
                print(f"\n{'-'*60}")
                print(f"Skipping completed task: {task['name']}")
                print(f"{'-'*60}\n")
                continue

            print(f"{'='*60}")
            print(f"Task {i+1}/{len(phase_plan['tasks'])}")
            print(f"{'='*60}")

            # Execute task
            if not execute_task(task):
                print(f"\n✗ Task execution failed: {task['name']}")
                return False

            # Verify task
            if not verify_task(task):
                print(f"\n✗ Task verification failed: {task['name']}")
                return False

            # Update status
            update_task_status(phase_plan['plan_file'], i, '[x]')
            print(f"\n✅ Task completed: {task['name']}")

        print(f"\n{'='*60}")
        print(f"✅ Phase completed: {phase_num}")
        print(f"{'='*60}\n")

        return True

    except Exception as e:
        print(f"\n✗ Error running phase: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: run-phase.py <plan-directory> <phase-number>")
        print("\nExample:")
        print("  python run-phase.py .cattoolkit/plan/my-project 01")
        sys.exit(1)

    plan_dir = sys.argv[1]
    phase_num = sys.argv[2]

    valid = run_phase(plan_dir, phase_num)

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
