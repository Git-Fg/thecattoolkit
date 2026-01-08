# XML/Markdown Decision Framework for Commands

## Core Philosophy

**Prefer Markdown over XML when possible.** Use XML tags as semantic containers for sections that must be machine-parsed or strictly isolated. Reserve XML for structural logic, use Markdown for content.

## The Semantic Container Principle

Commands are **human-facing shortcuts** that should be simple to read and write. Use XML judiciously - only when structure genuinely helps organize complex content.

## When to Use XML in Commands

**Use XML tags when:**
- **Machine-parsed routing** - Command needs to analyze context and route to workflows
- **Strictly isolated** - Preventing confusion between data and instructions
- **Non-negotiable** - Structural boundaries that must be preserved

**Common XML Containers for Commands:**

- **`<intent_analysis>`** - Analyze command arguments/context to determine appropriate action
- **`<routing>`** - Decision tables mapping context to skills/workflows
- **`<workflow>`** - Non-negotiable step sequences (rare in commands)
- **`<constraints>`** - Critical boundaries (NEVER/MUST NOT)
- **`<output_format>`** - Machine-parseable response structures

## When to Use Pure Markdown

**Default to Pure Markdown when:**
- ✓ Simple, linear command execution
- ✓ Direct skill invocation
- ✓ Single workflow, no complex routing
- ✓ Human-readable instructions preferred

## Command Structure Patterns

### Ultra-Minimal Pattern (Pure Markdown)

**Best for:** Direct skill invocation, simple shortcuts

```markdown
---
description: Debug code using engineering skill
allowed-tools: Skill(engineering)
disable-model-invocation: true
---

Invoke the engineering skill to debug: $ARGUMENTS
```

### Structured Pattern (Pure Markdown)

**Best for:** Multi-step commands with clear sections

```markdown
---
description: Lifecycle manager for toolkit components
allowed-tools: Task
argument-hint: [agent|skill|command|hook] [create|audit] [name]
disable-model-invocation: true
---

## Objective

Perform $2 operation on $1 component: $3

## Process

Task the plugin-expert agent with: $1 $2 $3
```

### Complex Pattern (Hybrid XML/Markdown)

**Best for:** Commands that need intent analysis and routing

```markdown
---
description: Advanced command with intent routing
allowed-tools: Skill, Task, Read
disable-model-invocation: true
---

<intent_analysis>
Analyze the command arguments to determine appropriate action:

- If arguments contain "create" → route to creation workflow
- If arguments contain "audit" → route to audit workflow
- Default → provide usage guidance
</intent_analysis>

<routing>
| Context Indicates | Route To |
|------------------|----------|
| Arguments contain "create" | Plugin-expert with create operation |
| Arguments contain "audit" | Plugin-expert with audit operation |
| Missing or unclear | Usage guidance |

Agent executes routing logic directly.
</routing>
```

## Context Handling

**Dynamic Context (`!` prefix):**
```
Current git status: !git status
```

**File References (`@` prefix):**
```
Review implementation in: @src/utils/helpers.js
```

## Command YAML Frontmatter

**Required fields:**
- `description` - Clear, actionable description shown in command picker

**Common optional fields:**
- `argument-hint` - Usage guidance for command arguments
- `allowed-tools` - Tool restrictions for security
- `disable-model-invocation: true` - For wrapper commands that delegate to agents/skills

## Pattern Selection Checklist

- [ ] Simple shortcut → Ultra-minimal pattern (Pure Markdown)
- [ ] Multi-step process → Structured pattern (Pure Markdown)
- [ ] Needs intent analysis → Complex pattern (Hybrid XML/Markdown)
- [ ] Always prefer Markdown over XML when possible
- [ ] Use XML only when structure genuinely adds value
- [ ] Limit to 3-5 XML tags maximum, no nesting
- [ ] Commands are passive cookbooks - analyze context, don't ask questions

## Best Practices

1. **Start Simple**: Begin with Pure Markdown, add XML only when needed
2. **Human-Facing**: Commands should be readable and intuitive
3. **Passive Execution**: Analyze context, don't solicit user input
4. **Tool Security**: Use `allowed-tools` for restrictions
5. **Delegation Pattern**: Most commands delegate to skills/agents

---

*This content is extracted from the main SKILL.md to comply with progressive disclosure guidelines. Return to the main skill documentation for the full command management workflow.*