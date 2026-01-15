# The Tank: Interactive Mode Reference

**Tool:** `@playwright/mcp`

## Core Concept: The Accessibility Tree
Unlike a human who sees pixels, this tool sees the **Accessibility Tree** (a structured representation of the page).
*   **Tool:** `browser_snapshot`
*   **Returns:** A nested list of roles (link, button, heading) and their names.
*   **Critical:** You interact with `ref` IDs (e.g., `ref: 12`), NOT CSS selectors.

## Navigation Strategy

### 1. Reaching the Target
*   **Direct URL:** `browser_navigate(url)`
*   **Search:** Navigate to search engine -> Wait for input -> Type -> Press Enter.

### 2. Smart Waiting
The most common failure in automation is acting before the page is ready.
*   **Implicit Waits:** Playwright auto-waits for checks, but not for logic.
*   **Explicit Strategy:** If you click a "Search" button, do NOT immediately snapshot.
    *   *Bad:* Click -> Snapshot (Result: Old page or empty).
    *   *Good:* Click -> `browser_wait_for(text="Results")` OR `browser_wait_for(time=2000)` -> Snapshot.

### 3. Reading vs. Seeing
*   **Structure (Default):** `browser_snapshot` with `snapshot-mode: incremental`. This is fast and cheap. Use this for 95% of tasks.
*   **Vision (Expensive):** `browser_take_screenshot`. Use ONLY when:
    *   The user asks "What does this look like?"
    *   The snapshot is confusing (e.g., multiple buttons with the same name).
    *   You are debugging a "Element not found" error.

## Server Configuration & Behavior

### Incremental Snapshots
The server is configured to return incremental updates. Do not assume you have the full tree in every response; maintain a mental model or check the `ref` IDs.

### Image Omission
Images are omitted by default by the `pw-structure` server to save bandwidth/tokens. Use `pw-image` server if images are required.

## Evidence Strategies

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

## Z.AI Vision MCP Server Integration

### With Z.AI Vision MCP Server
If the MCP environment includes the Vision MCP Server (`@z_ai/mcp-server`), use it as an optional, cost-aware helper for cases that truly require vision:

**Capabilities:**
- OCR on screenshots
- Diagnosing error screenshots
- Interpreting diagrams
- Reading dense visual content

**When to Use:**
- OCR on error messages or code in screenshots
- Interpreting architecture diagrams or flowcharts
- Understanding complex visual layouts

### Without Vision MCP Server
If Vision MCP Server is not present, rely exclusively on structured snapshots as primary evidence. Only request screenshots when absolutely necessary for debugging or validation purposes.

## Failure Recovery Protocol

1.  **Action Fails:** You try to click `ref: 45` but it fails.
2.  **Diagnose:** Do not guess a new ID.
    *   *Step 1:* Take a new `browser_snapshot` (the tree might have updated).
    *   *Step 2:* If still ambiguous, `browser_take_screenshot`.
3.  **Recover:** Use the new evidence to find the correct target.

## Tool Selection Hierarchy

### 1. Navigation & State
*   `browser_navigate`: Go to URL.
*   `browser_run_code`: **Preferred** for complex setup (setting cookies, localStorage, viewport).

### 2. Interaction (Structure-First)
*   **`browser_snapshot`**: The primary way to "see". Returns the Accessibility Tree.
*   `browser_click`: Interaction. Use the `ref` ID from the snapshot.
*   `browser_type`: Data entry. Use the `ref` ID.

### 3. Visuals (Costly - Use Sparingly)
*   `browser_take_screenshot`: Only use if:
    1.  The user specifically asks about layout/colors.
    2.  `browser_snapshot` fails to reveal the necessary element.
    3.  Debugging a failed selector.

## Progressive Disclosure JS Library

### The Skeleton Probe (Layer 1)
Use this to find menus and global structure without a full snapshot:
```javascript
// Execute via browser_evaluate
() => {
  const map = {
    menus: Array.from(document.querySelectorAll('nav, [role="navigation"], header ul')).map(el => el.innerText.split('\n').slice(0, 5)),
    headings: Array.from(document.querySelectorAll('h1, h2')).map(h => h.innerText),
    mainCandidate: !!document.querySelector('main, article, #content, .main')
  };
  return map;
}
```

### The Search & Prune (Layer 2 & 3)
Before taking a snapshot, "Clean the Room" to save 70% of tokens:
```javascript
// Execute via browser_run_code
async (page) => {
  await page.evaluate(() => {
    // List of noise elements
    const selectors = ['nav', 'footer', 'script', 'style', 'iframe', '.ads', '.social-share'];
    selectors.forEach(s => document.querySelectorAll(s).forEach(el => el.remove()));

    // Highlight the target if known
    const main = document.querySelector('main, article, #content');
    if (main) {
      main.style.border = "5px solid red"; // Makes it obvious in screenshots
    }
  });
}
```

### Targeted Content Extraction (Layer 2)
Get just the text from a specific container:
```javascript
// Execute via browser_evaluate
() => {
  const container = document.querySelector('main, article, #content, .post-content');
  if (container) {
    return {
      title: document.querySelector('h1')?.innerText || '',
      content: container.innerText.trim(),
      wordCount: container.innerText.trim().split(/\s+/).length
    };
  }
  return null;
}
```

## Best Practices

1.  **Selectors:** Use the `ref` ID returned by the snapshot (e.g., `ref: 42`) rather than trying to guess CSS selectors.
2.  **Two-Pass Approach:** For research and scraping:
    - **Pass A (Map):** Visit the index/landing page. Return a constrained JSON list: `[{url, title, relevance_score}]`.
    - **Pass B (Extract):** Visit ONLY the top K most relevant URLs from Pass A. Extract specific fields.
3.  **Retry Discipline:** If a selector fails, try a broader selector ONCE. If that fails, capture a screenshot for debugging and STOP. Do not loop endlessly.
4.  **Incremental Updates:** The server returns incremental updates. Check `ref` IDs to understand what changed.
5.  **Image Handling:** Images are omitted by default to save bandwidth/tokens. Use `pw-image` server when images are required.
6.  **Progressive Disclosure:** Start with JS probes (Layer 1), scope to containers (Layer 2), only snapshot clean DOM (Layer 3).
