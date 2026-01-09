# CLAUDE.md

Primary operating system and architectural laws for Claude Code when building plugin-based toolkits.

---

## Project Hygiene (Mandatory)

- **Never create temporary markdown reports** - Output findings directly in responses, not files
- **Never create diagnostic/analysis files** - Use direct communication instead
- **Clean up after operations** - Remove any temp files, caches, build artifacts
- **Move to .attic IN THE ROOT PATH (thecattoolkit/.attic) instead of deleting** - When removing code/files during refactoring
- **No file pollution** - If a file wasn't requested, don't create it

---

## I. Agent Skills Standards (agentskills.io)

Skills are specialized procedural knowledge packages that extend agent capabilities.

### Directory Structure
```
skill-name/
├── SKILL.md          # Required: Instructions + Metadata
├── scripts/          # Optional: Executable scripts
├── references/       # Optional: On-demand documentation
└── assets/           # Optional: Templates, data files
```

### Progressive Disclosure

| Layer | Budget | When Loaded |
|-------|--------|-------------|
| Metadata (`name` + `description`) | ~100 tokens | Startup |
| Instructions (SKILL.md body) | <5000 tokens | Activation |
| Resources (scripts/, references/, assets/) | As needed | On reference |

### Writing Style Requirements

1.  **Imperative/Infinitive Form:** Write SKILL.md body using verb-first instructions. This allows skills to be read as **direct instructions by spawned agents**.
    -   ✅ Correct: "Verify indentation using 2-space standard."
    -   ❌ Incorrect: "You should check the indentation."
2.  **Third-Person Description:** The YAML `description` determines when the skill is loaded.
    -   ✅ Correct: "This skill should be used when..."
    -   ❌ Incorrect: "Use this skill when..."

**Key principles:** Keep SKILL.md under 500 lines. Move detailed references to `references/`. Use relative paths from skill root.

### YAML Frontmatter

```yaml
---
name: skill-name          # Required. Max 64 chars, lowercase, hyphens only
description: |            # Required. Follow Discovery Tiering Matrix
  Description text here
license: MIT              # Optional
allowed-tools: Read Edit  # Optional. Space-delimited pre-approved tools
compatibility: python>=3.9 # Optional. Max 500 chars
---
```

### Discovery Tiering Matrix

| Tier | Use Case | Pattern |
|:-----|:---------|:--------|
| **1: High Fidelity** | Complex/fuzzy tasks, LLM capability overlap | `[MODAL] when [CONDITION]. Examples: <example>...` |
| **2: High Gravity** | Safety-critical, governance, mandatory protocols | `[MODAL] USE when [CONDITION].` |
| **3: Utility** | Single-purpose, self-documenting utilities | `{Action Verb} + {Object} + {Purpose}` |

**Selection Rules:**
1. >40% overlap with built-in tools → Tier 1
2. Governance/safety layer → Tier 2
3. Self-documenting name → Tier 3

### Security & Execution

Scripts must be self-contained, include error messages, and handle edge cases. Validate all inputs. Run in isolated environments when possible.

---

## II. Toolkit Standards

### The Trinity Philosophy

The architecture is defined by **Separation of Concerns between Intent, Intelligence, and Protocol**:

| Component | Role | Native Mechanic | Where Logic Lives |
|:----------|:-----|:----------------|:------------------|
| **Command** | Prompt Definition | Markdown file with instructions FOR Claude | Orchestration: defines the "What" via `allowed-tools` |
| **Agent** | Autonomous Capability | Triggered via **Task tool** when `description` matches | Execution: determines the "How" dynamically |
| **Skill** | Passive Knowledge | Auto-loaded if listed in agent frontmatter | Guidelines: defines the "Rules of the Game" |

> **The Skill-Informed Agent Pattern:** Commands are prompt templates that instruct Claude to orchestrate. Skills are passive libraries. Agents are triggered by their `description` frontmatter—this field is the API.

### The .cattoolkit Root
All runtime artifacts stored in `.cattoolkit/`:
- **Session State**: `.cattoolkit/context/`
- **Project Management**: `.cattoolkit/planning/`
- **Hooks**: `.cattoolkit/hooks/`

### Mercenary Isolation

Agents must be **mercenary**: they should never assume they are part of a specific command.

- **Caller Independence:** Agents MUST NOT reference plugin-specific files in system prompts
- **Context via Prompting:** Commands inject content via natural language prompts, not XML envelopes
- **Zero Shared State:** Plugins function independently
- **Eternal Skills:** Commands are transient; Skills are eternal. Domain expertise lives in Skills, not Agent system prompts.

