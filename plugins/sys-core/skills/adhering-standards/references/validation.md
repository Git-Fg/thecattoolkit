# Validation Protocol

## Component Validation

Any component MUST pass validation before deployment:

### Skills Validation
- [ ] Valid YAML frontmatter
- [ ] Description starts with "USE when"
- [ ] `allowed-tools` specified (or explicitly omitted)
- [ ] Templates selected correctly
- [ ] Progressive disclosure applied if complex
- [ ] References organized in `references/`

### Commands Validation
- [ ] Valid YAML frontmatter
- [ ] Orchestrates 2+ distinct Skills (not single-skill wrapper)
- [ ] Clear, specific description
- [ ] Semantic category selected
- [ ] Tool restrictions added (if needed)
- [ ] Tested with real invocation

### Agents Validation
- [ ] Valid YAML frontmatter
- [ ] Description optimized for routing
- [ ] Tool restrictions (least privilege)
- [ ] Well-structured system prompt
- [ ] Model selection appropriate
- [ ] AskUserQuestion only in coordinators, not workers

## Best Practices

### For Skills

1. **Inline-First:** Default to inline execution for quota efficiency
2. **Fork Only When:** Task exceeds context window OR strict isolation needed
3. **Progressive Disclosure:** Keep SKILL.md < 400 lines, move details to `references/`
4. **Template-Driven:** Always use templates from `assets/templates/`

### For Commands

1. **Multi-Skill Orchestration:** Commands should sequence 2+ skills
2. **User-Centric:** Design for human convenience, not programmatic APIs
3. **Autonomous Execution:** Avoid interactive prompts; make decisions automatically
4. **Argument Integration:** Use `$ARGUMENTS` for user input

### For Agents

1. **Persona Binding:** Design agents to be bound to Skills via `agent:` field
2. **Least Privilege:** Specify `tools` whitelist for security
3. **Background Safety:** Read-only tools (Read, Grep, Glob) for background execution
4. **No AskUser in Workers:** Remove `AskUserQuestion` from worker agent `tools`

## Integration Points

- **standards-communication.md** - Common principles for all components
- **scaffold-component** - Natural language to component generation
- **meta-builder** - Live documentation fetching for compliance
- **validate-toolkit** - Comprehensive testing and validation

## Continuous Improvement

### Refactoring Triggers

**Consider refactoring when:**
- Component becomes too complex
- Usage patterns change
- New patterns emerge
- Standards evolve

### Refactoring Principles

- Enforce clean breaks over backward compatibility (Codebase > History)
- Preserve core functionality
- Improve clarity and usability
- Reduce complexity
- Enhance maintainability
