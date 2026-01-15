---
name: architecting-agents
description: "Provides industry-proven design patterns for effective AI agents based on production systems like Claude Code, Manus, and Cursor. Use when designing agent architectures, optimizing context management, or implementing sub-agent patterns."
user-invocable: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Agent Design Patterns

Comprehensive guide to agent design patterns distilled from production systems (Claude Code, Manus, Cursor) and research. Focuses on context management as the core challenge for effective agent design.

## Cost Warning (CRITICAL)

Before using sub-agents, understand the costs:

| Approach | Token Cost | Quota Cost | When to Use |
|:---------|:-----------|:-----------|:------------|
| **Inline** | ~1x | Free (tool call) | Most tasks |
| **Fork** | ~3x | Free (tool call) | Isolation needed |
| **Subagent** | ~25k+ | 1 prompt per spawn | Parallelization only |

**Default Recommendation:** Use `context: fork` in skills for isolation. Subagents are ONLY appropriate when parallelization benefit clearly exceeds 20K token startup cost AND quota overhead.

See [references/subagent-risks.md](references/subagent-risks.md) for detailed evidence.

---

## Core Principle

> Context must be treated as a finite resource with diminishing marginal returns. Like humans with limited working memory, LLMs have an "attention budget." Every new token depletes it.

**Context engineering is the delicate art and science of filling the context window with just the right information for the next step.**

## Pattern Index

