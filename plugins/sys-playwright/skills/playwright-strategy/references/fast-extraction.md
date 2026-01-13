# Fast Extraction (URL-to-MD)

The `url-to-md.ts` script provides a high-speed, token-efficient way to extract content from web pages without the overhead of a full browser instance.

## When to Use

- **Static Content**: Documentation, blog posts, news articles, and simple landing pages.
- **Speed is Priority**: When you need to quickly scan multiple pages.
- **Token Efficiency**: The conversion uses Mozilla's Readability to strip boilerplate (navbars, footers, ads), leaving only the core content.

## When NOT to Use

- **Heavy JavaScript**: If the page content is primarily rendered via client-side JS.
- **Authentication**: If the content is behind a login.
- **Complex UI Interaction**: If you need to click buttons, fill forms, or hover to reveal content.

## Usage

```bash
bun run scripts/url-to-md.ts <url> [pages] [concurrency]
```

### Parameters

- `url`: The starting URL to crawl/fetch.
- `pages` (optional, default: 1): Maximum number of pages to crawl.
- `concurrency` (optional, default: 3): Maximum concurrent requests.

### Output

The script returns a JSON object:

```json
{
  "status": "success",
  "results": [
    {
      "url": "https://example.com",
      "markdown": "# Page Content...",
      "title": "Page Title",
      "links": ["https://link1.com", "..."]
    }
  ]
}
```
