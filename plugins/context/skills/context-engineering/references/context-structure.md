# Context Structure Reference

## The .cattoolkit/context/ Directory

### Purpose
Persistent session state management independent of LLM context window. Enables continuity across sessions, tools, and interruptions.

### Why Persistent Context vs Ephemeral Context

**Ephemeral Context (In-Conversation Only):**
- ❌ Lost when session ends
- ❌ No continuity across tools
- ❌ Must rebuild context each time
- ❌ Context window limits apply
- ❌ Cannot track long-term decisions

**Persistent Context (File-Based):**
- ✅ Survives session boundaries
- ✅ Works across all tools
- ✅ Quick context recovery
- ✅ Scales beyond context window
- ✅ Preserves decision history

## Directory Structure

```
.cattoolkit/context/
├── scratchpad.md          # Current thinking and decisions
├── todos.md              # Persistent task tracking
├── context.log           # Session context history
├── handoff.md            # Session handoff summary
└── checkpoints/          # Critical state snapshots
    ├── YYYY-MM-DD-feature-start.md
    ├── YYYY-MM-DD-implementation-complete.md
    └── YYYY-MM-DD-testing-phase.md
```

### Core Files

#### scratchpad.md
**Purpose**: Real-time thinking, decisions, and context tracking

**Contents**:
- Current Session Context
- Technical Decisions
- Recent Changes
- Open Questions
- TODO Items

**Update Frequency**: Throughout session as work progresses

**Example Structure**:
```markdown
# Project Scratchpad

## Current Session Context
- **Active Task:** Feature implementation
- **Current Phase:** Backend API development
- **Next Step:** Database schema design

## Technical Decisions
- **Framework:** Express.js + TypeScript
- **Database:** PostgreSQL with Prisma ORM
- **Authentication:** JWT-based

## Recent Changes
- 2026-01-05: Added user authentication module
- 2026-01-05: Implemented database connection pool

## Open Questions
- How to handle password reset flow?
- What email service to use for notifications?

## TODO Items
- [ ] Design user registration endpoint
- [ ] Implement password validation
- [ ] Add unit tests for auth module
```

#### todos.md
**Purpose**: Persistent task tracking across sessions

**Contents**:
- Current tasks with status
- Completed items (keep for history)
- Blocked items with reason
- Next actions

**Update Frequency**: When tasks change state


#### context.log
**Purpose**: Session history and timeline

**Contents**:
- Session start/end timestamps
- Key events
- Decisions made
- Files modified

**Update Frequency**: End of session or major milestones

#### handoff.md
**Purpose**: Session handoff summary

**Contents**:
- Completed work
- Current state
- Next steps
- Critical context
- Files to review

**Update Frequency**: Before session rotation

### Checkpoints Directory

**Purpose**: Critical state snapshots before major changes

**Naming Convention**: `YYYY-MM-DD-description.md`

**Contents**:
```markdown
# Checkpoint: YYYY-MM-DD

## Current State
- Task: What you're working on
- Progress: Percentage/phase
- Files: List modified files

## Important Context
- Decisions made: List
- Rationale: Why these decisions
- Assumptions: What you're assuming

## Next Actions
- [ ] Action 1
- [ ] Action 2

## Rollback Plan
If things go wrong:
1. Rollback step 1
2. Rollback step 2
```

## Context Management Workflows

### 1. Initialization
```bash
# Create directory structure
mkdir -p .cattoolkit/context/checkpoints

# Initialize core files
touch .cattoolkit/context/scratchpad.md
touch .cattoolkit/context/todos.md
touch .cattoolkit/context/context.log
touch .cattoolkit/context/handoff.md
```

### 2. Real-Time Updates
```bash
# Update scratchpad with decisions
echo "## Decision: Chose PostgreSQL over MongoDB" >> .cattoolkit/context/scratchpad.md

# Update todos with progress
echo "- [x] Task completed" >> .cattoolkit/context/todos.md

# Log context changes
echo "2026-01-05 14:30: Session started" >> .cattoolkit/context/context.log
```

### 3. Context Monitoring
Track context window usage:
- At 60%: Start tracking more aggressively
- At 70%: Create checkpoint
- At 80%: Prepare for handoff

