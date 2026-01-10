# CLAUDE.md

Project Context Definition for Claude Code. This document defines the **Cat Toolkit Orchestration Framework**—a layered architecture where **Skills**, **Commands**, and **Agents** serve as parallel entry points for capabilities.

---

## Scope: Claude Code Standards vs Cat Toolkit Extensions

This document covers both **standard Claude Code features** and **Cat Toolkit-specific extensions**. Understanding the distinction is important for compatibility.

### Standard Claude Code Features

These features work with any Claude Code installation:

| Feature | Status | Notes |
|:--------|:-------|:------|
| **Skills** (`skills/*/SKILL.md`) | ✅ Standard | Core capability |
| **Commands** (`commands/*.md`) | ✅ Standard | Core capability |
| **Agents** (`agents/*.md`) | ✅ Standard | Core capability |
| **Hooks** (`hooks.json`) | ✅ Standard | Core capability |
| **MCP** (`.mcp.json`) | ✅ Standard | Core capability |
| **LSP** (`.lsp.json`) | ✅ Standard | Core capability |
| **Plan Mode** | ✅ Standard | Built-in workflow |
| **Task tool** | ✅ Standard | Core mechanism |

### Cat Toolkit Extensions

These are **conventions specific to the Cat Toolkit ecosystem**:

| Feature | Type | Compatibility |
|:--------|:-----|:--------------|
| `.claude-plugin/` directory | Convention | Cat Toolkit only |
| `marketplace.json` schema | Extension | Cat Toolkit only |
| `plugin.json` with `capabilities` field | Extension | Partial (standard fields work) |
| Plugin namespace for commands | Convention | Automatic in Cat Toolkit |
| Custom marketplace distribution | Extension | Cat Toolkit only |

### Design Philosophy

The Cat Toolkit is designed to:
1. **Extend** Claude Code with additional conventions
2. **Maintain compatibility** with standard plugins
3. **Provide tooling** for plugin management and distribution
4. **Standardize** common patterns across plugins

> [!TIP]
> When creating plugins for general distribution, prioritize **standard Claude Code features**. Use Cat Toolkit extensions only when the additional functionality is needed.

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

> [!WARNING]
> `AskUserQuestion` is **strongly discouraged** in Skills. Use it only when the task is **inherently interactive** (e.g., wizards, multi-step configuration).
>
> **Why?**
> - **Composability**: Skills should be composable building blocks. Interactive breaks prevent chaining skills together.
> - **Agent autonomy**: When agents orchestrate skills, they cannot handle user interruptions gracefully.
> - **Background execution**: Forked skills with `AskUserQuestion` will fail silently in background contexts.
>
> **When is it allowed?**
> - User-facing wizards where interaction is the primary purpose
> - Tasks requiring explicit confirmation (e.g., destructive operations)
> - Commands (not skills) where user interaction is expected

### Pillar 3: Native Delegation
**"Never write in code what can be described in intent."**

| Anti-Pattern | Native Pattern |
|:-------------|:---------------|
| `find . -name "*.ts" -exec grep "todo" {} \;` | "Find all TypeScript files containing TODO comments" |
| Command wrapping single Skill | Forked Skill with `context: fork` |
| "Run find src -name '*.js'" | "Locate source files using filesystem tools" |

#### Two Dimensions: Discovery vs Execution

**Discovery** (How the skill is found):
| Method | Trigger | Use Case |
|:-------|:--------|:---------|
| **Auto-discovery** | Semantic matching of `description` | Model finds skill automatically |
| **Explicit call** | `Skill(/skill-name)` in code | Command/agent orchestration |
| **Passive injection** | Agent's `skills` field | Knowledge without execution |

**Execution** (How the skill runs):
| Mode | Context | Use Case |
|:-----|:--------|:---------|
| **Inline** | Main conversation | Simple operations, no isolation needed |
| **Forked** (`context: fork`) | Isolated subagent | Heavy computation, large outputs, independent execution |

> [!NOTE]
> Manual `Skill()` loading is **not an anti-pattern**. Choose based on your needs:
> - **Fork for isolation**: Large outputs, independent tasks
> - **Explicit call for orchestration**: Multi-step workflows
> - **Passive field for knowledge**: Agent pattern adoption

**Delegation Decision Tree:**
```
┌─ Atomic, isolated task? → Forked Skill (context: fork)
├─ Multi-phase workflow?  → Command orchestrating Skills
└─ Persona-based reasoning? → Agent-bound Skill (agent: [name])
```

