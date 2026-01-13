# Skill Creation Workflow Details

In-depth explanation of each phase in the skill creation process.

## Phase 1: Documentation Research (docs/)

**Purpose**: Understand Cat Toolkit architecture before designing.

**Read order matters**:
1. `docs/guides/skills.md` - Understand 4 skill archetypes
2. `docs/guides/commands.md` - Know when to use Commands vs Skills
3. `docs/REFERENCES.md` section 3.1 - Component selection matrix

**Key concepts to extract**:

**Skill Archetypes** (from skills.md):
1. **Procedural**: Step-by-step workflows (e.g., Release Process)
2. **Qualitative**: Design/style patterns (e.g., CSS Guidelines)
3. **Migration**: API translation (e.g., v1 → v2)
4. **Zero-Context**: Tool wrappers (scripts only)

**Component Selection**:
- **Skill**: Knowledge, frameworks, protocols
- **Command**: Workflows, orchestration triggers
- **Agent**: High volume, isolation needs

## Phase 2: Meta-Skill Investigation

**Purpose**: Understand creation standards and templates.

**Read**: `plugins/sys-core/skills/meta-skill/SKILL.md`

**Key information to extract**:

**Template Selection**:
| Template | Use When | Complexity |
|----------|----------|------------|
| Standard | Single capability, straightforward | Low |
| Progressive | Complex domain expertise | High |
| Router | Multiple workflows/paths | Medium |
| Minimal | Internal tools, utilities | Low |
| Checklist | Task-oriented with validation | Medium |

**Naming Rules**:
- Regex: `^[a-z][a-z0-9-]{2,49}$`
- 3-64 characters
- Directory name MUST match `name` field

**Description Pattern**:
- Standard: `{CAPABILITY}. Use when {TRIGGERS}.`
- Enhanced: `{CAPABILITY}. {MODAL} Use when {TRIGGERS}.`
- Modals: MUST, PROACTIVELY, SHOULD (for internal tools)

## Phase 3: External Research

**Purpose**: Gather domain knowledge from external sources.

**GitHub Repositories**:
```bash
Use mcp__plugin_sys-research_gitingest__ask_question with:
- repoName: owner/repo (extract from URL)
- question: "What is the main purpose? Key features? Integration points?"
```

**Web Documentation**:
```bash
Use mcp__web_reader__webReader with:
- url: provided URL
- return_format: markdown
- retain_images: false
```

**General Research**:
```bash
Use mcp__plugin_sys-research_duckduckgo__search with:
- query: "Claude Code skill [domain] best practices"
- max_results: 10
```

**Synthesis Goals**:
- Core domain concepts
- Typical workflows/patterns
- Key terminology for descriptions
- Potential integration points

## Phase 4: Existing Skill Audit

**Purpose**: Avoid fragmentation and duplication.

**Search patterns**:
```bash
# Domain keyword search
Grep pattern="keyword" path="plugins/**/*.md" output_mode="files_with_matches"

# List all skills
Glob pattern="plugins/**/skills/*/"
```

**Decision criteria**:

**Extend if**:
- Existing skill has compatible scope
- New feature is natural addition
- Maintains skill coherence

**Create new if**:
- Distinct domain boundary
- Different use case triggers
- Would overcomplicate existing skill

**Consolidate if**:
- Three or more overlapping micro-skills
- Shared domain knowledge
- Clear architectural benefit

## Phase 5: Plugin Placement Strategy

**Decision Matrix**:

| Plugin | Domain | Examples | Decision Criteria |
|--------|--------|----------|-------------------|
| **sys-core** | Universal tooling | meta-skill, audit-plugins | General utility, scaffolding, validation |
| **sys-builder** | Build workflows | architecture, test-writer | Development lifecycle, planning |
| **sys-research** | External data | researcher, gitingest | APIs, data gathering, search |
| **sys-cognition** | AI/ML techniques | prompt-engineering | Reasoning, memory, context |
| **sys-multimodal** | Cross-modal | multimodal-understanding | Vision, audio, translation |
| **sys-edge** | Mobile/offline | edge-ai-management | Edge computing, mobile |