### 4. Session Handoff
Generate handoff summary by creating `.cattoolkit/context/handoff.md` with:

```
# Session Handoff: YYYY-MM-DD

## Completed Work
- [ ] Task 1
- [ ] Task 2

## Current State
- Working on: current task
- Context: important context to preserve
- Files modified: list

## Next Steps
1. Next action
2. Follow-up action

## Critical Context
- Important decisions
- Architectural choices
- Known issues

## Files to Review
- File 1 - Why important
- File 2 - Why important
```

## Best Practices

### When to Update Context

**High Priority (Always Update)**:
- Major decisions made
- Architecture changes
- Errors encountered and resolved
- Progress milestones
- Context window reaching 60%

**Medium Priority (Update When Relevant)**:
- Minor code changes
- Incremental progress
- Research findings
- Tool switches

**Low Priority (Update Periodically)**:
- Session summaries
- General notes
- Backlog items

### Context Quality

**Good Context**:
- Actionable information
- Current and relevant
- Preserves decisions and rationale
- Clear next steps
- Organized structure

**Poor Context**:
- Outdated information
- Irrelevant details
- Missing rationale
- Unclear next steps
- Disorganized

### Context Health Checks

Before session handoff, verify:

- [ ] All major decisions documented
- [ ] Current state clearly described
- [ ] Next steps identified
- [ ] Critical files listed
- [ ] Open questions noted
- [ ] Checkpoint created if needed

## Integration Examples

### With Planning
Project plans are managed via the **planner** plugin in `.cattoolkit/planning/`. Session-level context in `scratchpad.md` should complement these plans.

### With Engineering
```markdown
# In debugging session
Update .cattoolkit/context/scratchpad.md with:
- Error discovered
- Hypothesis tested
- Resolution approach
- Prevention measures
```

### With Git Workflow
```markdown
# In git-workflow
Reference .cattoolkit/context/checkpoints/ for:
- Pre-change state
- Rollback plan
- Change rationale
```

## Common Patterns

### Pattern 1: Feature Development
1. Initialize context structure
2. Brainstorm in scratchpad.md
3. Create implementation plan
4. Track progress in todos.md
5. Monitor context usage
6. Create checkpoint before implementation
7. Execute with context tracking
8. Generate handoff summary
9. Continue in new session if needed

### Pattern 2: Bug Fix Investigation
1. Initialize context structure
2. Document bug in scratchpad.md
3. Track investigation in context.log
4. Create hypothesis in scratchpad.md
5. Test hypothesis, log results
6. Document root cause
7. Create fix plan
8. Implement with context tracking
9. Verify fix, create checkpoint

### Pattern 3: Multi-Project Management
1. Create project-specific context structure
2. Track project progress separately
3. Use scratchpad.md for cross-project insights
4. Create checkpoints before project switches
5. Generate handoff summaries for each project

## Tool Switching

When switching between Claude Code, Cursor, Codex:

1. **Generate handoff** in current tool
2. **Preserve context** in .cattoolkit/context/ directory
3. **Import context** in new tool
4. **Continue work** with full context

**Context portability**:
- Keep all context in .cattoolkit/context/
- Use standard templates
- Document assumptions
- Preserve decision history

## Troubleshooting

### Lost Context Recovery

If context is lost:

1. Check .cattoolkit/context/ for scratchpad files
2. Review git history for recent changes
3. Examine filesystem for modified files
4. Request context reconstruction from user

### Stale Context

If context appears outdated:

1. Verify timestamps in context files
2. Check for recent git commits
3. Review active files
4. Update context with current state

### Context Bloat

If context grows too large:

1. Archive old checkpoints
2. Summarize completed work
3. Remove irrelevant details
4. Focus on actionable context

## Advanced Patterns

### Context Compression
When context is full:
1. Identify non-critical context
2. Archive to checkpoint
3. Preserve critical decisions
4. Summarize remaining context

### Parallel Context
For parallel workstreams:
1. Create separate context directories
2. Track each workstream independently
3. Use master context for coordination
4. Merge contexts when workstreams converge

### Context Sharing
For team contexts:
1. Generate tool-agnostic handoff
2. Preserve context in shared files
3. Use consistent context structure
4. Enable quick context recovery
