---
name: builder-core
description: PROACTIVELY USE when planning or executing projects. Auto-discovers codebase patterns, creates multi-phase plans, and orchestrates parallel agent execution. Primary entry point for all planning and execution workflows.
user-invocable: false
allowed-tools: [Read, Write, Edit, Glob, Grep, Task, Bash(mkdir:-p), Bash(ls:*)]
---

# Builder Core Protocol

## Purpose

Comprehensive planning and execution system with automatic codebase discovery and optimized parallel agent orchestration. This is the **primary entry point** for all project planning and execution workflows.

## Canonical Output Location

**MANDATORY**: All planning artifacts MUST be created in:
```
.cattoolkit/planning/{project-slug}/
```

**NEVER** create PLAN.md, ROADMAP.md, or BRIEF.md at the project root.

## Quick Reference

| Mode | Entry Point | Description |
|:-----|:------------|:-------------|
| **Plan** | User requests planning | "Create a plan for X", "I need a roadmap for Y" |
| **Execute** | User requests execution | "Execute this plan", "Run phase 02" |
| **Lite** | Simple features | "Add X feature" (2-3 tasks, single phase plan file) |

## Operational Protocol

### 2026 Execution Logic (The Cost Matrix)

**1. Context Assessment Protocol**
Before executing ANY plan, run: `find . -maxdepth 2 -not -path '*/.*' -type f | wc -l`

**2. Execution Mode Selection**
| File Count | Complexity | Mode | Cost | Action |
|:---|:---|:---|:---|:---|
| **< 10** | Low | **INLINE** | 1 | Execute directly in current session. |
| **10 - 50** | Medium | **INLINE** | 1 | Use `Read` + `Grep` to navigate. Do NOT spawn agent. |
| **> 50** | High | **AGENT** | 2xN | Spawn `@director` (or specific worker) to handle scale. |

**3. Anti-Pattern Warning**
> Spawning a "Planner" or "Director" agent for a project with < 50 files is a **Quota Violation**. You are smart enough to handle small contexts directly.

**4. Template Access**
Load `references/templates/` on-demand based on Plan Type.

## Workflow Routing
- **Lite Plan**: Follow inline protocol (2-3 tasks, single phase plan file in .cattoolkit/planning/)
- **Standard Plan**: Delegate to `@director` (Forked when >50 files OR >5 subdirectories)

## Document Templates

| Document | Template | Purpose |
|:---------|:---------|:--------|
| Project Brief | `references/templates/brief.md` | Project definition |
| Roadmap | `references/templates/roadmap.md` | Multi-phase overview |
| Phase Plan | `references/templates/phase-plan.md` | Executable phase plans |
| Handoff | `references/templates/handoff.md` | Session pause/resume |
| Summary | `references/templates/summary.md` | Phase completion |
| Discovery | `references/templates/discovery.md` | Auto-discovery findings |
| Issues | `references/templates/issues.md` | Deferred enhancements |

## Planning Protocol

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
    │   └── 01-01-PLAN.md (phase plan file)
    └── 02-{name}/
        └── 02-01-PLAN.md (phase plan file)
