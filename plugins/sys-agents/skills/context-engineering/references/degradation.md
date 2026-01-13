# Context Degradation Detection Reference

Identifying and preventing context-related failures in AI agent systems.

## The Five Degradation Patterns

### 1. Lost-in-Middle (U-Shaped Attention)

**Definition:** Information at positions 40-60% of context window has poorest retrieval.

**Characteristics:**
- U-shaped attention curve
- Independent of context window size
- Affects both instructions and tool outputs

**Detection:**
```javascript
const positions = [0.1, 0.3, 0.5, 0.7, 0.9]
// Insert facts at each position
// Query after agent operations
// Plot retrieval accuracy by position
// If middle (0.5) shows >15% lower accuracy → Lost-in-Middle
```

**Mitigation:**
- Place critical info at beginning/end
- Apply compression when >60% full
- Use observation masking for mid-context

### 2. Context Poisoning (Hallucination Cascade)

**Definition:** Initial errors compound through subsequent references.

**Characteristics:**
- Small error → referenced as fact → compounded
- Agent "remembers" incorrect outputs
- Dangerous in multi-turn reasoning

**Mitigation:**
- Require source citations for factual claims
- Validation checkpoints before acting on information
- External verification for critical information

### 3. Context Distraction (Overwhelm)

**Definition:** Large context overwhelms model's training knowledge.

**Characteristics:**
- Over-relies on external context
- Ignores domain expertise from training
- Decreased performance on common-sense tasks

**Detection:**
```javascript
const withContext = runTask(complexContext)
const withoutContext = runTask(minimalContext)
// If withContext significantly worse → distraction
```

**Mitigation:**
- Quality over quantity in context selection
- Use high precision retrieval
- Balance context with internal knowledge

### 4. Context Confusion (Irrelevant Information)

**Definition:** Irrelevant information leads to incorrect associations.

**Characteristics:**
- Draws connections between unrelated concepts
- Increased error rate in fine distinctions
- Problematic in technical/legal domains

**Mitigation:**
- Rigorous context selection (precision > recall)
- Clear information boundaries in prompts
- Use sub-agents with specialized contexts

### 5. Context Clash (Contradictory Information)

**Definition:** Contradictory information creates reasoning conflicts.

**Characteristics:**
- Unable to resolve contradictions
- Task paralysis or random choice
- Dangerous in decision-making tasks

**Mitigation:**
- Detect and flag contradictions before agent sees them
- Establish information hierarchy (recent vs authoritative)
- Use contradiction-aware prompts

## Continuous Monitoring

| Metric | Threshold | Action |
|--------|-----------|--------|
| Lost-in-Middle Rate | >15% middle degradation | Trigger compression |
| Poisoning Incidents | >2 contradictions/task | Increase validation |
| Distraction Score | >10% performance drop | Filter context |
| Confusion Rate | >5% error increase | Tighten selection |
| Clash Events | Any unresolved conflict | Escalate to human |

## Prevention Strategies

### Progressive Disclosure Pattern
- Keep skill files ≤500 lines
- Move detailed theory to `references/`
- Context injection for heavy theory on-demand

### Four-Bucket Approach
1. **Write**: Save to files outside context
2. **Select**: Pull only relevant context
3. **Compress**: Reduce while preserving info
4. **Isolate**: Separate contexts across agents
