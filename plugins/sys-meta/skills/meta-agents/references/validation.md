# Agent Validation Checklist

## Frontmatter Validation

### Required Fields

- [ ] **name** field exists
  - [ ] 1-64 characters
  - [ ] Lowercase, alphanumeric, hyphens only
  - [ ] No consecutive hyphens
  - [ ] No leading/trailing hyphens

### Optional Fields

- [ ] **description** field exists (highly recommended)
  - [ ] 1-1024 characters
  - [ ] Single line
  - [ ] Uses modal + trigger pattern
  - [ ] Clear about agent's purpose

- [ ] **tools** field exists (**CRITICAL**)
  - [ ] NOT omitted (security risk if omitted)
  - [ ] Explicit whitelist of tools
  - [ ] Tool names are valid
  - [ ] Syntax is correct (parentheses for restrictions)

- [ ] **skills** field exists (if needed)
  - [ ] Skill names are valid
  - [ ] Skills exist in toolkit
  - [ ] No circular dependencies

- [ ] **permissionMode** (if specified)
  - [ ] Valid value (plan, acceptEdits, default, etc.)
  - [ ] Appropriate for agent type
  - [ ] Consider using runtime default instead

## Security Validation

### Tool Whitelist

- [ ] **tools** field is specified
- [ ] Tools match agent purpose
- [ ] No unnecessary tools included
- [ ] Tool restrictions use correct syntax
- [ ] `Bash(command:*)` NOT `Bash[command]`

### Background Safety

- [ ] If background agent:
  - [ ] NO `AskUserQuestion` in tools
  - [ ] Error handling defined
  - [ ] Timeout strategy documented
  - [ ] Autonomous decision making

### Permission Mode

- [ ] **Omit** `permissionMode` (use runtime default)
- [ ] If specified:
  - [ ] Valid value
  - [ ] Matches agent type
  - [ ] Document why override needed

## Persona Validation

### Clear Role Definition

- [ ] Agent purpose is clear
- [ ] Role is distinct from other agents
- [ ] Constraints are documented
- [ ] Behavioral standards referenced

### Appropriate Tools

- [ ] Tools match persona needs
- [ ] No tool creep (unnecessary tools)
- [ ] Tool restrictions appropriate

### Skill Bindings

- [ ] Skills are relevant to agent role
- [ ] No conflicting skills
- [ ] Skills exist in toolkit
- [ ] Skill dependencies are satisfied

## Common Violations

| Issue | Fix | Severity |
|:------|:-----|:---------|
| Missing `tools` field | Add explicit tool whitelist | **CRITICAL** |
| `AskUserQuestion` in background agent | Remove from tools | **CRITICAL** |
| Wrong tool restriction syntax | Use `Bash(cmd:*)` not `Bash[cmd]` | **CRASH** |
| Over-permissive analyst | Remove Write/Edit/Bash | Warning |
| Unclear agent role | Clarify purpose and constraints | Warning |
| `permissionMode` hardcoded | Omit field, use runtime default | Warning |

## Pattern-Specific Validation

### Worker Agent

- [ ] `tools: [Read, Write, Edit, Bash, Glob, Grep]` (or similar)
- [ ] NO `AskUserQuestion` in tools
- [ ] `skills: [execution-core, software-engineering]` (or similar)
- [ ] UNINTERRUPTED FLOW constraints documented
- [ ] Self-verification requirements specified

### Analyst Agent

- [ ] `permissionMode: plan` (or similar read-only mode)
- [ ] `tools: [Read, Glob, Grep]` (read-only only)
- [ ] NO Write/Edit/Bash tools
- [ ] Clear read-only constraints
- [ ] Domain skills included if needed

### Director Agent

- [ ] `tools: [Task, AskUserQuestion, Read, Write, Edit]` (or similar)
- [ ] Can spawn workers via Task
- [ ] Can interact with user
- [ ] Coordination patterns documented
- [ ] Prompt engineering referenced

### Background Agent

- [ ] NO `AskUserQuestion` in tools
- [ ] Autonomous decision making documented
- [ ] Error handling defined
- [ ] Timeout strategy specified
- [ ] Checkpoint capability for long tasks

### Specialist Agent

- [ ] Domain-specific skills included
- [ ] Tools focused on domain
- [ ] Domain constraints documented
- [ ] Expertise boundaries defined

## Validation Commands

**Manual validation:**
```bash
# Check agent file exists
ls agents/agent-name.md

# Validate YAML frontmatter
grep -A 20 '^---' agents/agent-name.md

# Check for tools field
grep '^tools:' agents/agent-name.md

# Check for AskUserQuestion in background agents
grep -l 'AskUserQuestion' agents/background-*.md  # Should be empty

# Verify tool syntax
grep 'Bash\[' agents/*.md  # Should find nothing (wrong syntax)
```

## Integration Validation

- [ ] Referenced skills exist
- [ ] Skill names match `name` fields
- [ ] No circular dependencies
- [ ] Compatible with execution-core standards
- [ ] Compatible with software-engineering quality

## Security Audit Checklist

- [ ] `tools` field specified for all agents
- [ ] Background agents have NO `AskUserQuestion`
- [ ] Tool restrictions use correct syntax
- [ ] `permissionMode` omitted (uses runtime default)
- [ ] Agent permissions match task requirements
- [ ] No over-permissive configurations
- [ ] Error handling prevents privilege escalation
