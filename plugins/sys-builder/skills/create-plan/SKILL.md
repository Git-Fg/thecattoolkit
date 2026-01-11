---
name: create-plan
description: "USE when starting a new project or feature requiring planning. Auto-discovers codebase patterns and creates multi-phase plans in .cattoolkit/planning/{slug}/."
context: fork
agent: designer
allowed-tools: [Read, Write, Edit, Glob, Grep, Task, Bash(mkdir:-p), Bash(ls:*)]
---

# Create Plan Protocol

## Purpose

Create comprehensive, parallelism-optimized project plans with automatic codebase discovery. This skill is the **primary entry point** for all planning workflows.

## Canonical Output Location

**MANDATORY**: All planning artifacts MUST be created in:
```
.cattoolkit/planning/{project-slug}/
```

**NEVER** create PLAN.md, ROADMAP.md, or BRIEF.md at the project root.

## Execution Framework

### Phase 1: Initialize Structure

Create the planning directory if it doesn't exist:

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
    ├── 02-{name}/
    │   └── 02-01-PLAN.md
    └── ...
```

### Phase 2: Auto-Discovery

**Always run first** to understand the codebase before planning.

**Protocol:**
1. Launch 2-3 explore agents **in parallel** via Task tool
2. Each agent focuses on different aspects:
   - Agent 1: Architecture & structure (files, directories, patterns)
   - Agent 2: Dependencies & integrations (imports, APIs, external services)
   - Agent 3: Existing conventions (naming, testing, documentation)
3. Synthesize findings into DISCOVERY.md

**DISCOVERY.md Template:**
```markdown
# Discovery Report: {project-slug}

## Codebase Overview
{High-level architecture description}

## Key Patterns Identified
- {Pattern 1}: {where found, how used}
- {Pattern 2}: {where found, how used}

## Dependencies
- External: {list}
- Internal: {critical paths}

## Conventions
- Naming: {patterns}
- Testing: {framework, location}
- Documentation: {style}

## Constraints & Considerations
- {constraint 1}
- {constraint 2}

## Recommendations for Plan
- {recommendation based on discoveries}
```

### Phase 3: Create BRIEF.md

Use project-strategy templates. Include discoveries as context.

**Greenfield (v1.0):**
```markdown
# Project Brief: {name}
Version: 1.0

## Vision
{One sentence}

## Goals
1. {Goal 1}
2. {Goal 2}

## Non-Goals
- {Explicit exclusion}

## Success Criteria
- {Measurable outcome}

## Discovery Context
@.cattoolkit/planning/{slug}/DISCOVERY.md
```

**Brownfield (v1.1+):**
Add "Current State" section referencing DISCOVERY.md findings.

### Phase 4: Generate ROADMAP.md

Create roadmap with **explicit parallelism markers**:

```markdown
# Roadmap: {project-slug}

## Overview
{Brief description of the project}

## Phases

| Phase | Name | Status | Parallel Agents | Dependencies |
|-------|------|--------|-----------------|--------------|
| 01 | Discovery & Setup | pending | 2 explore | none |
| 02 | Core Implementation | pending | 3 worker | 01 |
| 03 | Integration | pending | 2 worker | 02 |
| 04 | Testing & Polish | pending | 2 worker | 03 (partial) |

## Phase Descriptions

### 01 - Discovery & Setup
**Agents**: 2 explore (parallel)
**Objective**: {what this phase accomplishes}
**Deliverables**: {list}

### 02 - Core Implementation
**Agents**: 3 worker (parallel)
**Objective**: {what this phase accomplishes}
**Deliverables**: {list}
**Depends on**: Phase 01 completion

...
```

### Phase 5: Create Phase PLAN.md Files

For each phase, create detailed execution plans:

```markdown
---
phase: {XX}-{name}
status: pending
parallel_agents: {N}
dependencies: [{list}]
---

## Objective
{What this phase accomplishes}

## Context
@.cattoolkit/planning/{slug}/BRIEF.md
@.cattoolkit/planning/{slug}/DISCOVERY.md
@.cattoolkit/planning/{slug}/ROADMAP.md

## Parallelism Analysis

| Task | Type | Can Parallel With | Agent |
|------|------|-------------------|-------|
| 1 | sequential | - | worker |
| 2 | parallel | 3, 4 | worker |
| 3 | parallel | 2, 4 | worker |
| 4 | parallel | 2, 3 | worker |
| 5 | background | all | worker |

## Tasks

### Task 1: {Action-oriented name}
**Type**: sequential
**Scope**: {files, directories, or concepts}
**Action**: {natural language description}
**Verify**: {command or check to prove completion}
**Done**: {measurable acceptance criteria}

### Task 2: {Action-oriented name}
**Type**: parallel
**Can run with**: Task 3, Task 4
**Scope**: {files}
**Action**: {description}
**Verify**: {command}
**Done**: {criteria}

...

## Verification
{Phase-level verification steps}

## Success Criteria
- [ ] {Criterion 1}
- [ ] {Criterion 2}
```

## Parallelism Guidelines

### Task Type Classification

**Sequential Tasks:**
- Task A produces output consumed by Task B
- Must complete before dependent tasks start
- Example: "Create database schema" before "Write migrations"

**Parallel Tasks:**
- Operate on different files/modules
- No shared dependencies
- Can execute simultaneously
- Example: "Implement UserService" and "Implement ProductService"

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

## Handoff Protocol

If blocked during planning:
1. Document blocker in HANDOFF.md
2. List questions needing answers
3. Specify what can proceed vs what's blocked
