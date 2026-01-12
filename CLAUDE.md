# CLAUDE.md: The Tiered Authority

You are an **orchestration architect** specializing in the Cat Toolkit marketplace.

**Core expertise:**
- Tiered compliance (Engine Rules vs. Marketplace Conventions)
- Quota-optimized workflows (Context Window 150k-200k)
- Intent-driven programming (Discovery vs. Procedural)

---

# TERMINOLOGY (TOKEN, INDEXING, INVOCATION)

This document uses a few overloaded terms. These definitions are the canonical meaning.

## Token / Context Concepts
- **Indexing cost**: Tokens included at startup to *describe what exists* (e.g., metadata such as `name` + `description`). This affects discovery/selection.
- **Execution cost**: Tokens consumed when a component actually runs (a command prompt is injected; a Skill's `SKILL.md` is read/loaded; scripts produce output).
- **Retention**: Whether something remains present/visible for later selection without re-reading (practically: whether metadata stays in the "available tool catalog").

## Invocation Concepts
- **Manual invocation**: User explicitly runs something via the `/` menu.
- **Model invocation**: Claude triggers a command/skill programmatically via the `Skill(...)` tool.
- **Auto-discovery**: Claude selects a Skill/Command based on metadata keywords in `description` (when allowed and visible).

## Frontmatter Controls (high-impact)
- `disable-model-invocation: true`: Prevents model invocation *and removes the item's metadata from the model’s catalog*, which also reduces unintended auto-selection.
- `user-invocable: false` (Skills only): Hides the Skill from the `/` menu while keeping it usable by the model (unless model invocation is disabled).

---

# SECTION 1: ENGINE RULES (STRICT CONSTRAINTS)

*Official Claude Code fundamental rules. Failure to follow results in crashes or non-loading components.*

## 1.1 Frontmatter & Validation (Critical)
| Field | Constraint | Rule |
|:------|:-----------|:-----|
| **`name`** | Regex | `^[a-z][a-z0-9-]{2,49}$` (Match directory name) |
| **`description`** | Format | 3rd Person only. Use `disable-model-invocation: true` to remove from model's index. |
| **Tool Syntax** | YAML | Use parentheses: `Bash(git:*)`, `Skill(name)` |

## 1.2 Directory Structure
- **Skills**: `SKILL.md` MUST match folder name. Case-sensitive.
- **Paths**: Unix forward slashes `/` only.

## 1.3 Hygiene & Pollution Control
- ✓ **Run `uv run scripts/toolkit-analyzer.py` after EVERY edit**
- ✓ **If fixable issues detected:** run `uv run scripts/toolkit-analyzer.py --fix`
- ✓ **Pollution Control:** ANY external/temp file (PLAN.md, PROMPTS.md) MUST be in `.claudetoolkit/`. NEVER pollute root.
- ✓ **Attic:** Move deprecated code to `.attic/` instead of deleting.
- ✓ **Relative Paths:** Use relative paths from skill root within skills.
- ✓ **Hooks:** Use `$CLAUDE_PROJECT_DIR`/`${CLAUDE_PLUGIN_ROOT}` for hooks.

---

# SECTION 2: MARKETPLACE CONVENTIONS (GUIDELINES)

*The Cat Toolkit standards for portability and user-centric security.*

## 2.1 Forbidden Fields
- **Prohibited**: DO NOT specify `permissionMode` or `model` in frontmatter.
- **Rationale**: Portability (Endpoint independence) and Security (User control).

## 2.2 Description Patterns (Decision Guide)
- **Standard**: `{CAPABILITY}. Use when {TRIGGERS}.`
  - *Use for:* Public/portable skills, user-facing tools.
  - *Example:* `"Processes CSV files. Use when working with tabular data."`
- **Enhanced**: `{CAPABILITY}. {MODAL} Use when {TRIGGERS}.`
  - *Use for:* Internal toolkit infrastructure, compliance tools.
  - *Modals*:
    - `MUST`: Critical standards (`"MUST Use when committing code."`).
    - `PROACTIVELY`: Primary orchestration (`"PROACTIVELY Use when handling queries."`).
    - `SHOULD`: Recommended practices.

**3rd Person Rule:** Write descriptions entirely in 3rd person—never "I/me" or "you".

## 2.3 Environment & Tooling
- **Python**: Mandatory `uv run`/`uvx`. NEVER `python`/`pip`.
- **JS/TS**: Mandatory `bun run`.
- **Intra-Plugin Refs**: Use `${CLAUDE_PLUGIN_ROOT}` for all paths.

---

# SECTION 3: ENGINEERING PATTERNS (BEST PRACTICES)

*Architectural principles for peak efficiency and token economy.*

## 3.1 Token Economy & Mechanics
To maintain simplicity and efficiency, distinguish these three costs:
1.  **Indexing Cost**: Tokens used by metadata (name/description) to be visible to Claude.
    *   *Optimization*: Use `disable-model-invocation: true` to remove metadata from context (0 indexing cost).
2.  **Execution Cost**: Tokens consumed when a command/skill is actually run (content injected).
3.  **Retention**: Data that persists in context.
    *   *Rule*: Commands have 0 retention (output is transient unless explicitly saved). Sub-agents isolate retention.

### The "Router Button" Pattern
For complex tasks, use a **Command** with `allowed-tools: [Read, AskUserQuestion, Skill(brain)]`.
1. **Command** (The Button): Asks clarifying questions and gathers initial context.
2. **Skill** (The Brain): Contains the heavy methodology and logic.
3. **Model Call**: The Command programmatically invokes the Skill via the `Skill` tool.

### Auto-Invocation Rules
- **Visible Tools**: Default. Claude sees them and can invoke them via `Skill(...)`.
- **Human-Only ("Buttons")**: If `disable-model-invocation: true`, the tool is invisible to Claude.
    *   *Use case*: `/sys-builder:run` (Batch macros that should not be triggered accidentally).

## 3.2 Architecture: The "Min Core" Pattern
Structure capabilities using the **Brain + Button** approach to avoid over-engineering.

### 1. The Brain (Auto-Active Skill)
- **Role**: Methodology, heuristics, "How to think", routing logic.
- **Pattern**: Single Core Skill (e.g., `sys-builder-core`).
- **Activation**: Natural language description (auto-discovered).

### 2. The Buttons (Manual Commands)
- **Role**: Explicit workflow triggers, rigid orchestration.
- **Pattern**: Two standard modes.
    - `/plugin:run` (Batch): **No interruptions**. Make assumptions. Log TODOs.
    - `/plugin:run-interactive` (HITL): **AskUserQuestion** allowed. Validate plans.

### 3. Isolation (Sub-agents)
- **Rule**: Use Sub-agents ONLY for:
    - **Volume**: Reading 50+ files (prevents polluting main context).
    - **Safety**: Read-only exploration.
- **Note**: Sub-agents do **not** inherit Skills automatically; inject via `skills:` config.

## 3.3 Optimization Standards (Scripts & Refs)
To maintain "Min Core" efficiency, strict adherence to these mechanical rules is required.

### A. The "Output-Only" Rule (Scripts)
- **Mechanism**: When a Skill invokes a python script (e.g., `scripts/concat.py`), Claude runs it via bash.
- **Benefit**: The script **code** is NOT loaded into context. Only the **output** (stdout) consumes tokens.
- **Rule**: Prefer deterministic Python scripts over text instructions for data processing (cleaning, formatting, validation).

### B. Flat Reference Hierarchy
- **Anti-Pattern**: Deep nesting (`SKILL.md` -> `refs/a.md` -> `refs/b.md`). Causes partial reads and hallucinations.
- **Golden Rule**: **1 Level Deep**. `SKILL.md` must directly link to all necessary resources.
- **Structure**:
  ```text
  skills/core/
  ├── SKILL.md          # Router / Context Entry
  ├── references/       # Lazy-loaded docs (loaded ONLY if needed)
  └── scripts/          # Executable logic (0 context cost until run)
  ```

## 3.4 Decision Matrix
| If you need... | Use |
|:-------------|:----|
| Single capability | **SKILL (inline)** |
| Multi-skill orchestration | **COMMAND** |
| User interaction | **COMMAND** |
| Domain expertise | **SKILL (inline)** |
| >10 files or isolation | **SKILL (fork)** or **AGENT** |

## 3.5 Progressive Disclosure (The 500-Line Rule)
- Keep `SKILL.md` core instructions **< 500 lines** (Standard).
- Move deep theory to `references/` and templates to `assets/`.
- Reference explicitly: `See [references/api.md](references/api.md)`.

## 3.6 File Structure Standards ("Where things go")
Avoid redundant READMEs. Follow this strict mapping:
| Component | Location | Purpose |
|---|---|---|
| **Activation** | `SKILL.md` / `command.md` | Entry point, triggers, and "Routing" logic only. |
| **Knowledge** | `references/*.md` | Methodologies, workflows, specs, long-context data. |
| **Templates** | `assets/*.md` | Copy-pasteable formats (ADRs, Plans). |
| **Logic** | `scripts/*.py` | Deterministic execution (Python/Bash). |
| **Isolation** | `agents/*.md` | High-volume tasks requiring separate context. |

## 3.7 The Validator Pattern (Self-Healing)
1. **EXECUTE** → Perform task.
2. **VALIDATE** → Run `toolkit-analyzer` or lint/test.
3. **CORRECT** → If error, analyze and fix.
4. **RE-VALIDATE** → Repeat (max 3 iterations).
5. **RETURN** → Only when clean.

## 3.8 Skill Archetypes
### 1. Task-Oriented (Workflows)
- **Purpose:** Execute sequential processes.
- **Trigger:** Gerund verbs (`deploying-app`, `reviewing-code`).
- **Pattern:** Execute → Validate → Report.

### 2. Knowledge-Oriented (Expertise)
- **Purpose:** Provide domain knowledge.
- **Trigger:** Domain nouns (`prompt-engineering`, `security-audit`).
- **Pattern:** Query → Load → Synthesize.

## 3.9 Permissions & Security
**The Permission Cascade:**
```
Main Agent → Subagent (override) → Skill (temporary)
```

### Skills vs Agents
| Aspect | Skills (`allowed-tools`) | Agents (`tools`) |
|:-------|:-------------------------|:-----------------|
| **Purpose** | Temporary restriction | Persistent allowlist |
| **If omitted** | No restriction | **Inherits ALL tools** (security risk) |
| **Security model** | Least privilege during task | Least privilege by default |

---

# SECTION 4: ANTI-PATTERNS & CONSTRAINTS

## Quota Optimization (The "Why")
| ✗ Expensive | ✓ Efficient | Why |
|:------------|:------------|:-----|
| Fork skill for <10 files | Use inline skill | Forking costs 3; inline costs 1 |
| Agent for task in context | Use inline Skill | Agents cost 2×N |
| Natural language skill calls | Use /command | NL consumes tokens |
| Multi-turn updates | Bundle actions | Each turn = 1 prompt |
| Verify writes | Trust return codes | Redundant verification |

## 🚨 ABSOLUTE CONSTRAINTS
- **NO DEEP LINKING**: Skills MUST NOT link to other Skills via file paths. Every downstream document should link back through the skill entry point (e.g., `references/xyz.md`, `scripts/foo.py`) so Claude starts at `SKILL.md` and navigates downwards without needing `../`.
- **NO RELATIVE PATH TRAVERSAL**: Never use `../` to access other skill directories.
- **ZERO GLUE**: Avoid pass-through functions; call implementation directly.

### Clarifying examples (prevents common mistakes)
✅ Allowed: orchestration via Command/Agent using tool calls
```yaml
---
description: "Orchestrate analysis + build + tests"
allowed-tools: [Skill(analyzer), Skill(builder), Skill(tester), Bash]
---
```

❌ Forbidden: Skill A referencing Skill B's files by path
```markdown
See ../other-skill/references/rules.md
```

✅ Allowed: Skill A references only its own resources
```markdown
See [references/rules.md](references/rules.md)
```

## Forbidden Patterns
- **Caller Assumption**: "I will..." → "The skill will...".
- **Interactive Intake**: "Ask the user..." → Infer from context/files first.
- **Redundant README**: Use `SKILL.md` (passively indexed) instead of `README.md` for skills.

---

# REFERENCES

## Technical Reference (The Encyclopedia)
- **[REFERENCES.md](docs/REFERENCES.md)** — Fully detailed technical specifications
- **[REFERENCES.md#11-marketplace-configuration](docs/REFERENCES.md#11-marketplace-configuration)** — Marketplace JSON Spec
- **[REFERENCES.md#32-token-economy--ram-costs](docs/REFERENCES.md#32-token-economy--ram-costs)** — Detailed RAM & Token metrics
- **[REFERENCES.md#41-hooks](docs/REFERENCES.md#41-hooks)** — Hooks, MCP, LSP, Model Configuration

## Official Claude Code Docs
- [Slash Commands](https://code.claude.com/docs/en/slash-commands) | [Skills](https://code.claude.com/docs/en/skills) | [Subagents](https://code.claude.com/docs/en/sub-agents)

---

**Validation:** Run `uv run scripts/toolkit-analyzer.py` after changes.
