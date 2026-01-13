# Persistence & Memory

Claude has a short memory (context). Your plugin must have a long memory (disk).

## 1. Session Lifecycle

*   **Exit / New Session:** All memory state is lost.
*   **Resume (`claude --continue`):** State is restored.
*   **Design Pattern:** Educate the user. Display "To resume this work later, run `claude --continue`" at the end of long commands.

## 2. The Save & Restore Pattern (Compaction)

When the conversation is too long, Claude "forgets" the beginning (Compaction). To survive this:

### Step 1: Save (`PreCompact`)
A `command` hook triggered before compaction.
*   Reads the recent JSONL transcript.
*   Extracts critical info (IDs, decisions).
*   Writes a hard file (e.g., `.claude/compact/state.md`).

### Step 2: Restore (`SessionStart`)
A `command` hook triggered at startup AND after compaction.
*   Reads `.claude/compact/state.md`.
*   Returns content in the `additionalContext` JSON field via stdout.
*   *Result:* Claude "remembers" immediately after forgetting.

**Note:** Do not inject 10MB. Inject a summary.

## 3. Multi-Agent Orchestration ("Swarm" Pattern)

Subagents do not share memory.
*   **Problem:** Agent A finds a bug. Agent B must fix it, but does not see A's discovery.
*   **Solution:** The File Data Bus.
    1.  Agent A writes `audit-report.md`.
    2.  Main Agent reads the report.
    3.  Main Agent launches Agent B with "Read `audit-report.md` then fix bugs".
*   **Explicit Handoff:** Never rely on telepathy. Pass files.

### The File Data Bus
Since agents don't share memory, the filesystem is their only shared brain.
1.  **Drafts:** Agent A writes `_drafts/api-spec.md`.
2.  **Review:** Agent B reads `_drafts/api-spec.md` and writes `_drafts/review.md`.
3.  **Finalize:** Agent A reads `_drafts/review.md` and updates the spec.
*Tip:* Use hidden folders or temp directories (`.claude/tmp/`) for this intermediate state to keep the user's workspace clean.
