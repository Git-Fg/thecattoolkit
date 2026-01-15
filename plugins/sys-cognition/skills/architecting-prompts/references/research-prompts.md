# Research Prompt Library

## Operational Protocol

These prompts transform AI from a "cool toy" into a research weapon capable of performing 10 hours of work in 60 seconds. They operationalize critical thinking frameworks into copy-paste templates.

**Usage Pattern:**
1. Identify the cognitive mode you need (Critique, Synthesis, Inversion, Meta)
2. Select the appropriate prompt template
3. Replace `{{content}}` with your material
4. Apply directly or adapt variables as needed

**Framework Synergies:**
These prompts map to thinking-frameworks methodologies:
- **First-Principles**: Contradictions Finder, Explain Backwards, Assumption Stress Test, Translate Across Domains
- **Inversion**: Reviewer #2, What Would Break This?, Assumption Stress Test
- **Second-Order Thinking**: Turn Into Paper, What Changed My Mind?
- **Occam's Razor**: One-Page Mental Model
- **Via Negativa**: Reviewer #2, Steal the Structure

---

## Critique Mode (Adversarial Analysis)

### 1. Contradictions Finder
**Framework:** First-Principles + Inversion
**Use When:** Auditing logical consistency of arguments, papers, reports, or long documents

**Template:**
```
Analyze {{content}}.

List all internal contradictions, unresolved tensions, or claims that don't fully follow from the evidence.

For each finding:
1. Quote the contradicting statements
2. Explain the tension
3. Rate severity: Minor | Moderate | Critical
```

**Example Application:**
> Input: Academic paper on climate policy
> Output: Identifies contradiction between stated goals and proposed timeline, flags unsupported causal claims

**Pro Tip:** Pair with "Assumption Stress Test" for comprehensive logical audit.

---

### 2. Reviewer #2 (Skeptical Peer Review)
**Framework:** Inversion + Via Negativa
**Use When:** Need harsh, honest critique before publication/presentation

**Template:**
```
Critique {{content}} like a skeptical peer reviewer. Be harsh.

Focus on:
- Methodology flaws
- Missing controls
- Overconfident claims
- Unsupported conclusions

Do NOT soften feedback. Identify the 3 most damaging weaknesses.
```

**Example Application:**
> Input: Business proposal claiming 300% ROI
> Output: Exposes lack of market validation, missing competitive analysis, unrealistic assumptions

**Pro Tip:** Use after initial draft to identify blind spots before sharing.

---

### 3. Assumption Stress Test
**Framework:** First-Principles + Inversion
**Use When:** Testing the foundation of an argument before building on it

**Template:**
```
List every assumption {{content}} relies on.

Now tell me which ones are most fragile and why.

Rate each assumption:
- Foundation: Core truth that cannot be questioned
- Plausible: Reasonable but unproven
- Fragile: Weak, untested, or likely false
```

**Example Application:**
> Input: Startup pitch about AI disruption
> Output: Identifies assumptions about market readiness, technology maturity, regulatory environment

**Pro Tip:** This is the "5-Whys" of argument analysis—dig until you hit system-level assumptions.

---

## Synthesis Mode (Knowledge Compression)

### 4. Turn Into Paper (Structured Research Brief)
**Framework:** Second-Order + SWOT
**Use When:** Converting raw notes, links, or half-baked ideas into structured research

**Template:**
```
Turn the following material into a structured research brief:

{{content}}

Include:
- Key claims
- Evidence supporting each claim
- Assumptions underlying the research
- Counterarguments
- Open questions
- Anything weak or missing

Flag any claims that lack sufficient evidence.
```

**Example Application:**
> Input: Collection of news articles about industry trends
> Output: Structured brief with 3 main claims, supporting data, identified gaps

**Pro Tip:** This replaces hours of manual cleanup and structuring.

---

### 5. One-Page Mental Model
**Framework:** Occam's Razor + Pareto
**Use When:** Compressing complex topics into memorable, actionable models

**Template:**
```
Compress {{content}} into a single mental model I can remember.

Requirements:
- Fits on one page
- Contains core insight (not just facts)
- Uses analogy or metaphor for memorability
- Provides decision-making framework

If it can't compress, I don't own it yet.
```

**Example Application:**
> Input: Complex technical architecture
> Output: "Layered onion" model showing dependency hierarchy and change propagation

**Pro Tip:** Use this to create personal knowledge frameworks, not just summaries.

---

### 6. Translate Across Domains
**Framework:** First-Principles
**Use When:** Understanding concepts through analogies from different fields

**Template:**
```
Explain {{content}} using analogies from a completely different field.

Requirements:
- Use field: [specify field, e.g., biology, engineering, sports]
- Explain core mechanism
- Highlight transferable principles
- Identify what breaks in the analogy

This unlocks insight, not just understanding.
```

