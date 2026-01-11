# Progressive Disclosure Architecture

## The Principle

Reference files are NOT bloat—they are **context rot prevention**.

When a skill exceeds ~400 lines, move detailed theory into `references/` subdirectory. The SKILL.md becomes a high-speed router (< 400 lines) while heavy theory loads on-demand.

## Load Strategy

### Discovery Phase (~50-100 tokens)
- Only `name` and `description` loaded at startup
- AI scans all skills for semantic matching

### Activation Phase (<500 tokens)
- Full `SKILL.md` loaded when skill is activated
- Should contain: quick reference, triggers, common patterns

### Resource Phase (On-Demand)
- Files in `scripts/`, `references/`, `assets/` loaded only when needed
- Triggered by explicit references in SKILL.md

## When to Split

**Move to `references/` when:**
- Theory exceeds 100 lines
- Content is reference material (tables, checklists, standards)
- Content is domain-specific background
- Content is rarely needed for common tasks

**Keep in `SKILL.md` when:**
- Core operational protocol
- Quick reference tables
- Common patterns
- Triggers for loading references

## Split Pattern

**Before (Monolithic SKILL.md - 600+ lines):**
```markdown
# My Skill

## Core Protocol
[50 lines]

## Detailed Theory
[200 lines of theory]

## Reference Tables
[150 lines of tables]

## Examples
[100 lines of examples]

## Edge Cases
[100 lines of edge cases]
```

**After (Progressive Disclosure):**

**SKILL.md (< 400 lines):**
```markdown
# My Skill

## Core Protocol
[50 lines]

## Quick Reference
[Summary table]

## Operational Protocol
[50 lines]

## When to Load References
- Load `references/theory.md` for detailed background
- Load `references/tables.md` for complete reference data
- Load `references/examples.md` for detailed examples
```

**references/theory.md:**
```markdown
# Detailed Theory

[200 lines of theory]
```

**references/tables.md:**
```markdown
# Reference Tables

[150 lines of tables]
```

**references/examples.md:**
```markdown
# Examples

[100 lines of examples]
```

## Benefits

1. **Context Efficiency:** Only load what's needed for the current task
2. **Faster Discovery:** AI can scan more skills without hitting token limits
3. **Better Maintenance:** Theory separated from protocol
4. **Clearer Structure:** SKILL.md as router, references/ as detail

## Implementation Checklist

- [ ] SKILL.md is under 400 lines
- [ ] SKILL.md contains quick reference and triggers
- [ ] Heavy theory moved to `references/`
- [ ] Reference files are clearly named
- [ ] SKILL.md indicates when to load each reference
- [ ] References use relative paths from skill root
