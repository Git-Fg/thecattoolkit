---
name: manage-healing
description: USE when diagnosing failures or applying repair protocols for self-correcting AI components.
allowed-tools: Read
---

# Healing Protocols

Diagnostic logic for identifying why an AI component failed and repair strategies to fix it. Used by the `/heal` command in main context.

## Shared Standards

For common principles, integration patterns, and anti-patterns, see:
- **[shared-standards.md](references/shared-standards.md)** - Common standards for all management skills

## Diagnostic Reference

### 1. Skill Drifts

**Symptom:** AI tries to use a specific tool/workflow mentioned in the Skill but fails (e.g., "Tool not found" or "Invalid arguments").

**Diagnosis:** The `SKILL.md` examples or instructions are out of sync with the actual tools available.

**Repair:** Update `SKILL.md` examples to match the actual tool signature found in the environment.

### 2. Agent Constraints

**Symptom:** Subagent enters an infinite loop, asks user questions when prohibited, or fails to create output.

**Diagnosis:** Weak negative constraints in `agents/*.md`.

**Repair:** Add explicit `<constraints>` or `NEVER` clauses to the agent definition.

### 3. Command Hallucinations

**Symptom:** Command invents arguments or fails to gather necessary context before delegation.

**Diagnosis:** `argument-hint` or `description` is vague.

**Repair:** Update frontmatter `argument-hint` and add explicit context gathering steps.

## Repair Patterns

### The "Add Example" Fix

If the model failed to format an output correctly:

**Action:** Do not just change instructions. Add a concrete example block using Markdown to the component's definition showing the *correct* input/output pair based on the recent failure.

### The "Constraint Hardening" Fix

If the model violated a rule (e.g., edited a protected file):

**Action:** Move the rule from "Instructions" to a dedicated `<constraints>` XML block or use uppercase "MUST/NEVER" language.

### The "Path Correction" Fix

If the model hallucinated a file path:

**Action:** Verify the actual path using `ls/find` and update the reference in the documentation.

## Bootstrap Protocol (Emergency Recovery)

When core tools (`/build`, `/heal`) are corrupted, use git restore to recover. See `/heal` command's "Emergency Bootstrap Recovery" section for protocols.

## Knowledge Base

| Reference | Purpose |
|-----------|---------|
| [shared-standards.md](references/shared-standards.md) | Common standards for all management skills |
| [diagnosis-patterns.md](references/diagnosis-patterns.md) | Decision tree for root cause analysis |
| [bootstrap-protocol.md](references/bootstrap-protocol.md) | Emergency git-based recovery procedures |
