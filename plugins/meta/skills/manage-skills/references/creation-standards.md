# Skill Creation Standards

## Overview

This document defines the standards for creating new Cat Toolkit skills. These standards ensure consistency, portability, and maintainability across all skills.

## Naming Standards

### Skill Name Rules

- **Format:** `lowercase-with-hyphens` (kebab-case)
- **Length:** Maximum 64 characters
- **Matching:** Must match directory name exactly
- **Prefixes:** Use descriptive prefixes like `create-*`, `manage-*`, `setup-*`, `generate-*`, `build-*`

### Naming Decision Logic

| Context | Naming Pattern |
|---------|---------------|
| Task execution | `{action}-{object}` (e.g., `process-pdfs`, `validate-input`) |
| Lifecycle management | `manage-{component}` (e.g., `manage-skills`, `manage-commands`) |
| Knowledge base | `{domain}-patterns` or `{domain}-expertise` (e.g., `react-patterns`) |
| Planning | `create-{artifact}` (e.g., `create-plans`, `create-prompts`) |

## Directory Structure Standards

### Default: Project-Level

**Location:** `.claude/skills/{skill-name}/`
**Advantages:** Portable, version-controlled, team-shared

```bash
# For simple skills
mkdir -p .claude/skills/{skill-name}

# For router pattern skills
mkdir -p .claude/skills/{skill-name}/workflows
mkdir -p .claude/skills/{skill-name}/references

# For skills with output structures
mkdir -p .claude/skills/{skill-name}/templates

# For skills with reusable code
mkdir -p .claude/skills/{skill-name}/scripts
```

### Alternative: User-Level

**Location:** `~/.claude/skills/{skill-name}/`
**Use case:** Only if explicitly requested for global availability

## Template Selection Standards

### Template Decision Matrix

| Condition | Template |
|-----------|----------|
| Single workflow, under 200 lines | `minimal.md` |
| Action-oriented task execution | `task-execution.md` |
| 4+ distinct workflows requiring routing | `router-pattern.md` |
| Exhaustive domain knowledge with full lifecycle | `domain-expertise.md` |
| Detailed knowledge in separate references | `progressive-disclosure.md` |

### Template Selection Logic

```
IF single workflow + minimal knowledge
  → Use `minimal.md` template

ELIF action-oriented task execution
  → Use `task-execution.md` template

ELIF 4+ distinct workflows requiring routing
  → Use `router-pattern.md` template

ELIF exhaustive domain knowledge covering full lifecycle
  → Use `domain-expertise.md` template

ELIF detailed knowledge in separate references
  → Use `progressive-disclosure.md` template
```

## Context Hydration Standards

### Pre-Creation Analysis

Before generating any skill, perform the following analysis:

**1. Scan Existing Ecosystem**

```bash
# Identify similar skills that might overlap
find .claude/skills -name "*.md" -type f
find ~/.claude/skills -name "*.md" -type f 2>/dev/null || true
```

**2. Analyze Existing Patterns**

- Read 2-3 existing SKILL.md files
- Identify structural patterns (simple vs router)
- Note naming conventions and description styles

**3. Identify Dependencies**

- Tool/permission patterns in similar skills
- MCP server references
- Related slash commands

**4. Clarify Intent**

- Problem this skill solves
- Relationship to existing functionality
- Whether refactoring vs new creation

## Description Generation Standards

### Standardized Formula

**Formula:** `{Action Verb} + {Trigger} + {Purpose}`

### Vocabulary Standards

- **Prefixes:** "Invoke this skill when..." OR "Use this skill to..."
- **Action verbs:** Create, Manage, Analyze, Debug, Review, Design, Plan, Execute
- **Strong language:** MUST USE / PROACTIVELY INVOKE / CONSULT

### Description Examples

