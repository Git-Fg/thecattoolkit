---
name: claude-code-mastery
description: "Provides comprehensive guide for mastering Claude Code including plan mode workflows, context optimization, and advanced skills/subagents/MCP patterns. Use when building with Claude Code, optimizing workflows, or implementing advanced features. Do not use for skill authoring, plugin development, or system design."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Claude Code Mastery Guide

## Core Purpose

This skill provides expert guidance for mastering Claude Code (Anthropic's CLI tool) based on production-tested workflows from enterprise developers. It covers everything from fundamental planning principles to advanced system architecture patterns.

## Quick Start (Choose Your Path)

### 1. Fundamentals (Start Here)
**If you're new to Claude Code or want to improve basic usage:**
- Load [Fundamentals Guide](references/fundamentals.md)
- Covers: Plan mode, CLAUDE.md optimization, context windows, prompting

### 2. Advanced Features
**If you want to leverage skills, subagents, and MCP:**
- Load [Advanced Features Guide](references/advanced-features.md)
- Covers: Custom skills, subagents, MCP connectors, system building

### 3. Context Optimization
**If you're working with large projects or long conversations:**
- Load [Context Window Strategies](references/context-window.md)
- Covers: Context degradation, preservation techniques, conversation management

### 4. Best Practices
**For proven patterns and anti-patterns:**
- Load [Patterns & Best Practices](references/patterns.md)
- Covers: What works, what doesn't, troubleshooting

## Key Concepts

### 1. Think First (Plan Mode)
**The #1 mistake**: Starting to type immediately without planning.

> **Golden Rule**: 10 out of 10 times, plan mode produces significantly better results than just starting to talk.

**How to access**: Press `Shift+Tab` twice to enter plan mode
**When to use**: Always, for any task involving architecture, complex implementation, or multi-step workflows

### 2. CLAUDE.md Optimization
Your project's instruction file that Claude reads at startup.

**Keep it**:
- Short (150-200 instructions max)
- Specific to your project
- Explains *why*, not just *what*
- Updated constantly (press `#` to auto-add instructions)

**Don't make it**:
- A novel (Claude will start ignoring things)
- Generic documentation
- Outdated

### 3. Context Window Management
Claude Code provides a consistent 200K token window (unlike tools like Cursor which may truncate earlier).

**Critical thresholds**:
- **<20%**: Optimal performance
- **20-40%**: Quality starts degrading
- **>40%**: Significant degradation, consider strategies

**Strategies**:
- External memory (write plans to files)
- Copy-paste reset (clear and preserve essentials)
- Scope conversations (one task per conversation)

### 4. The Advanced Trinity

#### Skills: Teaching Claude Your Workflows
Create `~/.claude/skills/skill-name/SKILL.md` to teach Claude specific patterns.

**Structure**:
```yaml
---
name: code-review-standards
description: "Apply team standards when reviewing code. Use when reviewing PRs or asking for feedback."
---
# Your methodology here
```

#### Subagents: Isolated Context
Separate Claude instances with their own context windows for complex tasks.

**Benefits**:
- Fresh context for each sub-task
- Prevent context pollution
- Parallel execution

**Built-in types**:
- Explore (fast, read-only analysis)
- Plan (research and planning)
- General-purpose (complex multi-step tasks)

#### MCP Connectors: Never Leave Claude
Connect external services directly: GitHub, Slack, databases, issue trackers.

**Command**:
```bash
claude mcp add --transport http <name> <url>
```

**Impact**: Transform workflows that required 5 context switches into one continuous session.

## Progressive Disclosure

For deeper exploration:

| Topic | Reference | When to Load |
|-------|-----------|--------------|
| **Planning workflows** | [references/fundamentals.md](references/fundamentals.md) | New to plan mode or complex tasks |
| **Context optimization** | [references/context-window.md](references/context-window.md) | Working with large codebases |
| **Skills creation** | [references/advanced-features.md](references/advanced-features.md) | Building custom workflows |
| **System architecture** | [references/patterns.md](references/patterns.md) | Production deployments |
| **Troubleshooting** | [references/patterns.md#troubleshooting](references/patterns.md#troubleshooting) | When stuck or looping |

## Success Criteria

You'll know you've mastered Claude Code when you:
- [ ] Always use plan mode for complex tasks
- [ ] Have a living, updated CLAUDE.md
- [ ] Manage context proactively, not reactively
- [ ] Use skills for repeatable patterns
- [ ] Leverage subagents for complex workflows
- [ ] Connect external services via MCP
- [ ] Build systems, not just run one-off tasks

## Next Steps

1. Start with [Fundamentals](references/fundamentals.md)
2. Identify your most repeated tasks → turn them into skills
3. Practice context management techniques
4. Experiment with MCP connectors for your workflow
5. Build systems using headless mode (`claude -p`)
