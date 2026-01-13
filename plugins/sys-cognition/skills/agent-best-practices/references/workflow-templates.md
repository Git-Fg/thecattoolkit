# Workflow Templates: Ready-to-Use Agent Workflows

## Template 1: Feature Development Workflow

### When to Use
Implementing new features, functionality, or capabilities.

### Structure
```
1. Requirement Analysis
2. Architecture Design
3. Implementation Plan
4. Development
5. Testing
6. Documentation
7. Review
8. Deployment
```

### Example Implementation
```markdown
# Feature Development Workflow

## Step 1: Requirement Analysis
**Prompt**: "Analyze the request to add user profile management. Identify:
- Core requirements
- Edge cases
- Dependencies
- Success criteria"

**Agent Output**:
- Requirements summary
- Clarifying questions
- Risk assessment

## Step 2: Architecture Design
**Prompt**: "Design architecture for user profile system:
- Data models (User, Profile, Settings)
- API endpoints needed
- Database schema
- Integration points"

**Agent Output**:
- Architecture diagram (text-based)
- API specification
- Data models
- Integration plan

## Step 3: Implementation Plan
**Prompt**: "Create implementation plan for user profiles:
- Breakdown into tasks
- Task dependencies
- Estimated effort
- Risk mitigation"

**Agent Output**:
- Task list with priorities
- Dependencies mapped
- Timeline estimate
- Risk register

## Step 4: Development
**Prompt**: "Implement user profile system according to plan:
- Follow architecture design
- Use existing patterns
- Add tests
- Update documentation"

**Agent Output**:
- Code implementation
- Test coverage
- Documentation updates

## Step 5: Testing
**Prompt**: "Verify user profile implementation:
- Run all tests
- Manual testing of critical paths
- Edge case validation
- Performance check"

**Agent Output**:
- Test results
- Performance metrics
- Issues found (if any)

## Step 6: Documentation
**Prompt**: "Update documentation for user profiles:
- API documentation
- User guide
- Developer notes
- Change log"

**Agent Output**:
- Updated docs
- Examples
- Migration guide

## Step 7: Review
**Prompt**: "Review user profile implementation:
- Code quality check
- Architecture review
- Security review
- Performance review"

**Agent Output**:
- Review checklist
- Issues identified
- Recommendations

## Step 8: Deployment
**Prompt**: "Deploy user profile system:
- Deploy to staging
- Run integration tests
- Deploy to production
- Monitor for issues"

**Agent Output**:
- Deployment status
- Monitoring dashboard
- Rollback plan
```

## Template 2: Bug Fix Workflow

### When to Use
Fixing defects, errors, or unexpected behavior.

### Structure
```
1. Problem Identification
2. Reproduction
3. Root Cause Analysis
4. Solution Design
5. Fix Implementation
6. Verification
7. Prevention
```

### Example Implementation
```markdown
# Bug Fix Workflow

## Step 1: Problem Identification
**Prompt**: "Investigate bug report: 'Users can't log in after password change'
Gather:
- Error messages
- User actions
- Environment details
- Frequency"

**Agent Output**:
- Problem summary
- Affected systems
- Initial hypotheses

## Step 2: Reproduction
**Prompt**: "Reproduce the login bug:
- Follow exact user steps
- Note exact error messages
- Check browser console
- Test in different environments"

**Agent Output**:
- Reproduction steps
- Error details
- Environment details
- Consistent or intermittent?

## Step 3: Root Cause Analysis
**Prompt**: "Analyze root cause of login bug:
- Check authentication flow
- Review password change logic
- Examine token handling
- Look for race conditions"

**Agent Output**:
- Root cause identified
- Evidence collected
- Impact assessment

## Step 4: Solution Design
**Prompt**: "Design fix for login bug:
- Multiple solution options
- Pros/cons of each
- Risk assessment
- Implementation complexity"

**Agent Output**:
- Recommended solution
- Alternative options
- Implementation plan

## Step 5: Fix Implementation
**Prompt**: "Implement fix for login bug:
- Follow solution design
- Add tests
- Update error handling
- Document changes"

**Agent Output**:
- Fixed code
- Tests added
- Documentation updated

## Step 6: Verification
**Prompt**: "Verify fix works:
- Test reproduction scenario
- Test edge cases
- Run full test suite
- Performance check"

**Agent Output**:
- Verification results
- Test coverage
- No regressions

## Step 7: Prevention
**Prompt**: "Prevent future occurrence:
- Add monitoring
- Improve tests
- Update documentation
- Create runbook"

**Agent Output**:
- Monitoring added
- Tests improved
- Documentation updated
- Runbook created
```

