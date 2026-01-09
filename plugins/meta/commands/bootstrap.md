---
description: |
  [Emergency] Safe Mode Bootstrap. Breaks the circular dependency by using pure git operations to restore corrupted toolkit files. USE when /build or /heal fails.
  <example>
  Context: Component corruption detected
  user: "/bootstrap plugins/meta"
  assistant: "I'll perform a soft reset of the meta plugin to restore it to the last known good state from HEAD."
  </example>
  <example>
  Context: System-wide failure
  user: "/bootstrap --hard 1"
  assistant: "I'll perform a hard reset to HEAD~1 to recover from catastrophic state drift."
  </example>
allowed-tools: [Bash, Read, AskUserQuestion]
argument-hint: [path or --hard <N> or --remote <path>]
disable-model-invocation: true
---

# Safe Mode Bootstrap

<role>
You are the **System Auditor**. You operate in **Safe Mode (Vector)** to break circular dependencies. You must NOT use any local Python scripts or complex agents. Use only pure `Bash` and `git` commands.
</role>

## Step 1: Mode Selection

Analyze $ARGUMENTS to determine restore mode:

1. **Path-based (Default):** Restore specific files/directories from HEAD.
   - Usage: `/bootstrap <path>`
   - Command: `git checkout HEAD -- $path`

2. **Hard Reset:** Reset entire repository to a previous commit.
   - Usage: `/bootstrap --hard <N>`
   - Command: `git reset --hard HEAD~$N`
   - **CAUTION:** This discards all uncommitted changes.

3. **Remote Restore:** Fetch and restore from origin/main.
   - Usage: `/bootstrap --remote <path>`
   - Command: `git fetch origin && git checkout origin/main -- $path`

## Step 2: Diagnostic Verification

Identify the target for restoration:
- If no path provided, default to `plugins/meta`.
- Verify the target exists in git history using `git ls-files`.

## Step 3: Execution

1. **Dry Run/Diff:** Show the user what will be restored.
   - `git diff HEAD -- $path`
2. **Approval:** Use `AskUserQuestion` to confirm the operation.
3. **Apply:** Execute the appropriate git command.
4. **Post-Check:** Verify `git status` for the target path.

## Step 4: Verification

Confirm the restoration was successful and the system is back in a consistent state.
Suggest running `/heal` or `/build` now that the core tools are restored.
