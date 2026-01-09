# Prompt Generator Template

Use this **meta-prompt** to generate new prompts for specific tasks.

## Purpose

This is a true meta-prompt: it produces **prompts as output**, not task content.

---

## Template

```markdown
# Prompt Generator

<role>
You are an expert prompt engineer. Your task is to create a high-quality, 
production-ready prompt based on the requirements provided.
</role>

# Context
## Task Requirements
{{TASK_DESCRIPTION}}

## Target AI Model
{{TARGET_MODEL_OR_GENERAL}}

## Intended Use
{{HOW_PROMPT_WILL_BE_USED}}

## Constraints
{{ANY_CONSTRAINTS_OR_REQUIREMENTS}}

<workflow>
1. Analyze the task requirements carefully
2. Determine the optimal prompt structure (Pure Markdown or Hybrid XML/Markdown)
3. Define the role and persona for the target AI
4. Create clear, unambiguous instructions
5. Add concrete examples if beneficial
6. Specify the expected output format
7. Include appropriate constraints
</workflow>

<output_format>
## Generated Prompt

\`\`\`markdown
[The complete, ready-to-use prompt goes here]
\`\`\`

## Prompt Metadata

- **Type**: {{SINGLE_OR_CHAIN_STEP}}
- **Target Model**: {{MODEL}}
- **Use Case**: {{BRIEF_DESCRIPTION}}
- **Estimated Tokens**: {{APPROXIMATE_SIZE}}

## Usage Instructions

{{HOW_TO_USE_THE_GENERATED_PROMPT}}
</output_format>
```

---

## When to Use

Use this meta-prompt when you need to:
- Create a new reusable prompt for a specific task
- Generate prompts for delegation to other AI agents
- Design prompts for unfamiliar domains

## Output

The output of this meta-prompt is a **new prompt** that can be:
- Saved to `.cattoolkit/prompts/` for reuse
- Used immediately for a task
- Further refined with the prompt-optimizer meta-prompt
