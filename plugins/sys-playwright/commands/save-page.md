---
name: save-page
description: "Downloads a web page and saves it as a clean Markdown file. Use when you need to archive a URL to a specific local path."
argument-hint: "<url> [path]"
---

# Command: /save-page

Fetches a URL, converts it to clean Markdown, and saves the result to a specified file path.

## Usage

```bash
/save-page <url> [path]
```

## Protocol

1.  **Selection**: Use this command when the user asks to "download", "save", "archive", or "keep" a specific webpage as Markdown.
2.  **Path Resolution**:
    - If `[path]` is provided, use it as the destination. Ensure the parent directory exists.
    - If `[path]` is omitted, derive a filename from the URL or page title and save it in the current directory or a relevant `docs/` folder.
3.  **Run**: Execute the extraction script:
    ```bash
    bun run ${CLAUDE_PLUGIN_ROOT}/skills/playwright-strategy/scripts/url-to-md.ts <url>
    ```
4.  **Persistence**:
    - Extract the `markdown` from the JSON response.
    - Write the content to the resolved path using the `Write` tool.
5.  **Confirmation**: Report the success and the absolute path of the saved file.

## Example

```bash
/save-page https://claudemcp.com/docs ./docs/mcp-guide.md
```

## Natural Language Triggers

- "Save this page to my docs folder"
- "Download the content of https://example.com as md"
- "Archive the documentation at <url> to ./references/api.md"
