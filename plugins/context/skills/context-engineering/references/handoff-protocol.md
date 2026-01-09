# Workflow: Create Handoff Document

## Purpose
Generate comprehensive handoff document preserving critical context for session rotation, tool switching, or delegation.

## When to Use
- Context window >70% (critical threshold)
- End of work session
- Switching between tools (Claude Code ↔ Cursor ↔ Codex)
- Delegating work to another session
- Taking extended break
- Before critical implementation phase

## Required Reading
1. `references/context-structure.md` - Session handoff best practices
2. `templates/handoff.md` - Handoff document template

## Pre-requisites
- Context structure initialized
- Work session with tracking enabled
- Session summary created (run `summarize-session` first recommended)

## Step 1: Create Final Checkpoint

### 1a: Create Checkpoint Before Handoff

Create checkpoint file `.cattoolkit/context/checkpoints/{YYYY-MM-DD}-handoff-prep.md` with the following content:

```
# Checkpoint: {YYYY-MM-DD} - Pre-Handoff State

## Current State
- Task: {active-task-from-scratchpad}
- Phase: {current-phase-from-scratchpad}
- Progress: {current-percentage}%
- Session Duration: {duration}

## Critical Context
{technical-decisions-from-scratchpad}

## Open Items
{open-questions-from-scratchpad}

## Next Actions
{next-steps-from-todos}

## Files Modified
{files-modified-during-session}

## Handoff Reason
{reason-for-handoff}

---
*Checkpoint created before handoff*
```

### 1b: Update Context Log

Append to `.cattoolkit/context/context.log`:

```
### {YYYY-MM-DD HH:MM} - Pre-Handoff Checkpoint
- Checkpoint: checkpoints/{YYYY-MM-DD}-handoff-prep.md
- Reason: {handoff-reason}
- Context Usage: {percentage}%
- Next Session: {target-session}
```

## Step 2: Compile Handoff Document

### 2a: Gather Context Data

Extract key information from context files:

- **Handoff Date**: Current timestamp
- **Start Time**: From context.log session start
- **Current Task**: From scratchpad.md
- **Current Phase**: From scratchpad.md
- **Recent Decisions**: Last 3-4 decisions from scratchpad.md
- **Open Questions**: From scratchpad.md
- **Completed Todos**: From todos.md
- **Next Steps**: From todos or scratchpad.md

### 2b: Generate Comprehensive Handoff

Create `.cattoolkit/context/handoff.md` using the handoff template from `templates/handoff.md`.

Populate with the following sections:

**Executive Summary:**
- Project overview and current phase
- Session overview and work completed
- Handoff reason

**Completed Work:**
- Major milestones achieved
- Technical decisions made
- Files modified

**Current State:**
- Active context (task, phase, files)
- Recent changes and progress
- Errors resolved

**Critical Context:**
- Technical architecture
- Key decisions with rationale
- Assumptions and constraints

**Open Items:**
- Open questions
- Blocked tasks
- Known issues

**Next Steps:**
- Immediate actions for next session
- Short-term goals
- Medium-term milestones

**Implementation Details:**
- Code changes summary
- Configuration changes
- Dependencies (external and internal)
- Database changes
- API changes

**Tool-Specific Instructions:**
- For Claude Code
- For Cursor
- For other tools

**Quality Assurance:**
- Testing status
- Documentation status
- Security review

**Rollback Plan:**
- Emergency rollback steps
- Restore points
- Recovery checklist

**Success Criteria:**
- For next session
- For current phase
- For project completion

**Files to Review:**
- High priority files
- Medium priority files
- Reference files

**Context Files Reference:**
- Complete context files list
- Checkpoints
- Quick recovery guide

**Session Metrics:**
- Duration and activity counts
- Context health metrics
- Recommendations

## Step 3: Create Tool-Specific Handoffs

### 3a: Claude Code Handoff

Create `.cattoolkit/context/handoff-claude.md`:

```
# Handoff for Claude Code

## Quick Start
1. Read .cattoolkit/context/handoff.md for complete context
2. Review .cattoolkit/context/scratchpad.md for decisions
3. Check .cattoolkit/context/todos.md for current tasks

## Claude-Specific Instructions
{claude-specific-setup-instructions}

## Available Skills
- engineering: For debugging and code review
- context-engineering: For continuing context tracking
- manage-planning: For plan execution

## Commands to Use
- /thecattoolkit:debug - Continue debugging
- /thecattoolkit:review - Code review
- /run-plan - Execute existing plan

## Context Recovery
1. Check .cattoolkit/context/handoff.md
2. Run: ls -la .cattoolkit/context/
3. Review scratchpad.md recent entries
```

### 3b: Cursor Handoff

Create `.cattoolkit/context/handoff-cursor.md`:

```
# Handoff for Cursor

## Quick Start
1. Open project in Cursor
2. Read .cattoolkit/context/handoff.md for context
3. Review .cattoolkit/context/scratchpad.md for decisions

## Cursor-Specific Instructions
{cursor-specific-setup-instructions}

## AI Context
Share .cattoolkit/context/ files with Cursor AI for context

## Files to Focus On
{focus-files}

## Next Steps
{next-steps-for-cursor}
```

