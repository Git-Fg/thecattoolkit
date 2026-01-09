---
name: manage-subagents
description: MUST CONSULT when creating, auditing, or configuring subagents for isolated context execution, specialized expertise, or background-safe operations.
allowed-tools: Read Write Edit Bash Grep
---

# Subagent Management Standards

## Core Principle

**Default to Pure Markdown.** Most subagents work well with simple Markdown structure (`## Role`, `## Workflow`, `## Constraints`). Add XML tags only when complexity genuinely requires it (multi-phase state tracking, critical safety constraints).

## Shared Standards

For common principles, integration patterns, and anti-patterns, see:
- **[shared-standards.md](references/shared-standards.md)** - Common standards for all management skills

For core architecture and authoring guidance, consult `CLAUDE.md`.

# Activation Triggers

## WHEN
User specifically asks to create, audit, or modify a Subagent (`.claude/agents/*.md`).

## WHEN NOT
User asks about Skills or Commands.

# Quick Reference

# Quick Reference

## When to Create a Subagent

Use subagents for **Agent Sovereignty** and **specialized expertise**:

1. **Focused Lens Required**: Adopting a specialized persona for deep thinking
2. **System Maintenance**: Maintaining AI infrastructure
3. **Specialized Expertise**: Domain-specific knowledge

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
- `Skill` - Invoke skills and commands
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

## Capabilities Field (Optional)

Array of strings describing the agent's core competencies.

**Purpose:**
- Document what the agent can do well
- Help with agent selection and routing
- Provide quick overview of agent specialization

**Example:**
```yaml
capabilities: ["orchestration", "dependency-analysis", "parallel-execution", "quality-assurance"]
```

**Best Practices:**
- Use lowercase-with-hyphens format
- Keep to 3-5 key capabilities
- Focus on unique strengths
- Use action-oriented verbs

## Compatibility Field (Optional)

String specifying Claude version or model requirements.

**Purpose:**
- Ensure agent works with available Claude version
- Handle version-specific features or behavior
- Prevent compatibility issues

**Example:**
```yaml
compatibility: "claude>=3.5"
```

**Format:**
- Semantic version specification
- Supports: `>=`, `>`, `<=`, `<`, `==`
- Can specify minimum version for features

**Common Values:**
- `claude>=3.5` - Requires Claude 3.5 or newer
- `claude>=3.0` - Requires Claude 3.0 or newer
- `claude>=4.0` - Requires Claude 4.0 or newer (for latest features)

# Execution Model

## Agent Sovereignty

**Agents are specialized lenses on the current session.**

Agents run within the conversation flow, sharing history but adopting a specialized persona. They:

- ✅ **Share Context**: Full access to conversation history (read-only)
- ✅ **Specialized Persona**: Adopts a focused system prompt
- ✅ **Visible Execution**: Thoughts and tool use are visible in the logs
- ❌ **NOT "Clean Slate"**: They are not empty sessions; they are focused subprocesses.

The main agent delegates to the sovereign agent via the `Task` tool.

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
