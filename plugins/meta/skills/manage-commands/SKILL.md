---
name: manage-commands
description: MUST CONSULT when creating or auditing slash commands to ensure compliance with command structure standards, semantic categorization, and permission patterns.
allowed-tools: Read Write Edit Bash
---

# Command Management Standards

## Essential Principles

1. **Passive Knowledge**: This skill provides standards and does not ask questions. Commands themselves MAY ask questions during Vector intake phases.
2. **Atomic Independence**: Commands do not depend on specific Commands. They are self-contained libraries of knowledge.
3. **Intelligence > Process**: Trust the model to determine execution steps based on standards and templates.
4. **User-Centric Design**: Commands are convenient shortcuts for human users, not programmatic interfaces.

## Capability Index

### Command Standards
**File:** [command-standards.md](references/command-standards.md)
**Use for:** Creating new slash commands, selecting templates, semantic categorization, YAML frontmatter, security patterns.

**Covers:**
- Command structure standards
- Semantic categories (Verbs, Personas, Objects, Execution)
- Template selection criteria
- YAML frontmatter requirements
- User-centric wrapper patterns
- Dynamic context standards
- Security and tool restrictions
- Validation and testing protocols

### Additional References

| Reference | Purpose |
|-----------|---------|
| [syntax-guide.md](references/syntax-guide.md) | Arguments, Frontmatter, and Categories |
| [background-execution.md](references/background-execution.md) | Background execution patterns |
| [permissions-guide.md](references/permissions-guide.md) | Security and tool restrictions |
| [cross-platform.md](references/cross-platform.md) | OS-specific considerations |

## Asset Library

### Templates (`assets/templates/`)

Production-grade templates for command scaffolding:

| Template | Use Case |
|----------|----------|
| `skill-delegator_minimalistic.md` | One-line skill wrapper (default) |
| `skill-delegator_structured.md` | Skill wrapper with structure |
| `agent-delegator.md` | Agent delegation |
| `complex-delegation.md` | Single/Parallel background agents |
| `hybrid-workflow.md` | Foreground + background work |
| `context-loader.md` | Dynamic context loading |

### Examples (`examples/`)

- **[bash-logic.md](examples/bash-logic.md)** - Git commits and deployment gates with dynamic context

## Anti-Patterns

| Pattern | Why Avoid | Alternative |
|---------|-----------|-------------|
| Vague description | Won't discover | Add specific purpose |
| Missing tool restrictions | Security risk | Add allowed-tools |
| No dynamic context | Missing state | Add ! `context` |
| Poor argument integration | Arguments ignored | Use $ARGUMENTS |
| Overly complex | Hard to use | Split into multiple commands |
| Interactive prompts | Breaks async | Make autonomous |

## Validation Protocol

Any command MUST pass:

- [ ] Valid YAML frontmatter
- [ ] Clear, specific description
- [ ] Semantic category selected
- [ ] Proper naming conventions
- [ ] Arguments properly handled
- [ ] Tool restrictions added (if needed)
- [ ] Dynamic context included (if needed)
- [ ] disable-model-invocation set (if wrapper)
- [ ] Tested with real invocation

## Integration Points

### With Skills

Commands invoke skills for domain expertise:
- Use `allowed-tools: Skill({skill-name})`
- Ensure skill exists and is accessible
- Match argument patterns
- Handle skill output appropriately

### With Agents

Commands delegate to agents for complex tasks:
- Use `allowed-tools: Task`
- Ensure agent exists
- Provide comprehensive context
- Handle agent output appropriately

### Between Commands

Commands should avoid calling other commands:
- Each command should be independent
- Use skills/agents instead of command chains
- Prevents circular dependencies

## Best Practices

See `references/command-standards.md` for comprehensive best practices including:
- Command naming conventions
- Argument handling patterns
- Description standards
- Template selection logic

## Continuous Improvement

### Refactoring Triggers

**Consider refactoring when:**
- Command becomes too complex
- Usage patterns change
- New patterns emerge
- Standards evolve

### Refactoring Principles

- Maintain backward compatibility when possible
- Preserve core functionality
- Improve clarity and usability
- Reduce complexity
- Enhance maintainability
