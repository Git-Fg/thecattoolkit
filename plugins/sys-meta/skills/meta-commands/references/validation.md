# Command Validation Checklist

## Frontmatter Validation

### Required Fields

- [ ] **description** field exists
  - [ ] 1-1024 characters
  - [ ] Single line only (no `>` or `|` YAML syntax)
  - [ ] Describes what the command does
  - [ ] Indicates expected outcome

### Optional Fields

- [ ] **argument-hint** (if specified)
  - [ ] Short and descriptive (1-10 words)
  - [ ] Indicates what argument is expected
  - [ ] Uses angle brackets for optional: `<name>`
  - [ ] No newlines or multi-line text

- [ ] **allowed-tools** (if specified)
  - [ ] Valid tool names
  - [ ] Correct array syntax
  - [ ] Skills listed in execution order
  - [ ] No invalid tool restrictions

- [ ] **disable-model-invocation** (if specified)
  - [ ] Boolean value (true or false)
  - [ ] Set appropriately for command type
  - [ ] Documented why this setting was chosen

## Structure Validation

- [ ] Command file exists in `commands/` directory
- [ ] Filename uses kebab-case
- [ ] Filename is descriptive (verb or object)

## Content Quality

### Command Body

- [ ] Clear purpose statement
- [ ] Defined workflow or procedure
- [ ] Expected output specified
- [ ] Error handling defined
- [ ] Constraints documented

### Orchestration (if applicable)

- [ ] Skills listed in execution order
- [ ] Dependencies between steps documented
- [ ] Error handling specified (abort/continue)
- [ ] Rollback procedure defined (if applicable)
- [ ] State management considered

### User Interaction (if applicable)

- [ ] `AskUserQuestion` usage appropriate
- [ ] `argument-hint` set for interactive commands
- [ ] Questions consolidated (not scattered)
- [ ] Clear options presented to users

## Retention Validation

- [ ] `disable-model-invocation` set correctly
  - [ ] `true` for human-only shortcuts
  - [ ] `true` for interactive wizards
  - [ ] `false` for AI-invoked analysis tools
  - [ ] `false` for frequently-used orchestrators

- [ ] Rationale documented for retention setting
  - [ ] Why is this command zero-retention or not?
  - [ ] Would AI benefit from autonomous access?

## Common Violations

| Issue | Fix | Severity |
|:------|:-----|:---------|
| Missing description | Add description field | **CRASH** |
| Multi-line description | Rewrite to single line | **CRASH** |
| Vague argument-hint | Make specific | Warning |
| Wrong allowed-tools syntax | Fix array format | Warning |
| Orchestration without `allowed-tools` | Add skill list | Warning |
| Wizard without `disable-model-invocation` | Add field | Warning |
| Analysis tool with `disable-model-invocation: true` | Remove field | Warning |

## Pattern Validation

### Wrapper Pattern

- [ ] Single skill in `allowed-tools`
- [ ] Clear relationship to wrapped skill
- [ ] Adds value (shortcut, alias, convenience)
- [ ] Not redundant with skill invocation

### Orchestrator Pattern

- [ ] Multiple skills/tools listed
- [ ] Execution order documented
- [ ] Dependencies specified
- [ ] Error handling defined
- [ ] State management considered

### Wizard Pattern

- [ ] `AskUserQuestion` used
- [ ] `argument-hint` set
- [ ] `disable-model-invocation: true` set
- [ ] Questions consolidated
- [ ] Clear phase structure

## Integration Validation

- [ ] Referenced skills exist
- [ ] Skill names match `name` fields
- [ ] No circular dependencies
- [ ] Compatible with `meta-skills` standards
- [ ] Compatible with `meta-agents` patterns

## Validation Commands

**Manual validation:**
```bash
# Check command file exists
ls commands/command-name.md

# Validate YAML frontmatter
grep -A 10 '^---' commands/command-name.md

# Check description length
grep '^description:' commands/command-name.md | cut -d'"' -f2 | wc -c

# Verify referenced skills exist
grep "Skill(" commands/command-name.md | sed 's/.*Skill(\(.*\)).*/\1/' | xargs -I {} find plugins -name "{}"
```
