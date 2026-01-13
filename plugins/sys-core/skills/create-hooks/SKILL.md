---
name: create-hooks
description: "Expert guidance for creating, configuring, and using Claude Code hooks. MUST Use when setting up event listeners, validating commands, automating workflows, or implementing hook-based automation. Do not use for skill creation, command development, or plugin configuration."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash(mkdir:-p), Bash(ls:*), Bash(cat:*), Bash(jq:*)]
---

# Create Hooks: Automation Authority

## Objective

Hooks are event-driven automation for Claude Code that execute shell commands or LLM prompts in response to tool usage, session events, and user interactions. This skill teaches you how to create, configure, and debug hooks for validating commands, automating workflows, injecting context, and implementing custom completion criteria.

> **Core Concept:** Hooks provide programmatic control over Claude's behavior without modifying core code, enabling project-specific automation, safety checks, and workflow customization.

## Quick Start Algorithm

1. **IDENTIFY** → Choose event (When?) and action (What?)
2. **CONFIGURE** → Create `.claude/hooks.json` entry
3. **TEST** → Run with `claude --debug`
4. **REFINE** → Optimize matchers and timeouts

**Creation Workflow:** See [references/examples.md](references/examples.md) for step-by-step hook creation examples.

## Capability Index & References

### 1. Concepts & Architecture
- **Hook Types & Events**: [references/hook-types.md](references/hook-types.md) (PreToolUse, PostToolUse, Stop, etc.)
- **Command vs Prompt**: [references/command-vs-prompt.md](references/command-vs-prompt.md) (Decision guide)
- **Input/Output Schemas**: [references/input-output-schemas.md](references/input-output-schemas.md) (JSON formats)
- **Environment Variables**: [references/environment-variables.md](references/environment-variables.md) (Available vars)

### 2. Configuration
- **Matchers & Patterns**: [references/matchers.md](references/matchers.md) (Regex, tool filtering)
- **Examples**: [references/examples.md](references/examples.md) (Common use cases)

### 3. Debugging & Issues
- **Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md) (Common errors)

## Validation (Security Checklist)

Before enabling hooks, verify:

- **Infinite Loops**: Check `stop_hook_active` in Stop hooks.
- **Timeouts**: Ensure `timeout` is set (default 60s).
- **Permissions**: Scripts must be executable (`chmod +x`).
- **Paths**: Use `$CLAUDE_PROJECT_DIR` for safety.
- **Validity**: Check JSON syntax with `jq`.

**Command:**
```bash
jq . .claude/hooks.json
```

## Practical Hook Examples

### 1. "Do More" Prompt (Keep Claude Running)

**Use Case:** Auto-continue tasks after Claude finishes

**Hook Type:** `Stop` - Runs after Claude responds

**Implementation:**
```json
{
  "hooks": {
    "Stop": {
      "if": "${stop_hook_active} == false",
      "timeout": 30,
      "command": "echo 'Continue with the next logical step of the current task. What should be done next?'"
    }
  }
}
```

**Why It Works:**
- Keeps Claude running for extended tasks
- Automatically prompts for next steps
- Prevents idle time between completions

### 2. Notification Sound (Completion Alert)

**Use Case:** Audio notification when Claude finishes

**Hook Type:** `Stop` - Audio alert on completion

**Implementation:**
```bash
#!/bin/bash
# notify.sh
afplay /System/Library/Sounds/Ping.aiff
```

**hooks.json:**
```json
{
  "hooks": {
    "Stop": {
      "timeout": 10,
      "command": "notify.sh"
    }
  }
}
```

**Use Cases:**
- Long-running tasks (debugging, builds)
- Background monitoring
- Task completion alerts

### 3. Pre-Execution Validation

**Use Case:** Validate commands before execution

**Hook Type:** `PreToolUse` - Check commands before running

**Implementation:**
```json
{
  "hooks": {
    "PreToolUse": {
      "if": "${tool_name} == 'Bash' && ${input} =~ /rm -rf/",
      "timeout": 5,
      "command": "echo 'WARNING: Destructive command detected. Confirm with user before proceeding.'"
    }
  }
}
```

### 4. Context Management Hook

**Use Case:** Add reminders during long tasks

**Hook Type:** `UserPromptSubmit` - Inject reminders at intervals

**Implementation:**
```json
{
  "hooks": {
    "UserPromptSubmit": {
      "if": "${message_count} % 10 == 0",
      "timeout": 5,
      "command": "echo 'Reminder: Maintain focus on authentication edge cases.'"
    }
  }
}
```

### 5. Task Tracking Hook

**Use Case:** Auto-update todo list after tool usage

**Hook Type:** `PostToolUse` - Update progress tracking

**Implementation:**
```bash
#!/bin/bash
# track.sh
echo "$(date): ${tool_name} completed" >> .cattoolkit/context/tool-usage.log
```

**hooks.json:**
```json
{
  "hooks": {
    "PostToolUse": {
      "timeout": 3,
      "command": "track.sh"
    }
  }
}
```

## Success Criteria

A working hook configuration has:
- [ ] Valid JSON in `.claude/hooks.json`
- [ ] Appropriate hook event selected
- [ ] Correct matcher pattern
- [ ] Tested with `--debug`
- [ ] No infinite loops
- [ ] Reasonable timeouts
