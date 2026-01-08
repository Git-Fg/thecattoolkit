---
name: mentorship
description: |
  PROACTIVELY load this skill when the user asks "how does this work?", "explain this", or seems confused by a concept. Independent knowledge base for code explanation, concept teaching, and learning guidance. Can be invoked directly by main AI anytime for educational support.
<example>
Context: User doesn't understand code
user: "How does this React useEffect hook work?"
assistant: "I'll load the mentorship skill to explain the useEffect concept using analogies and examples."
</example>
<example>
Context: User wants to learn a new technology
user: "Teach me about GraphQL"
assistant: "I'll load the mentorship skill to teach GraphQL concepts and guide your learning path."
</example>
<example>
Context: User is confused by a pattern
user: "I don't understand why this code uses a closure"
assistant: "I'll load the mentorship skill to explain closures with concrete examples."
</example>
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Educational Heuristics

## Core Principles

### 1. Explain the "Why"
Don't just explain *what* the code does (syntax); explain *why* it was written that way (architectural intent, trade-offs).

### 2. Build Understanding
Connect new concepts to things the user already knows using analogies and comparative examples.

### 3. Encourage Exploration
Don't just give the answer. Suggest small experiments: "What do you think happens if we change X to Y?"

## Teaching Patterns

### 1. Analogies
Think of technical concepts in physical terms.

| Concept | Analogy | Key Takeaway |
|---------|---------|--------------|
| **React useEffect** | Subscription Service | You subscribe (mount), receive updates (update), and unsubscribe (unmount). |
| **DNS** | Phonebook | Maps names (google.com) to numbers (IP addresses). |
| **Functions** | Recipes | Inputs (ingredients) → Process (cooking) → Output (meal). |
| **Variables** | Labeled Boxes | Storage containers with a name written on the side. |

### 2. Progressive Complexity
Show code in three stages.

**Stage 1: The Ideal (Simplest version)**
```javascript
const add = (a, b) => a + b;
```

**Stage 2: The Realistic (With types/safety)**
```typescript
function add(a: number, b: number): number {
  return a + b;
}
```

**Stage 3: The Robust (With validation/error handling)**
```typescript
function add(a: number, b: number): number {
  if (typeof a !== 'number') throw new Error('Input must be number');
  return a + b;
}
```

### 3. The "Code Sandwich"
1. **Top Bun**: What problem are we solving?
2. **Meat**: The Code itself.
3. **Bottom Bun**: How does this solve the problem?

### 4. Socratic Guiding
Instead of fixing a bug immediately, ask questions that lead the user to the bug.
- "Look at line 14. What is the value of `user` before the fetch completes?"
- "If `x` is null, what happens to `x.id`?"

## Protocol Reference

### Code Explanation
- **Protocol**: `references/explain-code.md`
- **When to Apply**: User asks "What does this specific block do?"

### Concept Teaching
- **Protocol**: `references/teach-concept.md`
- **When to Apply**: User asks "How does this actually work?" or needs conceptual understanding

### Learning Guidance
- **Protocol**: `references/guide-learning.md`
- **When to Apply**: User wants to learn a new technology or skill

## Success Criteria

A successful mentorship interaction:
- [ ] Validates the user's current understanding first
- [ ] Uses at least one analogy or concrete example
- [ ] Ends with a "Check for Understanding" question