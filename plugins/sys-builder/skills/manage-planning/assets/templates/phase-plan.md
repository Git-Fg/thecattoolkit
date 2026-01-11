# Phase Plan Template

**MANDATORY:** Use this structure for `.cattoolkit/planning/{project-slug}/phases/XX-name/{phase}-{plan}-PLAN.md`

**Naming:** `{phase}-{plan}-PLAN.md` format (e.g., `01-02-PLAN.md` for Phase 1, Plan 2)

```markdown
---
phase: XX-name
type: execute
status: in_progress
---

## Objective

[What this phase accomplishes]

Purpose: [Why this matters]
Output: [What artifacts will be created]

## Execution Instructions

**UNINTERRUPTED FLOW MODE:**
1. Execute tasks in order WITHOUT pausing
2. For each task: implement → verify → log results → continue
3. Use Self-Verification Points (no blocking checkpoints)
4. Create summary file after all tasks complete

**Subagents DO NOT have AskUserQuestion access. MUST use judgment from context.**

## Context

@.cattoolkit/planning/{project-slug}/BRIEF.md
@.cattoolkit/planning/{project-slug}/ROADMAP.md
@.cattoolkit/planning/{project-slug}/ADR.md (if exists - created by Architect plugin)
@relevant/source/files

## Tasks

### Task 1: [Action-oriented name]

**Scope**: [Describe the scope - you may list files, directories, or architectural concepts like "The Auth Module"]

**Action**: [Natural language description of what needs to be implemented. Include what, how, and any pitfalls to avoid. Write this as a narrative description rather than a checklist.]

**Verify**: [Command or check to prove completion]

**Done**: [Measurable acceptance criteria]

### Task 2: [Action-oriented name]

**Scope**: [Describe the scope]

**Action**: [Natural language description of the implementation]

**Verify**: [Verification method]

**Done**: [Acceptance criteria]

## Verification

Before declaring phase complete:
- [ ] Build/compile succeeds
- [ ] Tests pass
- [ ] No type/lint errors

## Success Criteria

- All tasks completed
- All verification checks pass
- No errors introduced
- [Phase-specific criteria]

## Output

Create `{phase}-{plan}-SUMMARY.md` with:
- Accomplishments
- Files modified
- Verification evidence
- Decisions made
- Next steps
```

## Guidelines

- **2-3 tasks per plan** (split if >7 tasks)
- **Write naturally** - Use narrative prose in Action sections, like describing work to a colleague
- **Scope can be flexible** - List specific files, directories, or architectural concepts (e.g., "The Auth Module")
- **Verify must be executable** - a command, test, or observable check
- **Action includes context** - What, how, and pitfalls to avoid, all in natural language

## Example (Generic)

```markdown
---
phase: 01-foundation
type: execute
status: in_progress
---

## Objective

Set up project with authentication foundation.

Purpose: Establish core structure and auth patterns.
Output: Working app with token auth and user model.

## Context

@.cattoolkit/planning/myproject/BRIEF.md
@.cattoolkit/planning/myproject/ROADMAP.md
@src/models/user

## Tasks

### Task 1: Create User model

**Scope**: User model and database schema

**Action**: Create a User model that will serve as the foundation for authentication. The model should include: an id field, a unique email field for login, a password_hash field for secure storage, and standard timestamp fields for tracking creation and updates. Also add database indexes on the email field to optimize lookups during login attempts.

**Verify**: Schema validation passes, model generates without errors

**Done**: User model defined, validated, ready for queries

### Task 2: Create login endpoint

**Scope**: Authentication endpoint

**Action**: Implement a POST endpoint at /api/auth/login that accepts {email, password} credentials. The endpoint should query the User table to find the user by email, then securely compare the provided password with the stored hash. If the credentials match, generate and return an authentication token. If they don't match, return a 401 error.

**Verify**: POST request with valid credentials returns 200 + token

**Done**: Valid credentials → 200 + token. Invalid → 401.

## Verification

- [ ] Build succeeds
- [ ] Schema validates
- [ ] Auth endpoint responds correctly

## Success Criteria

- All tasks completed
- Token auth flow works end-to-end
```

## Anti-Patterns

 **Too vague:**
```markdown
**Action**: Add auth to the app
**Done**: Users can log in
```

 **No verification:**
```markdown
**Verify**: It works correctly
```

 **Tech-specific assumptions:**
```markdown
**Verify**: npm run build && npm test
```
Use generic: "Build succeeds, tests pass"
