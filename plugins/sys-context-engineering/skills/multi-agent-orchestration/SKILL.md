---
name: multi-agent-orchestration
description: "MUST USE when designing multi-agent systems for context isolation and parallel execution. Implements three patterns: Orchestrator (task delegation), Swarm (parallel workers), and Hierarchical (supervisor-subordinate) for preventing context saturation and enabling specialization."
user-invocable: true
allowed-tools: [Read, Write, Bash, Grep, Glob]
---

# Multi-Agent Orchestration for Context Isolation

You are a **Multi-Agent Orchestration Specialist** focused on designing agent systems that prevent context window saturation through intelligent isolation. Your expertise lies in applying the right orchestration pattern for each use case: orchestrator for delegation, swarm for parallelism, and hierarchical for supervision.

## Core Capability

Design and implement multi-agent architectures that solve the fundamental problem of context isolation. Multi-agent systems are not about anthropomorphizing roles—they're about preventing any single agent's context from becoming saturated while enabling specialized, focused execution.

## The Three Orchestration Patterns

### 1. Orchestrator Pattern (Task Delegation)

**Definition:** Central planner delegates tasks to specialized executor agents, maintaining global context while sub-agents operate with isolated, focused contexts.

**When to Use:**
- Single complex task requiring different expertise areas
- Need to prevent main agent context saturation
- Tasks have clear sub-components that can be parallelized
- Want centralized planning with distributed execution

**Architecture:**
```mermaid
graph TB
    MAIN[\"Main Agent<br/>Global Context<br/>Task Planning<br/>20K tokens\"]

    TASK1[\"Executor Agent 1<br/>Code Specialist<br/>Isolated Context<br/>10K tokens\"]
    TASK2[\"Executor Agent 2<br/>Data Specialist<br/>Isolated Context<br/>10K tokens\"]
    TASK3[\"Executor Agent 3<br/>Testing Specialist<br/>Isolated Context<br/>10K tokens\"]

    MAIN -->|Task + Minimal Context| TASK1
    MAIN -->|Task + Minimal Context| TASK2
    MAIN -->|Task + Minimal Context| TASK3

    TASK1 -->|Results Only| MAIN
    TASK2 -->|Results Only| MAIN
    TASK3 -->|Results Only| MAIN

    MAIN -->|Synthesize Results| FINAL[\"Final Output<br/>Global Context<br/>10K tokens\"]
```

**Implementation Pattern:**
```javascript
// Orchestrator agent design
class OrchestratorAgent {
  constructor() {
    this.executors = {
      code: new ExecutorAgent('code'),
      data: new ExecutorAgent('data'),
      test: new ExecutorAgent('test')
    }
    this.globalContext = new ContextWindow(20000)  // Maintains global view
  }

  async executeTask(task) {
    // 1. Plan decomposition in global context
    const subtasks = await this.planDecomposition(task)

    // 2. Delegate to executors with MINIMAL context
    const results = await Promise.all(
      subtasks.map(subtask => this.delegate(subtask))
    )

    // 3. Synthesize in global context
    return this.synthesize(results)
  }

  async delegate(subtask) {
    // Pass ONLY what's needed for the subtask
    const minimalContext = {
      subtask: subtask.description,
      relevantFiles: subtask.files,
      constraints: subtask.constraints,
      // NO global context, NO conversation history
    }

    const executor = this.executors[subtask.type]
    const result = await executor.execute(minimalContext)

    // Return ONLY results, not full context
    return {
      subtaskId: subtask.id,
      output: result.output,
      artifacts: result.artifacts,
      success: result.success
    }
  }
}
```

**Context Isolation Rules:**

| Context Element | Main Agent | Executor Agent |
|-----------------|------------|---------------|
| **Global task** | ✓ Full | ✗ Overview only |
| **Conversation history** | ✓ All | ✗ Current subtask |
| **Previous decisions** | ✓ All | ✗ Relevant to subtask |
| **File system state** | ✓ Full | ✗ Relevant files only |
| **Tool outputs** | ✓ All | ✗ Current subtask |

**Benefits:**
- Main agent never saturates
- Each executor operates with focused context
- Parallel execution possible
- Central coordination maintained

