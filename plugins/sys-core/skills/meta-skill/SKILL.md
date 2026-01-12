---
name: meta-skill
description: "Comprehensive guide for creating Claude Code skills following Universal Agentic Runtime standards. MUST Use when building skills, designing skill architecture, implementing progressive disclosure, or validating skill structure."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash(mkdir:-p), Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(rm:*), Bash(mv:*)]
---

# Meta-Skill: Skill Architecture Authority

## Objective

Meta-Skill provides expert guidance for creating effective Claude Code skills that embody the Universal Agentic Runtime principles. It teaches you how to analyze requirements, choose appropriate templates, implement progressive disclosure, and validate skill structures to ensure optimal performance and maintainability.

> **Core Principle:** Skills are knowledge bases that provide domain expertise through progressive disclosure, not workflow routers. They should be designed for reusability and optimized for context window efficiency.

## Context & Standards

Skill creation follows Universal Agentic Runtime standards emphasizing:
- **Progressive Disclosure**: Core content in `SKILL.md` (< 500 lines), detailed docs in `references/`
- **Inline-First**: Avoid unnecessary forking (cost: inline=1, fork=3)
- **Zero-Waste**: Maximize inline skills for local engineering tasks
- **Intent-Driven**: Skills are discovered by intent, not called procedurally

## Quick Start Algorithm

1. **ANALYZE** → Understand purpose, complexity, and use cases
2. **DESIGN** → Choose template (Standard/Progressive/Router/Minimal/Checklist)
3. **IMPLEMENT** → Create `SKILL.md` with proper frontmatter
4. **VALIDATE** → Run validation scripts
5. **OPTIMIZE** → Apply progressive disclosure principles

**Detailed Workflow**: [references/creation-workflow.md](references/creation-workflow.md)

## Capability Index & References

### 1. Creation & Architecture
- **Creation Workflow**: [references/creation-workflow.md](references/creation-workflow.md)
- **Naming Conventions**: [references/naming-conventions.md](references/naming-conventions.md)
- **Description Patterns**: [references/description-patterns.md](references/description-patterns.md)
- **Progressive Disclosure**: [references/progressive-disclosure.md](references/progressive-disclosure.md)

### 2. Implementation Guides
- **Standard Skill Creation**: See [references/templates-usage.md](references/templates-usage.md)
- **Advanced Architectures**: See [references/integration-guide.md](references/integration-guide.md)
- **Template Usage**: [references/templates-usage.md](references/templates-usage.md)
- **Integration Guide**: [references/integration-guide.md](references/integration-guide.md)

### 3. Validation & Quality
- **Validation Rules**: See success_criteria section below
- **Anti-Patterns**: [references/anti-patterns.md](references/anti-patterns.md)
- **Quick Reference**: [references/quick-reference.md](references/quick-reference.md)

## Templates (Assets)

Available in `assets/`:

| Template | Use When | Complexity |
|----------|----------|------------|
| **Standard** | Single capability, straightforward | Low |
| **Progressive** | Complex domain expertise | High |
| **Router** | Multiple workflows/paths | Medium |
| **Minimal** | Internal tools, utilities | Low |
| **Checklist** | Task-oriented with validation | Medium |

## Validation Commands

**Run all validations:**
```bash
uv run scripts/validate-all.py ./my-skill/
```

**Individual Checks:**
- Name: `./scripts/validate-skill-name.py my-skill`
- Description: `./scripts/validate-description.py ./my-skill/`
- Frontmatter: `./scripts/validate-frontmatter.py ./my-skill/`
- Token Budget: `./scripts/check-token-budget.py ./my-plugin/`

## Success Criteria

A well-designed skill has:
- [ ] Valid name format (lowercase, kebab-case, 3-64 chars)
- [ ] Clear description (10-1024 chars, follows pattern)
- [ ] Proper structure (`SKILL.md` + organized `references/`)
- [ ] Progressive disclosure (< 500 lines in `SKILL.md`)
- [ ] No broken links (validated with scripts)
- [ ] Appropriate template choice (matches complexity)
- [ ] Complete validation (all scripts pass)
- [ ] Inline when possible (cost optimization)
- [ ] Intent-driven design (discovered, not called)
- [ ] No anti-patterns (follows best practices)
