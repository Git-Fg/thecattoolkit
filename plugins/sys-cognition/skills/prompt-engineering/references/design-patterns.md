# Design Patterns: Techniques & Structure

## Part 0: The 7 Golden Patterns (2026 Standards)

These foundational patterns represent the distilled best practices from analyzing actual Claude Code system prompts.

### Pattern 1: Specialized Persona Definition
**Core Principle:** Define role, domain, and success criteria immediately. Never use generic "helpful assistant."

**Structure:**
```markdown
You are a **[Specific Role]** specializing in **[Domain]**.
Your expertise lies in **[specific competencies]**.

**Your Strengths:**
- [Competency 1]
- [Competency 2]
- [Competency 3]

**Success Criteria:**
- [Criterion 1 with measurable outcome]
- [Criterion 2 with constraint]
- [Criterion 3 with quality gate]
```

**Example:**
```markdown
You are a **Senior PostgreSQL Database Administrator**.
Your goal is to optimize query performance without altering the underlying data schema unless absolutely necessary.

**Your Strengths:**
- Query plan analysis (EXPLAIN ANALYZE)
- Indexing strategies (B-Tree vs GIN/GiST)
- Vacuuming and maintenance configuration

**Success Criteria:**
- Reduced query execution time by >50%
- No degradation in write performance
- Zero downtime implementation
```

### Pattern 2: Hard Boundaries (Negative Constraints)
**Core Principle:** Use "Negative Prompting" to psychologically sandbox the model before technical sandboxing.

**Structure:**
```markdown
### OPERATIONAL BOUNDARIES
You are in **[Mode]**.

**=== CRITICAL: [MODE] MODE - [KEY RESTRICTION] ===**
You are STRICTLY PROHIBITED from:
- [Forbidden action 1]
- [Forbidden action 2]
- [Forbidden action 3]

**Why:** [Reasoning for each prohibition]
```

**Example (from Explore Agent):**
```markdown
**=== CRITICAL: READ-ONLY MODE - NO FILE MODIFICATIONS ===**
You are STRICTLY PROHIBITED from:
- Creating new files (no Write, touch, or file creation)
- Modifying existing files (no Edit operations)
- Deleting files (no rm)
- Moving or copying files
- Running ANY commands that change system state

Your role is EXCLUSIVELY to search and analyze existing code.
```

### Pattern 3: Dynamic Context Injection (Parsimonious XML)
**Core Principle:** Wrap dynamic context in XML tags, limit to 5-8 tag pairs maximum.

**Structure:**
```markdown
[Instruction text]

<env>
[Key 1]: [Value 1]
[Key 2]: [Value 2]
</env>

<file_contents filename="[name]">
[Content to process]
</file_contents>
```

**XML Tag Priority Matrix:**
| Priority | Tag Type | Purpose |
|:---------|:--------|:--------|
| 1 (Essential) | `<env>` | Runtime context injection |
| 2 (Essential) | `<example_correct>` / `<example_incorrect>` | Contrastive few-shot learning |
| 3 (High) | `<sub_agents>` | Sub-agent definitions |
| 4 (Medium) | `<file_contents>` | File data separation |
| 5 (Low) | `<thinking>` | Internal reasoning |

### Pattern 4: Protocol Prerequisites (Chain of Thought)
**Core Principle:** Enforce specific order of operations with mandatory prerequisites.

**Structure:**
```markdown
### DIAGNOSTIC PROTOCOL
Before [action], you MUST follow this sequence:

1. **Step 1:** [Specific verification]
2. **Step 2:** [Specific verification]
3. **Step 3:** [Specific verification]

ONLY after these steps are complete may you [perform action].

**Why this is non-negotiable:** [Consequence of skipping]
```

**Example (from MCP prompt):**
```markdown
**MANDATORY PREREQUISITE - THIS IS A HARD REQUIREMENT**
You MUST call `mcp-cli info <server>/<tool>` BEFORE ANY `mcp-cli call <server>/<tool>`.

**Why:** MCP tool schemas never match expectations. Even tools with pre-approved permissions require schema checks.

**Flow:**
1. `mcp-cli tools` (Discover)
2. `mcp-cli info <tool>` (Check Schema - **REQUIRED**)
3. `mcp-cli call <tool>` (Execute)
```

### Pattern 5: XML-Structured Few-Shot Examples
**Core Principle:** Provide contrastive examples to teach nuance.

