# Session Management Reference

Persistent session state management via the Passive Hook System.

## Directory Structure

```
.cattoolkit/
├── context/
│   ├── scratchpad.md     # Current thinking and decisions
│   ├── todos.md          # Persistent task tracking
│   ├── context.log       # Session context history
│   ├── handoff.md        # Session handoff summary
│   └── checkpoints/      # Critical state snapshots
└── planning/             # Managed by planning skills
```

## Scratchpad Hygiene

**CRITICAL:** Only update scratchpad for:
- Critical decisions made
- Errors encountered
- Phase changes
- Progress milestones

**NEVER update for:** Trivial file reads (prevents context churn)

## Hybrid Hook Architecture

**Command Hooks (Deterministic, Fast):**

| Hook | Trigger | Action |
|:-----|:--------|:-------|
| SessionStart | Session begins | Auto-load plan + scratchpad |
| PostToolUse | After Edit/Write/Bash | Auto-log state changes |
| PreCompact | Context near overflow | Create checkpoint |

**Deterministic Script Hooks:**

| Hook | Trigger | Action |
|:-----|:--------|:-------|
| Stop | Session stopping | Evaluate safe exit |
| SubagentStop | Agent stops | Verify completion |

## Context Window Thresholds

| Level | Action |
|-------|--------|
| 60% Warning | Begin context tracking |
| 70% Critical | Create checkpoint + handoff |
| 80% Overflow | Force session rotation |

## Progressive Disclosure Levels

| Level | Tokens | Content |
|-------|--------|---------|
| 1 | 500 | Immediate: current task, active files, next action |
| 2 | 2,000 | Task: requirements, approach, related files |
| 3 | 3,000 | Project: overview, decisions, conventions |
| 4 | On-demand | Reference: detailed docs, examples |

## Context Health Metrics

| Metric | Description |
|--------|-------------|
| Token Efficiency | Actionable context percentage |
| Information Density | Relevant info per token |
| Context Relevance | Context used in responses |
| Update Frequency | How often context refreshed |

## Handoff Protocol

When creating session handoff:

1. **Completed Work**: List finished tasks
2. **Current State**: Files modified, pending changes
3. **Next Steps**: Clear prioritized actions
4. **Critical Context**: Key decisions, blockers
5. **File Summary**: Important file locations

## Templates

**Scratchpad Template:**
```markdown
# Scratchpad

## Current Session
- Task: [description]
- Phase: [planning/implementing/testing]

## Decisions Made
- [Decision]: [Rationale]

## Open Questions
- [ ] [Question]

## Recent Progress
- [Progress item]
```

**Handoff Template:**
```markdown
# Session Handoff

## Completed
- [Task completed]

## Current State
- Working on: [task]
- Files modified: [files]

## Next Steps
1. [Priority action]

## Context
- Key decision: [decision]
- Blocker: [if any]
```
