# Skill Directory Structure

## Required Structure

A valid skill MUST be a directory containing at minimum a `SKILL.md` file:

```
skill-name/
└── SKILL.md          # Required: metadata + instructions
```

## Enhanced Structure (Progressive Disclosure)

For complex skills, use optional directories to manage context efficiently:

```
skill-name/
├── SKILL.md          # Router (<400 lines)
├── scripts/          # Executable code
│   └── *.py, *.sh, *.js
├── references/       # Theory and standards (load on-demand)
│   ├── detailed-guide.md
│   └── examples.md
└── assets/           # Templates, resources
    └── templates/
        └── scaffold.md
```

## Directory Purposes

### `SKILL.md` (Required)

**Purpose:** High-speed router and entry point
**Size:** <400 lines recommended
**Content:**
- Quick reference tables
- Triggers for loading reference files
- Operational protocol
- Common patterns

### `scripts/` (Optional)

**Purpose:** Executable code
**Standards:**
- Self-contained or clearly documented
- Helpful error messages
- Graceful edge case handling
- Use relative paths from skill root

### `references/` (Optional)

**Purpose:** Heavy theory and detailed documentation
**Load Strategy:** On-demand only
**Content Types:**
- Technical reference material
- Domain-specific guides
- Extended examples
- Standards documentation

**When to move content to `references/`:**
- Theory exceeding 100 lines
- Reference tables and checklists
- Multi-step protocol details
- Domain-specific background

### `assets/` (Optional)

**Purpose:** Templates and resources
**Content Types:**
- Scaffold templates
- Configuration templates
- Reusable assets
- Static resources

## Naming Conventions

**Skill Directory:**
- Lowercase, hyphens only
- Must match `name` field in frontmatter
- Examples: `pdf-processing`, `data-analysis`, `code-review`

**File Names:**
- Use kebab-case for multi-word files
- Examples: `phase-plan.md`, `best-practices.md`

## Path References

Use relative paths from skill root:

```markdown
See `references/validation.md` for the full checklist.

Run the extraction script:
scripts/extract.py input.pdf output.txt

Use the template from:
assets/templates/scaffold.md
```

**Best Practice:** Keep references one level deep from SKILL.md.
