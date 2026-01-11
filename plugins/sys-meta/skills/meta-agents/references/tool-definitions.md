# Standard Tool Definitions

## Overview

Agents work with a standard set of tools. Understanding these tools is critical for proper agent configuration.

## Core Tools

### Read

**Purpose:** Read file contents

**Usage:**
```yaml
tools: [Read]  # Can read files
```

**Capabilities:**
- Read entire file
- Read with line range (offset, limit)
- Read images (visual understanding)
- Read PDFs (text extraction)

**Use Cases:**
- Analysis agents
- All agents (most need Read)

### Write

**Purpose:** Create new files or overwrite existing

**Usage:**
```yaml
tools: [Write]  # Can write files
```

**Capabilities:**
- Create new file
- Overwrite existing file completely
- No partial updates (use Edit for that)

**Use Cases:**
- Worker agents
- Generator agents

### Edit

**Purpose:** Make targeted edits to files

**Usage:**
```yaml
tools: [Edit]  # Can edit files
```

**Capabilities:**
- Replace specific text
- Multiple replacements in one call
- Preserve file structure

**Use Cases:**
- Refactoring agents
- Worker agents (fine-grained changes)

### Bash

**Purpose:** Execute shell commands

**Usage:**
```yaml
tools: [Bash]  # All commands
tools: [Bash(git:*)]  # Only git commands
tools: [Bash(npm:test)]  # Only npm test
```

**Capabilities:**
- Execute any shell command
- Capture output
- Return exit codes

**Restrictions:**
- Can restrict to specific commands: `Bash(command:*)`
- Use parentheses syntax: `Bash(git:*)`, NOT `Bash[git]`

**Use Cases:**
- Build/deploy agents
- Worker agents
- Automation agents

### Glob

**Purpose:** Find files by pattern

**Usage:**
```yaml
tools: [Glob]  # Can search for files
```

**Capabilities:**
- Pattern-based file search
- Recursive directory search
- Fast path discovery

**Use Cases:**
- Analysis agents
- Discovery agents

### Grep

**Purpose:** Search file contents

**Usage:**
```yaml
tools: [Grep]  # Can search contents
```

**Capabilities:**
- Regex pattern search
- Multiple file search
- Content filtering

**Use Cases:**
- Analysis agents
- Audit agents

## Special Tools

### Task

**Purpose:** Spawn subagents

**Usage:**
```yaml
tools: [Task]  # Can spawn agents
```

**Capabilities:**
- Launch parallel agents
- Background execution
- Independent context

**Use Cases:**
- Director agents
- Orchestrator agents

**Note:** Increases cost (2×N for N agents)

### AskUserQuestion

**Purpose:** Interact with user

**Usage:**
```yaml
tools: [AskUserQuestion]  # Can prompt user
```

**Capabilities:**
- Present options to user
- Collect user input
- Get confirmation

**Critical:** NEVER use in background agents (will hang)

**Use Cases:**
- Director agents
- Wizard commands
- Interactive agents

### TodoWrite

**Purpose:** Manage task lists

**Usage:**
```yaml
tools: [TodoWrite]  # Can track progress
```

**Capabilities:**
- Create task lists
- Update task status
- Track progress

**Use Cases:**
- Worker agents (multi-step tasks)
- Planning agents

## Tool Combinations

### Read-Only Agent

```yaml
tools: [Read, Glob, Grep]
```

**Purpose:** Analysis without modification
**Use Cases:** Code review, security audit, exploration

### Standard Worker

```yaml
tools: [Read, Write, Edit, Bash, Glob, Grep]
```

**Purpose:** Full engineering capabilities
**Use Cases:** Implementation, refactoring, building

### Background Worker

```yaml
tools: [Read, Write, Edit, Bash, Glob, Grep, TodoWrite]
# NO AskUserQuestion
```

**Purpose:** Autonomous execution
**Use Cases:** Long-running tasks, parallel work

### Director

```yaml
tools: [Task, AskUserQuestion, Read, Write, Edit]
```

**Purpose:** Coordination and delegation
**Use Cases:** Project management, workflow orchestration

## Tool Restriction Syntax

### Correct Syntax (Parentheses)

```yaml
tools: [Bash(git:*)]  # Correct
tools: [Bash(npm:test)]  # Correct
tools: [Bash(python:scripts/*.py)]  # Correct
```

### Incorrect Syntax (Brackets)

```yaml
tools: [Bash[git]]  # WRONG
tools: [Bash[python, npm]]  # WRONG
```

## Best Practices

1. **Whitelist, don't blacklist:** Specify what IS allowed, not what isn't
2. **Match agent purpose:** Don't give capabilities the agent doesn't need
3. **Consider security:** More tools = more potential for damage
4. **Background safety:** No `AskUserQuestion` in background agents
5. **Test restrictions:** Verify tool restrictions work as expected

## Quick Reference

| Tool | Purpose | Restrictable | Background Safe |
|:-----|:--------|:------------:|:---------------:|
| Read | Read files | No | ✓ |
| Write | Write files | No | ✓ |
| Edit | Edit files | No | ✓ |
| Bash | Execute commands | Yes | ✓ |
| Glob | Find files | No | ✓ |
| Grep | Search contents | No | ✓ |
| Task | Spawn agents | No | ✓ |
| AskUserQuestion | Prompt user | No | ✗ |
| TodoWrite | Track tasks | No | ✓ |
