---
name: prompt-engineering
description: |
  This skill should be used when the user asks 'how to structure a prompt', 'optimize prompt results', 'reduce hallucinations', or 'which engineering pattern to use'. Provides prompt design theory (CoT, Trees), decision frameworks (XML vs Markdown), and optimization techniques to improve AI reasoning and output quality.
  <example>
  Context: User needs design guidance
  user: "How should I structure this prompt for better results?"
  assistant: "I will use the prompt-engineering skill to select the optimal design pattern."
  </example>
  <example>
  Context: User needs optimization help
  user: "Why is my prompt producing inconsistent results?"
  assistant: "I will use the prompt-engineering skill to analyze and optimize the prompt using CoT and few-shot patterns."
  </example>
  <example>
  Context: User wants to learn CoT
  user: "Explain Chain-of-Thought prompting and how to apply it."
  assistant: "I will use the prompt-engineering skill to explain CoT and structured thinking techniques."
  </example>
allowed-tools: [Read]
---

# Prompt Engineering Theory & Patterns

Master the art and science of prompt design through proven techniques and frameworks.

## Core Principles

### 1. Concise Is Key
Every token competes with conversation history. Assume Claude is already intelligent.
- **Does Claude already know this?** (Omit common knowledge)
- **Is this explanation necessary?** (Be direct)
- **Does this justify its token cost?** (Value-based inclusion)

### 2. Control Degrees of Freedom
Match specificity to task fragility:
- **High Freedom**: Multiple valid approaches (e.g., code review) → use text-based heuristics.
- **Medium Freedom**: Preferred pattern exists (e.g., refactoring) → use pseudocode with parameters.
- **Low Freedom**: Error-prone operations (e.g., migration) → use exact scripts.

### 3. Progressive Markdown Disclosure
- **Markdown Headers**: Use `# Context` and `# Assignment` as the primary structural elements for all prompts.
- **XML** (Limit to 15 tags): Use for logic containers (like `<thinking>`) or complex data isolation ONLY when Markdown headers are insufficient due to high data density.
- **Critical**: Never nest XML tags. Use markdown inside XML.

## Key Techniques

### Chain-of-Thought (CoT)
Encourage the model to reason before providing an answer.
- **Zero-shot CoT**: "Let's think step by step."
- **Structured CoT**: Use `<thinking>` blocks for internal monologue.
- **Step-back**: Address principles before specifics.

### Few-Shot Learning
Demonstrate intent through concrete examples.
- **One-shot**: Single demonstration for simple patterns.
- **Few-shot (3-8 examples)**: For complex categorization or formatting.
- **Isolation**: Use `<example>` tags to prevent example leakage.

## Decision Frameworks

### The "Signal-to-Noise" Rule (XML vs Markdown)

Instead of the prompt type determining the format, the **Density of Context** and **Logic Non-Negotiability** should drive the architecture.

| Feature | Use Markdown (Headers/Lists) | Use XML (Flat Semantic Tags) |
| :--- | :--- | :--- |
| **Instructional Flow** | Default: Linear, simple, or descriptive. | Complex: Strict, non-negotiable step sequences. |
| **Data Isolation** | Standard context and injected files. | High-density: Large logs or noisy data sets. |
| **Role Definition** | Standard: Professional persona. | Specialized: Isolated identity with high constraints. |
| **Output Type** | Standard: Conversational or Markdown. | Technical: Machine-parseable JSON or strict code. |
| **Safety Risk** | Standard: Analytic or creative tasks. | Critical: Security audits or data protection. |

### Upgrade Path Protocol

#### 1. The Default (Markdown First)
For 80% of standalone prompts, Markdown is superior because it consumes fewer tokens and aligns better with Claude's native training for following prose instructions.

#### 2. The Semantic Upgrade (XML Tags)
Upgrade to a **Hybrid XML/Markdown** structure only when the prompt hits these "Complexity Triggers":
*   **The "Data Isolation" Trigger:** If the prompt requires the user to paste >50 lines of raw data, use `<context>` or `<data>` to prevent the data from "leaking" into the instructions.
*   **The "Constraint Weight" Trigger:** If there are rules that MUST NEVER be broken (e.g., "Never expose API keys"), isolate them in `<constraints>` so the model's attention mechanism anchors to them.
*   **The "Internal Monologue" Trigger:** If the task is so complex that the model is prone to jumping to conclusions, use `<thinking>` to force a Chain-of-Thought isolated from the final answer.

## Reference Index

- `references/techniques.md`: Deep dive into CoT, few-shot, and reasoning patterns.
- `references/patterns.md`: Detailed library of prompt structure patterns.
- `references/optimization.md`: Systematic refinement and troubleshooting.
- `references/anti-patterns.md`: Common pitfalls and how to avoid them.

## Assets
- `assets/examples/few-shot.json`: Curated example datasets for various domains.
