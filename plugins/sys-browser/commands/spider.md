---
description: "Deep crawl (depth=20) to map a documentation site structure."
argument-hint: "<url>"
allowed-tools: [Skill(crawling-content)]
disable-model-invocation: true
---

Invoke `Skill(crawling-content)` to spider "$1" with `--pages 20 --output json`.
