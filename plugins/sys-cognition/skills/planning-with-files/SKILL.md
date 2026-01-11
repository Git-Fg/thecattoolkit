---
name: planning-with-files
description: USE when user mentions "create a plan", "organize work", "track progress", "multi-step task", or "research task". Implements Manus-style persistent markdown file planning for context engineering, working memory management, and structured workflow automation. Transforms chaotic tool call sequences into organized, trackable workflows with persistent state.
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

**Template:**
```markdown
# Task Plan: [Task Name]

## Goal
[One sentence describing the desired end state]

## Phases
- [ ] Phase 1: Plan and setup
- [ ] Phase 2: Research/gather information
- [ ] Phase 3: Execute/build
- [ ] Phase 4: Review and deliver

## Key Questions
1. [Question to answer before proceeding]
2. [Another important question]

## Decisions Made
- [Decision]: [Rationale]

## Errors Encountered
- [Timestamp] [Error]: [Resolution]

## Status
**Currently in Phase X** - [What you're doing now]
```

### File 2: notes.md
**Purpose:** Store research findings, sources, and intermediate work
**When to Update:** During research and information gathering

**Template:**
```markdown
# Notes: [Topic]

## Sources

### Source 1: [Name]
- URL: [link]
- Key points:
  - [Finding]
  - [Finding]

## Research Findings

### [Category 1]
- [Finding]
- [Finding]

### [Category 2]
- [Finding]
- [Finding]

## Questions Raised
- [Question]
- [Question]
```

### File 3: [deliverable].md
**Purpose:** Final output or implementation
**When to Update:** At task completion

**Content:** Depends on task type:
- Code changes: List of files and changes
- Research: Synthesized findings
- Analysis: Conclusions and recommendations

## The Workflow Loop

### Loop Structure
```
┌─────────────────────────────────────────┐
│ 1. Read task_plan.md                    │
│    (Refresh goals in attention)         │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 2. Execute phase                        │
│    (Write, Edit, Bash, etc.)           │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 3. Update task_plan.md                  │
│    (Mark [x], update status)            │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 4. Next phase or deliver                │
└─────────────────────────────────────────┘
```

### Loop 1: Plan
```bash
# Create the plan file first (non-negotiable!)
Write task_plan.md

# Template already shown above
# Goal: One sentence
# Phases: 4-6 phases with checkboxes
# Status: "Currently in Phase 1"
```

### Loop 2: Research
```bash
# Always read the plan first
Read task_plan.md

# Gather information
WebSearch "query"
Write notes.md

# Update progress
Edit task_plan.md
  # Mark Phase 2: [x]
  # Update Status: "Currently in Phase 3"
```

### Loop 3: Execute
```bash
# Read plan to refresh goals
Read task_plan.md

# Execute based on plan
Read notes.md
Write deliverable.md

# Update progress
Edit task_plan.md
  # Mark Phase 3: [x]
  # Status: "Currently in Phase 4"
```

### Loop 4: Deliver
```bash
# Final read of plan
Read task_plan.md

# Verify all phases complete
Read deliverable.md

# Task complete!
```

## Critical Rules

### Rule 1: ALWAYS Create Plan First
**Never** start a complex task without `task_plan.md`.

❌ **Wrong:**
```
User: "Research and fix the authentication bug"
Claude: Starts reading code, searching, testing...
[50 tool calls later]
Claude: "I found the issue..."
```

✅ **Correct:**
```
User: "Research and fix the authentication bug"
Claude: Write task_plan.md
  # Define phases
  # Set goal
  # Then proceed
```

### Rule 2: Read Before Decide
Before ANY major decision, read the plan file.

```bash
[Many tool calls have happened...]
[Context is getting long...]
[What was the original goal again?]

→ Read task_plan.md  # This brings goals back!
→ Now make the decision with fresh context
```

This is the **attention manipulation** technique that prevents the "lost in the middle" effect after ~50 tool calls.

### Rule 3: Update After Act
Immediately after completing a phase:
1. Mark checkbox [x]
2. Update Status section
3. Log any errors encountered

```bash
# After completing Phase 2
Edit task_plan.md
  - [x] Phase 2: Research and gather information
  - Status: Currently in Phase 3 - Implementing solution
```

