---
description: |
  Execute comprehensive security audit using OWASP patterns and vulnerability scanning protocols.
  <example>
  Context: User needs security review
  user: "Audit our code for security vulnerabilities"
  assistant: "I'll delegate to the security agent for comprehensive vulnerability assessment."
  </example>
  <example>
  Context: OWASP compliance check
  user: "Run a security audit on our API"
  assistant: "I'll use the security-audit command to check for OWASP Top 10 issues."
  </example>
  <example>
  Context: Focused security review
  user: "Audit our authentication system"
  assistant: "I'll delegate for focused security analysis of the auth system."
  </example>
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
argument-hint: [system description, codebase path, or security concern]
---

## Objective
Execute security audit workflow for: $ARGUMENTS

## Deep Discovery Phase

Before delegating to the agent, gather comprehensive context to ensure thorough security analysis.

### Step 1: Analyze Security Request

Determine the nature of the security audit:

**Analyze $ARGUMENTS to classify:**
- **Full Audit**: Comprehensive security assessment of entire codebase
- **Focused Review**: Specific area (authentication, data handling, APIs)
- **Vulnerability Scan**: Check for specific vulnerability types (OWASP Top 10)
- **Compliance Review**: Verify compliance with security standards
- **Penetration Test**: Simulate attack scenarios

### Step 2: Map Project Context

Gather essential project information:

**Technology Stack Identification:**
- Identify language and framework
- Identify database systems and ORMs
- Identify authentication/authorization systems
- Identify third-party dependencies

**System Architecture Mapping:**
- Locate entry points (API endpoints, web routes, handlers)
- Identify data flows and processing pipelines
- Check for external integrations and APIs
- Locate sensitive data storage (passwords, tokens, PII)

**Security Surface Analysis:**
- Identify user input endpoints (forms, APIs, file uploads)
- Locate data output points (HTML rendering, API responses, logs)
- Check authentication and authorization boundaries
- Identify admin interfaces and privileged operations

### Step 3: Threat Modeling

Identify potential attack vectors:

**OWASP Top 10 Categories:**
- **Injection**: SQL, NoSQL, OS command, LDAP
- **Broken Authentication**: Session management, credential handling
- **Sensitive Data Exposure**: Encryption, data in transit/rest
- **XML External Entities (XXE)**: XML parsing vulnerabilities
- **Broken Access Control**: Horizontal/vertical privilege escalation
- **Security Misconfiguration**: Default credentials, unnecessary features
- **Cross-Site Scripting (XSS)**: Reflected, stored, DOM-based
- **Insecure Deserialization**: Object injection
- **Using Components with Known Vulnerabilities**: Dependency scanning
- **Insufficient Logging & Monitoring**: Attack detection, audit trails

### Step 4: Environment Verification

Check security tools and configuration:
- Verify dependency vulnerability scanners available
- Check for static analysis tools (SAST)
- Identify security headers and CORS configuration
- Review authentication and authorization implementation

### Step 5: Delegation Package

Compile all gathered context into a comprehensive assignment for the code-implementer agent.

## Delegation Phase

<assignment>
Execute the security audit workflow from the engineering skill to assess: $ARGUMENTS

**Context Provided:**
- Audit Type: [full audit / focused review / vulnerability scan / compliance / pentest]
- Technology Stack: [language, framework, databases, auth systems, dependencies]
- System Architecture: [entry points, data flows, integrations, sensitive data storage]
- Security Surface: [input endpoints, output points, auth boundaries, admin interfaces]
- Threat Model: [OWASP categories, potential attack vectors]

**Follow the systematic security audit protocol:**
1. **Reconnaissance**: Find sensitive surface areas (passwords, api_keys, eval, etc.)
2. **Data Flow Analysis**: Trace user input from entry to sink (validation and escaping)
3. **Vulnerability Assessment**: Check for OWASP Top 10 patterns
4. **Report Creation**: Document findings with severity and fix recommendations

**Work autonomously using Uninterrupted Flow:**
- Use grep and search tools to scan for vulnerabilities
- Trace data flows through the codebase
- Log all findings with file:line references
- Create HANDOFF.md only for critical access blockers
- DO NOT use AskUserQuestion during execution

**Security Analysis Focus:**
- Read the security checklist from the engineering skill before starting
- Assume "Attacker Mindset" - how could this be abused?
- Check all input validation and sanitization
- Verify authentication and authorization at every boundary
- Ensure sensitive data is properly encrypted
- Check for hardcoded secrets and credentials
- Verify proper error handling (no information leakage)
- Assess logging and monitoring for attack detection

**Output Format:**
Create a structured security report with:
- **[CRITICAL]**: Immediate exploitation risk (fix now)
- **[HIGH]**: Significant vulnerability (fix soon)
- **[MEDIUM]**: Moderate risk (schedule fix)
- **[LOW]**: Minor issue (improve when possible)
- **[INFO]**: Best practice recommendation

Each finding must include:
- File:line reference
- Vulnerability type (OWASP category)
- Exploit scenario (how it could be abused)
- Severity assessment (CVSS estimation)
- Concrete fix recommendation
</assignment>

<context>
You are executing in isolated context to perform comprehensive security analysis. The engineering skill provides OWASP-based security protocols and vulnerability patterns.
All relevant project context has been gathered for you.
</context>

Execute via code-implementer agent.

## Success Criteria

- [ ] Audit type properly classified
- [ ] Project context fully mapped (stack, architecture, security surface)
- [ ] Threat model completed (OWASP categories, attack vectors)
- [ ] Environment verified (security tools, configuration)
- [ ] Agent receives comprehensive context package
- [ ] All critical inputs traced from entry to sink
- [ ] Report assumes "Attacker Mindset"
- [ ] Findings categorized by severity
- [ ] Each finding includes exploit scenario and fix recommendation
