# Communication Standards

## 1. The Envelope Pattern
When a Command delegates to an Agent (Triangle Pattern), it must construct a strict **Envelope**. The Agent does not have access to the main chat history; it only sees the Envelope.

**Envelope Structure (in Command):**
```xml
<envelope>
  <intent>
    {GOAL: What specific outcome is required?}
  </intent>
  <context>
    {DATA: Variables, file paths, and raw content needed.}
    <!-- Use !bash commands here to inject dynamic state -->
  </context>
  <standards>
    {RULES: Which Skill/Reference files must be obeyed?}
  </standards>
  <constraints>
    {BOUNDARIES: What is forbidden?}
  </constraints>
</envelope>
```

## 2. XML vs. Markdown usage
*   **Markdown:** Use for **Content** (Instructions, Explanations, Templates).
*   **XML:** Use for **Data Structures** (The Envelope, extracted code blocks, lists of files).
*   *Why:* LLMs follow Markdown instructions better, but parse XML data more accurately.

## 3. The "Hot-Potato" Handoff
*   **Interactive Phase:** The Command (Vector) asks the user for clarifications *before* dispatching.
*   **Silent Phase:** Once the Agent (Triangle) is launched, **NO USER INTERACTION IS ALLOWED**. The Agent must assume the Envelope is complete.
    *   If info is missing: The Agent checks `standards-quality.md` for default behaviors or fails gracefully.
