# Command Permissions Guide

## Overview

Commands use the `allowed-tools` field in their frontmatter to **restrict** which tools they can use. Unlike agents and skills, commands **inherit all tools by default** and use `allowed-tools` for security restrictions.

## Key Principle

> **Commands inherit all tools by default.** The `allowed-tools` field is used to **restrict** access to only the tools explicitly listed.

---

## ⚠️ VIBECODING PRINCIPLE: Autonomy First

**This toolkit is designed for autonomous operation.** Commands should execute workflows independently with minimal user interaction.

### AskUserQuestion: Use Only When Explicitly Required

⚠️ **WARNING**: `AskUserQuestion` should **NOT** be included in `allowed-tools` by default.

**Only include `AskUserQuestion` in allowed-tools when:**
- The command's purpose is **gathering input** before execution
- The user **explicitly requests** interactive behavior
- The workflow is **designed** to present options for user selection

**DO NOT include `AskUserQuestion` when:**
- The command should execute autonomously (most cases)
- You want to pause for decisions that can be reasonably assumed
- The command's role is execution, not gathering requirements
- You're unsure if it's needed

**Default Behavior:**
- Omit `AskUserQuestion` from `allowed-tools`
- Let the command make reasonable decisions based on context
- Provide options in the final output for user review
- Use the command's description to guide its behavior

**The goal**: You invoke the command → Command executes the workflow → You review the result.

---

---

## Frontmatter Field

| Field | Type | Required | Default | Behavior |
|-------|------|----------|---------|----------|
| `allowed-tools` | Array or comma-separated string | No | Inherit all | If specified, ONLY these tools are available (restriction) |

---

## allowed-tools Field Behavior

### When Omitted (Default)

```yaml
---
description: Shortcut to deploy the application
---
```

**Result**: Command has access to **ALL tools** from the conversation context.

**Use when**: Command needs full tool access (most common case).

### When Specified

```yaml
---
description: Shortcut to deploy the application
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git push:*)
---
```

**Result**: Command has **ONLY** the tools explicitly listed.

**Use when**: You need to restrict the command for security (e.g., deployment commands, dangerous operations).

---

## Syntax Format

### Array Format (Recommended)

```yaml
allowed-tools: [Read, Grep, Glob]
```

### Comma-Separated String

```yaml
allowed-tools: Read, Grep, Glob
```

### Mixed (Tools + Patterns)

```yaml
allowed-tools: [Read, Grep, Bash(git status:*), Bash(git diff:*)]
```

---

## Available Tools

### Standard/Core Tools

| Tool | Description | Example Usage |
|------|-------------|---------------|
| `Read` | Read file contents | `allowed-tools: [Read]` |
| `Write` | Create or overwrite files | `allowed-tools: [Write]` |
| `Edit` | Make targeted edits | `allowed-tools: [Edit]` |
| `Bash` | Execute shell commands | `allowed-tools: Bash(git:*)` |
| `Grep` | Search file contents | `allowed-tools: [Grep]` |
| `Glob` | Find files by pattern | `allowed-tools: [Glob]` |
| `TodoWrite` | Manage task lists | `allowed-tools: [TodoWrite]` |
| `AskUserQuestion` | Ask user multiple-choice questions | `allowed-tools: [AskUserQuestion]` |
| `Task` | Delegate to subagents | `allowed-tools: [Task]` |
| `SlashCommand` | Invoke other commands | `allowed-tools: [SlashCommand]` |
| `Skill` | Execute a skill | `allowed-tools: Skill(manage-skills)` |

### Claude-Specific Tools

| Tool | Description | When to Include |
|------|-------------|-----------------|
| `NotebookEdit` | Modify Jupyter notebooks | Working with notebooks |
| `WebFetch` | Fetch URL content | Web access needed |
| `WebSearch` | Search the web | Web search needed |
| `LSP` | Language server operations | LSP features needed |

⚠️ **WARNING**: Only include Claude-specific tools when explicitly required.

### MCP Tools

Format: `mcp__server__tool`

```yaml
allowed-tools: [mcp__github__ask_question, mcp__postgres__query]
```

Wildcard syntax:
```yaml
allowed-tools: [mcp__github__*]  # All tools from github server
```

---

## Pattern-Based Restrictions

Commands support pattern-based restrictions for fine-grained control.

