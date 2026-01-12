---
name: manage-planning
description: "Provides unified interface for creating specifications (BRIEF, ROADMAP) and dispatching autonomous workers. PROACTIVELY Use when planning projects or executing phases."
context: fork
agent: worker
allowed-tools: [Read, Write, Edit, Glob, Grep, Task, Bash]
---

# Planning & Execution Manager

## Core Purpose

A unified engine to **Design** project architecture and **Orchestrate** implementation in a single semantic authority.

## Canonical Output Location

**MANDATORY**: All planning artifacts MUST be created in:
```
.cattoolkit/planning/{project-slug}/
```

**NEVER** create PLAN.md, ROADMAP.md, or BRIEF.md at the project root.

---

## Mode 1: Planning Protocol

**Trigger:** `/plan` command or "Create a plan for..."

### Phase 1: Initialize Structure

Create the planning directory:
```bash
mkdir -p .cattoolkit/planning/{slug}/phases
```

**Output Structure:**
```
.cattoolkit/planning/{slug}/
├── BRIEF.md           # Project definition
├── DISCOVERY.md       # Auto-discovery findings
├── ROADMAP.md         # Phases with parallelism markers
└── phases/
    ├── 01-{name}/
    │   └── 01-01-PLAN.md
    └── 02-{name}/
        └── 02-01-PLAN.md
```

### Phase 2: Context Assessment (2026 Inline-First)

**CRITICAL: The 10-File Rule**

Before executing ANY plan, assess context:
```bash
find . -maxdepth 2 -not -path '*/.*' -type f | wc -l
```

**Discovery Mode Selection:**
| File Count | Mode | Action |
|:---|:---|:---|
| **≤ 10** | **INLINE** | Read README, package.json, config files directly |
| **> 10** | **INLINE** | Use Read/Glob/Grep for discovery |
| **> 50 OR >5 subdirs** | **PARALLEL** | Only THEN consider parallel explore agents |

**Quota Warning:** Spawning sub-agents for ≤10 files = **Quota Violation**. You have 150k+ tokens. Use them.

### Phase 3: Determine Plan Type

**Lite Plan:** Simple feature (2-3 tasks). Create phase plan file directly in `.cattoolkit/planning/{project-slug}/phases/XX-name/`.

**Standard Plan:** Complex project. Create full hierarchy:
- `BRIEF.md` (Project goals)
- `ROADMAP.md` (Phases and milestones)
- Phase plan files in `phases/` directories

### Phase 4: Create Documents

Use templates from `assets/templates/`:

**BRIEF.md** (using `brief.md` template):
- Greenfield (v1.0): Keep under 50 lines, measurable success criteria
- Brownfield (v1.1+): Add Current State section with shipped version info

**ROADMAP.md** (using `roadmap.md` template):
- 3-6 phases total
- Each phase delivers something coherent
- Split phases with >7 tasks
- **STRICTLY PROHIBITED:** Time estimates

**Phase plan file** (using `phase-plan.md` template):
- 2-3 tasks per plan (split if >7)
- Each task: Scope/Action/Verify/Done
- Parallelism analysis table

### Phase 5: Parallelism Analysis

Create ROADMAP.md with explicit parallelism markers:

```markdown
| Phase | Name | Status | Parallel Agents | Dependencies |
|-------|------|--------|-----------------|--------------|
| 01 | Discovery & Setup | pending | 2 explore | none |
| 02 | Core Implementation | pending | 3 worker | 01 |
| 03 | Integration | pending | 2 worker | 02 |
```

---

## Mode 2: Execution Protocol

**Trigger:** `/build` command or "Execute phase X..."

### Phase 1: Load State

1. Read ROADMAP.md for phase overview
2. Identify current phase (first pending or specified)
3. Read phase plan file for task details
4. Parse parallelism analysis table

### Phase 2: Resumability Check (State-in-Files)

**CRITICAL:** Before proceeding, check for interruption state:

