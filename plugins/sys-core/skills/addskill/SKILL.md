---
name: addskill
description: "Creates Claude Code skills following Anthropic best practices and Cat Toolkit standards. Provides step-by-step workflow from documentation research through validation. Use when creating new skills, designing skill architecture, implementing progressive disclosure, or scaffolding skill components."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Bash(mkdir:-p), Bash(ls:*), Bash(cat:*), AskUserQuestion, Skill(meta-skill)]
user-invocable: false
---

# AddSkill: Skill Creation Workflow

Guides creation of production-ready Claude Code skills optimized for context window efficiency and marketplace portability.

## Core Principles

**Token Optimization**:
- Keep `SKILL.md` < 500 lines (aim for 200-300)
- Move detailed content to `references/`
- Use `scripts/` for deterministic logic

**Progressive Disclosure**:
- Level 1: Frontmatter (trigger)
- Level 2: `SKILL.md` (router, < 500 lines)
- Level 3: `references/` (on-demand details)

**Third-Person Only**:
- ✓ "Processes CSV files. Use when..."
- ✗ "I can help you..."
- ✗ "Use this when you want..."

## Quick Start Workflow

```
Skill Creation Progress:
- [ ] Phase 1: Documentation research (docs/)
- [ ] Phase 2: Meta-skill investigation
- [ ] Phase 3: External research (if URL provided)
- [ ] Phase 4: Existing skill audit
- [ ] Phase 5: Plugin placement strategy
- [ ] Phase 6: Skill design
- [ ] Phase 7: Implementation
- [ ] Phase 8: Validation
- [ ] Phase 9: Command shortcut (optional)
- [ ] Phase 10: Summary report
```

## Phase 1: Documentation Research

Read in order to understand architecture:

1. **Skill architecture**: `docs/guides/skills.md`
2. **Command patterns**: `docs/guides/commands.md`
3. **Component selection**: `docs/REFERENCES.md` section 3.1

**Extract from docs:**
- Skill archetype (Procedural/Qualitative/Migration/Zero-Context)
- Progressive disclosure patterns
- Token optimization strategies

## Phase 2: Meta-Skill Investigation

**Read**: `plugins/sys-core/skills/meta-skill/SKILL.md`

**Key information:**
- Template selection (Standard/Progressive/Router/Minimal/Checklist)
- Naming conventions: `^[a-z][a-z0-9-]{2,49}$`
- Description patterns: `{CAPABILITY}. Use when {TRIGGERS}.`
- Success criteria checklist

## Phase 3: External Research

If user provides URL or external reference:

**For GitHub repos:**
```bash
mcp__plugin_sys-research_gitingest__ask_question
- repoName: extract from URL
- question: "What is the main purpose? Key features? How would this translate to a Claude skill?"
```

**For web documentation:**
```bash
mcp__web_reader__webReader
- url: provided URL
- return_format: markdown
- retain_images: false
```

**Synthesize research into:**
- Core domain concepts
- Typical workflows/patterns
- Key terminology
- Integration points

## Phase 4: Existing Skill Audit

Check for overlapping or related skills:

```bash
Grep pattern="<domain keyword>" path="plugins/**/*.md" output_mode="files_with_matches"
Glob pattern="plugins/**/skills/*/"
```

**If overlap found:**
- Read existing skill(s)
- Determine if extension or refactoring is appropriate
- Consider consolidation vs fragmentation

## Phase 5: Plugin Placement Strategy

**Plugin decision matrix:**

| Plugin | Use For | Examples |
|--------|---------|----------|
| **sys-core** | Universal tooling, scaffolding, validation | meta-skill, scaffold-component |
| **sys-builder** | Build workflows, architecture, planning | architecture, test-writer |
| **sys-research** | Data gathering, external APIs | researcher, gitingest |
| **sys-cognition** | AI/ML techniques, reasoning | prompt-engineering, thinking-frameworks |
| **sys-multimodal** | Vision, audio, cross-modal | multimodal-understanding |

**Placement criteria:**
1. Domain specificity match
2. Reusability (sys-core for general tools)
3. Infrastructure requirements

