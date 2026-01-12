# Workflow Examples

Complete, end-to-end examples demonstrating how to apply patterns and templates for real-world prompt engineering tasks.

## Example Catalog

### Example 1: Single Prompt Creation
**File:** `single-prompt-example.md`
**Pattern Applied:** Pattern 1 (Specialized Persona) + Pattern 2 (Hard Boundaries)
**Template Used:** `single-prompt.md`
**Complexity:** Low
**When to Use:** One-shot, direct task with clear requirements

### Example 2: Database Optimization Command
**File:** `complex-command-db-optimization.md`
**Pattern Applied:** GOLD_STANDARD_COMMAND (7 phases)
**Template Used:** `command-complex.md`
**Complexity:** High
**When to Use:** Multi-phase workflow with user approval gates

### Example 3: Sub-Agent Definition
**File:** `sub-agent-explorer.md`
**Pattern Applied:** Pattern 2 (Hard Boundaries) + Pattern 5 (Contrastive Examples)
**Template Used:** `agent-sub.md`
**Complexity:** Medium
**When to Use:** Specialized agent for specific domain task

### Example 4: Meta-Prompt Generator
**File:** `meta-prompt-generator.md`
**Pattern Applied:** Pattern 1 (Specialized Persona) + Pattern 4 (Protocol Prerequisites)
**Template Used:** `meta/` templates
**Complexity:** Medium
**When to Use:** Creating prompts that generate other prompts

### Example 5: Research Analysis Workflow
**File:** `research-workflow.md`
**Pattern Applied:** Pattern 6 (Plan Mode) + Research Prompts
**Template Used:** `command-complex.md` + Research Prompts
**Complexity:** High
**When to Use:** Complex analysis requiring multiple cognitive modes

## How to Use These Examples

1. **Identify Your Use Case:** Use the pattern matching guide in `references/discovery.md` to find the right example
2. **Copy the Template:** Start with the appropriate template from `assets/templates/`
3. **Follow the Pattern:** Apply the patterns demonstrated in the examples
4. **Customize:** Adapt the example to your specific domain and requirements
5. **Apply Quality Gates:** Use the approval workflow from `references/quality.md`

## Pattern-to-Example Mapping

| Pattern | Example | File |
|:--------|:--------|:-----|
| Pattern 1: Specialized Persona | Single Prompt | `single-prompt-example.md` |
| Pattern 2: Hard Boundaries | Sub-Agent | `sub-agent-explorer.md` |
| Pattern 3: Dynamic Context | Complex Command | `complex-command-db-optimization.md` |
| Pattern 4: Protocol Prerequisites | Meta-Prompt | `meta-prompt-generator.md` |
| Pattern 5: Contrastive Examples | Sub-Agent | `sub-agent-explorer.md` |
| Pattern 6: Plan Mode | Research Workflow | `research-workflow.md` |
| Pattern 7: Parsimonious XML | All examples | All files |

## Quality Checklist for Examples

- [ ] Follows all 7 golden patterns
- [ ] Uses appropriate template
- [ ] Includes hard boundaries
- [ ] Has clear output format
- [ ] Provides contrastive examples
- [ ] Implements quality gates (if complex)
- [ ] XML tag count ≤ 15
- [ ] No nested XML tags
