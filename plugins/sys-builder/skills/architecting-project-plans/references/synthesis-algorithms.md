# Synthesis Algorithms

## Overview

Synthesis Algorithms transform user requirements and discovery findings into actionable project plans.

## Algorithm 1: Greenfield Planning

**When to Use:**
- New project from scratch
- No existing codebase
- Clean slate approach

### Step-by-Step Process

#### Step 1: Requirement Analysis
```markdown
Input: User requirements
Process:
1. Extract functional needs (what it does)
2. Identify non-functional needs (how it performs)
3. Note constraints (timeline, tech stack, etc.)

Output: Requirement categories
```

**Example:**
```
User Input: "Build a task management app"
↓
Functional: Create, read, update, delete tasks
Non-Functional: Responsive UI, fast search, offline support
Constraints: React, 2 weeks, small team
```

#### Step 2: Technology Stack Selection
```markdown
Decision Matrix:

Frontend:
- React: Large ecosystem, popular
- Vue: Gentle learning curve
- Angular: Enterprise-ready
- Svelte: Performance-focused

Backend:
- Express: Minimalist, flexible
- Django: Batteries included
- FastAPI: Modern, fast, automatic docs
- Flask: Simple, lightweight

Database:
- PostgreSQL: Relational, ACID compliant
- MongoDB: Document-based, flexible
- SQLite: Embedded, zero-config
```

**Selection Criteria:**
1. Team expertise
2. Project requirements
3. Timeline constraints
4. Scalability needs
5. Maintenance burden

#### Step 3: Architecture Design
```markdown
Component Breakdown:

1. User Interface
   - Components
   - State management
   - Routing

2. Business Logic
   - Domain models
   - Use cases
   - Validation

3. Data Layer
   - Database schema
   - Repository pattern
   - Caching

4. Infrastructure
   - Authentication
   - Authorization
   - API gateway
```

#### Step 4: Phase Generation
```markdown
Foundation → Core → Enhancement → Polish

Phase 1: Foundation
- Setup project structure
- Install dependencies
- Configure build tools
- Create basic components

Phase 2: Core Features
- Implement CRUD operations
- Build main UI screens
- Add business logic

Phase 3: Enhancement
- Add advanced features
- Performance optimization
- Integration testing

Phase 4: Polish
- UI/UX improvements
- Documentation
- Final testing
```

#### Step 5: Task Atomicity
```markdown
Task Size Guidelines:

Too Large (> 3 hours):
❌ "Implement user authentication"
✅ "Create login form component"
✅ "Add JWT token validation"
✅ "Implement logout functionality"

Too Small (< 15 minutes):
❌ "Create button"
❌ "Add CSS class"
✅ "Create user dashboard with navigation"
✅ "Implement search functionality"

Just Right (30-90 minutes):
✅ "Add user registration form with validation"
✅ "Implement task filtering and sorting"
✅ "Create responsive layout for mobile"
```

### Greenfield Template

```markdown
# Greenfield Plan: {project-name}

## Requirements
**Functional:**
- {F1}
- {F2}
- {F3}

**Non-Functional:**
- {NF1}
- {NF2}

**Constraints:**
- {C1}
- {C2}

## Architecture
**Frontend:** {tech stack}
**Backend:** {tech stack}
**Database:** {tech stack}
**Deployment:** {platform}

## Phases

### Phase 1: Foundation
**Tasks:**
1. Setup project structure
2. Install dependencies
3. Configure build tools
4. Create basic components/pages

### Phase 2: Core Features
**Tasks:**
1. Implement {feature 1}
2. Implement {feature 2}
3. Implement {feature 3}

### Phase 3: Enhancement
**Tasks:**
1. Add {advanced feature}
2. Optimize {performance area}
3. Implement {integration}

### Phase 4: Polish
**Tasks:**
1. UI/UX improvements
2. Documentation
3. Final testing and deployment
```

## Algorithm 2: Brownfield Integration

**When to Use:**
- Adding to existing codebase
- Feature additions
- System modifications

