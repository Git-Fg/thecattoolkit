---
name: create-plans
description: MUST USE when planning projects, phases, or tasks that an AI agent will execute. Secondary: organizing complex work, creating roadmaps, structuring multi-step implementations, or planning agent-executable workflows.
---

# Essential Principles

## Meta Instructions

These are instructions for how plans should be structured to ensure subagents can execute them successfully:

### Context Management Rule

**Subagents are like new hires who started 5 seconds ago. They know NOTHING about the project, context, or what happened before.**

When creating PLAN.md files that will be executed by subagents:

1. **Every task MUST explicitly list required files:**
   - Don't just say "update the database" - say "update `src/database/schema.ts`"
   - Don't assume the subagent knows where files are - provide paths
   - Include configuration files needed (tsconfig.json, package.json, etc.)

2. **Every plan MUST be self-contained:**
   - The plan should contain ALL the context the subagent needs
   - Use `@file` references explicitly: "Read @src/database/schema.ts before modifying"
   - Include the "why" not just the "what" - subagents need to understand intent

3. **Context is NOT inherited:**
   - Subagents don't have access to conversation history
   - Subagents don't know about decisions made earlier
   - Subagents don't know the project vision unless told explicitly

**Rationale:** Without explicit context in the plan, subagents will:
- Make wrong assumptions about file locations
- Miss critical architectural constraints
- Duplicate existing work
- Break established patterns

## Solo Developer Plus Claude

You are planning for ONE person (the user) and ONE implementer (Claude).
No teams. No stakeholders. No ceremonies. No coordination overhead.
The user is the visionary/product owner. Claude is the builder.

## Plans Are Prompts

PLAN.md is not a document that gets transformed into a prompt.
PLAN.md IS the prompt. It MUST use strict Markdown structure to be machine-readable.

**Required Structure:**
1. `# Objective` - The single clear goal
2. `## Execution Context` - Critical files to read *before* starting
3. `## Tasks` - The step-by-step instructions with explicit file references
4. `## Success Criteria` - Measurable definitions of done

**Example Plan:**
```markdown
# Objective
Implement JWT Authentication

## Execution Context
Before starting, read these files to understand the project:
- .prompts/planning/BRIEF.md
- .prompts/planning/ROADMAP.md
- package.json
- tsconfig.json

## Tasks
- [ ] Install `jsonwebtoken` package: `bun add jsonwebtoken`
- [ ] Create `src/utils/auth.ts` with JWT generation functions
  - Reference: Read @src/utils/logger.ts to understand logging patterns
  - Reference: Read @src/types/user.ts to understand User interface
- [ ] Add authentication endpoint to `src/api/routes.ts`
  - Read the existing file first to understand route structure
- [ ] **[CHECKPOINT:human-verify]** Verify token generation works: run `node test-token.js`

## Success Criteria
- JWT tokens can be generated and verified
- Authentication endpoint accepts credentials and returns tokens
- Tokens include user ID and expiration
```

**Critical Requirements:**
- Use Markdown headers (`#`, `##`) not XML tags
- Every task MUST explicitly list files to read or modify
- Use `@file` references to indicate required reading
- Include configuration files in Execution Context
- Make the plan self-contained - subagents won't have conversation history

When planning a phase, you are writing the prompt that will execute it.

## Scope Control

Plans must complete within ~50% of context usage to maintain consistent quality.

**The quality degradation curve:**
- 0-30% context: Peak quality (comprehensive, thorough, no anxiety)
- 30-50% context: Good quality (engaged, manageable pressure)
- 50-70% context: Degrading quality (efficiency mode, compression)
- 70%+ context: Poor quality (self-lobotomization, rushed work)

**Critical insight:** Claude doesn't degrade at 80% - it degrades at ~40-50% when it sees context mounting and enters "completion mode." By 80%, quality has already crashed.

**Solution:** Aggressive atomicity - split phases into many small, focused plans.

