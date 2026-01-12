---
name: planning-with-files
description: "Implements Manus-style 3-file pattern for simple multi-step tasks. PROACTIVELY Use when tracking personal workflow progress with lightweight markdown files. For complex project planning, use manage-planning instead."
---

# Planning with Files: Manus-Style Workflow Automation

Transform your workflow using persistent markdown files as external working memory. This skill implements Manus's proven context engineering principles for reliable AI agent workflows.

## Core Philosophy

**Filesystem = Unlimited Memory**

Instead of stuffing everything into the context window, use files as persistent, structured memory:
- ✅ Store large content in files (notes, research, code)
- ✅ Keep only paths in working context
- ✅ Re-read plans to refresh goals in attention window
- ✅ Track progress with checkboxes and status updates
- ✅ Log errors for recovery and learning

## Quick Start

For ANY complex task (3+ steps):

### 1. Create the Plan FIRST
```bash
Write task_plan.md
```

### 2. Use the 3-File Pattern
```
task_plan.md    → Track phases and progress
notes.md        → Store findings and research
deliverable.md  → Final output
```

### 3. Execute the Loop
```
Loop 1: Create task_plan.md with phases
Loop 2: Research → notes.md → update task_plan.md
Loop 3: Synthesize → deliverable.md → update task_plan.md
Loop 4: Deliver
```

### 4. Read Before Decide
```bash
# Before major decisions:
Read task_plan.md  # Refreshes goals in attention window
```

## The 3-File Pattern

### File 1: task_plan.md
**Purpose:** Track phases, progress, decisions, and errors
**When to Update:** After each phase completion

**See:** `references/task-plan-template.md` for complete template

### File 2: notes.md
**Purpose:** Store research findings, sources, and intermediate work
**When to Update:** During research and information gathering

**See:** `references/notes-template.md` for complete template

### File 3: deliverable.md
**Purpose:** Final output, synthesis, or deliverable
**When to Update:** During synthesis and delivery phases

**See:** `references/deliverable-template.md` for complete template

## Workflow Pattern

### Loop 1: Plan
1. Create `task_plan.md` with phases
2. Define goals and success criteria
3. Identify key questions

### Loop 2: Research
1. Update `task_plan.md` status
2. Gather information → `notes.md`
3. Document sources and findings
4. Update `task_plan.md` with progress

### Loop 3: Synthesize
1. Update `task_plan.md` status
2. Synthesize findings → `deliverable.md`
3. Create final output
4. Update `task_plan.md` completion

### Loop 4: Deliver
1. Review all files
2. Finalize `deliverable.md`
3. Mark task complete in `task_plan.md`

## Use Cases

### Use Case 1: Research Task
**Pattern:** Plan → Research → Synthesize → Deliver
```
task_plan.md    → Research phases
notes.md        → Source findings
deliverable.md  → Research report
```

### Use Case 2: Implementation Task
**Pattern:** Plan → Build → Review → Deliver
```
task_plan.md    → Implementation phases
notes.md        → Technical decisions, code snippets
deliverable.md  → Final code/feature
```

### Use Case 3: Analysis Task
**Pattern:** Plan → Analyze → Synthesize → Deliver
```
task_plan.md    → Analysis framework
notes.md        → Data findings
deliverable.md  → Analysis report
```

## Best Practices

### Do's

✅ **Create task_plan.md FIRST**
- Always start with planning
- Define phases clearly
- Set success criteria

✅ **Update task_plan.md After Each Phase**
- Track progress with checkboxes
- Record decisions made
- Note errors encountered

✅ **Read task_plan.md Before Major Decisions**
- Refresh goals in attention window
- Check current phase status
- Review previous decisions

✅ **Store Sources in notes.md**
- Document all sources
- Include URLs and key points
- Track research progress

✅ **Keep Files Lightweight**
- Store content in files
- Keep paths in context
- Re-read as needed

### Don'ts

❌ **Don't Skip Planning**
- Always create task_plan.md first
- Define phases before execution
- Set clear goals

❌ **Don't Stuff Context Window**
- Use files for large content
- Keep only paths in context
- Re-read when needed

❌ **Don't Forget to Update**
- Update task_plan.md after phases
- Track progress continuously
- Record errors for recovery

❌ **Don't Work Without a Plan**
- Always define phases
- Set success criteria
- Track decisions

## Common Patterns

### Pattern 1: Simple Task (3-5 phases)
```
Phase 1: Plan
Phase 2: Research
Phase 3: Execute
Phase 4: Review
Phase 5: Deliver
```

### Pattern 2: Complex Task (5-10 phases)
```
Phase 1: Plan
Phase 2: Research requirements
Phase 3: Design solution
Phase 4: Implement
Phase 5: Test
Phase 6: Review
Phase 7: Refine
Phase 8: Deliver
```

### Pattern 3: Research Task
```
Phase 1: Plan research
Phase 2: Gather sources
Phase 3: Analyze findings
Phase 4: Synthesize insights
Phase 5: Write report
Phase 6: Review and deliver
```

**See:** `references/workflow-patterns.md` for more patterns

## Integration with Other Skills

### With manage-planning
- Use `manage-planning` for complex project planning
- Use `planning-with-files` for simple task tracking
- Combine for complex multi-phase projects

### With architecture
- Document architectural decisions in task_plan.md
- Store research in notes.md
- Create ADRs as deliverables

## Benefits

- **Reliable Execution** - Plans persist across sessions
- **Context Management** - Filesystem as unlimited memory
- **Progress Tracking** - Clear visibility into status
- **Error Recovery** - Learn from documented mistakes
- **Decision Audit** - Track rationale for choices
- **Knowledge Base** - Build reusable patterns

## Reference Materials

**Core Templates:**
- `references/task-plan-template.md` - Complete task_plan.md template
- `references/notes-template.md` - Complete notes.md template
- `references/deliverable-template.md` - Complete deliverable.md template

**Workflow Guides:**
- `references/workflow-patterns.md` - Common workflow patterns
- `references/progress-tracking.md` - Progress tracking strategies
- `references/error-recovery.md` - Error recovery patterns

**Theoretical Foundations:**
- `references/theoretical-foundations.md` - Manus context engineering research
- `references/examples.md` - Complete worked examples

## Next Steps

1. **Start Planning**
   - Create task_plan.md for next task
   - Define phases and goals
   - Set success criteria

2. **Execute Workflow**
   - Follow 3-file pattern
   - Update progress after each phase
   - Read task_plan.md before decisions

3. **Track Progress**
   - Use checkboxes to track completion
   - Document decisions and errors
   - Maintain clean file structure

4. **Deliver**
   - Synthesize findings
   - Create final deliverable
   - Mark task complete
