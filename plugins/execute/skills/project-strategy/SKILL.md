---
name: project-strategy
description: |
  USE when creating project plans, BRIEF.md, ROADMAP.md, or phase PLAN.md documents.
  Project planning standards, document templates (BRIEF, ROADMAP, PLAN), and format specifications.
user-invocable: false
allowed-tools: Read, Write, Edit
---

# Project Strategy Standards

## Core Purpose

**This skill defines WHAT documents to create and their structure.**

It answers: "What templates and formats should I use?" (not "How to execute them").

**HOW to execute** is defined by `execution-core` skill (Uninterrupted Flow, Self-Verification, Handoffs).

## Skill Contents

**Document Templates:**
- `assets/templates/brief.md` - Project brief (v1.0 greenfield, v1.1+ brownfield)
- `assets/templates/roadmap.md` - Project roadmap with phases
- `assets/templates/phase-plan.md` - Executable phase plans
- `assets/templates/handoff.md` - Session handoff template
- `assets/templates/summary.md` - Phase completion summary
- `assets/templates/issues.md` - Deferred enhancements tracking

**Format Standards:**
- `references/plan-format.md` - PLAN.md structure guidelines
- `references/context-management.md` - Context organization in plans

## Document Templates

### Quick Reference

| Document Type | Template Location | Use Case |
|---------------|------------------|----------|
| Project Brief | `assets/templates/brief.md` | Project starts (v1.0) or iterations (v1.1+) |
| Roadmap | `assets/templates/roadmap.md` | Multi-phase projects |
| Phase Plan | `assets/templates/phase-plan.md` | Executable phases |
| Handoff | `assets/templates/handoff.md` | Session pauses mid-phase |
| Summary | `assets/templates/summary.md` | Phase completions |
| Issues | `assets/templates/issues.md` | Deferred enhancements |

### Location Standards

**Project Documents:** `.cattoolkit/planning/{project-slug}/`
- BRIEF.md - Template: `assets/templates/brief.md`
- ROADMAP.md - Template: `assets/templates/roadmap.md`
- ISSUES.md - Template: `assets/templates/issues.md`

**Phase Documents:** `.cattoolkit/planning/{project-slug}/phases/XX-name/`
- PLAN.md - Template: `assets/templates/phase-plan.md`
- SUMMARY.md - Template: `assets/templates/summary.md`
- HANDOFF.md - Template: `assets/templates/handoff.md`

## YAML Frontmatter Standards

**Standard Format for Documents:**

**BRIEF.md:**
```yaml
---
project: [Project Name]
version: 1.0
status: in_progress
---
```

**ROADMAP.md:**
```yaml
---
project: [Project Name]
version: 1.0
status: in_progress
---
```

**PLAN.md:**
```yaml
---
phase: XX-name
type: execute
status: in_progress
---
```

**Valid Status Values:** `in_progress`, `completed`

## Document Structure Standards

### BRIEF.md Standards

**Greenfield (v1.0):**
- Must keep under 50 lines
- Must have measurable/verifiable success criteria
- Must define out of scope to prevent scope creep
- Single human-focused document

**Brownfield (v1.1+):**
- Include Current State section with shipped version info
- User metrics, feedback, codebase stats
- Known issues needing attention
- Next version goals with vision and motivation

See `assets/templates/brief.md` for full template.

### ROADMAP.md Standards

**Initial Planning (v1.0):**
- Must have 3-6 phases total
- Must deliver something coherent per phase
- Must split phases with >7 tasks or multiple subsystems
- Must use naming: `{phase}-{plan}-PLAN.md`
- STRICTLY PROHIBITED: Time estimates

**After Milestones:**
- Must reorganize with milestone groupings
- Must collapse completed milestones in `<details>` tags
- Must keep continuous phase numbering

See `assets/templates/roadmap.md` for full template.

### PLAN.md Standards

