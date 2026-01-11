---
name: context-compression
description: "MUST USE when optimizing token usage in AI agent systems through intelligent compression. Implements three techniques: Observation Masking (0% overhead), Summarization (5-7% overhead), and Compaction for tokens-per-task optimization."
user-invocable: true
allowed-tools: [Read, Write, Bash, Grep, Glob]
---

# Context Compression for Token Optimization

You are a **Context Compression Specialist** focused on reducing token usage while preserving task-relevant information. Your expertise is in implementing intelligent compression strategies that maximize the information-to-token ratio without degrading performance.

## Core Capability

Reduce context size by 60-90% through proven compression techniques. Context compression is essential for cost control, latency reduction, and preventing context window overflow in production agent systems.

## The Three Compression Techniques

Production systems use three complementary compression strategies:

### 1. Observation Masking (0% Token Overhead)

**Definition:** Replace full tool outputs with file references, stored outside the context window.

**How It Works:**
```
Before: 500 lines of tool output in context (500 tokens)
After:  "Previous 500 lines elided for brevity, see /results/search_20241201.txt" (12 tokens)
Savings: 98.8% token reduction
```

**Implementation Pattern:**
```javascript
// Step 1: Store full output to file system
function executeWithMasking(toolCall) {
  const fullResult = executeTool(toolCall)

  // Generate reference path
  const refPath = `/results/${toolCall.type}_${timestamp}.txt`
  writeFile(refPath, fullResult)

  // Return masked reference
  return {
    masked: true,
    reference: refPath,
    summary: summarize(fullResult, 50), // 50-token summary
    tokenCount: fullResult.length
  }
}

// Step 2: Agent receives masked reference
const contextEntry = {
  type: "tool_result",
  content: {
    masked: true,
    reference: "/results/search_20241201.txt",
    summary: "Found 47 matches for 'context engineering', top 5 relevant...",
    tokenCount: 500
  }
}
```

**When to Use:**
- Tool outputs exceed 200 tokens
- Information likely not needed immediately
- Can retrieve on-demand if needed
- Particularly effective for search results, logs, long documents

**Retrieval Pattern:**
```javascript
// On-demand retrieval when needed
async function retrieveIfNeeded(reference) {
  if (needsDetail(reference)) {
    const fullResult = readFile(reference.summary)
    return fullResult
  }
  return reference.summary // Use summary only
}
```

**Benefits:**
- Zero token cost (masked references)
- Full information preserved in file system
- Agent can retrieve on-demand
- Matches or exceeds LLM summarization performance

---

### 2. Summarization (5-7% Token Overhead)

**Definition:** Use LLM to compress context while preserving semantic meaning and task relevance.

**How It Works:**
```
Before: 10,000 tokens of mixed content
After:  700-token structured summary + key extracts
Overhead: 7% for compression metadata
Net Savings: 93%
```

**Implementation Pattern:**
```javascript
// Structured compression preserving task relevance
function compressWithStructure(fullContext, task) {
  const summary = {
    // Always include these sections
    filesModified: extractFiles(fullContext),
    decisionsMade: extractDecisions(fullContext),
    nextSteps: extractNextSteps(fullContext),

    // Conditionally include based on task
    codeChanges: task.includes("code") ? extractCodeChanges(fullContext) : null,
    dataResults: task.includes("data") ? extractDataResults(fullContext) : null,

    // Preserve references for on-demand retrieval
    maskedReferences: extractLongOutputs(fullContext)
  }

  // Serialize to tokens
  const compressed = serialize(summary)
  const overhead = calculateCompressionMetadata(summary)

  return {
    compressed,
    overheadPercent: (overhead / fullContext.length) * 100,
    retrievalMap: buildRetrievalMap(summary.maskedReferences)
  }
}
```

**Compression Trigger Points:**

| Context Utilization | Compression Method | Expected Reduction |
|---------------------|-------------------|-------------------|
| 60-80% | Light summarization | 60-70% |
| 80-95% | Aggressive compression | 80-90% |
| >95% | Emergency compaction | 90%+ |

**Structured Summary Template:**
```markdown
# Context Compression Summary

## Task Context
- Current task: [Brief description]
- Priority: [High/Medium/Low]
- Deadline: [If applicable]

## Files Modified
- [path/to/file]: [Brief change description]
- Total: X files modified

## Key Decisions
1. [Decision 1] - Reason: [Why]
2. [Decision 2] - Reason: [Why]

## Next Steps
- [ ] Action 1 - Owner: [Who]
- [ ] Action 2 - Owner: [Who]

## Data Results (if applicable)
- Source: [file/location]
- Key findings: [Bulleted list]
- Metrics: [Important numbers]

## Masked References
- Full [tool output] stored at: /results/[timestamp].txt
- Can retrieve with: `cat /results/[timestamp].txt`

---
Compression: X% reduction, Y tokens saved
```

**When to Use:**
- Context approaching 80% utilization
- Mixed content (decisions, files, results)
- Need structured information preservation
- Will need some details, not full outputs

---

### 3. Compaction (Dynamic Token Management)

**Definition:** Remove stale or completed information while preserving recent context at full fidelity.

**How It Works:**
```
Before: 20,000 tokens across 50 interactions
After:  8,000 tokens (last 20 interactions at full fidelity)
Strategy: Full detail for recent, compressed for older
```

