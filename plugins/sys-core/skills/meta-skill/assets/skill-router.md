---
name: {ROUTER_NAME}
# Standard Pattern (default - for public routers):
description: "Routes {TASK_TYPE} requests to specialized skills. Use when {ROUTING_CONTEXT}."
# OR Enhanced Pattern (for toolkit infrastructure routers):
# description: "Routes {TASK_TYPE} requests to specialized skills. PROACTIVELY Use when {ROUTING_CONTEXT}."
allowed-tools: [{ALLOWED_TOOLS}]
---

# {HUMAN_READABLE_ROUTER_NAME}

## Overview

This router analyzes {INPUT_TYPE} requests and intelligently routes them to the most appropriate specialized {SKILL_TYPE} for efficient processing.

## Activation Triggers

Router activates when users ask to:
- {Trigger phrase 1}
- {Trigger phrase 2}
- {Trigger phrase 3}

## Routing Logic

### Route 1: {ROUTE_NAME_1}
**Triggers:** {keyword1}, {keyword2}, {keyword3}
**Routes to:** {SKILL_NAME_1}
**User phrases:** "{Example phrase 1}", "{Example phrase 2}"

**When to use:** {Use case description}

**Example:**
```markdown
User: "{Example query}"
Action: Detect "{keyword}" → Route to {SKILL_NAME_1}
```

### Route 2: {ROUTE_NAME_2}
**Triggers:** {keyword1}, {keyword2}, {keyword3}
**Routes to:** {SKILL_NAME_2}
**Pattern:** "{Example user request}"

**When to use:** {Use case description}

**Example:**
```
User: "{Example query}"
Router: Detects "{keyword}" → Routes to {SKILL_NAME_2}
```

### Route 3: {ROUTE_NAME_3}
**Triggers:** {keyword1}, {keyword2}, {keyword3}
**Routes to:** {SKILL_NAME_3}
**Pattern:** "{Example user request}"

**When to use:** {Use case description}

**Example:**
```
User: "{Example query}"
Router: Detects "{keyword}" → Routes to {SKILL_NAME_3}
```

## Default Route

**Routes to:** {DEFAULT_SKILL}
**Pattern:** "{Default behavior}"

When no specific route matches, the router defaults to {description of default handling}.

## Implementation

### Routing Algorithm
```python
def route_request(user_request):
    """Route request to appropriate skill"""

    request_lower = user_request.lower()

    # Route 1: {ROUTE_NAME_1}
    if any(term in request_lower for term in [{keywords}]):
        return {{
            'skill': '{SKILL_NAME_1}',
            'pattern': '{routing pattern}',
            'confidence': 'high'
        }}

    # Route 2: {ROUTE_NAME_2}
    if any(term in request_lower for term in [{keywords}]):
        return {{
            'skill': '{SKILL_NAME_2}',
            'pattern': '{routing pattern}',
            'confidence': 'high'
        }}

    # Route 3: {ROUTE_NAME_3}
    if any(term in request_lower for term in [{keywords}]):
        return {{
            'skill': '{SKILL_NAME_3}',
            'pattern': '{routing pattern}',
            'confidence': 'medium'
        }}

    # Default route
    return {{
        'skill': '{DEFAULT_SKILL}',
        'pattern': '{default pattern}',
        'confidence': 'low'
    }}
```

### Delegation Pattern
```markdown
When routing to a specialized skill:

1. Analyze request to determine route
2. Format delegation prompt:
   # Context
   {User request details}

   # Assignment
   Route determined: {skill-name}
   Pattern: {specific instructions}

   # Requirements
   {Specific requirements for this route}

3. Delegate to target skill
4. Format response to user
```

## Routing Criteria

### Decision Factors
Router considers:
1. **{Factor 1}** - {How it influences routing}
2. **{Factor 2}** - {How it influences routing}
3. **{Factor 3}** - {How it influences routing}

### Confidence Levels
- **High Confidence:** Clear keywords match specific route
- **Medium Confidence:** Multiple factors suggest route
- **Low Confidence:** Default fallback

