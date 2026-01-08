# Semantic Command Categories

## Overview

Cat Toolkit uses **semantic naming** to make command purposes immediately clear. This creates cognitive affordances - users can predict command behavior based on naming patterns.

## The Four Categories

### 1. Verbs (Action Words)
**Interface:** Load
**Purpose:** Load skills into main chat

**Pattern:**
```markdown
---
description: Shortcut to load the {skill} skill for {purpose}
argument-hint: [{input description}]
---

Load the `{skill}` skill to {action}: $ARGUMENTS
```

**Examples:**
- `/think` - Load thinking frameworks
- `/debug` - Load engineering (debugging)
- `/review` - Load engineering (review)
- `/system-design` - Load engineering (architecture)
- `/sync-rules` - Load sync-rules skill

**When to Use:**
- Loading a skill into the current conversation
- The skill provides the knowledge and workflows
- User wants to use the skill directly in the main chat

### 2. Personas (Role Names)
**Interface:** Delegate
**Purpose:** Delegate to specialized subagents via explicit commands

**Pattern:**
```markdown
---
description: [Personas] Delegate to {agent-name} for {purpose}
allowed-tools: Task, Read, Glob, Grep
argument-hint: [{task description}]
disable-model-invocation: true
---

Delegate to the {agent-name} agent: $ARGUMENTS

This provides {benefit}.

Important: The context provided to the subagent must be exhaustive and cover all relevant information. It starts with a fully-clean slate - it's better to give it too much context than not enough.
```

**Note:** These are user-centric wrapper commands. The AI can already delegate to any subagent directly, so these commands exist as convenient shortcuts for human users. They should have `disable-model-invocation: true` to prevent programmatic invocation.

**Examples:**
- `/brainstorm [task]` - Delegate to brainstormer agent for strategic thinking
- `/prompt-engineer [task]` - Delegate to prompt-engineer for prompt optimization
- `/expert [task]` - Delegate to plugin-expert for system maintenance

**When to Use:**
- Need a specialized subagent with isolated context
- Keep main chat clean
- Provide focused expertise
- Enable deep, uninterrupted analysis

**Key Principle:** Explicit persona commands provide type-safe routing and better discoverability

### 3. Objects (Thing Names)
**Interface:** Load
**Purpose:** Lifecycle management for toolkit components

**Pattern:**
```markdown
---
description: Shortcut to load the {skill} skill for {purpose}
argument-hint: [{input description}]
---

Load the `{skill}` skill to {action}: $ARGUMENTS
```

**Examples:**
- `/build` - Lifecycle manager for toolkit components (create/audit agents, skills, commands, hooks)
- `/create-plan` - Load manage-planning skill

**When to Use:**
- Creating or managing toolkit components
- The command triggers a skill workflow
- Component lifecycle operations (create, update, audit, etc.)

### 4. Execution (Runners)
**Interface:** Execute
**Purpose:** Run existing artifacts

**Pattern:**
```markdown
---
description: Shortcut to load the {skill} skill for {purpose}
argument-hint: [{input description}]
---

Load the `{skill}` skill to {action}: $ARGUMENTS
```

**Examples:**
- `/run-plan` - Execute PLAN.md
- `/run-prompt` - Execute saved prompt

**When to Use:**
- Running existing artifacts (plans, prompts, etc.)
- Executing pre-created workflows
- Processing saved configurations

## Quick Decision Guide

| What are you trying to do? | Category | Pattern |
|---------------------------|----------|---------|
| Load a skill into main chat | **Verbs** | "Load the..." |
| Delegate to a specialized agent | **Personas** | "Delegate to the {agent} agent..." |
| Create a toolkit component | **Objects** | "Load the {skill} skill..." |
| Run an existing artifact | **Execution** | "Execute {artifact}..." |

## Description Templates

### Verbs
```
"Shortcut to load the {skill} skill for {purpose}"
```

### Personas
```
"[Personas] Delegate to {agent-name} for {purpose}"
```

### Objects
```
"Shortcut to load the {skill} skill for {purpose}"
```

