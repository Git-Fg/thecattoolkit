---
name: managing-plans
description: "Orchestrates project plan state management and execution. Manages ROADMAP.md state tracking, task dispatch, phase transitions, and handoff protocols. PROACTIVELY Use when managing project plans, executing phases, or coordinating task workflows. MUST Use for all plan-related operations (creation, modification, execution). Do not use for architecture design, system analysis, or creating new projects without a plan → see designing-architecture skill."
context: fork  # Required: Processes entire project directory (10+ files), coordinates task dispatch across multiple phases
allowed-tools: [Read, Write, Edit, Glob, Bash, Task]
---

# Project Plan State Management



## State Model

### Plan State (ROADMAP.md)
```markdown
- [ ] = Pending
- [~] = In Progress
- [x] = Complete
- [!] = Blocked
```

### Phase State
- Task Status: [ ] → [~] → [x]
- Handoff: Created when blocked
- Summary: Created when complete

## Quick Reference

### Templates
- **Roadmap**: `assets/templates/roadmap.md` - Phase-based progress tracking
- **Handoff**: `assets/templates/handoff.md` - Blocker documentation

### References
- **Creation**: `references/creation-workflow.md` - Logic for planning new projects (Autonomous vs Interactive)
- **Modification**: `references/modification-workflow.md` - Protocols for updating plans
- **Execution**: `references/execution-workflow.md` - State-based execution logic
- **State**: `references/state-management.md` - State tracking protocols
- **Handoffs**: `references/handoff-protocols.md` - Handle blockers and transfers
- **Verification**: `references/verification-workflows.md` - Success verification at task/phase/plan levels

## Execution Protocol
1. **Read State**: Read `.cattoolkit/plan/{project-slug}/ROADMAP.md` to find the active phase.
2. **Read Tasks**: Read the active phase file (e.g., `phases/01-setup/01-01-PLAN.md`).
3. **Execute Loop**:
   - Pick next `[ ]` task
   - **Execute**: Write code, run commands
   - **Verify**: Run tests/checks (Self-Correction)
   - **Mark Complete**: Edit phase file to `[x]`
4. **Stop**: When phase is done or blocked.

## Execution Checklist (Quick Reference)

### Phase Start
- [ ] Read ROADMAP.md & verify dependencies
- [ ] Update status [ ] → [~]

### Task Execution
- [ ] Dispatch to worker agent (non-interactive)
- [ ] Monitor & verify completion
- [ ] Update task status immediately

### Phase Complete
- [ ] All tasks [x] complete
- [ ] Create phase summary
- [ ] Update ROADMAP.md [~] → [x]

### Handoff Required
- [ ] Identify blocker
- [ ] Create HANDOFF.md using template
- [ ] Update status [~] → [!]
- [ ] Pause execution

## Error Handling



**Recovery Strategy:**
- Level 1: Automatic recovery (retry, clear cache, restart)
- Level 2: Partial recovery (skip task, use alternative)
- Level 3: Handoff required (authentication, critical errors, decisions)

## State Management Protocol

1. **Read State**: Always read ROADMAP.md before starting work
2. **Update State**: Update task status immediately upon completion
3. **Atomic Commits**: One commit per checkmark for reproducibility
4. **Handoff Creation**: Create HANDOFF.md for blockers
5. **Verification**: Verify completion at task, phase, and plan levels

## Architecture Decision Records

**When to Create ADR:**
- Technology stack changes
- Major architectural patterns
- Breaking API changes
- Infrastructure additions
- Significant refactors

**Protocol:**
- Auto-increment numbering (ADR-001, ADR-002, etc.)
- Append-only to `.cattoolkit/plan/{project}/ADR.md`
- Never delete or modify old entries

**Note**: For architecture design and system analysis, use `designing-architecture` skill.
