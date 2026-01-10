---
name: draft-prompt
description: |
  USE when user wants to create a new prompt from scratch for a specific task or use case.
  Guides through prompt design process: analyze requirements, select patterns, create prompt.
context: fork
agent: prompt-engineer
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Draft New Prompt

Create high-quality prompts from scratch using proven engineering patterns.

## Workflow

### 1. Analyze Task Requirements
Identify the core elements of your prompt need:
- **Purpose**: What should the prompt accomplish?
- **Context**: What background information is needed?
- **Constraints**: Any specific rules or limitations?
- **Output format**: How should results be structured?
- **Complexity level**: Simple task or multi-step workflow?

### 2. Select Appropriate Pattern
Based on the prompt-engineering skill, choose the right approach:
- **Chain-of-Thought (CoT)**: For reasoning-heavy tasks
- **Few-shot learning**: When examples help clarify intent
- **Role-based**: For specialized expertise (e.g., "You are a security auditor...")
- **Template-based**: Following standardized structure from prompt-library

### 3. Apply Complexity Decision Framework
Use the Signal-to-Noise Rule from prompt-engineering skill:
- **Markdown-first**: Default for most prompts (fewer tokens, Claude-native)
- **Hybrid XML/Markdown**: Only when complexity triggers met:
  - Data Isolation: >50 lines of raw data
  - Constraint Weight: Rules that MUST NEVER be broken
  - Internal Monologue: Complex reasoning requiring step-by-step

### 4. Create High-Quality Prompt
Structure the prompt following best practices:
- Use `# Context` section for background
- Use `# Assignment` section for specific instructions
- Include concrete examples when helpful
- Keep instructions clear and unambiguous
- Apply appropriate pattern from prompt-library templates

### 5. Output to File
Write the completed prompt to:
- **PROMPT.md** in the current directory
- Include YAML frontmatter if needed
- Follow template structure from prompt-library skill

## Key Resources
- **prompt-engineering skill**: Theory, patterns, and optimization techniques
- **prompt-library skill**: Templates and taxonomy
- **Template**: Use single-prompt.md from prompt-library skill

## Output
Complete prompt saved to `PROMPT.md` with:
- Clear instructions
- Appropriate structure (Markdown/XML)
- Examples if needed
- Ready for immediate use
