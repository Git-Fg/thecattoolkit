# Frontmatter Complete Reference

All frontmatter fields for slash commands with official documentation.

## Complete Frontmatter Table

| Field | Type | Purpose | Default | Required |
|-------|------|---------|---------|----------|
| `description` | string | Brief description of what the command does | First line of prompt | **Yes** |
| `allowed-tools` | array/pattern | List of tools the command can use (restricts access) | Inherits from conversation | No |
| `argument-hint` | string | Arguments expected, shown in autocomplete | None | No |
| `model` | string | Specific model to use | Inherits from conversation | No |
| `disable-model-invocation` | boolean | Prevent SlashCommand tool from programmatically invoking this specific command | false | No |

## description Field

**Required**: Yes

**Purpose**: Shown in `/help` command list and used by SlashCommand tool for context.

**Best Practices**:
- Be concise (one line)
- Describe what the command does
- Include trigger keywords for automatic discovery
- Use strong language (MUST USE, PROACTIVELY USE) for critical commands

**Examples**:

```yaml
# Good
description: Create git commit for current changes
description: MUST USE when investigating bugs requiring systematic analysis
description: Audit agent configuration for best practices compliance

# Bad
description: A command for commits
description: Helps with stuff
```

## allowed-tools Field

**Required**: No (only for restrictions)

**Default**: Inherits all tools from the conversation

**Purpose**: **RESTRICT** tool access, not enable tools.

**Key Point**: Commands automatically have access to all tools in the conversation. Only use this field to LIMIT what a command can do.

**Syntax**:

```yaml
# Array format
allowed-tools: [Read, Edit, Write]

# Single tool
allowed-tools: SequentialThinking

# Bash patterns (for ! prefix commands)
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)

# Mixed
allowed-tools: [Read, Grep, Bash(git status:*)]
```

**When to Use**:

✅ **Use when**:
- Using `!` prefix for bash execution (MUST specify Bash patterns)
- Security-sensitive operations (git, deployment)
- Read-only analysis commands
- Focused single-purpose commands

❌ **Don't use when**:
- Command delegates to agents (needs Task tool flexibility)
- Command may need various tools
- General-purpose commands
- Most cases - default is best

## argument-hint Field

**Required**: No

**Purpose**: Shown to users during command autocomplete. Helps users understand what arguments are expected.

**Format**: Square brackets `[]` for optional, angle brackets `<>` for required.

**Examples**:

```yaml
# Optional argument
argument-hint: [file-path]

# Required argument
argument-hint: <issue-number>

# Multiple arguments (mixed)
argument-hint: <pr-number> [priority] [assignee]

# Multiple choices
argument-hint: add [tagId] | remove [tagId] | list

# Structured
argument-hint: [what you want to build, audit, or fix]
```

**Best Practices**:
- Use `[square brackets]` for optional arguments
- Use `<angle brackets>` for required arguments
- Separate multiple arguments with spaces
- Use pipe `|` for mutually exclusive choices
- Keep hints concise but descriptive

## model Field

**Required**: No

**Default**: Inherits from the conversation

**Purpose**: Force a specific model for this command.

**Values**: Any valid model identifier (e.g., `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-20241022`)

**Example**:

```yaml
---
model: claude-3-5-haiku-20241022
description: Quick format check
---

Quick check code formatting.
```

**Use Cases**:
- Fast simple commands (use Haiku for speed)
- Complex reasoning tasks (use Sonnet/Opus)
- Cost-sensitive operations

**Note**: Usually better to let the conversation default apply.

## disable-model-invocation Field

**Required**: No

**Default**: `false`

**Purpose**: Prevent the SlashCommand tool from programmatically invoking this specific slash command. When set, also removes the command's metadata from context.

**Core Concept: User-Centric Wrappers**

This flag is for **user-centric wrapper commands**—commands that exist as convenient shortcuts for human users, not for AI programmatic invocation.

The AI can already:
- Use the `Skill` tool directly to invoke any skill
- Use the `Task` tool directly to invoke any subagent

Therefore, wrapper commands that simply delegate to these tools are intended for **manual user invocation only**.

**What it does**:
- Prevents the **SlashCommand tool** from calling this specific command
- Removes the command's metadata from context when set in frontmatter

**What it does NOT disable**:
- ✅ Task tool (can still invoke any subagent)
- ✅ Skill tool (can still invoke any skill)
- ✅ Other SlashCommands (other commands can still be invoked via SlashCommand tool)

