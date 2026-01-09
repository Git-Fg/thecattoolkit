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
