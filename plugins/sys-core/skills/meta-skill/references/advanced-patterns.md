# Advanced Skill Patterns

## Multi-Domain Skills

### Organizing by Domain

When a skill spans multiple domains, organize by domain:

```markdown
skill-name/
├── SKILL.md (overview + navigation)
└── references/
    ├── domain1.md (revenue, billing)
    ├── domain2.md (pipeline, opportunities)
    ├── domain3.md (usage, features)
    └── domain4.md (campaigns, attribution)
```

### Domain Loading Strategy

```markdown
## Domain Navigation

User asks about domain1 → Load references/domain1.md only
User asks about domain2 → Load references/domain2.md only
User asks about multiple → Load all relevant domains
```

**Benefits:**
- Token efficiency (load only needed domains)
- Focused expertise per domain
- Easier maintenance
- Scalable organization

### Example: Marketing Automation Skill

```markdown
## Domain Structure

references/
├── campaigns.md
  - Campaign creation
  - Audience targeting
  - Budget allocation
  - Performance tracking

├── email-marketing.md
  - Template design
  - List management
  - Automation workflows
  - A/B testing

├── social-media.md
  - Post scheduling
  - Engagement tracking
  - Hashtag research
  - Influencer outreach

└── analytics.md
  - Conversion tracking
  - ROI calculation
  - Attribution modeling
  - Reporting
```

## Skill Chaining

### Delegation Chain Pattern

```markdown
# Skill A delegates to Skill B

## Chain Flow
1. User invokes Skill A
2. Skill A analyzes request
3. Skill A routes to Skill B
4. Skill B executes specialized task
5. Skill B returns result to Skill A
6. Skill A formats and presents result

## Example: Data Analysis Chain

Skill A: data-analyzer
  ↓ delegates to
Skill B: csv-processor
  ↓ delegates to
Skill C: statistical-analysis

## Delegation Format
# Context
User Request: {request}
Analysis: {analysis}

# Assignment
Use {target_skill} to {specific_task}

# Requirements
{requirements}

# Expected Output
{format}
```

### Chain Benefits

- **Specialization:** Each skill focuses on one thing
- **Reusability:** Skills can be chained in different ways
- **Maintainability:** Update one skill without affecting others
- **Testing:** Test individual skills in isolation

### Chain Example: PDF Processing

```markdown
# pdf-processor (Router)
├─→ text-extractor (specialized)
├─→ image-extractor (specialized)
└─→ metadata-reader (specialized)

# Delegation Example
"Extract text from pages 1-10"

pdf-processor analyzes:
- Keywords: ["extract", "text", "pages"]
- Route: text-extraction
- Confidence: high

Delegates to text-extractor with:
- File: document.pdf
- Pages: 1-10
- Format: plain text
```

## Hybrid Skills (Skills + Commands)

### Pattern: Knowledge + Invocation

```markdown
# Skill: Provides domain knowledge
skill: data-processor/
├── SKILL.md (knowledge + workflows)
├── references/ (detailed techniques)
└── examples/ (use cases)

# Command: Provides easy invocation
command: /process-data
├── Shortcut to skill
├── Zero-retention
└─→ Routes to skill with user input
```

### Use Cases

**Frequent Operations:**
```markdown
Command: /deploy
Skill: deployment-router
Workflow: orchestrates deployment process
```

**Complex Workflows:**
```markdown
Command: /analyze-codebase
Skill: code-analyzer
Workflow: multi-step analysis with reporting
```

**User Convenience:**
```markdown
Command: /validate-skill
Skill: meta-skill
Workflow: validates skill structure and content
```

### Implementation

```markdown
## Command Structure

---
description: "Quick data processing shortcut"
argument-hint: Optional file path or description
allowed-tools: [Skill(data-processor)]
disable-model-invocation: true
---

# Process Data

Invoke data-processor skill with user request

## Usage
/process-data csv file.csv
/process-data "validate my data structure"
```

## Progressive Enhancement Pattern

### Level 1: Basic Skill

```markdown
# Basic Skill (MVP)
skill-basic/
└── SKILL.md (minimal workflow)
```

### Level 2: Enhanced Skill

