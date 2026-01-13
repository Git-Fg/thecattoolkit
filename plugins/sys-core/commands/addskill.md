---
description: "Interactive skill creation wizard with step-by-step guidance."
argument-hint: "[skill-name] [plugin]"
allowed-tools: [Skill(scaffold-component), AskUserQuestion, Read, Write, Edit, Bash, Bash(mkdir:-p), Bash(ls:*), Bash(cat:*)]
disable-model-invocation: true
---

# AddSkill Command

Interactive wizard for creating new Claude Code skills.

## Input Analysis

**Skill name**: `!echo "$1"`
**Plugin**: `!echo "$2"`

## Workflow

If skill name is empty, use `AskUserQuestion` to gather:

```markdown
{
  "questions": [
    {
      "question": "What is the skill name? (kebab-case, 3-64 chars)",
      "header": "Skill Name",
      "options": [
        {"label": "Provide name", "description": "Enter a custom skill name"},
        {"label": "Cancel", "description": "Exit the wizard"}
      ],
      "multiSelect": false
    },
    {
      "question": "Which plugin should contain this skill?",
      "header": "Plugin",
      "options": [
        {"label": "sys-core", "description": "Universal tooling, scaffolding, validation"},
        {"label": "sys-builder", "description": "Build workflows, architecture, planning"},
        {"label": "sys-research", "description": "Data gathering, external APIs"},
        {"label": "sys-cognition", "description": "AI/ML techniques, reasoning frameworks"},
        {"label": "sys-multimodal", "description": "Vision, audio, cross-modal processing"},
        {"label": "sys-edge", "description": "Mobile, offline, edge computing"}
      ],
      "multiSelect": false
    },
    {
      "question": "What archetype is your skill?",
      "header": "Skill Archetype",
      "options": [
        {"label": "Procedural", "description": "Deterministic, repeatable processes (Protocol autonomy)"},
        {"label": "Advisory", "description": "Expertise and recommendations (Guided autonomy)"},
        {"label": "Generator", "description": "Create structured outputs (Guided autonomy)"},
        {"label": "Orchestrator", "description": "Coordinate multiple capabilities"}
      ],
      "multiSelect": false
    }
  ]
}
```

## Execution

Invoke `Skill(scaffold-component)` with gathered information:

1. **Documentation Research** - Read guides in `docs/`
2. **Meta-Skill Investigation** - Study `meta-skill` standards
3. **External Research** - If URL provided, research domain
4. **Existing Skill Audit** - Check for overlapping skills
5. **Plugin Placement** - Confirm or adjust plugin choice
6. **Skill Design** - Create frontmatter and structure
7. **Implementation** - Write SKILL.md and references
8. **Validation** - Run `toolkit-analyzer.py` and fix issues
9. **Command Creation** - Generate companion command (optional)
10. **Summary Report** - Provide completion report

## Output Format

```
Created: <skill-name>
Location: plugins/<plugin>/skills/<skill-name>/SKILL.md
Archetype: <Procedural/Advisory/Generator/Orchestrator>
Autonomy: <Protocol/Guided/Heuristic>
Description: <SEO-optimized description>

Files created:
- SKILL.md (<n> lines)
- references/*.md (<n> files)
- scripts/*.py (<n> files)

Validation: PASSED

Next steps:
1. Test: /sys-core:<skill-name> <test-case>
2. Review: docs/guides/skills.md
3. Verify 12-Point QA Checklist
4. Iterate based on usage
```

## Quick Start

For immediate skill creation with defaults:

```bash
/sys-core:addskill my-skill sys-core
```

For interactive wizard:

```bash
/sys-core:addskill
```