### Step-by-Step Process

#### Step 1: Pattern Analysis
```markdown
Process:
1. Study existing patterns
2. Identify conventions
3. Note integration points
4. Document anti-patterns

Example:
- Naming: camelCase for JS, snake_case for Python
- Architecture: MVC with controllers in /controllers
- State: Redux for global, useState for local
- API: REST with /api/v1 prefix
```

#### Step 2: Gap Analysis
```markdown
Mapping:

Existing Codebase:
- Has: User model, database table
- Does: CRUD operations, validation

User Requirements:
- Wants: Social login, password reset
- Needs: OAuth integration, email service

Gap Identification:
- Gap 1: OAuth middleware
- Gap 2: Email service integration
- Gap 3: Password reset UI
```

#### Step 3: Integration Strategy
```markdown
Integration Patterns:

1. **Adapter Pattern**
   - Wrap new functionality in familiar interface
   - Example: New API wrapped in existing controller

2. **Decorator Pattern**
   - Add behavior without modifying existing code
   - Example: Add logging to existing functions

3. **Facade Pattern**
   - Simplify complex subsystem
   - Example: Create simple interface for complex library

4. **Dependency Injection**
   - Provide dependencies from outside
   - Example: Inject service into component
```

#### Step 4: Migration Planning
```markdown
Migration Strategy:

1. Backward Compatibility
   - Maintain existing API
   - Deprecate gradually
   - Provide migration path

2. Data Migration
   - Schema changes
   - Data transformation
   - Rollback strategy

3. Feature Flags
   - Gradual rollout
   - A/B testing
   - Quick rollback
```

### Brownfield Template

```markdown
# Brownfield Plan: {project-name}

## Existing System
**Architecture:** {MVC/Monolith/Microservices}
**Patterns:** {Naming, structure, conventions}
**Integration Points:** {Where to hook in}

## Gap Analysis
**Has:**
- {Existing capability 1}
- {Existing capability 2}

**Needs:**
- {Required capability 1}
- {Required capability 2}

**Gap:**
- {Gap 1}
- {Gap 2}

## Integration Strategy
**Approach:** {Adapter/Decorator/Facade/etc.}
**Pattern:** {How to integrate}
**Compatibility:** {Backward/Forward compatible}

## Migration Plan
**Phase 1: Foundation**
- {Setup OAuth provider}
- {Add email service}

**Phase 2: Core**
- {Implement social login}
- {Add password reset}

**Phase 3: Enhancement**
- {Add advanced features}
- {Optimize performance}

**Phase 4: Cleanup**
- {Remove deprecated code}
- {Update documentation}
```

## Algorithm 3: Feature Addition

**When to Use:**
- Adding specific feature to existing system
- Clear, bounded scope
- Well-understood requirements

### Step-by-Step Process

#### Step 1: Feature Scoping
```markdown
Scope Definition:

In Scope:
- {What the feature includes}
- {User interactions}
- {Data changes}

Out of Scope:
- {What the feature doesn't include}
- {Future enhancements}

Assumptions:
- {A1}
- {A2}
```

#### Step 2: Pattern Matching
```markdown
Find Similar Features:
1. Identify existing feature with similar functionality
2. Study implementation pattern
3. Adapt pattern for new feature
4. Document any deviations

Example:
- Adding "comments" to existing "posts"
- Follow same CRUD pattern
- Use same component structure
- Adapt for different data model
```

#### Step 3: Task Breakdown
```markdown
Task Hierarchy:

Epic: {Feature Name}
  ├── Task 1: Backend API
  │   ├── Subtask 1.1: Database schema
  │   ├── Subtask 1.2: API endpoints
  │   └── Subtask 1.3: Validation
  ├── Task 2: Frontend Components
  │   ├── Subtask 2.1: Form component
  │   ├── Subtask 2.2: List component
  │   └── Subtask 2.3: Detail view
  └── Task 3: Integration
      ├── Subtask 3.1: Connect API to UI
      ├── Subtask 3.2: Add tests
      └── Subtask 3.3: Documentation
```

