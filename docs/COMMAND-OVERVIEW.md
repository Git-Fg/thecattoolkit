# Command Recipes

This document provides practical YAML examples and patterns for command development. For complete specifications, see [CLAUDE.md](../CLAUDE.md#part-ii-command-intent-layer).

---

## Complex Orchestration Example

```markdown
---
description: Orchestrate full feature development workflow
argument-hint: [feature-description]
---

# Context
!git status
!cat ROADMAP.md

# Instructions
Orchestrate the feature development workflow for: $ARGUMENTS

Phase 1: Design Analysis
- Use skill: architecture-review (context: fork)
- Analyze requirements and existing patterns

Phase 2: Implementation Planning
- Use skill: code-generator (context: fork)
- Generate implementation plan with tests

Synthesize all phases into a cohesive feature implementation.
```

---

## Command Permission Patterns

### Safe Read-Only Command

```yaml
---
description: "Analyze project structure"
allowed-tools: [Read, Grep]
permissionMode: plan
---
```

### Development Command with Safety Checks

```yaml
---
description: "Development helper for code analysis"
allowed-tools:
  - Read
  - Grep
  - Bash(npm test:*)
  - Bash(npm run build:*)
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate-dev-command.sh $TOOL_INPUT"
          timeout: 60
---
```

---

## User-Centric vs Agent-Centric Commands

### User-Centric (Interactive)

```yaml
---
description: "Interactive project scaffolding wizard"
disable-model-invocation: true
---

# Instructions
Guide the user through project setup:
1. Ask which template they want (react, vue, svelte)
2. Confirm directory structure preferences
3. Execute scaffolding based on responses
```

### Agent-Centric (Autonomous)

```yaml
---
description: "Autonomous code review for CI/CD pipelines"
allowed-tools: [Read, Grep, Glob]
permissionMode: plan
---

# Instructions
Analyze the codebase and generate a review report.
DO NOT ask questions - use best judgment for all decisions.
Output findings to stdout in JSON format.
```

### Hybrid (Conditional Interaction)

```yaml
---
description: "Deploy with optional confirmation"
---

# Instructions
Deploy the application to $ARGUMENTS environment.

If ARGUMENTS contains "force":
- Skip confirmation, proceed directly

Otherwise:
- Present deployment plan
- Request user confirmation before executing
```
