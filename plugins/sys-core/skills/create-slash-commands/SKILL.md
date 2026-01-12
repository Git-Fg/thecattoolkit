---
name: create-slash-commands
description: "Expert guidance for creating Claude Code slash commands. MUST Use when working with slash commands, creating custom commands, or understanding command structure."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash(mkdir:-p), Bash(ls:*), Bash(cat:*)]
---

# Slash Commands: Command Creation Authority

## Objective

Create effective slash commands for Claude Code that enable users to trigger reusable prompts with `/command-name` syntax. Slash commands expand as prompts in the current conversation, allowing teams to standardize workflows and operations.

> **Core Concept:** Commands are reusable prompt templates with YAML frontmatter that expand when invoked, providing zero-token retention workflows.

## Quick Start

1. Create `.claude/commands/` directory
2. Create `command-name.md` file
3. Add YAML frontmatter (minimum: description)
4. Write command prompt
5. Test with `/command-name [args]`

**Example:**
```markdown
---
description: "Analyze code for performance issues"
---

Analyze this code for performance issues and suggest optimizations.
```

**Usage:** `/analyze`

## Core Structure

### YAML Frontmatter (Required)

**`description`** - What the command does
```yaml
description: "Analyze this code for performance issues and suggest optimizations"
```

**`argument-hint`** - Optional, when command accepts arguments
```yaml
argument-hint: [file-path]
```

**`allowed-tools`** - Optional, restricts available tools
```yaml
allowed-tools: [Read, Grep]
```

### Command Body

Commands use plain markdown after frontmatter. Reference:

**Dynamic arguments:**
- `$ARGUMENTS` - All arguments as string
- `$1`, `$2`, `$3` - Positional arguments

**Dynamic context:**
- `!` command - Execute before prompt (e.g., `! git status`)
- `@ file` - Reference file contents

## Command Types

### Simple Commands
Self-contained procedures operating on implicit context.

**Example:**
```markdown
---
description: "Review code for security vulnerabilities"
---

Review this code for security vulnerabilities:
1. Check for common vulnerabilities (XSS, SQL injection, etc.)
2. Identify specific issues with line numbers
3. Suggest remediation
```

### Parameterized Commands
Commands accepting user input via $ARGUMENTS.

**Example:**
```markdown
---
description: "Fix issue following coding standards"
argument-hint: [issue-number]
---

Fix issue #$ARGUMENTS following project coding standards.
```

### Context-Aware Commands
Commands loading dynamic state with bash execution.

**Example:**
```markdown
---
description: "Create a git commit"
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

Current status: ! git status
Changes: ! git diff HEAD

Create a commit for these changes.
```

### Tool-Restricted Commands
Commands with limited tool access for safety.

**Example:**
```markdown
---
description: "Analyze codebase safely"
allowed-tools: [Read, Grep, Glob]
---

Search codebase for: $ARGUMENTS
```

## File Locations

**Project commands:** `.claude/commands/` (shared via version control)
**Personal commands:** `~/.claude/commands/` (available across projects)

## Best Practices

1. **Clear descriptions** - Explain what the command does
2. **Use arguments wisely** - Accept input when needed, omit when not
3. **Restrict tools** - Limit permissions for safety when appropriate
4. **Load context** - Use `!` and `@` for dynamic state
5. **Keep focused** - Each command should have one clear purpose

## Quick Reference

**Arguments:**
- `$ARGUMENTS` - All user input
- `$1`, `$2`, `$3` - Positional arguments
- `argument-hint` - Document expected input

**Dynamic context:**
- `! command` - Execute and include output
- `@ file` - Reference file contents

**Tool restrictions:**
- `allowed-tools: [Read, Grep]` - Read-only
- `allowed-tools: Bash(git:*)` - Git commands only

## Examples

See [references/patterns.md](references/patterns.md) for:
- Git workflows
- Code analysis
- File operations
- Security reviews
- Testing workflows

See [references/arguments.md](references/arguments.md) for:
- Argument handling patterns
- Positional argument syntax
- Complex examples

See [references/tool-restrictions.md](references/tool-restrictions.md) for:
- Security patterns
- Bash restrictions
- Read-only commands
