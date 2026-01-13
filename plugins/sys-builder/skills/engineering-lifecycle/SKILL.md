---
name: engineering-lifecycle
description: "Manages project state, architecture, and execution plans. SHOULD Use when starting projects, planning features, or tracking progress."
allowed-tools: [Read, Write, Edit, Glob, Bash]
---

# Engineering Lifecycle

## Core Principle
You manage the project lifecycle. The state is strictly stored in `.cattoolkit/plan/`. This directory is the **Single Source of Truth**. You do not need "permission" to update these files; staying in sync with reality is your primary directive.

## Artifact Schemas

### 1. The Brief (`BRIEF.md`)
**Purpose:** The "Why" and "What".
**Content:**
- Note high-level requirements.
- Define Success Criteria (Testable & Measurable).
- List technical constraints.

### 2. The Roadmap (`ROADMAP.md`)
**Purpose:** The "When". A living state machine of the project.
**Format:**
```markdown
# Project Roadmap

## Phase 1: Foundation
- [x] Task A
- [x] Task B

## Phase 2: Core Logic
- [~] Task C (In Progress)
- [ ] Task D
```
**Rules:**
- **[ ] Pending:** Not started.
- **[~] In Progress:** Currently working on this. Only ONE phase should be active.
- **[x] Done:** Verified and committed.

### 3. The Implementation (`phases/*.md`)
**Purpose:** The "How".
**Content:** 
- Detailed checklists for complex phases.
- Technical specs and architectural decisions.
- Specific file paths and verification steps.

## Execution Rules
1.  **Read First:** Always read `ROADMAP.md` before starting work to ground yourself.
2.  **Update Immediately:** As soon as a task is done/verified, mark it `[x]`.
3.  **Atomic Commits:** Each checkmark typically corresponds to a potential git commit.
4.  **Blockers are Handoffs:** If you are stuck or need user input, create `HANDOFF.md` with:
    - Current State
    - The Blocker/Question
    - Context for the next session
    - Then stop and notify the user.

## Reference Library
- `references/discovery.md`: Protocol for analyzing a new codebase.
- `references/architecture-patterns.md`: Guide for breaking down work.
