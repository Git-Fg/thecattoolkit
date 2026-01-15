---
name: orchestrating-agents
description: "Implements Orchestrator, Swarm, and Hierarchical patterns for preventing context saturation. Use when designing multi-agent systems for context isolation and parallel execution."
user-invocable: true
allowed-tools: [Read, Write, Bash, Grep, Glob]
---

# Multi-Agent Orchestration for Context Isolation

Implements Orchestrator, Swarm, and Hierarchical patterns.



## The Three Orchestration Patterns

### 1. Orchestrator Pattern (Task Delegation)

### 1. Orchestrator Pattern (Task Delegation)

**When to Use:**
- Single complex task requiring different expertise areas
- Need to prevent main agent context saturation
- Tasks have clear sub-components that can be parallelized
- Want centralized planning with distributed execution



### 2. Swarm Pattern (Parallel Execution)

### 2. Swarm Pattern (Parallel Execution)

**When to Use:**
- Multiple independent tasks of same type
- Need for parallel speedup
- Different perspectives on same problem
- Large-scale data processing



### 3. Hierarchical Pattern (Supervision)

### 3. Hierarchical Pattern (Supervision)

**When to Use:**
- Large, complex tasks with hierarchy
- Need for quality control
- Multi-level task decomposition
- Quality gates required



## Pattern Selection Guide

### Decision Matrix

| Use Case | Orchestrator | Swarm | Hierarchical |
|----------|--------------|-------|--------------|
| **Task Decomposition** | Best | Possible | Good |
| **Parallel Execution** | Limited | Best | Possible |
| **Quality Control** | Limited | No | Best |
| **Scalability** | Medium | High | High |
| **Complexity** | Medium | Low | High |

### Selection Criteria

**Choose Orchestrator when:** Clear task decomposition available, need centralized coordination, different expertise areas required, single complex task

**Choose Swarm when:** Multiple independent tasks, parallel speedup needed, different perspectives helpful, large-scale processing

**Choose Hierarchical when:** Quality control critical, multi-level tasks, need supervision at each level, complex error handling required

## Context Isolation Principles



### The Solution: Context Isolation

**Rule 1: Specialized Contexts** - Each agent has focused context, only task-relevant information, no cross-agent contamination

**Rule 2: Minimal Exchange** - Pass only necessary data, use structured formats, avoid conversation history sharing

**Rule 3: Results, Not Context** - Agents return results, not ongoing context, synthesize results centrally, maintain global view in orchestrator

## Advanced Context Isolation Strategies



### Context Degradation Patterns

| Pattern | Symptom | Mitigation |
|:--------|:--------|:-----------|
| **Lost-in-Middle** | Info at 40-60% position ignored | Place critical info at start/end |
| **Context Poisoning** | Errors compound through references | Require source citations |
| **Context Distraction** | Model ignores training knowledge | Quality over quantity |
| **Context Confusion** | Incorrect associations | Rigorous context selection |
| **Context Clash** | Contradictory information | Establish information hierarchy |

### Context Isolation Techniques

#### 1. TodoWrite Attention Manipulation (Recitation)
Constantly rewrite todos to push objectives into recent attention span:

```markdown
# Update after every major tool call
## Phase 1: Research
- [x] Analyze codebase structure
- [ ] Identify patterns  ← Visible in recent attention
- [ ] Plan implementation
```

**Why It Works:**
- **Todo rewriting recites objectives into context end**

#### 2. System Reminders
Combat degradation through recurring objective injection:

**Effective Patterns:**
- **Objective recitation** - Reiterate main goal
- **Constraint reinforcement** - Re-emphasize requirements
- **Context anchoring** - Reference key elements

#### 3. Plan Mode Coordination
Use plan mode for complex, multi-phase tasks:

**When to Use:**
- Complex tasks requiring 10+ tool calls
- Multi-phase implementations
- When agent appears confused or drifting

**Best Practices:**
- Create plan at task start
- Update as understanding evolves
- Reference plan in reminders
- Store in `.cattoolkit/context/plan.md`

### Context Window Thresholds & Actions

| Utilization | Action | Technique |
|:------------|:-------|:----------|
| **<60%** | Monitor | No action needed |
| **60-80%** | Light compression | Observation masking |
| **80-95%** | Aggressive compression | Summarization + compaction |
| **>95%** | Emergency | Force session handoff |

## Best Practices

### Recommended Practices

**Define Clear Interfaces** - Specify input/output formats, use structured data, document expectations

**Minimize Context Sharing** - Pass only necessary data, avoid conversation history, use file-based coordination

**Isolate Agent Contexts** - Each agent focused on specific task, no cross-contamination, specialized expertise

**Return Results, Not Context** - Agents produce artifacts, structured outputs, central synthesis

**Test Isolation** - Verify agents don't share context, check result quality, validate coordination

**Use Progressive Context Loading** - Load only what's needed when needed

**Apply Attention Management** - Use TodoWrite, reminders, and plan mode strategically

### Practices to Avoid

**Sharing Full Context** - Never pass conversation history, don't share unrelated information, maintain isolation

**Over-Complicating** - Start simple, add complexity incrementally, use appropriate pattern

**Ignoring Coordination** - Plan result merging, handle conflicts, manage dependencies

**Violating Isolation** - Keep contexts separate, use file-based coordination, respect boundaries

**Ignoring Degradation** - Monitor context utilization, apply compression early

## Reference Materials

**Core Patterns:**
- **See:** [orchestrator-pattern.md](references/orchestrator-pattern.md) - Complete orchestrator implementation guide
- **See:** [swarm-pattern.md](references/swarm-pattern.md) - Complete swarm implementation guide
- **See:** [hierarchical-pattern.md](references/hierarchical-pattern.md) - Complete hierarchical implementation guide

**Implementation:**
- **See:** [implementation-guide.md](references/implementation-guide.md) - Step-by-step implementation
- **See:** [context-isolation.md](references/context-isolation.md) - Context management strategies
- **See:** [coordination.md](references/coordination.md) - Agent coordination patterns

## Next Steps

1. **Assess Requirements** - Task complexity, parallelism needs, quality requirements
2. **Choose Pattern** - Use decision matrix, consider constraints, match use case
3. **Design Architecture** - Define agent roles, plan context isolation, specify interfaces
4. **Implement Incrementally** - Start simple, add complexity, test isolation
5. **Monitor and Optimize** - Measure performance, check quality, optimize bottlenecks
