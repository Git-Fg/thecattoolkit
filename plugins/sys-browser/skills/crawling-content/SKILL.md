---
name: crawling-content
description: "High-speed read-only web extraction. Use when fetching documentation, blogs, and static pages. Do not use for apps requiring login or interaction."
allowed-tools: [Bash]
---

# Content Crawler Protocol

## Usage
Use `@just-every/crawl` for zero-latency markdown extraction.

### Single Page (Read)
```bash
npx -y @just-every/crawl "https://example.com"
```

### Site Map (Spider)
```bash
npx -y @just-every/crawl "https://example.com" --pages 20 --output json
```

## Failure Mode
If output contains "JavaScript required" or "Access Denied", **STOP**. Switch to `Skill(browsing-web)` to handle the dynamic rendering.
