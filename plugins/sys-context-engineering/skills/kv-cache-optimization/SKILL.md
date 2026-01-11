---
name: kv-cache-optimization
description: "MUST USE when optimizing AI agent cost and latency through KV-cache reuse. Implements four principles: Stable Prefix, Append-Only Context, Deterministic Serialization, and Explicit Breakpoints for 10× cost reduction."
user-invocable: true
allowed-tools: [Read, Write, Bash, Grep, Glob]
---

# KV-Cache Optimization for Cost Reduction

You are a **KV-Cache Optimization Specialist** focused on maximizing the reuse of computed attention states to reduce cost and latency in AI agent systems. Your expertise lies in implementing cache-friendly patterns that achieve 10× cost reduction through intelligent prompt design and context management.

## Core Capability

Optimize agent systems to achieve >80% KV-cache hit rate through systematic application of cache optimization principles. KV-cache optimization is the single most important cost reduction technique in production agent systems.

## The KV-Cache Problem

### What is KV-Cache?

**Key-Value Cache:** When LLMs process tokens, they compute and cache attention keys and values. If the same tokens appear again, the model reuses the cached computation instead of recomputing.

**Cost Impact:**
```
Claude Sonnet Pricing:
- Cached: $0.30 per 1M tokens
- Uncached: $3.00 per 1M tokens
- Savings: 90% cost reduction
```

**The Critical Metric:**
```
Average agent trajectory: 100 input tokens → 1 output token
Ratio: 100:1 input-to-output

If 80% of input tokens are cached:
- Cost per task: $0.12 → $0.012
- Savings: 90% cost reduction
```

### Why Most Systems Fail

**Anti-patterns that break KV-cache:**
1. **Unstable prefixes**: Changing system prompts invalidate cache
2. **In-place edits**: Modifying previous messages breaks cache
3. **Non-deterministic serialization**: Different JSON order = different tokens
4. **Implicit boundaries**: No clear cache segment markers

---

## The Four Optimization Principles

### 1. Stable Prefix (10× Impact)

**Principle:** Keep system prompts and base instructions completely unchanged across requests.

**Implementation:**
```javascript
// BAD: Changing system prompt
const badPrompt = {
  system: `You are an AI assistant. Date: ${new Date()}`,
  // System prompt changes every request!
}

// GOOD: Stable system prompt
const goodPrompt = {
  system: `You are an AI assistant.
  Current date: [SET_AT_RUNTIME]
  Version: v1.0`,
  runtimeVars: {
    date: new Date()
  }
}
```

**Cache-Friendly System Prompt Template:**
```javascript
function createStableSystemPrompt() {
  return {
    // NEVER CHANGE THIS ACROSS REQUESTS
    core: `You are an AI agent for task automation.

Core capabilities:
- File operations (read, write, edit)
- Code execution and testing
- Web search and information retrieval
- Data processing and analysis

Operational constraints:
- Always validate before executing
- Provide detailed reasoning
- Return structured results
- Log all actions taken`,

    // Separate stable from dynamic
    dynamic: {
      currentDate: null,        // Set at runtime
      userContext: null,       // Set per request
      taskSpecific: null       // Set per request
    }
  }
}
```

**Prefix Stability Checklist:**

| Element | Stability Rule | Cache Impact |
|---------|---------------|--------------|
| **System prompt** | Never change structure | High |
| **Tool definitions** | Keep order stable | High |
| **Base instructions** | Fixed across sessions | High |
| **Current date** | Inject separately | Medium |
| **User context** | Append only | Low |
| **Task details** | Append only | Low |

---

### 2. Append-Only Context (Critical)

**Principle:** Never modify previous messages. Always append new context to the end.

**Anti-pattern:**
```javascript
// BAD: Modifying previous messages
conversation[0] = updateSystemPrompt(newPrompt)  // Invalidates cache!
conversation[1] = addMissingContext(context)     // Invalidates cache!
```

