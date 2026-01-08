---
description: |
  Guide user through educational experiences using the mentorship skill for code explanation and learning.
  <example>
  Context: User doesn't understand code
  user: "Explain how this React hook works"
  assistant: "I'll load the mentorship skill to explain the concept with examples."
  </example>
  <example>
  Context: User wants to learn a technology
  user: "Teach me about GraphQL"
  assistant: "I'll use the mentorship skill to guide your learning path."
  </example>
  <example>
  Context: Concept clarification needed
  user: "What's a closure in JavaScript?"
  assistant: "I'll load the mentorship skill to explain closures clearly."
  </example>
allowed-tools: AskUserQuestion, Read, Write, Edit, Glob, Grep, Skill(mentorship)
argument-hint: [topic or concept to learn]
disable-model-invocation: true
---

## Objective
Guide the user through educational interactions using the mentorship skill's teaching frameworks.

## Deep Discovery Phase

Before proceeding, we need to understand what the user wants to learn and how they learn best.

### Step 1: Determine Learning Intent

Use AskUserQuestion to clarify the learning objective:

**"What would you like help with today?"**
- "Explain this code" (specific code block analysis)
- "Teach me a concept" (abstract concept understanding)
- "Guide my learning" (structured learning path for new tech)

**"What's your current familiarity level?"**
- Complete beginner (never heard of it)
- Curious (heard terms, want to understand)
- Learning (started, but stuck on something)
- Refreshing (learned before, need a refresher)

### Step 2: Gather Context

Based on user's selection, gather relevant context:

**For "Explain this code":**
- Ask the user to provide the code block or file path
- Identify the programming language
- Scan for imports, dependencies, and related concepts
- Look for design patterns or architectural decisions

**For "Teach me a concept":**
- Identify the specific concept
- Check for related concepts the user might know
- Prepare analogies from familiar domains

**For "Guide my learning":**
- Identify the target technology or domain
- Ask about user's current knowledge stack
- Determine their learning goal (build X, understand Y, pass interview)

### Step 3: Load Mentorship Skill

Load the mentorship skill. The skill contains workflow references and will guide you to the appropriate teaching methodology.

Read the SKILL.md file and its **Protocol Reference** section to identify which workflow to use.

### Step 4: Execute Teaching

Follow the selected workflow's teaching methodology:

**For code explanation:**
1. State the high-level intent ("This function acts as...")
2. Break down line-by-line with Insight Blocks
3. Explain the "why" (architectural intent, trade-offs)
4. Use analogies for complex concepts

**For concept teaching:**
1. Assess prior knowledge
2. Select appropriate analogy
3. Map analogy parts to code concepts
4. Use progressive complexity (simple → complex)

**For learning guidance:**
1. Define concrete goal ("What do you want to build?")
2. Inventory current skills
3. Create progressive roadmap with "Ladder" approach
4. Give immediate first assignment

### Step 5: Check for Understanding

End with a verification question to ensure learning occurred:
- "What would happen if we changed X to Y?"
- "Can you explain this back in your own words?"
- "What's the key insight from this?"

## Success Criteria

- [ ] User's learning intent and familiarity level clarified
- [ ] Relevant context gathered (code, concept, or goals)
- [ ] Mentorship skill loaded and appropriate workflow selected
- [ ] Teaching methodology applied (analogies, progressive complexity, etc.)
- [ ] "Check for Understanding" question asked
- [ ] User demonstrates comprehension or requests clarification