```markdown
# Enhanced Skill
skill-enhanced/
├── SKILL.md (core + examples)
├── references/ (detailed docs)
└── examples/ (concrete use cases)
```

### Level 3: Advanced Skill

```markdown
# Advanced Skill
skill-advanced/
├── SKILL.md (navigation + overview)
├── references/ (domain expertise)
├── examples/ (comprehensive)
├── workflows/ (complex processes)
└── assets/ (templates + tools)
```

### Level 4: Enterprise Skill

```markdown
# Enterprise Skill
skill-enterprise/
├── SKILL.md (lightweight router)
├── references/ (specialized domains)
├── workflows/ (advanced patterns)
├── assets/ (tools + templates)
├── scripts/ (automation)
└── tests/ (validation)
```

**Benefits:**
- Start simple, grow complexity
- User feedback guides enhancement
- Maintain backward compatibility
- Token-efficient progression

## Context-Aware Skills

### Pattern: Context Injection

```markdown
# Skill with Context Awareness

## Context Sources
- Previous user requests
- Loaded files
- Active workspace
- Session history

## Context Usage
When skill activates:
1. Analyze context
2. Adapt response
3. Provide relevant examples
4. Reference related information

## Example
User: "Create a CSV validator"
Context: Previous request for data cleaning

Skill Response:
"Based on your data cleaning needs, here's a CSV validator that integrates with your workflow..."
```

### Implementation

```markdown
## Context Analysis

### Available Context
- Files in workspace
- Recent commands
- Active skills
- User preferences

### Adaptation Strategy
- Reference relevant context
- Provide related examples
- Suggest complementary workflows
- Maintain conversation flow
```

## Token Optimization Patterns

### Pattern 1: Lazy Loading

```markdown
# Load on Demand

SKILL.md (always loaded):
- Overview
- Quick Start
- Navigation

references/ (loaded when needed):
- Detailed technical docs
- Advanced examples
- API references
```

### Pattern 2: Condensed Core

```markdown
# Essential Information Only

SKILL.md (core):
- What the skill does
- How to use it (minimal)
- Key examples (2-3)
- Success criteria

references/ (expansion):
- Detailed explanations
- Edge cases
- Advanced usage
- Troubleshooting
```

### Pattern 3: Smart Summaries

```markdown
# Summary + Reference Pattern

## In SKILL.md (brief):
"PDF processing supports text extraction, image extraction, and metadata reading. See references/pdf-processing.md for detailed workflows."

## In references/pdf-processing.md (detailed):
- Text extraction: step-by-step
- Image extraction: techniques
- Metadata reading: methods
- Troubleshooting: common issues
```

## Performance Patterns

### Pattern 1: Caching

```markdown
# Cache Expensive Operations

## Cache Strategy
- File analysis results
- User preference patterns
- Common workflow configurations
- Template generations

## Cache Invalidation
- File modifications
- User preference changes
- Time-based expiration
- Manual refresh
```

### Pattern 2: Parallel Processing

```markdown
# Parallel Skill Execution

## Independent Tasks
Task A: analyze file structure
Task B: extract metadata
Task C: generate summary

## Parallel Execution
Run in parallel → Combine results
```

### Pattern 3: Incremental Loading

```markdown
# Load Incremental Information

## Phase 1: Core (immediate)
- SKILL.md overview
- Quick Start guide
- Basic examples

## Phase 2: Details (on-demand)
- references/ domain content
- Advanced examples
- Technical documentation

## Phase 3: Advanced (when needed)
- workflows/ complex processes
- assets/ tools and templates
- scripts/ automation
```

## Error Handling Patterns

### Pattern 1: Graceful Degradation

```markdown
# Degrade Functionality Gracefully

## Full Capability
All tools available → Complete workflow

## Reduced Capability
Some tools restricted → Core functionality

## Minimal Capability
No tools available → Documentation only
```

### Pattern 2: Recovery Workflows

```markdown
# Error Recovery

## Common Errors
1. Tool not available → Use alternative
2. Permission denied → Request permission
3. File not found → Guide to locate
4. Invalid input → Validate and correct

## Recovery Actions
- Suggest alternatives
- Provide guidance
- Offer examples
- Enable manual override
```

