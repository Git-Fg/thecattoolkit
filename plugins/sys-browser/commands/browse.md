---
description: "Launch interactive browser session. Use for complex tasks."
argument-hint: "<url> [objective]"
allowed-tools: [Skill(browsing-web)]
disable-model-invocation: true
---

Invoke `Skill(browsing-web)` to navigate to "$1" and execute: "${2:-explore}".