**Correct Pattern:**
```javascript
// GOOD: Append-only
async function addContext(conversation, newContext) {
  // Never modify existing messages
  conversation.push({
    role: 'user',
    content: newContext
  })

  return conversation  // Previous messages unchanged
}
```

**Context Management Strategy:**
```javascript
class CacheFriendlyContext {
  constructor() {
    this.base = this.createStableBase()
    this.history = []  // Never modify base
  }

  addMessage(message) {
    // Always append, never modify
    this.history.push({
      timestamp: Date.now(),
      message: message
    })
  }

  // Separate dynamic from stable
  getPrompt() {
    return {
      stable: this.base,        // Cached
      dynamic: this.history     // Not cached
    }
  }
}
```

---

### 3. Deterministic Serialization (Essential)

**Principle:** Ensure identical data always serializes to identical strings. JSON key order matters!

**Anti-pattern:**
```javascript
// BAD: Non-deterministic JSON
const data = {
  user: "Alice",
  tasks: ["code", "test"],
  status: "active"
}

// Different execution = different key order
// Cache miss!
```

**Correct Pattern:**
```javascript
// GOOD: Deterministic serialization
function serializeDeterministic(obj) {
  return JSON.stringify(obj, Object.keys(obj).sort())
}

// Or use structured serialization
function serializeWithSchema(data) {
  return {
    user: data.user,
    tasks: data.tasks.sort(),
    status: data.status
  }
}

// Stable tool call format
function serializeToolCall(toolName, args) {
  const sorted = Object.keys(args)
    .sort()
    .reduce((result, key) => {
      result[key] = args[key]
      return result
    }, {})

  return `${toolName}(${JSON.stringify(sorted)})`
}
```

**Deterministic Data Structures:**

| Type | Pattern | Example |
|------|---------|---------|
| **Arrays** | Always sorted | `["a", "b", "c"]` not `["c", "a", "b"]` |
| **Objects** | Sorted keys | `{a: 1, b: 2}` not `{b: 2, a: 1}` |
| **Maps** | Stable order | Use arrays of tuples |
| **Dates** | ISO format | `2024-01-15T10:30:00Z` |

---

### 4. Explicit Breakpoints (Control)

**Principle:** Mark cache boundaries explicitly to control granularity and enable partial reuse.

**Implementation:**
```javascript
class CacheBreakpointManager {
  constructor() {
    this.breakpoints = []
  }

  setBreakpoint(name, tokenCount) {
    this.breakpoints.push({
      name: name,
      tokenCount: tokenCount,
      timestamp: Date.now()
    })
  }

  // Cache prefix up to breakpoint
  getCachedPrefix(breakpointName) {
    const bp = this.breakpoints.find(b => b.name === breakpointName)
    return this.extractPrefix(bp.tokenCount)
  }

  // Continue from breakpoint
  continueFromBreakpoint(breakpointName) {
    return {
      cachedPrefix: this.getCachedPrefix(breakpointName),
      dynamicContext: this.getContextAfter(breakpointName)
    }
  }
}

// Usage
const cache = new CacheBreakpointManager()

// Set strategic breakpoints
cache.setBreakpoint('system', 5000)        // System prompt + tools
cache.setBreakpoint('session', 15000)      // Session context
cache.setBreakpoint('taskStart', 25000)    // Task begins
```

**Strategic Breakpoints:**

| Breakpoint | Content | Cache Lifetime |
|------------|---------|----------------|
| **System** | System prompt + tools | Entire session |
| **Session** | User profile + history | Current task |
| **Task** | Task definition | Current subtask |
| **Subtask** | Specific instructions | Single action |

---

## Cache Optimization Architecture

### Multi-Level Caching Strategy