```
description: Create, audit, and maintain AI agent skills. MUST BE INVOKED when working with SKILL.md files, authoring new skills, improving existing skills, or understanding skill structure and best practices.

description: Strategic Thinking Specialist. PROACTIVELY USE when deep reasoning, strategic analysis, or framework-based problem solving requires isolated context.
```

### Generation Steps

1. Identify primary action (verb)
2. Define specific triggers (when to use)
3. Apply strong language (MUST USE/PROACTIVELY)
4. Format: "{Action} + {Triggers}. {Strong language} {Purpose}"

## YAML Frontmatter Standards

### Required Fields

```yaml
---
name: skill-name          # lowercase-with-hyphens, max 64 chars
description: ...          # Max 1024 chars, third person
---
```

### Optional Fields

```yaml
---
allowed-tools: [Read, Write, Edit, Bash]  # Tools to pre-approve
---
```

### Validation Requirements

- [ ] YAML frontmatter valid
- [ ] Name matches directory (lowercase-with-hyphens)
- [ ] Description uses strong language with specific triggers
- [ ] Description includes both what it does AND when to use it
- [ ] Third-person perspective ("Use this skill when..." not "I will help...")

## Domain Expertise Skills

### Critical Distinction

- **Regular skill:** "Do one specific task"
- **Domain expertise skill:** "Do EVERYTHING in this domain, with complete practitioner knowledge"

### Domain Examples

- macOS/iOS app development
- Python game development
- Rust systems programming
- Machine learning / AI
- Web scraping and automation
- Data engineering pipelines
- Audio processing / DSP
- 3D graphics / shaders
- Unity/Unreal game development
- Embedded systems

### Domain Expertise Structure

Domain expertise skills are generated into USER-SPACE paths only:

**Project-level** (default, recommended): `.claude/skills/expertise/{domain-name}/`
- Portable with the project
- Shared with team via version control
- Available only in this project

**User-level** (if explicitly specified): `~/.claude/skills/expertise/{domain-name}/`
- Available across all your projects
- Use only for personally useful domains

### Full Lifecycle Coverage

Domain expertise skills should cover:

1. **build-new-{thing}.md** - Create from scratch
2. **add-feature.md** - Extend existing {thing}
3. **debug-{thing}.md** - Find and fix bugs
4. **write-tests.md** - Test for correctness
5. **optimize-performance.md** - Profile and speed up
6. **ship-{thing}.md** - Deploy/distribute

## Companion Slash Command Generation

### Auto-Generation Criteria

Generate a companion slash command when:

- Skill is task-oriented (not just knowledge/reference)
- Skill solves a common problem
- Skill name is short and memorable
- Skill is frequently used

### Command Generation Standards

**File:** `.claude/commands/{skill-name}.md`

```yaml
---
description: Shortcut to invoke the {skill-name} skill for {purpose}
argument-hint: [{argument hint}]
disable-model-invocation: true
---

Invoke the `{skill-name}` skill to {action}: $ARGUMENTS
```

### Command Pattern Standards

- **Semantic category:** Objects (Thing names)
- **Language:** "Shortcut to invoke the {skill} skill..."
- **Body:** "Invoke the `{skill}` skill to {action}: $ARGUMENTS"
- **Max 2 lines** after frontmatter

## File Generation Order

**Standard sequence:**

1. Create directory structure
2. Generate SKILL.md with YAML frontmatter
3. Populate references/ based on template requirements
4. Create templates/ if output structures are needed
5. Create scripts/ if executable code is needed
6. Create workflows/ if using router pattern

## Verification Standards

All generated skills MUST pass:

- [ ] Architectural template selected from `assets/templates/`
- [ ] Context hydrated through ecosystem scan
- [ ] Requirements acquired through appropriate logic gates
- [ ] API research completed (if external service involved)
- [ ] Description generated using standardized formula
- [ ] Directory structure created
- [ ] Content generated from selected template
- [ ] Validation checklist passed
- [ ] Companion slash command created (if applicable)
- [ ] Verification completed
