# CLAUDE.md

Project Context Definition for Claude Code. This document defines the **Universal Agentic Runtime**—a layered architecture where **Skills**, **Commands**, and **Agents** serve as parallel entry points for capabilities.

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
| **Skill** | **Atomic Capability** | Top-level tool. User-invocable (`/skill-name`) OR model-discovered. Supports `context: fork` and `agent: [name]` binding. |
| **Command** | **Workflow Orchestrator** | Orchestrates single or multiple Skills. Provides deterministic shortcuts for any workflow. |
| **Agent** | **Persona** | Reusable identity/tools that Skills can bind to via `agent: [name]`. |

---

## 1.3 Core Pillars

### Pillar 1: Plugin Portability
**Intra-Plugin Collaboration, Inter-Plugin Independence:** Components within the same plugin should collaborate freely. Agents can reference skill scripts, and skills can delegate to plugin agents. However, **cross-plugin coupling is forbidden**—each plugin must be fully functional standalone. Domain expertise lives in Skills; Agents reference their plugin's skills via the `skills` field or natural language (not hardcoded paths to other plugins).

### Pillar 2: Atomic Capabilities with Hybrid Execution
Skills have dual nature: **passive knowledge** (auto-discovered) and **active execution** (via `context: fork` or user invocation). Commands can orchestrate single or multiple Skills—single-skill shortcuts are valid for deterministic access.
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

# PART II: ARCHITECTURE & SCHEMAS

## 2.1 The Marketplace Layer

The **Standard Marketplace Schema** aggregates and distributes plugins.

**Location**: `.claude-plugin/marketplace.json`

```json
{
  "$schema": "https://json.schemastore.org/claude-marketplace-1.0.0.json",
  "name": "The Cat Toolkit Official Marketplace",
  "version": "1.0.0",
  "plugins": [
    {
      "name": "meta",
      "source": "github:thecattoolkit/plugins/meta",
      "category": "core"
    }
  ]
}
```

## 2.2 The Plugin Layer

The **Standard Plugin Definition** required for every plugin.

**Location**: `.claude-plugin/plugin.json` (Plugin Root)

```json
{
  "$schema": "https://json.schemastore.org/claude-plugin-1.0.0.json",
  "name": "strategist",
  "version": "1.2.0",
  "capabilities": ["agents", "skills", "commands"],
  "readme": "README.md",
  "license": "MIT"
}
```

## 2.3 Plugin Portability

**Independent Units:**
- **Intra-Plugin**: Free referencing (agents ↔ skills).
- **Cross-Plugin**: **Strongly discouraged**. Avoid hardcoded paths (`../other-plugin`). Prefer natural language referencing ("use the planning skill") or explicit dependencies in `plugin.json`.

---

# PART III: AGENTS & PERMISSIONS

## 3.1 What Agents Are

Agents are **Specialized Personas** defined in `agents/*.md`.

- **Model Selection**: `haiku` (speed), `sonnet` (balance), `opus` (logic), or `'inherit'`.
- **Tool Restriction**: `tools` field is a **whitelist**. If omitted, inherits ALL tools. **Best practice:** Explicitly list tools for security-critical agents.
- **Context Sharing**: Subagents have their own context but can read session history.

## 3.2 Agent Permissions & Security

**Cascading Hierarchy:**
1. **Main Agent** sets baseline.
2. **Subagents** override `permissionMode`.
3. **Skills** override `permissionMode` and `allowed-tools`.

### Permission Modes

| Mode | Behavior | Security |
|:-----|:---------|:---------|
| `default` | Prompts for each tool | High |
| `acceptEdits` | Auto-approves file operations | Medium |
| `plan` | Read-only analysis | High |
| `dontAsk` | Auto-deny unless pre-approved | High |
| `bypassPermissions` | All tools approved | **Very Low** |

**Crucial:** If you omit `tools`, the agent inherits EVERYTHING. Always specify `tools` for security-critical agents.

## 3.3 Skills Field vs Context Fork

**Two distinct mechanisms:**
1. **Agent's `skills` list**: Makes skills **available** to the agent as passive knowledge. Does NOT affect execution mode.
2. **Skill's `context: fork`**: Dictates **execution behavior** when the skill is invoked—runs in isolated subagent context.

| Configuration | Availability | Execution |
|:--------------|:-------------|:----------|
| Listed in agent's `skills` | Available to agent | Inline (unless skill has `context: fork`) |
| Skill has `context: fork` | Per normal discovery | Forked subagent context |

## 3.4 Runtime Environment

Configure via `.claude/settings.json` or env vars:

| Variable | Purpose |
|:---------|:--------|
| `ANTHROPIC_BASE_URL` | API endpoint (Zai, Minimax proxy) |
| `ANTHROPIC_API_KEY` | Authentication token |

---

# PART IV: SKILL PROTOCOL

Skills are **Hybrid Capability Units**—passive knowledge with optional active execution (`context: fork`).

## 4.1 Skill Anatomy

```
skill-name/
├── SKILL.md          # Instructions + Metadata
├── scripts/          # Executable scripts (bash/python)
├── references/       # Docs loaded on-demand
└── assets/           # Templates/data
```

## 4.2 Frontmatter Standard

**Location**: `SKILL.md`

```yaml
---
name: my-skill-name
description: >
  USE when [condition].
  A concise, action-oriented description.
context: fork          # Optional: runs in subagent
allowed-tools: [Read, Write, Bash]
model: sonnet
hooks:
  PreToolUse: "validate-input"
---
```

