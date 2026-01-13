---
name: create-meta-prompts
description: "Creates optimized prompts for Claude-to-Claude pipelines with research, planning, and execution stages. Use when building prompts that produce structured outputs for other prompts to consume, or when running multi-stage workflows. Do not use for simple prompts, single-step tasks, or basic conversational AI."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Create Meta-Prompts

## Objective

Create prompts optimized for Claude-to-Claude communication in multi-stage workflows. Outputs are structured with XML metadata for efficient parsing by subsequent prompts.

## Quick Start

### Workflow

1. **Intake** - Determine purpose (Do/Plan/Research/Refine)
2. **Generate** - Create prompt using purpose-specific templates
3. **Execute** - Run prompt with dependency-aware execution
4. **Validate** - Verify output and create summary

### Directory Structure

```
.prompts/
├── 001-topic-research/
│   ├── 001-topic-research.md     # Prompt
│   ├── topic-research.md         # Output
│   └── SUMMARY.md                # Human summary
├── 002-topic-plan/
│   ├── 002-topic-plan.md
│   ├── topic-plan.md
│   └── SUMMARY.md
```

## Usage

### Create Research Prompt

```
/create-meta-prompt research authentication options for the app
```

**What it does:**
- Determines this is a Research task
- Scans for existing research files to reference
- Creates prompt with research-specific structure
- Saves to `.prompts/{number}-{topic}-research/`
- Executes with validation

### Create Planning Prompt

```
/create-meta-prompt plan the auth implementation approach
```

**What it does:**
- Detects existing auth-research.md
- Asks if it should reference the research
- Creates plan prompt with research context
- Runs after research completes

### Create Execution Prompt

```
/create-meta-prompt implement JWT authentication
```

**What it does:**
- References both research and plan
- Creates implementation prompt
- Includes verification steps

## Prompt Types

### Research Prompts

For gathering information with structured output.

**Structure:**
```xml
<objective>
Research {topic} to inform {purpose}
</objective>

<context>
{Background and requirements}
</context>

<output>
Save to: .prompts/{num}-{topic}-research/{topic}-research.md
Include: findings, recommendations, metadata
Create: SUMMARY.md
</output>
```

### Plan Prompts

For creating approaches and strategies.

**Structure:**
```xml
<objective>
Create implementation plan for {topic}
</objective>

<context>
Research: @.prompts/{num}-{topic}-research/{topic}-research.md
</context>

<output>
Save to: .prompts/{num}-{topic}-plan/{topic}-plan.md
Include: phases, tasks, dependencies
Create: SUMMARY.md
</output>
```

### Do Prompts

For executing tasks and producing artifacts.

**Structure:**
```xml
<objective>
{What to build/create/fix}
</objective>

<context>
Plan: @.prompts/{num}-{topic}-plan/{topic}-plan.md
</context>

<output>
Create/modify: specified files
Verify: tests and checks
Create: SUMMARY.md
</output>
```

## Execution Engine

### Single Prompt

Straightforward execution of one prompt:

1. Create folder: `.prompts/{number}-{topic}-{purpose}/`
2. Write prompt to: `{number}-{topic}-{purpose}.md`
3. Execute with Task agent
4. Validate output
5. Archive prompt

### Sequential Execution

For chained prompts:

1. Build execution queue from dependencies
2. Execute each prompt in order
3. Validate after each completion
4. Stop on failure
5. Report results

### Parallel Execution

For independent prompts:

1. Spawn all Task agents in single message
2. Wait for completion
3. Validate all outputs
4. Report consolidated results

## Chain Detection

Automatically detects dependencies:

- Scans for existing `*-research.md` and `*-plan.md`
- Matches by topic keyword
- Suggests relevant files to reference
- Determines execution order

## Validation

After execution, verifies:

- Output file created and not empty
- Required XML metadata present
- SUMMARY.md created with all sections
- One-liner is substantive

## Summary Format

Every execution creates `SUMMARY.md`:

```markdown
# {Topic} {Purpose} Summary

**{Substantive one-liner describing outcome}**

## Key Findings
- {Finding 1}
- {Finding 2}

## Files Created
- `path/file.ext` - Description

## Decisions Needed
{Specific items or "None"}

## Next Step
{Concrete forward action}
```

## References

**Templates:**
- [references/research-patterns.md](references/research-patterns.md) - Research prompt templates
- [references/plan-patterns.md](references/plan-patterns.md) - Planning prompt templates
- [references/do-patterns.md](references/do-patterns.md) - Execution prompt templates

**Supporting:**
- [references/metadata-guidelines.md](references/metadata-guidelines.md) - Metadata structure
- [references/question-bank.md](references/question-bank.md) - Intake questions
- [references/summary-template.md](references/summary-template.md) - Summary format

## Success Criteria

**Prompt Creation:**
- Purpose identified correctly
- Chain detection performed
- Prompt structure matches purpose
- Output location specified
- SUMMARY.md requirement included

**Execution:**
- Dependencies correctly ordered
- Output validated
- SUMMARY.md created
- Results presented clearly
