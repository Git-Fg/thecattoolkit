---
name: manage-hooks
description: Event-driven automation hooks for Claude Code. Security-hardened templates for PreToolUse, PostToolUse, SessionStart, and other hook events.
allowed-tools: Read Write Edit Bash Grep
---

## Protocol Overview

Hooks are event-driven automation for Claude Code. They execute shell commands or LLM prompts in response to:

- **Tool Events**: Before (PreToolUse) or after (PostToolUse) tool execution
- **Session Events**: SessionStart, SessionEnd, PreCompact
- **User Events**: UserPromptSubmit, PermissionRequest
- **Agent Events**: Stop, SubagentStart, SubagentStop
- **System Events**: Notification

**Core Principle:** Hooks operate within an event hierarchy: events trigger matchers (tool patterns) which execute hooks (commands or prompts). Hooks can block actions, modify tool inputs, inject context, or observe and log operations.

## Quick Reference

**Hook Creation Pattern:**
1. **Identify Event Type:** Select from 11 supported event types
2. **Choose Hook Type:** Command hook (shell) or Prompt hook (LLM)
3. **Configure Matcher:** Tool pattern filter (optional for some events)
4. **Define Action:** Shell command or LLM prompt
5. **Test:** Use `claude --debug` for verification

**Debug Hooks:**
- Run `python3 manage-hooks/assets/scripts/hook-tester.py quick-diag .claude/hooks/hooks.json` for comprehensive diagnostics
- Use `debug` command for detailed step-by-step analysis
- Check permissions with `permissions` command
- Validate JSON output with `json-check` command
- See `references/debugging-hooks.md` for complete guide

## Available Resources

### Templates and Assets

#### Python Templates (`assets/templates/`)

- **`universal-hook.py`** - Unified template for blocking/observer modes with security patterns
- **`hooks-json.md`** - Hook configuration JSON structure

#### Utilities (`assets/scripts/`)

- **`path-validator.py`** - Utility for preventing traversal attacks
- **`hook-tester.py`** - Automated validation tool for all hook events

#### Deployment Guide

- **`references/deployment-guide.md`** - Complete guide for deploying hooks with absolute paths (recommended)

---

## Canonical Reference Documentation

**Hook Types & Matchers**: [hook-types.md](references/hook-types.md) - Events, schemas, regex matchers, and MCP naming
**Debugging Hooks**: [debugging-hooks.md](references/debugging-hooks.md) - Comprehensive debugging workflows and diagnostics
**Deploying Hooks**: [deployment-guide.md](references/deployment-guide.md) - Static path deployment to avoid environment variable dependencies
