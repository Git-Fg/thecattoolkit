# Workflow: Explain Code

## Purpose
Deconstruct a piece of code to build mental models, not just syntax definition.

## Process

### Step 1: The "High-Level Intent"
Before analyzing lines, state the goal.
- **Pattern**: "This function acts as a [Role], responsible for [Outcome]."
- **Example**: "This `useEffect` acts as a subscription manager. It ensures we listen to data only while the component is on screen."

### Step 2: Line-by-Line (The "How")
Break down complex logic. Use the **Insight Block** format:

```text
★ Insight ─────────────────────────────────────
[2-3 key educational points about this code]
─────────────────────────────────────────────────

[Code block]

📚 What's happening here:
1. [Step-by-step explanation]
2. [Why each part matters]

## Success Criteria
- [ ] High-level intent clearly stated before line-by-line analysis
- [ ] Complex logic explained with Insight Blocks
- [ ] Architectural intent and trade-offs explained (not just syntax)
- [ ] User demonstrates understanding or asks clarifying questions