1. **Check for HANDOFF.md:**
   - Look for `.cattoolkit/planning/{project-slug}/phases/XX-name/HANDOFF.md`
   - If found, READ it immediately

2. **Resume from Handoff State:**
   - Review "In-Progress" section
   - Review "Next Actions" section
   - DO NOT restart completed tasks
   - Continue from "Next Actions" specifically

3. **If no HANDOFF.md:** Continue with fresh execution.

### Phase 3: Analyze Execution Strategy

**2026 Inline-First Rule:**

| Task Complexity | Mode | Action |
|:---|:---|:---|
| **Simple (<3 files)** | **INLINE** | Execute directly in main thread |
| **Complex (≥3 files)** | **DELEGATE** | Spawn `worker` agent via Task tool |
| **Massive phase** | **FALLBACK** | Use `@director` agent only if context insufficient |

**Anti-Pattern:** Spawning agents for tasks fitting in current context = Quota Violation.

### Phase 4: Orchestrate Tasks

**Sequential Tasks:**
- Execute one at a time in main thread (if simple)
- Or delegate sequentially to workers (if complex)

**Parallel Tasks:**
- Operate on different files with no shared dependencies
- Launch simultaneously in single message with multiple Task calls
- Each Task call spawns a worker agent

**Background Tasks:**
- Long-running operations (tests, builds, audits)
- Launch with `run_in_background: true`
- Don't block other tasks

### Phase 5: Worker Delegation Standard

**Agent Prompt Template:**
```markdown
You are executing Task {N} of Phase {XX}.

## Context
{Include BRIEF.md summary}
{Include relevant DISCOVERY.md sections}

## Your Task
**Scope**: {files/directories}
**Action**: {what to do}
**Verify**: {how to verify}
**Done**: {acceptance criteria}

## Execution Rules
- Execute in UNINTERRUPTED FLOW mode
- Self-verify before completing
- Log any blockers to HANDOFF.md
- Do NOT ask user questions during execution

## Output
When complete, report:
- Files modified
- Verification results
- Any issues encountered
```

**Provide complete context to each agent:** Include BRIEF.md summary, relevant plan sections, and specific task requirements.

### Phase 6: Verification & State Update

**After each task:**
- Trust tool return codes (no read-back unless error)
- Run high-fidelity validation (compiler, linter, tests)
- Update task status in phase plan file

**After each phase:**
- Update phase status in ROADMAP.md
- Create SUMMARY.md using template

**On blocker:**
- Create HANDOFF.md using template
- Specify what can proceed vs blocked
- Suggest resolution

---

## Asset Library

| Template | Purpose |
|:---------|:--------|
| `brief.md` | Project definition |
| `roadmap.md` | Multi-phase overview |
| `phase-plan.md` | Executable phase plans |
| `handoff.md` | Session pause/resume |
| `summary.md` | Phase completion |
| `discovery.md` | Auto-discovery findings |
| `issues.md` | Deferred enhancements |

**Location:** `assets/templates/`

---

## Integration Points

- **execution-core**: Behavioral standards for agents (Uninterrupted Flow, Self-Verification, Auth-Gates)
- **software-engineering**: Quality standards (TDD, debugging, security, code review)
- **architecture**: Design standards (when architecting new systems)

## Quality Standards

- Plans must be actionable without ambiguity
- Each task must have clear verification criteria
- Parallelism must be explicitly marked
- Dependencies must be traceable
- No time estimates
- All verification commands must be executable

## Error Handling

**Task Failure:**
1. Log failure details to SUMMARY.md
2. Analyze cause (code error vs verification criteria)
3. Option A: Retry with refined instructions
4. Option B: Mark blocked, create HANDOFF.md

**Agent Timeout:**
1. Check output file for progress
2. If stuck: Kill and respawn with different approach
3. If making progress: Extend timeout

**Blocker Encountered:**
1. Stop current task
2. Create HANDOFF.md with blocker details
3. Document what can proceed independently
