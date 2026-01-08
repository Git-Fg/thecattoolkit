# Command Creation Standards

## Overview

This document defines the standards for creating Cat Toolkit slash commands that enable users to trigger reusable prompts with `/command-name` syntax.

## Command Structure Standards

### Ultra-Minimalist Pattern (Default)

**Best for:** Most commands

```yaml
---
description: {Brief, human-friendly description}
argument-hint: [{optional argument description}]
---

{One-line instruction}
```

**Example:**
```yaml
---
description: Optimize code performance
---

Optimize the code for better performance
```

### Structured Pattern (When Needed)

**Use when:** Multi-step workflows, clear success criteria needed

```yaml
---
description: Review code for security issues
---

## Objective
Review code for security vulnerabilities

## Process
1. Scan for common vulnerabilities
2. Check input validation
3. Verify authentication

## Success Criteria
- All critical issues identified
- Remediation steps provided
```

### Advanced Pattern (Context-Dependent)

**Use when:** Dynamic context needed, tool restrictions required

```yaml
---
description: Create git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

## Context
Current git status: ! `git status`

## Objective
Create a well-structured git commit

## Process
1. Review changes
2. Write message
3. Execute commit
```

## Semantic Categories

### Category Selection

| Category | Naming Pattern | Purpose | Examples |
|----------|---------------|---------|----------|
| **Verbs** | Action words | Invoke skills | `/think`, `/debug`, `/analyze` |
| **Personas** | Role names | Delegate to agents | `/brainstorm`, `/expert`, `/reviewer` |
| **Objects** | Thing names | Lifecycle management | `/plan`, `/hook`, `/skill` |
| **Execution** | Runner pattern | Execute artifacts | `/run-plan`, `/run-prompt`, `/deploy` |

### Categorization Logic

1. **Invokes skill directly** → Use **Verbs** category
2. **Delegates to agent** → Use **Personas** category
3. **Manages lifecycle or artifacts** → Use **Objects** category
4. **Executes or runs artifacts** → Use **Execution** category

### Naming Standards

**Good names:**
- `optimize` - Clear action
- `create-plan` - Clear action and output
- `code-review` - Clear purpose
- `git-commit` - Specific operation

**Poor names:**
- `helper` - Too generic
- `stuff` - Not descriptive
- `my-command` - Not informative

## YAML Frontmatter Standards

### Required Fields

```yaml
---
description: {Clear, actionable description}
---
```

### Optional Fields

```yaml
---
argument-hint: [{input description}]  # If command uses arguments
allowed-tools: [Tool1, Tool2]         # For security restrictions
disable-model-invocation: true        # For user-centric wrappers
---
```

### Description Standards

**Strong language patterns:**
- **MUST**: Critical/essential commands
- **PROACTIVE**: Recommended commands
- **CONSULT**: Reference/expert commands

**Formula:** `{Action} + {Context}`

**Examples:**
```
description: Create git commits following conventional format
description: Audit code for security vulnerabilities
description: Generate comprehensive test suites
```

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

## Template Selection

### Template Decision Matrix

| Template | Use Case | Complexity |
|----------|----------|------------|
| `skill-delegator_minimalistic.md` | Skill wrapper, one-line | Low |
| `skill-delegator_structured.md` | Skill wrapper with structure | Medium |
| `agent-delegator.md` | Agent delegation | Low |
| `background-agent-delegator.md` | Long-running background tasks | Medium |
| `parallel-fan-out.md` | Multiple parallel agents | High |
| `context-loader.md` | Dynamic context loading | Medium |
| `argument-handler.md` | Positional arguments | Low |
| `hybrid-workflow.md` | Foreground + background | High |

### Background Execution Patterns

**Use background agent delegator when:**
- Task is long-running (minutes+)
- User wants to continue working during execution
- Agent is read-only (safe for background)
- Task doesn't require user interaction

**Use parallel fan-out when:**
- Multiple independent tasks need processing
- Tasks can run simultaneously
- Results can be synthesized together

**Use regular agent delegator when:**
- Task is quick (seconds)
- User needs to see results immediately
- Task requires user interaction

## User-Centric Wrapper Commands

### disable-model-invocation Flag

**For ALL wrapper commands** (skill wrappers AND agent wrappers):

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

### Wrapper Examples

**Skill Wrapper (Minimalistic):**
```yaml
---
description: [Verbs] Shortcut to invoke the {skill} skill for {purpose}
allowed-tools: Skill({skill})
argument-hint: [{arg hint}]
disable-model-invocation: true
---

Invoke the `{skill}` skill to {action}: $ARGUMENTS
```

**Agent Wrapper:**
```yaml
---
description: [Personas] Delegate to {agent} for {purpose}
allowed-tools: Task
argument-hint: [{task description}]
disable-model-invocation: true
---

Task the `{agent}` agent with: $ARGUMENTS
```

## Minimalistic vs Structured Decision

### Default to Minimalistic

**Use minimalistic when:**
- ✅ Skill is self-documenting
- ✅ Single clear purpose
- ✅ Skill is well-established
- ✅ You value speed over ceremony
- ✅ Skill changes frequently

**Example:**
```yaml
---
description: Invoke thinking skill for complex analysis
allowed-tools: Skill(thinking-frameworks)
disable-model-invocation: true
---

Invoke the thinking-frameworks skill for: $ARGUMENTS
```

### Use Structured Only When

**Use structured when:**
- ⚠️ Skill has complex pre-work
- ⚠️ Skill is new/unknown to users
- ⚠️ Success criteria are non-obvious
- ⚠️ Skill creates artifacts
- ⚠️ Users need mental preparation

