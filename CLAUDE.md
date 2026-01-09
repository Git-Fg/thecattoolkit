# CLAUDE.md

Primary operating system for Claude Code. This document defines the **Universal Agentic Runtime**—a hierarchical architecture where **Command (Intent) → Agent (Autonomy) → Skill (Protocol)**. This architecture is optimized for both official (Anthropic) and unofficial (Zai, Minimax) endpoints.

---

# PART I: PARADIGM

## 1.1 The Orchestration Runtime

The toolkit operates as an **Orchestration Runtime**. It is agnostic to the underlying endpoint (Official or Unofficial) but remains **Claude Code Centric** in its protocol.
- **The Model** is the CPU (Claude, GLM, MiniMax).
- **The Context** is the RAM.
- **The Components (Commands/Agents/Skills)** are the Software.

### Natural Language Orchestration
We do not program Claude with loops or scripts. We program with **Intent**.
> **The Parallel Paradigm:** Instead of scripting `for file in files`, instruct:
> *"Launch 3 code-explorer agents in parallel to audit the `src/` directory."*

The Runtime handles concurrency natively via the `Task` tool. Use **Declarative Orchestration** over Imperative Scripting.

---

## 1.2 The Unified Capability Architecture

The architecture centers on **Skills as atomic units of work** with Commands and Agents serving as composition mechanisms:

| Component | Role | Native Mechanic |
|:----------|:-----|:----------------|
| **Skill** | **Atomic Capability** | Auto-discoverable via semantic matching. Can be `user-invocable`, `context: fork`, and `agent: [name]` bound. |
| **Command** | **Orchestrator** | Manages multi-phase workflows by sequencing multiple Skills. |
| **Agent** | **Persona** | Reusable identity/tools that Skills can bind to via `agent: [name]`. |

> **The New Paradigm:**
> - Skills **execute** (atomic work units with Triggers + Execution + Context)
> - Commands **orchestrate** (multi-skill workflows)
> - Agents **provide** (reusable personas/toolsets for Skills)

### Tool Primitives

These native tools drive the architecture:

| Tool | Purpose |
|:-----|:--------|
| `Task` | Spawns subagents with specialized personas |
| `Skill` | Loads skills/invokes commands programmatically |
| `Read` / `Glob` / `Grep` | File system interaction |
| `Write` / `Edit` | File modification |
| `Bash` | Shell command execution |
| `AskUserQuestion` | User interaction during planning |

---

## 1.3 Core Laws

### Law 1: Atomic Independence
Components function standalone. Synergy is a side effect.
- **Agent Sovereignty:** No caller dependency. Self-sufficient discovery.
- **Skill Universality:** Human-readable. No hidden logic. Direct access.
- **Zero-Shared-State:** No cross-plugin file references.

**Mercenary Isolation:** Agents must be **mercenary**—never assume they are part of a specific command.
- **Caller Independence:** Agents MUST NOT reference plugin-specific files in system prompts
- **Context via Prompting:** Commands inject content via natural language prompts
- **Eternal Skills:** Commands are transient; Skills are eternal. Domain expertise lives in Skills, not Agent system prompts.

### Law 2: Law of Unification
**A Skill that defines its own context (`context: fork`) and trigger (`user-invocable`) requires no Command wrapper.**

Skills are now **atomic capability units** that can operate independently:
- **Forked Skills:** Use `context: fork` to run in isolation, replacing Task tool delegation
- **User-Invocable Skills:** Use `user-invocable: true` to appear in slash commands
- **Agent-Bound Skills:** Use `agent: [name]` to bind to reusable personas

This eliminates glue code where Commands exist solely to wrap single Skills.

### Law 3: Native Delegation
**"Never write in code what can be described in intent."**
If it involves reasoning, delegate to an Agent. Don't script it.

| Anti-Pattern | Native Pattern |
|:-------------|:---------------|
| `find . -name "*.ts" -exec grep "todo" {} \;` | "Find all TypeScript files containing TODO comments" |
| Parsing JSON → condition → action in Command | Delegate to agent with goal description |
| Step-by-step tool micromanagement | Goal-oriented natural language delegation |

