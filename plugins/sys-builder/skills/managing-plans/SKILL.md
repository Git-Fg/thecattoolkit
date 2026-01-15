---
name: managing-plans
description: "Orchestrates project plan state management and execution. Manages ROADMAP.md state tracking, task dispatch, phase transitions, and handoff protocols. PROACTIVELY Use when managing project plans, executing phases, or coordinating task workflows. MUST Use for all plan-related operations (creation, modification, execution). Do not use for architecture design, system analysis, or creating new projects without a plan."
context: fork
allowed-tools: [Read, Write, Edit, Glob, Bash, Task]
---

# Project Plan State Management

## Core Purpose

Orchestrates project execution through state-based plan management:

1. **State Management**: Track progress via ROADMAP.md phase files
2. **Task Dispatch**: Execute tasks through worker agents
3. **Phase Transitions**: Manage [ ] → [~] → [x] → [!] state flow
4. **Handoff Protocols**: Document blockers and enable seamless transfers

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

## Execution Checklist

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

**Categories:**
1. **Execution Errors**: Code errors, build failures
2. **State Errors**: Inconsistent state, corrupted files
3. **Dependency Errors**: Missing dependencies, version conflicts
4. **Resource Errors**: Out of memory, disk full, timeout

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