### Progressive Disclosure Enforcement

> **Rule:** Never exceed 500 words in an Agent's system prompt. If more instructions are needed, create a **Skill** and move procedural knowledge to `references/`.

This prevents "Agent Bloat" and keeps system prompts focused on identity and constraints, not methodology.

---

## III. Vibecoding Flow

**Core Innovation:** Uninterrupted Flow eliminates the Stop-and-Wait anti-pattern.

```
PLANNING: Deep Discovery (AskUserQuestion) → 100% clarity
    ↓
EXECUTION: Task → Self-verify → Log → Task → Self-verify → Log
    ↓
REVIEW: Phase boundary (SUMMARY.md with evidence)
```

### Phase Rules

| Phase | AskUserQuestion | Verification |
|-------|-----------------|--------------|
| Planning | MANDATORY | Via user dialog |
| Execution | PROHIBITED | Via CLI (automated) |
| Blocker | N/A | Create HANDOFF.md, exit |

---

## IV. Architectural Primitives

See `docs/VECTOR_vs_TRIANGLE.md` for detailed mechanics and examples.

### Pattern Summary

| Pattern | Composition | Use Case | Context Cost |
|:--------|:------------|:---------|:-------------|
| **Vector** | Command + Skill | Surgical edits, <30% context, user guidance needed | Spends current |
| **Triangle** | Command → Subagent → Skill | Heavy lifting, >50% context, no user input needed | New context |
| **Time-Server** | Command → Async Subagent | Long-running (>1 min), fire-and-forget | Background |
| **Swarm** | Command → [Subagent A, B, C] | Parallel search/audit, non-overlapping work | Multiple new |
| **Lazy Discovery** | Agent + Skill | Self-sufficient context acquisition | Fallback |

### Swarm Orchestration (Map-Reduce)
1. **Map:** Command slices into atomic, non-overlapping assignments
2. **Execute:** Agents produce standardized outputs (no shared state)
3. **Reduce:** Command synthesizes final result

---

## V. Command Types

See `docs/COMMAND-STANDARDS.md` for technical implementation details (Frontmatter, arguments, environment variables).

Commands work with both humans and AI agents using natural language:

| Type | Consumer | `disable-model-invocation` | AskUserQuestion |
|:-----|:---------|:---------------------------|:----------------|
| User-Centric | Human only | `true` | Yes |
| Subagent-Ready | AI subagents | `false` | No |
| Hybrid | Both | `false` | Conditional |

**Key Principle:** Commands are **Intent Envelopes**. Use `$ARGUMENTS` to capture full natural language context. Rigid argument parsing (e.g., `$1 $2`) is an anti-pattern reserved only for Tier 3 utilities.

**Rule of Thumb:** If a command leverages AskUserQuestion, it should be disabled for auto-invocation from AI agents through `disable-model-invocation: true`. Otherwise, omit this frontmatter.

---

## VI. Component Responsibilities

| Component | Primary Role | Permissions |
|:----------|:-------------|:------------|
| **Command** | Orchestration, context gathering, user interaction | Inherits all (restrict via `allowed-tools`) |
| **Agent** | Autonomous execution, framework application | Inherits all (restrict via `tools`) |
| **Skill** | Passive standards, templates, methodology | Asks permission (pre-approve via `allowed-tools`) |

**Constraint:** If Command is deleted, Agent + Skill must still work via Task tool.

**Agent Tool Restriction:** Define `tools` in Agent frontmatter to enforce "Privilege Restriction" (e.g., a `code-explorer` agent should restrict `Write` to prevent accidental drift).

### Complexity vs. Result Decision Matrix

Use this logic to determine where code or logic belongs:

| Question | Answer | Component |
|:---------|:-------|:----------|
| Does this require user interaction? | Yes | **Command** (`AskUserQuestion`) |
| Does this require parallel thinking or Opus-level reasoning? | Yes | **Agent** (subagent) |
| Is this a rule, template, or standard way of doing things? | Yes | **Skill** |
| Is this a long-running background task? | Yes | Delegate to **Agent** via **Command** |

---

## VII. Governance Layer (Hooks)

Hooks are the **Immune System**—interception, safety, context injection. Never heavy work.

| Hook | Trigger | Use Case |
|:-----|:--------|:---------|
| `PreToolUse` | Before tool execution | Block risky ops, modify inputs |
| `PostToolUse` | After tool success | Run linters, formatters |
| `UserPromptSubmit` | Before prompt processing | Auto-activate skills, inject context |
| `SessionStart` | Session begins | Load project context |
| `PermissionRequest` | Permission requested | Custom approval logic |

