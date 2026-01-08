# Subagent Permissions & Security

## Overview

Agents (subagents) use the `tools` field in their frontmatter to control which tools they can access. Unlike commands and skills, agents run in **isolated contexts** and have distinct permission semantics.

## Key Principle

> **Agents inherit all tools by default.** The `tools` field is used to **restrict** access to only the tools explicitly listed.

## Autonomy First Principle

**This toolkit is designed for autonomous operation.** Agents should complete tasks independently with minimal user interaction.

### AskUserQuestion: Use Only When Explicitly Required

⚠️ **WARNING**: `AskUserQuestion` should **NOT** be included in agent tools by default.

**Only include `AskUserQuestion` when:**
- The user **explicitly requests** interactive behavior
- The task **genuinely requires** human judgment that cannot be automated
- The workflow is **designed** to gather requirements upfront before execution

**DO NOT include `AskUserQuestion` when:**
- The agent should work autonomously (most cases)
- You want to pause for decisions that can be reasonably assumed
- The agent's role is analysis, not gathering input
- You're unsure if it's needed

**Default Behavior:**
- Omit `AskUserQuestion` from tools field
- Let the agent make reasonable decisions based on context
- Provide options in the final output for user review
- Use the agent's description to guide its behavior

**The goal**: You describe the task → Agent figures out how to do it → Agent completes it → You review the result.

## Frontmatter Field

| Field | Type | Required | Default | Behavior |
|-------|------|----------|---------|----------|
| `tools` | String (comma-separated) | No | Inherit all | If specified, ONLY these tools are available |

## Available Tools

**Core Tools:**
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

## Critical Permission Rules

### Inheritance Rules

**If `tools` field is omitted:**
- Agent inherits ALL tools from main conversation
- Including `AskUserQuestion` (if available in main)
- Use this for general-purpose agents

**If `tools` field is specified:**
- ONLY tools listed are available
- ALL other tools are blocked
- Use this for security and focus

### Background Execution Safety

**Read-only agents (safe for background):**
- Tools: `Read`, `Grep`, `Glob` only
- Cannot modify files or execute commands
- Safe for asynchronous execution

**Write/execute agents (unsafe for background):**
- Tools include `Write`, `Edit`, `Bash`
- Require user confirmation or foreground mode
- May need `AskUserQuestion` for permissions

## Security Principles

### Least Privilege

**Follow least privilege:**
- Grant only necessary tools
- Default to read-only when possible
- Add tools only when clearly needed
- Review permissions periodically

### Permission Patterns

**Analysis agents:**
```yaml
tools: Read, Grep, Glob
```

**Generation agents:**
```yaml
tools: Read, Write, Edit, Glob
```

**Research agents:**
```yaml
tools: Read, Grep, Glob, WebSearch, WebFetch
```

**Full-capability agents:**
```yaml
tools: Read, Write, Edit, Glob, Grep, Bash
```

## Model Selection

### Available Models

- `sonnet` - Default, good balance
- `opus` - Most capable, complex reasoning
- `haiku` - Fast, simple tasks
- `inherit` - Use same model as main conversation

### Model Selection Rules

**Use `inherit` (default) when:**
- Task doesn't need specific model capabilities
- User hasn't specified a model
- Agent should adapt to main conversation

**Use `sonnet` when:**
- Complex reasoning required
- Multi-step analysis
- Default choice for most agents

**Use `opus` when:**
- Highly complex reasoning
- Advanced problem-solving
- Explicitly requested

**Use `haiku` when:**
- Simple, straightforward tasks
- Speed is critical
- Basic information retrieval

## Background Execution

### Overview

Background subagent execution allows agents to run asynchronously without blocking the main conversation. This enables parallel processing, long-running tasks, and improved user experience by deferring work to separate contexts.

**⚠️ Platform-Specific Feature**

Background execution is **platform-dependent**. Not all AI systems support it, and implementations vary:

- Some platforms support true asynchronous background execution
- Some platforms simulate it through parallel agent invocation
- Some platforms don't support it at all

**Always document background execution as optional** and provide fallback behavior.

### Key Principle

> **Background agents run in isolation** - they cannot easily request user input or permissions during execution.

### Execution Modes

#### Foreground Execution (Default)

Subagent runs synchronously, blocking the main conversation until completion.

**Characteristics:**
- Main conversation waits for subagent to finish
- User sees subagent's final output when it completes
- Subagent can potentially request input (if tools allow)
- Context consumed in main conversation window

**Use when:**
- Task requires user interaction or confirmation
- Result is needed before proceeding
- Task is short (seconds to minutes)

#### Background Execution (Platform-Dependent)

Subagent runs asynchronously, main conversation continues immediately.

**Characteristics:**
- Main conversation continues without waiting
- Subagent runs in isolated context
- Result retrieved later (method varies by platform)
- Context NOT consumed in main conversation (major benefit)

**Use when:**
- Long-running tasks (minutes to hours)
- Parallel processing desired
- User wants immediate continuation
- Task doesn't need immediate result

### Risk Assessment Matrix

| Tool Type | Background Safe? | Requires Approval? | Risk Level |
|-----------|----------------|-------------------|------------|
| Read-only | Yes | No | Low |
| Write-only | Conditional | Yes | Medium |
| Execute (Bash) | No | Yes | High |
| Web access | Conditional | Yes | Medium |
| File edit | No | Yes | High |

### Safety Protocols

**Background-safe agents:**
- Use only read-only tools
- Pre-approved tool access
- Don't require user interaction
- Provide exhaustive context in task prompt

**Background-unsafe agents:**
- Use Write/Edit/Bash without pre-approval
- Require user interaction or confirmation
- Perform destructive operations
- Need immediate feedback

## Cross-Platform Compatibility

### Platform-Specific Considerations

**File System:**
- Use forward slashes in paths
- Avoid hardcoded separators
- Test across Windows/Mac/Linux

**Shell Commands:**
- Use POSIX-compliant syntax
- Avoid platform-specific features
- Test commands on target platforms

**Python Scripts:**
- Specify version requirements
- Use cross-platform libraries
- Avoid OS-specific imports

## Error Handling

### Common Failure Modes

**Permission denied:**
- Tool not in allowed list
- Background execution attempted
- Insufficient privileges

**Context isolation:**
- Cannot access main conversation state
- Must rely on task prompt context
- Cannot request additional information

**Tool unavailability:**
- MCP server not connected
- Platform doesn't support tool
- Version mismatch

### Recovery Strategies

**Graceful degradation:**
- Continue with available tools
- Log errors to disk
- Provide partial results

**Retry patterns:**
- One retry with different strategy
- Exponential backoff
- Circuit breaker for repeated failures

**Handoff protocol:**
- Create HANDOFF.md when blocked
- Document what was attempted
- Explain what user needs to do

## Testing Permissions

### Validation Checklist

**Before deploying agent:**
- [ ] Tools explicitly listed if needed
- [ ] Least privilege principle followed
- [ ] Background safety verified
- [ ] Cross-platform compatibility tested
- [ ] Error handling documented

**For each tool:**
- [ ] Tool actually needed
- [ ] Risk level acceptable
- [ ] Alternatives considered
- [ ] Security implications reviewed
