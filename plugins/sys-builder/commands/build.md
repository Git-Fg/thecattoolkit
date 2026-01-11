---
description: "USE when executing project plans, building current active phases from ROADMAP.md, and running implementation tasks."
allowed-tools: [Read, Bash, Skill(builder-core), Task]
---

# Zero-Token Build Execution

1. **Identify Active Phase**: Read `.cattoolkit/planning/*/ROADMAP.md` to find current phase status
2. **Output Status**: Display current phase and task status for immediate context
3. **Invoke Builder**: Call builder-core skill with the active phase context
4. **Execute**: Delegate to director agent for autonomous execution

**Goal**: Provide immediate phase context without requiring user to specify which phase to build.
