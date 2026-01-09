---
description: |
  [Deployment] Deploy Python guard hooks to the project with absolute paths. Copies Python hook scripts to .cattoolkit/hooks/scripts/ and generates hooks.json with absolute paths for reliable operation.
  <example>
  Context: User wants to deploy Python guard hooks
  user: "Setup Python guard hooks"
  assistant: "I'll deploy the guard-python hooks to .cattoolkit/hooks/ with absolute paths, eliminating the need for environment variables."
  </example>
  <example>
  Context: Initialize hooks for Python project
  user: "Setup-py"
  assistant: "I'll copy the Python guard hooks to .cattoolkit/hooks/scripts/ and generate the configuration with absolute paths."
  </example>
  <example>
  Context: Re-deploy with updated paths
  user: "Setup Python guard hooks again"
  assistant: "I'll re-deploy hooks to .cattoolkit/hooks/ with current absolute paths."
  </example>
allowed-tools: Task, Read, Glob, Bash, Write
disable-model-invocation: true
---

# Python Guard Hooks Deployment

## Analysis

Deploy guard-python hooks to the current project.

This command:
- Creates `.cattoolkit/hooks/` directory if it doesn't exist
- Copies Python hook scripts from plugin to project
- Generates hooks.json with ABSOLUTE PATHS (no environment variables)
- Sets execute permissions on all scripts
- Validates deployment

## Context Gathering

Locate the guard-python plugin directory:
- Source: `plugins/guard-python/hooks/scripts/`
- Scripts: `hook_runner.py`, `protect-files.py`, `security-check.py`, `type-check-on-edit.py`

## 3. The Envelope (Triangle Phase)

Launch the `plugin-expert` subagent with the following flat semantic structure:

<assignment>
Deploy guard-python hooks to .cattoolkit/hooks/ with absolute paths.
</assignment>

<context>
You MUST:
1. Create .cattoolkit/hooks/ directory if it doesn't exist
2. Copy hook scripts from plugins/guard-python/hooks/scripts/ to .cattoolkit/hooks/scripts/
3. Generate hooks.json with ABSOLUTE PATHS pointing to .cattoolkit/hooks/scripts/
4. DO NOT use ${CLAUDE_PLUGIN_ROOT} - use absolute paths only
5. Ensure scripts are executable (chmod +x)
6. Test that hooks can be invoked with absolute paths

Source directory: plugins/guard-python/hooks/scripts/
Target directory: .cattoolkit/hooks/scripts/
</context>

<constraints>
- Work in Background/Async mode if possible.
- NO USER INTERACTION. Assume default values if unspecified.
- Persist all results to disk immediately.
- Use absolute paths for all script invocations in hooks.json
- Ensure deployment is idempotent (can run multiple times safely)
</constraints>

## 4. Report Results

Return the agent's findings to the user with clear explanation of:
- What was deployed
- Where scripts are located
- What paths are configured in hooks.json
- How to verify the deployment worked
