# Core Standards: 2026 Complexity-Based Guidance

## 1. Attention Management Philosophy

**The Fundamental Principle:**

> "When designing prompts, your goal is **Attention Management**. Use Markdown headers to organize the hierarchy of thought. Use XML tags (Max 15, No Nesting) ONLY as semantic envelopes to isolate high-noise data from high-priority instructions."

**The Attention Economy:**
Every token competes with conversation history for model attention. Assume Claude is already intelligent.
- **Does Claude already know this?** → Omit common knowledge
- **Is this explanation necessary?** → Be direct
- **Does this justify its token cost?** → Value-based inclusion

## 2. Sycophancy Prevention (Truth-First)

**The Professional Objectivity Mandate:**

Prioritize technical accuracy and truthfulness over validating the user's beliefs. Focus on facts and problem-solving, providing direct, objective technical info without unnecessary superlatives, praise, or emotional validation.

**Key Behaviors:**
- If the user suggests a flawed path → CONTRADICT immediately
- Truth > Politeness. No "Great idea!" or "You're absolutely right!"
- Speed + Function > Enterprise Compliance
- Prototype-first. Skip complex hardening on local dev
- No corporate jargon. Speak in code, files, commands

**In Prompts:**
- Include explicit instruction: "Prioritize correctness over agreement"
- Add verification steps: "Verify all claims before output"
- Use structured reasoning with `<thinking>` blocks for complex decisions

## 3. Signal-to-Noise: XML vs Markdown Decision Matrix

### The Golden Rule
> **Start with Pure Markdown. Add XML only for explicit scaffolding of AI thinking OR data isolation.**

### Pattern Selection Flowchart

| Trigger | Pattern | XML Tags |
|:--------|:--------|:--------:|
| **Default** | Pure Markdown | 0 |
| Multi-phase execution | Hybrid (+ `<state>`) | 1-5 |
| Critical safety rules (NEVER/MUST) | Hybrid (+ `<constraints>`) | 1-5 |
| High-density data (>100 lines) | Hybrid (+ `<data>`) | 1-3 |
| Non-negotiable steps | Hybrid (+ `<workflow>`) | 1-5 |
| Internal reasoning | Hybrid (+ `<thinking>`) | 1-3 |
| Otherwise | Pure Markdown | 0 |

### XML Tag Hard-Cap

**Maximum 15 tags per prompt. Never nest XML tags.**

| Semantic Tag | Purpose | Usage |
|:-------------|:--------|:------|
| `<data>` | Isolate high-density data dumps | Raw logs, code blocks |
| `<workflow>` | Enforce strict step sequences | Non-negotiable procedures |
| `<constraints>` | Negative constraints (Safety/Security) | NEVER/MUST NOT rules |
| `<thinking>` | Isolate internal reasoning | CoT, complex decisions |
| `<output_format>` | Specify structural requirements | JSON, machine-parseable |
| `<state>` | Track execution phase | Multi-step workflows |
| `<example>` | Isolate few-shot demonstrations | Prevents example leakage |

### Anti-Patterns

| Pattern | Why Avoid | Alternative |
|:--------|:----------|:------------|
| Nested XML | `<workflow><step>...</step></workflow>` | Flat structure |
| XML for Simple Text | `<instruction>Summarize</instruction>` | Plain Markdown |
| Tag Soup | >5 tags in single prompt | Consolidate to Markdown |
| XML Headers | `<role>You are...</role>` | Use `## Role` |

## 4. Degrees of Freedom Matching

Match specificity to task fragility:

| Freedom | Characteristics | When to Use |
|:--------|:----------------|:------------|
| **High** | Multiple valid approaches, text-based heuristics | Creative tasks, exploration |
| **Medium** | Preferred pattern exists, pseudocode with parameters | Standard implementations |
| **Low** | Error-prone operations, exact scripts | Security, deployment, data migration |

## 5. Quota Optimization Principles

**Context Cost Hierarchy:**
1. **Inline Skill** (Cost: 1) - Uses current "RAM"
2. **Command** (Cost: 1) - Deterministic macro
3. **Forked Skill** (Cost: 3) - Isolated subagent
4. **Agent Task** (Cost: 2×N) - Parallel execution

**The Mega-Prompt Principle:**
Bundle multiple actions into a single turn. The model can perform ~15 internal operations (read, reason, write) for the cost of 1 prompt.

**Progressive Disclosure Value:**
Keep `SKILL.md` < 400 lines. Move heavy theory into `references/`. This reduces context rot while preserving knowledge depth.

## 6. Verification Standards

**Quality Gates:**
Add checklists inside prompts that the AI must verify before output.

```markdown
## Quality Gate
Before responding, ensure:
1. All security vulnerabilities are identified
2. Remediation steps are provided for each
3. Severity levels follow the defined scale
```

**Verification Steps:**
- Baseline Testing: Test with diverse set (simple, edge, complex, ambiguous)
- Metrics: Accuracy, format compliance, completeness, consistency
- A/B Validation: Compare optimized vs baseline using same inputs

## 7. Success Criteria

A prompt meets 2026 standards when:
- [ ] Uses Markdown headers for hierarchy (default)
- [ ] XML tags are < 15 and never nested
- [ ] Instructions are specific, actionable, and truth-focused
- [ ] Examples (if any) are isolated in `<example>` tags
- [ ] Reasoning is isolated in `<thinking>` blocks (if needed)
- [ ] Quality gate checklist is included
- [ ] Output format is clearly specified
