# Research & Prompting Anti-Patterns

A catalog of known pitfalls, mistakes, and red flags to avoid.

## Prompting Pitfalls

### 1. The "XML Soup"
**What**: Excessive or nested XML tags.
**Why**: Increases token cost and confuses the model's structural parsing.
**Prevention**: Limit to 15 flat tags. Use Markdown for content, XML only for containers.

### 2. Example Leakage
**What**: AI follows example content instead of instructions.
**Why**: Examples not properly isolated from the task instruction.
**Prevention**: Always wrap individual examples in flat `<example>` tags.

### 3. Vague Instructions
**What**: "Analyze this", "Check for bugs", "Be helpful".
**Why**: Lack of specific success criteria leads to generic, inconsistent output.
**Prevention**: Use specific action verbs and define exactly what "analysis" or "bugs" look like.

### 4. Over-Engineering
**What**: Adding 20 constraints and 10 examples for a simple task.
**Why**: Dilutes the attention of the model and risks hitting token limits.
**Prevention**: Start with Pure Markdown. Add complexity only where testing proves it's needed.

## Research Pitfalls

### 1. Scope Assumptions
**What**: Assuming evidence of absence is evidence of absence.
**Example**: "I didn't find a config file, so it doesn't exist."
**Prevention**: Explicitly verify all possible scopes (Global, Project, Local, Environment).

### 2. Deprecation Blindness
**What**: Relying on outdated documentation.
**Why**: Older docs (especially blogs/Q&A) often contradict current tool capabilities.
**Prevention**: Prioritize official docs and check "Updated" dates/Changelogs.

### 3. Single-Source Reliance
**What**: Basing critical claims on one source.
**Prevention**: Cross-reference multiple authoritative sources (Official Docs + GitHub Issues + Changelog).

### 4. Vagueness in Search
**What**: Poorly formulated queries like "How does X work?".
**Prevention**: Use specific, version-targeted queries like "{tool_name} v1.2 configuration example".

## Red Flags in AI Outputs

- **🚩 100% Success**: Every investigation perfectly succeeds (suspiciously clean).
- **🚩 Zero Citations**: Claims made without URLs or documentation references.
- **🚩 Binary Thinking**: "It is impossible" vs "It is the only way" without evidence.
- **🚩 Role Redefinition**: Forgetting the primary agent role in favor of a local prompt instruction.

## Verification Checklist
- [ ] Are examples isolated?
- [ ] Is XML minimal and flat?
- [ ] Are claims cited with URLs?
- [ ] Have all scopes been checked?
- [ ] Is the version relevance confirmed?
