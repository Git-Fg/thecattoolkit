# Workflow Patterns

Common workflow patterns for different types of tasks using the 3-file system.

## Pattern 1: Simple Task (3-5 phases)

**Use for:** Straightforward tasks with clear sequential steps

```
Phase 1: Plan
Phase 2: Research/Gather
Phase 3: Execute
Phase 4: Review
Phase 5: Deliver
```

### Structure
```
task_plan.md    → Simple 5-phase plan
notes.md        → Findings and intermediate work
deliverable.md  → Final output
```

### Example Tasks
- Create a simple script
- Research a single topic
- Write a basic document
- Fix a specific bug

## Pattern 2: Complex Task (5-10 phases)

**Use for:** Multi-step projects with dependencies

```
Phase 1: Plan
Phase 2: Requirements analysis
Phase 3: Design
Phase 4: Implementation
Phase 5: Testing
Phase 6: Review
Phase 7: Refinement
Phase 8: Delivery
```

### Structure
```
task_plan.md    → Detailed phase tracking
notes.md        → Technical decisions, research
deliverable.md  → Final product/code
```

### Example Tasks
- Build a complete feature
- Create comprehensive documentation
- Develop a new tool
- Write a detailed report

## Pattern 3: Research Task

**Use for:** Information gathering and synthesis

```
Phase 1: Plan research
Phase 2: Gather sources
Phase 3: Analyze findings
Phase 4: Synthesize insights
Phase 5: Write report
Phase 6: Review and deliver
```

### Structure
```
task_plan.md    → Research phases and questions
notes.md        → Source findings and citations
deliverable.md  → Research report
```

### Example Tasks
- Market research
- Literature review
- Competitive analysis
- Technical research

## Pattern 4: Multi-Stream Research

**Use for:** Complex research with multiple parallel topics

```
Phase 1: Plan research streams
Phase 2: Research Stream A
Phase 3: Research Stream B
Phase 4: Research Stream C
Phase 5: Synthesize all streams
Phase 6: Create comprehensive deliverable
```

### Structure
```
task_plan.md    → Stream tracking
notes.md        → Findings from all streams
deliverable.md  → Comprehensive synthesis
```

### Stream Tracking in task_plan.md

```markdown
## Research Streams

### Stream A: [Topic]
- Progress: 60%
- Next: Evaluate options
- Files: stream_a_research.md

### Stream B: [Topic]
- Progress: 80%
- Next: Final analysis
- Files: stream_b_research.md

### Stream C: [Topic]
- Progress: 40%
- Next: Begin investigation
- Files: stream_c_research.md

## Integration Plan
Will synthesize all streams in Phase 5
```

## Pattern 5: Implementation Task

**Use for:** Building software, features, or tools

```
Phase 1: Create plan
Phase 2: Understand requirements
Phase 3: Design solution
Phase 4: Implement code
Phase 5: Test thoroughly
Phase 6: Document
Phase 7: Review and refine
Phase 8: Deploy/deliver
```

### Structure
```
task_plan.md    → Implementation phases
notes.md        → Technical decisions, code snippets
deliverable.md  → Final code/feature
```

### Technical Notes in notes.md

```markdown
## Architecture Decisions
- Decision: [What was chosen]
  Rationale: [Why]
  Alternatives: [What else was considered]

## Code Snippets
### Authentication Helper
```python
def authenticate(user):
    # Implementation
    pass
```

## Dependencies
- Library X: v2.1 - For feature Y
- Library Z: v1.5 - For feature W

## Testing Notes
- Unit tests: 45 passing
- Integration tests: 12 passing
- Coverage: 85%
```

## Pattern 6: Analysis Task

**Use for:** Data analysis, process review, evaluation

```
Phase 1: Plan analysis
Phase 2: Gather data
Phase 3: Analyze patterns
Phase 4: Draw conclusions
Phase 5: Create recommendations
Phase 6: Document findings
```

### Structure
```
task_plan.md    → Analysis framework
notes.md        → Data findings and analysis
deliverable.md  → Analysis report
```

### Analysis Notes Structure