Examples:
- `01-01-PLAN.md` - Phase 1, Plan 1 (2-3 tasks: database schema only)
- `01-02-PLAN.md` - Phase 1, Plan 2 (2-3 tasks: database client setup)
- `01-03-PLAN.md` - Phase 1, Plan 3 (2-3 tasks: API routes)
- `01-04-PLAN.md` - Phase 1, Plan 4 (2-3 tasks: UI components)

Each plan is independently executable, verifiable, and scoped to **2-3 tasks maximum**.

**Atomic task principle:** Better to have 10 small, high-quality plans than 3 large, degraded plans. Each commit should be surgical, focused, and maintainable.

**Autonomous execution:** Plans without checkpoints execute via subagent with fresh context - impossible to degrade.

See: references/scope-estimation.md

## Human Checkpoints

**Claude automates everything that has a CLI or API.** Checkpoints are for verification and decisions, not manual work.

**Checkpoint types:**
- `checkpoint:human-verify` - Human confirms Claude's automated work (visual checks, UI verification)
- `checkpoint:decision` - Human makes implementation choice (auth provider, architecture)

**Rarely needed:** `checkpoint:human-action` - Only for actions with no CLI/API (email verification links, account approvals requiring web login with 2FA)

**Critical rule:** If Claude CAN do it via CLI/API/tool, Claude MUST do it. Never ask human to:
- Deploy to Vercel/Railway/Fly (use CLI)
- Create Stripe webhooks (use CLI/API)
- Run builds/tests (use Bash)
- Write .env files (use Write tool)
- Create database resources (use provider CLI)

**Protocol:** Claude automates work → reaches checkpoint:human-verify → presents what was done → waits for confirmation → resumes

See: references/checkpoints.md, references/cli-automation.md

## Deviation Rules

Plans are guides, not straitjackets. Real development always involves discoveries.

**During execution, deviations are handled automatically via 5 embedded rules:**

1. **Auto-fix bugs** - Broken behavior → fix immediately, document in Summary
2. **Auto-add missing critical** - Security/correctness gaps → add immediately, document
3. **Auto-fix blockers** - Can't proceed → fix immediately, document
4. **Ask about architectural** - Major structural changes → stop and ask user
5. **Log enhancements** - Nice-to-haves → auto-log to ISSUES.md, continue

**No user intervention needed for Rules 1-3, 5.** Only Rule 4 (architectural) requires user decision.

**All deviations documented in Summary** with: what was found, what rule applied, what was done, commit hash.

**Result:** Flow never breaks. Bugs get fixed. Scope stays controlled. Complete transparency.

See: workflows/execute-phase.md (deviation_rules section)

## Ship Fast, Iterate Fast

No enterprise process. No approval gates. No multi-week timelines.
Plan → Execute → Ship → Learn → Repeat.

**Milestone-driven:** Ship v1.0 → mark milestone → plan v1.1 → ship → repeat.
Milestones mark shipped versions and enable continuous iteration.

## Milestone Boundaries

Milestones mark shipped versions (v1.0, v1.1, v2.0).

**Purpose:**
- Historical record in MILESTONES.md (what shipped when)
- Greenfield → Brownfield transition marker
- Git tags for releases
- Clear completion rituals

**Default approach:** Extend existing roadmap with new phases.
- v1.0 ships (phases 1-4) → add phases 5-6 for v1.1
- Continuous phase numbering (01-99)
- Milestone groupings keep roadmap organized

**Archive ONLY for:** Separate codebases or complete rewrites (rare).

See: references/milestone-management.md

## Anti-Enterprise Patterns

NEVER include in plans:
- Team structures, roles, RACI matrices
- Stakeholder management, alignment meetings
- Sprint ceremonies, standups, retros
- Multi-week estimates, resource allocation
- Change management, governance processes
- Documentation for documentation's sake

If it sounds like corporate PM theater, delete it.

## Context Awareness

Monitor token usage via system warnings.

**At 25% remaining**: Mention context getting full
**At 15% remaining**: Pause, offer handoff
**At 10% remaining**: Auto-create handoff, stop

Never start large operations below 15% without user confirmation.

## User Gates

