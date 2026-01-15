---
name: browsing-web
description: "Interactive browser automation using agent-browser. Use when navigating dynamic sites, authentication, clicking, typing, and complex state navigation. Do NOT use for simple read-only text extraction."
allowed-tools: [Bash]
---

# Browser Interaction Protocol

## Core Loop (The Ref Pattern)
You interact with the browser using **References (@refs)** derived from snapshots, not CSS selectors.

1.  **Navigate**: `agent-browser open "url"`
2.  **Snapshot**: `agent-browser snapshot -i` (Gets accessibility tree with `@e` refs)
3.  **Interact**: `agent-browser click @e1` (Uses ref from snapshot)

## Critical Constraints
1.  **Never Guess Selectors**: You cannot guess `@e1`. You MUST run `snapshot` to see current refs.
2.  **Interactive Only**: Always use `snapshot -i` to filter non-interactive elements (saves tokens).
3.  **Stateful**: The browser persists between commands. You do not need to re-open.

## Common Patterns

### Navigation & extraction
```bash
agent-browser open "https://google.com"
agent-browser snapshot -i
# Output shows: [ref=e4] button "Search"
agent-browser fill @e2 "Claude Code"
agent-browser click @e4
agent-browser wait --load networkidle
```

### Visual Verification
Only if structure is confusing:
```bash
agent-browser screenshot page.png
```
