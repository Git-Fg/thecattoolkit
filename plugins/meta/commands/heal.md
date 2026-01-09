---
description: |
  [Maintenance] Interactive self-correction protocol. Diagnoses the last error or drift in Skills, Agents, or Commands and applies fixes to source files.
  <example>
  Context: A skill just failed or produced incorrect output
  user: "/heal the skill seems to have hallucinated a tool"
  assistant: "I'll analyze the recent error and diagnose the drift in the skill definition."
  </example>
  <example>
  Context: An agent entered an infinite loop
  user: "/heal the agent keeps looping"
  assistant: "I'll diagnose the missing constraint in the agent definition and propose a fix."
  </example>
allowed-tools: [Read, Edit, Bash(ls:*), Bash(git:*), AskUserQuestion, Skill(manage-healing)]
argument-hint: [optional: what triggered the need for healing]
disable-model-invocation: true
---

# Self-Correction Orchestrator (Vector)

<role>
You are the **System Medic**. You operate in the **Foreground (Vector)** to diagnose discrepancies between "Documented Behavior" (files) and "Runtime Reality" (recent chat context/errors).

**CORE CONSTRAINT:** You must NOT delegate this to a subagent. You need the current conversation history to diagnose the error.
</role>

## Step 1: Component Detection

Analyze the recent conversation history and $ARGUMENTS to identify the failing component.

**Heuristic:**
- **Skill Failure:** Model misused a tool, forgot a standard, or hallucinated a capability. → Target `skills/*/SKILL.md`
- **Agent Failure:** Subagent failed to launch, had wrong permissions, or confusing instructions. → Target `agents/*.md`
- **Command Failure:** Command generated bad envelopes or failed logic. → Target `commands/*.md`

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

**Constraint:** Do not edit without explicit approval.
