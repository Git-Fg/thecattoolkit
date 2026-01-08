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
**File:** `references/command-standards.md`
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
| `ultra-minimalist-commands.md` | Minimal command patterns |
| `semantic-categories.md` | Naming and categorization |
| `patterns.md` | Common patterns and examples |
| `background-patterns.md` | Background execution patterns |
| `tool-restrictions.md` | Security and permission patterns |
| `arguments.md` | Argument handling patterns |
| `cross-platform.md` | OS-specific considerations |
| `frontmatter.md` | YAML frontmatter specifications |
| `xml-markdown-decision-framework.md` | Prompt formatting guidance |

## Asset Library

### Templates (`assets/templates/`)

Production-grade templates for command scaffolding:

| Template | Use Case |
|----------|----------|
| `skill-delegator_minimalistic.md` | One-line skill wrapper (default) |
| `skill-delegator_structured.md` | Skill wrapper with structure |
| `agent-delegator.md` | Agent delegation |
| `background-agent-delegator.md` | Long-running background tasks |
| `parallel-fan-out.md` | Multiple parallel agents |
| `hybrid-workflow.md` | Foreground + background work |
| `context-loader.md` | Dynamic context loading |
| `argument-handler.md` | Positional arguments |

## Working Examples

Ready-to-use patterns can be found in the `examples/` directory:

| Example | Description |
|---------|-------------|
| **[git-commit-full.md](examples/git-commit-full.md)** | Commit with full context (status, diff, logs) |
| **[performance-optimization.md](examples/performance-optimization.md)** | Analyze code performance |
| **[security-review.md](examples/security-review.md)** | Scan for vulnerabilities |
| **[fix-issue.md](examples/fix-issue.md)** | Systematically fix issues with workflow |
| **[feature-workflow.md](examples/feature-workflow.md)** | End-to-end feature development |
| **[background-agent.md](examples/background-agent.md)** | Run analysis in background |
| **[parallel-fan-out.md](examples/parallel-fan-out.md)** | Run multiple background agents |
| **[project-health.md](examples/project-health.md)** | Dynamic environment loading |

### User-Centric Wrapper Commands

**For ALL wrapper commands** (skill AND agent wrappers):

```yaml
---
disable-model-invocation: true
---
```

**What it does:**
- Prevents SlashCommand tool from programmatically invoking
- Removes command metadata from context
- Still allows manual invocation via `/command-name`

**Why use it:**
- AI can already use Skill/Task tools directly
- Wrapper commands are convenience for human users
- Prevents unnecessary context loading

**When to use:**
- ✅ Skill wrappers (Verbs, Objects, Execution)
- ✅ Agent wrappers (Personas)
- ❌ Commands that need programmatic invocation

### Dynamic Context Standards

**Use `!` prefix for state-dependent commands:**
- Git status: `! `git status``
- File listings: `! `find . -name "*.py"``
- Environment variables: `! `echo $PATH``

**Example:**
```yaml
---
description: Create git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

## Context
Current git status: ! `git status`

## Objective
Create a well-structured git commit
```

### Security Standards

**Security-sensitive operations require `allowed-tools`:**

| Operation Type | Restriction Pattern |
|----------------|-------------------|
| Git operations | `Bash(git add:*)`, `Bash(git commit:*)` |
| Read-only analysis | `Read`, `Grep`, `Glob` only |
| Deployment | Specific deployment tools only |

### Minimalistic vs Structured Decision

**Default to minimalistic when:**
- ✅ Skill is self-documenting
- ✅ Single clear purpose
- ✅ Skill is well-established
- ✅ You value speed over ceremony
- ✅ Skill changes frequently

**Use structured only when:**
- ⚠️ Skill has complex pre-work
- ⚠️ Skill is new/unknown to users
- ⚠️ Success criteria are non-obvious
- ⚠️ Skill creates artifacts
- ⚠️ Users need mental preparation

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

### Command Naming

**Good names:**
- `optimize` - Clear action
- `create-plan` - Clear action and output
- `code-review` - Clear purpose
- `git-commit` - Specific operation

**Poor names:**
- `helper` - Too generic
- `stuff` - Not descriptive
- `my-command` - Not informative

### Argument Handling

**$ARGUMENTS (simple, default):**
```yaml
---
argument-hint: [code or file to review]
---

Review $ARGUMENTS for security issues
```

**$1, $2, $3 (structured input):**
```yaml
---
argument-hint: [operation] [target] [options]
---

Perform $1 on $2 with options: $3
```

### Description Standards

**Strong language patterns:**
- Clear action verbs (Create, Review, Optimize, Analyze)
- Specific context (git commits, code security, performance)
- Avoid vague terms (helps with, assists with, useful for)

**Examples:**
```
description: Create git commits following conventional format
description: Review code for security vulnerabilities
description: Generate comprehensive test suites
```

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
