---
name: spider
description: "Deep crawl (depth=20) to map a documentation site structure."
argument-hint: "<url>"
allowed-tools: Bash
---

# Command: /spider

Performs a structural map of a website.

## Context
!npx -y @just-every/crawl $1 --pages 20 --output json

## Protocol
1.  **Review JSON**: Analyze the links and titles returned above.
2.  **Report**: Present a high-level summary of the site's sections.
3.  **Suggest**: Recommend specific URLs to `/read`.
