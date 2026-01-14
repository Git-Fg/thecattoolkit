# THE ARCHETYPE-DRIVEN REFACTORING PLAN (v2.1 - FINAL)

The suggestion to "consolidate everything" risks creating **God Objects**—skills so broad that their semantic description becomes diluted, making it harder for the model to know *when* to invoke them automatically.

The **"Unit of Capacity"** must be **Atomic** enough to be discovered by a specific intent, but **Robust** enough to handle the full lifecycle of that intent.

---

9. ## 0. Strict Compliance Constraints (The Engine Rules)
10. *Before any refactor, every skill MUST adhere to these absolute constraints:*
11. 
12. 1.  **Frontmatter Integrity**: `name` MUST match the directory name exactly (`^[a-z][a-z0-9-]{2,49}$`).
13. 2.  **Protocol over Persona**: Replace all "You are a specialist..." narratives with "Follow this [X] Protocol". 
14. 3.  **SEO Description Formula**: `[Primary Capability]. [MODAL] USE when [trigger]. Do not use for [anti-trigger].`
15. 4.  **Context Forking**: Use `context: fork` ONLY for **Procedural** or **Orchestrator** skills handling complex I/O or >10 files. **Advisory** and **Generator** skills remain inline.
16. 5.  **Hub-and-Spoke**: `SKILL.md` is the central hub. All references/scripts must be one level deep. No relative traversal (`../`).
17. 6.  **No Deep Linking**: Skills MUST NOT link to other Skills via file paths. Use `Skill(name)` if orchestration is needed.
18. 7.  **Zero Glue**: Avoid pass-through functions; call implementation directly. Reduce directory layers.
19. 8.  **Atomic Naming (Gerunds)**: Use `verb-ing-noun` (e.g., `managing-plans`) for Skill names. This enforces "Action" over "Identity" and kills Personas. Nouns are reserved for Agents/Configs.

---

## 1. Domain: Infrastructure (`sys-core`)
*Goal: Provide the tools to build and maintain the toolkit itself.*

| Current Component | Status | New Name | Archetype | Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `toolkit-standards` | **Refactor** | `adhering-standards` | **Advisory** | **No** | Passive authority. Fix frontmatter `name`. |
| `plugin-auditor` | **Keep** | `auditing-plugins` | **Procedural** | No | Executes validation checklists. |
| `manage-healing` | **Refactor** | `repairing-state` | **Procedural** | **Yes** | Diagnosis + Repair loops. Heavy I/O. |
| `hook-generator` | **Refactor** | `generating-hooks` | **Generator** | No | Inputs -> Hook JSON/Scripts. Fix frontmatter `name`. |
| `hook-standards` | **Keep** | `applying-hooks` | **Advisory** | No | Knowledge base for hooks. |
| `mcp-integrator` | **Keep** | `integrating-mcp` | **Orchestrator** | **Yes** | Connects external tools (complex ops). |
| `type-checker` | **Keep** | `checking-types` | **Procedural** | No | Deterministic validation. |
| `audit-security` | **Keep** | `auditing-security` | **Procedural** | No | Protocol-based security scanning. |

---

## 2. Domain: Engineering (`sys-builder`)
*Goal: Managing the software development lifecycle.*

| Current Component | Status | New Name | Archetype | Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `managing-project-plans`| **Refactor** | `managing-plans` | **Orchestrator** | **Yes** | Manages `ROADMAP.md` state & handoffs. |
| `software-engineering` | **Refactor** | `applying-code-standards`| **Advisory** | No | Patterns (TDD, Analysis). Passive knowledge. |
| `execution-core` | **Refactor** | `executing-tasks` | **Procedural** | **Yes** | Execution loop (Do -> Verify). Needs isolation. |
| `test-writer` | **Keep** | `generating-tests` | **Generator** | No | Code -> Tests. |
| `director` (Agent) | **Delete** | - | - | - | Replaced by `managing-plans`. |
| `worker` (Agent) | **Keep** | `executor` | **Config Only** | - | Nouns allowed for Agents (Entities). |

---

## 3. Domain: Cognition & Agents (`sys-cognition` & `sys-agents`)
*Goal: Enhancing reasoning and architecting agentic systems.*

| Current Component | Status | New Name | Archetype | Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `thinking-frameworks` | **Rename** | `applying-reasoning` | **Advisory** | No | Mental models library (Pareto, Inversion, etc). |
| `claude-code-mastery` | **Merge** | `mastering-claude` | **Advisory** | No | Merge `agent-best-practices` & `context-engineering`. |
| `prompt-engineering` | **Split** | `architecting-prompts` | **Advisory** | No | Theory, patterns, and quality standards. |
| `create-meta-prompts` | **Split** | `generating-prompts` | **Generator** | No | Factory for .md prompt files. |
| `memory-systems` | **Merge** | `architecting-memory` | **Advisory** | No | Merge `agent-design-patterns` & `hybrid-search`. |
| `agent-orchestration` | **Refactor**| `orchestrating-agents`| **Orchestrator**| **Yes** | Designing context isolation and parallel flows. |

---

