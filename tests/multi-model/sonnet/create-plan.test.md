# Test: create-plan - Sonnet Tier

## Test Case 1: Discovery in Python Project
**Input**: `/sys-builder:create-plan "Add API endpoints to Django application"`
**Expected Output**: Django-specific plan with discovery findings
**Success Criteria**:
- [ ] Discovery scans project structure
- [ ] Identifies Django version and dependencies
- [ ] BRIEF.md includes Django context
- [ ] ROADMAP.md includes Django patterns (models, views, urls)
- [ ] API-specific tasks (serializers, viewsets, routing)
- [ ] Integration with existing codebase

## Test Case 2: React with TypeScript
**Input**: `/sys-builder:create-plan "Build a TypeScript React component library"`
**Expected Output**: TypeScript + React plan with component architecture
**Success Criteria**:
- [ ] Discovery identifies TypeScript configuration
- [ ] BRIEF.md mentions TypeScript + React
- [ ] ROADMAP.md has Foundation (TS setup), Core (components), Testing, Documentation
- [ ] Phase plans include tsconfig, type definitions, component templates
- [ ] Build tools configured (Vite/Webpack)
- [ ] Testing strategy (Jest + Testing Library)

## Test Case 3: Multi-Service Architecture
**Input**: `/sys-builder:create-plan "Create a microservices e-commerce platform"`
**Expected Output**: Multi-service plan with service communication
**Success Criteria**:
- [ ] Discovery scans for service patterns
- [ ] BRIEF.md defines service boundaries
- [ ] ROADMAP.md has: Foundation, Auth Service, Product Service, Order Service, API Gateway
- [ ] Each service has independent plan
- [ ] Inter-service communication defined
- [ ] Database per service pattern
- [ ] API gateway configuration

## Test Case 4: Database Migration Plan
**Input**: `/sys-builder:create-plan "Migrate from MongoDB to PostgreSQL"`
**Expected Output**: Migration strategy with rollback plan
**Success Criteria**:
- [ ] Discovery analyzes current MongoDB schema
- [ ] BRIEF.md documents migration scope
- [ ] ROADMAP.md includes: Assessment, Schema Design, Migration Script, Data Transfer, Validation, Rollback
- [ ] Migration scripts planned
- [ ] Data integrity verification
- [ ] Downtime minimization strategy
- [ ] Rollback procedures

## Test Case 5: Feature Addition with Tests
**Input**: `/sys-builder:create-plan "Add real-time chat to existing Vue.js app"`
**Expected Output**: Feature plan with testing integration
**Success Criteria**:
- [ ] Discovery scans Vue.js project
- [ ] Identifies existing state management (Vuex/Pinia)
- [ ] BRIEF.md mentions Vue.js and real-time requirements
- [ ] ROADMAP.md includes: WebSocket setup, Chat component, State integration, E2E tests
- [ ] Integration with existing patterns
- [ ] Testing strategy (unit + E2E)
- [ ] Deployment considerations
