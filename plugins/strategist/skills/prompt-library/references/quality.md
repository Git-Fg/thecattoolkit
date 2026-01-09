# Prompt Quality & Audit Criteria

The standards used to evaluate prompt artifacts for production readiness.

## Core Quality Pillars

### 1. Structure Compliance
- **Single Prompts**: Must be Pure Markdown (0 XML tags).
- **Chains/Meta-Prompts**: Hybrid XML (1-15 tags maximum).
- **Flat Tags**: No nested XML tags allowed.
- **Hierarchy**: Uses clear Markdown headings and lists.

### 2. Instructability
- **Actionable**: Steps are concrete and unambiguous.
- **Specific**: No vague commands like "be helpful" or "analyze".
- **Complete**: All necessary context for the task is included or requested.
- **Sequential**: Logical flow for multi-step instructions.

### 3. Output Control
- **Format**: Output format (JSON, Markdown, etc.) is explicitly defined.
- **Structure**: Clear schemas or templates for complex outputs.
- **Constraints**: Critical negative constraints (NEVER/MUST NOT) are highlighted.

### 4. Safety & Security
- **Isolation**: Few-shot examples are wrapped in `<example>` tags.
- **Data Protection**: No hardcoded credentials or sensitive data instructions.
- **Boundaries**: Clear scope on what the AI should and should NOT do.

## Audit Scoring Matrix

| Quality | Description | Ready? |
|:---|:---|:---:|
| **Production** | Meets all criteria, tested on edge cases, concise. | ✅ |
| **Needs Work** | Good content but minor structural or clarity issues. | ⚠️ |
| **Failing** | Nested XML, vague tasks, or missing output format. | ❌ |

## The "AI Soup" Anti-Checklist
- [ ] Is there any nested XML? (If yes, fix to flat).
- [ ] Is there a tag soup (>5 tags)? (If yes, consolidate).
- [ ] Is there instruction leakage? (Check if examples are isolated).
- [ ] Is it too verbose? (Prune low-value tokens).
- [ ] Is the role duplicated from a parent agent? (Keep it lean).

## Verification Strategy
1. **Manual Review**: Check against the pillars above.
2. **Execution Test**: Run with `run-prompt` on 3-5 diverse inputs.
3. **Audit Prompt**: Use the Prompt Auditor meta-prompt for an AI-driven critique.
