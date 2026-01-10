---
name: plan-execution
description: |
  USE when executing a project plan (PLAN.md).
  Orchestrates the execution of tasks, manages dependencies, delegates to worker agents, and verifies results.
context: fork
agent: director
allowed-tools: [Task, Read, Write, Bash(ls:*), Bash(cat:*), Bash(grep:*), Glob, Grep]
---

# Plan Execution Protocol

## Important: User-Facing Entry Point

**For user-invoked plan execution, use `/execute-plan` skill.**

This skill provides the execution protocols and standards. The execute-plan skill is the primary user-facing interface that wraps this functionality with user intent clarification.

## 1. Context Discovery (MANDATORY)

**Locate and read context files:**
You MUST locate and read:
- `BRIEF.md` (project brief)
- `PLAN.md` (the execution plan)
- `ADR.md` (architecture decisions, if exists)

**Discovery Strategy:**
- Follow `project-strategy` standards for file location.
- Use Glob tool to locate PLAN.md files if needed.

**If any required file is missing:** Log error and abort.

### 1.1 Resumability Check (CRITICAL)

**State-in-Files Enforcement:**
Before proceeding with execution, you MUST check for interruption state:

1. **Check for HANDOFF.md in current phase directory:**
   - Look for `.cattoolkit/planning/[phase-name]/HANDOFF.md`
   - If found, READ it immediately

2. **Resume from Handoff State:**
   - Review the "In-Progress" section to understand where execution stopped
   - Review the "Next Actions" section to resume from the correct point
   - DO NOT restart completed tasks listed in the handoff
   - Continue execution from the "Next Actions" specifically

3. **Handoff Format Required:**
   When creating HANDOFF.md files, ensure they contain:
   ```markdown
   # Handoff - Phase: [Phase Name]

   ## Completed Tasks
   - [List of tasks already completed]

   ## In-Progress
   - [Current task being worked on, if any]

   ## Next Actions
   - [Specific next steps to resume execution]

   ## Context
   - [Any relevant context for resuming]
   ```

4. **If no HANDOFF.md exists:** Continue with fresh execution as normal.

## 2. Plan Validation

**Validate the injected plan against project-strategy standards:**
- YAML frontmatter exists (phase, type: execute, status)
- Objective section is clear
- Context section lists required reading
- Every task has Scope (optional)/Action/Verify/Done
- Success criteria are measurable

## 3. Strategy Analysis

Analyze each task to identify:

**Sequential Chains:**
- Task A produces a file that Task B consumes
- Task B cannot start until Task A completes

**Parallel Groups:**
- Tasks operate on different files with no shared dependencies
- Can execute simultaneously

**Async/Background Tasks:**
- Long-running tasks (Audit, Test Suite) that block nothing
- Launch with `run_in_background: true`

## 4. Delegation

**MANDATORY:** Delegate to worker subagents with comprehensive context for autonomous execution.

**Format:**
Each `worker` agent receives natural language instructions with:
- **Task:** What needs to be done
- **Context:** Project brief, plan phase, dependencies
- **Requirements:** Key constraints and success criteria
- **Quality Standards:** Reference to `software-engineering` protocols

## 5. Quality Assurance (CRITICAL)

**After ANY subagent reports success, you MUST perform Objective Audit:**

1. **READ the files they modified** - Do NOT trust their report (Read-Back Protocol)
2. **Verify against the Plan's "Verify" criteria**
3. **Update PROJECT STATE** - Update PLAN.md status and ROADMAP.md
4. **Log verification results**

**If verification FAILS:** Respawn the worker with refined instructions (Correction Loop).

## 6. Completion

**When all tasks pass verification:**
1. Update PLAN.md status: `status: complete`
2. Create SUMMARY.md using `project-strategy/assets/templates/summary.md`
