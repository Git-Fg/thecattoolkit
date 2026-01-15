---
name: architecting-agents
description: "Provides industry-proven design patterns for effective AI agents based on production systems like Claude Code, Manus, and Cursor. Use when designing agent architectures, optimizing context management, or implementing sub-agent patterns."
user-invocable: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Architecting Agents Protocol

# Architecting Agents Protocol

Provides design patterns for agent context management.

## Cost Warning (CRITICAL)

Before using sub-agents, understand the costs:

| Approach | When to Use |
|:---------|:------------|
| **Inline** | Most tasks |
| **Fork** | Isolation needed |
| **Subagent** | Parallelization only (High Cost) |

**Default Recommendation:** Use `context: fork` in skills for isolation. Subagents are ONLY appropriate when parallelization benefit clearly exceeds 20K token startup cost AND quota overhead.

See [references/subagent-risks.md](references/subagent-risks.md) for detailed evidence.

---



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

**Components:**
- **Filesystem**: Persistent context storage, state across sessions
- **Shell**: Execute utilities, CLIs, scripts, or generated code

**Implementation:**
```
Agent → Bash Tool → Shell Utilities / CLIs / Scripts
Agent → File Tools → Read / Write / Edit filesystem
```

---

## 2. Multi-Layer Action Space



**Action Hierarchy:**
```
Level 1: Tool Calling (agent-visible)
  ↓
Level 2: Shell Utilities / CLIs (computer-level)
  ↓
Level 3: Code Execution (generated scripts)
```



---

## 3. Progressive Disclosure



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

**Approaches:**
- Write old tool results to files
- Store agent trajectories for later retrieval
- Apply summarization only after offloading diminishing returns

**Plan File Pattern:**
Write plan to file → Read periodically to reinforce objectives → Verify work against plan

---

## 5. Context Caching



**Caching Requirements:**
- Stable prefix (system prompt unchanged)
- Append-only message history
- Deterministic serialization (sorted JSON keys)

**Anti-Pattern:** Mutating history in ways that break cache prefix

---

## 6. Context Isolation



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
