# Communication Standards

## 1. The Markdown Prompt Pattern
When a Command delegates to an Agent (Triangle Pattern), it must construct a strict **Markdown Prompt**. The Agent does not have access to the main chat history; it only sees the Prompt.

**Prompt Structure (in Command):**
```markdown
# Context
{DATA: Variables, file paths, and raw content needed.}
<!-- Use !bash commands here to inject dynamic state -->

# Assignment
{GOAL: What specific outcome is required?}

## Standards
{RULES: Which Skill/Reference files must be obeyed?}

## Constraints
{BOUNDARIES: What is forbidden?}
```

*   **Markdown:** Use for **Content** and **Prompt Structure** (Instructions, Explanations, Templates, # Context, # Assignment).
*   **XML:** Use for **Machine Data Retrieval** ONLY (Max 5 tags, no nesting). Tags like `<example>` are reserved for the Runtime.
*   *Why:* Claude Code is optimized for Markdown prompts. XML tags in prompts are unnecessary and can be confusing.

## 3. The "Hot-Potato" Handoff
*   **Interactive Phase:** The Command (Vector) asks the user for clarifications *before* dispatching.
*   **Silent Phase:** Once the Agent (Triangle) is launched, **NO USER INTERACTION IS ALLOWED**. The Agent must assume the Prompt is complete.
    *   If info is missing: The Agent checks `standards-quality.md` for default behaviors or fails gracefully.
