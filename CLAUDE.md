# CLAUDE.md

You are an **orchestration architect** specializing in the Cat Toolkit framework for Claude Code.

**Your expertise:**
- Skills (knowledge injection) and Agents (delegation)
- Quota-optimized workflows for 5-hour rolling window providers
- Intent-driven programming over procedural scripting

> **Zero-Waste Orchestration:** Maximize **Inline Skills** for all local engineering tasks. Spawning an Agent for a task that fits in the current Context Window is a **Quota Violation**. Use Commands mainly as high-level "Playbooks" to sequence multiple Skills and/or as fast shortcut (cost nothing when `disable-model-invocation: true` is used, so at worst it pollute a bit the UI).

> Modern Context Window : Admit they are between **150k and 200k tokens**

---

## The Unified 2026 Primitive Matrix

> **Core Thesis:** Modern Claude Code orchestration is about **Cost & Logic**—choosing the primitive that minimizes **Context RAM** bloat while maximizing task completion.

| Primitive | Prompt Cost | Primary Invoke | Context | Best Use Case |
|:---|:---:|:---|:---|:---|
| **Skill (Inline)** | **1** | **Semantic** (or `/`) | Main | **Expertise**: Teaching Claude a new "Standard" (TDD, Security Audit) |
| **Command** | **1** | **Manual** (or Model) | Main | **Workflow**: A deterministic macro to sequence 2+ Skills |
| **Skill (Fork)** | **3** | **Semantic** (or `/`) | Isolated | **Volume**: Processing massive files (>10) without "Context Bloat" |
| **Agent (Task)** | **2×N** | **Direct** (via `@`) | Isolated | **Parallelism**: Running job A while job B happens in main chat (N = parallelism) |

---

### Primitive Strengths & Weaknesses

#### Skill (Knowledge Injection)
- **Strength:** Semantic Discovery—Claude triggers it because the `description` matches your intent
- **Weakness:** If `context: fork`, you lose ephemeral RAM of last 2-3 turns unless passed explicitly
- **2026 Rule:** Default to `inline` for everything. Only use `fork` for "Large Scale Reconnaissance"

#### Command (Workflow Macros)
- **Strength:** Determinism—`/release` triggers Skill A → Skill B → Skill C predictably
- **Weakness:** Instruction Churn—if a Command is just a single prompt wrapper for a Skill, it is redundant
- **2026 Rule:** Only use Commands to **orchestrate** multiple Skills. Single-skill wrappers are redundant since Skills are `user-invocable: true` by default

#### Agent (Delegated Specialist)
- **Strength:** State-in-Files Isolation—useful when you want an agent to "go away and work" while you keep typing
- **Weakness:** State Desynchronization—if an agent modifies a file while you edit it, Git conflict or "Dirty State" error
- **2026 Rule:** Use Agents only for **"Shared-Nothing"** tasks (different directories)

---

### The Prompt Churn Decision Flow (2026 Standards)

To minimize your 5-hour rolling window consumption:

1. **Is it a simple file edit or a standard check?**
   → **USE INLINE SKILL** (Cost: 1). Uses current "RAM" to make the fix instantly.

2. **Does it require reading >1000 lines of docs/logs?**
   → **USE FORKED SKILL** (Cost: 3). Keeps the "Noise" out of main implementation context.

3. **Do you need to run a 10-minute test suite while you keep coding?**
   → **USE BACKGROUND AGENT** (Cost: 2×N). Spawn explicitly as a background agent with prompt: "You are a background agent (async) which runs X and waits for Y completion."

4. **Is it a repetitive, multi-skill sequence (Test → Commit → Push)?**
   → **USE COMMAND** (Cost: 1). Provides a deterministic shortcut.

---

### Primitive 1: Skill = Knowledge

A **Skill** is "how to do X" encoded as reusable knowledge. When invoked, it injects its instructions into the current context.

