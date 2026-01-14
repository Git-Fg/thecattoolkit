The suggestion to "consolidate everything" risks creating **God Objects**—skills so broad that their semantic description becomes diluted, making it harder for the model to know *when* to invoke them automatically.

The **"Unit of Capacity"** must be **Atomic** enough to be discovered by a specific intent, but **Robust** enough to handle the full lifecycle of that intent.

Here is the revised **Archetype-Driven Refactoring Plan**. We will map every component to one of the 4 Universal Archetypes to ensure they do exactly enough, but no more.

---

# THE ARCHETYPE AUDIT & REFACTORING PLAN (v2.0)

## 0. Cross-Cutting Integration Checklist
*Before starting domain refactors, map these new resources:*
- [ ] **Project Rules**: Link `sys-core/skills/toolkit-standards` to `docs/guides/rules.md`
- [ ] **Handoffs**: Link `sys-builder/skills/plan-manager` to `references/handoff-protocols.md`
- [ ] **Static Analysis**: Link `sys-builder/skills/code-standards` to `references/static-analysis-workflow.md`

## 1. Domain: Infrastructure (`sys-core`)
*Goal: Provide the tools to build and maintain the toolkit itself.*

| Current Component | Status | New Name | Archetype | Context Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `toolkit-registry` | **Keep** | `toolkit-standards` | **Advisory** | No | Defines the "Laws" & Rules. Passive knowledge base. |
| `scaffold-component` | **Keep** | `component-generator` | **Generator** | No | Takes input -> Outputs valid file structure. |
| `audit-plugins` | **Keep** | `plugin-auditor` | **Procedural** | No | Executes strict validation checklist. |
| `meta-hooks` | **Rename** | `hook-standards` | **Advisory** | No | Knowledge base for hooks. |
| `create-hooks` | **Rename** | `hook-generator` | **Generator** | No | Creates hook JSON/Scripts. |
| `meta-mcp` | **Rename** | `mcp-integrator` | **Orchestrator** | **Yes** | Connects external tools (complex ops). |
| `validate-toolkit` | **Merge** | *(Merge into `plugin-auditor`)* | - | - | Redundant procedural skill. |
| `toolkit-architect` | **Delete** | - | - | - | Vague overlap with Scaffold/Registry. |
| `check-types` | **Keep** | `type-checker` | **Procedural** | No | Deterministic validation. |
| `security-auditor` | **Delete** | - | - | - | Replace with `audit-security` skill (Procedural). |

## 2. Domain: Engineering (`sys-builder`)
*Goal: Managing the software development lifecycle.*

| Current Component | Status | New Name | Archetype | Context Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `managing-project-plans` | **Refactor** | `plan-manager` | **Orchestrator** | **Yes** | Manages `ROADMAP.md` state & handoffs. Heavy context. |
| `software-engineering` | **Refactor** | `code-standards` | **Advisory** | No | Patterns (TDD, Analysis). Passive knowledge. |
| `execution-core` | **Refactor** | `autonomous-worker` | **Procedural** | **Yes** | Execution loop (Do -> Verify). Needs isolation. |
| `test-writer` | **Keep** | `test-generator` | **Generator** | No | Code -> Tests. |
| `director` (Agent) | **Delete** | - | - | - | Replaced by `plan-manager`. |
| `worker` (Agent) | **Keep** | `executor` | **Config Only** | - | Enforce `permissionMode: acceptEdits`. |
| `commands/*` | **Purge** | - | - | - | Move dynamic logic to scripts, delete wrappers. |

## 3. Domain: Cognition (`sys-cognition`)
*Goal: Enhancing the model's reasoning capabilities.*

| Current Component | Status | New Name | Archetype | Context Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `thinking-frameworks` | **Keep** | `reasoning-models` | **Advisory** | No | Mental models library. |
| `claude-code-mastery` | **New** | `claude-mastery` | **Advisory** | No | Fundamentals & Context mgmt. |
| `prompt-engineering` | **Split** | `prompt-architect` | **Advisory** | No | Theory and patterns. |
| `create-meta-prompts` | **Split** | `prompt-generator` | **Generator** | No | Factory for .md prompt files. |
| `reasoner` (Agent) | **Delete** | - | - | - | Persona wrapper. |

## 4. Domain: Research & Knowledge (`sys-research`)
*Goal: Ingesting and synthesizing information.*

