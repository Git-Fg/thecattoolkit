# Permissions & Security Reference

Complete reference for the Cat Toolkit permission system across Skills, Agents, and Commands.

---

## The Permission Cascade

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

When a Skill specifies `allowed-tools`:
- Claude can **only use the specified tools** while the Skill is active
- No permission prompts for the listed tools during execution
- **If omitted**: No restriction applies. Claude uses standard permission model and may prompt for tool usage.

> **Key Insight**: `allowed-tools` in Skills is a **temporary scoped restriction**, not a permanent capability grant. The restriction only exists during the Skill's activation.

### allowed-tools Format Examples

```yaml
# Recommended: YAML list (full tool access)
allowed-tools: [Read, Write, Bash, Grep]

# Alternative: String (requires parsing)
allowed-tools: "Read,Write,Bash,Grep"

# With tool restrictions using permission specifiers (parentheses syntax)
allowed-tools: [Bash(git add:*), Bash(git status:*), Read]  # Bash restricted to git commands

# Multiple Bash restrictions
allowed-tools: [Bash(python:*), Bash(npm:*), Read]  # Bash can only run python and npm

# Wildcard patterns
allowed-tools: [Bash(npm run test:*), Bash(git * main)]  # Specific command patterns
```

### Behavior Summary

| Configuration | Behavior |
|:--------------|:---------|
| **Omitted** | No restriction. Uses standard permission model (may prompt for tool usage) |
| **Specified** | ONLY listed tools available during Skill activation (no prompts for listed tools) |

---

## Agents: tools (Explicit Allowlist)

When an Agent specifies `tools`:
- Creates an **explicit allowlist** for the subagent
- **If omitted**: Subagent inherits **ALL tools** from parent (including MCP servers)
- **If specified**: Only the listed tools are available (deny-by-default)
- Can be further restricted with `disallowedTools` (denylist)

> **Security Warning**: Omitting `tools` in an Agent grants **full tool access** via inheritance. Always specify `tools` for security-critical agents.

### Configuration Matrix

| Configuration | Availability | Security Level |
|:--------------|:-------------|:---------------|
| **Omitted** | Inherits ALL tools from parent (including MCP) | Low (dangerous for security-critical agents) |
| **Specified** | ONLY listed tools available | High (explicit allowlist) |
| **With disallowedTools** | Listed tools MINUS disallowed list | Medium (denylist on top of allowlist) |

---

## Permission Modes

| Mode | Behavior | Security Level | Use Case |
|:-----|:---------|::--------------|:---------|
| `default` | Prompts for each tool | High | Uncertain operations |
| `acceptEdits` | Auto-approves file operations | Medium | Trusted refactoring |
| `plan` | Read-only analysis | High | Exploration without changes |
| `bypassPermissions` | All tools approved | **Very Low** | Dangerous automation |

> **Note**: `permissionMode` is **only valid for Agents**. Commands inherit permissions from the calling context and cannot set their own permission mode.

---

## Permission Specifiers Syntax

When restricting tools, use the `Tool(specifier)` syntax with **parentheses**, NOT brackets.

| Format | Example | Description |
|:-------|:--------|:------------|
| **Unrestricted** | `Bash`, `Read` | Full access to the tool |
| **Command-specific** | `Bash(git add:*)` | Allow only `git add` commands |
| **Wildcard prefix** | `Bash(npm *)` | Allow `npm` followed by any arguments |
| **Argument wildcard** | `Bash(git * main)` | Allow `git` with any command targeting `main` |
| **Multiple patterns** | `[Bash(python:*), Bash(npm:*)]` | Combine multiple restrictions |

### Syntax Rules

- **Unrestricted tool:** `Tool` (e.g., `Bash`, `Read`)
- **Restricted tool:** `Tool(specifier)` using parentheses, NOT brackets
- **Bash specifiers:** Use shell-style patterns like `Bash(git add:*)`, `Bash(npm run test:*)`
- **Wildcards:** `*` matches any characters, `:*` matches command arguments

### Correct vs Incorrect

| [X] Incorrect | [✓] Correct |
|:-------------|:------------|
| `allowed-tools: [Bash[python, npm]]` | `allowed-tools: [Bash(python:*), Bash(npm:*)]` |
| Bracket syntax `Bash[...]` | Parentheses syntax `Bash(...)` |

---

## Example: Security-Conscious Agent

```yaml
# agents/auditor.md
---
name: security-auditor
model: opus
permissionMode: plan          # Read-only
tools: [Read, Grep, Glob]     # Whitelist: NO Write, NO Bash
skills: [owasp-top-10, credential-scanner]
---
```

This agent can read files and search for patterns, but **cannot** modify files or execute commands. Even if the skill instructions request writes, the agent's tool whitelist prevents it.

---

## Common Security Patterns

### 1. Read-Only Agent
```yaml
permissionMode: plan
tools: [Read, Grep, Glob]
```

### 2. Git-Restricted Skill
```yaml
allowed-tools: [Bash(git add:*), Bash(git commit:*), Bash(git status:*)]
```

### 3. Audit Agent with Knowledge Injection
```yaml
permissionMode: plan
tools: [Read, Grep, Glob]
skills: [owasp-top-10, credential-scanner]
```

### 4. Development Agent (Full Access)
```yaml
# Omit tools = inherits ALL tools (dangerous for security-critical)
# Better: explicit allowlist
tools: [Read, Write, Edit, Bash, Grep, Glob]
```

---

## Quick Reference: Security Checklist

| Task | Recommended Configuration |
|:-----|:--------------------------|
| **Security audit** | `permissionMode: plan` + `tools: [Read, Grep, Glob]` |
| **Git operations only** | `allowed-tools: [Bash(git:*)]` |
| **Read-only exploration** | `permissionMode: plan` |
| **Trusted refactor** | `permissionMode: acceptEdits` |
| **Dangerous automation** | Avoid `permissionMode: bypassPermissions` |