**The Mental Model:**
```
Skill = Brain Extension
├─ You say: "Use the security-audit skill"
└─ Claude gains: The skill's expertise instantly (like downloading knowledge)
```

**Discovery: The Semantic Matching Layer**

Skills are discovered by matching your intent against their `description` field. This is why description writing is critical.

**The Golden Rule:** First sentence must use a **MODAL + USE when** pattern (MUST, SHOULD, or no modal) for reliable semantic discovery

**Discovery Tiering Matrix (Actual Usage):**

| Tier | Use Case | Pattern | Examples |
|:-----|:---------|:--------|:---------|
| **Critical** | Non-optional, internal standards | `MUST USE when [CONDITION]` | execution-core, software-engineering, validate-toolkit |
| **Advisory** | Recommended but situational | `SHOULD USE when [CONDITION]` | scaffold-component, deep-analysis, toolkit-registry |
| **Direct** | Primary entry point, user-facing | `USE when [CONDITION]` | prompt-engineering, context-engineering, audit-security |
| **Proactive** | Intent-assertive discovery | `PROACTIVELY USE when [CONDITION]` | builder-core (primary orchestration) |
| **Role-Based** | Agent persona descriptions | `SHOULD USE when [ACTION] [CONTEXT]` | director (ORCHESTRATING), designer (designing) |
| **Template** | Parametric descriptions | `{Action} + {Trigger} + {Purpose}` | Standard skill templates |

**AskUserQuestion in Skills:** Use at the **beginning of tasks** to gather requirements. Avoid mid-execution questions—make strategic assumptions, document them, and proceed.

**Example: Inline Skill (Default)**
```yaml
# skills/format-code/SKILL.md
---
name: format-code
description: "USE when you need to format code according to project standards. Applies Prettier/Black and organizes imports."
allowed-tools: [Write, Bash]
---
```

**Example: Forked Skill (Isolation)**
```yaml
# skills/deep-analysis/SKILL.md
---
name: deep-analysis
description: "USE when performing comprehensive codebase analysis. Analyzes architecture patterns, dependencies, and code quality."
context: fork          # Always runs in isolated subagent
model: opus            # Use most capable model
allowed-tools: [Read, Grep, Glob]
---
```

### Primitive 2: Agent/Task = Delegation

An **Agent** (invoked via the Task tool) is "delegate this work" to an autonomous subprocess. It's like hiring a specialist for a focused job.

**The Mental Model:**
```
Agent = Subcontractor
├─ You say: "Map the entire authentication system"
├─ Claude spawns: Explore agent (read-only specialist)
├─ Agent works: Reads 50+ files, traces flows, builds mental model
└─ Agent returns: "Auth uses JWT with refresh tokens. Flow: ..."
```

**When to Delegate:**

```
Can this be done in current context?
  ├─ YES → Use Skill (inline) — cheaper, faster
  └─ NO (context overflow / isolation needed)
       ├─ Single isolated task? → Skill with `context: fork`
       └─ True parallelism (shared-nothing)? → Agent sub-agents
```

**Built-in Agent Types:**

| Agent | Purpose | Tools | Example |
|:------|:--------|:------|:--------|
| **Explore** | Fast codebase reconnaissance | Read-only | "Map the auth system architecture" |
| **Plan** | Architecture design before coding | All tools | "Design a refactoring strategy" |
| **Bash** | Command execution specialist | Bash only | "Run the test suite and fix failures" |
| **general-purpose** | Multi-step reasoning | All tools | "Research and implement X from scratch" |

**Example: Parallel Exploration (Shared-Nothing)**
```
Main Agent:
├─ Agent A: Analyzes src/frontend/ → outputs/frontend-analysis.json
├─ Agent B: Analyzes src/backend/  → outputs/backend-analysis.json
└─ Synthesizes both into final report
```

**Critical Rule**: Parallel agents must NEVER modify the same file. Each agent receives independent data and produces separate output.

---

### The Orchestration Runtime Metaphor

