---
description: Guided feature development with codebase understanding and architecture focus
argument-hint: Optional feature description
---

# Feature Development

You are helping a developer implement a new feature. Follow a systematic approach: understand the codebase deeply, identify and ask about all underspecified details, design elegant architectures, then implement.

**Pattern:** Discovery First → Question Burst → Execution → Review
**Phases:** 7
**Question Points:** 2

## Core Principles

- **Ask clarifying questions**: Identify all ambiguities, edge cases, and underspecified behaviors. Present specific, concrete questions with multiple options rather than making assumptions. Wait for user responses before proceeding with implementation. Ask questions early (after understanding the codebase, before designing architecture).
- **Understand before acting**: Read and comprehend existing code patterns first
- **Read files identified by agents**: When launching agents, ask them to return lists of the most important files to read. After agents complete, read those files to build detailed context before proceeding.
- **Simple and elegant**: Prioritize readable, maintainable, architecturally sound code
- **Use TodoWrite**: Track all progress throughout

---

## Phase 1: Discovery

**Goal:** Understand what needs to be built
**Context:** Initial request: $ARGUMENTS
**Outcome:** Mental model of requirements, questions identified for later
**Interaction:** Zero (discovery only)

**Actions**:
1. Create todo list with all phases
2. Read and comprehend the feature request deeply
3. Form initial mental model of requirements
4. Note any unclear aspects for later questioning (do NOT ask yet)

---

## Phase 2: Codebase Exploration

**Goal:** Understand relevant existing code and patterns at both high and low levels
**Outcome:** Comprehensive codebase mental model, identified questions for clarification
**Interaction:** Zero (agent delegation only)
**Agents:** 2-3 parallel code-explorer agents

**Actions**:
1. Launch 2-3 code-explorer agents in parallel. Each agent should:
   - Trace through the code comprehensively and focus on getting a comprehensive understanding of abstractions, architecture and flow of control
   - Target a different aspect of the codebase (eg. similar features, high level understanding, architectural understanding, user experience, etc)
   - Include a list of 5-10 key files to read
   - Note architectural patterns, potential integration points, and implementation concerns for later analysis

   **Example agent prompts**:
   - "Find features similar to [feature] and trace through their implementation comprehensively"
   - "Map the architecture and abstractions for [feature area], tracing through the code comprehensively"
   - "Analyze the current implementation of [existing feature/area], tracing through the code comprehensively"
   - "Identify UI patterns, testing approaches, or extension points relevant to [feature]"

2. Once the agents return, read all files identified by agents to build deep understanding
3. Synthesize findings into comprehensive mental model of existing codebase
4. Identify gaps, ambiguities, and questions that need clarification (do NOT ask yet)

---

## Phase 3: Centralized Question Burst

**Goal:** Resolve ALL ambiguities at once for uninterrupted execution
**Outcome:** Complete requirements specification, all questions answered
**Interaction:** High (comprehensive Q&A)
**Critical:** This is the ONLY question-asking phase. DO NOT SKIP.

**Actions**:
1. Review findings from Phases 1-2 and original feature request
2. Compile comprehensive list of ALL questions needed:
   - Edge cases and error handling scenarios
   - Integration points with existing systems
   - Scope boundaries and feature requirements
   - Design preferences and architectural choices
   - Backward compatibility and performance needs
3. **Present all questions in one organized, centralized list**
4. **Wait for all answers before proceeding to architecture design**

This centralized approach enables uninterrupted flow through Phases 4-7.

If the user says "whatever you think is best", provide your recommendation and get explicit confirmation.

---

## Phase 4: Architecture Design

**Goal:** Design multiple implementation approaches with different trade-offs
**Outcome:** Architecture approach selected, implementation path defined
**Interaction:** Medium (architecture selection Q&A)
**Agents:** 2-3 parallel code-architect agents

**Actions**:
1. Launch 2-3 code-architect agents in parallel with different focuses: minimal changes (smallest change, maximum reuse), clean architecture (maintainability, elegant abstractions), or pragmatic balance (speed + quality)
2. Review all approaches and form your opinion on which fits best for this specific task (consider: small fix vs large feature, urgency, complexity, team context)
3. Present to user: brief summary of each approach, trade-offs comparison, **your recommendation with reasoning**, concrete implementation differences
4. **Ask user which approach they prefer**

---

## Phase 5: Implementation

**Goal:** Build the feature
**Outcome:** Fully implemented feature following chosen architecture
**Interaction:** Zero (pure execution)
**Critical:** DO NOT START WITHOUT USER APPROVAL

**Actions**:
1. Wait for explicit user approval
2. Read all relevant files identified in previous phases
3. Implement following chosen architecture
4. Follow codebase conventions strictly
5. Write clean, well-documented code
6. Update todos as you progress

---

## Phase 6: Quality Review

**Goal:** Ensure code is simple, DRY, elegant, easy to read, and functionally correct
**Outcome:** Quality issues identified and resolved based on user preferences
**Interaction:** Medium (quality findings + remediation decision)
**Agents:** 3 parallel code-reviewer agents

**Actions**:
1. Launch 3 code-reviewer agents in parallel with different focuses: simplicity/DRY/elegance, bugs/functional correctness, project conventions/abstractions
2. Consolidate findings and identify highest severity issues that you recommend fixing
3. **Present findings to user and ask what they want to do** (fix now, fix later, or proceed as-is)
4. Address issues based on user decision

---

## Phase 7: Summary

**Goal:** Document what was accomplished
**Outcome:** Complete documentation of implementation and decisions
**Interaction:** Zero (documentation only)

**Actions**:
1. Mark all todos complete
2. Summarize:
   - What was built
   - Key decisions made
   - Files modified
   - Suggested next steps