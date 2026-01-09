# Shared Management Standards

This document contains standards that apply to all management skills in the meta plugin.

## Common Principles

All management skills follow these principles:

1. **Passive Knowledge**: Management skills provide standards and templates for autonomous execution. They never ask questions.
2. **Atomic Independence**: Skills do not depend on specific Commands. They are self-contained libraries of knowledge.
3. **Intelligence > Process**: Trust the model to determine execution steps based on standards and templates.
4. **Progressive Disclosure**: SKILL.md < 500 lines; detailed standards live in `references/`.

## Integration Patterns

### With Commands
- Delegate to agents using **Triangle Prompt Pattern** (Triangle phase)
- Validate and present results

### With Agents
Agents provide the **execution layer**:
- Load skills for domain expertise
- Apply declarative standards autonomously
- Execute without asking questions (Triangle pattern)
- Use intelligence to determine "How" based on "What" and "Rules"

### With Other Skills
Skills are **self-contained libraries**:
- No cross-skill dependencies via relative paths
- Use natural language references
- Trust agent to load multiple skills
- Each skill is independently useful

## Success Criteria Template

All management skill outputs should:

- Apply appropriate standards from the skill
- Generate output compliant with validation protocols
- Use templates from assets/templates/ when available
- Execute autonomously without user interaction
- Provide comprehensive results with evidence

## Anti-Patterns to Avoid

| Pattern | Why Avoid | Alternative |
|---------|-----------|-------------|
| Vague descriptions | Won't discover | Add specific purpose and triggers |
| Missing tool restrictions | Security risk | Add allowed-tools or tools field |
| No dynamic context | Missing state | Add context gathering steps |
| Overly complex | Hard to use | Split into focused components |
| Interactive prompts | Breaks autonomy | Make skills passive knowledge |

## Common References

- **CLAUDE.md**: Core architecture and quality gates
- **standards-communication.md**: Triangle Prompt pattern, XML/Markdown usage, handoff protocols
- **standards-security.md**: Background execution, tool permissions, path traversal

## Usage in Management Skills

To use these shared standards:

1. Reference this file in the "Knowledge Base" or "References" section
2. Apply the common principles to your domain-specific content
3. Follow the integration patterns when describing how your skill works
4. Use the success criteria template as a checklist

This ensures consistency across all management skills while maintaining domain-specific expertise.