Never charge ahead at critical decision points. Use gates:
- **AskUserQuestion**: Structured choices (2-4 options)
- **Inline questions**: Simple confirmations
- **Decision gate loop**: "Ready, or ask more questions?"

Mandatory gates:
- Before writing PLAN.md (confirm breakdown)
- After low-confidence research
- On verification failures
- After phase completion with issues
- Before starting next phase with previous issues

See: references/user-gates.md

## Git Versioning

All planning artifacts are version controlled. Commit outcomes, not process.

- Check for repo on invocation, offer to initialize
- Commit only at: initialization, phase completion, handoff
- Intermediate artifacts (PLAN.md, RESEARCH.md, FINDINGS.md) NOT committed separately
- Git log becomes project history

See: references/git-integration.md

## Context Scan

**Run on every invocation** to understand current state:

```bash
# Check git status
git rev-parse --git-dir 2>/dev/null || echo "NO_GIT_REPO"

# Check for planning structure
ls -la .prompts/planning/ 2>/dev/null
ls -la .prompts/planning/phases/ 2>/dev/null

# Find any continue-here files
find . -name ".continue-here.md" -type f 2>/dev/null

# Check for existing artifacts
[ -f .prompts/planning/BRIEF.md ] && echo "BRIEF: exists"
[ -f .prompts/planning/ROADMAP.md ] && echo "ROADMAP: exists"
```

**If NO_GIT_REPO detected:**
Inline question: "No git repo found. Initialize one? (Recommended for version control)"
If yes: `git init`

**Present findings before intake question.**

## Domain Expertise

**Scan for domain expertise** to provide framework-specific context for planning:

```bash
# Check for project-level domain expertise
ls -la .claude/skills/expertise/ 2>/dev/null

# Check for user-level domain expertise
ls -la ~/.claude/skills/expertise/ 2>/dev/null
```

**Domain expertise locations:**
- **Project-level**: `.claude/skills/expertise/{domain-name}/` (portable with project)
- **User-level**: `~/.claude/skills/expertise/{domain-name}/` (available across projects)

**If domain expertise found:**
- Load relevant reference files to understand framework-specific patterns
- Include domain knowledge in planning decisions
- Reference domain workflows where appropriate

**If NO domain expertise found for current project stack:**
Present suggestion:
```
No domain expertise found for this stack. Consider generating custom expertise:

Run: /toolkit → Create → Domain Expertise Skill

This creates a comprehensive knowledge base for [Project Stack] in:
- .claude/skills/expertise/{domain-name}/ (project-level)
- ~/.claude/skills/expertise/{domain-name}/ (user-level)

Domain expertise provides:
- Framework-specific patterns and best practices
- Library comparisons and decision guidance
- Complete lifecycle workflows (build → debug → optimize → ship)
- Platform-specific considerations
```

**Note:** Domain expertise is generated on-demand into user-space paths. It is NOT shipped with the plugin.

## Planning Modes

<mode_selection>
The create-plans skill offers two modes to accommodate different complexity levels:

### Lite Mode
For simple tasks and quick iterations, Lite Mode creates a single `PLAN.md` in the current directory with a straightforward checklist structure.

**Characteristics:**
- Single file: `PLAN.md` in current directory
- Simple checklist format with `- [ ]` tasks
- Minimal ceremony - just the essentials
- Best for: quick prototypes, small features, one-off tasks, or when you need to move fast

**Structure:**
```markdown
# Objective
[Clear goal statement]

## Tasks
- [ ] Task 1 with specific file references
- [ ] Task 2 with specific file references
- [ ] Task 3 with specific file references

## Success Criteria
- [ ] Measurable criterion 1
- [ ] Measurable criterion 2
```

### Standard Mode
For complex projects requiring structured planning, Standard Mode maintains the full hierarchical approach (Brief → Roadmap → Phases).

**Characteristics:**
- Hierarchical structure: Brief → Roadmap → Phases
- Multiple planning artifacts
- Detailed context management
- Best for: multi-phase projects, complex architectures, team-level planning

