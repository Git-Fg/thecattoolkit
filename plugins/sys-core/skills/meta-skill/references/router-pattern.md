# Router Pattern Implementation

## When to Use Router Pattern

Router pattern is ideal when:
- Multiple specialized workflows exist
- Request analysis can determine best route
- Delegation to specialized skills is preferred
- Complex decision logic required

**Examples:**
- `toolkit-registry` → Routes to plugin components
- `data-processor` → Routes to format-specific processors
- `code-analyzer` → Routes to language-specific analyzers

## Router Architecture

### Core Components

```markdown
# Router Skill Structure

skill-router/
├── SKILL.md              # Main router logic + examples
├── workflows/
│   └── routing-algorithm.md   # Detailed routing logic
└── references/
    ├── route-definitions.md   # All routes defined
    ├── delegation-patterns.md  # How to delegate
    └── troubleshooting.md     # Common issues
```

### Router Workflow

```markdown
## Router Workflow

1. **Request Analysis**
   - Extract keywords and intent
   - Analyze user context
   - Determine complexity level

2. **Route Selection**
   - Match against route patterns
   - Calculate confidence score
   - Select best route

3. **Delegation**
   - Format delegation prompt
   - Invoke target skill
   - Handle errors

4. **Response Synthesis**
   - Format skill output
   - Add router context
   - Return to user
```

## Route Definition Pattern

### Route Specification

```yaml
routes:
  - name: route-name
    triggers:
      - keyword1
      - keyword2
      - phrase1
    target: target-skill
    confidence: high|medium|low
    pattern: "User request pattern"
    example: "Concrete user query"
```

### Route Examples

**Route 1: Data Format Detection**
```yaml
triggers: ["csv", "comma-separated", ".csv file"]
target: csv-processor
confidence: high
pattern: "process.*csv|analyze.*csv"
```

**Route 2: Image Processing**
```yaml
triggers: ["image", "photo", ".jpg", ".png"]
target: image-processor
confidence: high
pattern: "resize.*image|convert.*photo"
```

**Route 3: PDF Operations**
```yaml
triggers: ["pdf", ".pdf", "document"]
target: pdf-processor
confidence: high
pattern: "extract.*pdf|merge.*pdf"
```

**Default Route**
```yaml
target: general-processor
confidence: low
pattern: ".*"
description: "Fallback for unmatched requests"
```

## Implementation Examples

### Example 1: Simple Keyword Router

```markdown
## Routing Logic

### Request Analysis
When user says: "Process my CSV file"

**Detected Keywords:** ["csv", "process"]
**Route Match:** Data Format Router
**Confidence:** High

**Action:** Route to csv-processor skill
```

### Example 2: Pattern Matching Router

```markdown
## Routing Logic

### Request Analysis
When user says: "I need to validate the structure of my data"

**Pattern Match:** Validation Router
**Keywords:** ["validate", "structure"]
**Route Match:** data-validator
**Confidence:** High

**Action:** Route to data-validator skill
```

### Example 3: Confidence-Based Router

```markdown
## Routing Logic

### Request Analysis
When user says: "Help me with this file"

**Keywords:** ["file"]
**Multiple Routes Possible:**
- csv-processor (medium confidence)
- pdf-processor (medium confidence)

**Decision:** Ask for clarification OR route to general-processor

**Confidence Scores:**
- csv-processor: 0.6
- pdf-processor: 0.6
- general-processor: 0.3

**Action:** Route to general-processor (default)
```

## Delegation Patterns

### Pattern 1: Direct Delegation

```markdown
When routing to specialized skill:

# Context
User Request: {user_request}
Detected Keywords: {keywords}
Route Match: {route_name}

# Assignment
Process this request using {target_skill}

# Requirements
- Use the {target_skill} workflow
- Follow its success criteria
- Return formatted results

# Expected Output
{expected_format}
```

### Pattern 2: Enhanced Delegation

```markdown
# Enhanced Delegation with Context

## User Request
{user_request}

## Analysis
- Intent: {intent}
- Keywords: {keywords}
- Confidence: {confidence}

## Routing Decision
Route: {route_name}
Target: {target_skill}
Reason: {routing_reason}

## Task Requirements
{requirements}

## Success Criteria
{success_criteria}
```

### Pattern 3: Chained Delegation

```markdown
# Chained Routing

## Step 1: Initial Analysis
Request: {user_request}
Route: {initial_route}
Target: {initial_target}

## Step 2: Execution
Invoke {target_skill} with enhanced context

## Step 3: Response Processing
- Format output
- Add router metadata
- Return to user
```