### Pillar 4: Discovery via Semantic Matching
**The `description` field is the discovery mechanism.** Claude discovers capabilities by semantically matching user requests against skill/command descriptions.

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

#### XML Tag Examples

**Hook Signaling (in hooks.json or frontmatter):**
```xml
<promise>
This hook guarantees that all Python files will be formatted before commit.
</promise>

<status type="info">
This hook is experimental and may change.
</status>
```

**Prompt Grouping (in SKILL.md):**
```xml
<guidelines>
You must always:
1. Validate inputs before processing
2. Provide detailed error messages
3. Log all operations for debugging
</guidelines>
```

**High-Density Data (in SKILL.md):**
```xml
<patterns>
  <security>
    - Check for hardcoded credentials
    - Validate input sanitization
    - Review authentication flows
  </security>
  <performance>
    - Identify N+1 queries
    - Check for missing indexes
    - Review caching strategies
  </performance>
</patterns>
```

**Agent Discovery (in agent.md frontmatter):**
```yaml
---
tags:
  - security
  - code-review
  - audit
---
```

### Pillar 5: State-in-Files
**Files are the Anchor.** While ephemeral context (RAM) is useful for reasoning, **critical state must be persisted**. Do not rely on the chat context for long-term memory. Use files to checkpoint work.

### Pillar 6: Shared-Nothing Parallelism
**No dependencies between parallel agents.** Each agent works on independent data and produces separate outputs. The orchestrator synthesizes the results.

**What this means:**
- **No shared write targets**: Parallel agents must NEVER modify the same file
- **Independent inputs**: Each agent receives its own portion of work
- **Separate outputs**: Results go to separate files or are returned independently
- **Orchestrator synthesis**: The main agent/Command combines results after completion

**Example - Correct Pattern:**
```
Main Agent:
├─ Agent A: Analyzes src/frontend/ → outputs/frontend-analysis.json
├─ Agent B: Analyzes src/backend/  → outputs/backend-analysis.json
└─ Synthesizes both into final report
```

**Example - Anti-Pattern (AVOID):**
```
❌ Agent A and Agent B both write to results.json
❌ Agent B waits for Agent A to finish (creates dependency)
❌ Agents communicate directly with each other
```

**Why?** Parallel execution provides speed and isolation. Shared state creates race conditions, conflicts, and defeats the purpose of parallelism.

### Pillar 7: Meta-Synchronization
**Never "do what I say, not what I do."** Ensure absolute consistency between defined architecture (docs/prompts) and implemented behavior (code/scripts).

---

# PART II: ARCHITECTURE & SCHEMAS

## 2.1 The Marketplace Layer

The **Cat Toolkit Marketplace Schema** aggregates and distributes plugins within the Cat Toolkit ecosystem.

> [!NOTE]
> This schema is **specific to the Cat Toolkit**. Standard Claude Code plugins use a different distribution mechanism (direct GitHub URLs, npm packages, etc.).

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

The **Cat Toolkit Plugin Definition** required for every plugin in the ecosystem.

> [!NOTE]
> The `.claude-plugin/` subdirectory is a **Cat Toolkit convention**. Standard Claude Code plugins place `plugin.json` at the root directory.

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

**Cat Toolkit Extensions**: The `capabilities` and `readme` fields are **Cat Toolkit-specific**. Standard Claude Code plugins use: `name`, `description`, `publisher`, `version`, `license`.

## 2.3 Plugin Portability

**Independent Units:**
- **Intra-Plugin**: Free referencing (agents ↔ skills).
- **Cross-Plugin**: **Strongly discouraged**. Avoid hardcoded paths (`../other-plugin`). Prefer natural language referencing ("use the planning skill") or explicit dependencies in `plugin.json`.

## 2.4 Plugin Namespace

Commands from plugins are automatically namespaced to avoid conflicts.

**Namespace Format:** `{plugin-name}/{command-name}`

**Examples:**
| Plugin | Command File | Invocation |
|:-------|:-------------|:-----------|
| `my-toolkit` | `commands/deploy.md` | `/my-toolkit/deploy` |
| `security-scanner` | `commands/audit.md` | `/security-scanner/audit` |
| `project-local` (no plugin) | `commands/test.md` | `/test` |

**Key Points:**
- **Skills are NOT namespaced**: Skills from plugins are available globally by name only
- **Agents are NOT namespaced**: Agents from plugins are available globally by name only
- **Commands ARE namespaced**: Prevents naming conflicts between plugins
- **Local commands**: Commands in `.claude/commands/` (project-local) are not namespaced

