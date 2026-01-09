# Core Prompting Techniques

Master fundamental techniques for eliciting high-quality reasoning and task performance.

## Chain-of-Thought (CoT) Prompting

Encourage the model to break down complex problems into manageable steps.

### 1. Zero-Shot CoT
Force reasoning with a simple trigger phrase. Use when you need quick logic for a straightforward query.
```
{query}

Let's think step by step:
```

### 2. Structured CoT (Internal Monologue)
Dedicate a specific block for reasoning. This isolates "thinking" from the final answer.
```xml
<thinking>
1. Analyze requirements
2. Identify dependencies
3. Outline solution steps
</thinking>

Answer: [final output]
```

### 3. Tree-of-Thought (Exploration)
Explore multiple reasoning branches for creative or complex decision-making.
```markdown
Problem: {problem}

Approach 1: {reasoning_path_1} → Result 1
Approach 2: {reasoning_path_2} → Result 2
Approach 3: {reasoning_path_3} → Result 3

Synthesis: The best approach is...
```

### 4. Step-Back Prompting (Principles First)
Establish broader context/principles before solving specifics.
1. "Define the core principles for {domain}."
2. "Applying these principles, solve {problem}."

## Example-Based Learning

Show, don't just tell, using isolated examples.

### The Example Container Rule
**MANDATORY**: Always wrap each example in a flat `<example>` tag to prevent "example leakage".

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

### Strategy Selection
- **Zero-Shot**: Use for simple, well-defined tasks (e.g., "Summarize this").
- **One-Shot**: Use when the format is non-standard or hard to explain.
- **Few-Shot (3-8 examples)**: Use for complex patterns, classification, or style imitation.

### Few-Shot Best Practices
- **Mix Classes**: In classification, don't group all "Positive" examples together. Shuffle them.
- **Distribution Match**: Use an example set that matches the expected real-world distribution.
- **Diversity**: Choose examples that represent different edge cases and variations.

## Advanced Reasoning Patterns

### 1. Least-to-Most
Break a massive problem into a sequence of subproblems and solve them one by one, using previous answers as context for the next.

### 2. Verification Step
Add an explicit step where the model reviews its own reasoning for errors before finalizing.
"Now, verify all calculations and logical steps in your previous response."

### 3. Self-Consistency
Run the reasoning multiple times (internally) and select the most common final answer.

## Summary Checklist
- [ ] Complexity requires CoT?
- [ ] Format requires examples?
- [ ] Examples isolated in `<example>` tags?
- [ ] Reasoning isolated in `<thinking>` tags?
- [ ] Verification step included?
