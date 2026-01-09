# Protocol: Architectural Deep Discovery

This protocol defines the standard for gathering context before performing system design or architecture analysis. It ensures agents have a complete understanding of the technical, business, and operational landscape.

## Phase 1: Project Context Mapping

Gather essential project information to establish the baseline:

### 1. Technology Stack
- **Languages & Frameworks**: Identify core technologies in use.
- **Data Stores**: Identify databases, caches, and message brokers.
- **Infrastructure**: Identify cloud providers, container orchestration, and external services.
- **Integrations**: Map external API dependencies and third-party services.

### 2. Physical Structure
- **Architecture Docs**: Locate `ADR` folders, `docs/architecture`, or similar.
- **System Boundaries**: Identify modules, services, and clear separation points.
- **Diagrams**: Search for C4, UML, or high-level architecture diagrams (SVG/Mermaid/PNG).
- **Manifests**: Locate Kubernetes YAMLs, Terraform files, or deployment scripts.

### 3. Business Context
- **Domain**: Understand the core business problem.
- **Requirements**: Locate product specs, user stories, or RFCs.
- **Scale**: Identify current traffic (RPS), data volume (TB), and user count.
- **Growth**: Identify 10x growth targets and timelines.

## Phase 2: Requirements Analysis

Analyze the gathered context to define success criteria:

### 1. Functional Requirements
- List the MUST-HAVE features for the system.
- Map the "Happy Path" data flow through the components.
- Identify failure-critical integration points.

### 2. Non-Functional Requirements (The Quality Gates)
- **Scalability**: Define horizontal vs vertical scaling strategy for 10x loads.
- **Reliability**: Define SLA/SLO requirements and fault-tolerance expectations.
- **Security**: Define authentication, authorization, and encryption standards.
- **Performance**: Define latency budgets for critical paths.
- **Maintainability**: Identify technical debt that limits architectural evolution.

## Phase 3: Environment Verification

Verify the tools and access needed for implementation:
- Ensure diagramming tools (Mermaid, D2, or SVG) are usable.
- Verify access to existing architecture repositories.
- Check for existing templates or standard ADR formats in the project.

## Success Criteria Checklist
- [ ] Task type classified (Greenfield vs Brownfield).
- [ ] Tech stack mapped.
- [ ] Project structure understood.
- [ ] Requirements (Func/Non-Func) documented.
- [ ] Constraints identified.
