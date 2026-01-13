# Fast Extraction (URL-to-MD)

The `url-to-md.ts` script provides a high-speed, token-efficient way to extract content from web pages without the overhead of a full browser instance. It is built on `@just-every/crawl` and optimized for LLM consumption.

## When to Use

- **Static Content**: Documentation, blog posts, news articles, and simple landing pages.
- **Speed is Priority**: When you need to quickly scan multiple pages.
- **Token Efficiency**: Strips boilerplate (navbars, footers, ads) using Readability.

## Advanced Parameters

| Flag | Description | Recommendation |
|:-----|:------------|:---------------|
| `--pages <n>` | Max pages to crawl | Keep low (<10) to avoid context saturation. |
| `--concurrency <n>` | Max parallel requests | Default 3. Increase for large documentation sites. |
| `--no-robots` | Bypass robots.txt | Use ONLY if content is public but blocked for bots. |
| `--all-origins` | Cross-domain crawl | Use for sites that host assets/docs on subdomains. |
| `--max-length <n>` | Content truncation | Default 30,000 chars. Adjust based on context window. |
| `--timeout <ms>` | Request timeout | Default 30,000ms. Increase for slow servers. |

## LLM Optimization Layer

The wrapper script includes several optimizations for AI agents:
1.  **Metadata Injection**: Every result includes `length`, `truncated` status, and `duration`.
2.  **Smart Truncation**: Prevents single massive pages from flooding the context window.
3.  **Heuristic Analysis**: Detects "empty" content (e.g., Cloudflare challenges) and suggests fallbacks.

## Troubleshooting

### Content is Empty / Blocked
- **Cause**: The site might be using Cloudflare, a CAPTCHA, or heavy client-side rendering.
- **Solution**: Switch to full Playwright mode (`Skill(playwright-strategy)` Mode 2).

### "No JSON found in output"
- **Cause**: Network error or `npx` failed to execute.
- **Solution**: Check internet connectivity and ensure `node/npx` are available.

### Truncated Content
- **Cause**: Page exceeded the default `--max-length`.
- **Solution**: If the missing part is critical, re-run with a higher `--max-length`.

## Usage Example

```bash
bun run scripts/url-to-md.ts https://example.com --pages 3 --max-length 50000
```
