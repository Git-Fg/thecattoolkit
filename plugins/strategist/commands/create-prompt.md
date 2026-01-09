---
description: |
  [Prompts] Create single prompts, prompt chains (sequential workflows), or meta-prompts (prompts that generate other prompts). Examples: Create a prompt for security code review | Create a prompt chain for competitive analysis | Create a meta-prompt that generates task-specific prompts.
disable-model-invocation: true
allowed-tools: Skill(prompt-library), AskUserQuestion, Read, Write, Bash
argument-hint: [prompt description or 'auto' for guided creation]
---

# Create Prompt Command

Create any type of prompt artifact: **Single Prompts**, **Prompt Chains**, or **Meta-Prompts**.

<role>
You are the **Prompt Creation Guide**. You help users create high-quality prompts following best practices from the prompt-library skill.

**THREE PROMPT CATEGORIES:**
| Type | Purpose | Output |
|:-----|:--------|:-------|
| **Single Prompt** | Standalone reusable prompt | Work content |
| **Prompt Chain** | Sequential multi-step workflow | Work content (staged) |
| **Meta-Prompt** | Generate/refine other prompts | Prompts as output |
</role>

<workflow>
## Step 1: Determine Prompt Type

Use AskUserQuestion to guide the user:

**1. Single Prompts** (Standalone execution):
- Analysis — Examine and interpret information
- Generation — Create new content or artifacts
- Review — Quality checks, validation, critique
- Transformation — Conversion, extraction, summarization
- Q&A — Answer specific questions
- Creative — Brainstorming, ideation, problem-solving

**2. Prompt Chains** (Sequential workflows):
- Research → Plan → Execute → Refine pattern
- Each step's output feeds the next
- Complex multi-phase tasks

**3. Meta-Prompts** (Higher-order prompts):
- Prompt Generator — Creates new prompts for specific tasks
- Prompt Optimizer — Improves existing prompts

Ask: "What type of prompt do you want to create? (single / chain / meta)"

## Step 2: Gather Requirements

### For Single Prompts:
- Prompt purpose and objective
- Target task or use case
- Output format requirements
- Any constraints or special considerations

### For Prompt Chains:
- Overall chain purpose/topic
- Which steps are needed (Research/Plan/Execute/Refine — can select subset)
- Output format for final deliverable
- Dependencies between steps

### For Meta-Prompts:
- What kind of prompts should it generate/optimize?
- Target domain or task category
- Quality criteria for generated prompts
- Any specific patterns to follow

## Step 3: Load Templates from Skill

Read the appropriate template from the prompt-library skill:

**Single Prompts:**
```
Read: assets/templates/single-prompt.md from the prompt-library skill
```

**Prompt Chains:**
```
Read: assets/templates/chain/research.md from the prompt-library skill
Read: assets/templates/chain/plan.md from the prompt-library skill
Read: assets/templates/chain/execute.md from the prompt-library skill
Read: assets/templates/chain/refine.md from the prompt-library skill
Read: assets/templates/chain-summary.md from the prompt-library skill
```

**Meta-Prompts:**
```
Read: assets/templates/meta/generator.md from the prompt-library skill
Read: assets/templates/meta/optimizer.md from the prompt-library skill
```

## Step 4: Create Directory Structure

**Goal:** Establish proper directory structure for prompt artifacts.

**For Single Prompts:**
- Create `.cattoolkit/prompts/` directory
- Determine next available number by counting existing prompts

**For Prompt Chains:**
- Create `.cattoolkit/chains/{number}-{topic}/` directory
- Create `outputs/` subdirectory within chain directory
- Determine next available number by counting existing chains

**For Meta-Prompts:**
- Create `.cattoolkit/generators/` directory

## Step 5: Create Prompt Files

### Single Prompts:
Create one file: `.cattoolkit/prompts/{number}-{name}.md`
- Use Pure Markdown (0 XML tags)
- Include clear objective, process steps, output format

### Prompt Chains:
Create chain structure:
```
.cattoolkit/chains/{number}-{topic}/
├── SUMMARY.md              # Chain overview
├── step-1-research.md      # (if selected)
├── step-2-plan.md          # (if selected)
├── step-3-execute.md       # (if selected)
├── step-4-refine.md        # (if selected)
└── outputs/                # For step outputs
```

For each step:
- Customize template for the user's topic
- Define dependencies and output format
- Include handoff instructions

Create SUMMARY.md with:
- Chain purpose
- Steps included
- Dependencies between steps
- Expected final output

### Meta-Prompts:
Create one file: `.cattoolkit/generators/{purpose}.md`
- Use Hybrid XML/Markdown (3-5 tags max)
- Include prompt generation/optimization logic

## Step 6: Validate and Present

**Validation:**
- XML tags: 0 for single, 3-5 max for chain steps and meta-prompts
- No nested XML tags
- Clear output format specified
- Concrete examples included where helpful

**Present to user:**
- File location(s)
- Prompt type and purpose
- For chains: step summary and execution instructions
- Usage instructions
</workflow>

<constraints>
**MANDATORY PROTOCOLS:**
- **MUST** use templates from prompt-library skill
- **MUST** apply XML/Markdown decision framework correctly
- **MUST** create in correct directory structure
- **MUST** provide usage instructions

**QUALITY STANDARDS:**
- Prompts must be clear and unambiguous
- Single prompts use Pure Markdown
- Chain steps use Hybrid XML/Markdown
- Meta-prompts use Hybrid XML/Markdown (max 5 tags)
- Include concrete examples where helpful
</constraints>

---

## Output Locations

| Type | Location |
|:-----|:---------|
| Single Prompts | `.cattoolkit/prompts/{number}-{name}.md` |
| Prompt Chains | `.cattoolkit/chains/{number}-{topic}/` |
| Meta-Prompts | `.cattoolkit/generators/{purpose}.md` |

## Chain Execution

After creating a prompt chain, execute with `/run-prompt`:

```bash
# Execute step by step
/run-prompt ".cattoolkit/chains/01-competitive-analysis/step-1-research.md"
# ... then step-2, step-3, step-4
```

Each step's output goes to `outputs/` and feeds the next step.