---

### 2. Swarm Pattern (Parallel Workers)

**Definition:** N identical workers process independent tasks in parallel, each with identical starting context and isolated execution.

**When to Use:**
- Many independent, similar tasks
- Can parallelize without coordination
- Need horizontal scaling
- Tasks are stateless and idempotent

**Architecture:**
```mermaid
graph TB
    DISPATCHER[\"Dispatcher<br/>Task Queue<br/>Context: Task Definitions<br/>5K tokens\"]

    WORKER1[\"Worker 1<br/>Isolated Context<br/>Task A<br/>10K tokens\"]
    WORKER2[\"Worker 2<br/>Isolated Context<br/>Task B<br/>10K tokens\"]
    WORKER3[\"Worker 3<br/>Isolated Context<br/>Task C<br/>10K tokens\"]
    WORKERN[\"...<br/>Isolated Context<br/>Task N<br/>10K tokens\"]

    DISPATCHER -->|Same Starting Context| WORKER1
    DISPATCHER -->|Same Starting Context| WORKER2
    DISPATCHER -->|Same Starting Context| WORKER3
    DISPATCHER -->|Same Starting Context| WORKERN

    WORKER1 -->|Result 1| COLLECTOR[\"Collector<br/>Aggregate Results<br/>Context: Results Only<br/>5K tokens\"]
    WORKER2 -->|Result 2| COLLECTOR
    WORKER3 -->|Result 3| COLLECTOR
    WORKERN -->|Result N| COLLECTOR
```

**Implementation Pattern:**
```javascript
// Swarm orchestration
class SwarmOrchestrator {
  constructor(workerCount = 5) {
    this.workers = Array.from({ length: workerCount }, (_, i) =>
      new WorkerAgent(`worker-${i}`)
    )
    this.taskQueue = new Queue()
  }

  async executeSwarm(tasks) {
    // 1. Distribute tasks to workers
    const assignments = this.assignTasks(tasks, this.workers)

    // 2. Execute in parallel (workers are isolated)
    const results = await Promise.all(
      this.workers.map(worker => worker.execute(assignments[worker.id]))
    )

    // 3. Collect and aggregate
    return this.aggregate(results)
  }

  // Workers get IDENTICAL starting context
  getWorkerContext() {
    return {
      instructions: this.baseInstructions,
      tools: this.standardTools,
      resources: this.sharedResources
      // NO task-specific context here
    }
  }
}

// Each worker receives isolated context
class WorkerAgent {
  async execute(tasks) {
    const context = this.getIsolatedContext()
    const results = []

    for (const task of tasks) {
      // Add task-specific context ONLY for this task
      const taskContext = {
        ...context,
        task: task
      }

      const result = await this.processTask(taskContext)
      results.push(result)

      // Reset context for next task
      this.resetContext()
    }

    return results
  }
}
```

**Isolation Characteristics:**

| Aspect | All Workers Share | Each Worker Has Own |
|--------|------------------|---------------------|
| **Base instructions** | ✓ Identical | ✗ |
| **Tool definitions** | ✓ Identical | ✗ |
| **Task queue** | ✓ Shared | ✗ |
| **Execution history** | ✗ | ✓ Isolated |
| **Task results** | ✗ | ✓ Isolated |

**Benefits:**
- Perfect horizontal scaling
- No cross-contamination between tasks
- Workers are stateless and restartable
- Simple fault tolerance (restart failed workers)

---

### 3. Hierarchical Pattern (Supervisor-Subordinate)

**Definition:** Supervisor agent monitors and guides subordinate agents, providing oversight and quality control while maintaining context separation.

**When to Use:**
- Need quality control and validation
- Complex workflows requiring oversight
- Compliance or audit requirements
- Want to catch errors before completion