**Why this matters:**
When installing multiple plugins, naming conflicts are inevitable. Namespacing commands ensures `/deploy` from `plugin-a` doesn't conflict with `/deploy` from `plugin-b`. However, skills and agents are designed to be shared components, so they remain global.

---

# PART III: AGENTS & PERMISSIONS

## 3.1 What Agents Are

Agents are **Specialized Personas** defined in `agents/*.md`.

- **Model Selection**: `haiku` (speed), `sonnet` (balance), `opus` (logic), or `inherit` (same as parent).
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

### 1. Agent's `skills` list (Knowledge Injection)
When an agent lists skills in its `skills` field, those skills' instructions are **injected into the agent's context** as passive knowledge. The agent becomes aware of the skill's patterns, logic, and approaches, but does NOT automatically execute them.

**How the agent uses injected skills:**
- **Auto-discovery**: The model may invoke the skill via the `Skill` tool when it recognizes a matching pattern
- **Explicit invocation**: The agent can explicitly call `Skill(/skill-name)` when needed
- **Pattern adoption**: The agent adopts the skill's reasoning patterns without direct invocation

### 2. Skill's `context: fork` (Execution Mode)
When a skill has `context: fork`, it **always executes in an isolated subagent context** when invoked, regardless of who calls it (main agent, another agent, or command).

| Configuration | Availability | Execution Mode |
|:--------------|:-------------|:---------------|
| Listed in agent's `skills` | ✅ Available (knowledge injected) | Inline (default) |
| Skill has `context: fork` | Per normal discovery | ✅ Forked subagent |
| Both combined | ✅ Available | ✅ Forked (fork takes precedence) |

**Example:**
```yaml
# Agent definition
---
name: code-reviewer
skills: [security-patterns, clean-code-practices]
tools: [Read, Grep]
---
```

When `code-reviewer` runs, it has knowledge of `security-patterns` and `clean-code-practices` injected into its context. If either skill is invoked (by auto-discovery or explicit call), they execute inline unless they have `context: fork`.

### 3.3.1 Combining `context: fork` with `agent`

A forked skill can be bound to a specific agent persona using the `agent` field. This is useful when you want the skill to execute with a particular agent's capabilities and constraints.

**How it works:**
1. Skill is invoked (manually or via auto-discovery)
2. Claude spawns a subagent using the specified agent definition
3. The skill's instructions become the subagent's system prompt
4. The subagent executes with the agent's tools, permissions, and model

**Example:**
```yaml
# skills/deep-audit/SKILL.md
---
name: deep-audit
description: USE when you need a comprehensive security audit
context: fork
agent: security-analyzer
model: opus
allowed-tools: [Read, Grep, Bash]
---
```