## 4.3 Field Constraints

| Field | Required | Constraints |
|:------|:---------|:------------|
| `name` | **Yes** | Max 64 chars. Must match directory name. |
| `description` | **Yes** | Max 1024 chars. Must start with "USE when". |
| `allowed-tools` | No | Comma-delimited string or YAML list. |
| `model` | No | Model for skill execution (e.g., `sonnet`, `opus`). |
| `context` | No | `fork` for isolation. Omit for inline. |
| `agent` | No | Binds forked skill to Agent persona. Only applicable with `context: fork`. |
| `user-invocable` | No | `false` hides from slash command menu. Default: `true`. |

## 4.4 Discovery Tiering Matrix

| Tier | Use Case | Pattern |
|:-----|:---------|:--------|
| **1: High Fidelity** | Complex/fuzzy tasks | `[MODAL] when [CONDITION]. Examples: ...` |
| **2: High Gravity** | Safety-critical, governance | `[MODAL] USE when [CONDITION].` |
| **3: Utility** | Single-purpose tools | `{Action Verb} + {Object} + {Purpose}` |

---

# PART V: COMMAND INTENT

Commands are **Reusable Prompt Templates** (`commands/*.md`) that orchestrate workflows. They instruct the Main Agent.

## 5.1 Command Types (Recipes)

### 1. Safe Read-Only
```yaml
---
description: "Analyze project structure"
allowed-tools: [Read, Grep]
permissionMode: plan
---
```

### 2. Autonomous Agent Wrapper
```yaml
---
description: "Autonomous code review"
allowed-tools: [Read, Grep, Glob]
permissionMode: plan
---
Analyze codebase. Output JSON. DO NOT ask questions.
```

### 3. User Interactive (Wizard)
```yaml
---
description: "Project scaffolding wizard"
disable-model-invocation: true
---
Guide user through setup. Ask for template preference.
```

## 5.2 Complex Orchestration
For complex multi-phase workflows (Discovery → Plan → Act → Verify), refer to **[examples/GOLD_STANDARD_COMMAND.md](examples/GOLD_STANDARD_COMMAND.md)** (kept as reference).

---

# PART VI: RUNTIME MECHANICS

## 6.1 Hooks (The Immune System)

Hooks intercept events for safety and compliance.

**Key Events**: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`.

### Standard I/O Protocol
- **Input**: JSON via `stdin`
- **Output**: JSON via `stdout`
- **Exit Codes**: `0` (Success/Continue), `2` (Block/Fail)

**Example Hook (JSON)**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
           { "type": "command", "command": "./scripts/safety-check.py" }
        ]
      }
    ]
  }
}
```

**Safety Standards**:
- Always use `${CLAUDE_PLUGIN_ROOT}` in paths.
- Validate all `TOOL_INPUT` parameters.
- Prevent path traversal (`..`).

## 6.2 MCP Integration

Connect external tools via `.mcp.json`.

**Security Rule**: Explicitly allow servers. Avoid wildcard `*` unless necessary.
```yaml
allowedMcpServers:
  - serverUrl: "https://approved-api.com/*"
```

## 6.3 Universal Endpoint Adaptation

The toolkit supports multiple backends. Adjust behavior layout:

| Endpoint | Strategy |
|:---------|:---------|
| **Anthropic** | Full capability. Native `Task`/`Skill`. |
| **Zai (GLM)** | Use native function calling. `GLM-4.6V` for vision. |
| **Minimax** | Prioritize **Parallel Agents**. Very fast inference. |

## 6.4 Validation & Linting

| Script | Purpose |
|:-------|:--------|
| `./scripts/toolkit-lint.sh` | Comprehensive suite (Agents, Skills, Hooks) |
| `manage-hooks/assets/scripts/hook-tester.py` | Validates `hooks.json` syntax |

---

# PART VII: MAINTENANCE & REFERENCES

## 7.1 Hygiene & Standards

- **Clean up**: Remove temp files (`rm tmp.json`) after use.
- **Move not Delete**: Use `.attic/` for deprecated code during refactors.
- **Validation**: Run `./scripts/toolkit-lint.sh` after changes.
- **File Paths**: Use `assets/templates/doc.md` (relative) or `${CLAUDE_PLUGIN_ROOT}`.

## 7.2 Forbidden Patterns

<forbidden_pattern>
**Caller Assumption:** "Called by /command".
**Fix:** "You have been tasked with X".
</forbidden_pattern>

<forbidden_pattern>
**Cross-Plugin Hardlinks:** `../other-plugin/script.sh`.
**Fix:** Natural language referencing or explicit dependencies.
</forbidden_pattern>

<forbidden_pattern>
**Buried Trigger:** Text before "USE when".
**Fix:** "USE when" must be the FIRST sentence.
</forbidden_pattern>

<forbidden_pattern>
**Glue Code Bloat:** Wrappers >10 lines.
**Fix:** Collapse layers.
</forbidden_pattern>

---

## 7.3 External References

| Resource | Purpose |
|:---------|:--------|
| [CLI Reference](https://code.claude.com/docs/en/cli-reference.md) | Command-line usage |
| [Plugin Development](https://code.claude.com/docs/en/plugins.md) | Structure & API |
| [Skills System](https://code.claude.com/docs/en/skills.md) | SKILL.md rules |
| [Model Context Protocol](https://code.claude.com/docs/en/mcp.md) | Integration specs |
