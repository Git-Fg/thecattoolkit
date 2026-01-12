---
name: create-hooks
description: "Expert guidance for creating, configuring, and using Claude Code hooks. MUST Use when setting up event listeners, validating commands, automating workflows, or implementing hook-based automation."
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

## Success Criteria

A working hook configuration has:
- [ ] Valid JSON in `.claude/hooks.json`
- [ ] Appropriate hook event selected
- [ ] Correct matcher pattern
- [ ] Tested with `--debug`
- [ ] No infinite loops
- [ ] Reasonable timeouts
