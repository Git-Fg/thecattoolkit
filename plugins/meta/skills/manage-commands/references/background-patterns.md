# Background Execution Patterns for Commands

## Overview

Commands can delegate to subagents with background execution for asynchronous task processing. This enables commands to launch long-running work while allowing the user to continue working.

## Key Principle

> **Commands delegate, agents execute.** Commands should provide clear context and instructions for background agents to work autonomously.

---

## Core Patterns

### Pattern 1: Single Background Agent

**Use case:** Delegate a single long-running task to a background agent.

```yaml
---
description: Analyze codebase architecture in background
argument-hint: [path-to-analyze]
allowed-tools: Task
disable-model-invocation: true
---

Task the code-analyzer agent with: $ARGUMENTS

Run this agent in background so you can continue working.

**IMPORTANT: Provide exhaustive context including:**
- What the code does
- What you're looking for
- Any specific patterns or concerns
- Expected output format

Retrieve results later using the agent ID returned.
```

**When to use:**
- Single, well-defined task
- Task takes minutes to complete
- User wants to continue working during execution
- Task is read-only or non-destructive

### Pattern 2: Parallel Fan-Out

**Use case:** Launch multiple background agents simultaneously for independent tasks.

```yaml
---
description: Parallel analysis of multiple modules
argument-hint: [module1] [module2] [module3]
allowed-tools: Task
disable-model-invocation: true
---

Launch 3 background agents in parallel:

Agent 1: Analyze $1 for security vulnerabilities
Agent 2: Analyze $2 for performance issues
Agent 3: Analyze $3 for code quality

Provide each agent with:
- Full context about the module's purpose
- Specific focus areas for analysis
- Expected output format

Report back when all agents complete.
```

**When to use:**
- Multiple independent tasks
- Tasks can run simultaneously
- User wants all results together
- Tasks are similar in nature

### Pattern 3: Hybrid Foreground/Background

**Use case:** Launch background agents, then do foreground work while waiting.

```yaml
---
description: Background analysis with foreground prep work
argument-hint: [path-to-analyze]
allowed-tools: Task, Read, Edit
---

Task the code-explorer agent to analyze: $ARGUMENTS
Run in background with: run_in_background: true

While background agent runs:
1. Review existing documentation
2. Identify gaps and questions
3. Prepare integration plan

Once background agent completes:
4. Synthesize analysis with your findings
5. Provide comprehensive report
```

**When to use:**
- Background task + related foreground work
- User has work that can be done in parallel
- Results need to be synthesized together

### Pattern 4: Background with Explicit Result Retrieval

**Use case:** Command that retrieves and presents background agent results.

```yaml
---
description: Analyze code and retrieve results when complete
argument-hint: [path-to-analyze]
allowed-tools: Task
---

Spawn a background agent to analyze: $ARGUMENTS

The agent should search for patterns, structure, and dependencies.

When the agent completes, present the analysis in a clear, structured format showing:
- Files discovered
- Patterns found
- Dependencies identified
- Any concerns or recommendations
```

**When to use:**
- Results needed immediately after completion
- Command should present formatted results
- User shouldn't need to manually retrieve

---

## Permission Considerations

### Background Safety

Commands that delegate to background agents must consider permission requirements:

| Agent Tool Access | Background Safe? | Command Pattern |
|-------------------|------------------|-----------------|
| Read-only (Read, Grep, Glob) | ✅ Yes | `allowed-tools: Task` |
| File operations (Read, Write) | ⚠️ Maybe | Verify pre-approval |
| Bash execution | ❌ No | Don't use background |
| Full tool access | ❌ No | Don't use background |

**Best practice:** For background delegation, ensure the target agent:
1. Uses only read-only tools (safest)
2. Has tools pre-approved in permissions
3. Is explicitly designed for background execution

### Tool Restrictions in Commands

When delegating to background agents:

```yaml
---
# Good: Minimal delegation
allowed-tools: Task
---

# Also acceptable: Task plus context tools
allowed-tools: Task, Read, Grep, Glob

# Avoid: Restricting what agent can use
# (Agent's tools field should handle this)
allowed-tools: Task(Read)  # Don't do this
```

**Rationale:** The agent's own `tools` field should control what it can access. Commands should focus on delegation, not micromanaging agent permissions.

---

## Context Provisioning

### Critical: Exhaustive Context

Background agents start with fresh context. Commands must provide all relevant information:

**❌ Insufficient context:**
```yaml
---
description: Analyze the auth module
allowed-tools: Task
---

Task the analyzer agent to analyze: src/auth
```