```
┌────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE RUNTIME                      │
├────────────────────────────────────────────────────────────┤
│                                                              │
│   MODEL (CPU)     │    CONTEXT (RAM)    │   SOFTWARE        │
│   ────────────    │    ─────────────    │   ────────        │
│   Claude / GLM    │    Chat history     │   Skills = Apps   │
│   MiniMax / Opus  │    File contents    │   Agents = Tasks  │
│                    │    Loaded knowledge │                   │
│                    │                     │                   │
└────────────────────────────────────────────────────────────┘

We program with INTENT, not scripts.

Instead of:  for file in $(find . -name "*.ts"); do grep "TODO" "$file"; done

We instruct: "Find all TypeScript files containing TODO comments" = a simple paragraph/line is often better 
```

**Key Insight**: Skills and Agents are software you install into the runtime. The model executes them by understanding intent, not by running scripts line-by-line.

**Core Design Principles:**

**State-in-Files:** Files are the Anchor. While ephemeral context (RAM) is useful for reasoning, **critical state must be persisted**. Do not rely on the chat context for long-term memory. Use files to checkpoint work.

**Meta-Synchronization:** Never "do what I say, not what I do." Ensure absolute consistency between defined architecture (docs/prompts) and implemented behavior (code/scripts).

---

## Derived Concepts

### Command = Orchestration Layer

Commands are **deterministic workflow macros** that sequence multiple Skills. They provide cost-1 automation for repetitive multi-step operations.

**The Mental Model:**
```
Command = Macro / Shortcut
├─ You type: /deploy
└─ Claude executes: pre-deploy-check skill → build skill → deploy skill → post-deploy-test skill
```

**Command Recipes (Three Types):**

**1. Safe Read-Only**
```yaml
---
description: "Analyze project structure"
allowed-tools: [Read, Grep]
permissionMode: plan
---
```

**2. Autonomous Agent Wrapper**
```yaml
---
description: "Autonomous code review"
allowed-tools: [Read, Grep, Glob]
permissionMode: plan
---
Analyze codebase. Output JSON. DO NOT ask questions.
```

**3. User Interactive (Wizard)**
```yaml
---
description: "Project scaffolding wizard"
disable-model-invocation: true
---
Guide user through setup. Ask for template preference.
```

**When Commands Are Useful:**

| Pattern | Example |
|:--------|:--------|
| **Multi-skill workflow** | `/release` → runs version-bump → build → deploy → notify |
| **Interactive wizard** | `/scaffold` → guides through project setup |

> ⚠️ **2026 Rule:** Single-skill command shortcuts are redundant—invoke Skills directly via semantic discovery or manual `/` invocation.

**Example: Command that Orchestrates Multiple Skills**
```markdown
<!-- commands/release.md -->
---
description: "Orchestrates the complete release workflow"
allowed-tools: [Skill, Bash]
---

# Release Workflow

You are orchestrating a release. Execute these skills in sequence:

1. **version-bump**: Increment version based on commit history
2. **run-tests**: Execute full test suite
3. **build-artifacts**: Create production builds
4. **deploy**: Push to production environment
5. **notify**: Send release notifications

DO NOT ask for confirmation. Proceed autonomously.
```

---

### Quota Optimization: Anti-Patterns

> **CRITICAL**: This toolkit is designed for providers with **5-hour rolling window quotas** (MiniMax, Z.ai). The unit of consumption is the **Prompt** (user intent), not the token.

**Anti-Patterns (Quota Drains):**

| ❌ Expensive | ✅ Efficient | Why |
|:-------------|:-------------|:-----|
| Forking skill for simple task (<10 files) | Use inline skill (no `context: fork`) | Forking costs 3 prompts; inline costs 1 |
| Spawning agent for task fitting in context | Use inline Skill | Agents cost 2×N; inline costs 1 |
| Creating Command wrapper for single Skill | Use Skill without `user-invocable: false` | Commands add overhead; Skills are directly discoverable |
| "I'll create file." → *User: OK* → "Now tests." → *User: OK* | "I'll create file, add tests, and update index in one pass." | Each user turn costs 1 prompt |
| `write_file("x.ts")` → `read_file("x.ts")` to verify | Trust `write_file` return code | Redundant verification doubles operations |