**Architecture:**
```mermaid
graph TB
    SUPERVISOR[\"Supervisor Agent<br/>Global Oversight<br/>Quality Control<br/>Context: All tasks<br/>15K tokens\"]

    SUB1[\"Subordinate 1<br/>Focused Execution<br/>Context: Task Group 1<br/>10K tokens\"]
    SUB2[\"Subordinate 2<br/>Focused Execution<br/>Context: Task Group 2<br/>10K tokens\"]
    SUB3[\"Subordinate 3<br/>Focused Execution<br/>Context: Task Group 3<br/>10K tokens\"]

    SUPERVISOR -->|Task + Standards| SUB1
    SUPERVISOR -->|Task + Standards| SUB2
    SUPERVISOR -->|Task + Standards| SUB3

    SUB1 -->|Work Product| SUPERVISOR
    SUB2 -->|Work Product| SUPERVISOR
    SUB3 -->|Work Product| SUPERVISOR

    SUPERVISOR -->|Validation + Feedback| SUB1
    SUPERVISOR -->|Validation + Feedback| SUB2
    SUPERVISOR -->|Validation + Feedback| SUB3

    SUPERVISOR -->|Final Report| OUTCOME[\"Validated Output<br/>Global Context<br/>5K tokens\"]
```

**Implementation Pattern:**
```javascript
// Hierarchical supervision
class SupervisorAgent {
  constructor() {
    this.subordinates = [
      new SubordinateAgent('research'),
      new SubordinateAgent('implementation'),
      new SubordinateAgent('testing')
    ]
    this.oversightContext = new ContextWindow(15000)
  }

  async executeWithOversight(project) {
    const phases = this.planPhases(project)

    for (const phase of phases) {
      // Delegate to subordinate
      const subordinate = this.selectSubordinate(phase.type)
      const workProduct = await subordinate.execute(phase)

      // Validate in supervisor context
      const validation = await this.validate(workProduct, phase)

      if (!validation.passed) {
        // Provide feedback and retry
        await subordinate.revise(validation.feedback)
      }

      // Update supervisor context with validated work
      this.oversightContext.add(`Phase ${phase.id}: ${validation.summary}`)
    }

    return this.compileFinalReport()
  }

  async validate(workProduct, phase) {
    // Supervisor has full context of all phases
    // Can check for consistency, completeness, quality

    const validation = {
      phaseId: phase.id,
      checks: {
        completeness: this.checkCompleteness(workProduct),
        consistency: this.checkConsistency(workProduct),
        quality: this.checkQuality(workProduct),
        standards: this.checkStandards(workProduct)
      },
      passed: true
    }

    if (!validation.passed) {
      validation.feedback = this.generateFeedback(validation)
    }

    return validation
  }
}

class SubordinateAgent {
  constructor(specialization) {
    this.specialization = specialization
    this.isolatedContext = new ContextWindow(10000)
  }

  async execute(phase) {
    // Subordinate has context ONLY for this phase
    this.isolatedContext.reset()
    this.isolatedContext.add({
      phase: phase.description,
      requirements: phase.requirements,
      standards: this.getSpecializationStandards()
      // NO context of other phases
    })

    const workProduct = await this.performWork(phase)

    // Return work product, not full context
    return {
      phaseId: phase.id,
      output: workProduct,
      artifacts: workProduct.artifacts
    }
  }
}
```

**Supervision Rules:**

| Context Element | Supervisor | Subordinate |
|-----------------|------------|-------------|
| **All phases** | ✓ Complete | ✗ Current only |
| **Quality standards** | ✓ Full definition | ✗ Relevant to specialization |
| **Cross-phase consistency** | ✓ Can check | ✗ Cannot verify |
| **Current phase details** | ✓ Overview | ✓ Full detail |
| **Revision history** | ✓ All | ✗ Current iteration |

**Benefits:**
- Quality control at each phase
- Consistency across phases
- Supervisor maintains bird's-eye view
- Subordinates stay focused

---

## Pattern Selection Decision Tree

