# Command Recipes

This document provides practical YAML examples and patterns for command development. For complete specifications, see [CLAUDE.md](../CLAUDE.md#part-ii-command-intent-layer).

**Complex Orchestration Reference:** [GOLD_STANDARD_COMMAND.md](GOLD_STANDARD_COMMAND.md) - Full 7-phase workflow example.

---

## Orchestration Prompting Patterns

Commands instruct Claude using natural language prompts, not XML parsing.

### Single Agent Delegation

```
Launch an agent to analyze the authentication flow in src/auth/.
The agent should identify security vulnerabilities and report findings.
```

### Parallel Swarm Execution

```
Launch 4 agents in parallel to:
- Agent 1: Audit src/api/ for input validation
- Agent 2: Audit src/auth/ for session handling  
- Agent 3: Audit src/db/ for SQL injection
- Agent 4: Audit src/utils/ for unsafe operations

Each agent reports independently. Synthesize findings after all complete.
```

### Context Injection

```
Here is the current project brief:
[content of BRIEF.md]

Analyze the codebase against these requirements.
```

> **Key Insight:** Claude natively understands "launch X agents in parallel" instructions. No special syntax required.

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