## 4. Domain: Research & Multimodal (`sys-research` & `sys-multimodal`)
| Current Component | Status | New Name | Archetype | Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `researcher` | **Refactor** | `conducting-research` | **Orchestrator** | **Yes** | Routes Search/Docs/Code. Isolation needed. |
| `gitingest` | **Rename** | `ingesting-git` | **Procedural** | **Yes** | Fetch -> Format -> Output (Heavy I/O). |
| `scientific-slides` | **Refactor** | `architecting-slides` | **Advisory** | No | Narrative focus. Merge `data-storytelling`. |
| `statistical-analysis`| **Keep** | `analyzing-data` | **Advisory** | No | Methodology guide. |
| `alphafold-database` | **Keep** | `analyzing-bio-struct`| **Procedural** | No | Specific API interaction. |
| `video-production` | **Refactor** | `processing-media` | **Procedural** | **Yes** | Complex ffmpeg/processing loops. |
| `canvas-design` | **Rename** | `generating-ui` | **Generator** | No | Generates visual specs and UI code. |

---

## 5. Domain: Node.js Dev (`sys-nodejs`)
*Goal: TypeScript/JavaScript ecosystems and tooling.*

| Current Component | Status | New Name | Archetype | Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `python-tools` | **Keep** | `mastering-uv` | **Advisory** | No | UV/Ruff standards and workflows. |
| `typescript-advanced-types`| **Rename**| `mastering-typescript`| **Advisory** | No | Optimal type safety and `satisfies` patterns. |
| `npm-management` | **Keep** | `managing-npm` | **Procedural** | No | Dependency management protocols. |

---

## 6. Domain: Edge & Specialized (`sys-edge`)
*Goal: Optimization for constrained environments.*

| Current Component | Status | New Name | Archetype | Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `edge-ai-management` | **Rename** | `experimenting-edge`| **Experimental**| **Yes** | Unstable features/Parallel edge trials. |
| `mobile-optimization` | **Merge** | *(Merge into `...-edge`)*| - | - | Redundant expertise. |
| `offline-sync` | **Keep** | `synchronizing-data`| **Procedural** | No | Specific sync logic. |

---

## 7. Domain: Browser Automation (`sys-browser`)
*Goal: Web interaction, crawling, and testing.*

| Current Component | Status | New Name | Archetype | Fork? | Rationale |
|:---|:---|:---|:---|:---|:---|
| `crawler` | **Refactor** | `crawling-web` | **Procedural** | **Yes** | Web scraping with isolation (heavy I/O). |
| `browser-automation` | **Keep** | `driving-browser` | **Procedural** | **Yes** | Headless interaction protocols. |
| `e2e-testing` | **Keep** | `testing-e2e` | **Orchestrator** | **Yes** | Coordinates browser + server for tests. |

---

# EXECUTION PHASES

## Phase 1: Core & Builder Alignment (The Foundation)
1.  **Frontmatter Fixes**: Ensure `sys-core` directory names and `name` fields match perfectly.
2.  **Advisory Transition**: Demote `toolkit-standards` to non-forked.
3.  **Protocol Conversion**: Rewrite `autonomous-worker` and `plan-manager` to be Protocol-based.
4.  **VERIFY**: `uv run scripts/toolkit-analyzer.py`

## Phase 2: Cognition, Research & Multimodal
1.  **Merge & Purge**: Execute the `sys-cognition` and `sys-agents` merges.
2.  **The Masteries**: Establish `mastering-claude` and `mastering-typescript` as the primary Advisory hubs.
3.  **SEO Polish**: Apply the description formula to all `sys-research` and `sys-multimodal` skills.
4.  **VERIFY**: `uv run scripts/toolkit-analyzer.py`

## Phase 3: Specialized, Node & Browser
1.  **Browser Isolation**: Ensure `crawling-web` and `driving-browser` skills are properly forked.
2.  **Edge Consolidation**: Merge mobile/edge skills into `experimenting-edge`.
3.  **Node Standards**: Finalize `managing-npm` and `mastering-uv` protocols.
4.  **VERIFY**: `uv run scripts/toolkit-analyzer.py`

## Phase 4: Cleanup & Security (Final Polish)
1.  **Agent Purge**: Move persona content from `agents/` to relevant skills. Convert agent files to pure JSON/YAML configs.
2.  **Command Purge**: Delete simple skill wrappers in `commands/`.
3.  **Final Audit**: 
    ```bash
    uv run scripts/toolkit-analyzer.py --strict
    ```

---

# RECENT PHILOSOPHY UPDATE (Jan 2026)
*   **The 5-Hour Rule**: A Pro session is ~200k tokens. Subagents cost 25k to "say hello". Avoid them.
*   **Quota Impact**: Subagents consume 1 prompt quota (Z.AI/Subscription) per spawn. Use `context: fork` (Tool Call) to avoid this penalty.
*   **Skills-First**: Skills are the sovereign primitive. Agents are just containers.
*   **Death of Persona**: sonnet-3.5 doesn't need to be told it's a "Senior Dev". It needs a checklist.
*   **Atomicity & Naming**: Use Gerunds (`analyzing-data` vs `data-analyst`) to enforce "Action" over "Identity". This aligns with the "Protocol over Persona" rule and clarifies that Skills are *procedures*, not *workers*.
*   **The Delta Constraint**: Claude is smart. Don't explain what a PDF is. Only document the *diff* between general knowledge and your specific requirement.
*   **Skills Description**: Skills Description must be what to target, with optimal semantic, and being sufficiently focus on a task to be activated autonomously. **The Skill must be Atomic enough to be discovered by a specific intent, but Robust enough to handle the full lifecycle of that intent.**