# Agent Security Model

## The Golden Rule of Permissions

> **If `tools` is OMITTED, the Agent inherits ALL tools from the parent.**

This is a massive security risk. Always specify an explicit whitelist.

## Inheritance Cascade

```
Main Agent (baseline tools)
  ├─→ Subagent (can override via tools allowlist)
  └─→ Skill (can restrict during activation via allowed-tools)
```

## Permission Modes

| Mode | Behavior | Security Level | Use Case |
|:-----|:---------|:---------------|:---------|
| `plan` | Read-only, no edits | High | Exploration, analysis |
| `acceptEdits` | Auto-approves file operations | Medium | Trusted refactoring |
| `default` (omit) | Prompts for each tool | High | Uncertain operations |
| `dontAsk` | Auto-denies permission prompts | High | Non-interactive environments |
| `bypassPermissions` | All tools approved | **Very Low** | Dangerous automation |

**Best Practice:** Omit `permissionMode` from agent frontmatter. Let the runtime or CLI arguments determine the mode for maximum compatibility.

## Configuration Matrix

### Reader/Analyst Agent

**Purpose:** Exploration without modification

```yaml
---
name: code-analyst
permissionMode: plan
tools: [Read, Glob, Grep]
skills: [domain-knowledge]
---

# Code Analyst

You analyze code structure and patterns.
**Cannot** modify files or execute commands.
```

**Security Level:** High
- Read-only operations only
- No file modification possible
- No command execution

### Coder/Worker Agent

**Purpose:** Execute engineering tasks

```yaml
---
name: worker
# permissionMode: acceptEdits (or omit for default)
tools: [Read, Write, Edit, Bash, Glob, Grep]
skills: [execution-core, software-engineering]
---

# Builder Worker

Execute tasks in UNINTERRUPTED FLOW.
Follow behavioral standards from `execution-core`.
```

**Security Level:** Medium
- Can modify files
- Can execute commands
- Follows behavioral standards

### Director Agent

**Purpose:** Coordinate other agents

```yaml
---
name: director
# permissionMode: omit (uses default)
tools: [Task, AskUserQuestion, Read, Write, Edit]
skills: [manage-planning, prompt-engineering]
---

# Plan Director

Coordinate execution across multiple worker agents.
Provide clear instructions and verify results.
```

**Security Level:** Medium
- Can spawn subagents
- Can interact with user
- Coordinates but doesn't execute directly

### Background Agent

**Purpose:** Long-running autonomous work

```yaml
---
name: background-worker
# permissionMode: omit
tools: [Read, Write, Bash]  # NO AskUserQuestion
skills: [execution-core]
---

# Background Worker

Execute long-running tasks autonomously.
**CRITICAL:** No user interaction possible.
```

**Security Level:** Medium
- Autonomous operation
- No user prompts possible
- Must handle errors independently

## Tool Whitelist Patterns

### Restrictive (High Security)

```yaml
tools: [Read, Glob, Grep]
```

- Read-only access
- No file modification
- No command execution
- Use for: Analysis, exploration

### Standard (Medium Security)

```yaml
tools: [Read, Write, Edit, Bash, Glob, Grep]
```

- Full file operations
- Command execution
- Use for: Workers, implementers

### Permissive (Lower Security)

```yaml
tools: [Task, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep]
```

- Can spawn subagents
- Can prompt user
- Use for: Directors, coordinators

### Command-Restricted

```yaml
tools: [Read, Write, Bash(git:*), Bash(npm:*)]
```

- Restricts Bash to specific commands
- Use for: Git operations, package management

## Common Security Pitfalls

### 1. Missing Tools Field

**Bad:**
```yaml
---
name: worker
# No tools field = inherits EVERYTHING
---
```

**Good:**
```yaml
---
name: worker
tools: [Read, Write, Edit, Bash]
---
```

### 2. AskUserQuestion in Background Agent

**Bad:**
```yaml
---
name: background-worker
tools: [Read, Write, Bash, AskUserQuestion]  # Will hang!
---
```

**Good:**
```yaml
---
name: background-worker
tools: [Read, Write, Bash]  # No user interaction
---
```

### 3. Over-Permissive Analyst

**Bad:**
```yaml
---
name: analyst
tools: [Read, Write, Bash]  # Can modify files!
---
```

**Good:**
```yaml
---
name: analyst
permissionMode: plan
tools: [Read, Glob, Grep]  # Read-only
---
```

## Validation Checklist

- [ ] `tools` field specified (not omitted)
- [ ] Tools match agent purpose
- [ ] `AskUserQuestion` NOT in background agent tools
- [ ] `permissionMode` omitted (use runtime default)
- [ ] Security level appropriate for task
- [ ] Tool restrictions applied where needed
