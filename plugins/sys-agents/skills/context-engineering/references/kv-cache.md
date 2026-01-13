# KV-Cache Optimization Reference

Maximizing KV-cache reuse for 10× cost reduction in AI agent systems.

## The KV-Cache Problem

**Cost Impact:**
```
Claude Sonnet:
- Cached: $0.30 per 1M tokens
- Uncached: $3.00 per 1M tokens
- Potential savings: 90%

Average agent trajectory: 100 input : 1 output
If 80% cached: $0.12 → $0.012 per task
```

**Anti-patterns that break KV-cache:**
1. Unstable prefixes (changing system prompts)
2. In-place edits (modifying previous messages)
3. Non-deterministic serialization (different JSON order)
4. Implicit boundaries (no cache segment markers)

## The Four Optimization Principles

### 1. Stable Prefix (10× Impact)

Keep system prompts unchanged across requests.

```javascript
// BAD
const badPrompt = {
  system: `You are AI. Date: ${new Date()}`  // Changes every request!
}

// GOOD
const goodPrompt = {
  system: `You are AI. [DATE_PLACEHOLDER]`,
  runtimeVars: { date: new Date() }  // Injected separately
}
```

**Prefix Stability Checklist:**

| Element | Rule | Cache Impact |
|---------|------|--------------|
| System prompt | Never change structure | High |
| Tool definitions | Keep order stable | High |
| Base instructions | Fixed across sessions | High |
| Current date | Inject separately | Medium |

### 2. Append-Only Context (Critical)

Never modify previous messages. Always append.

```javascript
// BAD
conversation[0] = updateSystemPrompt(newPrompt)  // Invalidates cache!

// GOOD
conversation.push({ role: 'user', content: newContext })
```

### 3. Deterministic Serialization (Essential)

Identical data must serialize to identical strings.

```javascript
// BAD - Non-deterministic
JSON.stringify({ b: 2, a: 1 })  // Order varies

// GOOD - Deterministic
JSON.stringify(obj, Object.keys(obj).sort())
```

**Rules:**
- Arrays: Always sorted
- Objects: Sorted keys
- Dates: ISO format (`2024-01-15T10:30:00Z`)

### 4. Explicit Breakpoints (Control)

Mark cache boundaries for granular control.

```javascript
cache.setBreakpoint('system', 5000)     // System + tools
cache.setBreakpoint('session', 15000)   // Session context
cache.setBreakpoint('taskStart', 25000) // Task begins
```

| Breakpoint | Content | Cache Lifetime |
|------------|---------|----------------|
| System | System prompt + tools | Entire session |
| Session | User profile + history | Current task |
| Task | Task definition | Current subtask |

## Target Metrics

| Metric | Target |
|--------|--------|
| Cache Hit Rate | >80% |
| Cost Savings | >70% |
| Prefix Stability | 95% |
| Serialization Stability | 100% |

## Cost Impact Example

**Before Optimization:**
```
Cache hit rate: 20%
Cost per task: $0.135
```

**After Optimization:**
```
Cache hit rate: 85%
Cost per task: $0.040
Savings: 70%
```

**Breakdown:**
- System prompt (cached): 5K × $0.30 = $0.0015
- Tool definitions (cached): 10K × $0.30 = $0.003
- Session context (cached): 15K × $0.30 = $0.0045
- Dynamic context (uncached): 15K × $3.00 = $0.045
- **Total**: $0.054 (was $0.135)