### Law 4: Law of Description
**"The `description` field is the API."**
The Runtime discovers capabilities via semantic matching of descriptions.

Use natural language keywords for Semantic Discovery. Avoid XML `<example>` blocks in frontmatter.

| Avoid | Prefer |
|:------|:-------|
| `<example>...</example>` | Keywords: "audit code", "fix bugs", "deploy app" |
| XML boilerplate | Plain language descriptions |
| Structured examples | Natural triggers ("Use when...") |

### Law 5: State-in-Files
Context is ephemeral; files are eternal. Decisions → ADR. Tasks → Status file. If not on disk, it didn't happen.

### Law 6: Shared-Nothing Parallelism
- Atomic assignments (no dependencies between parallel agents)
- File locking (parallel agents never edit same file)
- Synthesis obligation (orchestrator merges outputs)

### Law 7: Passive Skills
Skills are cookbooks, not wizards. AskUserQuestion FORBIDDEN in skills. If input missing → agent judgment or HANDOFF.md.

### Law 8: Native Capabilities
Trust the model. Declarative over procedural. Universal over specific.

| Avoid | Prefer |
|:------|:-------|
| "Check package.json, then requirements.txt" | "Identify dependency management system" |
| "Run find src -name '*.js'" | "Locate source files using filesystem tools" |
| "Execute these grep commands: ..." | "Search for authentication patterns" |
| "Use the Read tool on path/to/file.ts" | "Read the config file in the src folder" |

### Law 9: XML Reserved for Machine Signaling
XML tags are reserved for **Machine Reliability** in specific cases only.

| Use Case | Status | Tags | Reason |
|:---------|:-------|:-----|:-------|
| **Agent Discovery** | **Optional** | `<example>`, `<commentary>` | Can help with complex agent selection, but description matching is primary. |
| **Hook Signaling** | **Allowed** | `<promise>`, `<status>` | Hooks use regex to extract signals from output. |
| **Prompt Grouping** | **Optional** | `<guidelines>`, `<rules>` | Helps the Model separate distinct rule sets. |
| **Data Isolation** | **Caution** | `<data>`, `<raw>` | Only for high-density (>100 lines) unstructured data. |

**Use Markdown** for all other prompt structure. Natural language and headers are preferred.

### Law 10: Meta-Synchronization
**When working on the toolkit itself (Meta-Tooling), ensure absolute consistency between the *defined architecture* (docs/prompts) and the *implemented behavior* (code/scripts).**

Never allow the system to "do what I say, not what I do"—if a standard is written, the implementation must rigorously obey it.

| Check | Requirement |
|:------|:------------|
| **Docs → Code** | Every documented pattern must have a working implementation |
| **Code → Docs** | Every implementation must be documented |
| **Prompt → Behavior** | Agent prompts must match actual agent behavior |
| **Standard → Compliance** | If a rule exists in CLAUDE.md, all components must follow it |

---

# PART II: COMMAND (Intent Layer)

## 2.1 What Commands Are

Commands are **Reusable Prompt Templates**—Markdown files that instruct the Main Agent for the current turn. They are instructions FOR Claude, not messages TO the user.

**Key Principles:**
- Use `$ARGUMENTS` to capture the user's full natural language input
- `argument-hint: [string]` is for UI documentation only (not parsed)
- Commands orchestrate workflows by instructing the Main Agent

---

## 2.2 Command Types

Commands work with both humans and AI agents using natural language:

| Type | Consumer | `disable-model-invocation` | AskUserQuestion |
|:-----|:---------|:---------------------------|:----------------|
| User-Centric | Human only | `true` | Yes |
| Agent-Ready | Specialized Agents | `false` | No |
| Hybrid | Both | `false` | Conditional |

---

## 2.3 Command Permissions

### Tool Restrictions
Commands can use the `allowed-tools` frontmatter to enforce safety or focus.

