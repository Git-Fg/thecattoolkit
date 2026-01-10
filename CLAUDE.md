# CLAUDE.md

Primary operating system for Claude Code. This document defines the **Universal Agentic Runtime**—the hierarchical architecture where **Command (Intent) → Agent (Autonomy) → Skill (Protocol)**.

---

# PART I: PARADIGM

## 1.1 The Orchestration Runtime

The toolkit operates as an **Orchestration Runtime** optimized for the Claude Code protocol.
- **The Model** is the CPU (Claude, GLM, MiniMax).
- **The Context** is the RAM.
- **The Components (Commands/Agents/Skills)** are the Software.

We program with **Intent**, not scripts. Instead of `for file in files`, instruct: *"Launch 3 code-explorer agents in parallel to audit the `src/` directory."*

---

## 1.2 The Unified Capability Architecture

| Component | Role | Native Mechanic |
|:----------|:-----|:----------------|
| **Skill** | **Atomic Capability** | Auto-discoverable via semantic matching. Can be `user-invocable`, `context: fork`, and `agent: [name]` bound. |
| **Command** | **Orchestrator** | Manages multi-phase workflows by sequencing multiple Skills. |
| **Agent** | **Persona** | Reusable identity/tools that Skills can bind to via `agent: [name]`. |

---

## 1.3 Core Pillars

### Pillar 1: Plugin Portability
**Intra-Plugin Collaboration, Inter-Plugin Independence:** Components within the same plugin should collaborate freely. Agents can reference skill scripts, and skills can delegate to plugin agents. However, **cross-plugin coupling is forbidden**—each plugin must be fully functional standalone. Domain expertise lives in Skills; Agents reference their plugin's skills via the `skills` field or natural language (not hardcoded paths to other plugins).

### Pillar 2: Atomic Capabilities with Hybrid Execution
Skills have dual nature: **passive knowledge** (auto-discovered) and **active execution** (via `context: fork` or user invocation). Commands orchestrate multi-skill workflows only—never wrap a single Skill.
*Note: `AskUserQuestion` is **strongly discouraged** in Skills to promote composability, but allowed for inherently interactive tasks (e.g., wizards).*

### Pillar 3: Native Delegation
**"Never write in code what can be described in intent."**

| Anti-Pattern | Native Pattern |
|:-------------|:---------------|
| `find . -name "*.ts" -exec grep "todo" {} \;` | "Find all TypeScript files containing TODO comments" |
| Command wrapping single Skill | Forked Skill with `context: fork` |
| "Run find src -name '*.js'" | "Locate source files using filesystem tools" |

**Skill Invocation Priority:**
1. **Prefer `context: fork`:** When a skill needs isolated execution, forked skills auto-execute with their own context
2. **Manual `Skill()` is valid:** Commands and agents can explicitly call `Skill(/skill-name)` when orchestrating workflows
3. **Passive `skills` field:** For knowledge injection without execution (agent references skill patterns)

> [!NOTE]
> Manual `Skill()` loading is **not an anti-pattern**. The priority is about choosing the right mechanism: fork for isolation, explicit call for orchestration, passive field for knowledge.

**Delegation Flow:**
1. **Atomic task** → Forked Skill (`context: fork`)
2. **Multi-phase workflow** → Command orchestrating multiple Skills
3. **Persona-based reasoning** → Agent-bound Skill (`agent: [name]`)

### Pillar 4: Interface via Intent
**The `description` field is the API.** The Runtime discovers capabilities via semantic matching.

**Description Writing Rules:**
- Place "USE when [CONDITION]" as the **first sentence**
- Use natural language keywords for discovery
- Avoid XML `<example>` blocks in frontmatter (reserved for machine signaling only)

| Avoid | Prefer |
|:------|:-------|
| `<example>...</example>` | Keywords: "audit code", "fix bugs", "deploy app" |
| Buried trigger text | "USE when" as first sentence |
| Vague marketing copy | Action verbs + specific contexts |

**XML Reserved Cases:** Agent discovery (optional), hook signaling (`<promise>`, `<status>`), prompt grouping (`<guidelines>`), high-density data isolation.

### Pillar 5: State-in-Files
**Files are the Anchor.** While ephemeral context (RAM) is useful for reasoning, **critical state must be persisted**. Do not rely on the chat context for long-term memory. Use files to checkpoint work.