**Example Application:**
> Input: Blockchain technology
> Output: Explained as "distributed ledger like a village record-keeping system with multiple trusted scribes"

**Pro Tip:** Compare multiple analogies to find the most robust explanation.

---

## Inversion Mode (Backward Reasoning)

### 7. Explain It Backwards
**Framework:** First-Principles + 5-Whys
**Use When:** Validating understanding by reconstructing from conclusion

**Template:**
```
Explain {{content}} backwards:

1. Start with the conclusion/finding
2. Work backward step by step to the assumptions
3. For each step, identify:
   - What must be true for this to follow?
   - What evidence supports this link?
   - Where could the chain break?

If the logic collapses, I'll see it immediately.
```

**Example Application:**
> Input: Complex financial model prediction
> Output: Step-by-step deconstruction revealing hidden assumptions about market behavior

**Pro Tip:** This exposes circular reasoning and logical gaps.

---

### 8. What Would Break This?
**Framework:** Inversion
**Use When:** Forecasting realistic failure modes and system robustness

**Template:**
```
Describe scenarios where {{content}} fails catastrophically.

Requirements:
- Not edge cases—realistic failure modes
- Multiple failure cascades
- Identify triggering conditions
- Assess probability and impact

Most people never ask this question.
```

**Example Application:**
> Input: SaaS growth strategy
> Output: Identifies market saturation, competitive response, customer acquisition cost explosion

**Pro Tip:** Combine with "Assumption Stress Test" for complete risk analysis.

---

### 9. What Changed My Mind?
**Framework:** Second-Order + Opportunity-Cost
**Use When:** Triggering belief updates and evidence-based reasoning

**Template:**
```
After analyzing {{content}}, what should change my current belief?

Requirements:
- Specific evidence that would flip my position
- Quantified thresholds (e.g., "If X happens 70% of the time...")
- Time-based triggers (e.g., "If no progress in 6 months...")
- Early warning indicators

This is how real researchers think.
```

**Example Application:**
> Input: Investment thesis
> Output: Clear criteria for exit strategy and position reevaluation

**Pro Tip:** Build in automatic reevaluation triggers, not just passive monitoring.

---

## Meta Mode (Structural Analysis)

### 10. Compare Like a Scientist
**Framework:** Opportunity-Cost + SWOT
**Use When:** Rigorous comparison of approaches, not just feature lists

**Template:**
```
Compare {{approach_a}} vs {{approach_b}} across:
- Theoretical grounding
- Failure modes
- Scalability constraints
- Real-world applicability
- Hidden costs/trade-offs

This is comparison, not feature listing.
```

**Example Application:**
> Input: Monolith vs microservices architecture
> Output: Systematic comparison of operational complexity, team structure, scaling patterns

**Pro Tip:** Focus on trade-offs, not advantages. Every solution has costs.

---

### 11. Steal the Structure
**Framework:** Via Negativa + Meta-cognition
**Use When:** Analyzing successful arguments, papers, or presentations to extract reusable patterns

**Template:**
```
Ignore the content of {{content}}. Analyze the structure:

- Argument flow pattern
- Evidence sequencing
- Rhetorical techniques
- Cognitive biases leveraged
- Why this structure works so well

Extract the reusable template.
```

**Example Application:**
> Input: Compelling TED Talk
> Output: Pattern: Hook → Problem → Journey → Solution → Vision (with specific techniques at each step)

**Pro Tip:** Apply this to great writing across domains to build a personal pattern library.

---

## Prompt Combinations (Advanced)

### Critical Analysis Combo
1. **Contradictions Finder** → Surface inconsistencies
2. **Assumption Stress Test** → Identify fragile foundations
3. **Reviewer #2** → Apply harsh peer review
4. **What Would Break This?** → Stress test robustness

### Synthesis Combo
1. **Turn Into Paper** → Structure raw material
2. **One-Page Mental Model** → Compress to essence
3. **Translate Across Domains** → Create memorable analogies

### Validation Combo
1. **Explain It Backwards** → Validate logic chain
2. **What Changed My Mind?** → Define evidence thresholds
3. **Compare Like a Scientist** → Benchmark against alternatives

---

## Source & Attribution

These prompts were collected by Chris Laub (@ChrisLaubAI) from viral posts across Reddit, X, and research communities. They represent the most effective prompt patterns for research and critical analysis.

**Original Thread:** "I collected every Claude prompt that went viral on Reddit, X, and research communities. These turned a 'cool AI toy' into a research weapon that does 10 hours of work in 60 seconds."

**Framework Mapping:** Operationalized using thinking-frameworks methodologies from the Cat Toolkit system.