## Example Scenarios

### Scenario 1: {Example}
**User Request:** "{Example query}"

**Router Analysis:**
- Keywords detected: {keywords}
- Route match: {route name}
- Confidence: {level}

**Action:** Routes to {skill name}
**Expected Output:** {description}

### Scenario 2: {Example}
**User Request:** "{Example query}"

**Router Analysis:**
- Keywords detected: {keywords}
- Route match: {route name}
- Confidence: {level}

**Action:** Routes to {skill name}
**Expected Output:** {description}

## Routing Statistics

| Route | Success Rate | Avg Response Time | User Satisfaction |
|-------|--------------|-------------------|-------------------|
| {Route 1} | {X}% | {Y}s | {Rating}/5 |
| {Route 2} | {X}% | {Y}s | {Rating}/5 |
| {Route 3} | {X}% | {Y}s | {Rating}/5 |

## Extensibility

### Adding New Routes

**Step 1:** Define route criteria
```python
# Add new route
if any(term in request_lower for term in ['new', 'route', 'keywords']):
    return {{
        'skill': 'new-skill-name',
        'pattern': 'Route to new specialized skill',
        'confidence': 'high'
    }}
```

**Step 2:** Update documentation
- Add route section
- Update examples
- Test with sample requests

**Step 3:** Validate routing
- Test edge cases
- Verify confidence levels
- Check delegation format

## Troubleshooting

### Route Not Matching
**Problem:** Request doesn't match any route
**Solution:** Check keywords, consider adding route or using default

### Incorrect Routing
**Problem:** Wrong route selected
**Solution:** Review keyword lists, adjust confidence levels

### Delegation Failure
**Problem:** Target skill not responding
**Solution:** Verify skill exists, check delegation format

## Success Criteria

### Routing Accuracy
- [ ] Routes match user intent >90% of time
- [ ] Default route handles unknown requests
- [ ] Confidence levels appropriate

### Performance
- [ ] Routing decision <100ms
- [ ] Delegation format consistent
- [ ] Error handling graceful

### User Experience
- [ ] Clear routing feedback
- [ ] Appropriate route selection
- [ ] Helpful error messages

## Testing

### Test Suite
```bash
# Test route detection
uv run scripts/test-router.py

# Expected output:
# ✓ Route 1: 10/10 correct
# ✓ Route 2: 9/10 correct
# ✓ Default: 5/5 correct
```

### Manual Testing
```markdown
# Test each route with 3-5 real user phrases

Route 1 Test Cases:
- "{phrase 1}" → Expected: {SKILL_1} ✓
- "{phrase 2}" → Expected: {SKILL_1} ✓
- "{phrase 3}" → Expected: {SKILL_1} ✓

Route 2 Test Cases:
- "{phrase 1}" → Expected: {SKILL_2} ✓
- "{phrase 2}" → Expected: {SKILL_2} ✓

Default Route Test Cases:
- "{ambiguous phrase}" → Expected: {DEFAULT_SKILL} ✓
```

### Test Script Template
```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Router test suite."""

def test_routes():
    test_cases = [
        ("{phrase 1}", "{SKILL_1}"),
        ("{phrase 2}", "{SKILL_2}"),
        ("{ambiguous}", "{DEFAULT}"),
    ]

    for query, expected in test_cases:
        result = route_request(query)
        assert result['skill'] == expected, f"Failed: {query}"

    print("✓ All tests passed")

if __name__ == "__main__":
    test_routes()
```

## Anti-Patterns

### ❌ Don't
- Hardcode specific user requests
- Create too many routes (max 5-7)
- Skip default route
- Ignore confidence levels
- Implement logic in router (delegate instead)

### ✅ Do
- Use keyword-based routing
- Provide clear examples
- Include default fallback
- Test edge cases
- Keep routing logic simple

## References

- `../../references/routing-patterns.md` - Advanced routing techniques
- `../../references/delegation-standards.md` - Proper delegation format
- `../../examples/router-examples.md` - Real-world routing examples