**Key distinction**: This flag is **command-specific**—it only prevents Claude from programmatically invoking that particular slash command via the SlashCommand tool. You can still manually invoke the command yourself using `/command-name`.

**When to Use**:

✅ **Use for ALL wrapper commands** (both skill wrappers AND agent wrappers):

**Skill Wrappers** (Verbs, Objects, Execution categories):
```yaml
---
description: [Objects] Shortcut to invoke the manage-commands skill for creating command lifecycle workflows.
allowed-tools: Skill(manage-commands)
argument-hint: [workflow description]
disable-model-invocation: true
---

## Objective
Create a command lifecycle workflow for: $ARGUMENTS

This establishes a sophisticated command structure that guides users through command creation and management.

## Process
1. Invoke the `manage-commands` skill to manage the command
2. Follow the command creation workflow

## Success Criteria
- Command created with proper structure
- Clear workflow transitions defined
```

**Agent Wrappers** (Personas category):
```yaml
---
description: [Personas] Delegate to expert for system maintenance and infrastructure.
allowed-tools: Task, Read, Glob, Grep
argument-hint: [maintenance or audit task]
disable-model-invocation: true
---

Task the plugin-expert agent with: $ARGUMENTS

This provides system maintenance expertise for auditing, creating, or fixing AI components (agents, skills, commands).

Important: The context provided to the Agent must be exhaustive and cover all relevant information. It starts with a fully-clean slate, like a child - it's better to give it too much context than not enough.
```

❌ **Don't use for**:
- Commands that implement complex multi-step workflows directly (not simple wrappers)
- Commands that need to be programmatically invoked by other commands

## Complete Examples

### Simple Command (Minimal Frontmatter)

```yaml
---
description: Review this code for bugs
---

Review this code for bugs and suggest fixes.
```

### Command with Arguments

```yaml
---
description: Fix issue following coding standards
argument-hint: [issue-number]
---

Fix issue #$ARGUMENTS following our coding standards.
```

### Git Command with Restrictions

```yaml
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create git commit
model: claude-3-5-haiku-20241022
---

## Context
Status: ! `git status`
Diff: ! `git diff HEAD`

Create a commit for these changes.
```

### Delegation Command (No restrictions)

```yaml
---
description: Audit an agent configuration
argument-hint: [agent-name-or-path]
---

## Objective
Audit agent at: ${ARGUMENTS:-.}

## Process
Use plugin-expert agent to audit:
```

### Command Intended for Manual Invocation Only

```yaml
---
description: One-time project setup
disable-model-invocation: true
---

## This command sets up the project structure
# Run manually once per project - Claude should not invoke this programmatically
```

## Frontmatter Validation

### Required Fields Checklist

- [ ] `description` field present
- [ ] `description` is concise and clear
- [ ] `description` uses strong language for critical commands

### Optional Fields Usage

- [ ] `allowed-tools` - only for security restrictions
- [ ] `argument-hint` - if command accepts arguments
- [ ] `model` - only if specific model needed
- [ ] `disable-model-invocation` - only for commands intended for manual invocation only

### Common Mistakes

❌ **Missing description**:
```yaml
---
# No description field
---
```

❌ **Over-restricting delegation commands**:
```yaml
---
allowed-tools: [Task]  # Prevents Read/Grep/Glob
description: Delegate to agent
---
```

❌ **Using allowed-tools to enable**:
```yaml
---
# WRONG - allowed-tools is for restricting, not enabling
allowed-tools: [Task]  # Doesn't enable Task, it restricts TO only Task
description: My command
---
```

✅ **Correct patterns**:
```yaml
---
# No restrictions - inherits from conversation
description: Delegate to agent
---

---
# Security restriction - limits to git commands only
allowed-tools: Bash(git add:*), Bash(git status:*)
description: Create commit
---

---
# Bash execution requirement - must specify Bash patterns
allowed-tools: Bash(git status:*), Bash(npm test:*)
description: Check status with tests
---
```

## Quick Reference

| I want to... | Frontmatter needed |
|--------------|-------------------|
| Basic command | `description` only |
| Accept arguments | Add `argument-hint` |
| Use bash `!` prefix | Add `allowed-tools: Bash(...)` |
| Restrict to specific tools | Add `allowed-tools: [...]` |
| Delegate to agent | No `allowed-tools` (inherit Task) |
| Force specific model | Add `model: <model-id>` |
| Prevent programmatic invocation | Add `disable-model-invocation: true` |
| Most commands | `description` + `argument-hint` only |
