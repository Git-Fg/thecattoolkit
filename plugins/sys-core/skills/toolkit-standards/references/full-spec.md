# Toolkit Registry - Full Specification

## Component Standards

### Skills Management

**Use for:** Creating new skills, selecting templates, progressive disclosure, YAML frontmatter, security patterns.

**Template Selection:**
- `standard-skill.md` - Single-workflow skills
- `router-pattern.md` - Complex skills with 4+ workflows
- `progressive-disclosure.md` - Skills with references/ subdirectory

### Commands Management

**Essential Principles:**

1. **Command Shortcuts are Standard** - Wrapping a single Skill is recommended
2. **Redundancy Check** - Avoid duplicating Skill logic in Commands
3. **Multi-Skill Orchestration** - Sequence multiple Skills

**Template Selection:**
- `read-only-command.md` - Analysis and exploration
- `autonomous-wrapper.md` - Autonomous execution
- `interactive-wizard.md` - User-guided workflows

### Agents Management

**Core Principle:** Agents are primarily personas for Skills, bound via `agent:` field.

**Template Selection:**
- `universal-agent.md` - Core/Specialized/Research agents (Default)
- `coordinator-agent.md` - Multi-step orchestration
- `background-safe-agent.md` - Read-only background execution

## File Structure Priority

| Type | Location | Priority | Scope |
|:-----|:---------|:---------|:------|
| **Project** | `.claude/` | Highest | Current project only, portable |
| **User** | `~/.claude/` | Medium | All projects |
| **Plugin** | Plugin directories | Lowest | All projects |

## Anti-Patterns

| Pattern | Why Avoid | Alternative |
|:--------|:----------|:------------|
| **Vague description** | Won't discover | Use "USE when [condition]" |
| **Logic Duplication** | Maintenance nightmare | Delegate to Skill |
| **Missing tool restrictions** | Security risk | Add `allowed-tools` |
| **AskUser in workers** | Background deadlocks | Read-only tools only |

## Description Standards (Law 4)

### SKILL descriptions:
- **MUST** start with "USE when" or "MUST" or "PROACTIVELY"
- Natural language only (no XML tags)
- Include specific triggers for discovery

### COMMAND descriptions:
- **NO XML**: Natural language only
- Use "USE when [condition]" or semantic action
- Must have `disable-model-invocation: true`
- Must have `argument-hint:`

### AGENT descriptions:
- Include role and trigger conditions
- "MUST USE" for required workers

## Validation

Any component MUST pass validation:

**Skills:** YAML frontmatter, description starts with "USE when", `allowed-tools`, progressive disclosure

**Commands:** YAML frontmatter, orchestrates 2+ Skills, clear description, tested invocation

**Agents:** YAML frontmatter, tool restrictions, well-structured prompt, no AskUser in workers

## Examples

### Skill Router Pattern
Delegates to sub-skills based on code analysis

### Command Orchestration
Multi-skill workflows with dynamic context

### Background-Safe Agent
Read-only execution for background tasks

## Standards Documentation

**Component Guidelines:**
- `references/component-guidelines.md` - Skills, Commands, Agents management
- `references/validation.md` - Validation protocol and best practices
- `references/examples.md` - Working examples and anti-patterns

**Standards Documentation:**
- `references/standards-communication.md` - Common principles
- `references/command-standards.md` - Command-specific standards
- `references/agent-security.md` - Agent security guidelines
- `references/standards-security.md` - Background execution and permissions