```yaml
---
description: Read-only codebase explorer
allowed-tools: [Read, Grep, LS, find]
---
```

This restriction cascades: if the Main Agent is restricted to `[Read, Grep]`, any subagents it spawns via the `Task` tool inherit these restrictions.

---

## 2.4 The Skill Tool (Recursive Pattern)

Agents can invoke Commands via the `Skill` tool. This transforms the Command Suite into a **Standard Library** for Agents.

- An Agent handling a feature can call `/commit` to save its work.
- An Agent debugging can call `/test` to verify.

**Syntax:** `Skill(/command-name)` for exact match. Arguments are passed using the command's `$ARGUMENTS` placeholder.

---

# PART III: AGENT (Autonomy Layer)

## 3.1 What Agents Are

Agents are **Specialized Personas** with their own system prompts and optional tool restrictions, launched via the `Task` tool.

**Key Concepts:**
- **Agent vs Subagent:** An Agent is the definition (`agents/*.md`); a "Subagent" is the runtime instance spawned via `Task` tool
- **Model Selection:** Agents can use `haiku` (speed), `sonnet` (balance), `opus` (logic), `default`, or `opusplan` (opus for planning, sonnet for execution)
- **Tool Restriction:** Defined via `tools` field in frontmatter (whitelist)
- **Context Sharing:** Each subagent operates in its own separate context window. They can access session conversation history (read-only) but have their own specialized system prompt. Provide exhaustive context when spawning.
- **Lifecycle:** `SubagentStop` hook triggers when a subagent completes

---

## 3.2 Agent Sovereignty (The Task Tool)

The `Task` tool is the primitive used to spawn subagents.

- **Mechanism:** Commands do not spawn agents directly; they instruct the Main Agent to use the `Task` tool.
- **Invocation:** The Main Agent interprets the Command's natural language instruction (e.g., "Launch the code-reviewer agent...") and invokes the `Task` tool to spawn the requested agent.
- **Why:** This maintains the "Command as Prompt" architecture while enabling agentic behavior.

### Agent Permissions

```yaml
---
name: code-reviewer
description: Analyzes code for quality issues
tools: Read, Grep, Glob, Bash  # Only these tools available
---

# Omitting tools field = inherits ALL tools from main thread
```

**Critical Rule:** If you omit the `tools` field, the agent inherits ALL tools including Read, Write, Edit, Bash, AskUserQuestion, Task, Skill, and all MCP tools.

---

## 3.3 Agent Discovery Protocol

Agents are triggered via **semantic description matching**. Claude Code proactively delegates tasks based on the `description` field.

**Best Practice Format:**
```yaml
---
name: security-reviewer
description: |
  USE when auditing code for security vulnerabilities.
  Specializes in OWASP patterns, injection flaws, and authentication issues.
  Keywords: security audit, vulnerability scan, penetration test
tools: Read, Grep, Glob
---
```

**Discovery relies on:**
- Clear description of **when** to use the agent
- Keywords matching common user intents
- Specific capability statements

> Description-based semantic matching is the primary discovery mechanism. XML `<example>` blocks are optional and only useful for complex disambiguation.

---

## 3.4 Delegation Patterns

**The Physics:** The decision to delegate is based on **Context Gravity** and **Attention Dilution**.

> **The 10-File Heuristic:** If a task requires reasoning about >10 files, it **SHOULD** move to a Delegated Agent to protect the Main Thread's attention focus.

### Pattern 1: Direct (Inline)
**Composition:** `Command + Skill`
- **Use Case:** "Fix this specific function." (Context < 30%)
- **Interaction:** High (Chatty).
- **Context:** Shared with User.

### Pattern 2: Delegated (Task)
**Composition:** `Command → Task → Agent`
- **Use Case:** "Refactor the Auth module." (Context > 50% or >10 files)
- **Interaction:** Autonomous (Fire & Await Report).
- **Context:** Shares session history but uses specialized persona.
- **Note:** Specialized Agents are **Transparent Subprocesses**, not black boxes. Their thoughts and tool uses are visible in logs.

