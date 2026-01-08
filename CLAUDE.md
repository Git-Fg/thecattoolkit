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

### The .cattoolkit Root
All runtime artifacts stored in `.cattoolkit/`:
- **Session State**: `.cattoolkit/context/`
- **Project Management**: `.cattoolkit/planning/`
- **Hooks**: `.cattoolkit/hooks/`

### Mercenary Isolation
- Agents MUST NOT reference plugin-specific files in system prompts
- Commands inject content via envelope pattern, never @file references
- Plugins function independently (zero shared state)

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
| **Triangle** | Command → Agent → Skill | Heavy lifting, >50% context, no user input needed | New context |
| **Time-Server** | Command → Async Agent | Long-running (>1 min), fire-and-forget | Background |
| **Swarm** | Command → [Agent A, B, C] | Parallel search/audit, non-overlapping work | Multiple new |
| **Lazy Discovery** | Agent + Skill | Self-sufficient context acquisition | Fallback |

### Swarm Orchestration (Map-Reduce)
1. **Map:** Command slices into atomic, non-overlapping assignments
2. **Execute:** Agents produce standardized outputs (no shared state)
3. **Reduce:** Command synthesizes final result

---

## V. Command Types

| Type | Consumer | `disable-model-invocation` | AskUserQuestion |
|:-----|:---------|:---------------------------|:----------------|
| A: User-Centric | Human only | `true` | Yes |
| B: Agent-Ready | AI agents | No | No |
| C: Hybrid | Both | No | Conditional |

---

## VI. Component Responsibilities

| Component | Primary Role | Permissions |
|:----------|:-------------|:------------|
| **Command** | Orchestration, context gathering, user interaction | Inherits all (restrict via `allowed-tools`) |
| **Agent** | Autonomous execution, framework application | Inherits all (restrict via `tools`) |
| **Skill** | Passive standards, templates, methodology | Asks permission (pre-approve via `allowed-tools`) |

**Constraint:** If Command is deleted, Agent + Skill must still work via Task tool.

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

| Avoid | Prefer |
|:------|:-------|
| "Check package.json, then requirements.txt" | "Identify dependency management system" |
| "Run find src -name '*.js'" | "Locate source files using filesystem tools" |
| "Execute these grep commands: ..." | "Search for authentication patterns" |

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

## X. Envelope Theory

Use semantic XML tags for context engineering. Flat structure only.

**Agent Definitions:** `<role>`, `<constraints>`, `<system_prompt>`
**Task Delegation:** `<assignment>`, `<context>`

```xml
✅ Flat & Semantic:
<context>
Authentication files: src/auth.ts, src/user.ts
Instruction: Analyze login flow.
</context>

❌ Nested (Forbidden):
<context><files><file path="..."/></files></context>
```

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

- **docs/VECTOR_vs_TRIANGLE.md** - Pattern mechanics and selection guide
- **README.md** - Installation and marketplace
- **Plugin READMEs** - Individual plugin documentation
