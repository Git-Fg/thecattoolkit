# Example 3: Complex Command - Database Performance Optimization

**Complexity:** High
**Pattern Applied:** GOLD_STANDARD_COMMAND (7 phases)
**Template Used:** `command-complex.md`
**When to Use:** Multi-phase workflow with user approval gates

---

## The Complete Workflow

This example demonstrates a 7-phase workflow for optimizing database performance, showing how complex prompts require structured phases with explicit approval gates.

### Phase 1: Discovery ✅

1. Create TodoWrite checklist with all 7 phases
2. Parse and comprehend the database optimization request
3. Form initial mental model of requirements
4. Document unclear aspects for Phase 3 questioning

**TodoWrite Created:**
```
- [ ] Phase 1: Discovery
- [ ] Phase 2: Database Exploration
- [ ] Phase 3: Requirements & Questions
- [ ] Phase 4: Optimization Strategy Design
- [ ] Phase 5: Implementation
- [ ] Phase 6: Performance Review
- [ ] Phase 7: Summary
```

---

### Phase 2: Database Exploration

**Goal:** Build comprehensive database schema and query mental model
**Mode:** READ-ONLY (via Explore agents)
**Interaction:** None

<sub_agents>
**Schema Agent:** Database structure specialist. Analyzes tables, indexes, relationships. READ-ONLY.

**Query Agent:** Query analysis specialist. Identifies slow queries, patterns, optimization opportunities. READ-ONLY.

**Performance Agent:** Performance monitoring specialist. Analyzes metrics, bottlenecks, resource usage. READ-ONLY.

**=== CRITICAL: ALL SUB-AGENTS ARE READ-ONLY — NO FILE MODIFICATIONS ===**
</sub_agents>

1. Launch 3 Explore agents **in parallel** via Task tool:
   - Agent 1: Map database schema (tables, indexes, relationships)
   - Agent 2: Analyze current queries and identify slow patterns
   - Agent 3: Review performance metrics and bottleneck identification

2. Read ALL files identified by agents
3. Synthesize findings into comprehensive mental model
4. Identify gaps → feed into Phase 3 questions

---

### Phase 3: Centralized Question Burst

**Goal:** Resolve ALL ambiguities for uninterrupted execution
**Mode:** READ-ONLY
**Interaction:** HIGH (comprehensive Q&A)

**=== CRITICAL: THIS IS THE ONLY QUESTION-ASKING PHASE ===**

**Questions Before Optimization:**

**Performance Goals:**
1. What is the target performance improvement (e.g., 50% faster queries)?
2. Are there specific queries that must meet particular SLAs?

**Constraints:**
3. Can we add indexes (storage overhead acceptable)?
4. Are schema changes allowed, or only query optimization?
5. What is the maintenance window for optimization work?

**Priority:**
6. Which database tables/queries are most critical to business operations?
7. Are there any queries that should NOT be modified (legacy, risk-averse)?

**Environment:**
8. What is the database version and configuration?
9. Are there replication or clustering considerations?

WAIT for complete answers before proceeding.

---

### Phase 4: Optimization Strategy Design

**Goal:** Design and present optimization approaches with trade-offs
**Mode:** READ-ONLY (via Plan agents)
**Interaction:** MEDIUM (strategy selection)

1. Launch 3 Plan agents **in parallel** via Task tool:
   - Approach A: Index Optimization (add indexes, query rewrites)
   - Approach B: Schema Redesign (normalize/denormalize, partitioning)
   - Approach C: Hybrid Approach (indexes + targeted schema changes)

2. Present to user with structured comparison:

### Optimization Options

| Approach | Pros | Cons | Estimated Improvement | Risk Level |
|----------|------|------|---------------------|------------|
| A: Index Only | Low risk, fast implementation | Limited improvement | 30-50% | Low |
| B: Schema Redesign | Maximum improvement | High risk, downtime | 70-90% | High |
| C: Hybrid | Balanced approach | More complex | 50-70% | Medium |

**Recommendation:** Approach C (Hybrid) because it provides significant improvement with manageable risk.

Which approach do you prefer?

3. WAIT for user selection before proceeding

---

### Phase 5: Implementation

**Goal:** Implement the selected optimization strategy
**Mode:** WRITE
**Interaction:** None (pure execution)

**=== CRITICAL: REQUIRES EXPLICIT USER APPROVAL ===**

**MANDATORY PREREQUISITE — VERIFY BEFORE STARTING:**
- [ ] User has explicitly selected an optimization approach
- [ ] All Phase 3 questions have been answered
- [ ] Database mental model is complete
- [ ] You have re-read critical schema files from Phase 2

1. Confirm explicit user approval to proceed
2. Re-read critical database files identified in Phase 2
3. Implement following the chosen optimization approach EXACTLY
4. Follow database best practices strictly:
   - Test all changes in staging first
   - Document all index additions
   - Verify query performance before/after
5. Update TodoWrite as each component completes

---

### Phase 6: Performance Review

**Goal:** Ensure optimization quality and correctness
**Mode:** READ-ONLY (via Review agents)
**Interaction:** MEDIUM (findings + decision)

1. Launch 3 Review agents **in parallel** via Task tool:
   - Reviewer 1: Performance metrics, improvement verification
   - Reviewer 2: Query correctness, edge cases, data integrity
   - Reviewer 3: Best practices, index efficiency, maintenance

2. Consolidate findings into severity-ranked list:

### Review Findings

**Critical (must fix):**
- [Performance regression in query X]: [Location] — [Reason]

**Recommended (should fix):**
- [Missing index on frequently queried column]: [Location] — [Reason]

**Optional (nice to have):**
- [Query could be further optimized with materialized view]: [Location] — [Reason]

How would you like to proceed?
- A) Fix all issues
- B) Fix critical + recommended only
- C) Fix critical only
- D) Deploy as-is

3. Implement fixes based on user decision

---

### Phase 7: Summary

**Goal:** Document what was accomplished
**Mode:** READ-ONLY
**Interaction:** None

1. Mark all TodoWrite items complete
2. Generate structured summary:

## Optimization Complete

**Built:** Database performance optimization for [system name]

**Key Decisions:**
- Selected Hybrid Approach (Index + Schema): Balanced improvement vs. risk
- Prioritized critical queries: Orders, Payments, User Management
- Added 12 strategic indexes: Improved join performance by 65%

**Files Modified:**
- `schema/tables/orders.sql` — Added composite index on (user_id, created_at)
- `migrations/2024_01_add_performance_indexes.sql` — New indexes for hot paths
- `docs/optimization-report.md` — Performance analysis and results

**Performance Results:**
- Average query time: Reduced from 450ms to 180ms (60% improvement)
- 95th percentile: Reduced from 1200ms to 350ms (71% improvement)
- Database CPU: Reduced from 85% to 45% average utilization

**Next Steps (if any):**
- Monitor performance for 2 weeks to confirm stability
- Consider partitioning strategy for orders table (Phase 2)
- Implement query result caching for top 10 queries

---

## Key Takeaways

1. **Phase Separation:** Clear read-only vs. write phases prevent mistakes
2. **Approval Gates:** User makes architectural decisions at Phases 3 and 4
3. **Parallel Agents:** Phase 2 and 6 use parallel execution for speed
4. **Question Consolidation:** All questions asked in Phase 3 prevent flow breaks
5. **Quality Review:** Phase 6 provides structured review with severity ranking
6. **Success Metrics:** Phase 7 documents measurable outcomes