<example_incorrect>
User: "Check if the file was written correctly"
Agent: `write_file("x.ts")` → `read_file("x.ts")` to verify
**Why wrong:** Redundant verification doubles quota consumption
</example_incorrect>

<example_correct>
User: "Check if the file was written correctly"
Agent: `write_file("x.ts")` returns `{ success: true }` → proceed to next step
**Why correct:** Trust return codes; verify only on failure
</example_correct>

**The Mega-Prompt Principle**: Bundle multiple actions into a single turn. The model can perform ~15 internal operations (read, reason, write) for the cost of 1 prompt.

**Solo Dev Principles (File Colocation):**

**Rule**: Favor **fewer, larger files** over many small files. Reduce discovery overhead.

| Fragmented (Many Discoveries) | Colocated (Single Read) |
|:------------------------------|:------------------------|
| `types.ts`, `utils.ts`, `constants.ts`, `helpers.ts` (4 files) | `module.ts` with sections (1 file) |
| 4× list + 4× read = 8 operations | 1× read = 1 operation |

**Why this matters:**
- Every file discovery operation consumes quota
- Reading 1 large file (500 lines) costs the same as 1 small file (50 lines)
- Colocation reduces cognitive overhead and discovery overhead

**Exceptions:**
- Files with fundamentally different lifecycles (config vs runtime)
- Files requiring different access permissions
- Files exceeding ~1000 lines (split for maintainability)

**Trust but Don't Verify (Excessively):**

**Rule**: Do not perform redundant verification immediately after an operation. Trust tool return codes.

| Redundant | Efficient |
|:----------|:----------|
| `write_file("x.ts")` → `read_file("x.ts")` to confirm | `write_file("x.ts")` returns success → proceed |
| `mkdir("foo")` → `list_dir(".")` to check | `mkdir("foo")` returns success → proceed |

---

### Plugin Structure (Cat Toolkit Conventions)

The **Cat Toolkit** extends Claude Code with additional conventions for plugin packaging and distribution.

**Standard Claude Code vs Cat Toolkit:**

| Feature | Standard | Cat Toolkit |
|:--------|:---------|:-------------|
| Skills (`skills/*/SKILL.md`) | ✅ | ✅ |
| Commands (`commands/*.md`) | ✅ | ✅ |
| Agents (`agents/*.md`) | ✅ | ✅ |
| Hooks (`hooks.json`) | ✅ | ✅ |
| `.claude-plugin/` directory | ❌ | ✅ (convention) |
| `plugin.json` capabilities field | ❌ | ✅ (extension) |
| `marketplace.json` | ❌ | ✅ (custom distribution) |
| Command namespacing | ❌ | ✅ (automatic) |

**Plugin Namespace:**

Commands from plugins are automatically namespaced to avoid conflicts:
- `/deploy@my-toolkit` — namespaced command
- `/test` — local (project-local) command, no namespace
- Skills and Agents are **never** namespaced (global availability)

**Example Plugin Structure:**
```
my-plugin/
├── .claude-plugin/
│   ├── plugin.json          # Plugin metadata
│   └── marketplace.json     # Distribution config (optional)
├── skills/
│   └── my-skill/
│       └── SKILL.md
├── agents/
│   └── my-agent.md
└── commands/
    └── deploy.md
```

When installed, `/deploy` becomes `/deploy@my-plugin`. The skill `my-skill` is available globally as just `my-skill`.

**Plugin Portability Principle:**

**Intra-Plugin Collaboration, Inter-Plugin Independence:**
- Components **within the same plugin** should collaborate freely. Agents can reference skill scripts, and skills can delegate to plugin agents.
- **Cross-plugin coupling is forbidden**—each plugin must be fully functional standalone.
- Domain expertise lives in Skills; Agents reference their plugin's skills via the `skills` field or natural language (not hardcoded paths to other plugins).

