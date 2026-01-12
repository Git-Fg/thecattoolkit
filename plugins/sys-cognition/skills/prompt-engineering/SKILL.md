---
name: prompt-engineering
description: "Applies 2026 Complexity-Based Guidance standards with Attention Management, Sycophancy Prevention, and XML/Markdown decision matrix. Use when designing, optimizing, or auditing AI prompts, system instructions, or multi-step chains."
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Prompt Engineering & Design Standards

## Operational Protocol

1. **Analyze Intent**: Determine if the goal is Drafting, Optimizing, Auditing, or serving as Knowledge Bank.
2. **Consult Standards**: PROACTIVELY load `references/core-standards.md` for Attention Management rules.
3. **Select Pattern (Signal-to-Noise Rule)**:
   - **Markdown-First** (Default): Use for 80% of tasks.
   - **Hybrid XML**: Use ONLY if:
     - Data Isolation (>50 lines raw data)
     - Strict Constraints (NEVER/MUST rules)
     - Internal Monologue (Complex reasoning)
4. **Execute Workflow**:
   - **Drafting**: Use `references/draft-workflow.md`
   - **Optimizing**: Use `references/optimization-workflow.md`
5. **Verify**: Apply `references/quality.md` gates before final output.

## Router Protocol

### 1. Drafting New Prompts
**Trigger**: "Create a prompt", "Draft system instructions", "New prompt for..."
**Protocol**: Apply workflow from `references/draft-workflow.md`
**Assets**: Use templates from `assets/templates/`

### 2. Optimizing Existing Prompts
**Trigger**: "Fix this prompt", "Make this prompt better", "Optimize..."
**Protocol**: Apply workflow from `references/optimization-workflow.md`
**Theory**: Apply `references/optimization.md`

### 3. Auditing Prompts
**Trigger**: "Review this prompt", "Check for issues", "Audit..."
**Protocol**: Apply `references/quality.md` checklist and `references/anti-patterns.md`

### 4. Library Access (Knowledge Bank Mode)
**Trigger**: "Show me examples", "List templates", "What patterns exist..."
**Action**: List contents of `assets/templates/` or `references/design-patterns.md`

### 5. Research Prompt Templates
**Trigger**: "research prompts", "analysis templates", "critique prompt", "synthesis prompt", "inversion prompt", "research templates"
**Action**: Load `references/research-prompts.md`, present cognitive mode categories
**Purpose**: Access viral research prompts that transform AI into research weapons

### 6. Agent Knowledge Injection
**Trigger**: Agent loads this skill via `skills:` field
**Purpose**: Ensure generated instructions follow 2026 standards
**Key Standards**: Truth-First, Attention Management, Signal-to-Noise optimization

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
| **research-prompts.md** | Viral research prompt templates (11 prompts) | Analysis, critique, synthesis tasks |

## Template Library

- `assets/templates/single-prompt.md` - General purpose template
- `assets/templates/chain-summary.md` - Chain result summary
- `assets/templates/chain/` - Research → Plan → Execute → Refine
- `assets/templates/meta/` - Generator and optimizer templates

## Success Criteria

A prompt meets 2026 standards when:
- [ ] Uses Markdown headers for hierarchy (default)
- [ ] XML tags are < 15 and never nested
- [ ] Instructions are specific, actionable, and truth-focused
- [ ] Examples (if any) are isolated in `<example>` tags
- [ ] Reasoning is isolated in `<thinking>` blocks (if needed)
- [ ] Quality gate checklist is included
- [ ] Output format is clearly specified