### Rule 4: Store, Don't Stuff
Large outputs → files, not context.

❌ **Wrong:**
```
Claude: "The API documentation says..."
[Stuffing 500 lines into context]
Claude: "Based on all that documentation..."
```

✅ **Correct:**
```
Claude: Write api_research.md
  # Store all findings
Claude: Read api_research.md
  # Reference specific sections as needed
```

### Rule 5: Log All Errors
Every error goes in "Errors Encountered" section.

```markdown
## Errors Encountered
- [2026-01-11] API timeout after 30s → Retried with exponential backoff, succeeded
- [2026-01-11] FileNotFoundError: config.json → Created default config template
```

This builds knowledge for error recovery and helps the model understand what was attempted.

## Context Engineering Principles

Based on Manus's $2B context engineering research:

### Principle 1: Filesystem as External Memory
- Markdown files = unlimited working memory
- Reversible compression (can read files back)
- Structured, searchable information

### Principle 2: Attention Manipulation
- Re-reading plan files refreshes goals in attention window
- Prevents "lost in the middle" effect
- Goals appear recent and salient

### Principle 3: Failure Trace Preservation
- Errors are learning opportunities
- Keep failed attempts in plan
- Model updates understanding when seeing errors

### Principle 4: Stable Prefixes for Cache
- Static content first (plan, templates)
- Append-only updates (don't modify history)
- Consistent structure enables caching

## Advanced Patterns

### Pattern 1: Error Recovery
When something fails:

❌ **Wrong:**
```
Action: Read config.json
Error: File not found
[Silent retry attempts...]
```

✅ **Correct:**
```
Action: Read config.json
Error: File not found

# Update task_plan.md
## Errors Encountered
- config.json not found → Will create default config

Action: Write config.json
Action: Read config.json
Success!
```

### Pattern 2: Decision Checkpointing
Before major decisions:

```bash
# When choosing between approaches
Read task_plan.md  # Refresh goals
Read notes.md      # Review research

# Update plan with decision
Edit task_plan.md
## Decisions Made
- Using approach B over A: Better performance, more maintainable
```

### Pattern 3: Phase Dependencies
Track what needs to be done:

```markdown
## Phases
- [x] Phase 1: Setup ✓
- [x] Phase 2: Research ✓
- [ ] Phase 3: Implementation (CURRENT)
  - [x] Design solution
  - [ ] Write code
  - [ ] Test implementation
- [ ] Phase 4: Review and deliver
```

### Pattern 4: Context Refresh
For very long tasks (>100 tool calls):

```bash
# Every ~30-40 tool calls
Read task_plan.md
Read notes.md
# This refreshes all context in attention window
```

## When to Use This Pattern

### ✅ Use 3-File Pattern For:
- Multi-step tasks (3+ steps)
- Research and analysis tasks
- Building/creating something new
- Tasks spanning multiple tool calls
- Complex debugging workflows
- Feature development
- Documentation projects
- Data analysis projects

### ❌ Skip For:
- Simple questions (one answer)
- Single file edits
- Quick lookups or searches
- Yes/no questions
- Reading a file and summarizing
- Straightforward modifications

## Anti-Patterns to Avoid

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Use TodoWrite for persistence | Create task_plan.md file |
| State goals once and forget | Re-read plan before each decision |
| Hide errors and retry silently | Log errors to plan file |
| Stuff everything in context | Store in files, reference paths |
| Start executing immediately | Create plan file FIRST |
| Rewrite entire plan each time | Use Edit to update checkboxes |
| Keep everything in head | Use files as external memory |

## Integration with Other Skills

This skill works seamlessly with:

- **Deep Analysis**: Store findings in notes.md
- **Prompt Engineering**: Save prompt iterations
- **Context Engineering**: Manage working memory
- **Thinking Frameworks**: Structure analysis

## Example: Complete Workflow

**User Request:** "Research microservices architecture patterns and create a implementation guide"

### Phase 1: Create Plan
```bash
Write task_plan.md
```

**task_plan.md:**
```markdown
# Task Plan: Microservices Architecture Guide

## Goal
Create comprehensive implementation guide for microservices architecture patterns

## Phases
- [x] Phase 1: Create plan ✓
- [ ] Phase 2: Research microservices patterns
- [ ] Phase 3: Analyze best practices
- [ ] Phase 4: Create implementation guide
- [ ] Phase 5: Review and finalize

## Key Questions
1. What are the core microservices patterns?
2. How to handle inter-service communication?
3. What are common anti-patterns to avoid?
4. How to structure data in microservices?

## Status
**Currently in Phase 1** - Plan created, ready to research
```

### Phase 2: Research
```bash
Read task_plan.md
WebSearch "microservices architecture patterns 2025"
WebSearch "microservices best practices"
Write notes.md
Edit task_plan.md
```

**notes.md:**
```markdown
# Notes: Microservices Architecture

## Sources

### Source 1: Martin Fowler on Microservices
- URL: https://martinfowler.com/articles/microservices.html
- Key points:
  - Independent deployability
  - Decentralized governance
  - Failure isolation
  - Infrastructure automation

### Source 2: Netflix Microservices
- URL: https://netflixtechblog.com
- Key points:
  - API Gateway pattern
  - Circuit breakers
  - Centralized logging
  - Service mesh
```

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create plan ✓
- [x] Phase 2: Research microservices patterns ✓
- [ ] Phase 3: Analyze best practices
- [ ] Phase 4: Create implementation guide
- [ ] Phase 5: Review and finalize

## Errors Encountered
- None so far

## Status
**Currently in Phase 3** - Analyzing research findings
```

### Phase 3: Synthesize
```bash
Read task_plan.md
Read notes.md
Write microservices_implementation_guide.md
Edit task_plan.md
```

### Phase 4: Deliver
```bash
Read task_plan.md
Read microservices_implementation_guide.md
Deliver microservices_implementation_guide.md
```

## Benefits of This Approach

### For You (User):
- ✅ Never lose track of goals
- ✅ See progress at a glance
- ✅ Recover from interruptions easily
- ✅ Reference decisions made
- ✅ Learn from errors logged

### For Claude (AI):
- ✅ Unlimited working memory
- ✅ Persistent context across interruptions
- ✅ Structured information retrieval
- ✅ Reduced context window pressure
- ✅ Better decision-making with refreshed goals

## Troubleshooting

### "I forgot what I was working on"
```bash
Read task_plan.md
# Goals refreshed!
```

### "I'm stuck in an error loop"
```bash
Edit task_plan.md
## Errors Encountered
- [Previous errors logged here]
- [Current issue]
```

### "Which phase am I in?"
```bash
Read task_plan.md
# Check Status section
```

### "What decisions did I make?"
```bash
Read task_plan.md
# Check "Decisions Made" section
```

## Quick Reference

### Essential Commands
```bash
# Start any complex task
Write task_plan.md

# Before major decisions
Read task_plan.md

# After completing work
Edit task_plan.md

# Store research/findings
Write notes.md

# Deliver final output
Write deliverable.md
```

### File Checklist
- [ ] task_plan.md exists
- [ ] Goal clearly defined
- [ ] Phases outlined
- [ ] Status updated
- [ ] Errors logged
- [ ] Progress tracked

## Advanced Techniques

### Parallel Research
```bash
# In notes.md, track multiple research streams
## Stream 1: Service Discovery
## Stream 2: Data Management
## Stream 3: Communication Patterns
```

### Complex Dependencies
```markdown
## Phases
- [ ] Phase 1: Setup
  - [x] Create repository
  - [x] Setup CI/CD
  - [ ] Configure database
- [ ] Phase 2: Core Services
  - [ ] Service A
  - [ ] Service B
  - [ ] Service C
```

### Knowledge Accumulation
```markdown
## Decisions Made
- 2026-01-11: Chose REST over GraphQL (simpler, better tooling)
- 2026-01-11: PostgreSQL for all services (consistency)
- 2026-01-11: Docker Compose for local dev (simplicity)
```

## Conclusion

Planning with Files transforms chaotic AI workflows into organized, trackable, recoverable processes. By treating the filesystem as unlimited memory and using the 3-file pattern, you gain:

- **Reliability**: Never lose track of goals
- **Persistence**: Work survives interruptions
- **Clarity**: See progress at a glance
- **Learning**: Errors become knowledge

Start with every complex task by writing `task_plan.md`. It's the foundation of all else.