### Pattern 3: Parallel (Multi-Task)
**Composition:** `Command → Task(A), Task(B), Task(C)`
- **Pattern:** Launch 3-4 agents simultaneously via the `Task` tool to handle complexity.
- **Map:** Command splits task ("Launch 3 agents in parallel to audit src/, tests/, and docs/").
- **Execute:** Subagents run in parallel, using their specialized instructions.
- **Reduce:** The Main Agent synthesizes atomic reports into a final answer.

### Pattern Selection Matrix

| Metric | Direct | Delegated | Parallel |
|:-------|:-------|:----------|:---------|
| **Files Involved** | 1-5 | 5-20 | 20+ |
| **Duration** | <1 min | 1-5 mins | 5+ mins |
| **User Input** | Required | Forbidden | Forbidden |
| **Context State** | Shared | Spec. Persona | Multi-Persona |

---

# PART IV: SKILL (Protocol Layer)

## 4.1 What Skills Are

Skills are **Knowledge Bases**—passive procedural knowledge packages. They provide standards, templates, and methodologies that agents "put on" like a lens to view a task.

**Key Principle:** Skills are cookbooks, not wizards. They inform but do not execute.

---

## 4.2 Skill Anatomy

### Directory Structure
```
skill-name/
├── SKILL.md          # Required: Instructions + Metadata
├── scripts/          # Optional: Executable scripts
├── references/       # Optional: On-demand documentation
└── assets/           # Optional: Templates, data files
```

---

## 4.3 Progressive Disclosure

Skills use a **3-level loading hierarchy** to minimize context usage:

| Layer | Budget | When Loaded |
|-------|--------|-------------|
| **Metadata** (`name` + `description`) | ~100 tokens | Startup |
| **Instructions** (SKILL.md body) | <5000 tokens | On activation (description match) |
| **Resources** (scripts/, references/, assets/) | Unlimited | On-demand when referenced |

**Resource Types:**
- `references/` - Text loaded into context (API docs, standards)
- `assets/` - Files used in output (templates, images)
- `scripts/` - Executed via `Bash` without being read into context (infinite token budget for procedural logic)

---

## 4.4 Writing Style Requirements

1.  **Imperative/Infinitive Form:** Write SKILL.md body using verb-first instructions.
    -   ✅ Correct: "Verify indentation using 2-space standard."
    -   ❌ Incorrect: "You should check the indentation."
2.  **Third-Person Description:** The YAML `description` determines when the skill is loaded.
    -   ✅ Correct: "This skill should be used when..."
    -   ❌ Incorrect: "Use this skill when..."

---

## 4.5 Discovery Tiering Matrix

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

## 4.6 YAML Frontmatter

```yaml
---
name: skill-name          # Required. Max 64 chars, lowercase, hyphens only
description: |            # Required. Follow Discovery Tiering Matrix
  Description text here
allowed-tools: Read Edit  # Optional. Space-delimited pre-approved tools
context: fork             # Optional. Run in isolated sub-agent context
agent: security-reviewer  # Optional. Bind to agent persona when forked
user-invocable: true      # Optional. Show in slash menu (default: true)
disable-model-invocation: false  # Optional. Block Skill tool invocation
hooks:                    # Optional. Skill-scoped hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
---
```

---

## 4.7 Security & Execution

Scripts must be self-contained, include error messages, and handle edge cases. Validate all inputs. Run in isolated environments when possible.

---

## 4.8 Skill Permissions

```yaml
---
name: safe-reader
description: Read files safely without modifications
allowed-tools:
  - Read
  - Grep
---

# Skills use allowed-tools to restrict tools during skill execution
```

---

# PART V: RUNTIME MECHANICS

## 5.1 Permission System

Claude Code implements a **defense-in-depth permission model** with two primary restriction mechanisms:

| Restriction Type | Used By | Syntax | Behavior |
|:-----------------|:--------|:-------|:---------|
| **`tools`** | Agents | `tools: Read, Grep, Bash` | Defines what tools agent CAN use (whitelist) |
| **`allowed-tools`** | Commands/Skills | `allowed-tools: [Read, Grep]` | Restricts tools DURING execution (blacklist) |

