# Execution Engine Logic

## Execution Modes

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

## Validation Logic
After execution, verifies:
- Output file created and not empty
- Required XML metadata present
- SUMMARY.md created with all sections
- One-liner is substantive
