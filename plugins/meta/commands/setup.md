---
description: |
  [Deployment] Initialize and deploy toolkit components (hooks, scripts, configurations) to the project. Use this to set up guard hooks, copy scripts to .cattoolkit/hooks/, and generate absolute path configurations.
  <example>
  Context: User wants to deploy guard hooks for a Python project
  user: "Setup guard hooks for type checking"
  assistant: "I'll deploy the guard hooks to .cattoolkit/hooks/ with absolute paths, eliminating the need for CLAUDE_PLUGIN_ROOT."
  </example>
  <example>
  Context: Initialize hooks for TypeScript project
  user: "Setup guard hooks"
  assistant: "I'll copy the TypeScript guard hooks to .cattoolkit/hooks/scripts/ and generate the configuration with absolute paths."
  </example>
  <example>
  Context: Re-deploy with updated paths
  user: "Setup hooks again"
  assistant: "I'll re-deploy hooks to .cattoolkit/hooks/ with current absolute paths."
  </example>
allowed-tools: Task, Read, Glob, Bash, Write
argument-hint: [component] [plugin]
disable-model-invocation: true
---

# Component Deployment

## Analysis

Interpret arguments:
- Component: $1 (hooks | scripts | config)
- Plugin: $2 (guard-python | guard-ts)

Defaults:
- Component: `hooks` (if not specified)
- Plugin: Auto-detect based on project files (Python = guard-python, TypeScript = guard-ts)

## Context Gathering

Locate the source plugin directory:
- If component is `hooks` and plugin is specified, prepare to deploy from that plugin
- If plugin is `guard-python`, prepare Python hooks and scripts
- If plugin is `guard-ts`, prepare TypeScript hooks and scripts
- Auto-detect by checking for Python files (.py) or TypeScript files (.ts)

## 3. The Envelope (Triangle Phase)

Launch the `plugin-expert` subagent with the following flat semantic structure:

<assignment>
Deploy component '$1' from plugin '$2' to .cattoolkit/hooks/ with absolute paths.
</assignment>

<context>
You MUST:
1. Create .cattoolkit/hooks/ directory if it doesn't exist
2. Copy hook scripts from plugin source to .cattoolkit/hooks/scripts/
3. Generate hooks.json with ABSOLUTE PATHS pointing to .cattoolkit/hooks/scripts/
4. DO NOT use ${CLAUDE_PLUGIN_ROOT} - use absolute paths only
5. Ensure scripts are executable (chmod +x)
6. Test that hooks can be invoked with absolute paths
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