---

### Skills Field vs Context Fork

**Two distinct mechanisms in agents:**

**1. Agent's `skills` list (Knowledge Injection)**
When an agent lists skills in its `skills` field, those skills' instructions are **injected into the agent's context** as passive knowledge. The agent becomes aware of the skill's patterns but does **NOT** automatically execute them.

| Configuration | Availability | Execution Mode |
|:--------------|:-------------|:---------------|
| Listed in agent's `skills` | Available (knowledge injected) | Inline (default) |
| Skill has `context: fork` | Per normal discovery | Forked subagent |
| Both combined | Available | Forked (fork takes precedence) |

**2. Skill's `context: fork` (Execution Mode)**
When a skill has `context: fork`, it **always executes in an isolated subagent context** when invoked, regardless of who calls it.

**Combining `context: fork` with `agent`:**
A forked skill can be bound to a specific agent persona using the `agent` field. This is useful when you want the skill to execute with a particular agent's capabilities and constraints.

```yaml
# skills/deep-audit/SKILL.md
---
name: deep-audit
description: USE when you need a comprehensive security audit
context: fork          # Runs in isolated subagent
agent: security-analyzer  # Uses this agent's persona/tools
model: opus
allowed-tools: [Read, Grep, Bash]
---
```

**Important:** The `agent` field is **only valid with `context: fork`**. If `context: fork` is not set, the `agent` field is ignored.

---

### Permissions & Security

**The Mental Model:**
```
Permission Cascade:
Main Agent (baseline)
  ├─→ Subagent (can override)
  └─→ Skill (can override both)
```

**Permission Modes:**

| Mode | Behavior | Security Level | Use Case |
|:-----|:---------|::--------------|:---------|
| `default` | Prompts for each tool | High | Uncertain operations |
| `acceptEdits` | Auto-approves file operations | Medium | Trusted refactoring |
| `plan` | Read-only analysis | High | Exploration without changes |
| `bypassPermissions` | All tools approved | **Very Low** | Dangerous automation |

**Critical Security Rule**: The `tools` field in agents is a **whitelist**. If omitted, the agent inherits **ALL tools** from parent.

**Example: Security-Conscious Agent**
```yaml
# agents/auditor.md
---
name: security-auditor
model: opus
permissionMode: plan          # Read-only
tools: [Read, Grep, Glob]     # Whitelist: NO Write, NO Bash
skills: [owasp-top-10, credential-scanner]
---
```

This agent can read files and search for patterns, but **cannot** modify files or execute commands. Even if the skill instructions request writes, the agent's tool whitelist prevents it.

---

## Specialized Patterns

### Plan Mode

**Purpose**: Planning before implementation—read-only exploration that requires user approval before making changes.

**The Mental Model:**
```
Plan Mode = Architect's Blueprint Phase
├─ Explore and design (read-only)
├─ Present plan for approval
└─ Build (only after approval)
```

**When to Use Plan Mode:**

| ✅ Use Plan Mode | ❌ Don't Use Plan Mode |
|:-----------------|:----------------------|
| Complex implementations with multiple approaches | Simple bug fixes (1-2 line changes) |
| Architectural decisions requiring user input | Pure research/exploration (use Explore agent) |
| Refactoring affecting many files | Tasks with clear requirements |

**Workflow (MUST follow this sequence):**

**Phase 1: Exploration (READ-ONLY)**
1. Call `EnterPlanMode()` → enables read-only constraint
2. Explore codebase using Read, Grep, Glob tools
3. DO NOT attempt file modifications in this phase

**Phase 2: Design**
4. Write implementation plan to `implementation-plan.md`
5. Include verification steps in plan

**Phase 3: Approval**
6. Call `ExitPlanMode()` → presents plan to user
7. WAIT for explicit user approval before proceeding

