#!/usr/bin/env python3
"""
Hook Tester - Validate Hook Configuration and Scripts

USAGE:
    python3 hook-tester.py validate <hooks.json>
    python3 hook-tester.py test <hooks.json>
    python3 hook-tester.py security-check <hooks.json>
    python3 hook-tester.py debug <hooks.json>
    python3 hook-tester.py permissions <hooks.json>
    python3 hook-tester.py json-check <hooks.json>
    python3 hook-tester.py quick-diag <hooks.json>

FEATURES:
    - Validate hooks.json structure
    - Test all hook scripts with sample data
    - Check security patterns
    - Verify execute permissions
    - Validate JSON output structure
    - Comprehensive diagnostics
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
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        return False, [f"File not found: {config_path}"]
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    # Check required fields
    if "description" not in config:
        errors.append("Missing 'description' field")

    if "hooks" not in config:
        errors.append("Missing 'hooks' field")

    # Validate hooks structure
    valid_events = {
        "PreToolUse",
        "PostToolUse",
        "UserPromptSubmit",
        "PermissionRequest",
        "Stop",
        "SubagentStart",
        "SubagentStop",
        "SessionStart",
        "SessionEnd",
        "PreCompact",
        "Notification",
    }

    for event, hook_list in config.get("hooks", {}).items():
        if event not in valid_events:
            errors.append(f"Invalid event type: {event}")

        if not isinstance(hook_list, list):
            errors.append(f"Hooks for {event} must be a list")

        # Events that don't require matchers
        no_matcher_events = {
            "UserPromptSubmit",
            "PermissionRequest",
            "Stop",
            "SubagentStart",
            "SubagentStop",
            "SessionStart",
            "SessionEnd",
            "PreCompact",
            "Notification",
        }

        for hook_config in hook_list:
            # Matcher is optional for certain events
            if event not in no_matcher_events and "matcher" not in hook_config:
                errors.append(f"Missing 'matcher' in {event} hook")
            if "hooks" not in hook_config:
                errors.append(f"Missing 'hooks' in {event} hook")

            for hook in hook_config.get("hooks", []):
                if "type" not in hook:
                    errors.append(f"Missing 'type' in {event} hook")
                hook_type = hook.get("type")
                if hook_type not in ("command", "prompt"):
                    errors.append(
                        f"Invalid type: {hook_type} (must be 'command' or 'prompt')"
                    )
                if hook_type == "command" and "command" not in hook:
                    errors.append(
                        f"Missing 'command' in {event} hook (command type requires 'command' field)"
                    )
                if hook_type == "prompt" and "prompt" not in hook:
                    errors.append(
                        f"Missing 'prompt' in {event} hook (prompt type requires 'prompt' field)"
                    )

                # Check timeout
                timeout = hook.get("timeout")
                if timeout is not None:
                    if not isinstance(timeout, int) or timeout <= 0:
                        errors.append(f"Invalid timeout in {event}: {timeout}")

                # Check command path (only for command type hooks)
                if hook_type == "command":
                    command = hook.get("command", "")
                    if command:
                        # Extract script path from command
                        script_path = command.split()[-1] if " " in command else command
                        script_path = script_path.strip("\"'")
                        script_path = script_path.replace("${CLAUDE_PLUGIN_ROOT}", ".")
                        script_path = script_path.replace("${CLAUDE_PROJECT_DIR}", ".")

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
        with open(script_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        return False, [f"Script not found: {script_path}"]

    # Check for path validation
    if "validate_path" not in content:
        warnings.append(f"No path validation found in {script_path}")

    # Check for error handling
    if "try:" not in content or "except" not in content:
        warnings.append(f"No error handling found in {script_path}")

    # Check for stop_hook_active (only for Stop hooks)
    if "stop_hook_active" in script_path.lower() or "Stop" in script_path:
        if "stop_hook_active" not in content:
            warnings.append(f"Stop hook missing stop_hook_active check: {script_path}")

    # Check for hardcoded paths
    if script_path.endswith(".py"):
        # Allow common patterns but flag suspicious ones
        if "/tmp/" in content and "base_dir" not in content:
            warnings.append(f"Potential hardcoded /tmp/ path in {script_path}")
        if "../../../" in content:
            warnings.append(f"Path traversal pattern detected in {script_path}")

    return len(warnings) == 0, warnings


def test_hook_script(
    script_path: str, test_input: str = None, verbose: bool = False
) -> Tuple[bool, str]:
    """
    Test hook script with sample input.

    WHY: Ensures script runs without errors before deployment.

    Returns:
        (success: bool, output: str)
    """
    try:
        if test_input is None:
            test_input = json.dumps(
                {
                    "tool_name": "Edit",
                    "tool_input": {"file_path": "test.py"},
                    "stop_hook_active": False,
                }
            )

        if verbose:
            print(f"  Testing: {script_path}")
            print(f"  Input: {test_input}")

        result = subprocess.run(
            ["python3", script_path],
            input=test_input,
            text=True,
            capture_output=True,
            timeout=5,
        )

        output = result.stdout + result.stderr

        if verbose:
            print(f"  Exit code: {result.returncode}")
            print(
                f"  Output: {output[:200]}..."
                if len(output) > 200
                else f"  Output: {output}"
            )

        # Check for unhandled exceptions
        if result.returncode != 0 and "SystemExit" not in output:
            return False, f"Script failed with code {result.returncode}: {output}"

        return True, output

    except subprocess.TimeoutExpired:
        return False, "Script timed out (>5s)"
    except Exception as e:
        return False, f"Error running script: {e}"


def check_permissions(script_path: str) -> Tuple[bool, List[str]]:
    """
    Check if script has execute permissions.

    WHY: Scripts must be executable to run as hooks.

    Returns:
        (success: bool, warnings: List[str])
    """
    warnings = []

    if not os.path.exists(script_path):
        return False, [f"Script not found: {script_path}"]

    if not os.path.isfile(script_path):
        return False, [f"Path is not a file: {script_path}"]

    # Check if file is executable by owner
    if not os.access(script_path, os.X_OK):
        warnings.append(f"Script not executable: {script_path}")
        return False, warnings

    return True, warnings


def validate_json_output(output: str) -> Tuple[bool, List[str]]:
    """
    Validate that hook output is valid JSON with correct structure.

    WHY: Claude Code requires specific JSON output format.

    Returns:
        (success: bool, errors: List[str])
    """
    errors = []

    try:
        # Try to parse as JSON
        data = json.loads(output)

        # Check for required fields based on expected structure
        if not isinstance(data, dict):
            errors.append("Output must be a JSON object")
            return False, errors

        # Validate blocking hook structure (approximate)
        if "status" not in data:
            errors.append("Missing 'status' field")
        else:
            status = data.get("status")
            valid_statuses = ["approve", "block", "success"]
            if status not in valid_statuses:
                errors.append(
                    f"Invalid status '{status}'. Must be one of: {valid_statuses}"
                )

        # If blocking, check for required fields
        if data.get("status") in ["block", "approve"]:
            if "updatedInput" in data:
                # updatedInput is valid but optional
                pass
            elif "block" in data.get("status", ""):
                # Block should have reason and message
                if "reason" not in data:
                    errors.append("Block status should include 'reason' field")
                if "message" not in data:
                    errors.append("Block status should include 'message' field")

        return len(errors) == 0, errors

    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON output: {e}")
        errors.append(f"Raw output: {output[:200]}")
        return False, errors
    except Exception as e:
        errors.append(f"Error validating JSON: {e}")
        return False, errors


def extract_script_path(command: str) -> str:
    """
    Extract script path from command string.

    WHY: Commands may include environment variables or full paths.

    Returns:
        script_path: Cleaned script path
    """
    # Extract script path from command
    # Handle: "python3 ${CLAUDE_PLUGIN_ROOT}/.claude/hooks/scripts/hook.py"
    script_path = command.split()[-1] if " " in command else command

    # Replace environment variables with current directory for testing
    script_path = script_path.replace("${CLAUDE_PLUGIN_ROOT}", ".")
    script_path = script_path.replace("${CLAUDE_PROJECT_DIR}", ".")

    return script_path


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("Hook Tester - Comprehensive Hook Validation and Testing")
        print("\nUsage:")
        print(
            "  python3 hook-tester.py validate <hooks.json>       - Validate hooks.json structure"
        )
        print(
            "  python3 hook-tester.py test <hooks.json>           - Test all hook scripts"
        )
        print(
            "  python3 hook-tester.py security-check <hooks.json> - Check security patterns"
        )
        print(
            "  python3 hook-tester.py debug <hooks.json>          - Detailed diagnostic output"
        )
        print(
            "  python3 hook-tester.py permissions <hooks.json>    - Check execute permissions"
        )
        print(
            "  python3 hook-tester.py json-check <hooks.json>      - Validate JSON output structure"
        )
        print(
            "  python3 hook-tester.py quick-diag <hooks.json>     - Run all checks at once"
        )
        print("\nExamples:")
        print("  python3 hook-tester.py quick-diag .claude/hooks/hooks.json")
        print("  python3 hook-tester.py debug .claude/hooks/hooks.json")
        sys.exit(1)

    command = sys.argv[1].lower()

    if len(sys.argv) < 3:
        print("Error: Please provide hooks.json file path")
        sys.exit(1)

    config_path = sys.argv[2]

    # Load config for commands that need it
    config = None
    if command in [
        "validate",
        "test",
        "security-check",
        "debug",
        "permissions",
        "json-check",
        "quick-diag",
    ]:
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            print(f"Error: Config file not found: {config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in config file: {e}")
            sys.exit(1)

    if command == "validate":
        success, errors = validate_hooks_json(config_path)

        if success:
            print(f"✓ Configuration valid: {config_path}")
            sys.exit(0)
        else:
            print(f"✗ Configuration invalid: {config_path}")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)

    elif command == "test":
        # Extract and test all scripts
        scripts_tested = 0
        scripts_passed = 0

        print(f"Testing hook scripts from: {config_path}\n")

        for event, hook_list in config.get("hooks", {}).items():
            print(f"Event: {event}")
            for hook_config in hook_list:
                for hook in hook_config.get("hooks", []):
                    hook_type = hook.get("type")
                    # Only test command type hooks (prompt hooks don't have scripts)
                    if hook_type == "command":
                        command = hook.get("command", "")
                        if "python3" in command:
                            script_path = extract_script_path(command)

                            scripts_tested += 1
                            success, output = test_hook_script(script_path)

                            if success:
                                print(f"  ✓ {script_path}")
                                scripts_passed += 1
                            else:
                                print(f"  ✗ {script_path}")
                                print(f"    {output}")

        print(f"\nResults: {scripts_passed}/{scripts_tested} scripts passed")
        sys.exit(0 if scripts_passed == scripts_tested else 1)

    elif command == "security-check":
        print(f"Security check for: {config_path}\n")

        for event, hook_list in config.get("hooks", {}).items():
            print(f"Event: {event}")
            for hook_config in hook_list:
                for hook in hook_config.get("hooks", []):
                    hook_type = hook.get("type")
                    # Only check security for command type hooks
                    if hook_type == "command":
                        command = hook.get("command", "")
                        if "python3" in command:
                            script_path = extract_script_path(command)

                            success, warnings = check_security_patterns(script_path)

                            if warnings:
                                print(f"  ⚠ {script_path}:")
                                for warning in warnings:
                                    print(f"    - {warning}")
                            else:
                                print(f"  ✓ {script_path} - Security checks passed")

    elif command == "debug":
        print(f"=== DEBUG MODE: {config_path} ===\n")

        # 1. Validate config
        print("1. Validating configuration...")
        success, errors = validate_hooks_json(config_path)
        if success:
            print("   ✓ Configuration valid\n")
        else:
            print("   ✗ Configuration has errors:")
            for error in errors:
                print(f"     - {error}\n")

        # 2. Check permissions
        print("2. Checking permissions...")
        for event, hook_list in config.get("hooks", {}).items():
            for hook_config in hook_list:
                for hook in hook_config.get("hooks", []):
                    if hook.get("type") == "command":
                        script_path = extract_script_path(hook.get("command", ""))
                        perm_ok, perm_warnings = check_permissions(script_path)
                        if perm_ok:
                            print(f"   ✓ {script_path} - Executable")
                        else:
                            print(f"   ✗ {script_path} - Issues:")
                            for warning in perm_warnings:
                                print(f"     - {warning}")
        print()

        # 3. Test each hook with verbose output
        print("3. Testing individual hooks...\n")
        for event, hook_list in config.get("hooks", {}).items():
            print(f"Event: {event}")
            for hook_config in hook_list:
                for hook in hook_config.get("hooks", []):
                    if hook.get("type") == "command":
                        script_path = extract_script_path(hook.get("command", ""))

                        # Test with appropriate sample data
                        if event == "Stop":
                            test_input = json.dumps({"stop_hook_active": False})
                        elif event in ["PreToolUse", "PostToolUse"]:
                            test_input = json.dumps(
                                {"tool": "Edit", "arguments": {"file_path": "test.txt"}}
                            )
                        else:
                            test_input = json.dumps({})

                        success, output = test_hook_script(
                            script_path, test_input, verbose=True
                        )

                        if success:
                            print(f"     ✓ Script executed")
                            # Validate JSON output
                            json_ok, json_errors = validate_json_output(output)
                            if json_ok:
                                print(f"     ✓ Valid JSON output")
                            else:
                                print(f"     ✗ Invalid JSON output:")
                                for error in json_errors:
                                    print(f"       - {error}")
                        else:
                            print(f"     ✗ Script failed: {output}")
            print()

    elif command == "permissions":
        print(f"Checking permissions for: {config_path}\n")

        for event, hook_list in config.get("hooks", {}).items():
            print(f"Event: {event}")
            for hook_config in hook_list:
                for hook in hook_config.get("hooks", []):
                    if hook.get("type") == "command":
                        script_path = extract_script_path(hook.get("command", ""))
                        perm_ok, warnings = check_permissions(script_path)

                        if perm_ok:
                            print(f"  ✓ {script_path}")
                            # Show permissions
                            perms = oct(os.stat(script_path).st_mode)[-3:]
                            print(f"    Permissions: {perms}")
                        else:
                            print(f"  ✗ {script_path}")
                            for warning in warnings:
                                print(f"    - {warning}")
                            print(f"    Fix: chmod +x {script_path}")
            print()

    elif command == "json-check":
        print(f"Validating JSON output for: {config_path}\n")

        for event, hook_list in config.get("hooks", {}).items():
            print(f"Event: {event}")
            for hook_config in hook_list:
                for hook in hook_config.get("hooks", []):
                    if hook.get("type") == "command":
                        script_path = extract_script_path(hook.get("command", ""))

                        # Generate test input based on event type
                        if event == "Stop":
                            test_input = json.dumps({"stop_hook_active": False})
                        elif event in ["PreToolUse", "PostToolUse"]:
                            test_input = json.dumps(
                                {"tool": "Edit", "arguments": {"file_path": "test.txt"}}
                            )
                        else:
                            test_input = json.dumps({})

                        success, output = test_hook_script(script_path, test_input)

                        if success:
                            json_ok, json_errors = validate_json_output(output)
                            if json_ok:
                                print(f"  ✓ {script_path} - Valid JSON structure")
                            else:
                                print(f"  ✗ {script_path} - Invalid JSON:")
                                for error in json_errors:
                                    print(f"    - {error}")
                        else:
                            print(
                                f"  ✗ {script_path} - Script failed (can't validate JSON)"
                            )
            print()

    elif command == "quick-diag":
        print(f"=== QUICK DIAGNOSTIC: {config_path} ===\n")

        # 1. Validate config
        print("1. Configuration validation...")
        success, errors = validate_hooks_json(config_path)
        if success:
            print("   ✓ Valid")
        else:
            print("   ✗ Invalid:")
            for error in errors[:3]:  # Show first 3 errors
                print(f"     - {error}")
        print()

        # 2. Check permissions
        print("2. Permission check...")
        perm_issues = 0
        for event, hook_list in config.get("hooks", {}).items():
            for hook_config in hook_list:
                for hook in hook_config.get("hooks", []):
                    if hook.get("type") == "command":
                        script_path = extract_script_path(hook.get("command", ""))
                        perm_ok, warnings = check_permissions(script_path)
                        if not perm_ok:
                            perm_issues += 1

        if perm_issues == 0:
            print("   ✓ All scripts executable")
        else:
            print(f"   ✗ {perm_issues} script(s) not executable")
        print()

        # 3. Test execution
        print("3. Execution test...")
        scripts_tested = 0
        scripts_passed = 0
        json_issues = 0

        for event, hook_list in config.get("hooks", {}).items():
            for hook_config in hook_list:
                for hook in hook_config.get("hooks", []):
                    if hook.get("type") == "command":
                        script_path = extract_script_path(hook.get("command", ""))

                        # Generate test input
                        if event == "Stop":
                            test_input = json.dumps({"stop_hook_active": False})
                        elif event in ["PreToolUse", "PostToolUse"]:
                            test_input = json.dumps(
                                {"tool": "Edit", "arguments": {"file_path": "test.txt"}}
                            )
                        else:
                            test_input = json.dumps({})

                        scripts_tested += 1
                        success, output = test_hook_script(script_path, test_input)

                        if success:
                            scripts_passed += 1
                            # Check JSON
                            json_ok, _ = validate_json_output(output)
                            if not json_ok:
                                json_issues += 1
                        else:
                            pass  # Already counted

        print(f"   Scripts tested: {scripts_tested}")
        print(f"   Scripts passed: {scripts_passed}")
        print(f"   JSON issues: {json_issues}")
        print()

        # 4. Security check
        print("4. Security check...")
        security_issues = 0
        for event, hook_list in config.get("hooks", {}).items():
            for hook_config in hook_list:
                for hook in hook_config.get("hooks", []):
                    if hook.get("type") == "command":
                        script_path = extract_script_path(hook.get("command", ""))
                        success, warnings = check_security_patterns(script_path)
                        if warnings:
                            security_issues += len(warnings)

        if security_issues == 0:
            print("   ✓ No security issues detected")
        else:
            print(f"   ⚠ {security_issues} security warning(s) detected")
        print()

        # Summary
        print("=== SUMMARY ===")
        if (
            success
            and perm_issues == 0
            and scripts_passed == scripts_tested
            and json_issues == 0
            and security_issues == 0
        ):
            print("✓ All checks passed!")
        else:
            print("✗ Issues detected:")
            if not success:
                print("  - Configuration errors")
            if perm_issues > 0:
                print("  - Permission issues")
            if scripts_passed != scripts_tested:
                print("  - Execution failures")
            if json_issues > 0:
                print("  - JSON validation issues")
            if security_issues > 0:
                print("  - Security warnings")

    else:
        print(f"Unknown command: {command}")
        print(
            f"Available commands: validate, test, security-check, debug, permissions, json-check, quick-diag"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