**✅ Sufficient context:**
```yaml
---
description: Analyze auth module for migration readiness
argument-hint: [auth-path]
allowed-tools: Task
---

Task the analyzer agent with:
"Analyze $ARGUMENTS for migration to session-based auth.

Context:
- Currently using JWT tokens stored in localStorage
- New session backend is in src/auth/sessions/
- API endpoints must remain compatible
- Look for: tight coupling to JWT, hardcoded token references, auth middleware usage

Expected output:
- List of files requiring changes
- Complexity assessment for each file
- Recommended migration order"
```

### Context Template

Use this structure for background agent prompts:

```
[Task description]

Context:
- Background: [relevant context about the project/codebase]
- Goal: [what we're trying to achieve]
- Constraints: [limitations or requirements]

Focus Areas:
- [Specific area 1]
- [Specific area 2]
- [Specific area 3]

Expected Output:
- [Format for results]
- [Specific information needed]
```

---

## Platform-Specific Patterns

### Built-in Research Agent (Platform-Specific)

**⚠️ WARNING:** Built-in agents are platform-specific. Document as optional.

```yaml
---
description: Quick code exploration using platform research agent
argument-hint: [search-term]
allowed-tools: Task
---

⚠️ NOTE: This requires platform support for built-in research agents.

If available, use the platform's read-only research agent to search for: $ARGUMENTS

Run in background for fast, parallel searching.

If not available, inform the user this command requires platform-specific agent support.
```

**Principles:**
- Clearly document platform dependency
- Provide fallback behavior
- Don't assume platform has the agent
- Test before deploying

### Cross-Platform Alternative

```yaml
---
description: Code exploration using custom agent
argument-hint: [search-term]
allowed-tools: Task
---

Task the code-searcher agent to find: $ARGUMENTS
Run in background so you can continue working.

Agent context:
- Search pattern: $ARGUMENTS
- Scope: Entire codebase
- Expected: File paths and line numbers

This uses a custom agent defined in .claude/agents/code-searcher.md
```

---

## Advanced Patterns

### Pattern 5: Staged Execution

**Use case:** Run background agents in sequence, where each depends on previous results.

```yaml
---
description: Multi-stage analysis with dependencies
argument-hint: [path-to-analyze]
allowed-tools: Task
---

Stage 1: Spawn a background agent to analyze architecture of $ARGUMENTS
Wait for completion, then proceed to Stage 2.

Stage 2: Spawn a background agent to map dependencies using the architecture analysis
Wait for completion, then proceed to Stage 3.

Stage 3: Combine architecture and dependency analyses into comprehensive report

Each stage should complete before the next begins.
```

**When to use:**
- Tasks have dependencies
- Each stage produces input for next
- Total time is sum of all stages

### Pattern 6: Background with Progress Notification

**Use case:** Long-running task where user wants progress updates.

```yaml
---
description: Long-running analysis with progress
argument-hint: [path-to-analyze]
allowed-tools: Task
---

Spawn a background agent to comprehensively analyze: $ARGUMENTS

Instruct the agent to provide progress updates at major milestones:
- Initial scan complete
- Pattern detection complete
- Analysis complete

Report significant progress updates to the user as they become available.
```

---

## Error Handling

### When Background Agent Fails

**Symptoms:**
- Agent never completes
- Results are incomplete or erroneous
- Agent appears stuck

**Command patterns for resilience:**

```yaml
---
description: Analyze with fallback behavior
allowed-tools: Task
---

Spawn a background agent to analyze: $ARGUMENTS

If the agent fails to complete or returns errors:
- Inform user the background task encountered issues
- Suggest alternative approach (foreground execution, different agent)
- Provide any partial results if available
```

**⚠️ Note:** Exact error detection methods vary by platform. Some provide explicit error handling, others require timeout-based detection.

### Validation Before Background Launch

```yaml
---
description: Validate before launching background agent
argument-hint: [path]
allowed-tools: Task, Glob
---

First validate path exists:
Glob(pattern: "$ARGUMENTS/**")

If found:
  Spawn a background agent to analyze: $ARGUMENTS
If not found:
  Inform user path doesn't exist
  Don't launch agent
```

---

## Templates

See `assets/templates/` for ready-to-use command templates:

- `background-agent-delegator.md` - Single background agent delegation
- `parallel-fan-out.md` - Multiple parallel agents
- `hybrid-workflow.md` - Foreground + background combination

---

## Related Documentation

- **Background Execution Reference (Subagents)**: Consult the `background-execution.md` from the `manage-subagents` skill for technical details on background execution.
- [Command Permissions Guide](./permissions-guide.md) - Tool restrictions and security
- **Subagent Invocation Reference**: Consult the `subagents.md` from the `manage-subagents` skill for details on Task tool parameters and invocation patterns.
