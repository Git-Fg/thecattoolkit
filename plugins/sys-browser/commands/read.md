---
name: read
description: "Instant readout of a web page URL. Zero-latency context fetching."
argument-hint: "<url>"
allowed-tools: Bash
---

# Command: /read

Instantly fetches the content of a URL using the Fast Mode strategy.

## Context
!npx -y @just-every/crawl $1 --output markdown

## Protocol
1.  **Analyze**: The content is loaded above.
2.  **Action**: Summarize or answer the user's specific question.
