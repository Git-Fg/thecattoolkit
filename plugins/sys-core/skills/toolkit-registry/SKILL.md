---
name: toolkit-registry
description: "MUST USE when creating, auditing, or managing plugin components (Skills, Commands, Agents). System Authority on 2026 Universal Agentic Runtime standards for all plugin components."
context: fork
agent: plugin-expert
allowed-tools: [Read, Write, Edit, Bash(ls:*), Bash(grep:*), Bash(cat:*), Bash(find:*), Glob, Grep]
---

# Toolkit Registry Standards

## Purpose

System Authority for managing all plugin components (Skills, Commands, Agents) following 2026 Universal Agentic Runtime standards.

## Quick Reference

| Component | Purpose | Entry Trigger |
|:----------|:--------|:--------------|
| **Skills** | Knowledge injection, reusable workflows | "Create a skill for X", "Audit skill Y" |
| **Commands** | Orchestration shortcuts, multi-skill workflows | "Create a command for X", "Audit command Y" |
| **Agents** | Persona binding, isolated context execution | "Create an agent for X", "Audit agent Y" |

## Shared Standards

For common principles, integration patterns, and anti-patterns, see:
- **[standards-communication.md](references/standards-communication.md)** - Common standards for all components

## Component Standards

### Skills Management

**Standards File:** `references/standards-communication.md`
**Use for:** Creating new skills, selecting templates, progressive disclosure, YAML frontmatter, security patterns.

**Covers:**
- Frontmatter requirements (name, description, allowed-tools, model, context, agent)
- Discovery optimization (Modal+Condition pattern)
- Progressive disclosure for complex skills
- Fork vs inline execution decision matrix
- Security and tool restrictions
- Reference file organization

**Template Selection:**

| Template | Use Case |
|----------|----------|
| `standard-skill.md` | Single-workflow skills (Minimal/Task) |
| `router-pattern.md` | Complex skills with 4+ workflows |
| `progressive-disclosure.md` | Skills requiring references/ subdirectory |
| `reference-file.md` | Reference document formatting |

### Commands Management

**Standards File:** `references/command-standards.md`
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

**Essential Principles:**

1.  **Command Shortcuts are Standard:** A Command that wraps a single Skill (e.g., `allowed-tools: [Skill(name)]`) is a **Recommended Pattern**. It acts as a Zero-Token Shortcut for the user.

2.  **Redundancy Check (The "Glue" Trap):**
    -   **FLAG**: A Command that *re-implements* the logic of a Skill in its prompt. This is code duplication.
    -   **FIX**: Delete the prompt logic and replace it with a call to `Skill(name)`.
    -   **FLAG**: A Command and a Skill with identical descriptions/triggers.
    -   **FIX**: Differentiate them. Logic lives in Skill ("USE when..."), Shortcut lives in Command ("Shortcut for...").

3.  **Commands Orchestrate Multi-Skill Workflows:** Commands are also used to sequence multiple Skills (Macro) or provide "Wizard" style interactions.

**Template Selection:**

| Template | Use Case |
|----------|----------|
| `read-only-command.md` | Analysis and exploration commands |
| `autonomous-wrapper.md` | Commands that execute without user interaction |
| `interactive-wizard.md` | Commands that guide users through setup |

### Agents Management

**Standards File:** `references/agent-security.md`
**Use for:** Creating new agents, selecting templates, persona binding, background execution safety.

**Covers:**
- Frontmatter requirements (see Agent Security reference for full specification)
- Persona binding for Skills
- Background execution safety
- Tool permissions and least privilege
- AskUserQuestion guidelines

**Core Principle:**

**Agents are Primarily Personas for Skills.** When defining an agent, primarily design it to be bound to a Skill via `agent: [name]` in the skill frontmatter.

**Default to Pure Markdown.** Most agents work well with simple Markdown structure (`## Role`, `## Workflow`, `## Constraints`). Add XML tags only when complexity genuinely requires it.

**Template Selection:**

| Template | Use Case |
|----------|----------|
| `universal-agent.md` | Core, Specialized, or Research agents (Default) |
| `coordinator-agent.md` | Multi-step orchestration |
| `explorer-agent.md` | Read-only code exploration |
| `background-safe-agent.md` | Read-only agents for background execution |

## File Structure Priority

| Type | Location | Scope | Priority |
|:-----|:---------|:------|:----------|
| **Project** | `.claude/` | Current project only, portable | Highest |
| **User** | `~/.claude/` | All projects | Medium |
| **Plugin** | Plugin's directories | All projects | Lowest |

Project-level components override user-level when names conflict.

## Asset Library

### Templates (`assets/templates/`)

Production-grade templates for component scaffolding:

**Skill Templates:**
- `standard-skill.md` - Single-workflow skills
- `router-pattern.md` - Complex skills with 4+ workflows
- `progressive-disclosure.md` - Skills requiring references/ subdirectory
- `reference-file.md` - Reference document formatting

**Command Templates:**
- `read-only-command.md` - Analysis and exploration
- `autonomous-wrapper.md` - Autonomous execution
- `interactive-wizard.md` - User-guided workflows

