# Skill Creation Workflow

## The Complete Creation Process

This workflow guides you through creating a skill from concept to publication.

### Phase 1: Analysis

**Step 1: Define Purpose**
- What problem does this skill solve?
- Who are the target users?
- What triggers will users say?

**Step 2: Assess Complexity**
- Simple utility (standard template)
- Complex domain (progressive template)
- Multiple workflows (router template)
- Internal tool (minimal template)

**Step 3: Research Context**
- Existing skills in the ecosystem
- User phrases and triggers
- Required tool integrations

### Phase 2: Design

**Step 4: Choose Template**
```markdown
Decision Matrix:
- Single purpose, linear workflow → Standard
- Complex domain, rich docs → Progressive
- Multiple specialized workflows → Router
- Internal/passive tool → Minimal
```

**Step 5: Plan Structure**
```
skill-name/
├── SKILL.md (核心内容 < 500 lines)
├── references/ (详细文档 > 100 lines each)
├── examples/ (具体用例)
├── workflows/ (复杂流程)
├── scripts/ (验证工具)
└── assets/ (模板和资源)
```

**Step 6: Define Metadata**
```yaml
---
name: skill-name
description: "(MODAL) USE when [condition with triggers]"
allowed-tools: [Read, Write, Edit, Bash]
user-invocable: true
---
```

### Phase 3: Implementation

**Step 7: Create SKILL.md**
Follow template structure:
- Overview (what and why)
- Quick Start (immediate value)
- Core Knowledge (domain expertise)
- Workflow (step-by-step process)
- Usage Examples (concrete code)
- Success Criteria (measurable outcomes)

**Step 8: Add References**
For each reference file:
- 100-500 lines of detailed content
- Specific domain knowledge
- Advanced techniques
- API documentation

**Step 9: Create Examples**
- 2-3 concrete use cases
- Real user phrases
- Expected outputs
- Common variations

### Phase 4: Validation

**Step 10: Name Validation**
```bash
# Check format
echo "skill-name" | grep -E '^[a-z][a-z0-9]*(-[a-z0-9]+)*$'

# Check length (3-50 chars)
[ ${#skill_name} -ge 3 ] && [ ${#skill_name} -le 50 ]
```

**Step 11: Description Validation**
- Starts with "(MODAL) USE when"
- 10-1024 characters
- Includes trigger phrases
- Describes actual capability

**Step 12: Content Validation**
```bash
# Check SKILL.md length
wc -l SKILL.md  # Should be < 400

# Check references exist
ls references/  # Should have relevant files

# Check examples exist
ls examples/    # Should have 2-3 examples
```

**Step 13: Standards Compliance**
- [ ] Follows Universal Agentic Runtime
- [ ] Uses Cat Toolkit conventions
- [ ] Implements progressive disclosure
- [ ] Passes all validation checks

### Phase 5: Optimization

**Step 14: Token Budget Check**
```bash
# Calculate total description characters
grep -r "description:" . | awk '{ sum += length($0) } END { print sum }'
# Should be < 15,000
```

**Step 15: Discovery Testing**
Test natural language triggers:
- "Create a skill for X"
- "How do I do Y?"
- "I need to Z"

**Step 16: Usability Review**
- Can users understand the workflow?
- Are examples concrete and actionable?
- Is documentation scannable?

### Phase 6: Publication

**Step 17: Final Checklist**
- [ ] All validation checks pass
- [ ] Token budget under limit
- [ ] Progressive disclosure implemented
- [ ] Examples tested
- [ ] Documentation reviewed

**Step 18: Publish**
- Commit to repository
- Run comprehensive validation
- Test with real users
- Gather feedback

## Quality Gates

### Gate 1: Structure
- SKILL.md under 500 lines
- Progressive disclosure implemented
- Proper file organization

### Gate 2: Content
- Concrete examples
- Clear workflow
- Success criteria defined

### Gate 3: Standards
- Naming conventions followed
- Description pattern correct
- Tool restrictions appropriate

### Gate 4: Usability
- Discovery works via natural language
- Examples are actionable
- Documentation is scannable

### Gate 5: Efficiency
- Token budget respected
- References properly used
- No redundant content

## Common Workflows

### Quick Skill (30 minutes)
```
Analysis (5 min) → Standard Template → SKILL.md only → Validate → Done
```
Use for: Simple utilities, straightforward workflows

### Complex Skill (2 hours)
```
Analysis (15 min) → Progressive Template → SKILL.md + references/ + examples/ → Validate → Done
```
Use for: Multi-domain skills, complex workflows

### Router Skill (3 hours)
```
Analysis (30 min) → Router Template → SKILL.md + delegation logic → Specialized skills → Validate → Done
```
Use for: Multiple workflows, pattern matching

## Troubleshooting

### Problem: SKILL.md too long
**Solution:** Move detailed content to references/

### Problem: Description not triggering
**Solution:** Add more trigger phrases and specific context

### Problem: Users confused about workflow
**Solution:** Add concrete examples and step-by-step process

### Problem: Token budget exceeded
**Solution:** Shorten descriptions, consolidate similar skills

### Problem: Poor discovery
**Solution:** Review naming and description patterns

## Success Metrics

Track these metrics to improve skill quality:

**Discovery Rate:** % of users who can find skill via natural language
**Usage Rate:** % who successfully complete workflow
**Satisfaction Score:** User feedback rating
**Efficiency Score:** Token usage vs value delivered

## Automation Scripts

Create these scripts for validation:

```bash
#!/bin/bash
# validate-skill.sh
echo "Checking skill structure..."

# Check SKILL.md
if [ $(wc -l < SKILL.md) -gt 400 ]; then
    echo "ERROR: SKILL.md exceeds 500 lines"
    exit 1
fi

# Check name format
if ! echo "$skill_name" | grep -qE '^[a-z][a-z0-9]*(-[a-z0-9]+)*$'; then
    echo "ERROR: Invalid name format"
    exit 1
fi

# Check description
desc_length=$(grep -o "description:" SKILL.md | wc -c)
if [ $desc_length -gt 1024 ]; then
    echo "ERROR: Description too long"
    exit 1
fi

echo "✓ Validation passed"
```

## Next Steps After Creation

1. **Monitor Usage** - Track discovery and success rates
2. **Gather Feedback** - Ask users what could be improved
3. **Iterate** - Update based on real-world usage
4. **Document Learnings** - Add insights to references/
5. **Share Patterns** - Contribute back to ecosystem
