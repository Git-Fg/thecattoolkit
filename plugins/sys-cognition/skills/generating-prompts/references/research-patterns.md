# Research Patterns

Prompt patterns for gathering information for planning or implementation.

## Template

```markdown
# Research: {Topic}

## Objective
Research {topic} to inform {purpose}

## Context
{Background and requirements}

## Scope
Include:
- {What to investigate}
- {Specific questions}

Exclude:
- {Out of scope}

Sources:
- {Official documentation URLs}
- {Search queries}

## Output
Save to: .prompts/{num}-{topic}-research/{topic}-research.md

Structure findings:

### Summary
{2-3 paragraph overview}

### Key Findings
- {Finding 1} - {Source}
- {Finding 2} - {Source}

### Recommendations
1. {Action} - {Why}
2. {Action} - {Why}

### Metadata
- **Confidence:** {high/medium/low}
- **Dependencies:** {What's needed}
- **Open Questions:** {What remains}
- **Sources:** {List consulted}

### Summary Requirements
Create .prompts/{num}-{topic}-research/SUMMARY.md:

```markdown
# {Topic} Research Summary

**{Substantive one-liner}**

## Key Findings
- {Finding 1}
- {Finding 2}

## Recommendations
- {Action 1}
- {Action 2}

## Next Step
{Create plan / proceed to implementation}
```

## Quality Checklist

Before completing research:
- [ ] All scope questions answered
- [ ] Sources verified and current
- [ ] Findings actionable
- [ ] Metadata complete
- [ ] SUMMARY.md created

## Research Types

### Technology Research
**Example:** JWT authentication libraries

```markdown
## Objective
Research JWT libraries for Node.js to select implementation library

## Context
Building authentication system for API-first application

## Scope
Include:
- Available libraries (jose, jsonwebtoken, etc.)
- Security track record
- Performance characteristics
- TypeScript support
- Maintenance status

Sources:
- npm package pages
- GitHub security advisories
- Performance benchmarks
```

### Best Practices Research
**Example:** Authentication security

```markdown
## Objective
Research authentication security best practices for implementation

## Context
Implementing user authentication for web application

## Scope
Include:
- OWASP guidelines
- Token storage patterns
- Common vulnerabilities
- Secure configurations

Sources:
- OWASP Authentication Cheat Sheet
- Security best practices documentation
```

### API Research
**Example:** Stripe payments

```markdown
## Objective
Research Stripe API for payment integration planning

## Context
Adding payment processing to SaaS application

## Scope
Include:
- API structure
- Authentication methods
- Key endpoints
- Webhooks
- Testing environment

Sources:
- Stripe API documentation
- Webhook guides
- SDK references
```