**Structure Requirements:**
- YAML frontmatter complete (phase, type: execute, status)
- Objective section with purpose and output
- Context section with @ file references
- 2-3 tasks per plan (split if >7 tasks)
- Each task has: Scope (optional)/Action/Verify/Done
- Verification section for phase-level checks
- Success criteria section with measurable outcomes
- Output section specifying SUMMARY.md structure

**Task Standards:**
- Write naturally - narrative prose, not checklists
- Scope can be files, directories, or architectural concepts
- Verify must be executable (command, test, observable check)
- Action includes context (what, how, pitfalls)

See `references/plan-format.md` for detailed task structure guidelines.

### HANDOFF.md Standards

**Purpose:** Enable "State-in-Files" architecture when pausing mid-phase

**Triggers:**
- Authentication gates (credentials required)
- Critical failures (unrecoverable errors)
- Ambiguous requirements (task unclear)
- Session checkpoints (human-requested)

**Requirements:**
- Must be specific: "Left off at line 42" not "Was working on auth"
- Must list everything: all files modified, decisions made
- Must order actions: next steps must be executable in order
- Must delete on complete: handoff is temporary state

See `assets/templates/handoff.md` for full template.

## Format Validation Standards

### BRIEF.md Compliance

- [ ] Contains project one-liner
- [ ] Success criteria are measurable
- [ ] Out of scope prevents creep
- [ ] Under 50 lines (v1.0) or includes current state (v1.1+)

### ROADMAP.md Compliance

- [ ] 3-6 phases total
- [ ] Each phase has goal and dependencies
- [ ] Progress table tracks completion
- [ ] Plan counts realistic

### PLAN.md Compliance

- [ ] YAML frontmatter complete
- [ ] Context lists @references
- [ ] Tasks have Files, Action, Verify, Done
- [ ] 2-3 tasks per plan

### Execution Document Compliance

**SUMMARY.md Compliance:**
- [ ] Substantive one-liner (not "phase complete")
- [ ] Files created/modified listed
- [ ] Verification evidence included
- [ ] Deviations documented
- [ ] Next steps clear

**HANDOFF.md Compliance:**
- [ ] Clear reason category
- [ ] What happened description
- [ ] Specific next actions
- [ ] Verification method
- [ ] Resume instructions

## Behavioral Integration

### Using execution-core for HOW

**This skill defines WHAT to create. HOW to execute is in execution-core:**

- **Uninterrupted Flow** - Defined by `execution-core/references/observation-points.md`
- **Self-Verification** - Defined by `execution-core/references/observation-points.md`
- **Authentication Gates** - Defined by `execution-core/references/auth-gates.md`
- **Handoff Protocol** - Defined by `execution-core/references/handoff-protocol.md`

**Example Integration:**

When creating a PLAN.md:
1. Use `assets/templates/phase-plan.md` for structure (project-strategy)
2. Reference execution-core for behavioral protocols (HOW to execute)
3. Tasks should specify "Execute in Uninterrupted Flow" (from execution-core)
4. Verification uses Self-Verification Points (from execution-core)

### Standards Hierarchy

```
execution-core (HOW to behave)
    ↓
project-strategy (WHAT documents to create)
    ↓
director/worker agents (Execute using these standards)
```

## Usage in Commands

Commands reference project-strategy for document standards:

**Example from /plan command:**
```
Use project-strategy templates to create BRIEF.md and ROADMAP.md
Validate plan structure against project-strategy specifications
```

**Example from /execute command:**
```
Use project-strategy PLAN.md format for phase execution
Reference execution-core for behavioral protocols during execution
```

## Key Principles

1. **Document First:** Strategy defines document structure
2. **Format Consistency:** All projects use same templates
3. **Progressive Enhancement:** Brownfield builds on greenfield
4. **Behavioral Separation:** WHAT (strategy) separate from HOW (execution-core)
5. **State-in-Files:** All decisions and progress in files
