---
name: save
description: "Downloads a web page and saves it as a clean Markdown file."
argument-hint: "<url> <path>"
allowed-tools: Bash, Write
---

# Command: /save

Fetches and persists web content.

## Context
!npx -y @just-every/crawl $1

## Protocol
1.  **Write**: Save the content above to the path specified in `$2`.
2.  **Confirm**: Return only the file path and a word count.