| Pattern | Purpose | When to Use |
|:--------|:--------|:------------|
| [Computer Access](#1-computer-access) | Persistent context via filesystem | Agent needs state persistence |
| [Multi-Layer Actions](#2-multi-layer-action-space) | Hierarchical tool design | Reducing tool definition overhead |
| [Progressive Disclosure](#3-progressive-disclosure) | Reveal actions on demand | Managing large action spaces |
| [Context Offloading](#4-context-offloading) | Filesystem storage for context | Context window pressure |
| [Context Caching](#5-context-caching) | Prompt caching strategies | Cost/latency optimization |
| [Context Isolation](#6-context-isolation) | Sub-agent separation | Long-running or parallel tasks |
| [Context Evolution](#7-context-evolution) | Continual learning | Building agent memories |

---

## 1. Computer Access

**Principle:** Give agents access to a computer (filesystem + shell) for persistent context and action execution.

**Key Insight:** The fundamental coding agent abstraction is the CLI, rooted in the fact that agents need access to the OS layer.

**Components:**
- **Filesystem**: Persistent context storage, state across sessions
- **Shell**: Execute utilities, CLIs, scripts, or generated code

**Production Examples:**
- Claude Code: "Lives on your computer"
- Manus: Virtual computer environment
- Both use tools to control the computer primitives

**Implementation:**
```
Agent → Bash Tool → Shell Utilities / CLIs / Scripts
Agent → File Tools → Read / Write / Edit filesystem
```

---

## 2. Multi-Layer Action Space

**Principle:** Use a small set of atomic tools that can execute broader actions on the computer.

**Key Insight:** Popular agents use surprisingly few tools (Claude Code ~12, Manus <20). They push actions to the computer layer.

**Action Hierarchy:**
```
Level 1: Tool Calling (agent-visible)
  ↓
Level 2: Shell Utilities / CLIs (computer-level)
  ↓
Level 3: Code Execution (generated scripts)
```

**Benefits:**
- Reduces tool definition token overhead
- Agents chain actions by writing/executing code
- Intermediate tool results stay on computer (not in context)

**Reference:** See CodeAct paper for chaining actions via code execution.

---

## 3. Progressive Disclosure

**Principle:** Show only essential information upfront; reveal details only when needed.

**Key Insight:** Tool definitions overload context. The GitHub MCP server has 35 tools with ~26K tokens of definitions.

**Strategies:**

| Layer | Approach |
|:------|:---------|
| Tool Calling | Index definitions, retrieve on demand |
| Shell Utilities | List available utilities in instructions; use `--help` when needed |
| MCP Servers | Sync descriptions to folder; read full spec only if task requires |
| Skills | YAML frontmatter indexed; full SKILL.md read on demand |

**Implementation Pattern:**
```
1. Provide short list of available capabilities
2. Agent reads detailed spec only when task matches
3. Execute with full knowledge loaded just-in-time
```

---

## 4. Context Offloading

**Principle:** Move context from the agent window to the filesystem.

**Key Insight:** Summarization can lose useful information. Offloading preserves full fidelity with on-demand retrieval.

**Approaches:**
- Write old tool results to files
- Store agent trajectories for later retrieval
- Apply summarization only after offloading diminishing returns

**Plan File Pattern:**
Write plan to file → Read periodically to reinforce objectives → Verify work against plan

**Production Examples:**
- Manus: Writes tool results to files
- Cursor: Offloads trajectories to filesystem

---

## 5. Context Caching

**Principle:** Maximize prompt cache hit rate for cost and latency efficiency.

**Key Insight:** Cache hit rate is the most important metric for production agents. A higher-capacity model with caching can be cheaper than a lower-cost model without it.

**Cost Impact:**
```
Cached tokens:   ~10x cheaper than uncached
Target hit rate: >80%
```

**Caching Requirements:**
- Stable prefix (system prompt unchanged)
- Append-only message history
- Deterministic serialization (sorted JSON keys)

**Anti-Pattern:** Mutating history in ways that break cache prefix

---

## 6. Context Isolation

**Principle:** Delegate tasks with isolated context windows.

**Default Approach: Use `context: fork`**

```yaml
---
name: processing-batch
description: "Processes multiple files in isolated context"
context: fork
allowed-tools: [Read, Write, Bash]
---
```

**Cost:** ~3x inline, but FREE as tool call within prompt quota.
**Use for:** Heavy operations (>10 files), parallel processing, isolation needs.

**Subagent Alternatives (Use Sparingly)**

ONLY when parallelization benefit > 20K token startup cost:

| Scenario | Pattern | Recommendation |
|:---------|:--------|:---------------|
| Parallelizable tasks | Map-reduce | Use fork unless >50 parallel units |
| Long-running tasks | Ralph Loop | Use fork with persistent files |
| Independent checks | Parallel reviewers | Use fork for cost efficiency |

**The Ralph Loop:**
```
1. Initializer sets up environment (plan file, tracking file)
2. Sub-agents tackle individual tasks from plan
3. Progress communicated via git history
4. Stop hooks verify work after each iteration
5. Repeat until plan satisfied
```

**Benefits:**
- Prevents single-agent context saturation
- Enables parallel execution
- Clear isolation boundaries

---

## 7. Context Evolution

**Principle:** Update agent context with learnings over time (continual learning in token space).

**Key Insight:** Agents that cannot adapt or learn often fail in production deployments.

**Evolution Patterns:**

| Type | Approach |
|:-----|:---------|
| Task-specific prompts | Collect trajectories → Score → Reflect on failures → Propose variants |
| Memory learning | Distill sessions into diary entries → Reflect → Update instructions |
| Skill learning | Reflect over trajectories → Distill reusable procedures → Save as new skills |

**Implementation:**
```
Session Log → Reflection → Memory/Skill Update → Context
```

---

## Future Directions

### Learned Context Management
Models may learn to perform their own context management, absorbing scaffolding currently in agent harnesses. Related: Recursive Language Model (RLM) research.

### Multi-Agent Coordination
Swarms of concurrent agents need coordination for shared context, conflict resolution, and proactive discourse. Example: Gas Town uses git-backed work tracking with a "Mayor" agent.

### Long-Running Agent Abstractions
New infrastructure needed: observability, human review hooks, graceful degradation. No current standards exist for agent debugging interfaces or monitoring patterns.

---

## Quick Reference

**For detailed implementations, see:**
- [references/computer-access.md](references/computer-access.md) - Filesystem/shell patterns
- [references/action-hierarchy.md](references/action-hierarchy.md) - Multi-layer tool design
- [references/progressive-disclosure.md](references/progressive-disclosure.md) - Just-in-time context loading
- [references/context-patterns.md](references/context-patterns.md) - Offload, cache, isolate, evolve

**Related Skills:**
- `agent-orchestration` - Multi-agent patterns (Orchestrator, Swarm, Hierarchical)
- `context-engineering` - Compression, degradation, KV-cache optimization
- `memory-systems` - Long-term memory architectures
