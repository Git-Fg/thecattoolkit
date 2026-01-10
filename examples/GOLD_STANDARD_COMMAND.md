---
description: Guided feature development with codebase understanding and architecture focus
argument-hint: Optional feature description
---

# Feature Development Command (Gold Standard)

This command demonstrates the **ideal pattern** for complex multi-phase workflows that orchestrate multiple agents.

**Pattern:** Discovery → Exploration (Agents) → Questions → Architecture (Agents) → Implementation → Review (Agents) → Summary

## Core Principles

- **Understand before acting:** Read and comprehend existing code patterns first
- **Ask clarifying questions:** Identify ambiguities early, present specific options
- **Delegate to agents:** Use parallel agents for exploration, architecture, and review
- **Use TodoWrite:** Track progress throughout

---

## Phase 1: Discovery

**Goal:** Understand what needs to be built
**Outcome:** Mental model of requirements
**Interaction:** None (discovery only)

**Actions:**
1. Create todo list with all phases
2. Read and comprehend the feature request: $ARGUMENTS
3. Form initial mental model of requirements
4. Note unclear aspects for later questioning

---

## Phase 2: Codebase Exploration

**Goal:** Understand relevant existing code and patterns
**Outcome:** Comprehensive codebase mental model
**Interaction:** None (agent delegation only)

**Actions:**
1. Launch 2-3 code-explorer agents **in parallel** via Task tool:
   - Agent 1: Find features similar to the requested feature
   - Agent 2: Map architecture and abstractions for the relevant area
   - Agent 3: Identify UI patterns, testing approaches, or extension points

   Each agent should return a list of 5-10 key files to read.

2. Read all files identified by agents
3. Synthesize findings into comprehensive mental model
4. Identify gaps and questions for Phase 3

---

## Phase 3: Centralized Question Burst

**Goal:** Resolve ALL ambiguities at once for uninterrupted execution
**Outcome:** Complete requirements specification
**Interaction:** High (comprehensive Q&A)
**Critical:** This is the ONLY question-asking phase

**Actions:**
1. Compile comprehensive list of ALL questions:
   - Edge cases and error handling
   - Integration points
   - Scope boundaries
   - Design preferences
   - Backward compatibility
2. Present all questions in one organized list
3. Wait for all answers before proceeding

---

## Phase 4: Architecture Design

**Goal:** Design implementation approaches with trade-offs
**Outcome:** Architecture approach selected
**Interaction:** Medium (architecture selection)

**Actions:**
1. Launch 2-3 code-architect agents **in parallel** via Task tool:
   - Approach 1: Minimal changes (smallest change, maximum reuse)
   - Approach 2: Clean architecture (maintainability, elegant abstractions)
   - Approach 3: Pragmatic balance (speed + quality)

2. Present to user:
   - Brief summary of each approach
   - Trade-offs comparison
   - Your recommendation with reasoning
3. Ask which approach they prefer

---

## Phase 5: Implementation

**Goal:** Build the feature
**Outcome:** Fully implemented feature
**Interaction:** None (pure execution)
**Critical:** Wait for explicit user approval

**Actions:**
1. Wait for explicit user approval
2. Read all relevant files from previous phases
3. Implement following chosen architecture
4. Follow codebase conventions strictly
5. Update todos as you progress

---

## Phase 6: Quality Review

**Goal:** Ensure code quality and correctness
**Outcome:** Quality issues resolved
**Interaction:** Medium (findings + decision)

**Actions:**
1. Launch 3 code-reviewer agents **in parallel** via Task tool:
   - Reviewer 1: Simplicity, DRY, elegance
   - Reviewer 2: Bugs, functional correctness
   - Reviewer 3: Project conventions, abstractions

2. Consolidate findings
3. Present to user and ask what they want to do
4. Address issues based on decision

---

## Phase 7: Summary

**Goal:** Document what was accomplished
**Outcome:** Complete documentation
**Interaction:** None

**Actions:**
1. Mark all todos complete
2. Summarize: what was built, key decisions, files modified, next steps