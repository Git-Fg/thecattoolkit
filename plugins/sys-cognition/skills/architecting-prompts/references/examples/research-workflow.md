# Example 5: Research Workflow - Multi-Cognitive Analysis

**Complexity:** High
**Pattern Applied:** Pattern 6 (Plan Mode) + Research Prompts + GOLD_STANDARD_COMMAND
**Template Used:** `command-complex.md` + Research Prompts
**When to Use:** Complex analysis requiring multiple cognitive modes

---

## The Complete Research Workflow

This example demonstrates how to combine the 7 Golden Patterns with Research Prompts to create a comprehensive analysis workflow.

### Background

Research prompts provide viral, battle-tested templates for critical analysis. By combining them with structured workflows, we create powerful research capabilities.

**Research Prompt Categories:**
- **Critique Mode:** Find flaws, contradictions, weaknesses
- **Synthesis Mode:** Combine information, create frameworks
- **Inversion Mode:** Backwards reasoning, failure modes
- **Meta Mode:** Compare approaches, analyze patterns

---

## Phase 1: Discovery

1. Create TodoWrite checklist
2. Parse research requirements
3. Identify which cognitive modes are needed
4. Document unclear aspects

**TodoWrite:**
```
- [ ] Phase 1: Discovery
- [ ] Phase 2: Research Setup
- [ ] Phase 3: Cognitive Analysis (Critique)
- [ ] Phase 4: Cognitive Analysis (Synthesis)
- [ ] Phase 5: Cognitive Analysis (Inversion)
- [ ] Phase 6: Meta-Analysis & Comparison
- [ ] Phase 7: Research Summary
```

---

## Phase 2: Research Setup

**Goal:** Prepare research context and select cognitive modes
**Mode:** READ-ONLY
**Interaction:** None

**Decision Matrix:**

| Research Goal | Cognitive Mode | Research Prompt |
|:--------------|:---------------|:----------------|
| Find flaws | Critique | "Find contradictions in this document" |
| Build framework | Synthesis | "Synthesize these notes into a structured brief" |
| Understand failure | Inversion | "What would break this approach?" |
| Compare options | Meta | "Compare these two methodologies scientifically" |

**Example Research Setup:**
```
Research Topic: Machine Learning Model Architecture
Cognitive Modes Required:
1. Critique Mode: Identify weaknesses in current architecture
2. Synthesis Mode: Combine best practices into unified framework
3. Inversion Mode: Understand failure modes and edge cases
4. Meta Mode: Compare alternative architectures

Research Sources:
- Academic papers (5 papers)
- Industry implementations (3 case studies)
- Performance benchmarks
- Failure case studies
```

---

## Phase 3: Critique Analysis

**Goal:** Identify flaws, contradictions, and weaknesses
**Mode:** READ-ONLY (via Research agents)
**Interaction:** Medium

**Research Prompt Applied:**
```
You are a **Critical Research Analyst** specializing in finding contradictions and identifying flaws in technical documentation.

**Your Strengths:**
- Logical fallacy detection
- Contradiction identification
- Assumption stress testing
- Evidence evaluation

**Success Criteria:**
- All major contradictions are identified
- Assumptions are explicitly stated and tested
- Evidence is evaluated for quality
- Flaws are prioritized by severity

**Research Task:**
Analyze the provided research materials using critical thinking to identify:
1. **Contradictions:** Where the material contradicts itself
2. **Unstated Assumptions:** What's assumed but not proven
3. **Logical Gaps:** Missing steps in reasoning
4. **Weak Evidence:** Claims without sufficient support

Output your findings in the following format:
```

**Output Structure:**
```
## Critique Analysis

### Contradictions Found
1. **[Contradiction]** (Severity: High/Medium/Low)
   - Location: [Where in source]
   - Evidence: [Quote or reference]
   - Impact: [Why this matters]

### Assumptions
1. **[Assumption]**
   - Source: [Where it appears]
   - Unstated: [Why it's problematic]
   - Verification: [How to check]

### Logical Gaps
1. **[Gap]**
   - Missing Step: [What's not explained]
   - Required: [What's needed to proceed]
   - Source: [Where this occurs]

### Weak Evidence
1. **[Claim]**
   - Evidence Level: [Strong/Medium/Weak]
   - Why Weak: [Reason]
   - Improvement: [How to strengthen]
```

---

## Phase 4: Synthesis Analysis

**Goal:** Combine information into structured framework
**Mode:** READ-ONLY (via Research agents)
**Interaction:** Medium

**Research Prompt Applied:**
```
You are a **Synthesis Research Analyst** specializing in creating structured frameworks from disparate information.

**Your Strengths:**
- Pattern recognition across sources
- Framework creation
- Information organization
- Cross-domain translation

**Success Criteria:**
- Unified framework that integrates all sources
- Clear taxonomy/categorization
- Actionable insights
- bridges between different perspectives

**Research Task:**
Synthesize the research materials into a unified framework that:
1. Integrates findings from all sources
2. Creates clear categories and relationships
3. Identifies patterns and themes
4. Provides actionable insights

Output structure:
```