### Pattern 3: User Guidance

```markdown
# Clear Error Messages

## Bad Error
"Error: Something went wrong"

## Good Error
"I couldn't process the CSV file. This might be because:
1. The file is encrypted (try decrypting first)
2. The file format isn't standard CSV (try converting to UTF-8)
3. The file is corrupted (try opening in a text editor)

Would you like me to guide you through any of these steps?"
```

## Integration Patterns

### Pattern 1: Cross-Skill Collaboration

```markdown
# Skill A + Skill B

## Collaboration Example
data-processor (skill A)
  + validation suite (skill B)
  = robust data processing

## Integration
- Share context
- Exchange results
- Coordinate workflows
- Avoid duplication
```

### Pattern 2: Command-Skill Orchestration

```markdown
# Orchestration Pattern

Command: /analyze-project
  ├─→ code-analyzer (skill)
  ├─→ dependency-checker (skill)
  └─→ security-scanner (skill)

## Workflow
1. Command orchestrates
2. Skills execute specialized tasks
3. Command synthesizes results
4. User receives comprehensive report
```

### Pattern 3: Hook-Based Activation

```markdown
# Hook-Triggered Skills

## SessionStart Hook
- Validate environment
- Setup context
- Load preferences

## PreToolUse Hook
- Validate operations
- Check permissions
- Provide warnings

## PostToolUse Hook
- Log results
- Update context
- Trigger follow-ups
```

## Testing Patterns

### Pattern 1: Example-Driven Testing

```markdown
# Test via Examples

## Test Cases
1. Example request → Expected output
2. Edge case → Error handling
3. Invalid input → Graceful failure
4. Complex workflow → Success criteria

## Validation
- Run examples automatically
- Verify outputs match expectations
- Track success rates
```

### Pattern 2: User Journey Testing

```markdown
# Complete User Journeys

## Journey 1: New User
1. Discover skill
2. Try simple example
3. Progress to advanced
4. Become expert

## Journey 2: Expert User
1. Find specific capability
2. Use advanced features
3. Customize workflow
4. Integrate with other tools
```

### Pattern 3: Regression Testing

```markdown
# Prevent Regressions

## Test Suite
- Core functionality tests
- Example validation tests
- Integration tests
- Performance tests

## Continuous Validation
- Run tests on every change
- Track performance metrics
- Monitor user satisfaction
```

## Maintenance Patterns

### Pattern 1: Version Management

```markdown
# Skill Versions

## Version 1: MVP
Basic functionality
Limited features
Core workflows

## Version 2: Enhancement
Add features
Improve examples
Better documentation

## Version 3: Optimization
Performance improvements
Token efficiency
User experience
```

### Pattern 2: Deprecation Strategy

```markdown
# Deprecating Skills

## Phase 1: Mark Deprecated
- Add deprecation notice
- Suggest alternatives
- Maintain backwards compatibility

## Phase 2: Limited Support
- Bug fixes only
- No new features
- Migration guidance

## Phase 3: Removal
- Archive old skill
- Redirect to alternatives
- Update documentation
```

### Pattern 3: Evolution Tracking

```markdown
# Track Skill Evolution

## Changes Log
- Feature additions
- Bug fixes
- Performance improvements
- User feedback integration

## Impact Assessment
- Breaking changes
- Migration requirements
- Compatibility matrix
```

## Best Practices Summary

### DO

✅ **Start simple, enhance gradually**
✅ **Use progressive disclosure**
✅ **Provide concrete examples**
✅ **Handle errors gracefully**
✅ **Optimize for token efficiency**
✅ **Test with real users**
✅ **Track metrics and improve**

### DON'T

❌ **Over-engineer from start**
❌ **Skip error handling**
❌ **Ignore token limits**
❌ **Create brittle workflows**
❌ **Skip testing**
❌ **Avoid user feedback**
❌ **Forget maintenance**

## Conclusion

Advanced patterns help you:
- Scale complexity gracefully
- Maintain token efficiency
- Improve user experience
- Enable collaboration
- Ensure reliability

Choose patterns based on:
- Skill complexity
- User needs
- Performance requirements
- Maintenance capacity