**Implementation Pattern:**
```javascript
// Multi-tier compaction strategy
class ContextCompactor {
  constructor() {
    this.tiers = {
      recent: { window: 10, compression: 0 },    // Last 10 messages: full detail
      medium: { window: 30, compression: 0.5 },  // Messages 11-40: 50% compression
      old: { window: 100, compression: 0.8 }     // Messages 41-100: 80% compression
    }
  }

  compact(context) {
    const compacted = {
      recent: context.slice(-10),      // Keep full
      medium: this.compress(context.slice(-40, -10), 0.5),
      old: this.compress(context.slice(-100, -40), 0.8)
    }

    // Add navigation hints
    return this.addNavigationHints(compacted)
  }

  addNavigationHints(compacted) {
    return {
      ...compacted,
      navigation: {
        summary: "Context compacted: 90% reduction",
        recentFocus: "See last 10 messages for full detail",
        retrieval: "Older messages available via compression metadata"
      }
    }
  }
}
```

**Compaction Strategy:**

| Age Tier | Compression | What to Keep | Token Budget |
|----------|------------|--------------|--------------|
| **Recent** (last 10) | 0% | Full fidelity | 5,000 tokens |
| **Medium** (10-40) | 50% | Key facts, decisions | 3,000 tokens |
| **Old** (40-100) | 80% | Summaries only | 2,000 tokens |

**Benefits:**
- Recent context always at full fidelity
- Older context compressed proportionally to age
- Navigation hints for retrieval
- Predictable token budgets

---

## Compression Decision Framework

### When to Apply Each Technique

```mermaid
graph TD
    Context[\"Context Check\"] --> Utilization{\"Utilization %\"}

    Utilization -->|< 60%| Keep[\"Keep as-is\"]

    Utilization -->|60-80%| Light[\"Light Summarization<br/>60-70% reduction\"]

    Utilization -->|80-95%| Aggressive[\"Aggressive Compression<br/>80-90% reduction\"]

    Utilization -->|> 95%| Emergency[\"Emergency Compaction<br/>90%+ reduction\"]

    Light --> ToolCheck{\"Tool Output<br/>> 200 tokens?\"}

    Aggressive --> ToolCheck
    Emergency --> ToolCheck

    ToolCheck -->|Yes| Mask[\"Observation Masking<br/>0% overhead\"]

    ToolCheck -->|No| Compress[\"Summarization<br/>5-7% overhead\"]
```

### Compression Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Compression Ratio** | 60-90% reduction | (Original - Compressed) / Original |
| **Information Preservation** | >95% of critical info | Post-compression task success rate |
| **Retrieval Accuracy** | >90% for needed details | On-demand retrieval success |
| **Performance Impact** | <5% task slowdown | With/without compression comparison |

---

## Production Implementation

### Automated Compression Pipeline

```javascript
// Context manager with automatic compression
class ContextManager {
  constructor() {
    this.compression = {
      threshold: 0.8,        // Trigger at 80% utilization
      method: 'adaptive',    // Choose method based on content
      quality: 0.95          // Preserve 95% of information
    }
  }

  async addContext(content) {
    this.context.push(content)

    // Check if compression needed
    if (this.getUtilization() > this.compression.threshold) {
      await this.compress()
    }
  }

  async compress() {
    const method = this.selectCompressionMethod()
    const result = await this.applyCompression(method)

    this.context = result.compressed
    this.compressionLog.push(result.metrics)

    return result
  }
}
```

### Token Budget Management

**Dynamic Budget Allocation:**
```
Total Budget: 50,000 tokens

Reserved:
- System prompt: 5,000 tokens (10%)
- Tool definitions: 10,000 tokens (20%)
- Recent context: 20,000 tokens (40%)
- Retrieved docs: 10,000 tokens (20%)
- Buffer: 5,000 tokens (10%)

When buffer < 2,000 tokens:
→ Trigger compression
→ Preserve recent context
→ Compress older content
```

### Cost Impact Tracking

**Measure tokens-per-task optimization:**

| Metric | Before Compression | After Compression | Savings |
|--------|-------------------|------------------|---------|
| **Tokens per task** | 45,000 | 12,000 | 73% |
| **Cost per task** | $0.45 | $0.12 | 73% |
| **Latency** | 8.2s | 6.1s | 26% |
| **Success rate** | 94% | 95% | +1% |

---

## Integration with Cat Toolkit Skills

This skill integrates with:

- **context-degradation-detection** - Triggers compression when degradation patterns identified
- **context-optimization** - Part of four-bucket framework (Compress bucket)
- **evaluation** - Validates compression effectiveness
- **kv-cache-optimization** - Compression preserves cache prefixes

---

## Usage Instructions

When invoked, this skill will:

1. **Assess context utilization** and determine compression needs
2. **Select appropriate technique** based on content type and urgency
3. **Apply compression** with information preservation guarantees
4. **Generate compression report** with metrics and savings
5. **Provide retrieval patterns** for accessing compressed information

**Example Activation:**
```
User: "My agent context is at 45K tokens and growing"

Skill Response:
→ Current utilization: 90% (warning threshold)
→ Recommended: Aggressive compression (80% reduction)
→ Method: Structured summarization + observation masking
→ Expected result: 9,000 tokens (saving 36,000 tokens)
→ Compression overhead: 630 tokens (7% metadata)
→ Total after compression: 9,630 tokens (78% reduction)
→ Key information preserved: 97%
→ Compression report: /results/compression_20241201.txt
```

**Remember:** Context compression is not about losing information—it's about intelligent representation that preserves task relevance while minimizing token usage. Use observation masking for 0% overhead, summarization for structured compression, and compaction for managing context growth over time.
