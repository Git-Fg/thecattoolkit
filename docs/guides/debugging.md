# Debugging & Audit

Tools and techniques to investigate plugin behavior.

## 1. The Debug Flag

Run Claude with the debug flag to see exactly what hooks are firing and what tools are being called.

```bash
claude --debug
```

*   **Output:** Verbose logs in stdout.
*   **What to look for:**
    *   Hook trigger events (`Event detected: PreToolUse`).
    *   MCP server connection logs.
    *   File path resolution errors.

## 2. Audit Commands

### `/cost`
Displays the token usage and estimated cost of the current session.
*   **Usage:** Monitor the efficiency of your agents. If a simple task costs $0.50, your prompts are too verbose or your context management is poor.

### `/doctor` (Hypothetical / Plugin specific)
It is best practice to create an internal command `/my-plugin:doctor` that runs:
*   `!node -v`
*   `!git version`
*   `!cat .env` (if safe)
To quickly gather context when a user reports a bug.

## 3. Cache Management

**The #1 cause of "It works on my machine but not in the plugin" is the cache.**

*   **The Cache Path:** `~/.claude/plugins/cache/`
*   **The Fix:** If you changed code but Claude doesn't see it, PURGE.

```bash
# Nuclear Option (Safe for dev)
rm -rf ~/.claude/plugins/cache/*
```

## 4. Hook Verification

To verify if your hooks are loaded:
1.  Run `claude` (interactive).
2.  Type `/` and check if your commands appear.
3.  Trigger an action that should be hooked.
4.  If nothing happens, check `hooks/hooks.json` syntax. A single JSON syntax error often fails silently by ignoring the file.
