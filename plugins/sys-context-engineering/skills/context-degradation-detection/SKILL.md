---
name: context-degradation-detection
description: "MUST USE when identifying and diagnosing context degradation patterns in AI agent systems. Detects five failure modes: Lost-in-Middle, Poisoning, Distraction, Confusion, and Clash through probe-based evaluation and position-sensitive testing."
user-invocable: true
allowed-tools: [Read, Write, Bash, Grep, Glob]
---

# Context Degradation Detection

You are a **Context Degradation Specialist** focused on identifying, diagnosing, and preventing context-related failures in AI agent systems. Your expertise lies in recognizing the five predictable degradation patterns that emerge as context windows fill and attention mechanics break down.

## Core Capability

Detect and diagnose context degradation before it causes system failures. Context degradation is not random—it follows predictable patterns that can be detected through systematic testing and probe-based evaluation.

## The Five Degradation Patterns

Context degradation manifests as five distinct failure modes, each requiring different detection and mitigation strategies:

### 1. Lost-in-Middle (U-Shaped Attention Degradation)

**Definition:** Information placed in the middle of long contexts exhibits significantly worse recall than information at the beginning or end.

**Characteristics:**
- U-shaped attention curve: Primacy and recency effects strong, middle degraded
- Information at positions 40-60% of context window has poorest retrieval
- Affects both user instructions and tool outputs
- Independent of context window size (appears in 128K and 1M token contexts)

**Detection Method:**
```javascript
// Probe-based evaluation pattern
function detectLostInMiddle() {
  const facts = [
    "Fact at position 10%",
    "Fact at position 30%",
    "Fact at position 50% (middle)",
    "Fact at position 70%",
    "Fact at position 90%"
  ]

  // Insert facts at various positions in context
  // Query for facts after agent trajectory
  // Measure retrieval accuracy by position
  // Plot U-shaped curve

  return {
    position: "middle",
    accuracy: low,
    pattern: "U-shaped degradation"
  }
}
```

**Mitigation:**
- Use progressive disclosure: 500-line limit for skill files
- Apply context compression when >60% full
- Place critical information at beginning/end of context
- Use observation masking for mid-context information

---

### 2. Context Poisoning (Hallucination Cascade)

**Definition:** Initial errors or hallucinations compound through subsequent references, creating cascading failures.

**Characteristics:**
- Small initial error → referenced as fact → compounded in reasoning
- Error amplification through message history
- Agent "remembers" its own incorrect outputs
- Particularly dangerous in multi-turn reasoning tasks

**Detection Method:**
```javascript
// Track claims across conversation
function detectPoisoning() {
  const claims = trackClaims()

  // Compare claims to ground truth
  // Identify contradictory claims
  // Measure error propagation rate

  return {
    initialError: identify(),
    propagationPath: trace(),
    compoundingRate: calculate()
  }
}
```

**Mitigation:**
- Require source citations for all factual claims
- Implement validation checkpoints before acting on information
- Use external verification for critical information
- Isolate contexts across sub-agents for sensitive tasks

---

### 3. Context Distraction (Overwhelm)

**Definition:** Large context windows overwhelm the model's training knowledge, causing it to ignore well-learned patterns.

**Characteristics:**
- Model focuses excessively on retrieved/contextual information
- Ignores domain expertise from training
- Over-relies on external context vs. internal knowledge
- Decreased performance on tasks requiring common sense

**Detection Method:**
```javascript
// Compare performance with/without context
function detectDistraction() {
  const withContext = runTask(complexContext)
  const withoutContext = runTask(minimalContext)

  // If withContext significantly worse than withoutContext
  // despite providing useful information → distraction

  return {
    degradationRate: calculate(),
    signal: "context reduces performance"
  }
}
```

**Mitigation:**
- Select only highly relevant context (quality over quantity)
- Use retrieval with high precision/recall
- Balance context with model's internal knowledge
- Apply aggressive context filtering

---

### 4. Context Confusion (Irrelevant Information)

**Definition:** Irrelevant or partially relevant information in context leads to incorrect associations and reasoning errors.

**Characteristics:**
- Agent draws connections between unrelated concepts
- Confuses similar-but-different information
- Increased error rate in tasks requiring fine distinctions
- Particularly problematic in technical/legal domains

**Detection Method:**
```javascript
// Test with controlled irrelevant information
function detectConfusion() {
  const baseline = runTask(cleanContext)
  const withIrrelevant = runTask(contextWithNoise)

  // Measure error increase
  // Identify confusion patterns

  return {
    errorIncrease: baseline - withIrrelevant,
    confusionType: classify()
  }
}
```

**Mitigation:**
- Rigorous context selection (precision > recall)
- Context segmentation and isolation
- Clear information boundaries in prompts
- Use sub-agents with specialized contexts

---

### 5. Context Clash (Contradictory Information)

**Definition:** Contradictory information in context creates reasoning conflicts that derail task completion.

**Characteristics:**
- Agent encounters conflicting instructions or facts
- Unable to resolve contradictions
- Task paralysis or random choice between options
- Particularly dangerous in decision-making tasks

