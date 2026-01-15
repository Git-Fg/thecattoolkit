---
name: driving-browser
description: "The master knowledge base for web interaction. Teaches the strategic use of lightweight crawling vs. heavy browser automation. Use when handling any web tasks: searching, reading, scraping, navigation, and testing."
compatibility: "Requires npx, @just-every/crawl, and @playwright/mcp"
user-invocable: true
allowed-tools:
  - Bash
  - Write
  - Read
  - Edit
  - AskUserQuestion
---

# Browser Automation Strategy Protocol

Follow this protocol to orchestrate the most efficient path to information for web tasks. This skill provides knowledge about two distinct engines and strategies for selecting and combining them based on task requirements.

## 1. The Two Engines: Comparative Analysis

### Engine A: The Sprinter (`@just-every/crawl`)
*   **Mechanism:** Raw HTTP requests + HTML parsing + Markdown conversion.
*   **Pros:** Extremely fast, low token cost, zero browser overhead, parallel processing.
*   **Cons:** Cannot execute JavaScript, fails on Single Page Apps (SPAs), blocked by strict anti-bot systems, cannot interact (click/type).
*   **Best For:** Bulk reading, static documentation, blogs, news sites, archiving.

### Engine B: The Tank (`@playwright/mcp`)
*   **Mechanism:** Full headless browser (Chromium) controlled via CDP.
*   **Pros:** Renders everything (JS, Canvas), handles complex auth, interacts with UI, handles navigation state.
*   **Cons:** Slower, higher latency, requires managing the "Accessibility Tree" (Snapshot), sequential operations.
*   **Best For:** Web apps, search engine results pages (SERPs), complex forms, debugging, visual validation.

## 2. Dynamic Selection & Hybrid Workflows

Do not stick to one tool blindly. Evaluate the target and adapt in real-time.

### Strategy: The "Search & Scatter" (Best for Research)
When you need to research a topic, using the "Tank" for everything is too slow. Use a hybrid approach:
1.  **Phase 1 (The Tank):** Use Playwright to navigate to a search engine (Google/Bing/DDG). Handle any consent popups. Type the query.
2.  **Phase 2 (The Handoff):** Extract the resulting URLs from the search page.
3.  **Phase 3 (The Sprinter):** Feed those URLs into `npx web-crawl` in parallel to get the content of 3-5 pages instantly.
4.  **Phase 4 (Synthesis):** Synthesize the answer from the bulk markdown.

### Strategy: The "Probe & Escalate" (Best for Unknown Links)
1.  **Attempt 1:** Try `npx web-crawl <url>`.
2.  **Evaluation:** Check the output.
    *   *Is it empty?* (Likely JS-rendered) -> **Switch to Playwright**.
    *   *Is it a 403/429?* (Bot block) -> **Switch to Playwright** (it mimics a real user better).
    *   *Is it good?* -> **Done**.

## 3. Navigation & Search Knowledge Base

### Search Engine Handling
Search engines are hostile to bots.
*   **Avoid:** `web-crawl google.com/search?q=...` (It will likely fail or return a captcha).
*   **Prefer:** Playwright `browser_navigate` -> `browser_type` -> `browser_click`.
*   **Optimization:** Once on the results page, use `browser_snapshot` to get the link list, then **stop using the browser** for reading the results. Switch to `web-crawl` for the actual reading.

### Handling "Application" vs "Document"
*   **Document Mode:** If the user wants *information* (e.g., "How do I configure Webpack?"), prioritize extracting text. Visual layout is irrelevant.
*   **Application Mode:** If the user wants *action* (e.g., "Log in and check my bill"), layout matters. Stick to Playwright. Use `browser_snapshot` frequently to understand the UI state.

## 4. State Anchoring

For any multi-step session, you must track your position.
1.  Check/Create `_state.md`.
2.  Update it as you move:
    ```markdown
    # Session State
    - [x] Phase 1: Search for "MCP Protocol" (Done via Playwright)
    - [ ] Phase 2: Read Top 3 Links (Pending via web-crawl)
    - [ ] Phase 3: Synthesize Summary
    ```

## 5. Playwright Evidence Strategies

When using the Tank (Playwright MCP), you must choose one evidence strategy and keep it stable unless the user requests otherwise.

### Strategy A: Image-First (Visual Analysis)
Use when visual rendering matters: layout differences, styling regressions, charts, maps, canvases, complex widgets, or when semantics are unreliable.

**Policy:**
- Prefer screenshots as the primary evidence to understand what is on screen
- For actions, prefer deterministic interaction driven by structured page semantics when available
- Use coordinate-based interaction only as an exception when semantic structure cannot target the intended UI reliably