```mermaid
graph TB
    REQUEST[\"New Request\"] --> CHECK[\"Check Cache\"]

    CHECK --> HIT[\"Cache Hit\"] --> RETURN[\"Return Cached Result<br/>90% savings\"]
    CHECK --> MISS[\"Cache Miss\"] --> COMPUTE[\"Compute Full<br/>Full cost\"]

    COMPUTE --> STORE[\"Store in Cache\"] --> RETURN

    subgraph \"Cache Levels\"
        L1[\"System Prompt<br/>Never changes\"]
        L2[\"Session Context<br/>Changes rarely\"]
        L3[\"Task Context<br/>Changes per task\"]
        L4[\"Dynamic Context<br/>Changes frequently\"]
    end

    L1 --> CHECK
    L2 --> CHECK
    L3 --> CHECK
    L4 --> CHECK
```

### Implementation Pattern

```javascript
class CacheOptimizedAgent {
  constructor() {
    this.basePrompt = this.createStableBasePrompt()
    this.cache = new KVCache()
    this.serializer = new DeterministicSerializer()
  }

  async process(task) {
    // 1. Build cache key from stable prefix + task
    const cacheKey = this.buildCacheKey(task)

    // 2. Check cache
    const cached = await this.cache.get(cacheKey)

    if (cached) {
      return {
        result: cached,
        cacheHit: true,
        costSavings: 0.9  // 90% saved
      }
    }

    // 3. Compute (cache miss)
    const result = await this.compute(task)

    // 4. Store in cache
    await this.cache.set(cacheKey, result)

    return {
      result: result,
      cacheHit: false,
      costSavings: 0
    }
  }

  buildCacheKey(task) {
    // Combine stable prefix with task signature
    const stable = this.basePrompt
    const dynamic = this.serializer.serialize(task)

    return this.hash(`${stable}:${dynamic}`)
  }

  createStableBasePrompt() {
    return this.serializer.serialize({
      role: "system",
      content: `You are an AI agent.

Capabilities:
- File operations
- Code execution
- Web search
- Data analysis

Always:
- Validate before executing
- Provide reasoning
- Return structured results`,

      // Fixed structure, never change
      version: "1.0",
      capabilities: ["file_ops", "code_exec", "web", "data"]
    })
  }
}
```

---

## Cache Hit Rate Optimization

### Measuring Cache Performance

```javascript
class CacheMetrics {
  constructor() {
    this.hits = 0
    this.misses = 0
    this.totalTokens = 0
    this.cachedTokens = 0
  }

  recordRequest(cacheHit, tokenCount) {
    if (cacheHit) {
      this.hits++
      this.cachedTokens += tokenCount
    } else {
      this.misses++
      this.totalTokens += tokenCount
    }
  }

  getHitRate() {
    return this.hits / (this.hits + this.misses)
  }

  getTokenSavings() {
    const cachedValue = this.cachedTokens * 0.30  // $0.30 per 1M tokens
    const fullValue = this.totalTokens * 3.00     // $3.00 per 1M tokens
    return (fullValue - cachedValue) / fullValue
  }

  report() {
    return {
      hitRate: `${(this.getHitRate() * 100).toFixed(1)}%`,
      costSavings: `${(this.getTokenSavings() * 100).toFixed(1)}%`,
      totalRequests: this.hits + this.misses,
      cacheHits: this.hits,
      cacheMisses: this.misses
    }
  }
}
```

### Target Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Cache Hit Rate** | >80% | (Cache hits / Total requests) |
| **Cost Savings** | >70% | (Full cost - Cached cost) / Full cost |
| **Prefix Stability** | 95% | (Stable tokens / Total tokens) |
| **Serialization Stability** | 100% | Deterministic serialization |

---

## Production Implementation

### Cache-Aware Context Manager

