# Command Standards: Orchestration Layer

## 1. Philosophy: Commands Orchestrate Multi-Skill Workflows

**IMPORTANT:** With the Unified Skill Capability model, most simple tasks no longer require Command wrappers. Make your Skill user-invocable (default) with `context: fork` instead.

Commands are **Orchestration Layer** components that manage multi-phase workflows by sequencing multiple Skills together.

**The Pattern:**
1. **Gather Context:** Use `!bash` to get ground truth from the environment
2. **Capture Intent:** Inject user's natural language via `$ARGUMENTS`
3. **Orchestrate:** Sequence multiple Skills to complete complex workflows

**When to Use Commands:**
- Multi-phase workflows (Skill A → Skill B → Skill C)
- Need `argument-hint` for UI documentation
- Complex orchestration requiring decision trees

**When NOT to Use Commands:**
- Single atomic task → Use Forked Skill instead
- Wrapping one Skill → Use Forked Skill instead

---

## 2. Anatomy of a Command

Location: `plugins/<plugin-name>/commands/<command-name>.md`

```markdown
---
description: Natural language description for AI discovery
argument-hint: [string]  # Optional: UI documentation hint only
---

# Context
!git diff --staged
!ls -R src/

# Instructions
Based on the context above, analyze the changes and $ARGUMENTS.

Launch agents in parallel if needed to handle complexity.
```

### The Feature Dev Pattern (Complex Orchestration)

```markdown
---
description: Orchestrate full feature development workflow
argument-hint: [feature-description]
---

# Context
!git status
!cat ROADMAP.md

# Instructions
Orchestrate the feature development workflow for: $ARGUMENTS

Phase 1: Design Analysis
- Use skill: architecture-review
- Analyze requirements and existing patterns

Phase 2: Implementation Planning
- Use skill: code-generator
- Generate implementation plan with tests

Phase 3: Code Generation
- Use skill: implementation-expert
- Generate code following project standards

Phase 4: Testing
- Use skill: test-validator
- Generate comprehensive tests

Phase 5: Documentation
- Use skill: doc-generator
- Update documentation

Synthesize all phases into a cohesive feature implementation.
```

**Simple tasks** (like commit messages) should now use Forked Skills instead of Commands.

---

## 3. Rules & Standards

### Use `$ARGUMENTS` for Everything
Native intelligence parses "fix the login button" better than rigid parsing.

```markdown
# Good
Launch an agent to fix $ARGUMENTS

# Bad - rigid positional parsing
Arg 1: $1 (file path)
Arg 2: $2 (action)
```

### Use Markdown for Structure
Commands use **Markdown headers** for structure, not XML tags.

```markdown
# Good
## Context
## Instructions
## Constraints

# Bad - XML for structure
<context>...</context>
<assignment>...</assignment>
```

### Orchestration Patterns

**Multi-Skill Orchestration:**
```markdown
Orchestrate a security audit of the codebase:

Phase 1: Architecture Analysis
- Use skill: security-scanner (context: fork)
- Scan for common vulnerabilities

Phase 2: Deep Analysis
- Use skill: vulnerability-expert (context: fork)
- Analyze specific vulnerability patterns

Phase 3: Compliance Check
- Use skill: compliance-validator (context: fork)
- Verify against security standards

Phase 4: Report Generation
- Use skill: report-generator (context: fork)
- Synthesize findings into actionable report

Each skill runs independently in forked context. Commands orchestrate the sequence.
```

**Parallel Skill Execution:**
```markdown
Launch skills in parallel to audit different components:

- Use skill: api-security-scanner (context: fork)
- Use skill: auth-security-scanner (context: fork)
- Use skill: db-security-scanner (context: fork)
- Use skill: utils-security-scanner (context: fork)

Each skill reports independently. Synthesize findings after all complete.
```

Commands now orchestrate **Skills** (not agents) in the unified model.

---

## 4. Tool Restrictions

Commands can use `allowed-tools` frontmatter to enforce safety or focus:

```yaml
---
description: Read-only codebase explorer
allowed-tools: [Read, Grep, Glob]
---
```

This restriction cascades: subagents spawned via `Task` inherit these restrictions.

---

## 5. Command Types

| Type | Consumer | `disable-model-invocation` | AskUserQuestion |
|:-----|:---------|:---------------------------|:----------------|
| User-Centric | Human only | `true` | Yes |
| Agent-Ready | Specialized Agents | `false` | No |
| Hybrid | Both | `false` | Conditional |

---

## 6. Valid Frontmatter Fields

```yaml
---
description: "Natural language description for AI discovery"  # Required
argument-hint: "[description]"  # Optional: UI hint only
allowed-tools: [Read, Grep, Task]  # Optional: restrict tools
disable-model-invocation: true  # Optional: prevent Skill tool invocation
model: sonnet  # Optional: model to use (sonnet, opus, haiku, or 'inherit')
permissionMode: plan  # Optional: permission mode (default, acceptEdits, dontAsk, bypassPermissions, plan, ignore)
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
---
```

## 7. Command Permission Security

### Safe Command Examples

```yaml
# Safe read-only command
---
description: "Analyze project structure"
argument-hint: "[path]"
allowed-tools: [Read, Grep]
permissionMode: plan  # Read-only mode
---
# Analysis will be read-only, preventing accidental modifications

# Safe git command with specific operations
---
description: "Git operations for project maintenance"
argument-hint: "[operation]"
allowed-tools:
  - Bash(git status:*)
  - Bash(git add:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git branch:*)
permissionMode: dontAsk  # Auto-deny dangerous operations
model: haiku
---
# Only allows specific git commands, auto-denies everything else

# Dangerous command (should be avoided)
---
description: "Execute any bash command"
allowed-tools: [Bash]  # ❌ DANGEROUS - allows ANY bash command
permissionMode: bypassPermissions  # ❌ VERY DANGEROUS - bypasses safety
---
```

### Command Permission Patterns

```yaml
# Development command with safety checks
---
description: "Development helper for code analysis"
allowed-tools:
  - Read
  - Grep
  - Bash(npm test:*)
  - Bash(npm run build:*)
  - Bash(python -m pytest:*)
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate-dev-command.sh $TOOL_INPUT"
          timeout: 60
---

# Production deployment command (maximum safety)
---
description: "Production deployment operations"
allowed-tools:
  - Bash(docker-compose up:*)
  - Bash(docker-compose down:*)
  - Bash(./deploy.sh:*)
permissionMode: dontAsk  # Auto-deny unless explicitly pre-approved
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./production-validate.sh $TOOL_INPUT"
          timeout: 300
---
```
