---
name: managing-project-plans
description: "Manages project lifecycle from inception to completion. Handles state management, execution orchestration, architecture design, and plan management. PROACTIVELY Use when creating, executing, or managing project plans."
context: fork
allowed-tools: [Read, Write, Edit, Glob, Bash, Task]
---

# Project Lifecycle Management

## Core Purpose

This skill manages the complete project lifecycle across four integrated capabilities:

1. **State Management**: Track progress via BRIEF.md, ROADMAP.md, and phase files
2. **Execution Orchestration**: Dispatch tasks, manage state transitions, verify completion
3. **Architecture Design**: Apply system design frameworks, create ADRs, analyze requirements
4. **Plan Management**: Create, update, and maintain project plans and handoffs

## Integration Pattern

This skill **orchestrates**:
- Worker agent execution for tasks
- Architecture designer agent for design work
- State tracking across all project phases
- Handoff protocols for blockers

This skill **uses**:
- Templates for consistent artifacts (BRIEF, ROADMAP, HANDOFF)
- References for detailed methodology
- Agents for specialized execution

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

### 1. Project Creation & Planning
**Templates:**
- **Brief**: `assets/templates/brief.md` - Project requirements and success criteria
- **Roadmap**: `assets/templates/roadmap.md` - Phase-based progress tracking
- **Handoff**: `assets/templates/handoff.md` - Blocker documentation

**Methodology:**
- **Discovery**: `references/discovery.md` - Analyze existing systems
- **Architecture**: `references/system-design.md` - System design workflows
- **Patterns**: `references/architecture-patterns.md` - Design patterns guide

### 2. State Management
**Protocol:**
- Read `ROADMAP.md` before starting work
- Update task status immediately upon completion
- Use atomic commits for each checkmark
- Create `HANDOFF.md` for blockers

**Reference:**
- `references/state-management.md` - State tracking protocols

### 3. Execution Orchestration
**Process:**
1. Check ROADMAP.md for phase status
2. Verify dependencies are [x] complete
3. Update phase status [ ] → [~]
4. Dispatch tasks to worker agent
5. Verify completion and update state

**References:**
- `references/verification-workflows.md` - Success verification at task/phase/plan levels
- `references/handoff-protocols.md` - Handle blockers and transfers

### 4. Architecture & Design
**Workflow:**
1. **Discovery**: Apply `references/discovery.md` to gather requirements
2. **Design**: Use `references/system-design.md` for new systems
3. **Documentation**: Create ADRs using `references/adr-template.md`
4. **Quality**: Validate using `references/quality-checklist.md`

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