### Pillar 6: Shared-Nothing Parallelism
**No dependencies between parallel agents.** Never edit the same file. Orchestrator synthesizes outputs.

### Pillar 7: Meta-Synchronization
**Never "do what I say, not what I do."** Ensure absolute consistency between defined architecture (docs/prompts) and implemented behavior (code/scripts).

---

# PART II: COMMAND (Intent Layer)

## 2.1 What Commands Are

Commands are **Reusable Prompt Templates**—Markdown files that instruct the Main Agent for the current turn.

- Use `$ARGUMENTS` to capture user's full natural language input
- `argument-hint: [string]` is for UI documentation only
- Commands orchestrate workflows by instructing the Main Agent

---

## 2.2 Command Types

| Type | Consumer | `disable-model-invocation` | AskUserQuestion |
|:-----|:---------|:---------------------------|:----------------|
| User-Centric | Human only | `true` | Yes |
| Agent-Ready | Specialized Agents | `false` | No |
| Hybrid | Both | `false` | Conditional |

---

## 2.3 The Skill Tool (Recursive Pattern)

Agents invoke Commands via `Skill(/command-name)` or `Skill(/command:*)` for prefix matching.

---

## 2.4 Complex Orchestration Pattern

For complex multi-phase orchestration, follow the pattern in **[docs/GOLD_STANDARD_COMMAND.md](docs/GOLD_STANDARD_COMMAND.md)**.

**Pattern:** Discovery → Exploration (Agents) → Questions → Architecture (Agents) → Implementation → Review (Agents) → Summary

---

# PART III: AGENT (Autonomy Layer)

## 3.1 What Agents Are

Agents are **Specialized Personas** with their own system prompts and optional tool restrictions, launched via the `Task` tool.

- **Agent vs Subagent:** An Agent is the definition (`agents/*.md`); a "Subagent" is the runtime instance spawned via `Task`
- **Model Selection:** `haiku` (speed), `sonnet` (balance), `opus` (logic), or `'inherit'`
- **Tool Restriction:** `tools` field in frontmatter (whitelist). If omitted, inherits ALL tools
- **Permission Mode:** `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`, or `ignore`
- **Context Sharing:** Each subagent has its own context window but can access session history (read-only)

---

## 3.2 Agent Permissions

```yaml
---
name: code-reviewer
description: Analyzes code for quality issues
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: plan
skills: security-standards
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
---
```

**Critical:** If you omit `tools`, the agent inherits ALL tools including Read, Write, Edit, Bash, AskUserQuestion, Task, Skill, TodoWrite, and all MCP tools.

### The `skills` Field: Passive Knowledge Loading

The `skills` field lists skills whose instructions should be available to the agent as **passive knowledge**.

**How it works:**
- At agent startup: Only skill `name + description` loaded (~100 tokens)
- On activation: Full SKILL.md content loaded when relevant (<5000 tokens)
- On-demand: Resources (references/, assets/, scripts/) loaded as needed

**IMPORTANT:** The `skills` field does NOT trigger `context: fork`. It operates in **passive mode** only.

| Concept | Agent `skills` Field | Skill `context: fork` |
|:--------|:---------------------|:----------------------|
| **Mode** | Passive knowledge | Active execution |
| **When** | Agent startup/activation | When skill is invoked |
| **Fork?** | No | Yes - creates isolated subagent |
| **Use Case** | Agent needs skill's patterns | Skill needs isolated context |

**Non-Recursive:** An agent can list a skill that has `context: fork` without creating a loop. The agent gets passive access to the skill's content, but the fork only occurs when the skill is actively invoked (e.g., via `/skill-name` or semantic matching).

**Example - The Scribe Pattern:**
```yaml
# scribe.md (agent)
skills: [context-engineering]  # Passive: loads patterns on-demand

# context-engineering/SKILL.md
context: fork                   # Active: forks when invoked
agent: scribe                   # Persona to use during fork
```
This is valid: scribe gets context-engineering patterns passively, but `/context-engineering` invocation creates a fresh fork with scribe persona.

---

## 3.3 Agent Discovery Protocol

Agents are triggered via **semantic description matching**.

```yaml
---
name: security-reviewer
description: |
  USE when auditing code for security vulnerabilities.
  Specializes in OWASP patterns, injection flaws, and authentication issues.
capabilities:
  - security audit
  - vulnerability scan
  - penetration test
tools: Read, Grep, Glob
---
```

---

## 3.4 Delegation Patterns