## Phase 6: Skill Design

**Frontmatter requirements:**
- `name`: kebab-case, 3-64 chars, matches directory
- `description`: 3rd person, `{CAPABILITY}. Use when {TRIGGERS}.`
- `allowed-tools`: Minimum required (security principle)
- Optional: `user-invocable: false`, `context: fork`, `disable-model-invocation: true`

**SKILL.md structure:**
1. Core instructions (< 100 lines)
2. Resource links to `references/*.md`
3. Script calls to `scripts/*.py`

**Naming validation:**
```bash
uv run scripts/validate-skill-name.py <skill-name>
```

**Reference organization:**
- `references/theory.md` - Deep domain knowledge
- `references/workflows.md` - Step-by-step procedures
- `references/examples.md` - Concrete usage examples
- `assets/templates/` - Reusable templates

## Phase 7: Implementation

**Create directory:**
```bash
mkdir -p plugins/<plugin>/skills/<skill-name>/{references,assets,scripts}
```

**Write files:**
1. `SKILL.md` - Entry point with frontmatter
2. `references/*.md` - Domain knowledge
3. `assets/templates/` - Templates (if applicable)
4. `scripts/*.py` - Deterministic logic (if applicable)

**Critical constraints:**
- NO `../` relative paths
- NO Windows-style paths (`\`)
- Each skill owns its `references/`, `assets/`, `scripts/`

## Phase 8: Validation

**Run validation:**
```bash
uv run scripts/toolkit-analyzer.py
```

**Fix any issues:**
- Name format violations
- Description format issues
- Missing required fields
- Path traversal violations
- Broken internal links

**Re-validate until clean.**

## Phase 9: Command Shortcut (Recommended)

Create companion command at `plugins/<plugin>/commands/<skill-name>.md`:

```yaml
---
description: "Quick access to <skill-name> functionality"
argument-hint: "[args]"
allowed-tools: [Skill(<skill-name>)]
disable-model-invocation: true
---

# <Skill Name> Command

Invoke Skill(<skill-name>) with provided arguments.
```

## Phase 10: Summary Report

Provide user with:

```
Created: <skill-name>
Location: plugins/<plugin>/skills/<skill-name>/SKILL.md
Type: <archetype>
Description: <description text>
Command: /<plugin>:<skill-name>

Files:
- SKILL.md (<n> lines)
- references/*.md (<n> files)

Validation: PASSED

Next steps:
1. Test: /<plugin>:<skill-name> <test-case>
2. Review: docs/guides/skills.md
3. Iterate based on usage
```

## Detailed References

**YAML Frontmatter**: [references/frontmatter-standards.md](references/frontmatter-standards.md)
**Workflow Details**: [references/workflow-details.md](references/workflow-details.md)
**Validation Rules**: [references/validation-criteria.md](references/validation-criteria.md)
**Template Examples**: [references/template-examples.md](references/template-examples.md)
**Anti-Patterns**: [references/anti-patterns.md](references/anti-patterns.md)

## Validation Checklist

Before completing skill creation:

**Frontmatter:**
- [ ] Name matches directory (kebab-case)
- [ ] Description is 3rd person
- [ ] Description includes "Use when" pattern
- [ ] No forbidden fields (`permissionMode`, `model`)
- [ ] `allowed-tools` specified (security)

**Structure:**
- [ ] SKILL.md < 500 lines
- [ ] No nested references (one level deep)
- [ ] No `../` paths
- [ ] Unix-style forward slashes

**Content:**
- [ ] Assumes Claude is smart
- [ ] Consistent terminology
- [ ] Concrete examples
- [ ] Progressive disclosure used

**Validation:**
- [ ] `toolkit-analyzer.py` passes
- [ ] No broken links
- [ ] Name regex passes

## Success Criteria

A well-designed skill has:
- Valid name format
- Clear 3rd-person description
- Proper structure (SKILL.md + references/)
- Progressive disclosure (< 500 lines)
- No broken links
- Appropriate template choice
- Complete validation (all scripts pass)
- Inline-first when possible (cost optimization)
- Intent-driven design
- No anti-patterns