### Feature Addition Template

```markdown
# Feature Plan: {feature-name}

## Scope
**In Scope:**
- {S1}
- {S2}

**Out of Scope:**
- {OS1}
- {OS2}

**Assumptions:**
- {A1}
- {A2}

## Existing Patterns
**Similar Feature:** {reference-feature}
**Pattern:** {What pattern to follow}
**Deviations:** {How it differs}

## Tasks

### Backend
- [ ] Database schema changes
- [ ] API endpoints
- [ ] Validation logic
- [ ] Tests

### Frontend
- [ ] Form components
- [ ] List/detail views
- [ ] State management
- [ ] Integration tests

### Integration
- [ ] API-UI connection
- [ ] End-to-end tests
- [ ] Documentation
```

## Algorithm 4: Refactoring

**When to Use:**
- Improving existing code
- Reducing technical debt
- Performance optimization
- Code cleanup

### Step-by-Step Process

#### Step 1: Problem Identification
```markdown
Problem Statement:
- What is broken?
- Why is it a problem?
- What is the impact?

Metrics:
- Performance: {slow queries, memory leaks, etc.}
- Maintainability: {complexity, coupling, etc.}
- Reliability: {bugs, edge cases, etc.}
```

#### Step 2: Current State Analysis
```markdown
Analysis:

Code Metrics:
- Lines of code
- Cyclomatic complexity
- Coupling/cohesion
- Test coverage

Issues:
- Code smells
- Anti-patterns
- Technical debt items
```

#### Step 3: Target Design
```markdown
Design Goals:
1. {Goal 1 - measurable}
2. {Goal 2 - measurable}
3. {Goal 3 - measurable}

Approach:
- {Refactoring technique}
- {Pattern to apply}
- {Tools to use}

Constraints:
- Must maintain API compatibility
- Cannot break existing tests
- Zero downtime deployment
```

#### Step 4: Migration Strategy
```markdown
Strangler Fig Pattern:

1. Identify boundaries
2. Create new implementation
3. Route traffic gradually
4. Remove old implementation

Phases:
Phase A: Create new alongside old
Phase B: Route some traffic to new
Phase C: Route all traffic to new
Phase D: Remove old implementation
```

### Refactoring Template

```markdown
# Refactoring Plan: {component-name}

## Problem
**Current Issue:** {What is broken}
**Impact:** {User/business impact}
**Metrics:** {Current performance/maintainability}

## Goals
1. {Goal 1 - measurable}
2. {Goal 2 - measurable}
3. {Goal 3 - measurable}

## Current State
**Code Metrics:**
- LOC: {X}
- Complexity: {Y}
- Test Coverage: {Z}%

**Issues:**
- {Issue 1}
- {Issue 2}

## Target Design
**Architecture:** {New structure}
**Patterns:** {Design patterns}
**Performance:** {Expected improvement}

## Migration Plan

### Phase 1: Foundation
- {Setup new structure}
- {Create interfaces}

### Phase 2: Migration
- {Migrate functionality}
- {Update tests}

### Phase 3: Cleanup
- {Remove old code}
- {Optimize performance}
```

## Synthesis Checklist

### Before Creating Plan
- [ ] Requirements analyzed
- [ ] Context understood
- [ ] Constraints identified
- [ ] Success criteria defined

### During Synthesis
- [ ] Appropriate algorithm selected
- [ ] Tasks are atomic
- [ ] Dependencies explicit
- [ ] Phases structured logically

### After Synthesis
- [ ] Plan validated against requirements
- [ ] Timeline realistic
- [ ] Resources adequate
- [ ] Risks mitigated

## Common Pitfalls

### ❌ Avoid
- Creating tasks > 3 hours
- Missing dependencies
- Unclear success criteria
- Ignoring existing patterns
- Over-engineering solutions
- No rollback strategy

### ✅ Follow
- Atomic task size (30-90 min)
- Explicit dependencies
- Measurable success criteria
- Follow existing patterns
- Simplest solution first
- Plan for rollback
