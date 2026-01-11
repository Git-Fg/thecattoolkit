# Permissions & Security Reference

> **📘 Official Docs:** [Identity and Access Management](https://code.claude.com/docs/en/iam) - Complete official guide to permissions, security, and tool access rules.  
> **📖 Quick Reference:** See [CLAUDE.md](../CLAUDE.md#permissions--security) for a summary with decision guidance.

Complete reference for the Cat Toolkit permission system across Skills, Agents, and Commands.

---

## The Permission Cascade

> **📘 Official Docs:** [Permission configuration](https://code.claude.com/docs/en/iam#configuring-permissions)

```
Main Agent (baseline)
  ├─→ Subagent (can override via tools allowlist)
  └─→ Skill (can restrict during activation via allowed-tools)
```

---

## Skills vs Agents: Critical Distinction

| Aspect | Skills (`allowed-tools`) | Agents (`tools`) |
|:-------|:------------------------|:-----------------|
| **Purpose** | Temporary restriction during Skill activation | Persistent allowlist for subagent lifetime |
| **If omitted** | **No restriction** → uses standard permission model | **Inherits ALL tools** from parent (including MCP) |
| **If specified** | Restricts to specified tools only | Allowlist: ONLY specified tools available |
| **Security model** | "Least privilege during task" | "Least privilege by default (explicit)" |

---

## Skills: allowed-tools (Temporary Restriction)

Temporary scoped restriction during Skill activation (not a permanent capability grant).

| Configuration | Behavior | Examples |
|:--------------|:---------|:---------|
| **Omitted** | No restriction; standard permission model (may prompt) | - |
| **Specified** | ONLY listed tools available (no prompts for listed tools) | `[Read, Write, Bash]` or `"Read,Write,Bash"` |
| **With specifiers** | Restricted tool access using parentheses syntax | `[Bash(git:*), Bash(npm:*), Read]` |

**Syntax:** Use `Tool(specifier)` with parentheses, NOT brackets. Examples: `Bash(git add:*)`, `Bash(npm run test:*)`, `Bash(git * main)`.

---

## Agents: tools (Explicit Allowlist)

| Configuration | Availability | Security Level |
|:--------------|:-------------|:---------------|
| **Omitted** | Inherits ALL tools from parent (including MCP) | Low (dangerous for security-critical) |
| **Specified** | ONLY listed tools available | High (explicit allowlist) |
| **With disallowedTools** | Listed tools MINUS disallowed list | Medium (denylist filter) |

**Security Warning:** Omitting `tools` grants full tool access via inheritance. Always specify `tools` for security-critical agents.

**disallowedTools:** Removes specific tools from inherited/specified list. Acts as filter; cannot add tools.

---

## Permission Modes

> **⚠️ Best Practice:** Do NOT specify `permissionMode` in agent frontmatter. Let the runtime or CLI arguments determine the mode for maximum compatibility.


| Mode | Behavior | Security Level | Use Case |
|:-----|:---------|:---------------|:---------|
| `default` | Prompts for each tool | High | Uncertain operations |
| `acceptEdits` | Auto-approves file operations | Medium | Trusted refactoring |
| `dontAsk` | Auto-denies permission prompts (explicitly allowed tools still work) | High | Non-interactive environments (CI/CD, batch processing) |
| `plan` | Read-only analysis | High | Exploration without changes |
| `bypassPermissions` | All tools approved | **Very Low** | Dangerous automation |

> **Note**: `permissionMode` is **only valid for Agents**. Commands inherit permissions from the calling context and cannot set their own permission mode.

---

## Permission Specifiers Syntax

Use `Tool(specifier)` with **parentheses**, NOT brackets.

| Format | Example | Description |
|:-------|:--------|:------------|
| **Unrestricted** | `Bash`, `Read` | Full tool access |
| **Command-specific** | `Bash(git add:*)` | Allow only `git add` commands |
| **Wildcard prefix** | `Bash(npm *)` | Allow `npm` + any arguments |
| **Argument wildcard** | `Bash(git * main)` | Allow `git` commands targeting `main` |
| **Multiple patterns** | `[Bash(python:*), Bash(npm:*)]` | Combine restrictions |

**Rules:** Unrestricted = `Tool`. Restricted = `Tool(specifier)`. Wildcards: `*` matches any chars, `:*` matches command args.  
**Incorrect:** `Bash[python, npm]` → **Correct:** `Bash(python:*), Bash(npm:*)`

---

## Example: Security-Conscious Agent

```yaml
# agents/auditor.md
---
name: security-auditor
# model: omit (use runtime default)
# permissionMode: omit (use runtime default)
tools: [Read, Grep, Glob]     # Whitelist: NO Write, NO Bash
skills: [owasp-top-10, credential-scanner]
---
```

This agent can read files and search for patterns, but **cannot** modify files or execute commands. Even if the skill instructions request writes, the agent's tool whitelist prevents it.

---

## Common Security Patterns

| Pattern | Configuration |
|:--------|:--------------|
| **Read-Only Agent** | `permissionMode: plan` + `tools: [Read, Grep, Glob]` |
| **Git-Restricted Skill** | `allowed-tools: [Bash(git add:*), Bash(git commit:*), Bash(git status:*)]` |
| **Audit Agent** | `permissionMode: plan` + `tools: [Read, Grep, Glob]` + `skills: [owasp-top-10, credential-scanner]` |
| **Development Agent** | `tools: [Read, Write, Edit, Bash, Grep, Glob]` (explicit allowlist, not omitted) |

---

## Quick Reference: Security Checklist

| Task | Recommended Configuration |
|:-----|:--------------------------|
| **Security audit** | `permissionMode: plan` + `tools: [Read, Grep, Glob]` |
| **Git operations only** | `allowed-tools: [Bash(git:*)]` |
| **Read-only exploration** | `permissionMode: plan` |
| **Trusted refactor** | `permissionMode: acceptEdits` |
| **Non-interactive (CI/CD)** | `permissionMode: dontAsk` + allow rules in settings.json |
| **Dangerous automation** | Avoid `permissionMode: bypassPermissions` |