## Template 3: Refactoring Workflow

### When to Use
Improving code structure, readability, or maintainability without changing behavior.

### Structure
```
1. Assessment
2. Strategy
3. Incremental Plan
4. Safe Refactoring
5. Verification
6. Documentation
```

### Example Implementation
```markdown
# Refactoring Workflow

## Step 1: Assessment
**Prompt**: "Assess refactoring target: 'Authentication middleware is too complex'
Analyze:
- Current code structure
- Complexity metrics
- Pain points
- Dependencies"

**Agent Output**:
- Current state summary
- Complexity issues
- Refactoring opportunities
- Risk areas

## Step 2: Strategy
**Prompt**: "Design refactoring strategy:
- Target improvements
- Approach (big-bang vs incremental)
- Risk mitigation
- Success criteria"

**Agent Output**:
- Refactoring strategy
- Target improvements
- Risk mitigation plan
- Success criteria

## Step 3: Incremental Plan
**Prompt**: "Create incremental refactoring plan:
- Break into safe steps
- Each step is reversible
- Test after each step
- Rollback plan"

**Agent Output**:
- Step-by-step plan
- Testing strategy
- Rollback procedures

## Step 4: Safe Refactoring
**Prompt**: "Execute refactoring incrementally:
- Complete one step at a time
- Run tests after each step
- Commit frequently
- Monitor for issues"

**Agent Output**:
- Refactored code
- Test results
- Commits

## Step 5: Verification
**Prompt**: "Verify refactoring quality:
- All tests pass
- No performance regression
- Code review passed
- Behavior unchanged"

**Agent Output**:
- Verification results
- Performance metrics
- Review feedback

## Step 6: Documentation
**Prompt**: "Document refactoring:
- What was changed
- Why it was changed
- Benefits achieved
- Lessons learned"

**Agent Output**:
- Refactoring summary
- Benefits achieved
- Lessons learned
- Future recommendations
```

## Template 4: Code Review Workflow

### When to Use
Reviewing agent-generated or team-generated code for quality.

### Structure
```
1. Pre-Review Setup
2. Initial Scan
3. Detailed Review
4. Testing Assessment
5. Security Review
6. Performance Review
7. Final Report
```

### Example Implementation
```markdown
# Code Review Workflow

## Step 1: Pre-Review Setup
**Prompt**: "Set up code review for authentication PR:
- Understand context
- Review requirements
- Check related PRs
- Prepare review checklist"

**Agent Output**:
- Review context
- Checklist prepared
- Questions noted

## Step 2: Initial Scan
**Prompt**: "Perform initial scan of auth PR:
- High-level architecture
- Code organization
- Immediate red flags
- File structure"

**Agent Output**:
- Initial assessment
- Red flags (if any)
- Overall impression

## Step 3: Detailed Review
**Prompt**: "Detailed review of auth PR:
- Logic correctness
- Edge cases
- Error handling
- Code style
- Best practices"

**Agent Output**:
- Detailed findings
- Specific issues
- Recommendations

## Step 4: Testing Assessment
**Prompt**: "Review test coverage:
- Unit tests present
- Integration tests adequate
- Edge cases covered
- Test quality"

**Agent Output**:
- Test coverage assessment
- Missing tests
- Test quality feedback

## Step 5: Security Review
**Prompt**: "Security review of auth PR:
- Input validation
- Authentication/authorization
- Sensitive data handling
- Security best practices"

**Agent Output**:
- Security assessment
- Vulnerabilities (if any)
- Security recommendations

## Step 6: Performance Review
**Prompt**: "Performance review of auth PR:
- Time complexity
- Space complexity
- Bottlenecks
- Scalability concerns"

**Agent Output**:
- Performance assessment
- Bottlenecks identified
- Optimization suggestions

## Step 7: Final Report
**Prompt**: "Compile final review report:
- Summary of findings
- Critical issues
- Recommended changes
- Overall recommendation"

**Agent Output**:
- Review summary
- Action items
- Final recommendation
```

## Template 5: Research Workflow

### When to Use
Exploring new technologies, patterns, or approaches.

### Structure
```
1. Define Research Questions
2. Gather Information
3. Analyze Options
4. Prototype/Proof of Concept
5. Evaluate Results
6. Recommendations
```