**Placement algorithm**:
1. Does it fit an existing plugin theme? → Place there
2. Is it general-purpose utility? → sys-core
3. New domain category? → Consider project-level or new plugin

## Phase 6: Skill Design

**Frontmatter Design**:

**name**: Gerund form recommended
- ✓ `processing-pdfs`, `serving-llms`, `analyzing-data`
- ✗ `pdf-processor`, `llm-server`, `data-analyzer`

**description**: Include key terms for discovery
```yaml
# Good: Specific with triggers
description: Implements hybrid search with keyword and vector queries. Use when building RAG systems, optimizing retrieval relevance, or implementing semantic search.

# Bad: Vague without triggers
description: A search implementation tool.
```

**allowed-tools**: Security whitelist
```yaml
# Minimize for security
allowed-tools: [Read, Write, Edit, Bash(npm:*)]

# Default: ALL tools (no restriction)
# Omit allowed-tools entirely
```

**SKILL.md Structure**:
1. **Header** (< 10 lines): Purpose and principles
2. **Quick Start** (20-30 lines): Immediate workflow
3. **Detailed Sections** (100-200 lines): Core procedures
4. **Resource Links** (10-20 lines): references/ pointers
5. **Checklists** (20-30 lines): Validation criteria

**Total target**: 200-300 lines

## Phase 7: Implementation

**Directory Creation**:
```bash
mkdir -p plugins/<plugin>/skills/<skill-name>/{references,assets,scripts}
```

**File Writing Order**:
1. `SKILL.md` - Entry point with frontmatter
2. `references/` - Domain knowledge files
3. `assets/templates/` - Reusable templates
4. `scripts/*.py` - Deterministic logic

**Path Standards**:
- Use relative paths from skill root: `references/file.md`
- NO traversal: `../other-skill/` (validation failure)
- Unix slashes only: `scripts/helper.py`
- Use `${CLAUDE_PLUGIN_ROOT}` for hooks

## Phase 8: Validation

**Validation Commands**:
```bash
# Full validation
uv run scripts/toolkit-analyzer.py

# Fix issues automatically
uv run scripts/toolkit-analyzer.py --fix

# Individual checks
uv run scripts/validate-skill-name.py my-skill
uv run scripts/validate-description.py ./my-skill/
```

**Common Issues**:

**Name validation**:
- Invalid characters (uppercase, underscores)
- Wrong length (< 3 or > 64)
- Reserved words (claude, anthropic)

**Description validation**:
- First person ("I can help")
- Missing "Use when" pattern
- Too long (> 1024 chars)
- XML tags present

**Link validation**:
- Broken internal links
- Traversal paths (`../`)
- Windows paths (`\`)

## Phase 9: Command Shortcut

**Purpose**: User-friendly invocation point.

**Structure**:
```yaml
---
description: "Brief description for menu"
argument-hint: "[optional] [args]"
allowed-tools: [Skill(<skill-name>)]
disable-model-invocation: true
---

# Command Name

Invoke Skill(<skill-name>) with arguments:
- $1: First argument
- $2: Second argument

Execute the skill workflow with provided context.
```

**Two-Mode Pattern** (Brain + Button):
1. **Batch mode** (`run`): No questions, use defaults
2. **Interactive mode** (`run-interactive`): AskUserQuestion for critical decisions

## Phase 10: Summary Report

**Report Template**:
```
Created: <skill-name>
Location: plugins/<plugin>/skills/<skill-name>/SKILL.md
Type: <Procedural/Qualitative/Migration/Zero-Context>
Description: <description text>
Command: /<plugin>:<skill-name> (if created)

Files created:
- SKILL.md (<n> lines)
- references/*.md (<n> files)
- scripts/*.py (<n> files)

Validation: PASSED

Next steps:
1. Test: /<plugin>:<skill-name> <test-case>
2. Review: docs/guides/skills.md
3. Iterate based on usage
```

**Success metrics**:
- All validation scripts pass
- No broken links
- Progressive disclosure achieved
- Clear user value proposition
