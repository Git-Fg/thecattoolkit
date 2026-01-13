---
name: crawl
description: "High-speed web crawling and Markdown extraction. Use for documentation, articles, and static pages. Optimized for LLM consumption."
argument-hint: "<url> [options]"
---

# Command: /crawl

Extracts clean Markdown from one or more URLs using the fast extraction engine.

## Usage

```bash
/crawl <url> [options]
```

## Options

| Option | Description | Default |
|:-------|:------------|:--------|
| `--pages <n>` | Maximum number of pages to crawl | `1` |
| `--concurrency <n>` | Max concurrent requests | `3` |
| `--no-robots` | Ignore robots.txt restrictions | `false` |
| `--all-origins` | Allow crawling across different domains | `false` |
| `--max-length <n>` | Truncate Markdown at N characters (LLM optimization) | `30000` |

## Execution Protocol

1.  **Selection**: Use this command when the target is static content (docs, blogs, news).
2.  **Run**: Execute the internal script:
    ```bash
    bun run ${CLAUDE_PLUGIN_ROOT}/skills/playwright-strategy/scripts/url-to-md.ts <url> [options]
    ```
3.  **Analyze**: 
    - Review the `status` and `results`.
    - If `recommendation` is present, consider switching to `Skill(playwright-strategy)` for full browser automation.
    - If content is truncated, you may re-run with a higher `--max-length` if the context window allows.

## Example

```bash
/crawl https://docs.example.com --pages 5 --concurrency 5
```
