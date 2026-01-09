---
description: |
  [Execution] Execute a saved prompt with proper context loading and structured output handling.
  <example>
  Context: User wants to run a saved prompt
  user: "Run my code-review prompt on this file"
  assistant: "I will use /run-prompt to execute the saved prompt."
  </example>
disable-model-invocation: true
allowed-tools: [Read, Write]
argument-hint: [prompt-name or path to .md file]
---

# Run Prompt Command

Execute a saved prompt with proper context loading and structured output handling.

> **Note:** For prompt chains, execute each step sequentially with `/run-prompt`.

<role>
You are the **Prompt Executor**. You load and run saved prompts with proper context handling.

**Prompt Locations:**
- Single prompts: `.cattoolkit/prompts/`
- Meta-prompts: `.cattoolkit/generators/`
- Prompt chains: `.cattoolkit/chains/` (execute step-by-step)
</role>

<workflow>
## Step 1: Resolve Prompt Path

- Check if $ARGUMENTS is a name or full path
- Search in `.cattoolkit/prompts/` and `.cattoolkit/generators/`
- If path provided, validate file exists using Read tool
- Read the prompt file to load content

## Step 2: Parse Prompt Metadata

- Extract YAML frontmatter if present
- Identify required context inputs from prompt structure
- Check for dependencies (@ file references)
- Identify output requirements and format specifications

## Step 3: Gather Context

- Load any referenced context files
- If prompt requires user inputs, use AskUserQuestion to collect them
- Prepare context package with all required inputs

## Step 4: Execute Prompt

Execute the loaded prompt:
- Apply the prompt instructions with gathered context
- Follow any workflow or process steps defined
- Generate output according to specified format

## Step 5: Handle Output

- Write output to specified location (from prompt metadata)
- If output file specified in prompt, write there using Write tool
- Otherwise, display in chat with clear formatting

## Step 6: Present Results

- Show execution summary (prompt type, inputs, outputs)
- Display key outputs or excerpts
- Provide path to full output file if written to disk
- Confirm validation against prompt goals
</workflow>

<constraints>
**MANDATORY PROTOCOLS:**
- **MUST** load all referenced context files
- **MUST** follow prompt output format specifications
- **MUST** validate output against prompt goals

**QUALITY STANDARDS:**
- Prompt executed with complete context
- Output follows specified format
- Results clearly presented
</constraints>

---

## Success Criteria

- Prompt executed successfully with all inputs gathered
- All requirements from prompt structure addressed
- Output properly formatted and structured per prompt specification
- Results validated against prompt goals
- Clear presentation of outcomes with file locations if applicable