### Execution
```
"Shortcut to load the {skill} skill for executing {artifact}"
```

## Best Practices

### DO:
- Use semantic naming based on the action
- Keep descriptions soft and human-friendly
- Focus on what the user wants to accomplish
- Use "shortcut to load" language for Verbs/Objects/Execution
- Use "Delegate to" for Personas
- Make the purpose immediately clear

### DON'T:
- Mix semantic categories in one command
- Use technical jargon in descriptions
- Make descriptions verbose or complex
- Use generic names like "create" or "build" without context
- Create commands that don't fit clearly into one category

## Examples by Category

### Verbs Examples

**Loading Engineering Skill:**
```markdown
---
description: Shortcut to load the engineering skill for debugging and bug fixing
argument-hint: [error description]
---

Load the `engineering` skill (debugging workflow) and investigate: $ARGUMENTS
```

**Loading Thinking Frameworks:**
```markdown
---
description: Shortcut to load the thinking-frameworks skill for strategic decision making
argument-hint: [topic or question]
---

Load the `thinking-frameworks` skill to analyze: $ARGUMENTS
```

### Personas Examples

**Delegating to Brainstormer:**
```markdown
---
description: [Personas] Delegate to brainstormer for strategic thinking and framework-based analysis
allowed-tools: Task, Read, Glob, Grep
argument-hint: [problem or task to analyze]
disable-model-invocation: true
---

Delegate to the brainstormer agent: $ARGUMENTS

This leverages strategic thinking expertise to break down complex problems and explore multiple solution pathways.

Important: The context provided to the subagent must be exhaustive and cover all relevant information. It starts with a fully-clean slate - it's better to give it too much context than not enough.
```

**Delegating to Prompt Engineer:**
```markdown
---
description: [Personas] Delegate to prompt-engineer for prompt optimization and design
allowed-tools: Task, Read, Glob, Grep
argument-hint: [prompt or task requiring prompt engineering]
disable-model-invocation: true
---

Delegate to the prompt-engineer agent: $ARGUMENTS

This applies advanced prompt engineering techniques to create high-quality, optimized prompts.

Important: The context provided to the subagent must be exhaustive and cover all relevant information. It starts with a fully-clean slate - it's better to give it too much context than not enough.
```

**Delegating to Plugin Expert:**
```markdown
---
description: [Personas] Delegate to expert for system maintenance and infrastructure
allowed-tools: Task, Read, Glob, Grep
argument-hint: [maintenance or audit task]
disable-model-invocation: true
---

Delegate to the plugin-expert agent: $ARGUMENTS

This provides system maintenance expertise for auditing, creating, or fixing AI components (agents, skills, commands).

Important: The context provided to the subagent must be exhaustive and cover all relevant information. It starts with a fully-clean slate - it's better to give it too much context than not enough.
```

### Objects Examples

**Creating a Skill:**
```markdown
---
description: Shortcut to load the manage-skills skill for creating AI agent skills
argument-hint: [skill-name or description]
---

Load the `manage-skills` skill to create a skill for: $ARGUMENTS
```

**Creating a Hook:**
```markdown
---
description: Shortcut to load the manage-hooks skill for creating automation hooks
argument-hint: [hook-type or description]
---

Load the `manage-hooks` skill to create hooks for: $ARGUMENTS
```

### Execution Examples

**Running a Plan:**
```markdown
---
description: Shortcut to load the manage-planning skill for executing project plans
argument-hint: [plan-path]
---

Load the `manage-planning` skill (run-plan workflow) to execute: $ARGUMENTS
```

**Running a Plan:**
```markdown
---
description: Shortcut to load the manage-planning skill for executing saved plans
argument-hint: [plan-name or path]
---

Load the `manage-planning` skill to run the plan at: $ARGUMENTS
```

## Summary

**Semantic Categories** make commands predictable:
- **Verbs** → Load skills
- **Personas** → Delegate to subagents
- **Objects** → Manage components
- **Execution** → Run artifacts

Choose the category that best matches the command's purpose, then follow the pattern for that category.
