#!/usr/bin/env python3
"""
Hook Tester - Validate Hook Configuration and Scripts

USAGE:
    python3 hook-tester.py validate
    python3 hook-tester.py test hooks.json
    python3 hook-tester.py security-check hooks.json
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def validate_hooks_json(config_path: str) -> Tuple[bool, List[str]]:
    """
    Validate hooks.json configuration file.

    WHY: Catches configuration errors before they cause runtime issues.

    Returns:
        (success: bool, errors: List[str])
    """
    errors = []

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        return False, [f"File not found: {config_path}"]
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    # Check required fields
    if 'description' not in config:
        errors.append("Missing 'description' field")

    if 'hooks' not in config:
        errors.append("Missing 'hooks' field")

    # Validate hooks structure
    valid_events = {
        'PreToolUse', 'PostToolUse', 'UserPromptSubmit',
        'PermissionRequest', 'Stop', 'SubagentStart',
        'SubagentStop', 'SessionStart', 'SessionEnd',
        'PreCompact', 'Notification'
    }

    for event, hook_list in config.get('hooks', {}).items():
        if event not in valid_events:
            errors.append(f"Invalid event type: {event}")

        if not isinstance(hook_list, list):
            errors.append(f"Hooks for {event} must be a list")

        # Events that don't require matchers
        no_matcher_events = {
            'UserPromptSubmit', 'PermissionRequest', 'Stop',
            'SubagentStart', 'SubagentStop', 'SessionStart',
            'SessionEnd', 'PreCompact', 'Notification'
        }

        for hook_config in hook_list:
            # Matcher is optional for certain events
            if event not in no_matcher_events and 'matcher' not in hook_config:
                errors.append(f"Missing 'matcher' in {event} hook")
            if 'hooks' not in hook_config:
                errors.append(f"Missing 'hooks' in {event} hook")

            for hook in hook_config.get('hooks', []):
                if 'type' not in hook:
                    errors.append(f"Missing 'type' in {event} hook")
                hook_type = hook.get('type')
                if hook_type not in ('command', 'prompt'):
                    errors.append(f"Invalid type: {hook_type} (must be 'command' or 'prompt')")
                if hook_type == 'command' and 'command' not in hook:
                    errors.append(f"Missing 'command' in {event} hook (command type requires 'command' field)")
                if hook_type == 'prompt' and 'prompt' not in hook:
                    errors.append(f"Missing 'prompt' in {event} hook (prompt type requires 'prompt' field)")

                # Check timeout
                timeout = hook.get('timeout')
                if timeout is not None:
                    if not isinstance(timeout, int) or timeout <= 0:
                        errors.append(f"Invalid timeout in {event}: {timeout}")

                # Check command path (only for command type hooks)
                if hook_type == 'command':
                    command = hook.get('command', '')
                    if command:
                        # Extract script path from command
                        script_path = command.split()[-1] if ' ' in command else command
                        script_path = script_path.replace('${CLAUDE_PLUGIN_ROOT}', '.')
                        script_path = script_path.replace('${CLAUDE_PROJECT_DIR}', '.')

                        if not Path(script_path).exists():
                            errors.append(f"Script not found: {script_path}")

    return len(errors) == 0, errors


def check_security_patterns(script_path: str) -> Tuple[bool, List[str]]:
    """
    Check if hook script follows security best practices.

    WHY: Automated security checks catch common vulnerabilities.

    Returns:
        (success: bool, warnings: List[str])
    """
    warnings = []

    try:
        with open(script_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return False, [f"Script not found: {script_path}"]

    # Check for path validation
    if 'validate_path' not in content:
        warnings.append(f"No path validation found in {script_path}")

    # Check for error handling
    if 'try:' not in content or 'except' not in content:
        warnings.append(f"No error handling found in {script_path}")

    # Check for stop_hook_active (only for Stop hooks)
    if 'stop_hook_active' in script_path.lower() or 'Stop' in script_path:
        if 'stop_hook_active' not in content:
            warnings.append(f"Stop hook missing stop_hook_active check: {script_path}")

    # Check for hardcoded paths
    if script_path.endswith('.py'):
        # Allow common patterns but flag suspicious ones
        if '/tmp/' in content and 'base_dir' not in content:
            warnings.append(f"Potential hardcoded /tmp/ path in {script_path}")
        if '../../../' in content:
            warnings.append(f"Path traversal pattern detected in {script_path}")

    return len(warnings) == 0, warnings


def test_hook_script(script_path: str, test_input: str = None) -> Tuple[bool, str]:
    """
    Test hook script with sample input.

    WHY: Ensures script runs without errors before deployment.

    Returns:
        (success: bool, output: str)
    """
    try:
        if test_input is None:
            test_input = json.dumps({
                "tool_name": "Edit",
                "tool_input": {"file_path": "test.py"},
                "stop_hook_active": False
            })

        result = subprocess.run(
            ['python3', script_path],
            input=test_input,
            text=True,
            capture_output=True,
            timeout=5
        )

        output = result.stdout + result.stderr

        # Check for unhandled exceptions
        if result.returncode != 0 and 'SystemExit' not in output:
            return False, f"Script failed with code {result.returncode}: {output}"

        return True, output

    except subprocess.TimeoutExpired:
        return False, "Script timed out (>5s)"
    except Exception as e:
        return False, f"Error running script: {e}"


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 hook-tester.py validate <config.json>")
        print("  python3 hook-tester.py test <config.json>")
        print("  python3 hook-tester.py security-check <config.json>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'validate':
        if len(sys.argv) < 3:
            print("Error: Please provide config file path")
            sys.exit(1)

        config_path = sys.argv[2]
        success, errors = validate_hooks_json(config_path)

        if success:
            print(f"✓ Configuration valid: {config_path}")
            sys.exit(0)
        else:
            print(f"✗ Configuration invalid: {config_path}")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)

    elif command == 'test':
        if len(sys.argv) < 3:
            print("Error: Please provide config file path")
            sys.exit(1)

        config_path = sys.argv[2]

        # Load config
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

        # Extract and test all scripts
        scripts_tested = 0
        scripts_passed = 0

        for event, hook_list in config.get('hooks', {}).items():
            for hook_config in hook_list:
                for hook in hook_config.get('hooks', []):
                    hook_type = hook.get('type')
                    # Only test command type hooks (prompt hooks don't have scripts)
                    if hook_type == 'command':
                        command = hook.get('command', '')
                        if 'python3' in command:
                            script_path = command.split()[-1]
                            script_path = script_path.replace('${CLAUDE_PLUGIN_ROOT}', '.')
                            script_path = script_path.replace('${CLAUDE_PROJECT_DIR}', '.')

                            scripts_tested += 1
                            success, output = test_hook_script(script_path)

                            if success:
                                print(f"✓ {script_path}")
                                scripts_passed += 1
                            else:
                                print(f"✗ {script_path}")
                                print(f"  {output}")

        print(f"\nResults: {scripts_passed}/{scripts_tested} scripts passed")

    elif command == 'security-check':
        if len(sys.argv) < 3:
            print("Error: Please provide config file path")
            sys.exit(1)

        config_path = sys.argv[2]

        # Load config
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

        # Check security for all scripts
        for event, hook_list in config.get('hooks', {}).items():
            for hook_config in hook_list:
                for hook in hook_config.get('hooks', []):
                    hook_type = hook.get('type')
                    # Only check security for command type hooks
                    if hook_type == 'command':
                        command = hook.get('command', '')
                        if 'python3' in command:
                            script_path = command.split()[-1]
                            script_path = script_path.replace('${CLAUDE_PLUGIN_ROOT}', '.')
                            script_path = script_path.replace('${CLAUDE_PROJECT_DIR}', '.')

                            success, warnings = check_security_patterns(script_path)

                            if warnings:
                                print(f"\n{script_path}:")
                                for warning in warnings:
                                    print(f"  ⚠ {warning}")
                            else:
                                print(f"✓ {script_path} - Security checks passed")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
