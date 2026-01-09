# @cattoolkit/prompter

**Prompt engineering, meta-prompting, and prompt chain orchestration for AI-to-AI workflows.**

**License:** MIT

## Purpose

Provides comprehensive prompt crafting capabilities including prompt engineering theory, reusable prompt library, meta-prompt chains, and optimization strategies for autonomous AI workflows.

## Commands

### /create-prompt
Create single prompts, prompt chains, or meta-prompts.

```bash
/create-prompt "Prompt description or 'auto' for guided creation"
```

**Types:**
- **Single Prompt** - Standalone reusable prompt → `.cattoolkit/prompts/`
- **Prompt Chain** - Sequential workflow (Research → Plan → Execute → Refine) → `.cattoolkit/chains/`
- **Meta-Prompt** - Generates/optimizes other prompts → `.cattoolkit/generators/`

**Use for:**
- Creating reusable prompts for specific tasks
- Building multi-step sequential workflows
- Standardizing prompt structures

### /refine-prompt
Refine existing prompts through fast edit, improvement, or meta-prompt refactoring.

```bash
/refine-prompt "Prompt-name or path to .md file"
```

**Modes:**
- **Fast Edit** - Fix specific issues (typos, single section)
- **Improve** - Enhance quality (better examples, clarity)
- **Refactor** - Complete optimization via meta-prompt

### /prompt-engineer
Advanced prompt engineering with autonomous agent.

```bash
/prompt-engineer "Complex prompt requirements or optimization task"
```

**Use for:**
- Complex prompt requirements
- Multi-stage AI workflows
- Prompt optimization needed
- Custom prompt architectures

### /run-prompt
Execute saved prompts.

```bash
/run-prompt "Prompt-name"
```

**Use for:**
- Running previously created prompts
- Executing meta-prompt chains
- Reusing proven prompt structures

## Skills

### prompt-engineering
Theory, patterns, and techniques of prompt design.

**Resources:**
- Core techniques (CoT, Trees, etc.)
- XML/Markdown hybrid pattern selection
- Decision frameworks for architecture
- Common anti-patterns and pitfalls
- Optimization strategies

### prompt-library
Templates and lifecycle management for prompt artifacts.

**Resources:**
- Prompt taxonomy and directory standards
- Discovery and requirement gathering guides
- Templates (Single, Chain, Meta)
- Quality and audit criteria

## Agent

### prompt-engineer
Advanced prompt engineering and optimization agent.

**Pattern:** Sovereign Triangle (specialized engineer)

**Capabilities:**
- Creates sophisticated prompt structures
- Optimizes prompts for specific use cases
- Designs meta-prompt chains
- Analyzes prompt effectiveness

## Workflow Example

```bash
# Step 1: Create a prompt
/create-prompt "Code review prompt for security vulnerabilities"

# Step 2: Test and refine
/refine-prompt "security-review"

# Step 3: Advanced engineering if needed
/prompt-engineer "Optimize security-review prompt for false positives"

# Step 4: Use the prompt
/run-prompt "security-review"
```

## Integration

- **With @cat-toolkit/meta** - Build prompt creation and optimization tools
- **With @cat-toolkit/think** - Apply structured thinking to prompt design
- **With @cat-toolkit/builder** - Create prompts for planning workflows and code generation