---

## VIII. Core Laws

### 1. Atomic Independence
Components function standalone. Synergy is a side effect.

- **Agent Sovereignty:** No caller dependency. Self-sufficient discovery.
- **Skill Universality:** Human-readable. No hidden logic. Direct access.
- **Zero-Shared-State:** No cross-plugin file references.

### 2. State-in-Files
Context is ephemeral; files are eternal. Decisions → ADR. Tasks → Status file. If not on disk, it didn't happen.

### 3. Shared-Nothing Parallelism
- Atomic assignments (no dependencies between parallel agents)
- File locking (parallel agents never edit same file)
- Synthesis obligation (orchestrator merges outputs)

### 4. Passive Skills
Skills are cookbooks, not wizards. AskUserQuestion FORBIDDEN in skills. If input missing → agent judgment or HANDOFF.md.

### 5. Native Capabilities
Trust the model. Declarative over procedural. Universal over specific.

> **Rule:** AI Agents inherently understand standard tools (`Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`). ALWAYS use natural language. A simple "read file X from folder Y" is more performant and reliable than micromanagement prompts.

| Avoid | Prefer |
|:------|:-------|
| "Check package.json, then requirements.txt" | "Identify dependency management system" |
| "Run find src -name '*.js'" | "Locate source files using filesystem tools" |
| "Execute these grep commands: ..." | "Search for authentication patterns" |
| "Use the Read tool on path/to/file.ts" | "Read the config file in the src folder" |

### 6. Law of Description
> **"Agents are triggered by their `description` frontmatter. This field is the API."**

The `description` must contain examples of when to trigger. Claude uses this field to determine which agent to spawn via the Task tool.

### 7. Task Tool Primitive
> **"Complex workflows use the Task tool to launch agents."**

Commands orchestrate by instructing Claude to spawn specialists. Native instruction format:
- Single agent: "Launch an agent to analyze the authentication flow"
- Parallel agents: "Launch 3 agents in parallel to audit directories X, Y, Z"

### 8. Hook Safety Standards
- **Portability:** ALWAYS use `${CLAUDE_PLUGIN_ROOT}` for script paths. Never hardcode absolute paths.
- **Input Hygiene:** Command hooks MUST read stdin as JSON, validate inputs using `jq`, and quote ALL variables.
- **Output Protocol:** Return valid JSON (`continue`, `systemMessage`). Use Exit Code `0` for success, `2` for blocking errors.
- **Prompt First:** Prefer Prompt-Based hooks for logic requiring reasoning; reserve Command hooks for performance/determinism.

### 9. Law of Native Delegation
> **"Never write in code what can be described in intent."**

If a task requires searching, analyzing, and editing, do not write a bash script in a command. Describe the goal and launch a specialized agent. Trust the agent to select the tools.

| Anti-Pattern | Native Pattern |
|:-------------|:---------------|
| `!`bash find . -name "*.ts" -exec grep "todo" {} \;`` | "Find all TypeScript files containing TODO comments" |
| Parsing JSON → condition → action in Command | Delegate to agent with goal description |
| Step-by-step tool micromanagement | Goal-oriented natural language delegation |

---

## IX. File Path Standards

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

## X. Prompt Engineering for Orchestration

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

## XI. Token Budget Guidelines

| Component | Budget | Notes |
|:----------|:-------|:------|
| Command description | <200 tokens | AI discovery |
| Agent description | <500 tokens | Include examples for Tier 1 |
| Skill description | <200 tokens | Keywords for activation |
| SKILL.md body | <5000 tokens | ~500 lines max |
| Reference files | Unlimited | On-demand loading |

**Context Gravity Rule:** If phase requires >5 source files → use Triangle pattern.

---

## XII. Forbidden Patterns

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
**Vector Bloat:** Using Vector when context >70% full.
**Fix:** Delegate to Triangle to preserve main context.
</forbidden_pattern>

<forbidden_pattern>
**Implicit Context:** Assuming subagent knows project from main thread.
**Fix:** Explicitly pass project-brief.md and roadmap.md to subagent.
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

---

## Documentation References

- **docs/AI-ARCHITECTURE.md** - Agentic Runtime paradigm and cognitive capabilities
- **docs/VECTOR_vs_TRIANGLE.md** - Pattern mechanics and selection guide
- **README.md** - Installation and marketplace
- **Plugin READMEs** - Individual plugin documentation