## Step 4: Validate Handoff Quality

### 4a: Handoff Checklist

**Completeness:**
- [ ] Handoff document created
- [ ] Checkpoint created
- [ ] Tool handoffs created (optional)

**Content Quality:**
- [ ] Comprehensive (>50 lines)
- [ ] Next steps identified
- [ ] Decisions documented
- [ ] Questions noted

**Files:**
- [ ] Scratchpad available
- [ ] Todos available

### 4b: Generate Handoff Summary

Create `.cattoolkit/context/handoff-summary.txt`:

```
HANDOFF SUMMARY
===============

Date: {YYYY-MM-DD HH:MM}
Reason: {handoff-reason}
Context Usage: {percentage}%

Files Created:
- handoff.md (main handoff)
- handoff-claude.md (Claude-specific)
- handoff-cursor.md (Cursor-specific)
- checkpoints/{YYYY-MM-DD}-handoff-prep.md (snapshot)

Next Session Should:
1. Read .cattoolkit/context/handoff.md
2. Review .cattoolkit/context/scratchpad.md
3. Continue with next steps

Estimated Time to Context Recovery: 5-10 minutes
```

## Step 5: Archive Context (Optional)

### 5a: Create Session Archive

Create compressed archive: `.cattoolkit/context/archives/session-{YYYYMMDD-HHMM}.tar.gz`

Include:
- scratchpad.md
- todos.md
- context.log
- handoff.md

### 5b: Clean Context Files

Create fresh scratchpad with current state from handoff.md:

```
# Project Scratchpad

## Current Session Context
- **Project:** {project-name}
- **Active Task:** {from-handoff}
- **Current Phase:** {from-handoff}
- **Continued From:** Session {YYYY-MM-DD HH:MM}
- **Context Window:** Fresh session

## Critical Context (from previous session)
{link-to-handoff}

## New Decisions
_Record new decisions here_

## Next Steps
_Continue from handoff.md next steps_

---
*Continued from previous session handoff*
```

## Step 6: Final Steps

### 6a: Update Context Log

Append to `.cattoolkit/context/context.log`:

```
### {YYYY-MM-DD HH:MM} - Handoff Complete
- Main handoff: handoff.md
- Checkpoint: checkpoints/{YYYY-MM-DD}-handoff-prep.md
- Tool handoffs: handoff-*.md
- Session archived: session-{YYYYMMDD-HHMM}.tar.gz
- Next session: {target-tool}
- Recovery time: ~5-10 minutes
```

### 6b: Display Handoff Status

Display the following status:

```
=========================================
HANDOFF COMPLETE
=========================================

Primary Handoff Document:
  📄 .cattoolkit/context/handoff.md

Tool-Specific Handoffs:
  📄 .cattoolkit/context/handoff-claude.md
  📄 .cattoolkit/context/handoff-cursor.md

Checkpoint:
  📸 .cattoolkit/context/checkpoints/{YYYY-MM-DD}-handoff-prep.md

Archive:
  📦 .cattoolkit/context/archives/session-{YYYYMMDD-HHMM}.tar.gz

Recovery Instructions:
  1. New session starts with .cattoolkit/context/handoff.md
  2. Review scratchpad.md for quick context
  3. Continue with next steps from handoff

Context preserved for seamless continuation.
=========================================
```

## Handoff Quality Checklist

### Must Have
- [ ] Current task and phase documented
- [ ] Major technical decisions recorded
- [ ] Open questions identified
- [ ] Next steps clearly stated
- [ ] Files to review listed
- [ ] Checkpoint created

### Should Have
- [ ] Tool-specific instructions
- [ ] Rollback plan
- [ ] Success criteria
- [ ] Session metrics
- [ ] Recommendations

### Nice to Have
- [ ] Session archive
- [ ] Clean context for next session
- [ ] Multiple tool handoffs
- [ ] Integration notes

## Best Practices

### Before Handoff
1. Complete session summary
2. Update all context files
3. Create checkpoint
4. Review checklist
5. Generate comprehensive handoff

### During Handoff
1. Preserve critical context
2. Document decisions and rationale
3. Clear next steps
4. Tool-specific guidance
5. Recovery procedures

### After Handoff
1. Archive session
2. Clean context (optional)
3. Update log
4. Provide recovery instructions
5. Ensure continuity

## Troubleshooting

### Incomplete Handoff
Review handoff.md for any TODO markers or incomplete sections.

### Missing Checkpoint
Create checkpoint immediately with critical state snapshot.

### Tool-Specific Issues
Generate missing handoff by copying main handoff and adapting for specific tool.

## Integration

### With Session Summary
Summarize → Checkpoint → Handoff

### With Checkpoint System
Pre-handoff checkpoint → Handoff → Archive

### With Context Management
Handoff preserves context → Next session recovers

## Next Session Recovery

1. **Read handoff.md** - Full context
2. **Review scratchpad.md** - Quick reference
3. **Check todos.md** - Current tasks
4. **Examine checkpoint** - Pre-handoff state
5. **Continue work** - With full context

Handoff document created. Context preserved for seamless continuation.