```mermaid
graph TD
    Start[\"Task Analysis\"] --> Q1{\"Can task be<br/>decomposed?\"}

    Q1 -->|No| Single[\"Single Agent<br/>+ Context Compression\"]

    Q1 -->|Yes| Q2{\"Are subtasks<br/>independent?\"}

    Q2 -->|Yes| Q3{\"Many similar tasks<br/>(>10)?\"}

    Q2 -->|No| Q4{\"Need quality<br/>control?\"}

    Q3 -->|Yes| Swarm[\"Swarm Pattern<br/>Parallel Workers\"]

    Q3 -->|No| Orchestrator[\"Orchestrator Pattern<br/>Task Delegation\"]

    Q4 -->|Yes| Hierarchical[\"Hierarchical Pattern<br/>Supervisor-Subordinate\"]

    Q4 -->|No| Orchestrator

    Single --> End1[\"Optimize single agent\"]
    Swarm --> End2[\"Scale horizontally\"]
    Orchestrator --> End3[\"Delegate with isolation\"]
    Hierarchical --> End4[\"Supervise with oversight\"]
```

**Pattern Comparison:**

| Criterion | Orchestrator | Swarm | Hierarchical |
|-----------|-------------|-------|--------------|
| **Context isolation** | High | Very High | High |
| **Parallelization** | Medium | Maximum | Low |
| **Coordination overhead** | Medium | Low | High |
| **Quality control** | Low | None | Maximum |
| **Complexity** | Medium | Low | High |
| **Use case fit** | Mixed tasks | Identical tasks | Complex workflows |

---

## Context Isolation Best Practices

### 1. Minimize Context Passing

**Rule:** Pass only what's absolutely necessary for the subtask.

```javascript
// BAD: Passing excessive context
const excessiveContext = {
  fullHistory: allMessages,           // 50K tokens
  allFiles: entireFileSystem,        // 100K tokens
  allDecisions: everyDecisionEver,   // 20K tokens
  subtask: "fix this bug"            // 10 tokens
}
// GOOD: Minimal context
const minimalContext = {
  subtask: "fix null pointer in userService.js line 47",
  relevantFiles: ["userService.js", "userTest.js"],
  constraints: ["don't modify other files", "tests must pass"],
  successCriteria: "userService.getUser() handles null input"
}
```

### 2. Return Results, Not Context

**Rule:** Sub-agents should return artifacts and results, not their full context.

```javascript
// BAD: Returning context
subagentResult = {
  context: fullAgentContext,    // 50K tokens
  result: actualOutput          // 500 tokens
}
// GOOD: Returning artifacts
subagentResult = {
  filesModified: ["userService.js"],
  testResults: { passed: 47, failed: 0 },
  changes: { added: 12, removed: 5, modified: 3 },
  output: "Fixed null pointer, all tests pass"
}
```

### 3. Use File System for Shared State

**Rule:** Persist important information to file system, not context.

```javascript
// Use file system for persistence
const sharedState = {
  projectPlan: writeFile('/state/project_plan.md', plan),
  decisionLog: writeFile('/state/decisions.log', decisions),
  progress: writeFile('/state/progress.json', progress)
}
// Pass references, not content
const context = {
  plan: { reference: '/state/project_plan.md' },
  decisions: { reference: '/state/decisions.log' },
  progress: { reference: '/state/progress.json' }
}
```

---

## Integration with Cat Toolkit Skills

This skill integrates with:

- **context-degradation-detection** - Prevents degradation through isolation
- **context-compression** - Compresses context before delegation
- **memory-systems** - Manages shared state via file system
- **kv-cache-optimization** - Maintains cache across agent boundaries

---

## Usage Instructions

When invoked, this skill will:

1. **Analyze task structure** to determine appropriate pattern
2. **Design multi-agent architecture** with context isolation
3. **Implement orchestration logic** with minimal context passing
4. **Configure agent boundaries** and communication protocols
5. **Provide monitoring framework** for multi-agent health

**Example Activation:**
```
User: "I need to process 1000 documents in parallel"

Skill Response:
→ Recommended: Swarm Pattern (parallel workers)
→ Architecture: 10 workers × 100 documents each
→ Context strategy: Identical starting context per worker
→ Isolation: Each worker gets only task definition + relevant doc
→ Expected: 10× speedup with zero cross-contamination
→ Implementation: /workers/ directory with dispatcher script
```

**Remember:** Multi-agent systems are about context isolation, not role anthropomorphization. The goal is to prevent any single agent from saturating its context window while enabling specialized, focused execution. Choose the pattern based on task structure: orchestrator for delegation, swarm for parallelism, hierarchical for oversight.
