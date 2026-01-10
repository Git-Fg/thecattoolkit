---
name: manage-subagents
description: USE when creating, auditing, or configuring subagents for isolated context execution, specialized expertise, or background-safe operations.
allowed-tools: Read, Write, Edit, Bash, Grep
---

# Subagent Management Standards

## Core Principle

**Agents are Primarily Personas for Skills.** When defining an agent, primarily design it to be bound to a Skill via `agent: [name]` in the skill frontmatter. This enables Skills to inherit a specialized identity without creating wrapper commands.

**Default to Pure Markdown.** Most subagents work well with simple Markdown structure (`## Role`, `## Workflow`, `## Constraints`). Add XML tags only when complexity genuinely requires it (multi-phase state tracking, critical safety constraints).

## Shared Standards

For common principles, integration patterns, and anti-patterns, see:
- **[shared-standards.md](../../styles/shared-standards.md)** - Common standards for all management skills

For core architecture and authoring guidance, consult `CLAUDE.md`.

# Activation Triggers

## WHEN
User specifically asks to create, audit, or modify a Subagent (`.claude/agents/*.md`).

## WHEN NOT
User asks about Skills or Commands.

# Quick Reference

## When to Create a Subagent

Use subagents for **isolated context** and **specialized expertise**:

1. **Persona Binding:** Define agents that Skills can bind to via `agent: [name]` in skill frontmatter.
2. **Separate Context Required:** Deep thinking and analysis requiring isolated context.
3. **System Maintenance:** Maintaining AI infrastructure.
4. **Specialized Expertise:** Domain-specific knowledge.

Consult `CLAUDE.md` for the comprehensive decision matrix.

## Subagent Creation Pattern

1. **Default**: Project-level (`.claude/agents/`) for portability
2. Define the subagent:
   - **name**: lowercase-with-hyphens
   - **description**: "[Role]. MUST/PROACTIVELY USE when [trigger condition]"
   - **tools**: Optional comma-separated list
   - **skills**: List relevant skills
3. Write system prompt using normal conversational language
4. Test with real delegation

## Background Execution Considerations

**Background-safe subagents:**
- Use read-only tools (Read, Grep, Glob) - safest
- Have pre-approved tool access
- Don't require user interaction
- Provide exhaustive context in task prompt

**Background-unsafe subagents:**
- Use Bash or Write tools without pre-approval
- Require user interaction or confirmation
- Perform destructive operations

See `references/agent-security.md` for comprehensive guidance.

# File Structure

| Type | Location | Scope | Priority |
|------|----------|-------|----------|
| **Project** (default) | `.claude/agents/` | Current project only, portable | Highest |
| **User** (if requested) | `~/.claude/agents/` | All projects | Lower |
| **Plugin** | Plugin's `agents/` dir | All projects | Lowest |

Project-level subagents override user-level when names conflict. Use project location for portability.

# Configuration

## Name Field
- Lowercase letters and hyphens only
- Must be unique

## Description Field
- Natural language description of purpose
- Include when Claude should invoke this subagent
- Used for automatic subagent selection

## Tools Field

**Available tools:**
- `Read`, `Write`, `Edit` - File operations
- `Glob`, `Grep` - File search
- `Bash` - Execute shell commands
- `TodoWrite` - Manage todo lists
- `Skill`, `SlashCommand` - Invoke skills and commands
- `Task` - Delegate to subagents
- `WebSearch`, `WebFetch` - Web access
- `BashOutput`, `KillShell` - Background shell management
- `NotebookEdit` - Jupyter notebook editing
- `ExitPlanMode` - Plan mode control

**Plus:** MCP tools from configured MCP servers can also be specified.

**Critical:** Subagents can use `AskUserQuestion` if configured via the `tools` field. If `tools` field is omitted, they inherit all tools including `AskUserQuestion`. If `tools` is specified, `AskUserQuestion` must be explicitly included.

## Model Field

- `sonnet`, `opus`, `haiku`, or `inherit`
- `inherit`: uses same model as main conversation
- **IMPORTANT**: Omit this field by default to keep subagents generalist
- Only specify a model if the user explicitly requests it or if the task requires specific model capabilities
- If omitted: defaults to configured subagent model (usually sonnet)

# Execution Model

## Critical Constraint

**Subagents are black boxes that CAN interact with users, but intermediate steps are hidden.**

Subagents run in isolated contexts and return their final output to the main conversation. They:

- ✅ Can use tools like Read, Write, Edit, Bash, Grep, Glob
- ✅ Can access MCP servers and other non-interactive tools
- ✅ **Can use AskUserQuestion** ONLY if they are **Planning Phase Coordinators** (Director/Orchestrator). Execution Phase Workers are **STRICLY PROHIBITED** from using it.
- ❌ **User never sees subagent's intermediate steps** (only final output)

The main conversation sees only the subagent's final report/output.

# Templates

**MANDATORY: When creating or editing subagents, always read and use the appropriate template from `assets/templates/`.**

| Template | Use Case |
|----------|----------|
| `universal-agent.md` | Core, Specialized, or Research agents (Default) |
| `coordinator-agent.md` | Multi-step orchestration |
| `explorer-agent.md` | Read-only code exploration |

# Working Examples

Ready-to-use canonical patterns:

- **[background-safe-agent.md](examples/background-safe-agent.md)** - Read-only code explorer (Background Safe)

# References

**Security**: [agent-security.md](references/agent-security.md)
- Tool permissions and least privilege
- Background execution safety
- AskUserQuestion guidelines

*Consult `CLAUDE.md` for core architecture and quality gates.*

# Success Criteria

A well-configured subagent has:

- Valid YAML frontmatter (name matches file, description includes triggers)
- Clear role definition in system prompt
- Appropriate tool restrictions (least privilege)
- Well-structured system prompt with role, approach, and constraints
- Description field optimized for automatic routing
- Successfully tested on representative tasks
- Model selection appropriate for task complexity
