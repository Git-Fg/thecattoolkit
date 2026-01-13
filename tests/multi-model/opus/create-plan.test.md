# Test: create-plan - Opus Tier

## Test Case 1: Large Monolith Discovery
**Input**: `/sys-builder:create-plan "Add CI/CD pipeline to 10-year-old Java monolith"`
**Expected Output**: Complex plan with migration strategy
**Success Criteria**:
- [ ] Discovery scans 1000+ files
- [ ] Identifies legacy patterns (Ant, JSP, EJB)
- [ ] Maps dependencies and module structure
- [ ] BRIEF.md documents technical debt
- [ ] ROADMAP.md: Assessment, Modernization, CI/CD, Deployment
- [ ] Migration path from Ant to Maven/Gradle
- [ ] Testing strategy (legacy test coverage)
- [ ] Rollback plan for critical system

## Test Case 2: Multi-Tenant SaaS Platform
**Input**: `/sys-builder:create-plan "Convert single-tenant app to multi-tenant SaaS"`
**Expected Output**: Architectural transformation plan
**Success Criteria**:
- [ ] Discovery analyzes data model
- [ ] Tenant isolation strategy defined
- [ ] BRIEF.md defines tenant model (shared DB, separate schema, or separate DB)
- [ ] ROADMAP includes: Data isolation, Authentication, Billing, Multi-tenancy features
- [ ] Security boundaries documented
- [ ] Migration strategy for existing users
- [ ] Performance considerations (shared vs isolated resources)
- [ ] Compliance requirements (GDPR, SOC2)

## Test Case 3: Distributed System Integration
**Input**: `/sys-builder:create-plan "Integrate 5 microservices with event-driven architecture"`
**Expected Output**: Event-driven integration plan
**Success Criteria**:
- [ ] Discovery maps service boundaries
- [ ] Event schema registry planned
- [ ] BRIEF.md defines event catalog
- [ ] ROADMAP: Event Store, Message Broker, Service Integration, Dead Letter Handling
- [ ] Event sourcing patterns
- [ ] Saga pattern for distributed transactions
- [ ] Observability (tracing, logging, metrics)
- [ ] Eventual consistency strategy

## Test Case 4: AI/ML Feature Integration
**Input**: `/sys-builder:create-plan "Add ML recommendation engine to e-commerce platform"`
**Expected Output**: ML pipeline integration plan
**Success Criteria**:
- [ ] Discovery identifies data sources
- [ ] BRIEF.md defines ML requirements (supervised/unsupervised, features)
- [ ] ROADMAP: Data Pipeline, Model Training, Inference Service, Feature Store, A/B Testing
- [ ] Model versioning strategy
- [ ] Data privacy (PII handling, anonymization)
- [ ] Real-time vs batch inference
- [ ] Model monitoring and drift detection
- [ ] Integration with existing product catalog

## Test Case 5: Legacy System Modernization
**Input**: `/sys-builder:create-plan "Modernize COBOL banking system to cloud-native architecture"`
**Expected Output**: Full modernization roadmap
**Success Criteria**:
- [ ] Discovery scans COBOL programs and JCL
- [ ] Business logic mapping
- [ ] BRIEF.md documents compliance requirements (PCI-DSS, SOX)
- [ ] ROADMAP: Assessment, Microfiche Digitization, COBOL to Java/Go, Cloud Migration, Security Hardening
- [ ] Zero-downtime migration strategy
- [ ] Parallel run period
- [ ] Regulatory approval process
- [ ] Disaster recovery planning
- [ ] Legacy system sunset timeline
