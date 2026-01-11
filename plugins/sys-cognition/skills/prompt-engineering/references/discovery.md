# Prompt Discovery & Requirements Gathering

Use these questions to gather the context needed to build high-quality prompts.

## Universal Discovery Questions

1. **Objective**: "What is the primary goal of this prompt?"
2. **Success Criteria**: "How will we know if the output is successful?"
3. **Target Audience**: "Who is the intended consumer of the output?"
4. **Input Data**: "What specific information or files will be provided to the prompt?"

## Category-Specific Discovery

### For Single Prompts:
- "What is the required output format (Markdown, JSON, Code)?"
- "Are there any hard constraints (e.g., length, specific library versions)?"
- "Do you have any 'golden' examples of what a perfect output looks like?"

### For Prompt Chains:
- "Which phases are required (Research, Plan, Execute, Refine)?"
- "How does information flow between the steps?"
- "What is the final deliverable for the entire chain?"

### For Meta-Prompts:
- "What specific task should the generated prompts perform?"
- "What quality standards should the generated prompts follow?"
- "Are there specific prompt engineering patterns to prioritize?"

## Refinement Discovery (The "Why")

When refining an existing prompt, ask:
- "What specific issues are you seeing (e.g., hallucinations, wrong format)?"
- "Can you provide an example of a failure case?"
- "What would a 'perfect' fix look like for this issue?"

## Rules for Effective Discovery
- **2-4 questions max** per interaction to avoid overwhelming the user.
- **Provide options** when choices are knowable (e.g., "Would you prefer JSON or Markdown?").
- **Listen for constraints** mentioned in natural language and formalize them.

## Research Prompt Discovery Keywords

These keywords trigger the research prompt templates:

### Cognitive Mode Keywords

**Critique Mode:**
- critique, critical analysis, peer review
- review, audit, examine
- find contradictions, identify flaws
- stress test assumptions
- skeptical review

**Synthesis Mode:**
- synthesize, compress, summarize
- structure, organize, compile
- mental model, framework
- translate across domains, analogy
- turn into paper, research brief

**Inversion Mode:**
- inversion, backwards, backward reasoning
- failure modes, what would break
- explain backwards, deconstruction
- belief update, what changed my mind

**Meta Mode:**
- compare, comparison, scientist
- structure, pattern, framework
- steal structure, analyze pattern
- methodology, approach analysis

### Research Context Keywords

- research prompts, viral prompts
- analysis templates
- research weapon, research tool
- Reddit prompts, research communities
- critical thinking, analytical reasoning
- academic analysis, peer review style
- argument analysis, logic testing
- evidence evaluation, fact-checking

### Framework-Trigger Keywords

**When combined with thinking-frameworks:**
- First-Principles + "analyze assumptions" → Assumption Stress Test
- Inversion + "failure modes" → What Would Break This?
- Second-Order + "cascade effects" → What Changed My Mind?
- Occam's Razor + "simplify" → One-Page Mental Model

### Discovery Patterns

Users seeking research prompts typically say:
- "I need to critique this [paper/proposal/argument]"
- "How do I find contradictions in this document?"
- "I want to stress-test the assumptions in this theory"
- "Help me synthesize these notes into a structured brief"
- "What would break this approach?"
- "Compare these two methodologies scientifically"
- "Turn my raw notes into a research paper"

---

## Pattern Matching: User Intent → Solution

Use this matrix to quickly identify which pattern, template, or technique to apply.

### By Task Complexity

| If User Says... | Pattern/Template to Use | Why |
|:----------------|:------------------------|:-----|
| "Create a single prompt for..." | `single-prompt.md` | One-shot, direct execution |
| "I need a workflow with multiple steps" | `command-complex.md` | 7-phase structured approach |
| "Build a prompt that generates other prompts" | `meta/` templates | Higher-order prompt creation |
| "Create an agent for X task" | `agent-sub.md` | Specialized sub-agent definition |
| "Document how to use a tool" | `tool-prompt.md` | Tool instruction template |

### By Structural Pattern