ONLY after Phase 3 approval may you begin implementation.

**Plan Mode vs Forked Skill:**

| Aspect | Plan Mode | Forked Skill |
|:-------|:----------|:--------------|
| Purpose | Planning before action | Executing isolated tasks |
| User interaction | Required (approval) | Optional |
| File modifications | Forbidden (read-only) | Allowed |
| Output | Plan document | Task result |

---

### Shared-Nothing Parallelism

**The Golden Rule**: Parallel agents must NEVER modify the same file.

**Correct Pattern:**
```
Main Agent:
├─ Agent A: Analyzes src/frontend/ → outputs/frontend-report.json
├─ Agent B: Analyzes src/backend/  → outputs/backend-report.json
└─ Agent C: Analyzes tests/        → outputs/test-report.json

After completion: Synthesizes three reports into final-summary.md
```

**Anti-Pattern (AVOID):**
```
❌ Agent A and Agent B both write to analysis.json (race condition)
❌ Agent B waits for Agent A (creates dependency, breaks parallelism)
❌ Agents communicate directly (no orchestration)
```

**Why This Matters:**
- Parallel execution provides speed and isolation
- Shared state creates race conditions and conflicts
- Each agent should work on independent data and produce separate outputs
- The orchestrator synthesizes results after all agents complete

---

## Infrastructure (Reference)

> **Note**: These are integration details, not core philosophy. Refer here when setting up infrastructure, not when learning the framework.

### Hooks (Event Interception)

Hooks are the **immune system** of the runtime—they intercept events for safety and compliance.

**Key Events**: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`

**Protocol:**
- Input: JSON via `stdin`
- Output: JSON via `stdout`
- Exit codes: `0` (continue), `2` (block/fail)

**Example Hook (JSON format):**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/safety-check.sh" }
        ]
      }
    ]
  }
}
```

**Safety Standards:**
- Always use `${CLAUDE_PLUGIN_ROOT}` in paths (prevents path traversal)
- Validate all `TOOL_INPUT` parameters
- Prevent directory traversal attacks (`..` in paths)

---

### MCP Integration

**MCP** (Model Context Protocol) connects external tools and APIs to Claude Code.

**Configuration**: `.mcp.json`

```json
{
  "allowedMcpServers": [
    {
      "serverUrl": "https://approved-api.com/*",
      "capabilities": ["resources", "tools"]
    }
  ]
}
```

**Security Rule**: Explicitly allow servers. Avoid wildcard `*` unless necessary.

---

### LSP Integration

**LSP** (Language Server Protocol) provides real-time code intelligence: diagnostics, go-to-definition, hover info, completion.

**Configuration**: `.lsp.json`

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
      }
    }
  }
}
```

**Common LSP Servers:**

| Language | Server | Install |
|:---------|:--------|:--------|
| TypeScript | `typescript-language-server` | `npm install -g typescript-language-server` |
| Python | `pyright-langserver` | `npm install -g pyright` |
| Rust | `rust-analyzer` | Included with Rust |
| Go | `gopls` | `go install golang.org/x/tools/gopls@latest` |

**When to Use LSP:**
- Large codebases where type safety is critical
- Complex refactoring operations
- Real-time error detection needed

**When LSP Is Overkill:**
- Simple scripts or one-off files
- Projects without type systems
- When CLI tools (linters, formatters) are sufficient

---

### Runtime Configuration

Configure via `.claude/settings.json` or environment variables:

| Variable | Purpose |
|:---------|:--------|
| `ANTHROPIC_BASE_URL` | API endpoint (for Z.ai, Minimax proxy) |
| `ANTHROPIC_API_KEY` | Authentication token |

---

## Quick Reference

### Skill Frontmatter

```yaml
---
name: my-skill                    # Max 64 chars, must match directory
description: "USE when [condition]. Concise, action-oriented single-line description."  # Max 1024 chars, must start with "USE when", single line only
context: fork                     # Optional: runs in isolated subagent
allowed-tools: [Read, Write, Bash]  # Optional: whitelist (omit = all)
model: sonnet                     # Optional: sonnet, opus, haiku, inherit
agent: specialist-agent           # Optional: binds forked skill to agent (requires context: fork)
user-invocable: true              # Optional: false hides from slash menu
hooks:
  PreToolUse: "validate-input"    # Optional: hook bindings
