# Cross-Platform Slash Commands

A comparison of slash command implementations across major AI coding platforms.

## Platform Overview

| Platform | Base Directory | File Extension | Frontmatter Required |
|----------|----------------|----------------|---------------------|
| Claude Code | `.claude/commands/` | `.md` | Yes (`description`) |
| Roo Code | `.roo/commands/` | `.md` | Yes (`description`) |
| OpenCode | `.opencode/commands/` | `.md` | No (optional metadata) |

## Frontmatter Fields Comparison

### Claude Code

```yaml
---
description: Required - shown in /help and used for auto-discovery
allowed-tools: Optional - restrict tools (not enable)
argument-hint: Optional - shown in autocomplete
model: Optional - specific model to use
disable-model-invocation: Optional - prevent programmatic invocation via Skill tool
---
```

### Roo Code (Additional Fields)

```yaml
---
description: Required - command description
argumentHint: Optional - alias for argument-hint
mode: Optional - switch mode before execution
---
```

**Roo Code `mode` field examples:**
- `mode: code` - Switch to Code mode
- `mode: architect` - Switch to Architect mode
- `mode: ask` - Switch to Ask mode

### OpenCode

```yaml
---
# Optional metadata (JSON-style)
name: command-name
description: Command description
---
```

OpenCode focuses on automatic discovery with minimal required frontmatter.

## Argument Handling

All platforms support similar argument patterns:

| Pattern | Syntax | Description |
|---------|--------|-------------|
| All arguments | `$ARGUMENTS` | All arguments as string |
| Positional | `$1`, `$2`, `$3` | Individual arguments |
| File reference | `@ $ARGUMENTS` | File path reference |
| Default value | `${ARGUMENTS:-default}` | Shell parameter expansion |

## Dynamic Context

### Claude Code & Roo Code

Use `!` prefix for bash execution:

```markdown
## Context
- Status: ! `git status`
- Changes: ! `git diff HEAD`
```

**Requirement**: Must specify `allowed-tools: Bash(...)` when using `!` prefix.

### OpenCode

Supports similar dynamic context but may have different tool permission models.

## Tool Restrictions

### Claude Code

```yaml
allowed-tools: Bash(git add:*), Bash(git status:*)
```

**Key point**: `allowed-tools` is for RESTRICTING, not enabling. Commands inherit all tools by default.

### Roo Code

Similar to Claude Code with Bash pattern restrictions.

### OpenCode

Uses pattern-based permissions in configuration files:

```json
{
  "permission": {
    "bash": {
      "git-*": "allow",
      "*": "deny"
    }
  }
}
```

## Command Discovery

All platforms use automatic directory scanning:

| Platform | Discovery Method | Reload Behavior |
|----------|-----------------|-----------------|
| Claude Code | Directory scan | Automatic or restart |
| Roo Code | File watchers | Real-time |
| OpenCode | Directory scan | Automatic |

## Naming Conventions

| Platform | Name Source | Character Rules |
|----------|-------------|-----------------|
| Claude Code | Filename | Lowercase, hyphens |
| Roo Code | Filename | Lowercase, special chars removed |
| OpenCode | Filename or `name` field | Alphanumeric + hyphens |

### Examples

```
# All platforms interpret similarly
.claude/commands/git-commit.md → /git-commit
.roo/commands/api_docs.md → /api-docs (Roo removes underscore)
.opencode/commands/fix-issue.md → /fix-issue
```

## Mode Switching (Roo Code Specific)

Roo Code supports mode switching via frontmatter:

```yaml
---
mode: architect
description: Design system architecture
---
```

When invoked, Roo switches to the specified mode before executing the command.

**Common modes:**
- `code` - Implementation mode
- `architect` - Design and planning mode
- `ask` - Q&A mode without file modifications

## Generalist Best Practices

### Platform-Agnostic Patterns

These patterns work across all platforms:

1. **Required description** - All platforms benefit from clear descriptions
2. **Argument hints** - Improve user experience on all platforms
3. **File references** - `@` prefix works universally
4. **Dynamic context** - `!` prefix for bash (where supported)

### When to Use Platform-Specific Features

| Feature | Use When | Notes |
|---------|----------|-------|
| `mode` (Roo) | Need mode-switching behavior | Fallback to manual instructions |
| `disable-model-invocation` | Commands intended for manual invocation only | Not supported everywhere |
| `allowed-tools` | Security restrictions | Use default inheritance when possible |
| Tool permissions | Fine-grained control | OpenCode uses config files |

## Cross-Platform Command Template

```markdown
---
description: Clear, specific description of when to use this command
argument-hint: [optional-argument]
---

## Objective
One-sentence summary of what this command does.

## Context
- Dynamic state: ! `command-if-needed`

## Process
1. First step
2. Second step
3. Third step

## Success Criteria
- Expected outcome 1
- Expected outcome 2
```

This template works across Claude Code, Roo Code, and OpenCode with minimal modification.

## Migration Guide

### From Claude Code to Roo Code

1. `argument-hint` → `argumentHint` (optional, both work)
2. Add `mode` field if mode-switching needed
3. Move file from `.claude/commands/` to `.roo/commands/`

### From Claude Code to OpenCode

1. Remove `allowed-tools` from frontmatter (use config instead)
2. Move file from `.claude/commands/` to `.opencode/commands/`
3. Add optional `name` field if different from filename

### From Roo Code to Claude Code

1. Remove `mode` field (add instruction to switch manually)
2. `argumentHint` → `argument-hint` (optional, both work)
3. Move file from `.roo/commands/` to `.claude/commands/`

## Key Differences Summary

| Aspect | Claude Code | Roo Code | OpenCode |
|--------|-------------|----------|----------|
| Tool restrictions | Frontmatter | Frontmatter | Config file |
| Mode switching | No | Yes (frontmatter) | No |
| Argument hint | `argument-hint` | Both forms | `argument-hint` |
| Permissions | `allowed-tools` | `allowed-tools` | JSON config |
| Auto-invocation control | Yes | No | No |

## Recommendations

### For Maximum Portability

1. **Use common frontmatter fields:**
   ```yaml
   ---
   description: Clear description
   argument-hint: [args]
   ---
   ```

2. **Avoid platform-specific features:**
   - Skip `mode` field (add manual instruction)
   - Skip `disable-model-invocation` (document as manual invocation only)
   - Use default tool inheritance

3. **Use standard argument patterns:**
   - `$ARGUMENTS` for all args
   - `$1`, `$2` for positional
   - `@ $ARGUMENTS` for files

4. **Document platform differences:**
   ```markdown
   ## Platform Notes
   - Claude Code: Uses /command-name
   - Roo Code: Switches to code mode first
   - OpenCode: Requires skill permission
   ```

### For Platform Optimization

When targeting a specific platform, leverage its unique features:

**Claude Code:**
- Use `allowed-tools` for security
- Use `disable-model-invocation` for commands intended for manual invocation only
- Strong description keywords for discovery

**Roo Code:**
- Use `mode` for automatic switching
- Leverage file watchers for rapid iteration
- Use mode-specific command directories

**OpenCode:**
- Configure permissions in `opencode.json`
- Use skill system for command packaging
- Leverage Claude-compatible paths