**The Physics:** Delegation is based on **Context Gravity** and **Attention Dilution**.

> **The 10-File Heuristic:** If a task requires reasoning about >10 files, delegate to preserve Main Thread's attention focus.

### Pattern Selection Matrix

| Metric | Direct | Delegated | Parallel |
|:-------|:-------|:----------|:---------|
| **Files Involved** | 1-5 | 5-20 | 20+ |
| **Duration** | <1 min | 1-5 mins | 5+ mins |
| **User Input** | Required | Forbidden | Forbidden |

---

# PART IV: SKILL (Protocol Layer)

## 4.1 What Skills Are

Skills are **Hybrid Capability Units**—passive knowledge with optional active execution.

| Mode | Trigger | Behavior |
|:-----|:--------|:---------|
| **Passive** | Description matches user request OR agent's `skills` field | Standards/guidance loaded into context |
| **Active (Fork)** | `context: fork` set + skill invoked | Runs as isolated subagent |
| **Active (User)** | User types `/skill-name` | Direct invocation |

### Agent-Skill Binding Patterns

**Pattern 1: Passive Knowledge (Agent loads Skill)**
```yaml
# Agent definition
skills: [context-engineering]  # Passive: patterns available in-agent
```
When an agent lists a skill, the skill's content loads passively. The agent references the skill's patterns directly without forking.

**Pattern 2: Active Execution (Skill binds to Agent)**
```yaml
# Skill definition
context: fork
agent: scribe  # When forked, use scribe persona
```
When the skill is invoked, it creates an isolated subagent using the specified agent's persona and tool restrictions.

**Pattern 3: Combined (Both)**
```yaml
# scribe.md (agent)
skills: [context-engineering]  # Passive knowledge

# context-engineering/SKILL.md
context: fork                   # Active execution
agent: scribe                   # Use scribe when forked
```
**How it works:**
- Main Agent launches scribe via `Task` → scribe has context-engineering patterns available
- Someone invokes `/context-engineering` → skill forks with scribe persona
- **No recursion**: Passive loading never triggers `context: fork`

---

## 4.2 Skill Anatomy

```
skill-name/
├── SKILL.md          # Required: Instructions + Metadata
├── scripts/          # Optional: Executable scripts
├── references/       # Optional: On-demand documentation
└── assets/           # Optional: Templates, data files
```

---

## 4.3 Progressive Disclosure

| Layer | Budget | When Loaded |
|-------|--------|-------------|
| **Metadata** (`name` + `description`) | ~100 tokens | Startup |
| **Instructions** (SKILL.md body) | <5000 tokens | On activation |
| **Resources** (scripts/, references/, assets/) | Unlimited | On-demand |

---

## 4.4 Discovery Tiering Matrix

> [!IMPORTANT]
> The tiers below are **pattern guidance** for writing effective descriptions. Do NOT include `[Tier X: Name]` as a literal prefix.

| Tier | Use Case | Pattern |
|:-----|:---------|:--------|
| **1: High Fidelity** | Complex/fuzzy tasks, LLM capability overlap | `[MODAL] when [CONDITION]. Examples: <example>...` |
| **2: High Gravity** | Safety-critical, governance, mandatory protocols | `[MODAL] USE when [CONDITION].` |
| **3: Utility** | Single-purpose, self-documenting utilities | `{Action Verb} + {Object} + {Purpose}` |

**Selection Rules:**
1. >40% overlap with built-in tools → Tier 1
2. Governance/safety layer → Tier 2
3. Self-documenting name → Tier 3

---

## 4.5 YAML Frontmatter

For complete YAML schema, see **[docs/SKILL_FRONTMATTER_STANDARD.md](docs/SKILL_FRONTMATTER_STANDARD.md)**.

Required: `name` (max 64 chars), `description` (start with "USE when"). Optional: `allowed-tools`, `context: fork`, `agent`, `model`, `hooks`.

---

# PART V: RUNTIME MECHANICS

## 5.1 Permission System

Three-level cascading hierarchy:

1. **Main Agent** sets baseline permissions
2. **Subagents** can override `permissionMode` but inherit tool restrictions unless explicitly overridden
3. **Skills** can override both `permissionMode` and `allowed-tools`

| Restriction Type | Used By | Behavior |
|:-----------------|:--------|:---------|
| **`tools`** | **Agents** | Whitelist of what agent CAN use (hard boundary) |
| **`allowed-tools`** | **Commands/Skills** | Runtime restriction during execution |