**Agent Templates:**
- `universal-agent.md` - Core/Specialized/Research agents
- `coordinator-agent.md` - Multi-step orchestration
- `explorer-agent.md` - Read-only exploration
- `background-safe-agent.md` - Background-safe execution

### References (`references/`)

Consolidated standards and documentation:

| Reference | Purpose |
|:----------|:--------|
| `standards-communication.md` | Skill creation, auditing, and communication patterns |
| `command-standards.md` | Command creation and auditing |
| `agent-security.md` | Agent creation, auditing, and security |
| `standards-security.md` | Background execution, tool permissions |

### Examples (`examples/`)

Ready-to-use canonical patterns:

- `router-pattern.md` - Code analysis router demonstrating delegator pattern
- `bash-logic.md` - Git commits and deployment gates with dynamic context
- `background-safe-agent.md` - Read-only code explorer (Background Safe)

## Anti-Patterns

| Pattern | Why Avoid | Alternative |
|:--------|:----------|:------------|
| **Vague description** | Won't discover | Add specific purpose with "USE when" |
| **XML in description** | Violates Law 4 | Natural Language + USE triggers |
| **Logic Duplication** | Code rot, maintenance nightmare | Delegate to Skill via `allowed-tools` |
| **Missing tool restrictions** | Security risk | Add `allowed-tools` whitelist |
| **AskUser in worker agents** | Background deadlocks | Remove from worker `tools` whitelist |
| **Overly complex** | Hard to use | Split into multiple components |
| **Interactive prompts in forked skills** | Breaks async | Make autonomous |

## Description Standards (Law 4)

**SKILL descriptions:**
- **MUST** start with "USE when [condition]"
- Natural language only (no XML tags)
- Include specific triggers for discovery
- Use Modal+Condition pattern for high-fidelity matching

**COMMAND descriptions:**
- **NO XML**: Do not use `<example>` tags
- Natural Language: Use "USE when [condition]" or semantic action
- Include keywords for fuzzy matching

**AGENT descriptions:**
- Include role and trigger conditions
- "MUST USE" for required workers
- "PROACTIVELY USE" for autonomous delegates

## Validation Protocol

Any component MUST pass:

**Skills:**
- [ ] Valid YAML frontmatter
- [ ] Description starts with "USE when"
- [ ] `allowed-tools` specified (or explicitly omitted)
- [ ] Templates selected correctly
- [ ] Progressive disclosure applied if complex
- [ ] References organized in `references/`

**Commands:**
- [ ] Valid YAML frontmatter
- [ ] Orchestrates 2+ distinct Skills (not single-skill wrapper)
- [ ] Clear, specific description
- [ ] Semantic category selected
- [ ] Tool restrictions added (if needed)
- [ ] Tested with real invocation

**Agents:**
- [ ] Valid YAML frontmatter
- [ ] Description optimized for routing
- [ ] Tool restrictions (least privilege)
- [ ] Well-structured system prompt
- [ ] Model selection appropriate
- [ ] AskUserQuestion only in coordinators, not workers

## Working Examples

### Skill Router Pattern

See `examples/router-pattern.md` for a canonical example of a skill that:
- Analyzes code to determine workflow
- Delegates to appropriate sub-skills
- Uses progressive disclosure

### Command Orchestration

See `examples/bash-logic.md` for a command that:
- Executes git operations
- Runs deployment gates
- Uses dynamic context

## Best Practices

### For Skills
1. **Inline-First:** Default to inline execution for quota efficiency
2. **Fork Only When:** Task exceeds context window OR strict isolation needed
3. **Progressive Disclosure:** Keep SKILL.md < 400 lines, move details to `references/`
4. **Template-Driven:** Always use templates from `assets/templates/`

### For Commands
1. **Multi-Skill Orchestration:** Commands should sequence 2+ skills
2. **User-Centric:** Design for human convenience, not programmatic APIs
3. **Autonomous Execution:** Avoid interactive prompts; make decisions automatically
4. **Argument Integration:** Use `$ARGUMENTS` for user input

### For Agents
1. **Persona Binding:** Design agents to be bound to Skills via `agent:` field
2. **Least Privilege:** Specify `tools` whitelist for security
3. **Background Safety:** Read-only tools (Read, Grep, Glob) for background execution
4. **No AskUser in Workers:** Remove `AskUserQuestion` from worker agent `tools`

## Integration Points

- **standards-communication.md** - Common principles for all components
- **scaffold-component** - Natural language to component generation
- **meta-builder** - Live documentation fetching for compliance
- **validate-toolkit** - Comprehensive testing and validation

## Continuous Improvement

### Refactoring Triggers

**Consider refactoring when:**
- Component becomes too complex
- Usage patterns change
- New patterns emerge
- Standards evolve

### Refactoring Principles

- Enforce clean breaks over backward compatibility (Codebase > History)
- Preserve core functionality
- Improve clarity and usability
- Reduce complexity
- Enhance maintainability
