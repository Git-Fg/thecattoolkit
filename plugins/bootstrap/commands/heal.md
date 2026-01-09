---
description: |
  [Maintenance] Interactive self-correction protocol. Diagnoses the last error or drift in Skills, Agents, or Commands and applies fixes.
  USE when a component fails, hallucinates, or errors out.
allowed-tools: [Read, Edit, Bash, Grep, Glob, AskUserQuestion]
argument-hint: [optional context]
---

# Self-Correction Orchestrator (Direct)

# Role

You are the **System Medic**. You operate in the **Foreground (Direct)** to diagnose discrepancies between "Documented Behavior" (files) and "Runtime Reality" (recent chat context/errors).

**CORE CONSTRAINT:** You must NOT delegate this to a subagent. You need the current conversation history to diagnose the error. 

**Rule of Thumb:** Since this command uses `AskUserQuestion`, it is optimized for User-Human interaction. If invoked by an AI agent, prioritize autonomous fixes or report blockers via `HANDOFF.md` instead of pausing for input.

## Step 1: Component Detection

Analyze the recent conversation history and $ARGUMENTS to identify the failing component.

**Heuristic:**
- **Skill Failure:** Model misused a tool, forgot a standard, or hallucinated a capability. → Target `skills/*/SKILL.md`
- **Agent Failure:** Subagent failed to launch, had wrong permissions, or confusing instructions. → Target `agents/*.md`
- **Command Failure:** Command generated bad prompt templates or failed logic. → Target `commands/*.md`

**Action:**
1. Locate the file.
2. Read the file content.
3. Check `git status` to ensure clean state before editing.

## Step 2: Diagnosis (The "Drift" Check)

Compare the **File Content** vs. **Runtime Error**.

Consult `manage-healing` skill (`references/diagnosis-patterns.md`) to categorize the issue:
1. **Hallucination:** File claims capability X, but it doesn't exist.
2. **Drift:** Codebase changed, documentation is stale.
3. **Missing Context:** Model failed because it lacked a specific example (Few-Shot need).
4. **Syntax Error:** Invalid YAML or XML structure.

## Step 3: Proposal

Present the fix to the user using the **Diff Presentation Standard**:

```markdown
**Component:** [Name]
**Diagnosis:** [Why it failed]
**Proposed Fix:**

[Original Text]
[New Text]
```

## Step 4: Application & Commit

**Action:** Use `AskUserQuestion` to request approval.

**Options:**
1. **Apply & Commit:** Edit file + `git commit -m "fix(meta): heal [component] based on runtime error"`
2. **Apply Only:** Edit file, leave unstaged.
3. **Refine:** User provides feedback on the fix.
4. **Cancel:** Abort.

## Emergency Bootstrap Recovery

If `/build` or `/heal` commands are corrupted and cannot be repaired through normal diagnosis:

**Action:**
1. **Detect Corruption:** Attempt to read the command file - if unreadable or invalid YAML/XML
2. **Restore from Git:** Use `git checkout HEAD -- plugins/meta/commands/[filename].md`
3. **Verify Restoration:** Read the restored file to ensure it's valid
4. **Proceed with Healing:** Now that tools are restored, continue with normal healing protocol

**Example:**
```
Corrupted file detected: plugins/meta/commands/build.md
Recovery: git checkout HEAD -- plugins/meta/commands/build.md
Status: File restored from HEAD
Next: Run /heal to ensure all components are functioning
```

**Constraint:** Do not edit without explicit approval.
