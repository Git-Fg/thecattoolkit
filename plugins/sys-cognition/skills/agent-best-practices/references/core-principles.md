# Core Principles: Agent Development

## The Three Pillars of Effective Agent Systems

### 1. Agent Harness Components

Every effective agent system requires three coordinated elements working in harmony:

#### Instructions (System Prompts & Rules)
- **Purpose**: Define agent behavior, constraints, and operational guidelines
- **Best Practice**: Keep instructions clear, specific, and actionable
- **Examples**:
  - Coding standards and style guides
  - Security policies and constraints
  - Review criteria and quality gates
  - Communication protocols

#### Tools (Capabilities & Integrations)
- **Purpose**: Enable agents to interact with systems and data
- **Categories**:
  - File operations (read, write, edit, search)
  - Code execution (terminal, build tools, tests)
  - External APIs (databases, services, cloud platforms)
  - Specialized tools (linters, formatters, validators)

#### User Messages (Intent & Context)
- **Purpose**: Direct agent actions and provide context
- **Characteristics**:
  - Clear, specific requests
  - Contextual information
  - Success criteria
  - Constraints and requirements

### 2. Planning-First Approach

**Research Finding**: Studies of professional developers show that those who plan before coding achieve significantly better results.

#### Why Planning Matters
- Forces clear thinking about the problem
- Provides concrete goals for agents to work toward
- Reduces iteration cycles and rework
- Improves code quality and maintainability
- Facilitates better communication with team members

#### Planning Benefits
- **Cognitive Load**: Offloads working memory to external documentation
- **Traceability**: Creates audit trail of decisions
- **Collaboration**: Enables review and feedback before implementation
- **Quality**: Reduces bugs through upfront design
- **Efficiency**: Minimizes wasted effort on incorrect approaches

### 3. Progressive Complexity Management

Effective agent systems handle complexity through layers:

#### Layer 1: Simple Prompts
For straightforward tasks with clear requirements:
```
"Add authentication middleware to all API endpoints"
```

#### Layer 2: Contextual Prompts
With specific files and patterns:
```
"Add authentication middleware to API endpoints in routes/api/*.js,
following the pattern in middleware/auth-example.js"
```

#### Layer 3: Structured Plans
For complex, multi-step tasks:
```
"Refactor the user management system:
1. Analyze current implementation
2. Identify pain points
3. Design new architecture
4. Create migration plan
5. Implement changes
6. Add tests
7. Update documentation"
```

## Universal Agentic Runtime Principles

### Token Efficiency
- Minimize context window usage through progressive disclosure
- Use short, focused instructions
- Reference documents rather than including full content
- Leverage search tools for context discovery

### Intent-Driven Design
- Design for discoverability through intent
- Allow agents to find relevant capabilities
- Avoid rigid command structures
- Support natural language interaction

### Isolation & Context Management
- Use forks for high-volume operations
- Start new conversations for different logical tasks
- Maintain clean context by removing completed subtasks
- Leverage agent memory for session continuity

### Verification & Quality
- Implement multiple verification layers
- Use tests as executable specifications
- Leverage type systems for correctness
- Automated linting and formatting
- Human review at critical checkpoints

## The Iteration Loop

Effective agent development follows a continuous improvement cycle:

```
Plan → Implement → Verify → Review → Refine
  ↑                                    ↓
  └─────────── Iterate ←────────────────┘
```

### Planning Phase
- Define objectives and success criteria
- Identify constraints and requirements
- Break down into manageable steps
- Document assumptions and decisions

### Implementation Phase
- Execute plan systematically
- Follow established patterns
- Validate at each milestone
- Document any deviations

### Verification Phase
- Run automated tests
- Perform code review
- Check against requirements
- Validate edge cases

### Review Phase
- Assess outcome against plan
- Identify lessons learned
- Note areas for improvement
- Update patterns and guidelines

### Refinement Phase
- Apply learnings to future work
- Update rules and skills
- Improve workflows
- Enhance documentation
