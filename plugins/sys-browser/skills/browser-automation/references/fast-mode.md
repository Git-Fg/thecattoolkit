# The Sprinter: Fast Mode Reference

**Tool:** `@just-every/crawl` (CLI)

## Capabilities & Limits

| Capability | Status | Note |
|:--- |:--- |:--- |
| **Speed** | 🚀 High | Fetches raw HTML, no rendering. |
| **JavaScript** | ❌ None | Will see `<noscript>` content only. |
| **Auth** | ❌ None | Public pages only. |
| **Batching** | ✅ Yes | Can crawl multiple URLs concurrently. |

## Execution Patterns

### 1. The Standard Read
Best for direct links provided by the user.
```bash
npx -y @just-every/crawl <url>
```

### 2. The Batch Fetch (Parallel)
Best for reading multiple search results at once.
```bash
npx -y @just-every/crawl <url1> <url2> <url3> --concurrency 3 --output json
```
*Note: Always use JSON output for batch operations to separate the content cleanly.*

### 3. The "Spider" (Depth Crawl)
Best for mapping documentation structure.
```bash
npx -y @just-every/crawl <url> --pages 10 --output json
```

## When to Abandon (Switch to Playwright)

Watch the output for these signs. If you see them, **immediately** switch to Interactive Mode. Do not retry with the same tool.

1.  **Cloudflare/Incapsula blocks:** "Please verify you are human", "Attention Required", 403 Forbidden.
2.  **SPA Shells:** Output contains only `<div id="root"></div>` or "You need to enable JavaScript to run this app."
3.  **Cookie Walls:** Content is obscured by a "Accept Cookies" overlay text that hides the body (though `readability` often handles this, sometimes it fails).
