# Plan Format

## Overview

Claude-executable plans have a specific format that enables Claude to implement without interpretation. This reference defines what makes a plan executable vs. vague.

**Key insight:** PLAN.md IS the executable prompt. It contains everything Claude needs to execute the phase, including objective, context references, tasks, verification, success criteria, and output specification.

**Scoped Organization:** All plans use scoped folders: `.cattoolkit/planning/{project-slug}/` where `{project-slug}` is kebab-case project name (e.g., `user-auth-system`).

## Uninterrupted Flow Architecture

This plugin uses **Uninterrupted Flow** - agents execute autonomously without blocking for human input. Use **Self-Verification Points** instead of checkpoints. See `execution-observation-points.md` for patterns.

## Core Principle

A plan is Claude-executable when Claude can read the PLAN.md and immediately start implementing without asking clarifying questions.

If Claude has to guess, interpret, or make assumptions - the task is too vague.

## Prompt Structure
**Template:** `references/templates/phase-plan.md`

## 3. Plan Components

### Header Validation
Every plan MUST start with specific metadata.

**Required Fields:**
- `id`: Unique identifier (e.g., `feature-auth-login`)
- `parent`: ID of parent roadmap item (e.g., `roadmap-q1-2024`)
- `status`: [proposed | approved | in-progress | complete | blocked]
- `owner`: Agent responsible (e.g., `executor`)
- `mode`: [plan | act] (default: `plan`)

### Context Section
**Must include:**
- **Objective**: Clear 1-sentence goal
- **Dependencies**: Prerequisite files/PRs
- **Constraints**: Security, performance, or tech stack limits
- **Outcome**: Verifiable definition of done

### Task List
**Format:** `references/templates/phase-plan.md` (See Tasks section), you can omit this field.

### Field: Action

**What it is**: Natural language description of what needs to be implemented, written as narrative prose.

**Good**: "Create a POST endpoint that accepts {email, password} credentials. The endpoint should query the User table to find the user by email, then securely compare the provided password with the stored hash. If the credentials match, generate and return an authentication token."

**Bad**: "Add authentication", "Make login work"

Write this like a senior engineer describing work to another senior engineer. Include context, constraints, and what's important to get right.

### Field: Verify

**What it is**: How to prove the task is complete.

**Good**:

- Tests pass
- `curl -X POST /api/auth/login` returns 200 with Set-Cookie header
- Build completes without errors

**Bad**: "It works", "Looks good", "User can log in"

Must be executable - a command, a test, an observable behavior.

### Field: Done

**What it is**: Acceptance criteria - the measurable state of completion.

**Good**: "Valid credentials return 200 + JWT cookie, invalid credentials return 401"

**Bad**: "Authentication is complete"

Should be testable without subjective judgment.

## Task Structure

All tasks use a single format. Agents execute autonomously in Uninterrupted Flow.

### Task Format

See `references/templates/phase-plan.md` for the exact task format.

### Self-Verification Points

After completing tasks, agents log verification evidence in SUMMARY.md:

```markdown
### Self-Verification Point

**Verification**: Run tests and build

**Evidence**: Log test results, build output, and CLI confirmations

**Proceed**: Continue to next task or phase boundary
```

**Uninterrupted Flow Pattern:**
1. Execute task
2. Run automated verification
3. Log result in SUMMARY.md
4. Proceed to next task

**STRICTLY PROHIBITED:** Blocking Checkpoints, "Resume Signals", waiting for human input during execution.

**Blockers:** If truly blocked (auth gates, unrecoverable errors), create HANDOFF.md and exit. See `execution-observation-points.md`.

**Human Review:** Occurs at phase boundaries via SUMMARY.md, not during task execution.

## Context References

Use @file references to load context for the prompt:

```markdown
## Context
@.cattoolkit/planning/BRIEF.md           # Project vision
@.cattoolkit/planning/ROADMAP.md         # Phase structure
@.cattoolkit/planning/phases/02-auth/FINDINGS.md  # Research results
@src/lib/db.ts                # Existing database setup
@src/types/user.ts            # Existing type definitions
```

Reference files that Claude needs to understand before implementing.

## Verification Section

Overall phase verification (beyond individual task verification):

```markdown
## Verification
Before declaring phase complete:
- [ ] Build succeeds without errors
- [ ] Tests pass
- [ ] No compilation errors
- [ ] Feature works end-to-end manually
```

## Success Criteria Section

Measurable criteria for phase completion:

```markdown
## Success Criteria
- All tasks completed
- All verification checks pass
- No errors or warnings introduced
- JWT auth flow works end-to-end
- Protected routes redirect unauthenticated users
```

## Output Section

Specify the SUMMARY.md structure:

```markdown
## Output
After completion, create `.cattoolkit/planning/phases/XX-name/SUMMARY.md`:

# Phase X: Name Summary

**[Substantive one-liner]**

## Accomplishments
## Files Created/Modified
## Decisions Made
## Issues Encountered
## Next Phase Readiness
```

## Specificity Levels

### Too Vague

```markdown
### Task 1: Add authentication

**Scope**: ??? (unknown)

**Action**: Implement auth (vague - how?)

**Verify**: ??? (unclear how to verify)

**Done**: Users can authenticate (subjective)
```

Claude: "How? What type? What library? Where?"

### Just Right

```markdown
### Task 1: Create login endpoint with JWT

**Scope**: Authentication endpoint

**Action**: Implement a POST endpoint that accepts {email, password} credentials. The endpoint should query the User table to find the user by email, then securely compare the provided password with the stored hash. If the credentials match, generate a JWT token using the jose library (not jsonwebtoken - CommonJS issues with Next.js Edge runtime) and set it as an httpOnly cookie with 15-minute expiry. Return 200. On mismatch, return 401.

**Verify**: `curl -X POST localhost:3000/api/auth/login -H "Content-Type: application/json" -d '{"email":"test@test.com","password":"test123"}'` returns 200 with Set-Cookie header containing JWT

**Done**: Valid credentials → 200 + cookie. Invalid → 401. Missing fields → 400.
```

Claude can implement this immediately.

### Too Detailed

Writing the actual code in the plan. Trust Claude to implement from clear instructions.

## Anti-Patterns

### Vague Actions

- "Set up the infrastructure"
- "Handle edge cases"
- "Make it production-ready"
- "Add proper error handling"

These require Claude to decide WHAT to do. Specify it.

### Unverifiable Completion

- "It works correctly"
- "User experience is good"
- "Code is clean"
- "Tests pass" (which tests? do they exist?)

These require subjective judgment. Make it objective.

### Missing Context

- "Use the standard approach"
- "Follow best practices"
- "Like the other endpoints"

Claude doesn't know your standards. Be explicit.

## Sizing Tasks

Good task size: 15-60 minutes of Claude work.

**Too small**: "Add import statement for bcrypt" (combine with related task)
**Just right**: "Create login endpoint with JWT validation" (focused, specific)
**Too big**: "Implement full authentication system" (split into multiple plans)

If a task takes multiple sessions, break it down.
If a task is trivial, combine with related tasks.

**Note on scope:** If a phase has >7 tasks or spans multiple subsystems, split into multiple plans using the naming convention `{phase}-{plan}-PLAN.md`.
