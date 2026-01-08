---
description: |
  Execute comprehensive system design and architecture analysis using autonomous agent for deep architectural work.
  <example>
  Context: User needs system architecture
  user: "Design a real-time collaborative editing service"
  assistant: "I'll delegate to the architect agent for comprehensive system design."
  </example>
  <example>
  Context: Architecture analysis
  user: "Analyze our current architecture for scalability"
  assistant: "I'll use the system-design command for architecture analysis."
  </example>
  <example>
  Context: Technology selection
  user: "Design the architecture for our new API service"
  assistant: "I'll delegate for comprehensive system design and planning."
  </example>
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
argument-hint: [system requirements, design task, or architecture analysis request]
---

## Objective
Execute system design and architecture analysis for: $ARGUMENTS

## Deep Discovery Phase

Before delegating to the agent, gather comprehensive context by following the **Architectural Deep Discovery Protocol** from the `architecture` skill (`references/discovery.md`).


## Delegation Phase

<assignment>
Execute comprehensive system design or architecture analysis for: $ARGUMENTS

**Instruction:**
1. Read the `architecture` skill to understand the required frameworks and patterns.
2. Produce the final architecture package (Diagrams, ADRs, Roadmap) as specified in the skill.
</assignment>

<context>
You are the System Architect Agent executing in isolated context. 
Full project mapping and requirements analysis must be performed autonomously if not provided.
</context>

Execute via architect agent.

## Success Criteria

- [ ] Task type properly classified.
- [ ] Discovery protocol followed (`references/discovery.md`).
- [ ] Agent receives targeted context package.
- [ ] Architecture analysis addresses all quality criteria.
- [ ] Comprehensive documentation produced (Diagrams, ADRs, Roadmap, Risks).

