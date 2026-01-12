# Metadata Guidelines

Standard metadata structure for research and plan outputs.

## Structure

```xml
### Metadata
- **Confidence:** {high/medium/low} - {Why}
- **Dependencies:** {What's needed}
- **Open Questions:** {What remains uncertain}
- **Assumptions:** {What was assumed}
```

## Confidence Levels

- **High** - Official docs, verified patterns, clear consensus
- **Medium** - Mixed sources, some gaps, reasonable approach
- **Low** - Sparse docs, conflicting info, best guess

## Examples

### High Confidence

```markdown
### Metadata
- **Confidence:** High - OWASP guidelines + multiple authoritative sources
- **Dependencies:** Team familiarity with JWT concepts
- **Open Questions:** Specific rate limits under production load
- **Assumptions:** REST API architecture (not GraphQL)
```

### Medium Confidence

```markdown
### Metadata
- **Confidence:** Medium - Library docs good, limited real-world benchmarks
- **Dependencies:** npm packages available, Node.js environment
- **Open Questions:** Performance with >100k concurrent users
- **Assumptions:** Single region deployment
```

### Low Confidence

```markdown
### Metadata
- **Confidence:** Low - Sparse documentation, conflicting community reports
- **Dependencies:** Access to beta feature flags
- **Open Questions:** Long-term maintenance status
- **Assumptions:** Team can learn new patterns
```

## Usage

**Research outputs:** Always include confidence, dependencies, open questions

**Plan outputs:** Include confidence, dependencies, assumptions

**Do outputs:** Typically omit metadata (focus on verification)
