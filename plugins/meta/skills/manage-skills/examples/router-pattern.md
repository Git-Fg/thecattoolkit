# Example: Code Analysis Router (Router Pattern)

A router skill that delegates to specialized analysis skills based on the request type.

```markdown
---
name: code-analysis-router
description: Route code analysis requests to appropriate specialized skills based on analysis type
---
```

# Structure

```markdown
# Code Analysis Router

## Purpose
Route code analysis requests to the most appropriate specialized skill for the task.

## Activation Triggers
- "Analyze code for..."
- "Review this code"
- "Find issues in..."
- "Security scan..."

## Routing Logic

### Security Analysis
**Triggers:** "security", "vulnerabilities", "XSS", "SQL injection"
**Routes to:** Security analysis skill
**Pattern:** "Analyze code for security issues"

### Performance Analysis
**Triggers:** "performance", "speed", "optimization", "bottleneck"
**Routes to:** Performance analysis skill
**Pattern:** "Analyze code for performance issues"

### Style Analysis
**Triggers:** "style", "formatting", "lint", "convention"
**Routes to:** Code style skill
**Pattern:** "Review code style and formatting"

### General Analysis
**Triggers:** "general", "overall", "review"
**Routes to:** General code review skill
**Pattern:** "Perform general code review"

## Implementation

```python
def route_analysis_request(request):
    """Route to appropriate analysis skill"""

    request_lower = request.lower()

    # Security routing
    if any(term in request_lower for term in ['security', 'vulnerab', 'xss', 'injection']):
        return {
            'skill': 'security-analysis',
            'pattern': 'Analyze code for security issues'
        }

    # Performance routing
    if any(term in request_lower for term in ['performance', 'speed', 'optimize', 'bottleneck']):
        return {
            'skill': 'performance-analysis',
            'pattern': 'Analyze code for performance issues'
        }

    # Style routing
    if any(term in request_lower for term in ['style', 'format', 'lint', 'convention']):
        return {
            'skill': 'code-style',
            'pattern': 'Review code style and formatting'
        }

    # Default routing
    return {
        'skill': 'general-review',
        'pattern': 'Perform general code review'
    }
```

## Usage Example

**Input:** "Analyze this code for security vulnerabilities"
**Routing:** Detects "security" → Routes to security-analysis skill
**Output:** "Delegating to security-analysis skill for vulnerability assessment"

**Input:** "Review this function for performance issues"
**Routing:** Detects "performance" → Routes to performance-analysis skill
**Output:** "Delegating to performance-analysis skill for performance assessment"

## Anti-Patterns to Avoid

❌ **Over-complex routing logic** - Keep it simple and clear
❌ **Hardcoding all possible requests** - Use keyword matching
❌ **No default route** - Always have a fallback
❌ **Bypassing specialized skills** - Don't try to do everything in router

## Success Criteria

- [ ] Routes correctly to specialized skills
- [ ] Handles unknown requests gracefully
- [ ] Clear delegation messages
- [ ] No infinite routing loops
- [ ] Easy to add new routes
```
