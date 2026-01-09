# Skill Frontmatter Comparison & Universal Guide

To ensure `thecattoolkit` skills are consistent and powerful, we adhere to Claude Code's native frontmatter schema as our primary standard.

## 1. Frontmatter Comparison Matrix

| Field | Claude Code | **TheCatToolkit Standard** |
| :--- | :--- | :--- |
| `name` | **Required** (kebab-case) | **Required** |
| `description` | **Required** (Max 1024) | **Required** |
| `context` | **Native** (`fork`) | **Recommended** (`context: fork`) |
| `allowed-tools`| **Native** | Optional |
| `hooks` | **Native** (PreToolUse, PostToolUse, Stop) | Optional |
| `model` | **Native** (haiku/sonnet/opus) | Optional |
| `agent` | **Native** (agent type specification) | Optional |
| `user-invocable` | **Native** (boolean) | Optional |

### Key Differences & Verified Findings
### Key Findings
1.  **Claude Code**: Supports powerful native fields:
    *   `context: fork`: Spawns an isolated sub-agent for the skill with its own conversation history (highly recommended for complex tasks).
    *   `hooks`: Supports lifecycle events including PreToolUse, PostToolUse, and Stop.
    *   `model`: Specifies which AI model (haiku/sonnet/opus) to use for this skill.
    *   `user-invocable`: Controls whether the skill appears in slash command menu (default: true).

## 2. Skill Frontmatter Strategy
 
 We adopt a **Native-First Schema**. We use Claude Code's native schema as the baseline for our skills, as it is the most robust.

### The "Gold Standard" Header
Every skill in `thecattoolkit` MUST start with this header:

```yaml
---
name: my-skill-name
description: >
  A concise, action-oriented description of what this skill does.
  CRITICAL: This text is used for "Semantic Intent Matching".
  Keep it under 1024 characters.
context: fork         # Claude Code: Isolated sub-agent with own conversation history
allowed-tools:        # Claude Code: Explicit tool permissions
  - Read
  - Write
  - Bash
model: sonnet         # Claude Code: Specify AI model (haiku/sonnet/opus)
user-invocable: true # Claude Code: Show in slash command menu (default: true)
hooks:                # Claude Code: Lifecycle automation
  PreToolUse: "validate-input"
  PostToolUse: "log-operation"
  Stop: "cleanup"
metadata:             # Extensibility for other tools
  category: core
  complexity: low
---
```

**Note:** The `version` field is available at the **plugin manifest** level (`.claude-plugin/plugin.json`) but not in individual skill YAML frontmatter.

### Discovery Rules
*   **Claude Code**: Utilizes `context` for "Mercenary Isolation" and `allowed-tools` for security. Skills are discovered in `skills/` directories (local or global).

## 3. Understanding `context: fork`

The `context: fork` field is one of Claude Code's most powerful features, enabling skills to run in **complete isolation** from the main conversation.

### What is Fork Context?

When a skill uses `context: fork`, it **spawns a completely isolated sub-agent** with:

- ✅ **Separate conversation history** - The forked agent has its own context window
- ✅ **Zero context pollution** - Main conversation remains clean
- ✅ **Autonomous execution** - Operates independently without main thread interference
- ✅ **Automatic result merging** - Results seamlessly integrate back to main conversation

### Isolation Behavior

| Aspect | Isolated in Fork | Shared with Main |
|:-------|:-----------------|:-----------------|
| **Conversation History** | ✅ Separate | ❌ |
| **Context Window** | ✅ Fresh | ❌ |
| **Task Memory** | ✅ Independent | ❌ |
| **Filesystem** | ❌ Same | ✅ |
| **Environment Variables** | ❌ Same | ✅ |
| **MCP Tools** | ❌ Same (unless restricted) | ✅ |
| **Git State** | ❌ Same | ✅ |

### Fork vs Regular Delegation

**Regular Task Delegation:**
```
Main Agent → Subagent (SHARED conversation history)
```

**Fork Context:**
```
Main Agent → Isolated Forked Agent → Results merged back
```

### When to Use `context: fork`

**✅ USE when:**
- Complex multi-step operations (>10 steps)
- Long-running analysis that would bloat main context
- Token conservation is critical
- Need parallel execution
- Specialized workflows requiring isolation

**❌ AVOID when:**
- Simple, single-step operations (<5 steps)
- Need user interaction during execution
- Require tight integration with main conversation

### The `agent` Field

The `agent` field works **only with `context: fork`** to specify sub-agent type:

```yaml
---
name: my-skill
description: Complex codebase analysis
context: fork
agent: Explore       # Fast, read-only exploration
model: opus         # Powerful model for complex reasoning
---

# Available agent types:
# - general-purpose: Capable agent for complex tasks
# - Explore: Fast, read-only exploration
# - Plan: Specialized for planning workflows
# - Custom: From .claude/agents/ directory
```

### Limitations

**Critical constraints:**
1. **No subagent chaining** - Forked agents cannot spawn other sub-agents
2. **No context inheritance** - Must provide ALL context in skill instructions
3. **No live communication** - Cannot ask questions mid-execution
4. **Self-contained skills required** - Must work completely autonomously

### Example: Comprehensive Security Audit

```yaml
---
name: comprehensive-security-audit
description: Performs thorough security analysis across entire codebase
context: fork
agent: general-purpose
model: opus
allowed-tools: Read, Grep, Glob, Bash
---

# Security Audit Skill
# Purpose: Analyze codebase security without cluttering main conversation
#
# This skill will:
# 1. Scan hundreds of files in isolation
# 2. Analyze authentication patterns
# 3. Check for vulnerabilities
# 4. Generate detailed report
# 5. Merge results back to main thread
#
# Main conversation stays pristine throughout!
```

### Key Takeaway

`context: fork` enables **"Mercenary Isolation"** - skills execute as autonomous specialists with zero contamination of the main conversation. This is essential for complex operations while maintaining conversation clarity.

## 4. Best Practices for Description

Since `description` is the *only* semantic signal shared by ALL frameworks, it must be engineered perfectly.

**Do:**
*   Use imperative verbs ("Extract", "Analyze", "Generate").
*   Mention specific file types or contexts ("...from PDF files", "...in the `src` directory").
*   Include "trigger keywords" (e.g., "Use this when the user asks to debug").

**Don't:**
*   Write vague marketing copy ("The best skill for coding").
*   Exceed 1024 characters (strict limit for Claude Code).
*   Put critical instructions in the description (put them in the Body).

## 5. SKILL.md Body Structure

To support all frameworks, the body should follow a standard "Instructional" format.

```markdown
# [Skill Name]

## Purpose
Brief explanation of the goal.

## Instructions
1. Step one...
2. Step two...

## Examples
User: "Fix the bug"
Assistant: [Action]
```

This structure is natively supported by Claude Code.