### Permission Modes

| Mode | Behavior | Security |
|:-----|:---------|:---------|
| `default` | Prompts for each tool | High |
| `acceptEdits` | Auto-approves file operations | Medium |
| `plan` | Read-only analysis | High |
| `dontAsk` | Auto-deny unless pre-approved | High |
| `bypassPermissions` | All tools approved | **Very Low** |
| `ignore` | Ignores permission system | **None** |

---

## 5.2 Hooks (Governance)

Hooks are the **Immune System**—interception, safety, context injection. Never heavy work.

| Hook | Trigger |
|:-----|:--------|
| `SessionStart` | New session begins |
| `UserPromptSubmit` | Before prompt processing |
| `PreToolUse` | Before tool execution |
| `PermissionRequest` | Permission dialog shown |
| `PostToolUse` | After tool success |
| `Notification` | System notifications |
| `Stop` | Main agent finishes |
| `SubagentStop` | After task completion |
| `PreCompact` | Before context compaction |
| `SessionEnd` | Session ends |

For I/O protocol, validation scripts, and safety standards, see **[docs/HOOKS_OVERVIEW.md](docs/HOOKS_OVERVIEW.md)**.

---

## 5.3 MCP Integration

Plugins connect to external services via the **Model Context Protocol (MCP)**.

**Security:** Restrict by URL pattern, audit third-party servers, use OAuth tokens. Never use wildcard `*`.

