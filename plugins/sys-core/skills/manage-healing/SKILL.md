---
name: manage-healing
description: "Performs forensic investigation and applies permanent fixes. MUST USE when diagnosing component failures, hallucinations, or instruction drift. Do not use for routine tasks, standard debugging, or preventive maintenance."
context: fork
allowed-tools: [Task, Read, Write, Edit, Glob, Grep]
---

# Forensic Healing Protocol

## Phase 0: Target Acquisition
You MUST first resolve the user's input to a concrete file path:
1. **Validation**: Check if the input is already a valid absolute or relative path.
2. **Search**: If it's a name (e.g., "manage-healing"), use `find_by_name` to locate the `SKILL.md` or component definition.
3. **Ambiguity Resolution**: If multiple files match, pick the one in `plugins/` that matches the component type (Agent, Skill, Command).

## Phase 1: Evidence Retrieval (Forensics)
You MUST analyze the "Black Box" of the failure by reading the following state files:
1. **The Pulse**: `.cattoolkit/context/context.log` (Find the exact timestamp of the error).
2. **The Memory**: `.cattoolkit/context/scratchpad.md` (Check the agent's intent vs. its tool usage).
3. **The Guard**: `hooks/hooks.json` (Verify if a hook intercepted the tool call).
4. **The Manifesto**: The failing `SKILL.md`, `agent.md`, or `command.md`.

## Phase 2: Diagnosis (Drift Detection)
Compare the **Tool Prompt** (from context.log) against the **Instructions** (from the manifesto).
- **Hallucination**: The model used a tool argument not defined in the skill.
- **Interception**: A hook returned a `block` status that the agent didn't handle.
- **Instruction Drift**: The skill provides an example that is incompatible with the current toolkit version.

## Phase 3: The Healing Fix
DO NOT revert files. Update the logic to be more resilient:
1. **Correct the Example**: Update the Markdown code block to show the correct tool signature.
2. **Harden Constraints**: Add a `## Constraints` section with specific `MUST NOT` instructions addressing the error.
3. **Path Sanitization**: If the error was a "File Not Found," add a "Context Discovery" step to the protocol.

## Phase 4: Prevention (Immunization)
Update the component's **Description** keywords to better match its actual successful triggers, and add a "Troubleshooting" section to the bottom of the component's file documenting this fix.

## Reference Assets
- [bootstrap-protocol.md](references/bootstrap-protocol.md): Protocol for initializing healing environment
- Cross-skill standards: Refer to the `toolkit-registry` skill’s `standards-communication` reference when you need shared policies.
- [diagnosis-patterns.md](references/diagnosis-patterns.md): Common error patterns
- [bootstrap.sh](assets/scripts/bootstrap.sh): Environment setup script
