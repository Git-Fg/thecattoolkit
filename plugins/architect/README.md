# @cat-toolkit/architect (The System Designer)

**Purpose**: Comprehensive system architecture, design patterns, and technical decision documentation for complex software systems.

**License:** MIT

## Target User
The System Designer, Software Architect, or Technical Lead.

## Overview
The Architect plugin provides comprehensive system design capabilities including greenfield architecture design, brownfield analysis, architecture pattern selection, and Architecture Decision Record (ADR) documentation. It operates in isolated context (Sovereign Triangle pattern) to perform deep architectural analysis without polluting the main chat context.

## Quick Start

### Design a New System
```bash
# Comprehensive system design for new projects
/system-design "Design a real-time collaborative document editing service"

# The architect agent will:
# - Analyze functional and non-functional requirements
# - Select appropriate architecture patterns
# - Design technology stack and data architecture
# - Create architecture diagrams
# - Document decisions with ADRs
# - Provide implementation roadmap
```

### Analyze Existing Architecture
```bash
# Brownfield architecture analysis
/system-design "Analyze our microservices architecture for scalability issues"

# The architect agent will:
# - Perform comprehensive system mapping
# - Identify architectural patterns and anti-patterns
# - Analyze data flow and component relationships
# - Document technical debt and constraints
# - Recommend incremental improvements
# - Prioritize by impact and effort
```

### Direct Agent Invocation
```bash
# Delegate architecture tasks directly to the architect agent
# Analyze system design
"Analyze our system's scalability for 10x growth"

# Technology selection
"Design the architecture for our new API service"

# Architecture review
"Review our current authentication system architecture"
```

## Skills

### architecture
**Purpose**: System design frameworks and architecture analysis

**Resources:**
- System Design Workflow - Greenfield and brownfield processes
- Architecture Patterns - Monolith, microservices, serverless, event-driven
- Quality Checklist - Scalability, reliability, security, performance criteria
- ADR Template - Architecture Decision Record documentation

**Quality Criteria:**
Comprehensive evaluation across Scalability, Reliability, Security, Performance, and Operability. See `references/quality-checklist.md` in the architecture skill for the full checklist.

## Agents

### architect
**Purpose**: System design and architecture analysis

**Capabilities:**
- Comprehensive system design (greenfield)
- Architecture analysis (brownfield)
- Architecture pattern selection
- Technology stack recommendations
- Architecture Decision Records (ADRs)
- System mapping and documentation

**Tools:**
- Read, Write, Edit, Glob, Grep - Comprehensive analysis
- Bash - System operations
- TodoWrite - Design task tracking

**Skills Used:**
- architecture (system design workflows, quality criteria)

**Pattern**: Sovereign Triangle (specialized analyst)

## Commands

### /system-design
**Purpose**: System architecture and design analysis

**Pattern**: Sovereign Triangle (delegates to architect agent)

**Usage:**
```bash
/system-design "Design requirements or analysis request"
```

**Workflow:**
1. **Deep Discovery Phase** - Gather project context, requirements, constraints
2. **Task Classification** - Greenfield (new) vs Brownfield (existing)
3. **Delegation** - Comprehensive context package to architect agent
4. **Analysis** - Deep architectural work in isolated context
5. **Documentation** - Diagrams, ADRs, roadmap, risks

**Features:**
- Greenfield system design (new projects)
- Brownfield system analysis (existing systems)
- Architecture pattern selection
- Architecture Decision Records (ADRs)
- Technology stack recommendations
- Scalability and reliability analysis
- Risk assessment and mitigation

## Architecture Patterns & Analysis

The plugin supports a wide range of architectural patterns and analysis methodologies for both greenfield and brownfield projects.

### Patterns
Supports Monolith, Modular Monolith, Microservices, Serverless, and Event-Driven architectures. Detailed selection criteria and trade-off analysis are available in `references/system-design.md` within the `architecture` skill.

### Analysis Focus
Performs deep system mapping, dependency analysis, and technical debt assessment. Recommendations are provided for incremental improvements and strategic refactoring. See the `architecture` skill for the complete brownfield analysis protocol.

## Integration

### With Planner Plugin
- Architecture design precedes project planning
- Implementation roadmap feeds into PLAN.md
- Technical constraints inform project brief

### With Engineer Plugin
- Architecture provides blueprints for implementation
- Engineer executes architecture decisions
- ADRs guide refactoring and development

### With Think Plugin
- Thinking frameworks for architectural trade-off analysis
- Mental models for system design decisions
- Structured problem analysis for architecture

## Best Practices

1. **Design Before Planning** - Use architect before planner for new systems
2. **Document Decisions** - Always create ADRs for significant architectural choices
3. **Analyze Trade-offs** - Every pattern has pros and cons; document them explicitly
4. **Think Long-Term** - Design for 10x growth and team expansion
5. **Verify Quality** - Use quality checklist for all designs
6. **Plan for Failure** - Design resilience and recovery from the start

## Architecture Decision Records (ADRs)

ADRs document significant architectural decisions with:
- **Context**: The problem being addressed
- **Decision**: What was chosen and why
- **Consequences**: Positive, negative, and neutral outcomes
- **Alternatives**: What else was considered
- **Implementation**: Tasks, timeline, owner

## Example Workflows

### New System Design
```bash
# Design new system
/system-design "Design a real-time chat application"

# Architect agent will:
# - Analyze requirements (functional, non-functional, constraints)
# - Select architecture pattern (e.g., event-driven microservices)
# - Design technology stack (e.g., WebSockets, Redis, Node.js)
# - Create data architecture (user data, message storage, sync)
# - Document decisions with ADRs
# - Provide implementation roadmap
```

### Existing System Analysis
```bash
# Analyze existing system
/system-design "Analyze our monolith for microservices migration"

# Architect agent will:
# - Perform comprehensive system mapping
# - Identify bounded contexts and service boundaries
# - Analyze data dependencies and transactions
# - Document technical debt and constraints
# - Recommend incremental migration path
# - Prioritize by business value and technical risk
```

### Technology Selection
```bash
# Architecture decision
/system-design "Should we use SQL or NoSQL for our user analytics data?"

# Architect agent will:
# - Analyze data model and query patterns
# - Evaluate consistency requirements
# - Assess scalability needs
# - Compare technology options
# - Document decision with ADR
# - Provide implementation guidance
```

## Quality Assurance

### Architecture Review
- Quality checklist verification (scalability, reliability, security, performance)
- Anti-pattern detection (god objects, tight coupling, golden hammer)
- Trade-off analysis (every decision has consequences)
- ADR completeness (context, decision, consequences, alternatives)

### Design Principles
- **Separation of Concerns**: Each component has single responsibility
- **Loose Coupling**: Components depend on abstractions
- **High Cohesion**: Related functionalities co-located
- **Reusability**: Components reusable in different contexts
- **Open/Closed**: Extensible without modification

## Documentation References

### Core Architecture
- **Architectural Patterns** - See main toolkit documentation for Vector vs Triangle patterns
- **Development Standards** - See main toolkit development standards

### Skill Documentation
- **[skills/architecture/](skills/architecture/)** - System design frameworks and quality criteria

## License

MIT License - see plugin directory for full license text.