### Bash Command Patterns

**Syntax**: `Bash(command:args)`

- Exact match: `Bash(npm test)`
- Prefix match with wildcard: `Bash(npm:*)`
- Wildcard only at end: `Bash(git status:*)`

✅ **Valid patterns:**
```yaml
allowed-tools: Bash(git status:*)
allowed-tools: Bash(npm test:*)
allowed-tools: Bash(curl http://example.com/:*)
```

❌ **Invalid patterns:**
```yaml
# Wildcard not at end - doesn't work
allowed-tools: Bash(git:* status)

# Regex patterns - not supported
allowed-tools: Bash(git (status|log):*)

# Glob patterns - not supported
allowed-tools: Bash(git ?)
```

⚠️ **IMPORTANT**: Bash patterns use **prefix matching only**. The `:*` wildcard only works at the end of a pattern.

### Read/Edit Path Patterns

Commands support gitignore-style path patterns for `Read` and `Edit` tools.

**Pattern types:**

| Pattern | Meaning | Example |
|---------|---------|---------|
| `//path` | Absolute from filesystem root | `Read(//Users/alice/secrets/**)` |
| `~/path` | From home directory | `Read(~/Documents/*.pdf)` |
| `/path` | Relative to settings file | `Edit(/src/**/*.ts)` |
| `path` or `./path` | Relative to current directory | `Read(*.env)` |

**Examples:**
```yaml
allowed-tools: [Edit(/docs/**)]  # Edit files in <project>/docs/
allowed-tools: [Read(~/.zshrc)]  # Read home directory .zshrc
allowed-tools: [Edit(//tmp/*.txt)]  # Edit /tmp/*.txt
allowed-tools: [Read(src/**)]  # Read from <cwd>/src/
```

⚠️ **WARNING**: A pattern like `/Users/alice/file` is relative to settings file, NOT absolute. Use `//Users/alice/file` for absolute paths.

### WebFetch Domain Patterns

**Syntax**: `WebFetch(domain:example.com)`

```yaml
allowed-tools: WebFetch(domain:github.com)
allowed-tools: WebFetch(domain:api.anthropic.com)
```

---

## Common Patterns

### Pattern 1: Git-Only Command

Commands that should only interact with git:

```yaml
---
description: Shortcut to commit and push changes
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*)
---
```

### Pattern 2: Read-Only Analysis

Commands that analyze but don't modify:

```yaml
---
description: Shortcut to analyze code quality
allowed-tools: [Read, Grep, Glob]
---
```

### Pattern 3: Test Runner

Commands that run tests but don't deploy:

```yaml
---
description: Shortcut to run tests and linting
allowed-tools: Bash(npm test:*), Bash(npm run lint:*)
---
```

### Pattern 4: Safe Deployment

Commands that deploy to staging but not production:

```yaml
---
description: Shortcut to deploy to staging
allowed-tools: Bash(npm run deploy:staging), Bash(git push origin:staging)
---
```

### Pattern 5: Skill Delegation

Commands that delegate to a specific skill:

```yaml
---
description: Shortcut to invoke the engineering skill
allowed-tools: Skill(engineering)
---
```

### Pattern 6: Agent Delegation

Commands that delegate to a specific agent:

```yaml
---
description: Shortcut to delegate to the brainstormer agent
allowed-tools: Task
---
```

**Note**: When delegating to agents, don't restrict tools heavily. Agents should have access to tools through conversation inheritance.

### Pattern 7: Dynamic Context Loading

Commands that use the `!` prefix for dynamic context loading:

```yaml
---
description: Shortcut to analyze current git state
! git status
allowed-tools: Bash(git status:*), Bash(git diff:*)
---
```

⚠️ **CRITICAL**: If a command uses `!` prefix, you **must** include `allowed-tools: Bash(...)` with the relevant Bash patterns.

---

## When to Use allowed-tools

### ✅ Use allowed-tools when:

- Command performs **dangerous operations** (deployment, git push, etc.)
- Command needs **security restrictions** (read-only access)
- Command uses `!` prefix for dynamic context
- Command should be **limited to specific tools** for safety
- Command is a **shortcut to a specific skill** or agent

### ❌ Omit allowed-tools when:

