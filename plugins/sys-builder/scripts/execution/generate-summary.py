#!/usr/bin/env python3
"""
Generate Summary

Generates a phase summary from completed tasks.
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime


def extract_completed_tasks(plan_file: Path) -> list:
    """Extract completed tasks from a phase plan."""
    content = plan_file.read_text()
    completed_tasks = []

    # Split by tasks
    task_sections = re.split(r'### Task \d+:', content)

    for section in task_sections[1:]:  # Skip first split
        lines = section.split('\n')
        task_name = lines[0].strip() if lines else ""

        # Check if task is complete
        if '**Status:** [x]' in section:
            # Extract task details
            task_details = {
                'name': task_name,
                'scope': '',
                'action': '',
                'verify': '',
                'done': ''
            }

            # Extract fields
            for field in ['Scope:', 'Action:', 'Verify:', 'Done:']:
                pattern = rf'{field}(.*?)(?:\n\n|\n### |$)'
                match = re.search(pattern, section, re.DOTALL)
                if match:
                    value = match.group(1).strip()
                    # Remove markdown formatting
                    value = re.sub(r'\*\*(.*?)\*\*', r'\1', value)
                    task_details[field[:-1].lower()] = value

            completed_tasks.append(task_details)

    return completed_tasks


def extract_deliverables(plan_file: Path) -> list:
    """Extract deliverables from phase plan."""
    content = plan_file.read_text()
    deliverables = []

    # Look for deliverable information
    deliverable_section = None
    if '## Overview' in content:
        overview = content.split('## Overview')[1].split('##')[0]
        if 'deliverable' in overview.lower():
            deliverable_section = overview

    # Extract from tasks
    task_sections = re.split(r'### Task \d+:', content)

    for section in task_sections[1:]:
        # Look for deliverable indicators
        if any(word in section.lower() for word in ['create', 'implement', 'build', 'add']):
            # Try to extract deliverable name
            lines = section.split('\n')
            for line in lines[:5]:  # Check first few lines
                if '**Action:**' in line:
                    action = line.split('**Action:**')[1].strip()
                    # Simplify action to get deliverable name
                    deliverable = action.replace('Create', '').replace('Implement', '').replace('Build', '').strip()
                    if deliverable:
                        deliverables.append(deliverable)
                    break

    return deliverables


def generate_summary(plan_file: Path, phase_num: str, phase_name: str) -> str:
    """Generate a phase summary."""
    completed_tasks = extract_completed_tasks(plan_file)
    deliverables = extract_deliverables(plan_file)

    today = datetime.now().strftime('%Y-%m-%d')

    summary = f"""# Phase {phase_num} Summary: {phase_name}

**Date:** {today}
**Status:** ✅ Complete

## Completed Tasks
"""

    for task in completed_tasks:
        summary += f"- [x] {task['name']}\n"

    summary += "\n## Deliverables\n"

    if deliverables:
        for i, deliverable in enumerate(deliverables, 1):
            summary += f"{i}. **{deliverable}**\n"
    else:
        summary += "*(See task list for detailed deliverables)*\n"

    summary += "\n## Key Decisions\n"

    # Look for decisions in tasks
    decisions = []
    for task in completed_tasks:
        if task.get('done'):
            # Extract decision points
            done_text = task['done']
            if 'decision' in done_text.lower() or 'choose' in done_text.lower():
                decisions.append(f"**{task['name']}:** {done_text[:100]}...")

    if decisions:
        for decision in decisions:
            summary += f"- {decision}\n"
    else:
        summary += "- *No significant decisions recorded*\n"

    summary += "\n## Challenges Overcome\n"

    # Look for challenges
    challenges = []
    for task in completed_tasks:
        if task.get('verify'):
            verify_text = task['verify']
            if any(word in verify_text.lower() for word in ['issue', 'problem', 'error', 'challenge']):
                challenges.append(f"**{task['name']}:** Resolved through testing and verification")

    if challenges:
        for challenge in challenges:
            summary += f"- {challenge}\n"
    else:
        summary += "- *No major challenges encountered*\n"

    summary += "\n## Files Modified\n"

    # Look for scope information
    files = set()
    for task in completed_tasks:
        if task.get('scope'):
            scope = task['scope']
            # Simple extraction of file paths
            paths = re.findall(r'[\w/\.-]+\.\w+', scope)
            files.update(paths)

    if files:
        for file_path in sorted(files):
            summary += f"- `{file_path}`\n"
    else:
        summary += "- *Files tracked in task details*\n"

    summary += "\n## Tests/Validation\n"

    # Look for verification information
    tests = []
    for task in completed_tasks:
        if task.get('verify'):
            verify = task['verify']
            if any(word in verify.lower() for word in ['test', 'verify', 'check', 'validate']):
                tests.append(f"**{task['name']}:** {verify[:80]}...")

    if tests:
        for test in tests:
            summary += f"- {test}\n"
    else:
        summary += "- *Tests documented in task details*\n"

    summary += "\n## Next Phase\n"
    next_phase_num = f"{int(phase_num) + 1:02d}"
    summary += f"**Phase {next_phase_num}:** *Ready to start*\n"
    summary += "**Status:** Ready to start\n"

    summary += "\n## Notes\n"
    summary += "*Additional observations and context can be added here*\n"

    return summary


def main():
    """Main entry point."""
    if len(sys.argv) < 4:
        print("Usage: generate-summary.py <plan-directory> <phase-number> <phase-name>")
        print("\nExample:")
        print("  python generate-summary.py .cattoolkit/plan/my-project 01 'Foundation'")
        sys.exit(1)

    plan_dir = sys.argv[1]
    phase_num = sys.argv[2]
    phase_name = sys.argv[3]

    plan_path = Path(plan_dir)
    phases_dir = plan_path / "phases"

    # Find phase directory
    phase_dir = None
    for dir_path in phases_dir.iterdir():
        if dir_path.is_dir() and dir_path.name.startswith(f"{phase_num}-"):
            phase_dir = dir_path
            break

    if not phase_dir:
        print(f"✗ Phase directory not found: {phase_num}-*")
        sys.exit(1)

    # Find plan file
    plan_files = list(phase_dir.glob("*-PLAN.md"))

    if not plan_files:
        print(f"✗ No plan file found in {phase_dir}")
        sys.exit(1)

    # Generate summary
    summary = generate_summary(plan_files[0], phase_num, phase_name)

    # Write summary
    summary_path = phase_dir / "SUMMARY.md"
    summary_path.write_text(summary)

    print(f"\n{'='*60}")
    print(f"✅ Summary generated: {summary_path}")
    print(f"{'='*60}\n")

    print("Summary preview:")
    print("-" * 60)
    print(summary[:500] + "..." if len(summary) > 500 else summary)
    print("-" * 60)


if __name__ == "__main__":
    main()