### Strategy B: Structure-First (Functional Testing)
Use for systematic navigation, extraction of text/labels, form workflows, link/button flows, crawling/scraping pipelines, and reproducible test-like runs.

**Policy:**
- Prefer structured snapshots (semantic representation) as the primary source of truth
- Only request screenshots when the structure is ambiguous, incomplete, or missing visually critical information
- When screenshots are required, prefer targeted, minimal captures over full-page captures to control cost

### Z.AI Vision MCP Server Handling

**If Z.AI Vision MCP Server (`@z_ai/mcp-server`) is available:**
- Use it as an optional, cost-aware helper for vision-required cases
- Capabilities: OCR on screenshots, diagnosing error screenshots, interpreting diagrams, reading dense visual content

**If Vision MCP Server is NOT available:**
- Rely exclusively on structured snapshots as primary evidence
- Only request screenshots for debugging or validation purposes

## 6. Two-Pass Crawl & Retry Discipline

### Two-Pass Approach
For research and scraping, use a two-pass approach to minimize waste:
1.  **Pass A (Map):** Visit the index/landing page. Return a constrained JSON list: `[{url, title, relevance_score}]`.
2.  **Pass B (Extract):** Visit ONLY the top K most relevant URLs from Pass A. Extract specific fields.

### Retry Discipline
- If a selector fails, try a broader selector ONCE
- If that fails, capture a screenshot for debugging and STOP
- Do not loop endlessly trying to guess selectors

## 7. Token Economy & Artifact Policy

### Token Economy Rules
*   **No Wall of Text:** Never output the full text of a webpage into the chat unless explicitly asked. Summarize or extract specific data points.
*   **Snapshot Discipline:** In Interactive Mode, use `browser_snapshot` (Accessibility Tree). Only use screenshots if visual layout analysis is explicitly requested.
*   **Compact Extraction:** Prioritize returning specific, requested fields (e.g., Title, Canonical URL, top 20 links) rather than entire page body.
*   **Default MCP:** Prefer `pw-structure` (incremental snapshots, images omitted) for all tasks unless the user explicitly mentions visual layout issues.

### Artifact Policy
*   **Never return full snapshots inline:** Always save snapshots to `${CLAUDE_PLUGIN_ROOT}/.playwright-output/` and only provide a summary or file path in the chat.
*   **Screenshots are for evidence only:** Do not attempt to parse actions from screenshots. Use them only for debugging or verifying visual intent.
*   **Limit Resnapshots:** At most 1 resnapshot per page unless navigation has occurred.

### Persistence
*   **Artifacts:** If the user asks to "save" or "download", write the output to a file (e.g., `docs/<slug>.md`). Do not rely on chat history for storage.

## 8. Protocol: Progressive Layered Inspection

Do not pull a full snapshot of an unknown page immediately. Disclose data in three distinct layers to preserve tokens:

### Layer 1: Structural Probe (The Map)
**Goal:** Identify menus, global patterns, and layout.
**Action:** Use `browser_evaluate` with a script to return a "Skeleton JSON" (tags, IDs, and text of nav/headers).
**Reasoning:** Understand where you are without reading 2,000 lines of body text.

### Layer 2: Scoped Search (The Target)
**Goal:** Isolate the specific section containing the user's answer.
**Action:** Use `browser_evaluate` to find the `innerText` or `innerHTML` of the most relevant container (e.g., `#main`, `.article-content`).
**Reasoning:** If the info is in a sidebar, why snapshot the footer?

### Layer 3: Final Extraction (The Content)
**Goal:** Get clean, structured data for the final answer.
**Action:**
1. Use `browser_run_code` to `remove()` non-essential elements (ads, nav, footer).
2. Execute `browser_snapshot` on the remaining "Clean DOM."

**When to Disclose Body Text:** Only move to Layer 3 (Full Snapshot) if:
1. Layer 1 confirms the page is relevant.
2. Layer 2 identifies a "Main Content" container.
3. The user needs a precise quote or detailed data extraction.

## 9. Cross-Cutting Rules
*   Stabilize before collecting evidence: wait for navigation, transitions, and async content to settle
*   Use persistent session only for stateful behavior (e.g., authenticated flows); otherwise prefer clean/isolated runs
*   Keep outputs small: avoid repeatedly collecting large evidence artifacts
*   If results are uncertain, collect one additional orthogonal signal rather than looping

## 10. Reference Manuals

For technical details on specific commands:
*   [The Sprinter Guide (Fast Mode)](references/fast-mode.md)
*   [The Tank Guide (Interactive Mode)](references/interactive-mode.md)