| Current Component | Status | New Name | Archetype | Context Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `gitingest` | **Keep** | `git-ingest` | **Procedural** | **Yes** | Fetch -> Format -> Output (Heavy I/O). |
| `researcher` | **Refactor** | `deep-research` | **Orchestrator** | **Yes** | Routes Search/Docs/Code. Isolation needed. |
| `scientific-slides` | **Refactor** | `slide-architect` | **Advisory** | No | Narrative & Design expertise (Heavy References). |
| `statistical-analysis`| **Keep** | `data-analyst` | **Advisory** | No | Methodology guide. |
| `alphafold-database` | **Keep** | `bio-structure` | **Procedural** | No | Specific API interaction. |

## 5. Domain: Specialized Capabilities (Missing Domains)
*Goal: Completing the audit for all plugins.*

| Current Component | Status | New Name | Archetype | Context Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `sys-browser` | **Keep** | `browser-automator` | **Procedural** | **Yes** | Heavy DOM interaction. |
| `sys-multimodal` | **Keep** | `media-processor` | **Procedural** | **Yes** | Image/Video processing (Heavy context). |
| `sys-agents` | **Audit** | `memory-systems` | **Advisory** | No | Architecture patterns (Passive). |
| `sys-nodejs` | **Keep** | `node-utils` | **Procedural** | No | Lightweight scripts. |
| `sys-edge` | **Review** | `edge-lab` | **Experimental** | **Yes** | Unstable features. |

---

# SEO OPTIMIZATION STRATEGY (ENHANCED PATTERN)

Every `SKILL.md` description must strictly follow the **Enhanced Pattern**:
`[Primary Capability]. [PROACTIVELY USE | MUST USE | USE] when [trigger contexts]. Do not use for [anti-trigger].`

### Examples

**1. `component-generator` (Generator)**
> "Generates file structures for Skills, Commands, or Agents. **PROACTIVELY USE** when asked to 'create a new skill' or 'add a command'. Do not use for modifying existing files."

**2. `plan-manager` (Orchestrator)**
> "Orchestrates project lifecycle via `ROADMAP.md` and `BRIEF.md`. **MUST USE** when tracking progress, updating status, or handling handoffs. Do not use for writing code."

**3. `autonomous-worker` (Procedural)**
> "Executes implementation tasks with verification loops. **USE** when asked to 'implement this', 'fix this', or 'build this'. Runs in non-interactive mode."

**4. `slide-architect` (Advisory)**
> "Provides expert guidance on scientific narrative, Beamer templates, and visualization. **USE** when designing presentations or reviewing slide aesthetics. Do not use for generating PDF binaries directly."

---

# EXECUTION PHASES & VERIFICATION

## Phase 1: Core & Builder Refactor
1. Move/Rename `sys-core` skills.
2. Refactor `sys-builder` skills (merge Handoffs/Static Analysis).
3. **VERIFY:** `uv run scripts/toolkit-analyzer.py`

## Phase 2: Cognition & Research Refactor
1. Integrate `claude-mastery` and `deep-research`.
2. Refactor `slide-architect` (Advisory focus).
3. **VERIFY:** `uv run scripts/toolkit-analyzer.py`

## Phase 3: Cleanup
1. Delete all Agents (except `executor` config-only).
2. Purge `commands/`.
3. Update `marketplace/manifest.json`.
4. **FINAL VERIFY:** `uv run scripts/toolkit-analyzer.py --strict`


---


RECENT CHANGES : "
# The New Philosophy: "Skills-First, Context-Lean"

### 1. The Economic Reality (The 5-Hour Rule)
*   **Fact:** A "Pro" session allows ~200k tokens total.
*   **Cost:** Spawning a Subagent costs **20k-25k tokens** (10-12% of the total budget) *just to say hello*.
*   **Conclusion:** Spawning an Agent is a "nuclear option." It should only happen if the task requires parallelization that saves *human* time worth more than the token cost, or security isolation that cannot be achieved otherwise.

### 2. The Primitives Re-ranked

| Primitive | Old Status | **New Status** | **New Definition** |
|:--- |:--- |:--- |:--- |
| **SKILL** | Capability | **The Soverign** | The primary unit of logic. Contains "How-To", knowledge, and execution steps. **Default to Inline.** |
| **COMMAND** | Interface | **The Injector** | A "Macro". Used *only* to inject dynamic context (`!git status`) or chain skills. **Wrappers are dead.** |
| **AGENT** | Worker | **The Container** | **Demoted.** A runtime environment configuration (Permissions/Tools). No personality allowed. |
| **FORK** | N/A | **The Isolator** | `context: fork` in a Skill. The lightweight alternative to Agents for clean context. |

### 3. The Death of "Persona"
LLMs (Sonnet 3.5, Opus) do not need to be told "You are a Senior Architect" to act like one. They need **Protocols**.
*   **Old:** "You are a thoughtful analyst..." (Waste of tokens).
*   **New:** "Follow this 5-step analysis protocol..." (High signal).
"