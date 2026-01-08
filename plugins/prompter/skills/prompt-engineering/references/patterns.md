# Prompt Structure & Patterns

Advanced architectural patterns for structuring AI cognition and outputs.

## XML/Markdown Hybrid Framework

We use a simplified two-pattern model designed specifically for AI Agents (like Claude Code).

| Pattern | Tags | Use Case |
|:---|:---:|:---|
| **Pure Markdown** | 0 | Default for simple, linear workflows. |
| **Hybrid XML** | 1-5 | For structuring cognition, state, safety, and data isolation. |

### The Golden Rule
> **Start with Pure Markdown. Add XML only for explicit scaffolding of AI thinking OR data isolation.**

### Pattern Selection Flowchart
1. **Multi-phase execution?** → YES → Hybrid (+ `<state>`)
2. **Critical safety rules?** (NEVER/MUST NOT) → YES → Hybrid (+ `<constraints>`)
3. **Large data blocks?** (confusing instructions) → YES → Hybrid (+ `<context>`)
4. **Non-negotiable steps?** → YES → Hybrid (+ `<workflow>`)
5. **Otherwise** → Pure Markdown

## Semantic Logic Containers

Limit to **5 tags maximum** per prompt. Never nest XML tags.

| Tag | Purpose |
|:---|:---|
| `<context>` | Separate large data dumps from instructions. |
| `<workflow>` | Enforce strict, non-negotiable step sequences. |
| `<constraints>` | High-priority negative constraints (Safety/Security). |
| `<thinking>` | Isolate internal reasoning/monologue. |
| `<output_format>` | Specify machine-parseable or structural requirements. |

## Structural Components

A well-structured prompt typically follows this layout:

1. **Role/Identity**: Who the AI is.
2. **Context/Background**: What the AI needs to know.
3. **Task/Instructions**: What the AI needs to do.
4. **Constraints/Guidelines**: Constraints on performance.
5. **Examples**: Demonstration dataset.
6. **User Input**: The specific data to process.
7. **Output Specification**: How the result should look.

## Common Task Templates

### 1. Classification
```markdown
Classify the {content} into one of these categories: {categories}
Rules: [classification logic]
{content}: {user_input}
Category:
```

### 2. Extraction
```markdown
Extract {information} from the provided text.
Fields: {field_list}
Text: {user_input}
Result:
```

### 3. Transformation
```markdown
Transform {source_format} to {target_format}.
Rules: {transformation_logic}
Input: {user_input}
Output:
```

## Anti-Patterns to Avoid
- **Nested XML**: `<workflow><step>...</step></workflow>` (Too complex).
- **XML for Simple Text**: `<instruction>Summarize this</instruction>` (Unnecessary).
- **Tag Soup**: Using >5 tags in a single prompt.
- **Vague Roles**: "You are an AI." (Be specific: "You are a Senior Architect.")

## Success Criteria Checklist
- [ ] Pattern (Pure vs Hybrid) matches task complexity?
- [ ] ≤ 5 XML tags used?
- [ ] No nested XML tags?
- [ ] Markdown used for all general content?
- [ ] Output format clearly specified?