**Structure:**
```
.prompts/planning/
├── BRIEF.md
├── ROADMAP.md
└── phases/
    ├── 01-foundation/
    └── 02-feature/
```
</mode_selection>

## Intake

Based on scan results, present context-aware options:

<handoff_protocol>
**If handoff found:**
```
Found handoff: .prompts/planning/phases/XX/.continue-here.md
[Summary of state from handoff]

1. Resume from handoff
2. Discard handoff, start fresh
3. Different action
```
</handoff_protocol>

**If planning structure exists:**
```
Project: [from BRIEF or directory]
Brief: [exists/missing]
Roadmap: [X phases defined]
Current: [phase status]

What would you like to do?
1. Plan next phase
2. Execute current phase
3. Create handoff (stopping for now)
4. View/update roadmap
5. Something else
```

**If no planning structure:**
```
No planning structure found.

What would you like to do?
1. Start new project (create brief)
2. Create roadmap from existing brief
3. Jump straight to phase planning
4. Get guidance on approach
```

**Wait for response before proceeding.**

## Routing

| Response | Workflow |
|----------|----------|
| "lite", "simple", "quick", "single plan" | **CREATE SINGLE PLAN.MD** → Create a simple PLAN.md in current directory |
| "brief", "new project", "start", 1 (no structure) | `workflows/create-brief.md` |
| "roadmap", "phases", 2 (no structure) | `workflows/create-roadmap.md` |
| "phase", "plan phase", "next phase", 1 (has structure) | `workflows/plan-phase.md` |
| "chunk", "next tasks", "what's next" | `workflows/plan-chunk.md` |
| "execute", "run", "do it", "build it", 2 (has structure) | **EXIT SKILL** → Use `/run-plan <path>` slash command |
| "research", "investigate", "unknowns" | `workflows/research-phase.md` |
<handoff_protocol>
| "handoff", "pack up", "stopping", 3 (has structure) | `workflows/handoff.md` |
| "resume", "continue", 1 (has handoff) | `workflows/resume.md` |
</handoff_protocol>
| "transition", "complete", "done", "next" | `workflows/transition.md` |
| "milestone", "ship", "v1.0", "release" | `workflows/complete-milestone.md` |
| "guidance", "help", 4 | `workflows/get-guidance.md` |

**Lite Mode Routing:** When user requests Lite Mode (via "lite", "simple", "quick", etc.):
1. Ask user to describe the task
2. Create a single `PLAN.md` in the current directory with:
   - `# Objective` - Clear goal
   - `## Tasks` - Checklist with explicit file references
   - `## Success Criteria` - Measurable completion criteria
3. Exit skill - user can execute with `/run-plan PLAN.md`

**Standard Mode Routing:** All other responses follow the hierarchical workflow.

**Critical:** Plan execution should NOT invoke this skill. Use `/run-plan` for context efficiency (skill loads ~20k tokens, /run-plan loads ~5-7k).

**After reading the workflow, follow it exactly.**

## Hierarchy

The planning hierarchy (each level builds on previous):

```
BRIEF.md          → Human vision (you read this)
    ↓
ROADMAP.md        → Phase structure (overview)
    ↓
RESEARCH.md       → Research prompt (optional, for unknowns)
    ↓
FINDINGS.md       → Research output (if research done)
    ↓
PLAN.md           → THE PROMPT (Claude executes this)
    ↓
SUMMARY.md        → Outcome (existence = phase complete)
```

Rules:
- Roadmap requires Brief (or prompts to create one)
- Phase plan requires Roadmap (knows phase scope)
- PLAN.md IS the execution prompt
- SUMMARY.md existence marks phase complete
- Each level can look UP for context

## Output Structure

All planning artifacts go in `.prompts/planning/`:

