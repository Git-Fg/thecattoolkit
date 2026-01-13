---
name: playwright-strategy
description: "Browser automation strategy. PROACTIVELY Use when handling any browser-related tasks including automation, crawling, scraping, research, QA, testing, and debugging."
---

When using Playwright through an MCP-based client, always choose one primary evidence strategy and keep it stable unless the user requests otherwise.

## Fast Extraction Protocol (LIGHTWEIGHT)
Before using full Playwright automation, evaluate if the task can be completed using the high-speed conversion script.

**Criteria for Fast Extraction:**
- Target is a public article, documentation, or static page.
- No interaction (login, clicks) is required.
- You need clean Markdown for LLM consumption.

**Action:**
Execute `npx/bunx run scripts/url-to-md.ts <url>`.
See [references/fast-extraction.md](references/fast-extraction.md) for details.

## Mode 1 — Image-first (primary: pixels; fallback: structure)
Use when visual rendering matters: layout differences, styling regressions, charts, maps, canvases, complex widgets, or when semantics are unreliable.

Policy:
- Prefer screenshots as the primary evidence to understand what is on screen.
- For actions, prefer deterministic interaction driven by structured page semantics when available.
- Use coordinate-based interaction only as an exception when semantic structure cannot target the intended UI reliably.

## Mode 2 — Structure-first / "image diminished" (primary: structure; fallback: pixels)
Use for most tasks where semantics are enough: systematic navigation, extraction of text/labels, form workflows, link/button flows, crawling/scraping pipelines, and reproducible test-like runs.

Policy:
- Prefer structured snapshots (semantic representation) as the primary source of truth.
- Only request screenshots when the structure is ambiguous, incomplete, or missing visually critical information.
- When screenshots are required, prefer targeted, minimal captures over full-page captures to control cost.

### Special note: external vision server present
If the MCP environment includes the tool "Vision MCP Server (`@z_ai/mcp-server`)", use it as an optional, cost-aware helper for cases that truly require vision (OCR on screenshots, diagnosing error screenshots, interpreting diagrams, reading dense visual content).

If the Vision MCP Server is not present, this means the MCP environment has no native vision capabilities available. In this case, you must rely exclusively on the Mode 2 policy: use structured snapshots as primary evidence, and only request screenshots when absolutely necessary for debugging or validation purposes.

## Cross-cutting rules (both modes)
- Stabilize before collecting evidence: wait for navigation, transitions, and async content to settle.
- Use a persistent session only when you need stateful behavior (e.g., authenticated flows); otherwise prefer clean/isolated runs for reproducibility.
- Keep outputs small: avoid repeatedly collecting large evidence artifacts unless necessary.
- If results are uncertain, collect one additional orthogonal signal (structure vs pixels vs runtime signals) rather than looping the same signal repeatedly.
