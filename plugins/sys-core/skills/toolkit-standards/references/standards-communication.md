# Communication Standards

## 1. Natural Language Delegation (Delegated Pattern)
When a Command delegates to an Agent (Delegated Pattern), it must construct a structured prompt using Markdown headers. The Agent does not have access to the main chat history; it only sees the provided prompt.

**Standard Delegation Structure:**
```markdown
# Context
{DATA: Background variables, file paths, and raw content needed.}
<!-- Pro-Tip: Inject dynamic state directly into the section -->

# Assignment
**Goal:** {Specific outcome required}

## Instructions
{Step-by-step guidance for the agent}

## Requirements & Constraints
{RULES: Which Skill/Reference files must be obeyed? What is forbidden?}

## Quality Standards
{Expected output format and verification criteria}
```

## 2. XML vs. Markdown usage (Law 9)
*   **Markdown:** The PRIMARY format for **Instructions** and **Structuring Thought**.
*   **XML:** Reserved for **Machine Signaling** and **Data Isolation**.
    *   *Usage:* Grouping high-noise raw data (hooks), signaling tool outputs, or semantic grouping in complex inputs.
    *   *Constraint:* Max 15 tags per scope, no deep nesting.

## 3. Direct execution (Direct Pattern)
*   **Interactive Phase:** Commands running in the foreground (Direct Pattern) may use `AskUserQuestion` for clarifications.
*   **Execution Isolation:** Once an Agent (Delegated) is launched, **NO USER INTERACTION IS ALLOWED**. The Agent operates in Uninterrupted Flow.
    *   If info is missing: The Agent uses `execution-core` Handoff protocols and terminates.
