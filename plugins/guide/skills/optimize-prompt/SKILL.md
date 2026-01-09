---
name: optimize-prompt
description: |
  USE when user has an existing prompt that needs improvement or refinement.
  Analyzes prompt weaknesses, applies optimization techniques, produces enhanced version.
context: fork
agent: prompt-engineer
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Optimize Existing Prompt

Refine and enhance prompts for better performance using systematic optimization techniques.

## Workflow

### 1. Analyze Current Prompt
Read and evaluate the existing prompt:
- **Strengths**: What's working well?
- **Weaknesses**: Where does it break down or underperform?
- **Ambiguity**: Are instructions clear and unambiguous?
- **Completeness**: Are all necessary details included?
- **Structure**: Is the format optimal for the task?

### 2. Identify Improvement Opportunities
Based on prompt-engineering skill, locate specific issues:
- **Clarity**: Vague or confusing instructions?
- **Specificity**: Need more concrete guidance?
- **Examples**: Would examples improve understanding?
- **Structure**: Should format be Markdown or XML/Markdown hybrid?
- **Constraints**: Missing critical rules or safety measures?
- **Context**: Insufficient background information?

### 3. Apply Optimization Techniques
Use proven methods from prompt-engineering skill:
- **Progressive Disclosure**: Add headers for organization
- **Chain-of-Thought**: Add reasoning steps for complex tasks
- **Few-Shot Learning**: Insert concrete examples
- **Role Definition**: Clarify the AI's persona/expertise
- **Constraint Isolation**: Highlight critical rules
- **Signal-to-Noise**: Optimize format selection

### 4. Implement Improvements
Refactor the prompt systematically:
- Fix ambiguous language
- Add missing context or examples
- Restructure for better flow
- Apply appropriate pattern from prompt-library
- Remove unnecessary complexity
- Strengthen constraints where needed

### 5. Output Optimized Version
Save improvements to:
- **OPTIMIZED_PROMPT.md** in the current directory
- Include comparison notes in comments
- Maintain original intent while enhancing execution
- Apply template structure from prompt-library skill

## Key Resources
- **prompt-engineering skill**: Optimization techniques and frameworks
- **prompt-library skill**: Templates and best practices
- **Anti-patterns**: `references/anti-patterns.md` from prompt-engineering
- **Quality criteria**: `references/quality.md` from prompt-library

## Output
Optimized prompt saved to `OPTIMIZED_PROMPT.md` with:
- Clearer instructions
- Better structure
- Added examples if needed
- Enhanced effectiveness
- Performance improvements documented
