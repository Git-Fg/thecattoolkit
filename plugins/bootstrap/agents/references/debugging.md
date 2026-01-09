# Debugging Protocols

This document provides debugging protocols for the plugin-expert agent.

## Verifying Guard Hooks

**When verifying guard hooks:**

1. **Detect Plugin Type:**
   - From command context or plugin source directory
   - `guard-python` → Python hooks
   - `guard-ts` → TypeScript hooks

2. **Verify Configuration:**
   - Check `hooks.json` exists in plugin directory
   - Confirm paths use `${CLAUDE_PLUGIN_ROOT}`
   - Confirm no hardcoded absolute paths to other users' machines

3. **Validate:**
   - Run `hook-tester.py validate` on the plugin's `hooks.json`

## Debug Hooks Capability

When debugging hook failures, focus on systematic validation of the hook system components:

### Validate Hook Configuration
Locate and verify the hooks.json configuration file exists in the correct location (.claude/hooks/hooks.json). Validate the JSON structure is well-formed and matches the expected schema for the hook events being used.

### Verify Hook Script Readiness
Ensure all referenced hook scripts are present in the .cattoolkit/hooks/scripts/ directory and have proper execute permissions. Check that scripts can be invoked without permission errors.

### Test Hook Functionality
Validate hook scripts by testing them with appropriate JSON payloads matching their expected event types. Verify that each script outputs valid JSON responses conforming to Claude Code's requirements:
- Blocking hooks (PreToolUse, Stop) must return approve, block with reason, or approve with updatedInput
- Observer hooks (PostToolUse, SessionStart) must return success with optional systemMessage

### Diagnose Common Issues
Identify and resolve common failure patterns:
- Missing execute permissions on scripts
- Syntax errors or import failures in hook scripts
- Invalid JSON input or output formatting
- Timeout issues from long-running scripts
- File path resolution problems
- Missing dependencies in hook environments
- Mismatched event type handlers

### Validate Security and Compliance
Ensure hooks implement appropriate security patterns including path validation, error handling, and proper checking of flags like stop_hook_active for stop events.

### Run Comprehensive Testing
Execute full validation using the hook testing tools to verify the complete hook suite functions correctly across all configured events.
