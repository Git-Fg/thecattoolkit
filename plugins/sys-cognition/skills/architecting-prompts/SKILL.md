---
name: architecting-prompts
description: "Applies 2026 Complexity-Based Guidance standards with Attention Management, Sycophancy Prevention, and XML/Markdown decision matrix. Provides theory, patterns, and quality evaluation criteria for AI prompt design. Use when designing, optimizing, or auditing AI prompts, system instructions, or multi-stage chains. Do not use for generating prompt files, basic conversational AI, or single-step interactions."
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Prompt Architecture & Design Standards

## Operational Protocol

1. **Analyze Intent**: Determine if the goal is Drafting, Optimizing, or Auditing a prompt.
2. **Consult Standards**: PROACTIVELY load `references/core-standards.md` for Attention Management rules.
3. **Select Pattern (Signal-to-Noise Rule)**:
   - **Markdown-First** (Default): Use for 80% of tasks.
   - **Hybrid XML**: Use ONLY if:
     - Data Isolation (>50 lines raw data)
     - Strict Constraints (NEVER/MUST rules)
     - Internal Monologue (Complex reasoning)
4. **Apply Theory**: Use `references/optimization.md` for refinement workflows.
5. **Verify**: Apply `references/quality.md` gates before final output.

## Core Principles (Quick Reference)

### Attention Management
> Every token competes with conversation history for model attention.

Use Markdown headers for hierarchy. XML tags (Max 15, No Nesting) ONLY for semantic data isolation or thinking scaffolding.

### Sycophancy Prevention (Truth-First)
> Technical accuracy > User validation.

If user suggests flawed path → CONTRADICT immediately. No "Great idea!" or superlatives. Speak in code, files, commands.

### Signal-to-Noise Rule
- **Default**: Markdown (80% of prompts) - fewer tokens, Claude-native
- **Upgrade to XML/Markdown hybrid** only when:
  - Data Isolation: >50 lines of raw data
  - Constraint Weight: NEVER/MUST rules that cannot be broken
  - Internal Monologue: Complex reasoning requiring step-by-step

## Knowledge Index (Progressive Disclosure)

| Reference | Purpose | Load When |
|:----------|:--------|:----------|
| **core-standards.md** | Attention, Sycophancy, Quota, XML/MD matrix | ALWAYS consult first |
| **design-patterns.md** | CoT, Few-Shot, Taxonomy, Structural patterns | Selecting technique |
| **optimization.md** | Systematic refinement workflow | Improving existing prompts |
| **quality.md** | Production quality gates | Final verification |
| **anti-patterns.md** | Common mistakes to avoid | Prevention |
| **taxonomy.md** | Single vs Chain vs Meta categorization | Storage/planning |
| **execution-protocol.md** | Standard completion reporting | Structured output |

## Design Patterns

### Chain of Thought (CoT)
Use for complex reasoning tasks requiring step-by-step decomposition.

### Few-Shot Learning
Provide 3-5 examples to establish patterns and expectations.

### Structured Output
Specify exact output format with XML tags or Markdown sections.

### Constraint Encoding
Use NEVER/MUST rules for critical safety or correctness requirements.

## Success Criteria

A prompt meets 2026 standards when:
- [ ] Uses Markdown headers for hierarchy (default)
- [ ] XML tags are < 15 and never nested
- [ ] Instructions are specific, actionable, and truth-focused
- [ ] Examples (if any) are isolated in `<example>` tags
- [ ] Reasoning is isolated in `<thinking>` blocks (if needed)
- [ ] Quality gate checklist is included
- [ ] Output format is clearly specified

**Note**: For generating .md prompt files for Claude-to-Claude pipelines, use `generating-prompts` skill.