**Structure:**
```markdown
<example_correct>
User: [Input scenario]
Assistant: [Desired response]
Reasoning: [Why this is correct]
</example_correct>

<example_incorrect>
User: [Same scenario]
Assistant: [Undesired response]
Reasoning: [Why this is wrong]
</example_incorrect>
```

### Pattern 6: Plan Mode Workflow (State Machines)
**Core Principle:** Separate "Thinking" from "Doing" through phased workflows.

**Structure:**
```markdown
**Plan mode is active.**
You MUST NOT make any edits or run non-readonly tools. You may only edit the plan file: `{{PLAN_FILE_PATH}}`.

**Workflow:**
1. **Phase 1 (Initial Understanding):** [Actions]
2. **Phase 2 (Design):** [Actions]
3. **Phase 3 (Review):** [Actions]
4. **Phase 4 (Final Plan):** [Actions]
5. **Phase 5 (Exit):** [Action]
```

### Pattern 7: Parsimonious XML Usage (5-8 Tag Rule)
**Core Principle:** Limit to 5-8 XML tag pairs maximum. Prioritize tags by semantic value.

**What to Convert to Markdown:**
- `<persona>` → **Bold header**
- `<success_criteria>` → **Numbered list**
- `<protocol>` → Steps listed directly
- `<output_format>` → Inline code block or table

**Bad Example (11+ tags):**
```markdown
<persona>...</persona>
<success_criteria>...</success_criteria>
<env>...</env>
<agent_persona type="Explore">...</agent_persona>
<protocol>...</protocol>
<example_correct>...</example_correct>
```

**Good Example (6 tags):**
```markdown
**Your Strengths:** [markdown list]
**Success Criteria:** [markdown list]

<env>...</env>

<sub_agents>
[All agent personas consolidated here]
</sub_agents>

<example_correct>...</example_correct>
<example_incorrect>...</example_incorrect>
```

---

## Part I: Reasoning Techniques

### Chain-of-Thought (CoT) Prompting

Encourage the model to break down complex problems into manageable steps.

#### 1. Zero-Shot CoT
Force reasoning with a simple trigger phrase. Use when you need quick logic for a straightforward query.

```
{query}

Let's think step by step:
```

**Use Case:** Simple logical deductions, straightforward multi-step problems.

#### 2. Structured CoT (Internal Monologue)
Dedicate a specific block for reasoning. This isolates "thinking" from the final answer.

```xml
<thinking>
1. Analyze requirements
2. Identify dependencies
3. Outline solution steps
</thinking>

Answer: [final output]
```

**Use Case:** When you want to see the reasoning process without having it contaminate the final output.

#### 3. Tree-of-Thought (Exploration)
Explore multiple reasoning branches for creative or complex decision-making.

```markdown
Problem: {problem}

Approach 1: {reasoning_path_1} → Result 1
Approach 2: {reasoning_path_2} → Result 2
Approach 3: {reasoning_path_3} → Result 3

Synthesis: The best approach is...
```

**Use Case:** Creative tasks, strategic decisions, when multiple valid approaches exist.

#### 4. Step-Back Prompting (Principles First)
Establish broader context/principles before solving specifics.

1. "Define the core principles for {domain}."
2. "Applying these principles, solve {problem}."

**Use Case:** Domain-specific problems where established principles should guide the solution.

### Example-Based Learning

Show, don't just tell, using isolated examples.

#### The Example Container Rule
**MANDATORY:** Always wrap each example in a flat `<example>` tag to prevent "example leakage."

```xml
<example>
  Input: [demonstration 1]
  Output: [desired result 1]
</example>
<example>
  Input: [demonstration 2]
  Output: [desired result 2]
</example>
```

#### Strategy Selection

| Strategy | When to Use | Example Count |
|:---------|:------------|:-------------:|
| **Zero-Shot** | Simple, well-defined tasks | 0 |
| **One-Shot** | Non-standard format or hard to explain | 1 |
| **Few-Shot** | Complex patterns, classification, style imitation | 3-8 |

#### Few-Shot Best Practices
- **Mix Classes:** In classification, don't group all "Positive" examples together. Shuffle them.
- **Distribution Match:** Use an example set that matches the expected real-world distribution.
- **Diversity:** Choose examples that represent different edge cases and variations.

### Advanced Reasoning Patterns

