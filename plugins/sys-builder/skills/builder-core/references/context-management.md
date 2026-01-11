# Context Management Reference

## Principle

**Plans are executable prompts** - autonomous sessions run them with ZERO additional context.

## Critical Rules

### 1. Self-Contained Plans

Every plan must include:
- All @ file references for required reading
- Clear instructions for each task
- All necessary context in the plan itself

### 2. @ References

Use @ syntax to reference files:

```markdown
## Context

@.cattoolkit/planning/{project-slug}/BRIEF.md
@.cattoolkit/planning/{project-slug}/ROADMAP.md
@src/components/Button.tsx
@docs/api-spec.md
```

### 3. Context Budget

Aim for balanced context usage:
- ~50% for file references and reading
- ~30% for task definitions
- ~20% for verification criteria

### 4. File Paths

**Always use absolute or project-root relative paths:**

✅ Good:
- `@src/components/Button.tsx`
- `@.cattoolkit/planning/my-project/BRIEF.md`

❌ Bad:
- `@../../../components/Button.tsx`
- `@Button.tsx`

## Examples

### Minimal Context (Lite Plan)

```markdown
## Context

@.cattoolkit/planning/quick-fix/BRIEF.md
@src/utils/helpers.ts
```

### Full Context (Standard Plan)

```markdown
## Context

**Project Scope:**
@.cattoolkit/planning/user-auth-system/BRIEF.md
@.cattoolkit/planning/user-auth-system/ROADMAP.md

**Architecture:**
@.cattoolkit/planning/user-auth-system/ADR.md (if exists - created by Architect plugin)

**Source Files:**
@src/lib/db.ts
@src/middleware/auth.ts
@src/models/User.ts

**Configuration:**
@docs/api-design.md
@project configuration files
```

## Context Checklist

Before finalizing a plan, verify:

- [ ] All required files have @ references
- [ ] References use clear paths
- [ ] No relative paths like `../../`
- [ ] File paths are accurate and current
- [ ] Context budget is balanced
- [ ] Plan is self-contained

## Progressive Context Loading

Plans are loaded progressively:

1. **Level 1 (Startup)**: SKILL.md metadata
2. **Level 2 (When triggered)**: Full SKILL.md content
3. **Level 3 (On demand)**: Workflow files, templates, references

This keeps initial load minimal while providing full depth when needed.
