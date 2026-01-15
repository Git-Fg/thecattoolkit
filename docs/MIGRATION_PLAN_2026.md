# 2026 Migration Plan: Heavy Commands to Skills

**January 2026**

## Executive Summary

This migration plan addresses critical architectural drift identified in the Cat Toolkit plugins. The core issue is **"Heavy Commands"** - commands containing extensive business logic that violates the 2026 standard mandating Commands be zero-token wrappers delegating to Skills.

**Severity: Critical** - Prevents reusability, bloats context, splits logic between Command/Skill.

---

## Table of Contents

1. [Scope of Changes](#scope-of-changes)
2. [Priority 1: sys-builder Commands](#priority-1-sys-builder-commands)
3. [Priority 2: sys-browser Commands](#priority-2-sys-browser-commands)
4. [Priority 3: sys-cognition Commands](#priority-3-sys-cognition-commands)
5. [Priority 4: Documentation Updates](#priority-4-documentation-updates)
6. [Validation Protocol](#validation-protocol)

---

## Scope of Changes

### Affected Components

| Plugin | Component | Issue | Impact | Priority |
|:-------|:----------|:------|:-------|:---------|
| **sys-builder** | `commands/plan.md` | 244 lines of workflow logic | Heavy Command | P1 |
| **sys-builder** | `commands/run-plan.md` | 380 lines of execution protocol | Heavy Command | P1 |
| **sys-builder** | `commands/manage-plan.md` | 473 lines of modification logic | Heavy Command | P1 |
| **sys-builder** | `commands/code-review.md` | 69 lines, documentation-heavy | Delegation OK, docs excessive | P5 |
| **sys-browser** | `commands/*.md` (4 files) | Missing `disable-model-invocation` | Context Pollution | P2 |
| **sys-cognition** | `commands/think.md` | 22 lines of persona logic | Heavy Command | P3 |
| **sys-agents** | `skills/architecting-agents/` | Missing Subagent cost warnings | Cost Efficiency | P4 |

### Already Compliant (No Action Required)

| Component | Lines | Status |
|:----------|:------|:-------|
| `sys-edge/commands/migrate-python.md` | 19 | Proper wrapper, delegates to `Skill(python-tools)` |
| `sys-core/commands/doctor.md` | 16 | Proper wrapper |
| All sys-browser commands | 17-20 | Just need `disable-model-invocation` field |

### Target State

**Commands become pure delegation wrappers:**
```yaml
---
description: "..."
allowed-tools: [Skill(target-skill)]
disable-model-invocation: true
---

Invoke `Skill(target-skill)` with intent: "$ARGUMENTS"
```

---

## Priority 1: sys-builder Commands

### Current State Analysis

**Files:**
- `plugins/sys-builder/commands/plan.md` (244 lines)
- `plugins/sys-builder/commands/run-plan.md` (380 lines)
- `plugins/sys-builder/commands/manage-plan.md` (473 lines)

**Problem:** These contain:
- Routing logic (autonomous vs interactive detection)
- Workflow protocols (Investigation → Synthesis → Plan Creation)
- Execution protocols (Read State → Dispatch → Verify)
- Modification protocols (Parse → Modify → Report)

**Should Be:** In `skills/managing-plans/SKILL.md` or dedicated sub-skills.

### Migration Strategy

#### Step 1: Create Planning Workflow Skill

**New Skill:** `plugins/sys-builder/skills/creating-plans/SKILL.md`

**Purpose:** Consolidate all planning workflow logic from `plan.md` command.

**Content Structure:**
```markdown
---
name: creating-plans
description: "Intelligently architects project plans using auto-detection for routing between autonomous and interactive workflows. Use when starting projects, planning features, or creating project roadmaps."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Skill(managing-plans), Skill(designing-architecture), AskUserQuestion]
context: fork
---

# Project Planning Workflow

## Routing Logic
[From plan.md: lines 19-41]

## Autonomous Workflow
[From plan.md: lines 42-91]

## Interactive Workflow
[From plan.md: lines 92-142]

## Detection Algorithm
[From plan.md: lines 165-192]
```

**References to Create:**
- `references/routing-logic.md` - Complexity detection and workflow selection
- `references/autonomous-workflow.md` - Investigation → Synthesis → Creation phases
- `references/interactive-workflow.md` - Discovery → Question Burst → Architecture phases

#### Step 2: Create Execution Workflow Skill

**New Skill:** `plugins/sys-builder/skills/executing-workflows/SKILL.md`

**Purpose:** Consolidate all execution protocol logic from `run-plan.md` command.

**Content Structure:**
```markdown
---
name: executing-workflows
description: "Manages project plan execution through state-based orchestration. Handles phase transitions, task dispatch, verification, and handoff protocols. PROACTIVELY Use when executing project plans, running phases, or coordinating task workflows."
allowed-tools: [Read, Write, Edit, Task, Skill(managing-plans)]
context: fork
---

# Plan Execution Workflow

## Phase 1: Read State
[From run-plan.md: lines 61-85]

## Phase 2: Dispatch to Worker
[From run-plan.md: lines 87-114]

## Phase 3: Verify Results
[From run-plan.md: lines 116-141]

## Phase 4: Continue Flow
[From run-plan.md: lines 143-168]
```

**References to Create:**
- `references/execution-states.md` - State transition protocols
- `references/worker-dispatch.md` - Agent spawning and context passing
- `references/handoff-creation.md` - Blocker documentation and recovery

#### Step 3: Create Plan Modification Skill

**New Skill:** `plugins/sys-builder/skills/modifying-plans/SKILL.md`

**Purpose:** Consolidate all modification logic from `manage-plan.md` command.

**Content Structure:**
```markdown
---
name: modifying-plans
description: "Manages plan file modifications including status updates, structural changes, and content edits. Use when updating plan files, modifying structure, viewing status, or resuming from handoffs."
allowed-tools: [Read, Write, Edit, Skill(managing-plans)]
context: fork
---

# Plan Modification Protocol

## Phase 1: Parse Request
[From manage-plan.md: lines 68-89]

## Phase 2: Modify Plan
[From manage-plan.md: lines 91-131]

## Phase 3: Report Changes
[From manage-plan.md: lines 133-167]
```

**References to Create:**
- `references/modification-types.md` - Status, structural, and content changes
- `references/validation-rules.md` - Pre/post modification validation
- `references/common-operations.md` - View, update, modify, resume patterns

#### Step 4: Atomize Commands

After skills are created, replace command content with pure delegation:

**plan.md:**
```markdown
---
description: "Intelligently architect project plans. Auto-detects complexity to route between autonomous and interactive modes."
argument-hint: "<project description> [--interactive] [--force-autonomous] [--skip-discovery] [--output-dir <path>]"
allowed-tools: [Skill(creating-plans)]
disable-model-invocation: true
---

Invoke `Skill(creating-plans)` with user input: "$ARGUMENTS".
```

**run-plan.md:**
```markdown
---
description: "Execute the next pending phase in the roadmap."
argument-hint: "[optional: phase number]"
allowed-tools: [Skill(executing-workflows)]
disable-model-invocation: true
---

Invoke `Skill(executing-workflows)` with phase input: "$ARGUMENTS".
```

**manage-plan.md:**
```markdown
---
description: "Update or modify existing plans."
argument-hint: "<status update or change request>"
allowed-tools: [Skill(modifying-plans)]
disable-model-invocation: true
---

Invoke `Skill(modifying-plans)` with modification request: "$ARGUMENTS".
```

### Validation Checklist

- [ ] Skills created with proper frontmatter
- [ ] All protocols migrated from commands
- [ ] References created and linked
- [ ] Commands atomized to delegation only
- [ ] `toolkit-analyzer.py` passes
- [ ] Skills work via `/sys-builder:plan` invocation
- [ ] Skills work via `Skill(creating-plans)` direct call

---

## Priority 2: sys-browser Commands

### Current State Analysis

**Files:**
- `plugins/sys-browser/commands/crawl.md`
- `plugins/sys-browser/commands/read.md`
- `plugins/sys-browser/commands/save.md`
- `plugins/sys-browser/commands/spider.md`

**Problem:** All missing `disable-model-invocation: true` in frontmatter.

**Risk:** Models may hallucinate tool calls to these commands or confuse them with actual tools.

### Migration Strategy

**Add missing frontmatter field to all four commands:**

```yaml
---
name: crawl
description: "Advanced crawling with configuration options (depth, format, etc)."
argument-hint: "<url> [options]"
allowed-tools: Bash
disable-model-invocation: true  # <-- ADD THIS LINE
---
```

### Validation Checklist

- [ ] All 4 commands updated with `disable-model-invocation: true`
- [ ] `toolkit-analyzer.py` passes
- [ ] Commands still execute correctly via `/crawl`, `/read`, etc.

---

## Priority 3: sys-cognition Commands

### Current State Analysis

**File:** `plugins/sys-cognition/commands/think.md` (22 lines)

**Problem:** Contains "Reasoning Facilitator" persona and instructions:
- "You are a Reasoning Facilitator..."
- Instructions for context check, analysis, framework selection
- Success criteria

**Should Be:** In a dedicated `facilitating-reasoning` skill.

### Migration Strategy

#### Step 1: Create Reasoning Facilitation Skill

**New Skill:** `plugins/sys-cognition/skills/facilitating-reasoning/SKILL.md`

```markdown
---
name: facilitating-reasoning
description: "Clarifies goals and applies structured thinking frameworks (Pareto, Inversion, First-Principles) to complex problems. Use when exploring constraints, analyzing decisions, or applying structured reasoning to uncover hidden assumptions."
allowed-tools: [Read, Skill(applying-reasoning), AskUserQuestion]
---

# Reasoning Facilitation Protocol

## Purpose
Help users clarify their thinking using structured frameworks before solving problems.

## Instructions
1. **Context Check**: Read `.cattoolkit/context/scratchpad.md` if exists
2. **Analyze Input**: Parse user's problem statement
3. **Select Frameworks**: Choose most relevant from `applying-reasoning` skill
4. **Targeted Questions**: Ask actionable questions based on frameworks to uncover hidden assumptions

## Success Criteria
- User provides specific constraints not initially mentioned
- Problem narrowed to actionable scope
- Session context preserved in scratchpad
```

#### Step 2: Atomize Command

```markdown
---
description: "USE when clarifying goals, exploring constraints, or applying structured thinking frameworks to complex problems."
argument-hint: "What is the problem or decision you are facing?"
allowed-tools: [Skill(facilitating-reasoning)]
disable-model-invocation: true
---

Invoke `Skill(facilitating-reasoning)` with user's problem: "$ARGUMENTS".
```

### Validation Checklist

- [ ] `facilitating-reasoning` skill created
- [ ] Protocols migrated from command
- [ ] Command atomized to delegation
- [ ] `toolkit-analyzer.py` passes
- [ ] `/think` command works correctly

---

## Priority 4: Documentation Updates

### sys-agents Subagent Cost Warnings

**File:** `plugins/sys-agents/skills/architecting-agents/SKILL.md`

**Current Issue:** Section 6 "Context Isolation" discusses sub-agents without warning about costs.

**Required Changes:**

#### Add Warning Section at Top of SKILL.md

```markdown
## Cost Warning (CRITICAL)

Before using sub-agents, understand the costs:

| Approach | Token Cost | Quota Cost | When to Use |
|:---------|:-----------|:-----------|:------------|
| **Inline** | ~1x | Free (tool call) | Most tasks |
| **Fork** | ~3x | Free (tool call) | Isolation needed |
| **Subagent** | ~25k+ | 1 prompt per spawn | Parallelization only |

**Default Recommendation:** Use `context: fork` in skills for isolation. Subagents are ONLY appropriate when parallelization speed clearly exceeds 20K token startup cost AND quota overhead.

See [docs/SUBAGENT_CRISIS.md](../../../../docs/SUBAGENT_CRISIS.md) for detailed evidence.
```

#### Update Section 6: Context Isolation

Replace current subagent promotion with fork-first guidance:

```markdown
## 6. Context Isolation

**Principle:** Delegate tasks with isolated context windows.

**Default Approach: Use `context: fork`**

```yaml
---
name: processing-batch
description: "Processes multiple files in isolated context"
context: fork
allowed-tools: [Read, Write, Bash]
---
```

**Cost:** ~3x inline, but FREE as tool call within prompt quota.
**Use for:** Heavy operations (>10 files), parallel processing, isolation needs.

**Subagent Alternatives (Use Sparingly)**

ONLY when parallelization benefit > 20K token startup cost:

| Scenario | Pattern | Recommendation |
|:---------|:--------|:---------------|
| Parallelizable tasks | Map-reduce | Use fork unless >50 parallel units |
| Long-running tasks | Ralph Loop | Use fork with persistent files |
| Independent checks | Parallel reviewers | Use fork for cost efficiency |
```

### Validation Checklist

- [ ] Cost warning added to top of SKILL.md
- [ ] Section 6 updated with fork-first guidance
- [ ] Links to SUBAGENT_CRISIS.md added
- [ ] Subagent recommendations qualified with cost warnings

---

## Priority 5: Documentation-Heavy Commands (Optional)

### code-review Command Optimization

**File:** `plugins/sys-builder/commands/code-review.md` (69 lines)

**Current State:**
- Already delegates correctly to `Skill(software-engineering)`
- Has `disable-model-invocation: true`
- Issue: Contains extensive documentation (modes, examples, workflow) that belongs in skill references

**Migration Strategy:**

#### Step 1: Move Documentation to Skill

**Update:** `plugins/sys-builder/skills/software-engineering/SKILL.md` references

Add to `references/review-workflow.md`:
```markdown
## Command Usage

### Interactive Mode (default)
```
/sys-builder:code-review
```
Prompts for target files/directories and analysis preferences.

### Direct Mode
```
/sys-builder:code-review analyze <path>
```
Runs full static analysis on specified path without prompts.

### Examples
- Interactive review of staged changes: `/sys-builder:code-review`
- Analyze specific file: `/sys-builder:code-review analyze src/api/users.ts`
- Full project scan: `/sys-builder:code-review analyze .`
- Security-focused scan: `/sys-builder:code-review security .`
```

#### Step 2: Simplify Command

```markdown
---
description: "Quick access to code review and static analysis capabilities. Runs automated checks including linting, type checking, and security scanning."
argument-hint: "[mode] [target]"
allowed-tools: [Skill(software-engineering)]
disable-model-invocation: true
---

Invoke `Skill(software-engineering)` for code review workflow with inputs: "$ARGUMENTS".

See [software-engineering references](../skills/software-engineering/references/review-workflow.md) for usage examples.
```

**Result:** Command reduced from 69 lines to ~10 lines.

### Validation Checklist

- [ ] Documentation moved to skill reference
- [ ] Command simplified to delegation + reference link
- [ ] `toolkit-analyzer.py` passes
- [ ] Command still functions correctly

---

## Validation Protocol

### Pre-Commit Validation

After completing each priority level:

```bash
# Run toolkit analyzer
uv run scripts/toolkit-analyzer.py

# Auto-fix if possible
uv run scripts/toolkit-analyzer.py --fix

# Verify skills load
claude --plugin-dir ./plugins/sys-builder
claude --plugin-dir ./plugins/sys-browser
claude --plugin-dir ./plugins/sys-cognition
claude --plugin-dir ./plugins/sys-agents

# Test command invocation
/sys-builder:plan "test"
/sys-browser:crawl "https://example.com"
/sys-cognition:think "test problem"
```

### Post-Migration Verification

1. **Functional Testing:**
   - [ ] All commands execute via CLI
   - [ ] All skills invoke via `Skill()` tool
   - [ ] No regressions in functionality

2. **Token Efficiency:**
   - [ ] Commands are <20 lines each
   - [ ] Skills properly use `context: fork` where appropriate
   - [ ] No duplicate logic between command/skill

3. **Documentation:**
   - [ ] CLAUDE.md reflects current architecture
   - [ ] README.md updated if needed
   - [ ] SUBAGENT_CRISIS.md referenced where appropriate

---

## Implementation Order

Recommended execution sequence:

1. **Priority 2 (sys-browser)** - Quick fix, low risk (add `disable-model-invocation`)
2. **Priority 3 (sys-cognition)** - Single command, isolated (think command)
3. **Priority 1 (sys-builder)** - Most complex, careful execution (plan, run-plan, manage-plan)
4. **Priority 4 (docs)** - After code changes settled (subagent warnings)
5. **Priority 5 (code-review)** - Optional polish (documentation consolidation)

**Rationale:**
- Start with low-risk fixes to build momentum
- Tackle isolated components before interconnected ones
- Handle complex refactoring when framework is proven
- Update docs after code stabilizes
- Optional polish can be deferred or skipped

---

## Rollback Plan

If issues arise:

1. **Revert Commands:** Restore original command files from git
2. **Keep Skills:** New skills can remain as reusable capabilities
3. **Update Delegation:** Commands can delegate to new skills if desired
4. **Document Issues:** Report findings for future refinement

---

## Success Criteria

Migration complete when:

- [ ] All commands are <20 lines (pure delegation)
- [ ] All business logic in skills
- [ ] `toolkit-analyzer.py` passes with no errors
- [ ] All commands function correctly
- [ ] Subagent cost warnings present in documentation
- [ ] `disable-model-invocation` present on all commands