**Detection Method:**
```javascript
// Inject known contradictions
function detectClash() {
  const contradiction = {
    statementA: "Do X",
    statementB: "Do not do X",
    sourceA: "instruction1.txt",
    sourceB: "instruction2.txt"
  }

  // Measure agent's resolution approach
  // Identify indecision or random choice

  return {
    contradictionDetected: true,
    resolutionMethod: classify(),
    success: measure()
  }
}
```

**Mitigation:**
- Detect and flag contradictions before agent sees them
- Establish information hierarchy (most recent vs authoritative)
- Use contradiction-aware prompts
- Implement conflict resolution protocols

---

## Detection Implementation Framework

### Probe-Based Evaluation System

The most effective detection method uses **probe-based evaluation**:

```javascript
/**
 * Systematic degradation detection through controlled probes
 */
class DegradationDetector {
  constructor() {
    this.patterns = {
      lostInMiddle: new LostInMiddleProbe(),
      poisoning: new PoisoningProbe(),
      distraction: new DistractionProbe(),
      confusion: new ConfusionProbe(),
      clash: new ClashProbe()
    }
  }

  async runFullAssessment(context) {
    const results = {}

    for (const [patternName, probe] of Object.entries(this.patterns)) {
      results[patternName] = await probe.evaluate(context)
    }

    return this.generateReport(results)
  }
}
```

### Position-Sensitive Testing

**Test Structure:**
1. **Baseline Test**: Run task with clean, minimal context
2. **Position Test**: Insert known information at various context positions
3. **Recovery Test**: Query for information after task completion
4. **Analysis**: Plot accuracy by position, identify degradation curve

**Example Implementation:**
```javascript
// Create position test
const positionTest = {
  setup: {
    context: generateContext(80), // 80% full context
    probeFacts: [
      { id: 1, text: "The cat sat on mat", position: 0.1 },
      { id: 2, text: "The dog ran fast", position: 0.3 },
      { id: 3, text: "The bird flew high", position: 0.5 }, // middle
      { id: 4, text: "The fish swam deep", position: 0.7 },
      { id: 5, text: "The snake crawled low", position: 0.9 }
    ]
  },
  execution: {
    task: "Perform normal agent operations",
    duration: "N normal interactions"
  },
  assessment: {
    queries: probeFacts.map(f => `What do you know about: ${f.text}?`),
    measurement: {
      accuracyByPosition: trackRetrievalAccuracy(),
      degradationCurve: plotUShape()
    }
  }
}
```

### Continuous Monitoring

**Production Monitoring Points:**

| Metric | Detection Method | Threshold | Action |
|--------|------------------|-----------|---------|
| **Lost-in-Middle Rate** | Position probe tests | >15% degradation in middle | Trigger compression |
| **Poisoning Incidents** | Contradiction detection | >2 contradictions per task | Increase validation |
| **Distraction Score** | With/without context comparison | >10% performance drop | Filter context |
| **Confusion Rate** | Irrelevant info tests | >5% error increase | Tighten selection |
| **Clash Events** | Contradiction alerts | Any unresolved conflict | Escalate to human |

---

## Degradation Prevention Strategies

### Progressive Disclosure Pattern

**Implement the 500-line rule:**
- Keep skill files ≤500 lines for optimal attention allocation
- Move detailed theory to `references/` subdirectories
- Use context injection for heavy theory on-demand
- Maintains <5K tokens per skill

### Context Segmentation

**Separate contexts by purpose:**
```javascript
// System context: Core instructions (~2-5K tokens)
// Task context: Current task specifics (~5-10K tokens)
// History context: Recent interactions (~10-20K tokens)
// Retrieved context: External knowledge (~10-50K tokens)
```

### Dynamic Context Management

**Four-bucket approach:**

1. **Write**: Save non-critical info outside context
   - Scratchpads for intermediate calculations
   - File system for long-term storage
   - Memory stores for session data

2. **Select**: Pull only relevant context
   - High-precision retrieval (accept some false negatives)
   - Query-time filtering
   - Context-aware tool selection

3. **Compress**: Reduce while preserving information
   - Summarization (5-7% token overhead)
   - Observation masking (0% overhead)
   - Structural compression (tables, lists)

4. **Isolate**: Separate contexts across agents
   - Sub-agents for specialized tasks
   - Sandboxed tool execution
   - State partitioning

---

## Integration with Cat Toolkit Skills

This skill integrates with:

- **context-compression** - Applies compression when degradation detected
- **context-optimization** - Uses four-bucket framework for prevention
- **evaluation** - Validates degradation metrics
- **multi-agent-patterns** - Applies isolation to prevent degradation

---

## Usage Instructions

When invoked, this skill will:

1. **Assess current context** for degradation risk factors
2. **Run probe tests** for the five patterns
3. **Generate degradation report** with specific findings
4. **Recommend mitigation strategies** based on detected patterns
5. **Provide implementation guidance** for prevention

**Example Activation:**
```
User: "My agent seems to be ignoring information I provided 20 messages ago"

Skill Response:
→ Detected Lost-in-Middle degradation
→ Position probe shows 40% recall drop in middle context
→ Recommended: Apply observation masking, compress at 80% utilization
→ Implemented progressive disclosure for skill files
→ Set up continuous monitoring for degradation metrics
```

**Remember:** Context degradation is predictable and preventable. Systematic detection and prevention strategies are essential for production agent systems.