### Permission Modes

| Mode | Behavior | Use Case | Security |
|:-----|:---------|:---------|:---------|
| **`default`** | Prompts for each tool | Development | High |
| **`acceptEdits`** | Auto-approves file operations | Code editing | Medium |
| **`plan`** | Read-only analysis | Code review | High |
| **`dontAsk`** | Auto-deny unless pre-approved | CI/CD | High |
| **`bypassPermissions`** | All tools approved | Trusted environments | **Very Low** |

**Best Practice:** Use `plan` mode for analysis agents to ensure read-only operations.

### Common Permission Vulnerabilities

#### 1. Permission Escalation
```yaml
# ❌ Vulnerable: Agent inherits all tools
---
name: file-reader
description: Reads configuration files
# tools field omitted
---

# ✅ Fixed: Explicit restriction
---
name: file-reader
description: Reads configuration files
tools: Read, Grep  # Only read-only access
---
```

#### 2. Bash Command Injection
```yaml
# ❌ Vulnerable: Wildcard command
permissions:
  allow: ["Bash(npm *)"]  # Allows: npm && rm -rf /

# ✅ Fixed: Specific commands
permissions:
  allow: ["Bash(npm run build)", "Bash(npm test)"]
```

### Permission Audit Checklist

**Subagents:**
- [ ] `tools` field specified (never rely on inheritance)
- [ ] Only necessary tools granted
- [ ] Sensitive tools (Bash, Edit) require explicit approval
- [ ] Model selection appropriate for security needs

**Commands:**
- [ ] `allowed-tools` defined for safety
- [ ] Interactive commands restricted appropriately

**Skills:**
- [ ] `allowed-tools` defined for sensitive operations
- [ ] Read-only operations properly restricted

---

## 5.2 Hooks (Governance)

Hooks are the **Immune System**—interception, safety, context injection. Never heavy work.

| Hook | Trigger | Use Case |
|:-----|:--------|:---------|
| `SessionStart` | New session begins | Initial context setup |
| `UserPromptSubmit` | Before prompt processing | Auto-activate skills, inject context |
| `PreToolUse` | Before tool execution | Block risky ops, modify inputs |
| `PermissionRequest` | Permission dialog shown | Permission handling |
| `PostToolUse` | After tool success | Run linters, formatters |
| `Notification` | System notifications | External alerting/logging |
| `Stop` | Main agent finishes | Final cleanup |
| `SubagentStop` | After task completion | Synthesis, teardown |
| `PreCompact` | Before context compaction | Protect critical history |
| `SessionEnd` | Session ends | Final state cleanup |

### Hook Safety Standards
- **Portability:** ALWAYS use `${CLAUDE_PLUGIN_ROOT}` for script paths. Never hardcode absolute paths.
- **Input Hygiene:** Command hooks MUST read stdin as JSON, validate inputs using `jq`, and quote ALL variables.
- **Output Protocol:** Return valid JSON (`continue`, `systemMessage`). Use Exit Code `0` for success, `2` for blocking errors.
- **Prompt First:** Prefer Prompt-Based hooks for logic requiring reasoning; reserve Command hooks for performance/determinism.

---

## 5.3 MCP Integration

Plugins connect to external services (databases, APIs, browsers) via the **Model Context Protocol (MCP)**.
- **Configuration:** Managed via `.claude-plugin/plugin.json` in the plugin root.
- **Discovery:** Tools provided by MCP servers are automatically discovered by Claude when the plugin is active.
- **Scopes:** MCP servers can be configured at local, project, or user level.

### MCP Security

```yaml
# ✅ Good: Specific domain restrictions
allowedMcpServers:
  - serverUrl: "https://api.githubcopilot.com/mcp/"
  - serverCommand: ["npx", "-y", "approved-package"]

# ❌ Bad: Wildcard access
allowedMcpServers:
  - serverUrl: "*"
```

