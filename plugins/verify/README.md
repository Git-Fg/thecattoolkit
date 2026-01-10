# verify

**Validation Phase** - Verifying correctness of file changes and code safety.

## Purpose

The immune system of the toolkit. Shifts focus from "blocking" to "verifying correctness" - all hooks run in warn-only mode.

## Hooks

- **SessionStart** - Restores context plan, scratchpad, and history (restore-context.sh)
- **PreToolUse** - Warns about editing sensitive files and detects secrets (protect-files.sh, security-check.sh)
- **PostToolUse** - Auto-logs state-changing operations to context log (inline jq)
- **PreCompact** - Compacts memory before context limit (compact-memory.sh)
- **Stop** - Checks for uncommitted changes and active handoff files (evaluate-stop.sh)

## Design Philosophy

All hooks run non-blocking (warn-only). Type checkers auto-detect project configuration and skip if not applicable.