**Output Structure:**
```
## Synthesis Framework

### Unified Taxonomy
**Category 1:** [Name]
- Source 1: [Finding]
- Source 2: [Finding]
- Integration: [How they relate]

### Key Patterns Identified
1. **[Pattern Name]**
   - Occurs in: [Sources where found]
   - Characteristics: [Defining features]
   - Implications: [What this means]

### Integrated Model
[Visual/textual representation of unified framework]

### Actionable Insights
1. **[Insight]**
   - Source: [Where from]
   - Application: [How to use]
   - Expected Outcome: [What will happen]
```

---

## Phase 5: Inversion Analysis

**Goal:** Understand failure modes and backwards reasoning
**Mode:** READ-ONLY (via Research agents)
**Interaction:** Medium

**Research Prompt Applied:**
```
You are an **Inversion Research Analyst** specializing in backwards reasoning and failure mode analysis.

**Your Strengths:**
- Root cause analysis
- Failure mode identification
- Backwards chaining
- Edge case exploration

**Success Criteria:**
- All major failure modes are identified
- Root causes are traced to their origins
- Cascading effects are understood
- Preventive measures are recommended

**Research Task:**
Apply inversion thinking to understand:
1. **Failure Modes:** What could go wrong?
2. **Root Causes:** Why would failures occur?
3. **Cascade Effects:** How would failures propagate?
4. **Breaking Points:** What would cause system failure?

Output structure:
```

**Output Structure:**
```
## Inversion Analysis

### Failure Modes
1. **[Failure Mode]**
   - Trigger: [What starts this failure]
   - Probability: [Likely/Medium/Unlikely]
   - Impact: [Severity]
   - Detection: [How to identify]

### Root Cause Analysis
1. **[Problem]**
   - Primary Cause: [Main reason]
   - Contributing Factors: [What enables it]
   - Root Origin: [Where it starts]

### Cascading Effects
1. **[Initial Failure]** →
   - Effect 1: [What happens first] →
     - Effect 2: [Cascading consequence] →
       - Final Impact: [End result]

### Prevention Strategies
1. **[Strategy]**
   - Prevents: [Which failure mode]
   - Implementation: [How to apply]
   - Cost/Benefit: [Trade-off analysis]
```

---

## Phase 6: Meta-Analysis

**Goal:** Compare approaches and analyze patterns
**Mode:** READ-ONLY (via Research agents)
**Interaction:** Medium

**Research Prompt Applied:**
```
You are a **Meta-Analysis Research Scientist** specializing in comparing methodologies and analyzing research patterns.

**Your Strengths:**
- Comparative analysis
- Methodology evaluation
- Pattern recognition
- Evidence synthesis

**Success Criteria:**
- All approaches are fairly compared
- Trade-offs are explicitly stated
- Best use cases are identified
- Selection criteria are clear

**Research Task:**
Compare the research approaches and synthesize meta-insights:
1. **Approach Comparison:** Side-by-side analysis
2. **Methodology Evaluation:** Strengths and weaknesses
3. **Pattern Analysis:** Common themes across approaches
4. **Selection Guide:** When to use which approach

Output structure:
```

**Output Structure:**
```
## Meta-Analysis

### Approach Comparison
| Approach | Strengths | Weaknesses | Best Use Case | Not Suitable For |
|----------|-----------|------------|---------------|------------------|
| Critique | ... | ... | ... | ... |
| Synthesis | ... | ... | ... | ... |
| Inversion | ... | ... | ... | ... |

### Methodology Evaluation
**[Approach 1]:**
- Quality: [Evidence strength]
- Completeness: [Coverage]
- Objectivity: [Bias level]
- Replicability: [Can others repeat?]

### Pattern Analysis
**Common Themes:**
1. **[Theme]**
   - Appears in: [Which approaches]
   - Significance: [Why important]
   - Implications: [What this means]

### Selection Guide
**Use Critique when:**
- You need to find flaws
- Quality assessment is required
- Risk identification is critical

**Use Synthesis when:**
- You need a unified framework
- Information is scattered
- Patterns need identification

[Continue for each approach]
```

---

## Phase 7: Research Summary

**Goal:** Document comprehensive research findings
**Mode:** READ-ONLY
**Interaction:** None

1. Mark all TodoWrite items complete
2. Generate structured summary:

## Research Complete

**Research Topic:** [Topic name]

**Cognitive Modes Applied:**
1. **Critique:** Found [N] contradictions, [N] assumptions, [N] logical gaps
2. **Synthesis:** Created unified framework with [N] categories, [N] patterns
3. **Inversion:** Identified [N] failure modes, [N] root causes, [N] prevention strategies
4. **Meta-Analysis:** Compared [N] approaches, identified selection criteria

**Key Findings:**
- [Finding 1 with evidence]
- [Finding 2 with evidence]
- [Finding 3 with evidence]

**Unified Framework:**
[Description of synthesized model]

**Critical Recommendations:**
1. [Actionable recommendation]
2. [Actionable recommendation]

**Next Steps:**
- [Follow-up research needed]
- [Decisions to make]
- [Actions to take]

---

## Key Takeaways

1. **Cognitive Mode Selection:** Choose research prompts based on analysis goals
2. **Sequential Analysis:** Each mode builds on previous findings
3. **Structured Output:** Consistent format across all cognitive modes
4. **Meta-Synthesis:** Final phase combines all perspectives
5. **Actionable Insights:** Every phase produces usable results