```javascript
class CacheAwareContextManager {
  constructor() {
    this.levels = {
      stable: { tokens: 0, cacheable: true },
      session: { tokens: 0, cacheable: true },
      task: { tokens: 0, cacheable: true },
      dynamic: { tokens: 0, cacheable: false }
    }

    this.serializer = new DeterministicSerializer()
  }

  addToContext(level, content) {
    const serialized = this.serializer.serialize(content)
    this.levels[level].tokens += this.estimateTokens(serialized)

    return {
      level: level,
      content: serialized,
      cacheable: this.levels[level].cacheable
    }
  }

  getOptimizedPrompt() {
    // Combine cacheable levels (stable prefix)
    const cacheable = Object.entries(this.levels)
      .filter(([_, level]) => level.cacheable)
      .map(([level, _]) => level)
      .join('\n\n')

    // Dynamic content (not cached)
    const dynamic = this.levels.dynamic.content

    return {
      cachedPrefix: cacheable,
      dynamicContext: dynamic,
      cacheBreakpoint: this.calculateBreakpoint()
    }
  }

  calculateBreakpoint() {
    const totalCacheableTokens = Object.entries(this.levels)
      .filter(([_, level]) => level.cacheable)
      .reduce((sum, [_, level]) => sum + level.tokens, 0)

    return totalCacheableTokens
  }
}
```

### Automated Cache Optimization

```javascript
// Automated prompt refactoring for cache optimization
function optimizeForCache(prompt) {
  const analysis = analyzePrompt(prompt)

  // Identify unstable elements
  const unstable = analysis.filter(element => !element.isStable)

  // Generate optimized version
  const optimized = refactorPrompt(prompt, {
    stabilizeSystemPrompt: true,
    extractDynamicVariables: true,
    enforceDeterministicSerialization: true,
    addCacheBreakpoints: true
  })

  return {
    original: prompt,
    optimized: optimized,
    changes: {
      stabilized: unstable.length,
      estimatedHitRateImprovement: calculateImprovement(unstable)
    }
  }
}
```

---

## Cost Impact Examples

### Example 1: Code Review Agent

**Before Optimization:**
```
Cache hit rate: 20%
Tokens per task: 45,000
Cost per task: $0.135
```

**After Optimization:**
```
Cache hit rate: 85%
Tokens per task: 45,000 (same)
Cost per task: $0.040
Savings: 70% cost reduction
```

**Breakdown:**
- System prompt (cached): 5,000 tokens × 0.30 = $0.0015
- Tool definitions (cached): 10,000 tokens × 0.30 = $0.003
- Session context (cached): 15,000 tokens × 0.30 = $0.0045
- Dynamic context (uncached): 15,000 tokens × 3.00 = $0.045
- **Total**: $0.054 (was $0.135)

---

### Example 2: Data Analysis Pipeline

**Before Optimization:**
```
Cache hit rate: 10%
Tasks per day: 100
Daily cost: $13.50
Monthly cost: $405
```

**After Optimization:**
```
Cache hit rate: 80%
Tasks per day: 100
Daily cost: $4.05
Monthly cost: $121.50
Annual savings: $3,402
```

---

## Integration with Cat Toolkit Skills

This skill integrates with:

- **context-compression** - Compressed context maintains cache prefixes
- **multi-agent-orchestration** - Each agent maintains its own cache
- **memory-systems** - Long-term memory doesn't invalidate cache
- **context-degradation-detection** - Monitors cache hit rates

---

## Usage Instructions

When invoked, this skill will:

1. **Analyze current prompt structure** for cache-breaking patterns
2. **Refactor prompts** to follow four optimization principles
3. **Implement cache-friendly context management** with explicit breakpoints
4. **Set up cache monitoring** with hit rate and cost metrics
5. **Provide optimization report** with projected savings

**Example Activation:**
```
User: "My agent costs are too high - $0.50 per task"

Skill Response:
→ Cache hit rate analysis: 15% (target: >80%)
→ Identified issues:
  - Unstable system prompt (changes date each request)
  - Non-deterministic JSON serialization
  - No cache breakpoints
→ Optimizations applied:
  - Separated stable from dynamic content
  - Implemented deterministic serialization
  - Added explicit cache boundaries
→ Projected improvement:
  - Cache hit rate: 15% → 85%
  - Cost per task: $0.50 → $0.15
  - Monthly savings (1000 tasks): $350
```

**Remember:** KV-cache optimization is the single most important cost reduction technique. Focus on the four principles: Stable Prefix, Append-Only Context, Deterministic Serialization, and Explicit Breakpoints. A well-optimized system achieves 80%+ cache hit rates and 70%+ cost savings.
