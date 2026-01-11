# Command Syntax

## Frontmatter Fields

### Required Fields

#### `description` (Required)
- **Constraints:** 1-1024 characters
- **Purpose:** Describe what the command does
- **Best Practice:** Include action and outcome
- **Example:** `"Execute complete release workflow with validation"`

### Optional Fields

#### `argument-hint`
- **Purpose:** Brief hint for autocomplete/usage
- **Constraints:** Should be short (1-10 words)
- **Shown:** In `/` menu autocomplete
- **Example:** `"Optional configuration name"`

#### `allowed-tools`
- **Purpose:** Restrict which tools the command can use
- **Syntax:** Array of tool names
- **Common values:**
  - `[Skill(skill-name)]` - Force skill invocation
  - `[Task, Read, Write]` - Allow agent spawning
  - `[Bash(git:*)]` - Restrict Bash to git commands

**Examples:**
```yaml
# Single skill
allowed-tools: [Skill(audit-security)]

# Multiple skills
allowed-tools: [Skill(build), Skill(test), Skill(deploy)]

# With agent spawning
allowed-tools: [Skill(manage-planning), Task]

# Bash-restricted
allowed-tools: [Read, Write, Bash(git:*), Bash(npm:*)]
```

#### `disable-model-invocation`
- **Purpose:** Exclude from tool definitions (zero token retention)
- **Values:** `true` or `false` (default: `false`)
- **Effect when `true`:**
  - Command NOT in AI's system prompt
  - AI cannot invoke autonomously
  - Human can still invoke via `/command`

**When to use:**
- Heavy playbooks (complex workflows)
- Human-only shortcuts
- Interactive wizards

**When NOT to use:**
- Commands the AI needs for gathering information
- Analysis tools

## Dynamic Context

Commands can include dynamic context from the system using special syntax.

### Command Output Capture

Execute a command and use its output:
```yaml
---
description: "Deploy with current branch"
---

# Deploy Workflow

Deploy current branch:
```bash
! git branch --show-current
```

This runs `git branch --show-current` and injects the output into the prompt.

**Deployment for branch:** [output from command]
```

### Argument Substitution

Access user arguments:
```markdown
**User Request:** "$ARGUMENTS"

**Processing:** [handle $ARGUMENTS]
```

### Positional Arguments

Access specific arguments by position:
```markdown
**First Argument:** "$1"
**All Arguments:** "$@" or "$ARGUMENTS"
```

## Body Structure

Command bodies use Markdown for instructions.

### Section Pattern

```markdown
# [Command Name] Header

Brief description of what this command does.

## Goal
[What the command accomplishes]

## Workflow
1. **Step 1:** [Action]
2. **Step 2:** [Action]
3. **Step 3:** [Action]

## Output
[Expected result]
```

### Constraint Pattern

```markdown
## Constraints

- **Abort on error:** [Condition]
- **Require confirmation:** [Condition]
- **Skip:** [Condition]
```

## Examples

### Simple Wrapper with Argument

```yaml
---
description: "Quick grep search"
argument-hint: "<search pattern>"
allowed-tools: [Grep, Bash]
---

# Grep Shortcut

Search codebase for pattern: "$ARGUMENTS"

**Usage:** `/grep "search term"`

**Output:** Matching files and line numbers
```

### Orchestrator with Dynamic Context

```yaml
---
description: "Deploy current branch to staging"
allowed-tools: [Bash, Skill(deploy)]
---

# Deploy to Staging

Deploying current branch to staging environment.

**Current Branch:** ! git branch --show-current
**Latest Commit:** ! git log -1 --format='%h %s'

## Workflow
1. Run tests
2. Build artifacts
3. Deploy to staging
4. Verify deployment
```

### Wizard with Argument Hint

```yaml
---
description: "Interactive project setup"
argument-hint: "<project name> or template"
disable-model-invocation: true
---

# Setup Wizard

Interactive project setup.

## Input
User provided: "$ARGUMENTS"

If no argument provided, prompt for:
- Project name
- Template selection

## Workflow
1. Gather requirements via AskUserQuestion
2. Generate project structure
3. Initialize version control
4. Install dependencies
```