```
.prompts/planning/
├── BRIEF.md                    # Human vision
├── ROADMAP.md                  # Phase structure + tracking
└── phases/
    ├── 01-foundation/
    │   ├── 01-01-PLAN.md       # Plan 1: Database setup
    │   ├── 01-01-SUMMARY.md    # Outcome (exists = done)
    │   ├── 01-02-PLAN.md       # Plan 2: API routes
    │   ├── 01-02-SUMMARY.md
    │   ├── 01-03-PLAN.md       # Plan 3: UI components
    │   └── .continue-here-01-03.md  # Handoff (temporary, if needed)
    └── 02-auth/
        ├── 02-01-RESEARCH.md   # Research prompt (if needed)
        ├── 02-01-FINDINGS.md   # Research output
        ├── 02-02-PLAN.md       # Implementation prompt
        └── 02-02-SUMMARY.md
```

Naming convention:
- Plans: `{phase}-{plan}-PLAN.md` (e.g., 01-03-PLAN.md)
- Summaries: `{phase}-{plan}-SUMMARY.md` (e.g., 01-03-SUMMARY.md)
- Phase folders: `{phase}-{name}/` (e.g., 01-foundation/)

Files sort chronologically. Related artifacts (plan + summary) are adjacent.

## Reference Index

- `references/hierarchy-rules.md` - How levels build on each other
- `references/plan-format.md` - PLAN.md structure
- `references/context-management.md` - Token usage monitoring
- `references/scope-estimation.md` - Task sizing guidance
- `references/checkpoints.md` - Checkpoint types and handling
- `references/milestone-management.md` - Milestone completion
- `references/user-gates.md` - When to pause and ask
- `references/git-integration.md` - Version control patterns
- `references/research-pitfalls.md` - Known research mistakes
- `references/cli-automation.md` - CLI automation patterns

## Templates Index

- `templates/brief.md` - Project vision document with current state
- `templates/roadmap.md` - Phase structure with milestone groupings
- `templates/phase-prompt.md` - Executable phase prompt (PLAN.md)
- `templates/research-prompt.md` - Research prompt (RESEARCH.md)
- `templates/summary.md` - Phase outcome (SUMMARY.md) with deviations
- `templates/milestone.md` - Milestone entry for MILESTONES.md
- `templates/issues.md` - Deferred enhancements log (ISSUES.md)
- `templates/continue-here.md` - Context handoff format

## Workflows Index

- `workflows/create-brief.md` - Create project vision document
- `workflows/create-roadmap.md` - Define phases from brief
- `workflows/plan-phase.md` - Create executable phase prompt
- `workflows/execute-phase.md` - Run phase prompt, create summary
- `workflows/research-phase.md` - Create and run research prompt
- `workflows/plan-chunk.md` - Plan immediate next tasks
- `workflows/transition.md` - Mark phase complete, advance
- `workflows/complete-milestone.md` - Mark shipped version, create milestone entry
- `workflows/handoff.md` - Create context handoff for pausing
- `workflows/resume.md` - Load handoff, restore context
- `workflows/get-guidance.md` - Help decide planning approach

## When To Use

MUST USE when planning projects, phases, or tasks that an AI agent will execute.

**Context**: Plans are executable prompts, not documentation. Each plan should be:
- Scoped to 2-3 tasks maximum (~50% context usage)
- Independently executable by subagent with fresh context
- Verifiable with specific success criteria
- Complete with @file references for all context needed

**Workflow**: User → Brief → Roadmap → Phase Plans → Execute → Summary → Next Phase

**Example**: Phase "01-foundation" with 4 plans: database setup, API routes, UI components, frontend integration.

## Success Criteria

Planning skill succeeds when:
- [ ] Context scan runs before intake
- [ ] Appropriate workflow selected based on state
- [ ] PLAN.md IS the executable prompt (not separate)
- [ ] PLAN.md uses strict Markdown structure (not XML tags)
- [ ] Every task explicitly lists files to read/modify
- [ ] Plans are self-contained with Execution Context section
- [ ] Hierarchy is maintained (brief → roadmap → phase)
- [ ] Handoffs preserve full context for resumption
- [ ] Context limits are respected (auto-handoff at 10%)
- [ ] Deviations handled automatically per embedded rules
- [ ] All work (planned and discovered) fully documented
- [ ] Plan execution uses /run-plan command (not skill invocation)