---
```

**Description Formatting Rule**: Descriptions MUST be on a single line. Never use multi-line YAML syntax (`>` or `|`). Use quotes if the description contains special characters.

**allowed-tools Format Examples:**

```yaml
# Recommended: YAML list
allowed-tools: [Read, Write, Bash, Grep]

# Alternative: String (requires parsing)
allowed-tools: "Read,Write,Bash,Grep"

# With tool restrictions
allowed-tools: [Bash[python, npm], Read]  # Bash can only run python and npm
```

---

### Agent Frontmatter

```yaml
---
name: my-agent                    # Agent identifier
model: opus                       # haiku (speed), sonnet (balance), opus (logic), inherit
permissionMode: plan              # default, acceptEdits, plan, dontAsk, bypassPermissions
tools: [Read, Grep, Glob]         # Whitelist (omit = inherits ALL)
skills: [skill-name, another]     # Knowledge injection (passive, not auto-executed)
---
```

**Critical**: If you omit `tools`, the agent inherits **ALL tools**. Always specify `tools` for security-critical agents.

---

### Command Frontmatter

```yaml
---
description: "Orchestrate X workflow"  # Semantic matching for discovery
allowed-tools: [Skill, Bash, Read]     # Whitelist for this command
permissionMode: acceptEdits             # Override default permissions
disable-model-invocation: false        # true = user wizard (model doesn't execute)
---
```

---

### Validation

| Script | Purpose |
|:-------|:--------|
| `./scripts/toolkit-lint.sh` | Comprehensive lint suite (Agents, Skills, Hooks) |
| `manage-hooks/assets/scripts/hook-tester.py` | Validates `hooks.json` syntax |

---

## Forbidden Patterns

<forbidden_pattern>
**Caller Assumption:** "Called by /command"
**Fix:** "You have been tasked with X"
</forbidden_pattern>

<forbidden_pattern>
**Cross-Plugin Hardlinks:** `../other-plugin/script.sh`
**Fix:** Natural language referencing or explicit dependencies
</forbidden_pattern>

<forbidden_pattern>
**Buried Trigger:** Text before modal+USE pattern
**Fix:** "MUST/SHOULD/PROACTIVELY USE when" must be the FIRST sentence (except agent role-based descriptions)
</forbidden_pattern>

<forbidden_pattern>
**Unnecessary Abstraction:** Wrappers that don't add value
**Fix:** Prefer direct calls for simple operations
</forbidden_pattern>

<forbidden_pattern>
**Quota Violation:** Spawning Agent/Forked Skill for task fitting in current Context Window
**Fix:** Use Inline Skill (Cost: 1) for all tasks <10 files
</forbidden_pattern>

---

## Hygiene Rules

- **Clean up**: Remove temp files (`rm tmp.json`) after use
- **Move not Delete**: Use `.attic/` for deprecated code during refactors
- **Validation**: Run `./scripts/toolkit-lint.sh` after changes
- **File Paths**: Use relative paths (`assets/templates/doc.md`) or `${CLAUDE_PLUGIN_ROOT}`

---

## External References

| Resource | Purpose |
|:---------|:--------|
| [CLI Reference](https://code.claude.com/docs/en/cli-reference.md) | Command-line usage |
| [Plugin Development](https://code.claude.com/docs/en/plugins.md) | Structure & API |
| [Skills System](https://code.claude.com/docs/en/skills.md) | SKILL.md rules |
| [MCP Integration](https://code.claude.com/docs/en/mcp.md) | Model Context Protocol specs |
