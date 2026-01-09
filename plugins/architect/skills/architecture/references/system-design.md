# Protocol: Architecture Design & Analysis

## Auto-Detection
This protocol automatically detects the context and routes accordingly:

- **Greenfield (New System)**: Skip to System Design Process
- **Brownfield (Existing System)**: Follow Existing System Analysis process below

## System Design Process (New Systems)

### Step 1: Requirements Gathering
Analyze the provided requirements to identify:
- **Functional Requirements**: Core features and user stories
- **Non-Functional Requirements**: Performance, scalability, security, availability
- **Constraints**: Budget, timeline, technology preferences, regulatory requirements

### Step 2: Architecture Patterns
Based on requirements, select appropriate patterns:

**Monolith**
- Simple deployment, shared database
- Best for: Small teams, rapid prototyping, simple domains

**Modular Monolith**
- Separated modules within single deployable unit
- Best for: Medium complexity, team scaling preparation

**Microservices**
- Independently deployable services
- Best for: Large scale, multiple teams, complex domains

**Serverless**
- Function-as-a-Service architecture
- Best for: Event-driven, variable load, pay-per-use

**Event-Driven**
- Async communication via events
- Best for: High throughput, loose coupling, real-time processing

### Step 3: Technology Stack Selection
Recommend technologies based on:
- Team expertise and learning curve
- Ecosystem maturity and community support
- Performance and scalability requirements
- Operational complexity

### Step 4: Data Architecture
Define:
- **Database Type**: SQL vs NoSQL vs Polyglot
- **Data Flow**: Sync vs Async patterns
- **Data Consistency**: ACID vs BASE principles
- **Data Storage**: Caching, partitioning, replication

### Step 5: Architecture Diagram
Create comprehensive architecture diagram showing:
- **Components**: Services, databases, caches, external APIs
- **Interactions**: Synchronous and asynchronous communication
- **Data Flow**: Request-response and event flows
- **Infrastructure**: Load balancers, API gateways, containers

### Step 6: Architecture Decision Records (ADRs)
Document key decisions with:
- **Context**: The problem being addressed
- **Decision**: What was chosen and why
- **Consequences**: Positive, negative, and neutral outcomes
- **Alternatives**: What else was considered

## Existing System Analysis

For brownfield projects, perform comprehensive system analysis:
1. Understand current system architecture
2. Identify architectural patterns in use
3. Map component relationships
4. Analyze data flow patterns
5. Document technical debt and constraints

Then provide recommendations for:
- **Incremental Improvements**: Low-risk enhancements
- **Strategic Refactoring**: Medium to long-term architectural evolution
- **Migration Strategies**: Path to target architecture

## Architecture Quality Criteria

### Scalability
- Can the system handle 10x growth?
- What are the bottlenecks?
- How does it scale horizontally/vertically?

### Reliability
- What are the failure modes?
- How does the system recover?
- What's the disaster recovery plan?

### Security
- Authentication and authorization model
- Data encryption strategy
- Network security and API protection

### Performance
- Response time requirements
- Throughput expectations
- Latency-sensitive paths

### Operability
- Monitoring and observability
- Deployment strategy
- Maintenance and support model

## Success Criteria
- [ ] Architecture pattern selected with rationale
- [ ] Technology stack justified
- [ ] Architecture diagram created
- [ ] ADRs documented for key decisions
- [ ] Quality criteria evaluated
- [ ] Risks identified with mitigation strategies
