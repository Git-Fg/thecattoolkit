---
description: "Diagnose plugin environment and configuration."
argument-hint: "No arguments"
allowed-tools: [Bash, Skill(toolkit-registry)]
disable-model-invocation: true
---

# System Doctor

Run the following checks to verify the environment:

1. **Plugin Root**: !`echo ${CLAUDE_PLUGIN_ROOT}`
2. **Project Root**: !`echo ${CLAUDE_PROJECT_DIR}`
3. **Node Version**: !`node -v`
4. **Python Version**: !`python --version`
5. **UV Status**: !`uv --version`