For MCP configuration examples, see **[docs/IMPLEMENTATION-GUIDE.md](docs/IMPLEMENTATION-GUIDE.md#mcp-configuration)**.

---

## 5.4 Token Budget & Context Gravity

| Component | Budget |
|:----------|:-------|
| Command description | <200 tokens |
| Agent description | <500 tokens |
| Skill description | <200 tokens |
| SKILL.md body | <5000 tokens |
| Reference files | Unlimited |

**Context Gravity Rule:** If phase requires >5 source files → use Delegated pattern.

---

## 5.5 Interaction Graph

```mermaid
graph TB
    User["👤 User"]
    MainAgent["🤖 Main Agent<br/>(Claude)"]
    Commands["📋 Commands<br/>(Orchestrator)"]
    ForkedSkills["🔧 Forked Skills<br/>(context: fork)"]
    Skills["📚 Skills<br/>(Atomic Capabilities)"]
    Agents["👥 Agents<br/>(Personas)"]
    Tools["🛠️ Tools<br/>(Read, Write, Bash, etc.)"]
    Hooks["🪝 Hooks<br/>(Event Interception)"]
    MCP["🔌 MCP Servers<br/>(External Services)"]

    User -->|"Invokes (/skill)"| ForkedSkills
    User -->|"Invokes (/command)"| Commands
    User -->|"Natural Language"| MainAgent

    Commands -->|"Orchestrates"| Skills
    Commands -->|"Injects Instructions"| MainAgent

    MainAgent -->|"Auto-loads via description"| Skills
    MainAgent -->|"Uses"| Tools
    MainAgent -->|"Calls"| MCP

    Skills -->|"context: fork"| ForkedSkills
    ForkedSkills -.->|"Binds Persona"| Agents
    ForkedSkills -->|"Executes"| Tools
    Skills -->|"Auto-discoverable"| MainAgent

    Tools -->|"Triggers"| Hooks
    Hooks -.->|"Blocks/Warns/Injects"| MainAgent
```

---

# PART VI: MAINTENANCE

## 6.1 Project Hygiene

- **Never create temporary markdown reports** - Output findings directly in responses
- **Clean up after operations** - Remove temp files, caches, build artifacts
- **Move to .attic instead of deleting** - When removing code/files during refactoring
- **Run toolkit validation after changes** - `./scripts/toolkit-lint.sh`

IMPORTANT: If you have access to claude-code-guide agent, use it PROACTIVELY. Otherwise, refer to **[docs/RESEARCH_SOURCES.md](docs/RESEARCH_SOURCES.md)**.

---

## 6.2 File Path Standards

### Within Skills
```
✅ assets/templates/document.md
✅ references/format-guide.md
```

### Cross-Component
```
✅ "from the project-strategy skill"
❌ ../../../other-skill/assets/template.md
```

---

## 6.3 Forbidden Patterns

<forbidden_pattern>
**Caller Assumption:** Agent assumes specific command invoked it.
**Fix:** "You have been tasked with X" not "Called by /command".
</forbidden_pattern>

<forbidden_pattern>
**Command-Only Logic:** Business logic only in Command, not Skill.
**Fix:** Move logic to Skill. Command references, Agent reads.
</forbidden_pattern>

<forbidden_pattern>
**Cross-Plugin Coupling:** Component in Plugin A references component in Plugin B via hardcoded path.
**Fix:** Each plugin must be standalone. Cross-plugin references use natural language: "from the planning skill" (if installed). Intra-plugin references are allowed via skill-relative paths or `${CLAUDE_PLUGIN_ROOT} `.
</forbidden_pattern>

<forbidden_pattern>
**Blocking Interaction:** Unnecessary pausing for human input.
**Fix:** Prefer **Uninterrupted Flow** with `HANDOFF.md` for major blockers. Direct interaction is acceptable for quick, specific confirmations (e.g., "Deploy to prod?").
</forbidden_pattern>

<forbidden_pattern>
**Context Overflow (Direct Bloat):** executing complex logic inline when context >70% full.
**Fix:** Structured phases are **encouraged**, but if a phase requires deep reasoning or massive context, delegate it to an Agent. Keep the Command as the high-level conductor.
</forbidden_pattern>

<forbidden_pattern>
**Over-Prescription:** Micromanaging tool usage ("run ls then grep").
**Fix:** Goal-oriented: "Find the controller".
</forbidden_pattern>

<forbidden_pattern>
**Cross-Plugin Paths:** Hardcoded paths that reference components in other plugins.
**Fix:** Intra-plugin paths are fine (e.g., `scripts/validate.sh`, `${CLAUDE_PLUGIN_ROOT}/plugins/my-plugin/...`). Cross-plugin references must use natural language or gracefully handle missing plugins.
</forbidden_pattern>

<forbidden_pattern>
**Environment-Specific Coupling:** Hardcoding `model` or `permissionMode` when configurable.
**Fix:** Use environment variables or settings files for environment-specific values.
</forbidden_pattern>

<forbidden_pattern>
**Redundant Defaults:** Specifying default values in frontmatter (e.g., `user-invocable: true`).
**Fix:** Omit default values. Only specify if deviating.
</forbidden_pattern>

<forbidden_pattern>
**Buried Trigger:** Placing general description text BEFORE "USE when...".
**Fix:** "USE when" must be the very first sentence.
</forbidden_pattern>

---

## 6.4 Glue Code Detection

**The 10-Line Heuristic:** Glue code exceeding 10 lines **suggests** a missing abstraction or misplaced logic. Analyze carefully, but implement if necessary for robustness.

| Component Type | Acceptable | Red Flag |
|:---------------|:-----------|:---------|
| Command Wrapper | <10 lines | >10 lines |
| Skill Wrapper | <5 lines | >10 lines |
| Agent Pass-through | <5 lines | >10 lines |

**Refactoring:** Collapse layers, inline standards, merge overlapping commands.

---

## 6.5 The .cattoolkit Root

All runtime artifacts stored in `.cattoolkit/`:
- **Session State**: `.cattoolkit/context/`
- **Project Management**: `.cattoolkit/planning/`

---

# Documentation References

## Core Specifications
- **[docs/SKILL_FRONTMATTER_STANDARD.md](docs/SKILL_FRONTMATTER_STANDARD.md)** - Complete YAML schema and field reference

## Implementation & Recipes
- **[docs/IMPLEMENTATION-GUIDE.md](docs/IMPLEMENTATION-GUIDE.md)** - Validation scripts, MCP configuration, endpoint adaptation
- **[docs/COMMAND-OVERVIEW.md](docs/COMMAND-OVERVIEW.md)** - Command YAML recipes
- **[docs/HOOKS_OVERVIEW.md](docs/HOOKS_OVERVIEW.md)** - Hook I/O protocol, validation scripts, safety standards
- **[docs/ARCHITECTURE_REFERENCE.md](docs/ARCHITECTURE_REFERENCE.md)** - Multi-LLM provider technical details

## Reference
- **[docs/GOLD_STANDARD_COMMAND.md](docs/GOLD_STANDARD_COMMAND.md)** - Full-text command example
- **[docs/RESEARCH_SOURCES.md](docs/RESEARCH_SOURCES.md)** - External documentation links
- **[README.md](README.md)** - Installation and marketplace