**MCP Security Checklist:**
- [ ] **Restrict by URL pattern** - Never use wildcard `*`
- [ ] **Audit third-party servers** - Review server code before allowing
- [ ] **Use OAuth tokens** - Properly scoped authentication
- [ ] **Command-based restrictions** - For stdio servers
- [ ] **Regular permission reviews** - Audit MCP access

---

## 5.4 Token Budget & Context Gravity

| Component | Budget | Notes |
|:----------|:-------|:------|
| Command description | <200 tokens | AI discovery |
| Agent description | <500 tokens | Include examples for Tier 1 |
| Skill description | <200 tokens | Keywords for activation |
| SKILL.md body | <5000 tokens | ~500 lines max |
| Reference files | Unlimited | On-demand loading |

**Context Gravity Rule:** If phase requires >5 source files → use Delegated pattern.

---

## 5.5 Interaction Graph

```mermaid
graph TB
    User["👤 User"]
    MainAgent["🤖 Main Agent<br/>(Claude)"]
    Commands["📋 Commands<br/>(Orchestrator)"]
    Subagents["🔧 Subagents<br/>(Agent-bound Skills)"]
    Skills["📚 Skills<br/>(Atomic Capabilities)"]
    Tools["🛠️ Tools<br/>(Read, Write, Bash, etc.)"]
    Hooks["🪝 Hooks<br/>(Event Interception)"]

    User -->|"Invokes (/skill)"| Skills
    User -->|"Invokes (/command)"| Commands
    User -->|"Natural Language"| MainAgent

    Commands -->|"Orchestrates"| Skills
    Commands -->|"Injects Instructions"| MainAgent

    MainAgent -->|"Spawns via Task tool"| Subagents
    MainAgent -->|"Auto-loads via Description"| Skills
    MainAgent -->|"Uses"| Tools

    Skills -->|"context: fork"| Subagents
    Skills -->|"Auto-discoverable"| MainAgent

    Subagents -->|"Return Results"| MainAgent
    Subagents -->|"Auto-load"| Skills
    Subagents -->|"Uses"| Tools

    Tools -->|"Triggers"| Hooks
    Hooks -.->|"Blocks/Warns/Injects"| MainAgent
```

---

# PART VI: MAINTENANCE

## 6.1 Project Hygiene (Mandatory)

- **Never create temporary markdown reports** - Output findings directly in responses, not files
- **Never create diagnostic/analysis files** - Use direct communication instead
- **Clean up after operations** - Remove any temp files, caches, build artifacts
- **Move to .attic IN THE ROOT PATH (thecattoolkit/.attic) instead of deleting** - When removing code/files during refactoring
- **No file pollution** - If a file wasn't requested, don't create it

IMPORTANT: If you have access to claude-code-guide agent, you MUST use it PROACTIVELY. Spawn as much parallel background claude-code-guide agents with short and concise prompts descriptions as needed to verify and confirm any doubt.

---

## 6.2 File Path Standards

**Rule:** Skills are self-contained and portable.

### Within Skills
```
✅ assets/templates/document.md
✅ references/format-guide.md
```

### Cross-Component
```
✅ "from the planning skill"
✅ "the guide.md in the architect skill references"
❌ ../../../other-skill/assets/template.md
❌ plugins/plugin/skills/skill/...
```

### @ Syntax
Only works in Slash Commands / User Input. FORBIDDEN in static Skill/Agent files.

---

## 6.3 Workflow Patterns

**Core Pattern:** Uninterrupted Flow eliminates Stop-and-Wait.

```
PLANNING: Deep Discovery → 100% clarity
    ↓
EXECUTION: Agent Delegation → Self-verify → Log → Agent Delegation → Self-verify → Log
    ↓
REVIEW: Phase boundary (SUMMARY.md with evidence)
```

- **Planning:** Use AskUserQuestion to gather requirements.
- **Execution:** Avoid AskUserQuestion; delegate to agents.
- **Note:** These are recommended patterns, not strict requirements.

---