#### 1. Least-to-Most
Break a massive problem into a sequence of subproblems and solve them one by one, using previous answers as context for the next.

**Use Case:** Complex multi-stage problems where each stage builds on the previous.

#### 2. Verification Step
Add an explicit step where the model reviews its own reasoning for errors before finalizing.

```
"Now, verify all calculations and logical steps in your previous response."
```

**Use Case:** Mathematical problems, logical deductions, security analysis.

#### 3. Self-Consistency
Run the reasoning multiple times (internally) and select the most common final answer.

**Use Case:** Problems with multiple valid solution paths where consistency indicates correctness.

---

## Part II: Structural Patterns

### Prompt Architecture

A well-structured prompt typically follows this layout:

1. **Role/Identity:** Who the AI is
2. **Context/Background:** What the AI needs to know
3. **Task/Instructions:** What the AI needs to do
4. **Constraints/Guidelines:** Constraints on performance
5. **Examples:** Demonstration dataset
6. **User Input:** The specific data to process
7. **Output Specification:** How the result should look

### Common Task Templates

#### 1. Classification
```markdown
Classify the {content} into one of these categories: {categories}
Rules: [classification logic]
{content}: {user_input}
Category:
```

#### 2. Extraction
```markdown
Extract {information} from the provided text.
Fields: {field_list}
Text: {user_input}
Result:
```

#### 3. Transformation
```markdown
Transform {source_format} to {target_format}.
Rules: {transformation_logic}
Input: {user_input}
Output:
```

### XML/Markdown Hybrid Framework

We use a simplified two-pattern model designed specifically for AI Agents.

| Pattern | Tags | Use Case |
|:---|:---:|:---|
| **Pure Markdown** | 0 | **REQUIRED DEFAULT**. Use `# Context` and `# Assignment` headers. |
| **Hybrid XML** | 1-15 | For structuring cognition (`<thinking>`) or high-density data isolation ONLY. |

### Semantic Logic Containers

| Tag | Purpose | When to Use |
|:---|:--------|:------------|
| `<data>` | Isolate high-density data dumps | >50 lines of raw data |
| `<workflow>` | Enforce strict step sequences | Non-negotiable procedures |
| `<constraints>` | High-priority negative constraints | Safety/Security rules (NEVER/MUST) |
| `<thinking>` | Isolate internal reasoning | Complex decision-making |
| `<output_format>` | Specify structural requirements | JSON, machine-parseable output |
| `<example>` | Isolate few-shot demonstrations | Prevents example leakage |

### Prompt Taxonomy

#### 1. Single Prompts
Standalone, reusable prompts for direct, one-shot execution.
- **Storage:** `.cattoolkit/prompts/`
- **Template:** `assets/templates/single-prompt.md`

#### 2. Prompt Chains
Sequential multi-step workflows where output from one step feeds the next.
- **Storage:** `.cattoolkit/chains/{number}-{topic}/`
- **Pattern:** Research → Plan → Execute → Refine
- **Templates:** `assets/templates/chain/`

#### 3. Meta-Prompts
Higher-order prompts that generate, optimize, or analyze other prompts.
- **Storage:** `.cattoolkit/generators/`
- **Templates:** `assets/templates/meta/`

---

## Part III: Anti-Patterns

| Pattern | Why Avoid | Alternative |
|:--------|:----------|:------------|
| **Nested XML** | `<workflow><step>...</step></workflow>` (Too complex) | Flat structure |
| **XML for Simple Text** | `<instruction>Summarize this</instruction>` (Unnecessary) | Plain Markdown |
| **Tag Soup** | Using >5 tags in a single prompt | Consolidate to Markdown |
| **Vague Roles** | "You are an AI." (Not specific) | "You are a Senior Architect" |
| **Missing Examples** | Hard-to-explain formats without demos | Add 1-3 `<example>` blocks |
| **Unverified Output** | No self-check on reasoning | Add verification step |

---

## Part IV: Quality Checklist

Before finalizing a prompt, verify:

- [ ] Complexity requires CoT?
- [ ] Format requires examples?
- [ ] Examples isolated in `<example>` tags?
- [ ] Reasoning isolated in `<thinking>` tags?
- [ ] Verification step included?
- [ ] ≤ 15 XML tags used?
- [ ] No nested XML tags?
- [ ] Markdown used for all general content?
- [ ] Output format clearly specified?
- [ ] Examples shuffled (for classification)?
