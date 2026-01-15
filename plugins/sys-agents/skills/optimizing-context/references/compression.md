# Context Compression Reference

Detailed techniques for reducing token usage while preserving task-relevant information.

## The Three Compression Techniques

### 1. Observation Masking (0% Token Overhead)

Replace full tool outputs with file references stored outside context window.

**Implementation:**
```javascript
function executeWithMasking(toolCall) {
  const fullResult = executeTool(toolCall)
  const refPath = `/results/${toolCall.type}_${timestamp}.txt`
  writeFile(refPath, fullResult)

  return {
    masked: true,
    reference: refPath,
    summary: summarize(fullResult, 50),
    tokenCount: fullResult.length
  }
}
```

**When to Use:**
- Tool outputs exceed 200 tokens
- Information likely not needed immediately
- Can retrieve on-demand if needed

### 2. Summarization (5-7% Token Overhead)

Use LLM to compress context while preserving semantic meaning.

**Compression Trigger Points:**

| Context Utilization | Method | Expected Reduction |
|---------------------|--------|-------------------|
| 60-80% | Light summarization | 60-70% |
| 80-95% | Aggressive compression | 80-90% |
| >95% | Emergency compaction | 90%+ |

**Structured Summary Template:**
```markdown
# Context Compression Summary

## Task Context
- Current task: [Brief description]
- Priority: [High/Medium/Low]

## Files Modified
- [path/to/file]: [Brief change description]

## Key Decisions
1. [Decision 1] - Reason: [Why]

## Next Steps
- [ ] Action 1

## Masked References
- Full output stored at: /results/[timestamp].txt
```

### 3. Compaction (Dynamic Token Management)

Remove stale information while preserving recent context at full fidelity.

**Multi-tier Strategy:**

| Age Tier | Compression | Token Budget |
|----------|------------|--------------|
| Recent (last 10) | 0% | 5,000 tokens |
| Medium (10-40) | 50% | 3,000 tokens |
| Old (40-100) | 80% | 2,000 tokens |

## Compression Decision Flow

```
Context Check → Utilization %
├── < 60%: Keep as-is
├── 60-80%: Light Summarization (60-70% reduction)
├── 80-95%: Aggressive Compression (80-90% reduction)
└── > 95%: Emergency Compaction (90%+ reduction)
```

## Quality Metrics

| Metric | Target |
|--------|--------|
| Compression Ratio | 60-90% reduction |
| Information Preservation | >95% of critical info |
| Retrieval Accuracy | >90% for needed details |
| Performance Impact | <5% task slowdown |

## Cost Impact Example

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Tokens per task | 45,000 | 12,000 | 73% |
| Cost per task | $0.45 | $0.12 | 73% |
| Latency | 8.2s | 6.1s | 26% |
