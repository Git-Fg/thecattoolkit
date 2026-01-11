---
name: prompt-engineering
description: "USE when user needs to draft, optimize, or audit prompts. Includes Prompt Library, Chain-of-Thought patterns, and Optimization workflows."
context: fork
agent: prompt-engineer
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Prompt Engineering Domain

## Router Protocol

Analyze the user's intent and select the appropriate workflow:

### 1. Drafting New Prompts
**Trigger**: "Create a prompt", "Draft system instructions", "New prompt for..."
**Protocol**: Apply workflow from `workflows/draft.md`
**Assets**: Use templates from `assets/templates/`

### 2. Optimizing Existing Prompts
**Trigger**: "Fix this prompt", "Make this prompt better", "Optimize..."
**Protocol**: Apply workflow from `workflows/optimize.md`
**Theory**: Apply `references/optimization.md`

### 3. Library Access
**Trigger**: "Show me examples", "List templates", "Prompt templates"
**Action**: List contents of `assets/templates/`
**References**: Use `references/taxonomy.md` for categorization

## Core Theory

### Concise Is Key
Every token competes with conversation history. Assume Claude is already intelligent.
- **Does Claude already know this?** (Omit common knowledge)
- **Is this explanation necessary?** (Be direct)
- **Does this justify its token cost?** (Value-based inclusion)

### Control Degrees of Freedom
Match specificity to task fragility:
- **High Freedom**: Multiple valid approaches → use text-based heuristics
- **Medium Freedom**: Preferred pattern exists → use pseudocode with parameters
- **Low Freedom**: Error-prone operations → use exact scripts

### Signal-to-Noise Rule (XML vs Markdown)
- **Default**: Markdown (80% of prompts) - fewer tokens, Claude-native
- **Upgrade to XML/Markdown hybrid** only when complexity triggers met:
  - Data Isolation: >50 lines of raw data
  - Constraint Weight: Rules that MUST NEVER be broken
  - Internal Monologue: Complex reasoning requiring step-by-step

### Key Techniques

**Chain-of-Thought (CoT)**
- Zero-shot CoT: "Let's think step by step."
- Structured CoT: Use `<thinking>` blocks for internal monologue
- Step-back: Address principles before specifics

**Few-Shot Learning**
- One-shot: Single demonstration for simple patterns
- Few-shot (3-8 examples): For complex categorization or formatting
- Isolation: Use `<example>` tags to prevent example leakage

## Prompt Taxonomy

### 1. Single Prompts
Standalone, reusable prompts for direct, one-shot execution.
- **Storage**: `.cattoolkit/prompts/`
- **Template**: `assets/templates/single-prompt.md`

### 2. Prompt Chains
Sequential multi-step workflows where output from one step feeds the next.
- **Storage**: `.cattoolkit/chains/{number}-{topic}/`
- **Pattern**: Research → Plan → Execute → Refine
- **Templates**: `assets/templates/chain/`

### 3. Meta-Prompts
Higher-order prompts that generate, optimize, or analyze other prompts.
- **Storage**: `.cattoolkit/generators/`
- **Templates**: `assets/templates/meta/`

## Reference Index
- [Techniques](references/techniques.md)
- [Patterns](references/patterns.md)
- [Optimization](references/optimization.md)
- [Anti-Patterns](references/anti-patterns.md)
- [Execution Protocol](references/execution-protocol.md)
- [Taxonomy](references/taxonomy.md)
- [Quality Standards](references/quality.md)
- [Discovery Questions](references/discovery.md)
- [Metadata Standards](references/metadata.md)

## Template Library
- `assets/templates/single-prompt.md` - General purpose template
- `assets/templates/chain-summary.md` - Chain result summary
- `assets/templates/chain/` - Research → Plan → Execute → Refine
- `assets/templates/meta/` - Generator and optimizer templates

## Assets
- `assets/examples/few-shot.json` - Curated example datasets for various domains
