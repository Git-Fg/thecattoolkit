/// IMPORTANT : CLAUDE CODE AND ALL MODERN TOOLS HAVE AUTO-COMPACT CAPACITIES; NEVER REIMPLEMENT IT ///

1. Multi-Session-Agent Orchestration ("Swarm" Pattern)

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