## 6.4 Forbidden Patterns

<forbidden_pattern>
**Caller Assumption:** Agent assumes specific command invoked it.
**Fix:** "You have been tasked with X" not "Called by /command".
</forbidden_pattern>

<forbidden_pattern>
**Command-Only Logic:** Business logic only in Command, not Skill.
**Fix:** Move logic to Skill. Command references, Agent reads.
</forbidden_pattern>

<forbidden_pattern>
**Cross-Skill Coupling:** Skill A references Skill B via relative path.
**Fix:** Self-contained skills. Use natural language: "from the planning skill".
</forbidden_pattern>

<forbidden_pattern>
**Stop-and-Wait:** Pausing for human input during execution.
**Fix:** Uninterrupted Flow. HANDOFF.md for blockers only.
</forbidden_pattern>

<forbidden_pattern>
**Active Skills:** AskUserQuestion or execution steps in Skill.
**Fix:** Skills are passive standards. Move workflow to Command.
</forbidden_pattern>

<forbidden_pattern>
**Direct Bloat:** Using Direct (Inline) when context >70% full.
**Fix:** Delegate to Agent to preserve main context.
</forbidden_pattern>

<forbidden_pattern>
**Implicit Context:** Assuming specialized agent knows project from main thread.
**Fix:** Explicitly pass project-brief.md and roadmap.md to agent.
</forbidden_pattern>

<forbidden_pattern>
**Over-Prescription:** Micromanaging tool usage ("run ls then grep").
**Fix:** Goal-oriented: "Find the controller".
</forbidden_pattern>

<forbidden_pattern>
**Hardcoded Paths:** Absolute or exit-relative paths in skills.
**Fix:** Relative from skill root or natural language for cross-component.
</forbidden_pattern>

<forbidden_pattern>
**Role Confusion:** Commands doing agent analysis, agents doing user interaction.
**Fix:** Commands orchestrate, Agents execute, Skills provide methodology.
</forbidden_pattern>

<forbidden_pattern>
**The "Black Box":** Assuming specialized agents are invisible/unreachable.
**Fix:** Treat them as Sub-Processes that report back logs and results.
</forbidden_pattern>

<forbidden_pattern>
**Tool Citation Anti-Pattern:** Citing specific tool names in documentation.
**Fix:** Describe the behavior abstractly. Focus on "ask questions" not "use AskUserQuestion tool".
</forbidden_pattern>

<forbidden_pattern>
**Environment-Specific Coupling:** Hardcoding `model` or `permissionMode` in Agent, Command, or Skill frontmatter.
**Fix:** Remove these fields. These settings are environmental and non-portable; they break compatibility with custom endpoints (Zai, Minimax) and sandbox configurations. Trust the runtime or global settings to handle model selection and safety levels.
</forbidden_pattern>

---

## 6.5 Glue Code Detection & Removal

Glue code is the unnecessary middleman layer between intent and execution.

### The 10-Line Rule

**If glue code exceeds 10 lines, it's almost certainly an anti-pattern.**

| Component Type | Acceptable Complexity | Red Flag |
|:---------------|:---------------------|:---------|
| **Command Wrapper** | <10 lines | >10 lines |
| **Skill Wrapper** | <5 lines | >10 lines |
| **Agent Pass-through** | <5 lines | >10 lines |

### Anti-Pattern Catalog

#### Anti-Pattern 1: Wrapper Commands
```yaml
# Problem: Command exists only to call another command
---
name: analyze-project
description: "Analyzes project structure"
---
# Just calls /analyze with different parameters
Task(agent="analyzer", params=parsed_args)

# ✅ Solution: Merge the commands
---
name: analyze
description: "Analyzes project with optional deep mode"
---
```

#### Anti-Pattern 2: Skill Composition
```yaml
# Problem: Skill A requires Skill B to function
---
name: code-formatter
description: "Format code using project standards"
---
# Reads standard from another skill
standards = load_from("project-standards")

# ✅ Solution: Inline the standard
---
name: code-formatter
description: "Format code using industry standards"
---
# 2-space indentation, LF endings, trailing newline
```

