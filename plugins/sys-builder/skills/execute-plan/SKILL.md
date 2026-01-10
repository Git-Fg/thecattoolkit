---
name: execute-plan
description: |
  USE when ready to execute a plan created by create-plan.
  Orchestrates parallel agent execution following the plan's dependency graph.
  Reads from .cattoolkit/planning/{slug}/ and updates progress in-place.
context: fork
agent: director
allowed-tools: [Read, Write, Edit, Glob, Grep, Task, AskUserQuestion, Bash]
---

# Execute Plan Protocol

## Purpose

Execute project plans with optimized parallel agent orchestration. This skill is the **primary entry point** for all plan execution workflows.

## Canonical Input Location

**MANDATORY**: Plans MUST be read from:
```
.cattoolkit/planning/{project-slug}/
```

## Execution Framework

### Phase 1: Load Plan

1. Read ROADMAP.md for phase overview
2. Identify current phase (first pending or specified)
3. Read phase PLAN.md for task details
4. Parse parallelism analysis table

### Phase 2: User Intent Clarification

**Always ask user** via AskUserQuestion to determine execution mode:

```
Question: How would you like to execute this plan?

Options:
1. Start from Phase 1 (fresh execution)
2. Resume from Phase {X} (continue where left off)
3. Execute all remaining phases
4. Refine/update the plan first
```

**Based on response:**
- Fresh: Start from Phase 01, reset all statuses
- Resume: Continue from specified phase
- All remaining: Execute pending phases in order
- Refine: Return to create-plan for modifications

### Phase 3: Analyze Parallelism

For each task in the phase, classify:

**Sequential Tasks:**
- Must wait for previous task
- Has explicit dependency in "Can Parallel With" column showing "-"
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

```markdown
For parallel tasks 2, 3, 4:
- Send SINGLE message with 3 Task tool calls
- Each Task call spawns a worker agent
- Provide complete context to each agent including:
  - BRIEF.md content
  - DISCOVERY.md content
  - Task-specific scope and action
  - Verification criteria
```

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
3. **Verify outputs** - Run verification commands from "Verify" column
4. **Log results** - Write to phase SUMMARY.md

**Verification Protocol:**
```markdown
For each completed task:
1. Run "Verify" command/check
2. Compare against "Done" criteria
3. If PASS: Mark task complete
4. If FAIL: Log failure, decide retry vs escalate
```

### Phase 6: Update State

**After each task:**
- Update task status in PLAN.md (pending → in_progress → completed)

**After each phase:**
- Update phase status in ROADMAP.md
- Create SUMMARY.md with:
  - Tasks completed
  - Verification results
  - Time spent (if tracked)
  - Issues encountered
  - Lessons learned

**On blocker:**
- Create HANDOFF.md with:
  - Blocker description
  - Questions needing answers
  - What can proceed vs blocked
  - Suggested resolution

## Execution Patterns

### Pattern 1: Pure Sequential
```
Task 1 → Task 2 → Task 3
```
Execute one at a time, wait for completion.

### Pattern 2: Pure Parallel
```
[Task 1, Task 2, Task 3] (all at once)
```
Single message with multiple Task calls.

### Pattern 3: Sequential then Parallel
```
Task 1 → [Task 2, Task 3, Task 4]
```
Complete Task 1, then launch 2-4 simultaneously.

### Pattern 4: Parallel with Background
```
[Task 1, Task 2] + Task 3 (background)
```
Launch 1-2 foreground, 3 with `run_in_background: true`.

## State Management

### ROADMAP.md Status Values
- `pending` - Not started
- `in_progress` - Currently executing
- `completed` - All tasks done and verified
- `blocked` - Waiting on external input

### PLAN.md Task Status
- `pending` - Not started
- `in_progress` - Agent executing
- `completed` - Verified done
- `failed` - Verification failed
- `blocked` - External dependency

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
3. Ask user: Continue with other tasks or pause entirely?

## Quality Standards

- All tasks must be verified before marking complete
- Parallel execution must respect dependency constraints
- State files must be updated in real-time
- SUMMARY.md must capture actionable insights
- Handoffs must enable seamless session continuation

## Integration Points

- **create-plan**: Source of plans to execute
- **execution-core**: Behavioral standards for agents
- **project-strategy**: Templates for SUMMARY.md, HANDOFF.md
- **context-engineering**: Session state persistence
