---
name: crawl
description: "High-speed web crawling and Markdown extraction. Use for documentation, articles, and static pages. Optimized for LLM consumption."
argument-hint: "<url> [options]"
---

# Command: /crawl

Extracts clean Markdown from one or more URLs using the fast extraction engine.

## Usage

```bash
/crawl <url1> [url2] [url3] ... [options]
```

## Options

| Option | Description | Default |
|:-------|:------------|:--------|
| `--pages <n>` | Maximum number of pages to crawl per URL | `1` |
| `--concurrency <n>` | Max concurrent requests within a single crawl | `3` |
| `--parallel` | Fetch multiple base URLs in parallel | `false` |
| `--no-robots` | Ignore robots.txt restrictions | `false` |
| `--all-origins` | Allow crawling across different domains | `false` |
| `--max-length <n>` | Truncate Markdown at N characters (LLM optimization) | `30000` |

## Execution Protocol

1.  **Selection**: Use this command when the target is static content (docs, blogs, news). Supports multiple URLs for batch processing.
2.  **Run**: Execute the internal script:
    ```bash
    bun run ${CLAUDE_PLUGIN_ROOT}/skills/playwright-strategy/scripts/url-to-md.ts <url1> [url2] ... [options]
    ```
3.  **Analyze**: 
    - Review the `urlCount` and `results`.
    - If `recommendation` is present, consider switching to `Skill(playwright-strategy)` for full browser automation.
    - Results are returned in a single array containing data for all requested URLs.

## Example

```bash
/crawl https://docs.example.com https://blog.example.com --parallel
```