- Command needs **full tool access** (most cases)
- You're **unsure** what tools are needed
- Command is **delegating to an agent** (agents inherit tools)
- Command is a **simple reminder or template**
- Simplicity is **preferred**

---

## Security Considerations

### Principle of Least Privilege

When configuring command permissions:

1. **Start with no allowed-tools** (full access)
2. **Add restrictions only when needed** for security
3. **Use pattern-based restrictions** for fine-grained control
4. **Test that command still works** after restrictions

### Dangerous Command Patterns

| Pattern | Risk | Safe Alternative |
|---------|------|------------------|
| `allowed-tools: [Bash]` | Full shell access | Use `Bash(command:*)` patterns |
| `allowed-tools: []` | Command breaks | Remove field entirely |
| Over-restricting delegation | Agent can't function | Don't use `allowed-tools` with agent delegation |

### Bash Pattern Limitations

⚠️ **IMPORTANT**: Bash permission patterns have limitations:

1. **Prefix matches only** - not regex or glob
2. **`:*` wildcard only at end** of pattern
3. **Can be bypassed** in various ways:
   - Options before URL: `curl -X GET http://github.com/...`
   - Different protocol: `curl https://github.com/...`
   - Redirects: `curl -L http://bit.ly/xyz`
   - Variables: `URL=http://github && curl $URL`
   - Extra spaces: `curl  http://github.com`

**For more reliable URL filtering:**
- Use `WebFetch(domain:github.com)` permission
- Instruct Claude via CLAUDE.md about allowed patterns
- Use hooks for custom permission validation

---

## Migration from Other Components

### From Agent

| Agent Field | Command Equivalent | Notes |
|-------------|-------------------|-------|
| `tools: Bash` | `allowed-tools: Bash` | Same tool, different field name |
| `tools: [Read, Grep]` | `allowed-tools: [Read, Grep]` | Array format works |
| Pattern restrictions | Available | Commands support more patterns |

### From Skill

| Skill Field | Command Equivalent | Notes |
|-------------|-------------------|-------|
| N/A | `allowed-tools` | Skills don't have permission system |

---

## Examples

### Example 1: Simple Reminder Command

```yaml
---
description: Quick reminder of git commit conventions
---

# Git Commit Conventions

- Use present tense: "Add feature" not "Added feature"
- Reference issues: "Fix #123"
- Keep first line under 50 characters
```

**No `allowed-tools` needed** - command is just text.

### Example 2: Git Commit Command

```yaml
---
description: Shortcut to commit changes with proper formatting
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git commit:*)
---

Commit the current changes following team conventions.
```

**Restricted to git operations only** - safer deployment.

### Example 3: Code Analysis Command

```yaml
---
description: Shortcut to analyze code for potential issues
allowed-tools: [Read, Grep, Glob]
---

Analyze the codebase for:
- Common bugs
- Security issues
- Performance problems
```

**Read-only access** - cannot modify code.

### Example 4: Skill Invoker

```yaml
---
description: Shortcut to invoke the engineering skill
allowed-tools: Skill(engineering)
---

Debug, review, refactor, or audit code.
```

**Locked to specific skill** - focused purpose.

### Example 5: Full-Power Command

```yaml
---
description: Shortcut to run full development workflow
---

Run tests, lint, build, and deploy as needed.
```

**No `allowed-tools`** - full access for flexibility.

---

## Troubleshooting

### Command says it doesn't have access to a tool

**Problem**: Command cannot use a tool you think it should have.

**Solution**:
1. Check if `allowed-tools` is restricting access
2. Remove `allowed-tools` if not needed for security
3. Add the missing tool to `allowed-tools` if restrictions are needed

### Command with `!` prefix doesn't work

**Problem**: Command using `!` for dynamic context fails.

**Solution**: You **must** include `allowed-tools: Bash(...)` with relevant patterns.

```yaml
---
description: Show git status
! git status
allowed-tools: Bash(git status:*)  # REQUIRED when using !
---
```

### Agent delegation is restricted

**Problem**: Command delegates to agent but agent can't use tools.

**Solution**: Don't use `allowed-tools` when delegating to agents, or include `Task` in the list.

---

## Related Documentation

- [Command Frontmatter Reference](./frontmatter.md)
- [Tool Restrictions Guide](./tool-restrictions.md)
- [Command Patterns](./patterns.md)
- [Cross-Platform Considerations](./cross-platform.md)
