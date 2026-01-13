---
name: save-page
description: "Downloads one or more web pages and saves them as clean Markdown files. Use when you need to archive URLs to specific local paths or a directory."
argument-hint: "<url1> [url2] ... [target_path_or_dir]"
---

# Command: /save-page

Fetches one or more URLs, converts them to clean Markdown, and saves the results to disk.

## Usage

```bash
/save-page <url1> [url2] ... [target_path_or_dir]
```

## Protocol

1.  **Selection**: Use this command when the user asks to "download", "save", "archive", or "keep" webpages as Markdown.
2.  **Path Resolution**:
    - **Single URL**: 
        - If `target_path` is provided, save to that file.
        - If omitted, derive filename from URL/Title and save to `./docs/` or CWD.
    - **Multiple URLs**:
        - If a directory is provided as the last argument, save all files there with derived names.
        - If no directory is provided, save all to `./docs/archive/` or CWD with derived names.
3.  **Run**: Execute the extraction script:
    ```bash
    bun run ${CLAUDE_PLUGIN_ROOT}/skills/playwright-strategy/scripts/url-to-md.ts <url1> [url2] ...
    ```
4.  **Persistence**:
    - Loop through `results` in the JSON response.
    - For each result, write the `markdown` to the resolved file path using the `Write` tool.
5.  **Confirmation**: Report success for each file and provide absolute paths.

## Example

```bash
# Single page
/save-page https://example.com ./docs/example.md

# Multiple pages to a directory
/save-page https://example.com https://another.com ./archives/
```

## Natural Language Triggers

- "Save these 3 pages to my docs folder: <url1>, <url2>, <url3>"
- "Download the content of https://example.com as md"
- "Archive the documentation at <url> to ./references/api.md"