**Example:**
```yaml
---
description: Create project architecture plan
allowed-tools: Skill(create-plans)
argument-hint: [project description]
disable-model-invocation: true
---

## Objective
Create a comprehensive architecture plan for: $ARGUMENTS

## Process
1. Analyze project requirements
2. Identify components and relationships
3. Generate architecture diagram
4. Document technical decisions

## Success Criteria
- Complete architecture specification
- Visual diagram included
- Technology choices justified
```

## Directory Structure Standards

### Default: Project-Level

**Location:** `.claude/commands/`
**Advantages:** Portable, version-controlled, team-shared

```bash
# Create command file
cat > .claude/commands/{command-name}.md << 'EOF'
---
description: {description}
---

{instruction}
EOF
```

### Alternative: User-Level

**Location:** `~/.claude/commands/`
**Use case:** Only if explicitly requested for global availability

```bash
# Create global command
cat > ~/.claude/commands/{command-name}.md << 'EOF'
---
description: {description}
---

{instruction}
EOF
```

## Dynamic Context Standards

### When to Use Dynamic Context

**Use `!` prefix for:**
- State-dependent commands (git status, environment)
- File system queries (file listings, searches)
- API calls (current data fetching)
- External state (database queries, service status)

**Example:**
```yaml
---
description: Create git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

## Context
Current git status: ! `git status`
Recent changes: ! `git diff HEAD`

## Objective
Create a well-structured git commit

## Process
1. Review the git status
2. Stage relevant changes
3. Write commit message
4. Execute commit
```

### When NOT to Use Dynamic Context

**Skip dynamic context for:**
- Simple, state-independent operations
- Commands that don't need current state
- Performance-critical commands
- Read-only reference commands

## Security Standards

### Tool Restrictions

**Security-sensitive operations require `allowed-tools`:**

| Operation Type | Restriction Pattern |
|----------------|-------------------|
| Git operations | `Bash(git add:*)`, `Bash(git commit:*)` |
| Read-only analysis | `Read`, `Grep`, `Glob` only |
| Deployment | Specific deployment tools only |
| File operations | `Bash(touch:*)`, `Bash(mkdir:*)` |

**Why:**
- Limits scope for dangerous operations
- Prevents unintended side effects
- Enables security auditing

### Destructive Operations

**Flag or prevent dangerous actions:**

```yaml
---
description: Push changes to remote repository
allowed-tools: Bash(git push:*)
---

⚠️ **WARNING:** This will push changes to remote repository.

Review changes before pushing:
! `git diff origin/main`

Proceed only if changes are intended.
```

## Validation Standards

### Pre-Creation Checklist

- [ ] YAML frontmatter valid
- [ ] Description is clear and specific
- [ ] Semantic category selected
- [ ] Naming follows conventions
- [ ] Arguments properly handled
- [ ] Tool restrictions added (if needed)
- [ ] Dynamic context included (if needed)
- [ ] disable-model-invocation set (if wrapper)
- [ ] Tested with real invocation

### Post-Creation Testing

**Test command with:**
1. No arguments (if applicable)
2. Valid arguments
3. Invalid arguments
4. Edge cases
5. Integration with dependent components

## Integration Standards

### Command-Skill Integration

**When command invokes skill:**
- Use `allowed-tools: Skill({skill-name})`
- Ensure skill exists and is accessible
- Match argument patterns
- Handle skill output appropriately

### Command-Agent Integration

**When command delegates to agent:**
- Use `allowed-tools: Task`
- Ensure agent exists
- Provide comprehensive context
- Handle agent output appropriately

### Command-Command Integration

**Commands should avoid calling other commands:**
- Each command should be independent
- Use skills/agents instead of command chains
- Prevents circular dependencies

## Common Patterns

### Git Commands

**Commit command:**
```yaml
---
description: Create git commit following conventions
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

## Context
Current git status: ! `git status`

## Objective
Create a conventional commit message

## Process
1. Review changes
2. Stage files
3. Write message (type(scope): description)
4. Commit
```

### Analysis Commands

**Security review:**
```yaml
---
description: Review code for security vulnerabilities
allowed-tools: Read, Grep, Glob
---

## Objective
Identify security issues in: $ARGUMENTS

## Process
1. Scan for common vulnerabilities
2. Check input validation
3. Verify authentication
4. Assess authorization

## Success Criteria
- All critical issues found
- Severity levels assigned
- Remediation steps provided
```

### Generation Commands

**Test generation:**
```yaml
---
description: Generate comprehensive test suite
allowed-tools: Skill(test-generation)
---

## Objective
Create tests for: $ARGUMENTS

## Process
1. Analyze code structure
2. Identify test scenarios
3. Generate test cases
4. Add assertions

## Success Criteria
- All functions covered
- Edge cases included
- Tests are runnable
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Alternative |
|--------------|--------------|-------------|
| Vague description | Won't discover | Add specific purpose |
| Missing tool restrictions | Security risk | Add allowed-tools |
| No dynamic context | Missing state | Add ! `context` |
| Poor argument integration | Arguments ignored | Use $ARGUMENTS |
| Overly complex | Hard to use | Split into multiple commands |
| Interactive prompts | Breaks async | Make autonomous |
| Giant command file | Hard to maintain | Use skill/agent |

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

## Documentation Standards

### When to Document

**Document commands when:**
- Complex behavior
- Non-obvious usage
- Multiple modes
- Security considerations

### Documentation Format

**Include in command:**
- Clear description
- Usage examples
- Argument explanations
- Expected outputs

**External documentation:**
- README with command index
- Usage guides
- Examples repository