```markdown
## Data Sources
- Source 1: [Description]
- Source 2: [Description]

## Methodology
- Approach: [How analysis was done]
- Tools used: [List]

## Key Findings
1. [Finding]
   Evidence: [Details]
   Confidence: [High/Medium/Low]

2. [Finding]
   Evidence: [Details]
   Confidence: [High/Medium/Low]

## Patterns Identified
- Pattern 1: [Description]
- Pattern 2: [Description]

## Anomalies
- [Anomaly]: [Why it's unusual]
```

## Pattern 7: Iterative Refinement

**Use for:** Tasks requiring multiple iterations

```
Phase 1: Plan
Phase 2: Create initial version
Phase 3: Gather feedback
Phase 4: Refine and improve
Phase 5: Re-test
Phase 6: Finalize
```

### Tracking Iterations

In task_plan.md:

```markdown
## Iterations

### Iteration 1: Initial Draft
- Date: [Date]
- Changes: [What changed]
- Feedback: [Summary]

### Iteration 2: First Revision
- Date: [Date]
- Changes: [What changed]
- Feedback: [Summary]

### Iteration 3: Final Revision
- Date: [Date]
- Changes: [What changed]
- Feedback: [Summary]
```

## Pattern 8: Debugging Task

**Use for:** Finding and fixing bugs

```
Phase 1: Document problem
Phase 2: Gather information
Phase 3: Identify root cause
Phase 4: Design solution
Phase 5: Implement fix
Phase 6: Test fix
Phase 7: Verify resolution
```

### Debugging in notes.md

```markdown
## Problem Description
- Issue: [What is broken]
- Expected: [What should happen]
- Actual: [What is happening]
- Reproducible: [Yes/No]

## Investigation
- Step 1: [What was tried]
  Result: [What was found]
- Step 2: [What was tried]
  Result: [What was found]

## Root Cause
[Cause identified]

## Solution
[Fix implemented]

## Verification
- Test case: [How verified]
- Result: [Outcome]
```

## Choosing the Right Pattern

### Decision Matrix

| Task Type | Complexity | Recommended Pattern |
|-----------|-----------|-------------------|
| Simple feature | Low | Pattern 1 (Simple) |
| Research report | Medium | Pattern 3 (Research) |
| Complex feature | High | Pattern 2 (Complex) |
| Multi-topic research | High | Pattern 4 (Multi-Stream) |
| Bug fix | Low-Medium | Pattern 8 (Debugging) |
| Data analysis | Medium | Pattern 6 (Analysis) |
| Creative work | Medium | Pattern 7 (Iterative) |
| Software build | High | Pattern 5 (Implementation) |

### Quick Selection Guide

**Ask yourself:**
1. Is this a single, straightforward task? → Pattern 1
2. Does it require research? → Pattern 3
3. Does it have multiple independent topics? → Pattern 4
4. Does it involve building something? → Pattern 5
5. Does it involve analyzing data? → Pattern 6
6. Will it need multiple iterations? → Pattern 7
7. Is it a debugging task? → Pattern 8

### Pattern Combinations

You can combine patterns:

**Example:** Research + Implementation
1. Use Pattern 3 (Research) for initial investigation
2. Switch to Pattern 5 (Implementation) for building solution
3. Use Pattern 7 (Iterative) for refinement

**Example:** Analysis + Multi-Stream
1. Use Pattern 4 (Multi-Stream) to gather data
2. Use Pattern 6 (Analysis) to analyze findings
3. Use Pattern 7 (Iterative) to refine conclusions

## Pattern Variations

### Scaling Up
For very large tasks:
- Add more phases
- Break into sub-tasks
- Use parallel streams
- Create milestone checkpoints

### Scaling Down
For very small tasks:
- Reduce to 3 phases
- Combine related phases
- Use simpler templates
- Focus on essentials

### Hybrid Patterns
Mix elements from different patterns:
- Research + Simple (Pattern 1 + 3)
- Implementation + Debugging (Pattern 5 + 8)
- Analysis + Research (Pattern 6 + 3)

## Best Practices

### Always
✅ Start with Pattern 1 for simple tasks
✅ Choose the simplest pattern that fits
✅ Adjust pattern as task evolves
✅ Document which pattern you're using

### Never
❌ Use Pattern 2 for simple tasks
❌ Skip planning phase
❌ Mix patterns without documenting
❌ Use overly complex pattern

### Tips
- Start simple, add complexity as needed
- Patterns are guidelines, not rules
- Adjust based on task evolution
- Learn from each pattern usage
