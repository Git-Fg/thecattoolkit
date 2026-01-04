---
name: {{SKILL_NAME}}
description: {{What it does}} {{MUST USE/PROACTIVELY USE/CONSULT}} when {{trigger conditions}}.
---

## Essential Principles

## {{Core Concept}}

{{Principles that ALWAYS apply, regardless of which workflow runs}}

### 1. {{First principle}}
{{Explanation}}

### 2. {{Second principle}}
{{Explanation}}

### 3. {{Third principle}}
{{Explanation}}

## Interaction Protocol

**CRITICAL: Determine execution mode BEFORE proceeding**

**IF invoked by User (Interactive Mode):**
The user is directly asking for {{skill domain}} help. Follow the Intake & Smart Routing section below.

**IF invoked by another Agent (Read-Only Mode):**
1. **IGNORE** the Intake & Smart Routing section below.
2. Read only the **Essential Principles** section above.
3. Read the **Reference Index** below.
4. **DO NOT** ask the user any questions.
5. Return the requested information to the invoking agent.

---

## Intake & Smart Routing (Interactive Mode Only)

**SKIP this section in Read-Only Mode**

### Step 1: Analyze Intent (Priority)

Check arguments, conversation history, and context for keywords. **Auto-route immediately** if intent is clear.

### Step 2: Auto-Route (Keyword-Based)

{{First category}} Keywords:
- `{{keyword-a}}`, `{{keyword-b}}` → `workflows/{{first-workflow}}.md`

{{Second category}} Keywords:
- `{{keyword-c}}`, `{{keyword-d}}` → `workflows/{{second-workflow}}.md`

{{Third category}} Keywords:
- `{{keyword-e}}`, `{{keyword-f}}` → `workflows/{{third-workflow}}.md`

**Context/Read-Only Keywords:**
- `guidance`, `help`, `explain`, `how do I`, `best practices` → Read **Essential Principles** above and exit

### Step 3: Fallback (Interactive - Ambiguous Intent)

**ONLY if intent is completely unclear after keyword analysis:**

What would you like to do?

1. {{First option}}
2. {{Second option}}
3. {{Third option}}

**Wait for response before proceeding.**

---

## Routing Table (Interactive Mode - Reference Only)

**SKIP this section in Read-Only Mode**

This table documents the keyword mappings used in Step 2 above.

| Response | Workflow |
|----------|----------|
| 1, "{{keywords}}" | `workflows/{{first-workflow}}.md` |
| 2, "{{keywords}}" | `workflows/{{second-workflow}}.md` |
| 3, "{{keywords}}" | `workflows/{{third-workflow}}.md` |

**After reading the workflow, follow it exactly.**

## Quick Reference

## {{Skill Name}} Quick Reference

{{Brief reference information always useful to have visible}}

## Reference Index

## Domain Knowledge

All in `references/`:
- {{reference-1.md}} - {{purpose}}
- {{reference-2.md}} - {{purpose}}

## Workflows Index

## Workflows

All in `workflows/`:

| Workflow | Purpose |
|----------|---------|
| {{first-workflow}}.md | {{purpose}} |
| {{second-workflow}}.md | {{purpose}} |
| {{third-workflow}}.md | {{purpose}} |

## Success Criteria

A well-executed {{skill name}}:
- {{First criterion}}
- {{Second criterion}}
- {{Third criterion}}