```

### Phase 2: Auto-Discovery

**Context Assessment Protocol:**

1. **Check Project Size:** Run `find . -maxdepth 2 -not -path '*/.*' -type f | wc -l`

2. **Decision Point:**
   - **Greenfield/Empty (<10 files):** SKIP agent delegation. Perform inline discovery (Read README, package.json, or config files).
   - **Brownfield/Medium (10-50 files):** Perform inline discovery using Read/Glob/Grep
   - **Brownfield/Large (>=50 files OR >5 subdirectories):** Execute Parallel Agent Protocol.

**Parallel Agent Protocol (Large Projects Only):**

Launch 2-3 explore agents **in parallel** via Task tool. Each agent focuses on different aspects:
- Agent 1: Architecture & structure (files, directories, patterns)
- Agent 2: Dependencies & integrations (imports, APIs, external services)
- Agent 3: Existing conventions (naming, testing, documentation)

Synthesize findings into DISCOVERY.md using `references/templates/discovery.md`.

### Phase 3: Determine Plan Type

**Lite Plan:** Simple feature (2-3 tasks). Create phase plan file directly in `.cattoolkit/planning/{project-slug}/phases/XX-name/`.

**Standard Plan:** Complex project. Create full hierarchy:
- `BRIEF.md` (Project goals)
- `ROADMAP.md` (Phases and milestones)
- Phase plan files in `.cattoolkit/planning/{project-slug}/phases/XX-name/`

### Phase 4: Create Documents

Use templates from `references/templates/`:

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

## Execution Protocol

### Phase 1: Load Plan

1. Read ROADMAP.md for phase overview
2. Identify current phase (first pending or specified)
3. Read phase plan file for task details
4. Parse parallelism analysis table

### Phase 2: Resumability Check

**State-in-Files Enforcement:**

Before proceeding, check for interruption state:
1. Look for `.cattoolkit/planning/[phase-name]/HANDOFF.md`
2. If found, READ it immediately
3. Resume from "Next Actions" section
4. DO NOT restart completed tasks

### Phase 3: Analyze Parallelism

Classify each task:

**Sequential Tasks:**
- Must wait for previous task
- Has "-" in "Can Parallel With" column
- Execute one at a time

**Parallel Tasks:**
- Listed in each other's "Can Parallel With" column
- Launch simultaneously in single message with multiple Task calls
- Group by parallel compatibility

**Background Tasks:**
- Long-running operations (tests, builds, audits)
- Launch with `run_in_background: true`
- Don't block other tasks

### Phase 4: Spawn Agents

**Parallel Execution Pattern:**

For parallel tasks 2, 3, 4:
- Send SINGLE message with 3 Task tool calls
- Each Task call spawns a worker agent
- Provide complete context to each agent

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

### Phase 5: Monitor & Verify

1. **Wait for completion** - Use TaskOutput for foreground agents
2. **Check background agents** - Read output files periodically
3. **Verify outputs** - Run verification commands
4. **Log results** - Write to phase SUMMARY.md

**Verification Protocol:**
- Run "Verify" command/check
- Compare against "Done" criteria
- If PASS: Mark task complete
- If FAIL: Log failure, decide retry vs escalate

### Phase 6: Update State

**After each task:**
- Update task status in phase plan file (pending → in_progress → completed)

**After each phase:**
- Update phase status in ROADMAP.md
- Create SUMMARY.md using template

**On blocker:**
- Create HANDOFF.md using template
- Specify what can proceed vs blocked
- Suggest resolution

## Parallelism Guidelines

### Task Type Classification

**Sequential Tasks:**
- Task A produces output consumed by Task B
- Must complete before dependent tasks start

**Parallel Tasks:**
- Operate on different files/modules
- No shared dependencies
- Can execute simultaneously

**Background Tasks:**
- Long-running, non-blocking
- Audits, test suites, builds
- Launch with `run_in_background: true`

### Agent Count Recommendations

| Phase Type | Recommended Agents |
|------------|-------------------|
| Discovery | 2-3 explore |
| Core Implementation | 3 worker |
| Integration | 2 worker |
| Testing | 2 worker |
| Review | 2-3 reviewer |

## Quality Standards

- Plans must be actionable without ambiguity
- Each task must have clear verification criteria
- Parallelism must be explicitly marked
- Dependencies must be traceable
- No time estimates (per CLAUDE.md rules)
- All verification commands must be executable

## Error Handling

### Task Failure
1. Log failure details to SUMMARY.md
2. Analyze cause (code error vs verification criteria)
3. Option A: Retry with refined instructions
4. Option B: Mark blocked, create HANDOFF.md

### Agent Timeout
1. Check output file for progress
2. If stuck: Kill and respawn with different approach
3. If making progress: Extend timeout

### Blocker Encountered
1. Stop current task
2. Create HANDOFF.md with blocker details
3. Document what can proceed independently

## Integration Points

- **execution-core**: Behavioral standards for agents (Uninterrupted Flow, Self-Verification)
- **software-engineering**: Quality standards (TDD, debugging, security)
- **plan-execution**: Internal execution protocols referenced by agents
- **project-strategy**: (deprecated) Templates now in builder-core/references/templates/
