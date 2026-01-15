---
name: crawl
description: "Advanced crawling with configuration options (depth, format, etc)."
argument-hint: "<url> [options]"
allowed-tools: Bash
disable-model-invocation: true
---

# Command: /crawl

Executes a configurable crawl using the Fast Mode strategy.

## Usage
`npx @just-every/crawl <url> [options]`

## Context
!npx -y @just-every/crawl $ARGUMENTS

## Protocol
1.  **Analyze**: Review the output above.
2.  **Fallback**: If the output is empty or blocked (Cloudflare/JS), switch to **Interactive Mode** (Playwright) as defined in `Skill(browser-automation)`.