### Example Implementation
```markdown
# Research Workflow

## Step 1: Define Research Questions
**Prompt**: "Define research questions for 'Should we use GraphQL?'
- What problems does it solve?
- What are alternatives?
- What's the learning curve?
- Performance implications?
- Team impact?"

**Agent Output**:
- Research questions
- Success criteria
- Timeline

## Step 2: Gather Information
**Prompt**: "Gather information about GraphQL:
- Official documentation
- Case studies
- Performance benchmarks
- Community feedback
- Integration examples"

**Agent Output**:
- Information summary
- Key sources
- Data points

## Step 3: Analyze Options
**Prompt**: "Analyze GraphQL vs REST:
- Pros/cons comparison
- Use case fit
- Performance comparison
- Maintenance overhead"

**Agent Output**:
- Comparison matrix
- Fit assessment
- Trade-offs identified

## Step 4: Prototype
**Prompt**: "Create GraphQL proof of concept:
- Simple API example
- Compare with REST version
- Measure performance
- Assess complexity"

**Agent Output**:
- Working prototype
- Performance data
- Complexity analysis

## Step 5: Evaluate Results
**Prompt**: "Evaluate GraphQL POC:
- Does it meet requirements?
- Performance vs REST?
- Developer experience?
- Maintenance burden?"

**Agent Output**:
- Evaluation results
- Metrics collected
- Trade-offs confirmed

## Step 6: Recommendations
**Prompt**: "Make recommendation on GraphQL:
- Go/no-go decision
- Implementation approach
- Migration strategy
- Risk mitigation"

**Agent Output**:
- Clear recommendation
- Rationale
- Implementation plan
- Risk mitigation
```

## Template 6: Migration Workflow

### When to Use
Migrating between technologies, versions, or architectures.

### Structure
```
1. Inventory
2. Risk Assessment
3. Migration Plan
4. Pilot/MVP
5. Phased Migration
6. Validation
7. Completion
```

### Example Implementation
```markdown
# Migration Workflow

## Step 1: Inventory
**Prompt**: "Inventory components for React 17 → React 18 migration:
- All components
- Dependencies
- Peer dependencies
- Breaking changes needed"

**Agent Output**:
- Component inventory
- Dependency analysis
- Impact assessment

## Step 2: Risk Assessment
**Prompt**: "Assess migration risks:
- Breaking changes
- Performance risks
- Compatibility issues
- Rollback complexity"

**Agent Output**:
- Risk matrix
- Mitigation strategies
- Rollback plan

## Step 3: Migration Plan
**Prompt**: "Create migration plan:
- Phases/stages
- Testing strategy
- Rollback procedures
- Timeline"

**Agent Output**:
- Detailed migration plan
- Testing approach
- Rollback procedures

## Step 4: Pilot/MVP
**Prompt**: "Migrate pilot component:
- Choose low-risk component
- Complete migration
- Validate functionality
- Document learnings"

**Agent Output**:
- Migrated component
- Lessons learned
- Process refined

## Step 5: Phased Migration
**Prompt**: "Execute phased migration:
- Follow plan
- Test each phase
- Monitor for issues
- Adjust approach as needed"

**Agent Output**:
- Migration progress
- Issues encountered
- Adjustments made

## Step 6: Validation
**Prompt**: "Validate migration:
- All components migrated
- Tests passing
- Performance maintained
- No regressions"

**Agent Output**:
- Validation results
- Performance metrics
- No regressions confirmed

## Step 7: Completion
**Prompt**: "Complete migration:
- Remove old dependencies
- Update documentation
- Team training
- Celebrate! 🎉"

**Agent Output**:
- Migration complete
- Documentation updated
- Knowledge transferred
```

## Template Selection Guide

| Scenario | Template to Use |
|----------|----------------|
| New feature development | Feature Development Workflow |
| Bug fixing | Bug Fix Workflow |
| Code improvement | Refactoring Workflow |
| Code quality check | Code Review Workflow |
| Technology evaluation | Research Workflow |
| Technology migration | Migration Workflow |

## Customization Tips

### Adapt to Your Context
- Replace generic examples with your domain
- Adjust depth based on project complexity
- Add domain-specific steps
- Remove unnecessary steps

### Combine Templates
- Use Research + Feature Development for new features
- Use Refactoring + Code Review for improvements
- Use Bug Fix + Code Review for critical fixes

### Iterate and Improve
- Track which templates work best
- Adapt based on team feedback
- Add automation where possible
- Share learnings with team
