#!/bin/bash

HEADER="<system_constraints>
1. **Uninterrupted Flow**: NO questions mid-execution. Make strategic assumptions.
2. **Quota Efficiency**: Prefer COMMANDS (Cost:1) over AGENTS (Cost:20k).
3. **No Permission Fishing**: Invoke matching Skill/Command immediately.
4. **Trust Return Codes**: Do not read files immediately after writing if exit code is 0.
</system_constraints>

<quota_thresholds>
- Inline Skill: < 10 files
- Forked Skill: > 10 files
- Subagent: > 50 files (CRITICAL: AVOID IF POSSIBLE)
</quota_thresholds>"

# Auto-load persistent context if available
if [ -f ".cattoolkit/context/scratchpad.md" ]; then
    SCRATCHPAD=$(cat .cattoolkit/context/scratchpad.md)
    HEADER="$HEADER

=== PERSISTENT CONTEXT (Auto-Loaded) ===
$SCRATCHPAD
"
fi

# Auto-load project roadmap if available
if [ -f ".cattoolkit/planning" ] && find .cattoolkit/planning -name "ROADMAP.md" -type f 2>/dev/null | grep -q .; then
    ROADMAP=$(find .cattoolkit/planning -name "ROADMAP.md" -type f -exec cat {} \;)
    HEADER="$HEADER

=== PROJECT ROADMAP (Auto-Loaded) ===
$ROADMAP
"
fi

# CRITICAL OVERRIDE for Worker Agents
# This protocol injection prevents AskUserQuestion leaks in builder/executor agents
if [ -n "$CLAUDE_AGENT_NAME" ]; then
    if [[ "$CLAUDE_AGENT_NAME" == "worker" || "$CLAUDE_AGENT_NAME" == "builder" || "$CLAUDE_AGENT_NAME" == "executor" ]]; then
        HEADER="$HEADER

<CRITICAL_OVERRIDE>
You are running as a sub-agent named '$CLAUDE_AGENT_NAME':
1. FORBIDDEN from using AskUserQuestion - Make Strategic Assumptions
2. Check '.cattoolkit/planning/' files for missing information
3. If blocked, create 'HANDOFF.md' and exit
</CRITICAL_OVERRIDE>"
    fi
fi

jq -n --arg ctx "$HEADER" '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}'