## Advanced Routing Techniques

### 1. Multi-Stage Routing

```markdown
## Stage 1: Domain Detection
- Domain: data-processing
- Keywords: ["csv", "json", "excel"]

## Stage 2: Operation Detection
- Operation: validation
- Keywords: ["validate", "check", "verify"]

## Stage 3: Final Route
- Target: data-validator
- Confidence: high
```

### 2. Contextual Routing

```markdown
## Context Analysis
- User Role: {role}
- Previous Requests: {history}
- Current Session: {session_context}

## Routing Decision
Based on context + keywords + confidence
```

### 3. Learning Router

```markdown
## Route Analytics
Track:
- Success rate per route
- User satisfaction per route
- Common misroutes

## Improvement
Adjust confidence scores based on feedback
```

## Troubleshooting Routers

### Problem: No Route Matches

**Symptoms:**
- All routes have low confidence
- Default route always triggers

**Solutions:**
1. Add more trigger keywords
2. Lower confidence threshold
3. Add pattern matching
4. Improve default route

### Problem: Wrong Route Selected

**Symptoms:**
- Users complain about irrelevant results
- Low success rate for specific routes

**Solutions:**
1. Review trigger keywords
2. Adjust confidence scores
3. Add more specific patterns
4. Test with real examples

### Problem: Delegation Fails

**Symptoms:**
- Target skill not responding
- Error messages

**Solutions:**
1. Verify skill name matches
2. Check delegation format
3. Add error handling
4. Test with simple requests

## Testing Router Patterns

### Test Suite

```bash
# Test 1: Keyword Detection
echo "Process my CSV file" | grep -E "(csv|process)"
# Expected: Match

# Test 2: Route Selection
python router_test.py "validate my data"
# Expected: data-validator route

# Test 3: Delegation
curl -X POST /delegate -d "route=csv-processor"
# Expected: Success
```

### Validation Checklist

**Route Definition:**
- [ ] All routes have clear triggers
- [ ] Confidence scores appropriate
- [ ] Default route defined
- [ ] Examples provided

**Delegation:**
- [ ] Format consistent
- [ ] Context preserved
- [ ] Error handling present
- [ ] Response processing works

**Testing:**
- [ ] All routes tested
- [ ] Edge cases covered
- [ ] Success rates tracked
- [ ] User feedback integrated

## Best Practices

### DO

✅ **Keep routes simple and focused**
- One clear purpose per route
- Distinct trigger keywords
- Measurable success criteria

✅ **Use confidence scores appropriately**
- High: Clear keyword match
- Medium: Multiple factors suggest route
- Low: Default fallback

✅ **Provide clear examples**
- Real user phrases
- Expected routing behavior
- Sample outputs

✅ **Handle errors gracefully**
- Fallback routes
- Error messages
- Recovery options

### DON'T

❌ **Create too many routes (max 5-7)**
- Hard to maintain
- Confusing selection
- Poor user experience

❌ **Skip default route**
- Unmatched requests fail
- Poor user experience
- No recovery path

❌ **Hardcode specific requests**
- Inflexible routing
- Maintenance burden
- Poor scalability

❌ **Ignore confidence levels**
- Random routing
- Poor accuracy
- User frustration

## Integration with Commands

Router skills work well with commands:

```markdown
Command: /process-data
Skill: data-router
Pattern: Router → Specialized Skills

Usage:
/process-data csv file.csv → Routes to csv-processor
/process-data pdf doc.pdf → Routes to pdf-processor
```

## Performance Optimization

### Token Efficiency

- Keep SKILL.md under 500 lines
- Move detailed logic to workflows/
- Use references/ for route definitions
- Optimize delegation prompts

### Response Time

- Cache route decisions
- Optimize pattern matching
- Parallel skill invocation when possible
- Minimize delegation overhead

## Success Metrics

Track router performance:

**Routing Accuracy:** % of requests routed correctly
**User Satisfaction:** Rating per route
**Delegation Success:** % of delegations successful
**Response Time:** Average time per routed request

## Advanced Topics

### Machine Learning Routing

Future enhancement:
- Learn from user feedback
- Improve route selection
- Adapt to usage patterns

### Multi-Modal Routing

Support for:
- Text + image requests
- File type detection
- Context-aware routing

### Federated Routing

Multiple routers:
- Domain-specific routers
- Hierarchical routing
- Cross-domain delegation
