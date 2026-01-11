# Skill Validation Checklist

## Frontmatter Validation

### Required Fields

- [ ] **name** field exists
  - [ ] 1-64 characters
  - [ ] Lowercase only (no uppercase)
  - [ ] Alphanumeric and hyphens only
  - [ ] No consecutive hyphens (`--`)
  - [ ] No leading or trailing hyphens
  - [ ] Matches directory name exactly

- [ ] **description** field exists
  - [ ] 1-1024 characters
  - [ ] Single line only (no `>` or `|` YAML syntax)
  - [ ] Starts with Modal + "USE when" pattern
  - [ ] Clearly indicates when to invoke
  - [ ] Includes relevant keywords for discovery

### Optional Fields

- [ ] **allowed-tools** (if specified)
  - [ ] Valid tool names
  - [ ] Correct array syntax
  - [ ] No invalid tool restrictions

- [ ] **context** (if specified)
  - [ ] Valid value (`fork` or `inline`)
  - [ ] Used appropriately for skill type

- [ ] **user-invocable** (if specified)
  - [ ] Boolean value
  - [ ] Set appropriately (default: `true`)

## Structure Validation

- [ ] SKILL.md file exists in skill directory
- [ ] Directory name matches `name` field
- [ ] Optional directories use standard names:
  - [ ] `scripts/` (for executable code)
  - [ ] `references/` (for documentation)
  - [ ] `assets/` (for templates/resources)

## Content Quality

### SKILL.md Body

- [ ] Clear purpose statement
- [ ] Operational protocol defined
- [ ] Quick reference or summary table
- [ ] Triggers for loading reference files (if using progressive disclosure)
- [ ] Examples or common patterns
- [ ] Integration points documented

### Progressive Disclosure (if applicable)

- [ ] SKILL.md under 400 lines (recommended)
- [ ] Heavy theory in `references/`
- [ ] Reference files clearly named
- [ ] Relative paths from skill root
- [ ] Clear indication of when to load each reference

## Discovery Validation

- [ ] Description uses Modal + Trigger pattern
- [ ] Keywords match common user intents
- [ ] No ambiguous or vague language
- [ ] Specific about capabilities

### Modal Pattern Check

- [ ] `MUST USE when` - for critical internal standards
- [ ] `SHOULD USE when` - for recommended patterns
- [ ] `PROACTIVELY USE when` - for autonomous discovery
- [ ] `USE when` - for general capabilities

## Common Violations

| Issue | Fix | Severity |
|:------|:-----|:--------|
| Name contains uppercase | Rename to lowercase | **CRASH** |
| Name has underscores | Replace with hyphens | **CRASH** |
| Name doesn't match directory | Rename one to match | **CRASH** |
| Description is multi-line | Rewrite to single line | **CRASH** |
| Missing "USE when" pattern | Add modal + trigger | Warning |
| SKILL.md > 400 lines | Move theory to references/ | Warning |
| No clear operational protocol | Add protocol section | Warning |

## Validation Commands

**Using official skills-ref library:**
```bash
# Validate a skill directory
skills-ref validate <path>

# Generate available skills XML
skills-ref to-prompt <path>...
```

**Manual validation:**
```bash
# Check name matches directory
basename $(pwd) | grep -q "^$(grep '^name:' SKILL.md | cut -d' ' -f2)$"

# Check description length
grep '^description:' SKILL.md | cut -d'"' -f2 | wc -c
```
