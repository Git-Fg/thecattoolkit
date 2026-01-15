---
description: "Complete workflow to research, design, and create production-ready skills from inspiration or external documentation."
argument-hint: "<skill description, URL, or documentation source>"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, Skill(scaffold-component), mcp__plugin_sys-research_gitingest__ask_question, mcp__web_reader__webReader, mcp__plugin_sys-research_duckduckgo__search]
disable-model-invocation: true
---

# Skill Creation Workflow

## Input
User provided: `$ARGUMENTS`

## Phase 1: Documentation Research (docs/)

First, investigate the Cat Toolkit documentation to understand best practices for the type of skill being created.

**Read these files in order:**
1. `docs/guides/skills.md` - Skill architecture principles
2. `docs/guides/commands.md` - When to use Commands vs Skills
3. `docs/REFERENCES.md` sections:
   - Section 3.1: Component Selection Guide
   - Section 3.2: Progressive Disclosure
   - Section 3.3: Skill Architecture

**Extract from docs:**
- Appropriate skill archetype (Procedural, Qualitative, Migration, Zero-Context)
- Progressive disclosure patterns (what goes in SKILL.md vs references/)
- Token optimization strategies
- Anti-patterns to avoid

## Phase 2: Meta-Skill Investigation

Research the meta-skill authority to understand skill creation standards.

**Read:** `plugins/sys-core/skills/meta-skill/SKILL.md`

**Key information to extract:**
- Template selection (Standard/Progressive/Router/Minimal/Checklist)
- Naming conventions and validation rules
- Description patterns (Standard vs Enhanced)
- Progressive disclosure mechanics
- Success criteria checklist

**Also check:** `plugins/sys-core/skills/toolkit-registry/SKILL.md` for system authority standards.

## Phase 3: External Research (if URL provided)

If `$ARGUMENTS` contains a URL or reference to external documentation:

**For GitHub repositories:**
```bash
Use mcp__plugin_sys-research_gitingest__ask_question with:
- repoName: extract from URL
- question: "What is the main purpose of this repository? What are the key features? How would this translate to a Claude skill?"
```

**For web documentation:**
```bash
Use mcp__web_reader__webReader with:
- url: the provided URL
- return_format: markdown
- retain_images: false
```

**For general research:**
```bash
Use mcp__plugin_sys-research_duckduckgo__search with:
- query: "Claude Code skill best practices [domain]"
- max_results: 10
```

**Synthesize external research into:**
- Core domain concepts
- Typical workflows or patterns
- Key terminology to use in descriptions
- Potential integration points

## Phase 4: Existing Skill Audit

Check for overlapping or related existing skills that could be extended rather than creating new ones.

**Search for existing skills:**
```bash
Grep pattern="<domain keyword>" path="plugins/**/*.md" output_mode="files_with_matches"
Glob pattern="plugins/**/skills/*/"
```

**If overlap found:**
- Read the existing skill(s)
- Determine if extension or refactoring is more appropriate
- Consider consolidation instead of fragmentation

## Phase 5: Plugin Placement Strategy

Determine the optimal plugin location for the new skill.

**Plugin decision matrix:**
| Plugin | Use For | Examples |
|--------|---------|----------|
| **sys-core** | Universal tooling, validation, scaffolding | meta-skill, scaffold-component |
| **sys-builder** | Build workflows, architecture, planning | architecture, test-writer |
| **sys-research** | Data gathering, external APIs | researcher, gitingest |
| **sys-cognition** | AI/ML techniques, reasoning frameworks | prompt-engineering, thinking-frameworks |
| **sys-multimodal** | Vision, audio, cross-modal processing | multimodal-understanding |
| **sys-edge** | Mobile, offline, edge computing | edge-ai-management |
| **llm-application-dev** | LLM app development patterns | hybrid-search-implementation |

**Placement criteria:**
1. Domain specificity: Does the skill fit an existing plugin's theme?
2. Reusability: Is it general enough for sys-core?
3. Specialization: Does it require specific infrastructure?

**If no existing plugin fits:**
- Consider if a new plugin category is warranted
- Default to project-level (`.claude/skills/`) for user-specific skills

## Phase 6: Skill Design

Based on all research, design the skill with:

**Frontmatter:**
- `name`: lowercase-kebab-case, 3-64 chars, matches directory
- `description`: 3rd person, follows pattern `{CAPABILITY}. Use when {TRIGGERS}.`
- `allowed-tools`: Minimum required tools (security)
- Optional: `user-invocable: false`, `context: fork`, `disable-model-invocation: true`

**SKILL.md structure:**
1. **Core instructions** (< 100 lines): Immediate procedures
2. **Resource links**: References to `references/*.md`
3. **Script calls**: Zero-context execution via `scripts/`

**Progressive disclosure:**
- Keep `SKILL.md` < 500 lines
- Move deep theory to `references/theory.md`
- Move examples to `examples/` or `references/examples.md`
- Move templates to `assets/templates/`

## Phase 7: Implementation

**Create directory structure:**
```bash
mkdir -p plugins/<plugin>/skills/<skill-name>/{references,assets,scripts}
```

**Write files:**
1. `SKILL.md` - Entry point with frontmatter
2. `references/` - Domain knowledge, specs, workflows
3. `assets/templates/` - Reusable templates (if applicable)
4. `scripts/*.py` - Deterministic logic (if applicable)

**Naming validation:**
- Name regex: `^[a-z][a-z0-9-]{2,49}$`
- No underscores, no consecutive hyphens
- Directory name matches `name` field

## Phase 8: Validation

Run validation to ensure standards compliance:

```bash
uv run scripts/toolkit.py
```

**Fix any reported issues:**
- Name format violations
- Description format issues
- Missing required fields
- Path traversal violations
- Broken internal links

## Phase 9: Command Shortcut (Optional but Recommended)

Create a companion command for easy invocation at `plugins/<plugin>/commands/<skill-name>.md`:

```yaml
---
description: "Quick access to <skill-name> functionality"
argument-hint: "[optional args]"
allowed-tools: [Skill(<skill-name>)]
disable-model-invocation: true
---

# <Skill Name> Command

Invoke Skill(<skill-name>) with "$ARGUMENTS".
```

## Phase 10: Summary Report

Provide the user with:

```
Created: <skill-name>
Location: plugins/<plugin>/skills/<skill-name>/SKILL.md
Type: <archetype> (Procedural/Qualitative/Migration/Zero-Context)
Description: <description text>
Command: /<plugin>:<skill-name> (if created)

Files created:
- SKILL.md (<n> lines)
- references/*.md (<n> files)
- (other files)

Validation: PASSED

Next steps:
1. Test the skill: /<plugin>:<skill-name> <test-case>
2. Review documentation: docs/guides/skills.md
3. Iterate based on usage
```

## Critical Reminders

- **NO relative path traversal**: Never use `../` to reference other skills
- **Self-contained**: Each skill owns its references/, assets/, scripts/
- **Token efficiency**: Use scripts for deterministic logic (stdout only taxed)
- **Inline-first**: Fork only when necessary (cost: inline=1, fork=3)
- **Intent-driven**: Skills are discovered, not called procedurally
- **3rd person only**: Never use "I/me" or "you" in descriptions
- **Validate always**: Run `toolkit.py` after every edit