#### Anti-Pattern 3: Agent Delegation Chain
```
# Problem: A → B → C → D
# ✅ Solution: A → D directly
```

### Refactoring Strategies

#### Strategy 1: Collapse Layers
```
Before: Command → Agent → Function
After:  Command → Function
```

**Steps:**
1. Identify the middle layer (Agent/Command)
2. Check if it adds logic or just passes through
3. If pass-through → remove the middle layer
4. Call the underlying function directly

#### Strategy 2: Inline Standards
```
Before: Skill A → Skill B (for standards)
After:  Skill A contains standards directly
```

**Steps:**
1. Extract standards from Skill B
2. Inline into Skill A
3. Make Skill A self-contained
4. Delete Skill B if unused

#### Strategy 3: Merge Commands
```
Before: /command-a, /command-b (similar purpose)
After:  /command (with flags/options)
```

**Steps:**
1. Identify commands with overlapping purposes
2. Merge into single command
3. Use natural language for variations
4. Delete redundant command

### Performance Impact

**Glue code adds (estimated):**
- Latency: Each layer ≈ +50-100ms
- Context overhead: Each wrapper ≈ +50-200 tokens
- Maintenance cost: Each layer must be updated

### When Glue Code is Acceptable

Only in these rare cases:

1. **Security Layer** - Deliberate permission isolation
2. **Legacy Compatibility** - Temporary bridge during migration
3. **Aggregation** - Multiple sources combined into one API
4. **Transformation** - Actual data transformation, not just pass-through

### Glue Code Metrics

| Metric | Target | Warning | Critical |
|:-------|:-------|:--------|:---------|
| **Command Size** | <10 lines | 10-20 lines | >20 lines |
| **Delegation Depth** | 1 level | 2 levels | 3+ levels |
| **Skill References** | 0 per skill | 1-2 per skill | 3+ per skill |
| **Wrapper Functions** | 0 | 1-2 | 3+ |

### Prevention Checklist

- [ ] **Every wrapper must add logic** - If it just passes through, remove it
- [ ] **Skills are self-contained** - No `../other-skill/` references
- [ ] **Commands have unique purposes** - Don't create variations
- [ ] **Agents are specialized** - Don't create generic delegators
- [ ] **Review 10-line rule** - If >10 lines, justify or refactor

---

## 6.6 Prompt Engineering for Orchestration

Commands instruct Claude using natural language prompts, not XML parsing.

### Writing Orchestration Prompts

**Single Agent Delegation:**
```
Launch an agent to analyze the authentication flow in src/auth/.
The agent should identify security vulnerabilities and report findings.
```

**Parallel Swarm Execution:**
```
Launch 4 agents in parallel to:
- Agent 1: Audit src/api/ for input validation
- Agent 2: Audit src/auth/ for session handling  
- Agent 3: Audit src/db/ for SQL injection
- Agent 4: Audit src/utils/ for unsafe operations

Each agent reports independently. Synthesize findings after all complete.
```

**Context Injection (Native):**
```
Here is the current project brief:
[content of BRIEF.md]

Analyze the codebase against these requirements.
```

> **Key Insight:** Claude natively understands "launch X agents in parallel" instructions. No special syntax required.

---

## 6.7 The .cattoolkit Root

All runtime artifacts stored in `.cattoolkit/`:
- **Session State**: `.cattoolkit/context/`
- **Project Management**: `.cattoolkit/planning/`

---

# Documentation References

- **docs/COMMAND-OVERVIEW.md** - Command standards and patterns
- **docs/SKILLS-OVERVIEW.md** - Skill development guide
- **docs/HOOKS_OVERVIEW.md** - Hook system and events
- **docs/IMPLEMENTATION-GUIDE.md** - Full implementation details
- **docs/GOLD_STANDARD_COMMAND.md** - Command reference examples
- **docs/INTERACTION_GRAPH.md** - Component interaction map
- **README.md** - Installation and marketplace
