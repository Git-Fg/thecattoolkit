# Workflow: Initialize Context Structure

## Understanding Context Initialization

When starting a new project or beginning work that requires persistent state tracking, you need to establish a foundation for managing context independent of the LLM's context window. This workflow provides the knowledge and patterns for setting up this foundation.

## When This Applies

Use context initialization when:
- Beginning a complex, multi-step project
- Starting work that may span multiple sessions
- Needing to track decisions and state over time
- Working on tasks where context preservation matters

## The Context Directory Concept

**Purpose**: `.cattoolkit/context/` serves as persistent memory outside the LLM's context window.

**Why it matters**:
- Context windows are limited (typically 8K-200K tokens)
- Sessions can be interrupted or lost
- Complex work requires tracking state over time
- Decisions made early impact later work

## Core Files Knowledge

### scratchpad.md - The Living Document
**What it is**: Your real-time thinking and decision tracker
**Contains**: Current context, decisions, errors, progress, questions
**When to use**: Throughout your work session
**Knowledge**: Think of it as your working whiteboard that persists

### todos.md - Task State Tracker
**What it is**: Persistent task list across sessions
**Contains**: Active, in-progress, completed, blocked tasks
**When to use**: When tasks change state
**Knowledge**: Separates tasks from thinking - todos are actionable, scratchpad is context


### context.log - Historical Timeline
**What it is**: Session history and event tracking
**Contains**: Timestamps, key events, decisions, file changes
**When to use**: End of session or major milestones
**Knowledge**: Creates narrative of your work journey

### handoff.md - Session Transition Tool
**What it is**: Bridge for tool/session switching
**Contains**: Completed work, current state, next steps, critical context
**When to use**: Before session end, tool switching, or delegation
**Knowledge**: Enables seamless continuation with full context

## Setting Up the Structure

**Directory creation**:
- Base: `.cattoolkit/context/`
- Subdirectory: `.cattoolkit/context/checkpoints/`

**File creation**:
Each file has a purpose-built template (see templates/ directory)

**Checkpoint creation**:
Initial checkpoint captures your starting state for recovery

## Knowledge Patterns

### Pattern 1: Initialization Choices
- **New project**: Full initialization with all files
- **Existing project**: Check if structure exists, initialize if missing
- **Re-initialization**: Backup existing, initialize fresh, merge if needed

### Pattern 2: Template Customization
Templates provide structure, you provide context:
- Fill in project-specific details
- Adapt sections to your workflow
- Maintain consistency across files
- Keep templates as reference

### Pattern 3: State Awareness
Think in states:
- **Initialization**: Starting point
- **Active**: Work in progress
- **Checkpoint**: Milestone snapshot
- **Handoff**: Transition state
- **Recovery**: Restoring from checkpoint

## Workflow Templates

The templates/ directory contains:
- `scratchpad.md` - Structured thinking template
- `handoff.md` - Session transition template
- `context-log.md` - Timeline tracking template
- `checkpoint.md` - Snapshot template

## Decision Framework

**Should you initialize?**
- If work is complex AND spans time → Yes
- If work is simple AND quick → No
- If uncertain → Yes (can always skip using)

**What to initialize?**
- Always: scratchpad.md, todos.md
- If long-running: context.log
- If switching tools: handoff.md

## Integration Knowledge

**With Planning Skills**:
- Scratchpad links to builder's `PLAN.md` in `.cattoolkit/planning/`
- Checkpoints mark phase transitions
- Handoff preserves planning context

**With Engineering Skills**:
- Scratchpad tracks debugging decisions
- Errors logged for pattern recognition
- Checkpoints before risky changes

**With Thinking Skills**:
- Scratchpad records strategic thinking
- Decisions documented with rationale
- Questions tracked for later research

## Common Patterns

### Pattern 1: Clean Start
Initialize fresh for new project:
1. Create directory structure
2. Initialize all core files
3. Create initial checkpoint
4. Begin work with tracking

### Pattern 2: Mid-Project Start
Initialize when starting to track in existing project:
1. Check existing structure
2. Initialize missing files
3. Document current state
4. Begin tracking

### Pattern 3: Recovery
Re-initialize after corruption or loss:
1. Backup any salvageable data
2. Re-initialize structure
3. Restore from checkpoints
4. Continue with full context

## Usage Guidelines

### After Initialization
1. **Start tracking immediately** - Begin updating scratchpad.md with first decisions
2. **Monitor context usage** - Check percentage and update accordingly
3. **Use templates** - Fill in template sections as work progresses
4. **Create checkpoints** - Before major changes or at milestones

### Best Practices
- Update scratchpad.md throughout session
- Log significant events in context.log
- Keep todos.md current
- Review handoff.md before session end

### Context Window Monitoring
- **60% Warning** → Intensify context tracking
- **70% Critical** → Create checkpoint
- **80% Overflow** → Prepare handoff

## Integration

### With Other Skills
- **manage-planning**: Reference builder's `PLAN.md` for current phase
- **engineering**: Update scratchpad.md with debugging decisions
- **thinking-frameworks**: Log strategic thinking in scratchpad.md
- **git-workflow**: Link commits to checkpoints

### File References
When referring to context files in other workflows:
```
@ .cattoolkit/context/scratchpad.md
@ .cattoolkit/context/todos.md
```

## Knowledge Check

After initialization, you should understand:
- [ ] What each file in `.cattoolkit/context/` is for
- [ ] When to use scratchpad.md vs todos.md
- [ ] Why checkpoints matter for recovery
- [ ] How context integrates with other skills

## Next Steps

After initialization:
- Review the templates in `templates/` directory
- Begin working with context tracking
- Use the "Update Scratchpad" workflow for ongoing tracking
- Create checkpoints at important milestones

Your context foundation is ready. Think of it as establishing persistent memory for your work.