| If Task Requires... | Use Pattern | Example |
|:-------------------|:-----------|:--------|
| **Negative constraints** | Pattern 2 (Hard Boundaries) | "Read-only", "Must not modify" |
| **Step-by-step execution** | Pattern 4 (Protocol Prerequisites) | "Must do A before B" |
| **Parallel work** | GOLD_STANDARD_COMMAND Phase 2 | Multiple agents working simultaneously |
| **User approval at checkpoints** | GOLD_STANDARD_COMMAND Phases 3, 4, 6 | "Wait for user selection" |
| **Demonstration of correct behavior** | Pattern 5 (Contrastive Examples) | Show good and bad examples |

### By Domain Expertise

| If Building Prompt For... | Use Persona Pattern | Example |
|:--------------------------|:-------------------|:--------|
| **Database optimization** | PostgreSQL DBA | Query analysis, indexing strategies |
| **Code review** | Senior Reviewer | Security, bugs, conventions |
| **Architecture design** | Software Architect | Trade-offs, patterns, scalability |
| **API integration** | Integration Specialist | Schema validation, error handling |
| **Security analysis** | Security Auditor | Threat modeling, compliance |

### By Problem Type

| If User's Goal Is... | Discovery Question | Recommended Pattern |
|:---------------------|:------------------|:-------------------|
| **I need to understand this code** | "What's the structure?" | Explore Agent Pattern |
| **I need to design an approach** | "What's the best way?" | Plan Agent Pattern |
| **I need to verify quality** | "Is this correct?" | Review Agent Pattern |
| **I need to find similar patterns** | "What's already there?" | Pattern Matching + Discovery |
| **I need to enforce constraints** | "What must not happen?" | Hard Boundaries Pattern |

### By Output Format

| If Output Must Be... | Template/Pattern | Structure |
|:---------------------|:-----------------|:----------|
| **Structured data (JSON/YAML)** | `output_format` in templates | `<output_format>` tag |
| **Code with explanations** | Structured CoT Pattern | `<thinking>` + code blocks |
| **Step-by-step guide** | Protocol Prerequisites | Numbered steps with prerequisites |
| **Comparative analysis** | Multi-Approach Pattern | Table with pros/cons/complexity |
| **Implementation plan** | Command Complex Template | 7-phase workflow |

### By Risk/Complexity Level

| Level | When to Use | Pattern | Approval Required |
|:------|:------------|:--------|:----------------|
| **Low** | Simple, well-defined tasks | Single Prompt | No |
| **Medium** | Tasks with trade-offs | Chain Template | Phase 4 |
| **High** | Complex, multi-phase work | Command Complex | Phases 3, 4, 6 |
| **Critical** | Production systems | Full Workflow + Review | All phases |

### By Cognitive Mode

| Mode | User Intent | Pattern/Template |
|:-----|:------------|:----------------|
| **Analysis** | "Break down this problem" | Chain-of-Thought Patterns |
| **Synthesis** | "Combine these elements" | Research Prompts (Synthesis) |
| **Evaluation** | "Judge quality/correctness" | Review Agent + Quality Gates |
| **Creation** | "Build something new" | Command Complex + Implementation |
| **Comparison** | "Compare options A and B" | Multi-Approach Pattern |

---

## Quick Decision Tree

```
START: User describes their need
  ↓
Is it a SINGLE, direct task?
  ├─ YES → Use single-prompt.md template
  └─ NO → Continue
  ↓
Does it require MULTIPLE PHASES?
  ├─ NO → Use chain/ templates
  └─ YES → Continue
  ↓
Does it need USER APPROVAL at checkpoints?
  ├─ NO → Use chain/ templates
  └─ YES → Continue
  ↓
Does it need PARALLEL AGENT EXECUTION?
  ├─ NO → Use chain/ templates
  └─ YES → Continue
  ↓
Use command-complex.md (GOLD_STANDARD_COMMAND)
```

---

## Pattern Selection Checklist

Before finalizing your prompt, verify:

- [ ] **Complexity Assessment**: Is this simple (single-prompt) or complex (command-complex)?
- [ ] **Phase Requirements**: Which phases from GOLD_STANDARD_COMMAND are needed?
- [ ] **Agent Types**: Which sub-agents (Explore, Plan, Review) are required?
- [ ] **Approval Gates**: Where must the user explicitly approve decisions?
- [ ] **Parallel Execution**: Can work be done simultaneously?
- [ ] **Output Structure**: What format must the final output take?
- [ ] **Domain Expertise**: What specialized persona is needed?
- [ ] **Risk Level**: What are the consequences of failure?

Based on your answers, select the appropriate pattern/template combination.

