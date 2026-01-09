# Example: Code Review Style

**Use for:** Code reviews, pull request feedback, refactoring suggestions, quality assessments

## Characteristics

- **Objective** - Focus on code, not the coder
- **Constructive** - Offer solutions, not just criticism
- **Specific** - Point to exact locations and examples
- **Educational** - Explain the reasoning
- **Prioritized** - Critical issues first

## Structure

```markdown
# Code Review: [PR/Commit Title]

## Overall Assessment
[Summary of changes and general impression]

## ✅ Strengths
- [Positive aspect 1]
- [Positive aspect 2]

## 🔴 Critical Issues (Must Fix)
1. **[File:Line]** - [Issue]
   **Why:** [Impact/consequence]
   **Fix:** [Suggested solution]

2. **[File:Line]** - [Issue]

## 🟡 Important (Should Fix)
1. **[File:Function]** - [Issue]
   **Why:** [Maintainability/readability concern]
   **Suggestion:** [Improvement idea]

2. **[File:Function]** - [Issue]

## 💡 Suggestions (Could Improve)
1. **[File:Function]** - [Enhancement idea]
   **Benefit:** [Why this would be better]

2. **[File:Function]** - [Enhancement idea]

## 📚 Learning Opportunities
[Teaching moments - explain concepts]

## ✅ Tests
[Assessment of test coverage and quality]

## Security Considerations
[Any security concerns]

## Performance Notes
[Performance impacts observed or potential]

## Total Review Time
[X minutes/hours]
```

## Feedback Language

### Critical Issues (Must Fix)
**Language:**
- "This will cause [specific problem]"
- "Security risk: [vulnerability]"
- "This breaks [specific requirement]"

**Example:**
```javascript
// Critical: No input validation
function getUser(id) {
  return db.query(id); // SQL injection risk
}

// Fix:
function getUser(id) {
  if (typeof id !== 'string' || !id.match(/^[a-zA-Z0-9-_]+$/)) {
    throw new Error('Invalid user ID format');
  }
  return db.query('SELECT * FROM users WHERE id = $1', [id]);
}
```

### Important Issues (Should Fix)
**Language:**
- "Consider improving..."
- "This could be clearer if..."
- "Alternative approach..."

**Example:**
```javascript
// Should improve: Magic numbers
const timeout = 5000;

// Better:
const DEFAULT_TIMEOUT_MS = 5000;
const timeout = DEFAULT_TIMEOUT_MS;
```

### Suggestions (Could Improve)
**Language:**
- "You might consider..."
- "One option would be..."
- "Alternative pattern..."

**Example:**
```javascript
// Suggestion: Could use modern syntax
const users = data.filter(u => u.active).map(u => ({...u, status: 'active'}));

// Alternative:
const activeUsers = data.filter(u => u.active);
const formattedUsers = activeUsers.map(formatUser);
```

## Review Checklist

### Functionality
- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Input validation is present

### Code Quality
- [ ] Readable and well-named
- [ ] No duplicate code
- [ ] Appropriate abstractions
- [ ] Follows project conventions

### Security
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Authentication/authorization
- [ ] Sensitive data handling

### Performance
- [ ] No obvious inefficiencies
- [ ] Appropriate data structures
- [ ] Database queries are optimized
- [ ] No N+1 problems

### Testing
- [ ] Tests cover main functionality
- [ ] Edge cases are tested
- [ ] Tests are maintainable
- [ ] Appropriate test types (unit/integration)

## Comment Templates

### Requesting Changes
```markdown
**Issue:** [Brief description]

**Impact:** [What could go wrong]

**Suggestion:** [Your proposed fix]

**Alternative:** [If there are multiple ways to fix]
```

### Asking Questions
```markdown
**Question:** [Your question]

**Context:** [Why you're asking]

**Assumption:** [What you're assuming about the code]
```

### Giving Praise
```markdown
**Nice work:** [What they did well]

**Reason:** [Why this is good]

**Impact:** [How this helps]
```

### Sharing Knowledge
```markdown
**FYI:** [Information they're probably not aware of]

**Example:** [Concrete example of the concept]

**Reference:** [Link to documentation/standard]
```

## Tone Guidelines

**Do:**
- Focus on the code, not the person
- Explain the "why" behind suggestions
- Offer constructive alternatives
- Acknowledge good work
- Be specific and actionable

**Don't:**
- Use judgmental language
- Make personal attacks
- Suggest changes without explanation
- nitpick without reason
- Be overly critical

## Example Review Comment

```markdown
**File:** `src/auth.js:47`

**Issue:** User password is logged in plain text

```javascript
console.log('User login:', { email, password }); // 🔴 Critical
```

**Impact:** Passwords appear in application logs and log aggregation systems

**Fix:** Remove password from log statement

```javascript
console.log('User login attempt:', { email, timestamp: new Date().toISOString() });
// If debugging is needed, use a hash:
// console.log('User login:', { email, passwordHash: hash(password) });
```

**Why:** Passwords should never be logged, even for debugging
```

## Non-blocking Feedback

For suggestions that aren't critical:

```markdown
**💡 Nit:** Consider using `Array.prototype.groupBy()` (ES2024)

```javascript
// Current:
const grouped = {};
users.forEach(u => {
  grouped[u.department] = grouped[u.department] || [];
  grouped[u.department].push(u);
});

// Alternative:
const grouped = Object.groupBy(users, u => u.department);
```

**Note:** This is just a suggestion - current code is perfectly fine. The new method is slightly more concise but requires ES2024 support.
```
