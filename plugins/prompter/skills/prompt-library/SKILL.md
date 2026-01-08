---
name: prompt-library
description: |
  This skill should be used when the user asks to 'create a prompt', 'run a prompt', 'manage prompt chains', or 'refine prompt artifacts'. Manages the lifecycle of prompt artifacts including Single Prompts, Prompt Chains (Research/Plan/Do), and Meta-Prompts using standardized templates and quality audit criteria.
  <example>
  Context: User wants to create a prompt
  user: "Create a prompt for code review"
  assistant: "I will use the prompt-library skill templates to create a single prompt."
  </example>
  <example>
  Context: User needs a multi-step workflow
  user: "Build a prompt chain for document analysis"
  assistant: "I will use the prompt-library skill to design a sequential prompt chain."
  </example>
  <example>
  Context: User wants to execute a saved prompt
  user: "Run my competitive-analysis prompt"
  assistant: "I will use the prompt-library skill execution workflow to run the saved prompt."
  </example>
allowed-tools: [Read, Write, Edit, Bash]
---

# Prompt Library & Lifecycle Management

Standardized templates and management for prompt artifacts.

## Prompt Taxonomy

We distinguish three core categories of prompt artifacts:

### 1. Single Prompts
Standalone, reusable prompts for direct, one-shot execution.
- **Storage**: `.cattoolkit/prompts/`
- **Structure**: Pure Markdown (0 tags preferred)
- **Output**: Direct work product

### 2. Prompt Chains
Sequential multi-step workflows where output from one step feeds the next.
- **Storage**: `.cattoolkit/chains/{number}-{topic}/`
- **Pattern**: Research → Plan → Execute → Refine
- **Output**: Multi-stage work product

### 3. Meta-Prompts
Higher-order prompts that generate, optimize, or analyze other prompts.
- **Storage**: `.cattoolkit/generators/`
- **Output**: New or improved prompts

## Available Templates

### Creation
- `assets/templates/single-prompt.md`: General purpose template.
- `assets/templates/chain/`: Step-specific templates (research, plan, execute, refine).
- `assets/templates/meta/`: Specialized generators and optimizers.

### Metadata
- `references/metadata.md`: Guidelines for YAML frontmatter and SUMMARY.md.

## Lifecycle Operations

### 1. Exploration & Discovery
- `references/discovery.md`: Standard questions for gathering requirements.

### 2. Creation & Validation
- `references/taxonomy.md`: Detailed definitions and examples of prompt types.
- `references/quality.md`: Audit criteria for production-ready prompts.

### 3. Execution & Refinement
- Use `/run-prompt` for execution.
- Use `/refine-prompt` for updates.

## Directory Structure

### Skill Resources
```
assets/templates/
├── single-prompt.md
├── chain/ (research, plan, execute, refine)
└── meta/ (generator, optimizer)
```

### User Project Storage
```
.cattoolkit/
├── prompts/      # Single prompts
├── chains/       # Sequential workflows
└── generators/   # Meta-prompts
```
