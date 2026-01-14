# Component Guidelines

## Skills Management

### Standards File
**See:** `standards-communication.md` for complete skills standards

### Use Cases
Creating new skills, selecting templates, progressive disclosure, YAML frontmatter, security patterns

### Frontmatter Requirements
- `name`: Component identifier (1-64 chars, lowercase)
- `description`: Purpose and trigger conditions
- `allowed-tools`: Tool restrictions (security)
- `context`: fork or inline (for skills requiring isolation)
- `user-invocable`: Control visibility in / menu (for skills)
- `disable-model-invocation`: Prevent auto-triggering (for commands/skills)

### Template Selection

| Template | Use Case |
|----------|----------|
| `standard-skill.md` | Single-workflow skills (Minimal/Task) |
| `router-pattern.md` | Complex skills with 4+ workflows |
| `progressive-disclosure.md` | Skills requiring references/ subdirectory |
| `reference-file.md` | Reference document formatting |

### Key Principles
- Progressive disclosure for complex skills
- Fork vs inline execution decision matrix
- Security and tool restrictions
- Reference file organization

## Commands Management

### Standards File
**See:** `command-standards.md` for complete command standards

### Essential Principles

#### 1. Command Shortcuts are Standard
A Command that wraps a single Skill (e.g., `allowed-tools: [Skill(name)]`) is a **Recommended Pattern**. It acts as a Zero-Token Shortcut for the user.

#### 2. Redundancy Check (The "Glue" Trap)

**FLAG**: A Command that *re-implements* the logic of a Skill in its prompt. This is code duplication.

**FIX**: Delete the prompt logic and replace it with a call to `Skill(name)`.

**FLAG**: A Command and a Skill with identical descriptions/triggers.

**FIX**: Differentiate them. Logic lives in Skill ("USE when..."), Shortcut lives in Command ("Shortcut for...").

#### 3. Commands Orchestrate Multi-Skill Workflows
Commands are also used to sequence multiple Skills (Macro) or provide "Wizard" style interactions.

### Template Selection

| Template | Use Case |
|----------|----------|
| `read-only-command.md` | Analysis and exploration commands |
| `autonomous-wrapper.md` | Commands that execute without user interaction |
| `interactive-wizard.md` | Commands that guide users through setup |

## Agents Management

### Standards File
**See:** `agent-security.md` for complete agent standards

### Core Principle

**Agents are Primarily Personas for Skills.** When defining an agent, primarily design it to be bound to a Skill via `agent: [name]` in the skill frontmatter.

**Agent Frontmatter Fields:**
- `name`: Agent identifier
- `tools`: Tool whitelist (security - REQUIRED)
- `skills`: Skills to auto-load (optional)
- `description`: Agent role and purpose

**Default to Pure Markdown.** Most agents work well with simple Markdown structure (`## Role`, `## Workflow`, `## Constraints`). Add XML tags only when complexity genuinely requires it.

### Template Selection

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

### SKILL descriptions:
- **MUST** start with "USE when [condition]"
- Natural language only (no XML tags)
- Include specific triggers for discovery
- Use Modal+Condition pattern for high-fidelity matching

### COMMAND descriptions:
- **NO XML**: Do not use `<example>` tags
- Natural Language: Use "USE when [condition]" or semantic action
- Include keywords for fuzzy matching

### AGENT descriptions:
- Include role and trigger conditions
- "MUST Use" for required workers
- "PROACTIVELY Use" for autonomous delegates
