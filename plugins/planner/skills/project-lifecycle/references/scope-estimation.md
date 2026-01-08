# Scope Estimation Reference

## Core Principle

**2-3 tasks per phase maximum**

One phase ≈ one autonomous execution session (~50-100 turns)

## Task Sizing

### Too Large (Split It)

```markdown
❌ "Implement authentication"
→ This is 5+ tasks: User model, login endpoint, logout endpoint,
  auth middleware, token refresh
```

### Just Right

```markdown
✅ Task 1: "Create User model in Prisma schema"
✅ Task 2: "Create login API endpoint"
✅ Task 3: "Create auth middleware for protected routes"
```

## Sizing Guidelines

### Count Tasks by Verb-Noun Pairs

Each task = one primary action:

- "Create User model" = 1 task
- "Build login endpoint" = 1 task
- "Add auth middleware" = 1 task

**If you have 4+ verbs, split the phase.**

### Estimation by Complexity

| Complexity | Tasks | Example |
|------------|-------|---------|
| Simple | 1-2 | Add utility function, fix bug |
| Medium | 2-3 | Create API endpoint, add model |
| Complex | 3 | Build feature with multiple files |

### When to Split

**Split phase if:**
- >3 tasks needed
- Tasks span different concern areas (e.g., DB + API + UI)
- Context budget exceeds ~50%
- Related but separable functionality

## Splitting Example

### Before (Too Large)

```markdown
## Phase: Authentication
- Task 1: Create User model
- Task 2: Create login endpoint
- Task 3: Create logout endpoint
- Task 4: Create refresh endpoint
- Task 5: Add auth middleware
- Task 6: Add protected routes
```

### After (Split)

```markdown
## Phase 1: Auth Foundation
- Task 1: Create User model
- Task 2: Create login endpoint
- Task 3: Create auth middleware

## Phase 2: Auth Completion
- Task 1: Create logout endpoint
- Task 2: Create refresh endpoint
- Task 3: Add protected routes
```

## Phase Numbering

Use sequential numbering:
- `01-foundation`
- `02-auth`
- `03-features`

If splitting a phase later:
- `01-foundation-part-1`
- `01-foundation-part-2`

Or renumber:
- `01-foundation`
- `02-setup` (was part of 01)
- `03-implementation`

## Context Budget Management

**Aim for ~50% context usage:**

- Minimal context: 2-3 tasks, simple files
- Medium context: 3 tasks, moderate complexity
- High context: 3 tasks, complex architecture

**If context >70%, consider:**
- Splitting phase
- Reducing file references
- Using architecture docs instead of source files
