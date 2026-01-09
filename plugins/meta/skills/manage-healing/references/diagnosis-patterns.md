# Diagnosis Patterns

Decision tree for identifying the root cause of a failure during the `/heal` workflow.

## 1. Tool Usage Failures

**Did the AI try to use a tool and fail?**

- **Yes, "Tool not found":** The Skill/Agent definition lists a tool that isn't in `allowed-tools` or installed.
  - *Fix:* Update `allowed-tools` or remove the instruction.
- **Yes, "Invalid arguments":** The Skill/Agent provides an example with wrong syntax.
  - *Fix:* Correct the `<example>` block in the markdown.

## 2. Context Failures

**Did the AI ask a question it should have known?**

- **Yes:** The component failed to load necessary reference files.
  - *Fix:* Add `@reference` links to the Command or Agent prompt.

## 3. Orchestration Failures

**Did a subagent fail to complete the task?**

- **Yes, returned early:** Ambiguous success criteria.
  - *Fix:* Add explicit "Success Criteria" section to the Agent prompt.
- **Yes, hung/looped:** Missing "Stop" condition or "Handoff" protocol.
  - *Fix:* Add HANDOFF protocol to the Agent.

## 4. Output Format Failures

**Did the AI produce malformed output?**

- **Yes, wrong structure:** Missing or incorrect example in component definition.
  - *Fix:* Add concrete `<example>` block with correct input/output pair.
- **Yes, wrong encoding:** JSON/YAML syntax issues in frontmatter or examples.
  - *Fix:* Validate and correct syntax errors.

## 5. Permission/Safety Failures

**Did the AI attempt a blocked operation?**

- **Yes, file access denied:** Missing tool in `allowed-tools` or path outside scope.
  - *Fix:* Update `allowed-tools` or clarify path constraints.
- **Yes, violated constraint:** Weak constraint language (suggestion vs requirement).
  - *Fix:* Harden constraint with MUST/NEVER uppercase language.
