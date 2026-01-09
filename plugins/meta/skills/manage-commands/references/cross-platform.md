# Slash Command Standards

Technical specification for slash command implementations in the toolkit, aligned with Claude Code native primitives.

## Structure

Commands are defined in Markdown files with YAML frontmatter.

### Directory Layout
- **Project-Level**: `.claude/commands/`
- **User-Level**: `~/.claude/commands/`

### Frontmatter Schema

```yaml
---
description: Required - shown in /help and used for auto-discovery
argument-hint: Optional - shown in autocomplete (e.g., "[path] [query]")
allowed-tools: Optional - restrict tools (e.g., "[Read, Grep]")
model: Optional - specific model to use (haiku, sonnet, opus)
disable-model-invocation: Optional - prevent programmatic invocation via Skill tool
---
```

## Argument Handling

Use the following placeholders to handle user input:

| Pattern | Syntax | Description |
|---------|--------|-------------|
| All arguments | `$ARGUMENTS` | The entire argument string |
| Positional | `$1`, `$2`, `$3` | Individual space-separated tokens |
| File reference | `@ $ARGUMENTS` | Triggers file pickers/context attachment |
| Default value | `${ARGUMENTS:-default}` | Shell-style default fallback |

## Dynamic Context

Use the `!` prefix within the Markdown body to execute shell commands and inject their output into the prompt:

```markdown
## System Status
- Git: ! `git status --short`
- Environment: ! `env | grep CLAUDE`
```

**Security Requirement**: You must specify `allowed-tools` (including `Bash`) if using the `!` prefix.

## Discovery Rules

1. **Naming**: The command name is derived from the filename (e.g., `audit-logs.md` becomes `/audit-logs`).
2. **Semantic Matching**: Claude Code uses the `description` field to determine which command matches the user's intent.
3. **Hierarchy**: Project-level commands override user-level commands of the same name.

## Implementation Template

Follow this "Gold Standard" template for all toolkit commands:

```markdown
---
description: [Action-oriented description for semantic matching]
argument-hint: [Optional placeholder]
---

# [Command Name]

## Objective
[One sentence summary of the goal]

## Context
[Dynamic context using ! if needed]

## Instructions
[Step-by-step instructions for the Agent]

## Success Criteria
- [Expected outcome]
```

## Best Practices

1. **Keep it Declarative**: Describe the goal, not the tool list.
2. **Handle Arguments Gracefully**: Provide fallback instructions if `$ARGUMENTS` are missing.
3. **Mercenary Isolation**: Do not assume the command is being run by a specific agent.
4. **Use `@` for Files**: Encourage users to use the `@` prefix for targeted context.
