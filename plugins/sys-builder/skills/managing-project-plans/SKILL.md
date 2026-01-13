---
name: managing-project-plans
description: "Passive library of templates and standards for .cattoolkit/plan/ filesystem. USE when needing schemas for BRIEF, ROADMAP, or PHASE files."
allowed-tools: [Read, Write, Edit, Glob, Bash]
disable-model-invocation: true
---

# Managing Project Plans: Standards & Schema

## Core Philosophy

**State-in-Files:** The filesystem (`.cattoolkit/plan/`) is the source of truth.

This skill provides **templates and standards** ONLY. It does NOT define workflows or orchestration logic.

## File System Standard

All planning state is persisted in `.cattoolkit/plan/`.

### File Structure

```
.cattoolkit/plan/{project-slug}/
├── BRIEF.md           # Project definition
├── DISCOVERY.md       # Auto-discovery findings
├── ROADMAP.md         # Master list of phases with status
├── ADR.md             # Architecture Decision Records (optional)
└── phases/
    ├── 01-{name}/
    │   └── 01-01-PLAN.md
    └── 02-{name}/
        └── 02-01-PLAN.md
```

### Manus 3-File Pattern (Optional)

For simple tasks, use:
```
.cattoolkit/plan/{project-slug}/
├── task_plan.md       # Track phases and progress
├── notes.md           # Store findings and research
└── deliverable.md     # Final output
```

## File Schemas

### 1. BRIEF.md (The North Star)

**Purpose:** High-level goals, constraints, and success criteria.

**Schema:**
```markdown
# Project: {name}

## Objective
Clear, concise statement of what needs to be built

## Success Criteria
- [ ] Measurable criterion 1
- [ ] Measurable criterion 2
- [ ] Measurable criterion 3

## Constraints
- Technical constraints
- Business constraints
- Timeline constraints

## Current State (Brownfield only)
- Existing implementation
- Known issues
- Migration requirements
```

**Update Rule:** Only update when project scope changes significantly.

### 2. ROADMAP.md (The State Machine)

**Purpose:** Master list of phases and their status.

**Schema:**
```markdown
# Roadmap: {project-name}

## Phases

| Phase | Name | Status | Dependencies |
|-------|------|--------|--------------|
| 01 | Phase Name | [ ] | none |
| 02 | Phase Name | [ ] | 01 |
| 03 | Phase Name | [ ] | 02 |

## Status Codes
- `[ ]` = Pending (not started)
- `[~]` = In Progress (currently executing)
- `[x]` = Complete (finished)
- `[!]` = Blocked (needs intervention)

## Dependency Rule
Phase N cannot start until Phase N-1 is `[x]`.
```

### 3. Phase Plan Files (The Work Order)

**Purpose:** Atomic tasks for the Worker agent.

**Schema:**
```markdown
# Phase {XX}: {name}

## Tasks

### Task 1: {name}
**Scope:** {files/directories to modify}
**Action:** {what to do}
**Verify:** {how to verify success}
**Done:** {acceptance criteria}

### Task 2: {name}
**Scope:** {files/directories to modify}
**Action:** {what to do}
**Verify:** {how to verify success}
**Done:** {acceptance criteria}

## Handoff
If blocked, create `HANDOFF.md` in this directory with:
- What's been completed
- What's blocking progress
- What needs to happen next
```

### Manus 3-File Pattern (Optional)

For simple tasks (3-5 phases), use the Manus pattern:

#### File 1: task_plan.md
**Purpose:** Track phases, progress, decisions, and errors
**Schema:** See `references/task-plan-template.md`

#### File 2: notes.md
**Purpose:** Store research findings, sources, and intermediate work
**Schema:** See `references/notes-template.md`

#### File 3: deliverable.md
**Purpose:** Final output, synthesis, or deliverable
**Schema:** See `references/deliverable-template.md`

## Validation Rules

### 1. File Naming
- BRIEF.md: Must exist at project root
- ROADMAP.md: Must exist at project root
- Phase files: Must be in `phases/` directory
- Phase directories: Must be `XX-name` format (e.g., `01-setup`)

### 2. Status Codes
Only these codes are valid:
- `[ ]` = Pending
- `[~]` = In Progress
- `[x]` = Complete
- `[!]` = Blocked

### 3. Dependencies
- Phase N must depend on Phase N-1 being complete
- No circular dependencies allowed
- Dependencies must be explicitly stated in ROADMAP.md

## Templates

All templates are in `assets/templates/`:

| Template | File | Purpose |
|:---------|:-----|:--------|
| BRIEF | `brief.md` | Project definition |
| ROADMAP | `roadmap.md` | Multi-phase overview |
| Phase Plan | `phase-plan.md` | Executable phase tasks |
| HANDOFF | `handoff.md` | Session pause/resume |
| SUMMARY | `summary.md` | Phase completion |

## Usage Guidelines

**For Commands:**
- Use this skill's schemas when creating or modifying plan files
- Reference templates from `assets/templates/`
- Apply validation rules when checking file integrity

**For Agents:**
- Read plan files to understand current state
- Update status codes according to execution progress
- Create HANDOFF.md when blocked

**NOT Workflow Logic:**
This skill does NOT define:
- How to investigate a codebase
- When to ask user questions
- How to dispatch worker agents
- How to handle errors

Those workflows belong in Commands and specialized skills, not here.

## Quick Reference

### Creating a New Plan
1. Use `brief.md` template for BRIEF.md
2. Use `roadmap.md` template for ROADMAP.md
3. Use `phase-plan.md` template for phase files

### Validating a Plan
1. Check file structure matches standard
2. Verify status codes are valid
3. Confirm dependencies are correct

### Updating Progress
1. Change `[ ]` to `[~]` when starting a task
2. Change `[~]` to `[x]` when completing a task
3. Change `[ ]` to `[!]` when blocked

## References

**See:**
- `references/task-plan-template.md` - Manus pattern schema
- `references/notes-template.md` - Research notes schema
- `references/deliverable-template.md` - Final output schema
- `assets/templates/` - All document templates