When invoked, this skill:
- Spawns a subagent using the `security-analyzer` agent definition
- Uses the `opus` model (overrides agent's model if specified)
- Has access to Read, Grep, Bash tools
- Executes in isolated context (output doesn't pollute main conversation)

**Important:** The `agent` field is **only valid with `context: fork`**. If `context: fork` is not set, the `agent` field is ignored.

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
| `allowed-tools` | No | YAML list (recommended) or comma-delimited string. See examples below. |
| `model` | No | Model for skill execution (e.g., `sonnet`, `opus`, `haiku`, `inherit`). |
| `context` | No | `fork` for isolation. Omit for inline. |
| `agent` | No | Binds forked skill to Agent persona. Only applicable with `context: fork`. |
| `user-invocable` | No | `false` hides from slash command menu. Default: `true`. |

### allowed-tools Format Examples

**Recommended (YAML list):**
```yaml
allowed-tools: [Read, Write, Bash, Grep]
```

**Alternative (String - requires parsing):**
```yaml
allowed-tools: "Read,Write,Bash,Grep"
```

**With tool restrictions:**
```yaml
allowed-tools: [Bash[python, npm], Read]
```

> [!NOTE]
> The YAML list format is preferred for clarity and avoids string parsing ambiguity.

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

# PART V.I: PLAN MODE

Plan Mode is a dedicated workflow for **planning before implementation**. It allows exploration and design without committing to changes.

## 5.1 When to Use Plan Mode

✅ **Use Plan Mode for:**
- Complex implementations with multiple approaches
- Architectural decisions requiring user input
- Refactoring that affects many files
- Tasks where you need approval before proceeding

❌ **Don't use Plan Mode for:**
- Simple bug fixes (1-2 line changes)
- Trivial tasks with clear requirements
- Pure research/exploration (use the Explore agent instead)

## 5.2 Plan Mode Workflow

```
User Request
     ↓
Claude identifies complexity/ambiguity
     ↓
EnterPlanMode() tool called
     ↓
┌─────────────────────────────┐
│   PLAN MODE ACTIVE          │
│  - Read-only exploration     │
│  - Architecture design       │
│  - AskUserQuestion allowed  │
│  - No file modifications     │
└─────────────────────────────┘
     ↓
Plan written to file (.md)
     ↓
ExitPlanMode() tool called
     ↓
┌─────────────────────────────┐
│   USER APPROVAL PHASE       │
│  - User reviews plan        │
│  - Approve or request changes│
└─────────────────────────────┘
     ↓
Implementation (with approved plan)
```

## 5.3 Plan Mode Tools

| Tool | Purpose |
|:-----|:--------|
| **EnterPlanMode** | Transition to planning state (read-only) |
| **ExitPlanMode** | Submit plan for user approval |

## 5.4 Plan Mode vs Forked Skills

| Aspect | Plan Mode | Forked Skill (`context: fork`) |
|:-------|:----------|:------------------------------|
| **Purpose** | Planning before action | Executing isolated tasks |
| **User interaction** | Required (approval) | Optional |
| **File modifications** | Forbidden (read-only) | Allowed |
| **Output** | Plan document | Task result |
| **Use case** | Complex implementations | Atomic operations |

## 5.5 Writing a Good Plan

A good plan document should include:

```markdown
# Implementation Plan: [Feature Name]

## Overview
Brief description of what will be implemented.

## Approach
[Chosen approach and rationale]

## Files to Modify
- `path/to/file1.ts` - Changes: ...
- `path/to/file2.ts` - Changes: ...

## Implementation Steps
1. [First step]
2. [Second step]
3. [Third step]

## Testing Strategy
- How will this be tested?
- What edge cases need coverage?

## Potential Issues
- [Identified risks and mitigations]
```

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

## 6.3 LSP (Language Server Protocol) Integration

LSP provides real-time code intelligence—diagnostics, go-to-definition, hover info, and more.

**Configuration**: `.lsp.json` (in plugin root or `.claude/`)

```json
{
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "extensionToLanguage": {
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript"
      },
      "initializationOptions": {
        "preferences": {
          "disableSuggestions": false
        }
      }
    },
    "python": {
      "command": "pyright-langserver",
      "args": ["--stdio"],
      "extensionToLanguage": {
        ".py": "python"
      }
    }
  }
}
```

**Common LSP Servers:**

| Language | Server | Installation |
|:---------|:--------|:-------------|
| TypeScript | `typescript-language-server` | `npm install -g typescript-language-server` |
| Python | `pyright-langserver` | `npm install -g pyright` |
| Rust | `rust-analyzer` | Included with Rust |
| Go | `gopls` | `go install golang.org/x/tools/gopls@latest` |

**LSP Capabilities:**
- ✅ **Diagnostics**: Real-time error/warning detection
- ✅ **Go-to-definition**: Navigate to symbol definitions
- ✅ **Find references**: Locate all usages of a symbol
- ✅ **Hover information**: Type info and documentation on hover
- ✅ **Completion**: Code completion suggestions

**When to use LSP:**
- Large codebases where type safety is critical
- Projects requiring real-time feedback
- Complex refactoring operations
- When developing language-specific tools

**When LSP is overkill:**
- Small scripts or one-off files
- Projects without type systems
- When CLI tools (linters, formatters) are sufficient

## 6.4 Universal Endpoint Adaptation

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
**Unnecessary Abstraction Layers:** Creating wrappers or intermediate functions that don't add value.
**Fix:** Prefer direct calls for simple operations. If abstraction is needed, ensure it provides clear benefits (reusability 3+, testability, or significant simplification).
</forbidden_pattern>

---

## 7.3 External References

| Resource | Purpose |
|:---------|:--------|
| [CLI Reference](https://code.claude.com/docs/en/cli-reference.md) | Command-line usage |
| [Plugin Development](https://code.claude.com/docs/en/plugins.md) | Structure & API |
| [Skills System](https://code.claude.com/docs/en/skills.md) | SKILL.md rules |
| [Model Context Protocol](https://code.claude.com/docs/en/mcp.md) | Integration specs |
