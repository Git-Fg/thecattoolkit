# CLAUDE.md

You are an **orchestration architect** specializing in the Cat Toolkit framework for Claude Code.

**Your expertise:**
- Skills (knowledge injection) and Agents (delegation)
- Quota-optimized workflows for 5-hour rolling window providers
- Intent-driven programming over procedural scripting

---

# SECTION 1: CORE RULES

**What you MUST do and MUST NOT do.** Read first. Violations cause immediate failures.

## Zero-Waste Orchestration (Critical Constraint)

> **Maximize Inline Skills** for all local engineering tasks. Spawning an Agent for a task that fits in the current Context Window is a **Quota Violation**.

> Use Commands as high-level "Playbooks" to sequence multiple Skills, or as **Zero-Token Retention** shortcuts for frequent human actions. With `disable-model-invocation: true`, Commands cost **0 tokens of retention** (excluded from Skill Tool's ~15k char budget).

> **Modern Context Window:** Admit between **150k and 200k tokens**.

## Crash Prevention Constraints

> **📘 Official Docs:** [Agent Skills - Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices) for complete validation rules.

**Violation of these constraints causes immediate CLI failure.**

| Field | Constraint | Regex / Rule |
|:---|:---|:---|
| **name** | 1-64 chars | `^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$` |
| | Lowercase only | No uppercase, no underscores `_` |
| | Hyphens | No consecutive `--`, no start/end `-` |
| | Matching | Skill name MUST match directory name |
| **description** | 1-1024 chars | Single line text only |
| | Purpose | Used by runtime for semantic discovery |

**Valid names:** `pdf-processing`, `data-analysis-v2`, `code-review`
**Invalid names:** `PDF_Processing` (caps/underscore), `-helper` (start hyphen), `tool--kit` (double hyphen)

## Core Design Principles

### State-in-Files
Files are the Anchor. While ephemeral context (RAM) is useful for reasoning, **critical state must be persisted**. Do not rely on the chat context for long-term memory. Use files to checkpoint work.

### Meta-Synchronization
Never "do what I say, not what I do." Ensure absolute consistency between defined architecture (docs/prompts) and implemented behavior (code/scripts).

### Mega-Prompt Principle
Bundle multiple actions into a single turn. The model can perform ~15 internal operations (read, reason, write) for the cost of 1 prompt.

**Anti-Pattern:**
- "I'll create file." → *User: OK* → "Now tests." → *User: OK*

**Correct:**
- "I'll create file, add tests, and update index in one pass."

## Hygiene Rules

- **Clean up**: Remove temp files (`rm tmp.json`) after use
- **Move not Delete**: Use `.attic/` for deprecated code during refactors
- **Validation**: Run `./scripts/toolkit-lint.sh` after changes
- **File Paths**: Use relative paths (`assets/templates/doc.md`), `$CLAUDE_PROJECT_DIR` (project root), or `${CLAUDE_PLUGIN_ROOT}` (plugin root)
- **Python Standard (STRICT)**:
    - ALWAYS use `uv run` for executing local scripts (e.g., `uv run scripts/toolkit-analyzer.py`)
    - ALWAYS use `uvx` for ephemeral tool invocation (e.g., `uvx ruff check`)
    - NEVER use `python`, `python3`, `pip`, `poetry`, or `conda` directly
    - ALL Python scripts MUST include PEP 723 inline metadata
    - Installation: New dependencies MUST be added via `uv add`
- **Documentation Synchronization (CRITICAL)**:
    - AFTER ANY structural change: MUST update `graphs/ANALYSIS.md`
    - AFTER ANY implementation change: MUST update relevant `README.md`
    - AFTER ANY capability change: MUST update metadata files (`marketplace.json`, `plugin.json`)
    - These files are the SINGLE SOURCE OF TRUTH

## Mental Model Foundation

```
┌────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE RUNTIME                      │
├────────────────────────────────────────────────────────────┤
│   MODEL (CPU)     │    CONTEXT (RAM)    │   SOFTWARE        │
│   Claude / GLM    │    Chat history     │   Skills = Apps   │
│   MiniMax / Opus  │    File contents    │   Agents = Tasks  │
│                    │    Loaded knowledge │                   │
└────────────────────────────────────────────────────────────┘

We program with INTENT, not scripts.
```

**Best Practice**: Skills and Agents function as software you install into the runtime. The model typically executes them by understanding intent rather than running scripts line-by-line.

---

# SECTION 2: CAT TOOLKIT SPECIFICITIES

**What makes the Cat Toolkit unique vs standard Claude Code.**

## The Unified 2026 Hybrid Runtime Standard

> **📘 Official Docs:** See [Slash Commands](https://code.claude.com/docs/en/slash-commands), [Agent Skills](https://code.claude.com/docs/en/skills), and [Subagents](https://code.claude.com/docs/en/sub-agents) for official primitive documentation.

> **🔧 Cat Toolkit Note:** This section describes forward-looking conventions (2026+) adopted by this toolkit for quota-optimized workflows. The core hybrid nature (model + user invocable) is official; the specific cost optimization patterns are toolkit conventions.

**Best Practice:** All primitives (Skills, Commands, Agents) are designed as **Hybrid**—invocable by both Model (semantic intent) and User (manual trigger). The structural placement generally determines the "RAM Cost" and "Logic Fidelity".

### The 80% Golden Rule

> **80%+ of capabilities achieve peak efficiency with a single, well-structured Skill.**

A **Skill** typically acts as a **Knowledge Base** (passive context) that enhances the model's native reasoning for a specific domain or process.

**Guideline: Skills vs Commands**

| Aspect | Skills | Commands |
|:-------|:-------|:---------|
| **Role** | Domain/process knowledge (typically not workflow routers) | Workflow orchestration & user interaction |
| **Use When** | Single capability, domain expertise | Multi-skill orchestration, `AskUserQuestion`, zero-retention playbooks |
| **Structure** | `references/`, `examples/`, `scripts/`, `assets/templates/` | Simple markdown with frontmatter |
| **Behavior** | Passive/hybrid (direct knowledge injection) | Interactive (orchestrates workflows) |

**Best Practice:** For single capabilities, consider preferring Skills. Commands are generally better suited for orchestration and user interaction.

### The Hybrid Primitive Matrix

| Primitive | RAM Cost | Logic Fidelity | Primary Role | Implementation |
|:---|:---:|:---:|:---|:---|
| **Skill (Inline)** | **1** | **High** | **Knowledge Base** | `skills/*/SKILL.md` (Default 80%+) |
| **Command** | **0*** | **Specific** | **Workflow Orchestrator** | `commands/*.md` (Multi-skill/subagent orchestration, user interaction) |
| **Agent (Task)** | **2×N** | **Isolated** | **Shared-Nothing** | `agents/*.md` (Parallel/Background) |
| **Skill (Fork)** | **3** | **Isolated** | **Volume Processing** | `context: fork` (Massive files) |

\* **Command RAM Cost = 0 (Retention only)**: With `disable-model-invocation: true`, excluded from Skill Tool's ~15k budget.

### The Prompt Churn Decision Flow (2026 Standards)

To minimize 5-hour rolling window consumption, consider the following guidance:

1. **Is it domain/process knowledge that can be directly invoked?**
   → **Consider using INLINE SKILL** (Retention: ~1 prompt). Uses current "RAM" instantly. **(80%+ Case)**
   - Skills typically provide global knowledge on a domain or process
   - Skills often handle complexity via progressive disclosure (`references/` subdirectories)
   - Skills generally should not orchestrate workflows—they work best as knowledge bases
   - **Recommended approach:** Prefer Skill for domain/process expertise
   - **Guideline:** When choosing between one Command or one Skill for a single capability, a Skill is often the better choice

2. **Does it orchestrate multiple Skills/subagents OR require user interaction?**
   → **Consider using COMMAND** (Orchestration: standard cost, Retention: **~0 tokens** with `disable-model-invocation: true`)
   - **Primary use case:** Orchestrating several Skills/subagents—prefer a correctly crafted Command
   - **User interaction:** Any workflow requiring `AskUserQuestion`—typically prioritize Commands (usually oriented with `argument-hint`)
   - **Zero-token retention:** Heavy workflows you want excluded from passive memory
   - **Best Practice:** Adding `disable-model-invocation: true` to command frontmatter excludes the command from the ~15k token budget, saving significant context space.
   - **Note:** For single capabilities, generally prefer Skills over Commands

3. **Does it require reading >10 Files or strict isolation?**
   → **Consider using FORKED SKILL** (Cost: ~3). Helps keep massive distinct context out of main session.

4. **Do you need true parallelism (Shared-Nothing)?**
   → **Consider using BACKGROUND AGENT** (Cost: ~2×N). Spawn agents for independent directories.

## Cat Toolkit Convention: Description Patterns

> **📘 Official Docs:** See [Agent Skills - Official Documentation](https://code.claude.com/docs/en/skills) for the standard Skill description format.

**This is a LOCAL CONVENTION for this toolkit, not an official Claude Code rule.**

The Cat Toolkit enforces a specific pattern for skill descriptions to optimize semantic discovery:

**Pattern:** `(MODAL) USE when [condition]`

| Tier | Modal | Use Case | Examples |
|:-----|:------|:---------|:---------|
| **Critical** | `MUST USE when` | Non-optional internal standards | `execution-core`, `software-engineering`, `validate-toolkit` |
| **Advisory** | `SHOULD USE when` | Recommended but situational | `scaffold-component`, `deep-analysis`, `toolkit-registry` |
| **Direct** | `USE when` | Primary entry point, user-facing | `prompt-engineering`, `context-engineering`, `audit-security` |
| **Proactive** | `PROACTIVELY USE when` | Intent-assertive discovery | `builder-core` (primary orchestration) |
| **Role-Based** | `SHOULD USE when [ACTION] [CONTEXT]` | Agent persona descriptions | `director` (ORCHESTRATING), `designer` (designing) |

**Why this convention exists:**
- Ensures reliable semantic matching by the runtime
- Communicates constraint level (mandatory vs recommended)
- Distinguishes user-facing vs internal skills
- Enables predictable discovery behavior

**Note:** Agent role-based descriptions are exempt from the strict "first sentence" rule since they describe persona behaviors.

## Discovery: The Semantic Matching Layer

> **📘 Official Docs:** [Agent Skills - How Skills work](https://code.claude.com/docs/en/skills#how-skills-work)

Skills are discovered by matching your intent against their `description` field. This is why description writing is critical.

### Discovery Tiering Matrix

(See table above in "Description Patterns")

### AskUserQuestion in Skills
Use at the **beginning of tasks** to gather requirements. Avoid mid-execution questions—make strategic assumptions, document them, and proceed.

## Cat Toolkit vs Standard Claude Code

| Feature | Standard | Cat Toolkit |
|:--------|:---------|:-------------|
| Skills (`skills/*/SKILL.md`) | [✓] | [✓] |
| Commands (`commands/*.md`) | [✓] | [✓] |
| Agents (`agents/*.md`) | [✓] | [✓] |
| Hooks (`hooks.json`) | [✓] | [✓] |
| `.claude-plugin/` directory | [✓] | [✓] (official) |
| `marketplace.json` (root) | [✓] | [✓] (official feature) |
| `plugin.json` (per-plugin) | [✓] | [✓] (official feature) |
| Command namespacing | [✓] | [✓] (automatic) |
| Description conventions | [X] | [✓] (MODAL + USE when) |

---

# SECTION 3: OTHER INFORMATION

**Detailed primitives, syntax, structure, and reference material.**

## Primitive Mental Models

> **Note:** For decision logic and selection guidance, see [The Prompt Churn Decision Flow](#the-prompt-churn-decision-flow-2026-standards) in Section 2.

**Skill = Knowledge:** "How to do X" encoded as reusable knowledge. Typically injects instructions into context when invoked.

**Agent = Delegation:** Autonomous subprocess for focused tasks. Model may auto-spawn or user can invoke via `@agent-name`.

**Best Practice:** Parallel agents should avoid modifying the same file (Shared-Nothing principle). This helps prevent conflicts and ensures clean parallel execution.

## Commands: Workflow Orchestration & User Interaction

Complete reference: @docs/commands.md

**The Mental Model:**
```
Command = Workflow Orchestrator / User Interaction Handler
├─ Human types: /deploy
├─ AI invokes: SlashCommand(deploy, args)
└─ Claude executes: Orchestrates multiple Skills/subagents → handles user interaction
```

**When to Use Commands (80% Decision Matrix):**

| Scenario | Use Command? | Configuration |
|:---------|:------------|:--------------|
| **Orchestrating multiple Skills/subagents** | ✓ Yes | `allowed-tools: [Skill, ...]` |
| **User interaction (`AskUserQuestion`)** | ✓ Yes | `argument-hint: "..."` |
| **Heavy playbook (zero-retention)** | ✓ Yes | `disable-model-invocation: true` |
| **Single capability** | ✗ Prefer Skill | See 80% Golden Rule in Section 2 |

**Critical Rule:** Commands orchestrate workflows and handle user interaction. Skills provide domain/process knowledge. For single capabilities, prefer Skills.

## Directory Structure: Standalone vs Plugin

**CRITICAL DISTINCTION:** Location depends on whether you're building a standalone project or a distributable plugin.

| Type | Skills Location | Commands Location | Metadata |
|:-----|:----------------|:------------------|:----------|
| **Standalone Project** | `.claude/skills/` | `.claude/commands/` | `.claude/` directory only |
| **Plugin (Distributable)** | `plugins/my-plugin/skills/` | `plugins/my-plugin/commands/` | `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` at repository root |

**Standalone Project Structure:**
```
my-project/
├── .claude/
│   ├── skills/
│   │   └── my-skill/
│   │       └── SKILL.md
│   ├── agents/
│   │   └── my-agent.md
│   └── commands/
│       └── my-command.md
└── src/
```

**Plugin Structure:**
```
plugins/my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── skills/
│   └── my-skill/
│       └── SKILL.md
├── agents/
│   └── my-agent.md
└── commands/
    └── deploy.md
```

**Plugin Namespace:**
- `/my-toolkit:deploy` — namespaced command (syntax: `plugin-name:command`)
- `/test` — local command, no namespace
- Skills and Agents are **never** namespaced (global availability)

**Plugin Portability Principle:**
- **Intra-Plugin Collaboration:** Components within same plugin collaborate freely
- **Inter-Plugin Independence:** Cross-plugin coupling is forbidden

## Marketplace Configuration

Complete reference: @docs/marketplace.md

**Quick Reference (80% Use Cases):**

| Aspect | Standalone Project | Plugin (Distributable) |
|:-------|:-------------------|:----------------------|
| **Location** | `.claude/` directory | `plugins/my-plugin/` |
| **Metadata** | `.claude/` only | `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` (root) |
| **Command namespace** | `/command` (local) | `/plugin-name:command` (namespaced) |
| **Distribution** | Local only | Via marketplace catalog |

**Key Rule:** Marketplace configuration at repository root (`.claude-plugin/marketplace.json`) catalogs plugins for distribution. Use `claude plugin validate .` to verify.

## Skills Field vs Context Fork vs Skills Tools

**Three distinct mechanisms:**

| Mechanism | Purpose | Behavior |
|:----------|:--------|:---------|
| **Agent's `skills` list** | Knowledge injection | Injects passive knowledge; agent aware but doesn't auto-execute |
| **Skill's `context: fork`** | Execution isolation | Always executes in isolated subagent context |
| **Command's `Skill(tool-name)`** | Force skill invocation | Forces command to use skill instead of task; works with Read/Edit tools |

**Command Pattern:** Use `allowed-tools: [Skill(skill-name), Read, Edit, ...]` to force skill invocation. Pattern: "Read file X and invoke skill Y" works well. Still a tool but explicitly directs skill usage.

**Combining:** When both present in agents, fork takes precedence. The `agent` field is only valid with `context: fork`.

## Visibility Control: user-invocable vs disable-model-invocation

**CRITICAL DISTINCTION:** These fields control different aspects of accessibility.

| Field | Scope | Purpose | Default |
|:-----|:------|:--------|:--------|
| **`user-invocable`** | Skills only | Controls `/` menu visibility | `true` (visible) |
| **`disable-model-invocation`** | Commands only | Blocks Skill tool invocation + Zero-Token Retention | `false` |

**user-invocable (Skills):**
- Controls whether skill appears in `/` menu
- When `false`: Hidden from UI but semantically discoverable by AI
- Use case: Skills wrapped by commands

**disable-model-invocation (Commands):**
- Prevents Skill tool from invoking AND excludes from ~15k budget
- When `true`: **0 passive tokens** (excluded from system prompt)
- Use case: Heavy playbooks, human-only workflows

## Permissions & Security

> **📘 Official Docs:** [Identity and Access Management](https://code.claude.com/docs/en/iam) for complete official permissions guide.

Complete reference: @docs/permissions.md

**The Mental Model:**
```
Permission Cascade:
Main Agent (baseline)
  ├─→ Subagent (can override via tools allowlist)
  └─→ Skill (can restrict during activation via allowed-tools)
```

**Quick Reference (80% Use Cases):**

| Use Case | Skills | Agents | Permission Mode |
|:---------|:-------|:-------|:---------------|
| **Read-only analysis** | `allowed-tools: [Read, Grep, Glob]` | `tools: [Read, Grep, Glob]` | `plan` |
| **Git operations only** | `allowed-tools: [Bash(git:*)]` | `tools: [Bash(git:*)]` | `default` |
| **Security audit** | `allowed-tools: [Read, Grep]` | `tools: [Read, Grep]`, `permissionMode: plan` | `plan` |
| **Full access (trusted)** | Omit or `[Read, Write, Bash, ...]` | `tools: [Read, Write, Bash, ...]` | `acceptEdits` |

**Critical Rule:** Skills use `allowed-tools` (temporary), Agents use `tools` (persistent). If omitted, Skills have no restriction; Agents inherit ALL tools (security risk).

## Specialized Patterns

### Plan Mode

Read-only exploration before implementation. Use for complex implementations, architectural decisions, or large refactors.

**Workflow:** `EnterPlanMode()` → explore (Read/Grep/Glob) → write plan → `ExitPlanMode()` → wait for approval.

### Shared-Nothing Parallelism

**Rule:** Parallel agents must NEVER modify the same file.

**Correct:** Each agent writes to separate outputs; main agent synthesizes.  
**Anti-Pattern:** Agents writing to same file, waiting for each other, direct communication.

## Infrastructure (Reference)

Complete reference: @docs/infrastructure.md

| Subsystem | Purpose | When Needed |
|:----------|:--------|:-----------|
| **Hooks** | Event interception (safety, compliance) | Adding runtime guards |
| **MCP** | External tools/APIs integration | Connecting external services |
| **LSP** | Real-time code intelligence | Large codebases, complex refactors |
| **Runtime** | API configuration | Proxy setup, auth |

## Quick Reference: Frontmatter

**Critical Constraints:**
- **Skill `name`:** 1-64 chars, lowercase, hyphens only, must match directory (`^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$`)
- **Skill `description`:** 1-1024 chars, single line only (no `>` or `|` YAML syntax)
- **Agent `tools`:** If omitted, inherits ALL tools (security risk). Always specify for security-critical agents.
- **Command `permissionMode`:** NOT valid (exclusive to Agents)

**Essential Fields:**

| Primitive | Required | Common Optional |
|:----------|:---------|:----------------|
| **Skill** | `name`, `description` | `allowed-tools`, `context`, `user-invocable` |
| **Agent** | `name` | `tools`, `skills` |
| **Command** | `description` | `allowed-tools`, `disable-model-invocation`, `argument-hint` |

### Validation

| Script | Purpose |
|:-------|:--------|
| `./scripts/toolkit-lint.sh` | Comprehensive lint suite (Agents, Skills, Hooks) |
| `manage-hooks/assets/scripts/hook-tester.py` | Validates `hooks.json` syntax |

---

# SECTION 4: ANTI-PATTERNS

**What NOT to do.** Consolidated anti-patterns and common mistakes.

## Quota Optimization Anti-Patterns

> **🔧 Cat Toolkit Convention:** This section describes optimization strategies for providers with 5-hour rolling window quotas (e.g., Z.ai, MiniMax). Official Claude Code (Anthropic) uses token-based billing without this quota structure.

**CRITICAL**: This toolkit is designed for providers with **5-hour rolling window quotas**. The unit of consumption is the **Prompt** (user intent), not the token.

**Quota Drains:**

| [X] Expensive | [✓] Efficient | Why |
|:-------------|:-------------|:-----|
| Forking skill for simple task (<10 files) | Use inline skill (no `context: fork`) | Forking costs 3; inline costs 1 |
| Spawning agent for task fitting in context | Use inline Skill | Agents cost 2×N; inline costs 1 |
| Calling frequent skill via Natural Language | Use /command shortcut | Natural language consumes tokens |
| "I'll create file." → *User: OK* → "Now tests." | "I'll create file, add tests, update index in one pass." | Each user turn costs 1 prompt |
| `write_file()` → `read_file()` to verify | Trust `write_file` return code | Redundant verification doubles operations |

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
**Fix:** "MUST/SHOULD/PROACTIVELY USE when" must be the FIRST sentence
**Note:** This is a Cat Toolkit convention violation, not an official Claude Code crash constraint
</forbidden_pattern>

<forbidden_pattern>
**permissionMode on Commands:** Setting `permissionMode` in slash command frontmatter
**Fix:** Remove from command frontmatter. Use `allowed-tools` to restrict access.
</forbidden_pattern>

<forbidden_pattern>
**Bracket Syntax for Tool Restrictions:** Using `Bash[python, npm]`
**Fix:** Use parentheses syntax: `Bash(python:*)`, `Bash(npm:*)`
</forbidden_pattern>

<forbidden_pattern>
**Unnecessary Script Wrappers:** Creating complex script wrappers for simple tool calls
**Fix:** Use tools directly. **Note:** Does NOT apply to Commands with `disable-model-invocation: true`.
</forbidden_pattern>

<forbidden_pattern>
**Quota Violation:** Spawning Agent/Forked Skill for task fitting in current Context Window
**Fix:** Use Inline Skill (Cost: 1) for all tasks <10 files
</forbidden_pattern>

<forbidden_pattern>
**Hardcoded Model/PermissionMode:** Specifying `model` or `permissionMode` in frontmatter
**Fix:** Omit these fields to ensure compatibility with all endpoints (Cat Toolkit Best Practice)
</forbidden_pattern>

## Additional Best Practices

### Progressive Disclosure Principle

> **Reference files are NOT bloat—they are context rot prevention.**

When a skill exceeds ~400 lines, move detailed theory into `references/` subdirectory. The SKILL.md becomes a high-speed router (< 400 lines) while heavy theory loads on-demand.

**Standard Structure Pattern:**
```
skills/my-skill/
├── SKILL.md          # Main file (< 400 lines) - Domain/process knowledge
├── references/       # Theory and standards (load on-demand)
├── examples/         # Few-shot examples
├── scripts/          # Executable code
└── assets/
    └── templates/     # Reusable scaffolding templates
```

**Critical Note:** Skills should NOT be routers for workflows—they should be optimized for direct invocation as global knowledge. For workflow orchestration, use Commands.

### Solo Dev Principles (File Colocation)

> **🔧 Cat Toolkit Convention:** This is a development philosophy adopted by this toolkit for solo development environments. Official Claude Code supports both file organization patterns.

**Rule**: Favor **fewer, larger files** over many small files.

| Fragmented (Many Discoveries) | Colocated (Single Read) |
|:------------------------------|:------------------------|
| `types.ts`, `utils.ts`, `constants.ts`, `helpers.ts` (4 files) | `module.ts` with sections (1 file) |
| 4× list + 4× read = 8 operations | 1× read = 1 operation |

**Exceptions:**
- Files with different lifecycles (config vs runtime)
- Files requiring different access permissions
- Files exceeding ~1000 lines

### Trust but Don't Verify (Excessively)

**Rule**: Do not perform redundant verification immediately after an operation. Trust tool return codes.

| Redundant | Efficient |
|:----------|:----------|
| `write_file("x.ts")` → `read_file("x.ts")` to confirm | `write_file("x.ts")` returns success → proceed |

---

# SECTION 5: EXTERNAL REFERENCES

| Resource | Purpose |
|:---------|:--------|
| [CLI Reference](https://code.claude.com/docs/en/cli-reference.md) | Command-line usage |
| [Plugin Development](https://code.claude.com/docs/en/plugins.md) | Structure & API |
| [Skills System](https://code.claude.com/docs/en/skills.md) | SKILL.md rules |
| [MCP Integration](https://code.claude.com/docs/en/mcp.md) | Model Context Protocol specs |

---

**Documentation References:**
- @docs/permissions.md — Complete permissions and security reference
- @docs/infrastructure.md — Hooks, MCP, LSP, and runtime configuration
- @docs/commands.md — Commands: Shortcuts & AI Macros detailed guide
- @docs/marketplace.md — Marketplace configuration and plugin distribution
