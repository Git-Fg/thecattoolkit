# Security & Async Standards

## 1. Background Execution Safety
Agents running in the background/async cannot ask for permissions.
*   **Read-Only:** Agents using `Read`, `Grep`, `Glob` are always safe for background.
*   **Write/Execute:** Agents using `Write`, `Edit`, `Bash` must use the `auto-approve` flag or be invoked in Foreground mode.

## 2. Tool Restrictions
*   **Commands:** Must use `allowed-tools` to restrict scope.
*   **Agents:** Must specify `tools:` in frontmatter.
*   **Skills:** You Can specify tools, which act as permission bypass.

## 3. Path Traversal
*   **Rule:** References must use `${CLAUDE_PLUGIN_ROOT}` or relative paths.
*   **Forbidden:** Hardcoded absolute paths (e.g., `/Users/name/...`).

## 4. Tool Permission Standards

### Allowed Tools Declaration

**When to specify `allowed-tools`:**
- Skill needs specific permissions
- Security restrictions required
- Performance optimization needed
- Background execution intended

**When to omit `allowed-tools`:**
- Skill is reference-only
- No tool usage required
- Full tool access acceptable

### Security Principles

**Follow least privilege:**
- Grant only necessary tools
- Consider execution context (foreground vs. background)
- Validate all inputs
- Sanitize all outputs

## 5. Cross-Platform Compatibility

### Platform-Specific Considerations

**File System Differences:**
- Use forward slashes (/) in paths for cross-platform compatibility
- Avoid hardcoded directory separators
- Use environment variables for user-specific paths

**Shell Command Compatibility:**
- Use POSIX-compliant commands when possible
- Avoid platform-specific shell syntax
- Test commands across different platforms

**Python Script Compatibility:**
- Specify Python version requirements in scripts
- Use cross-platform libraries
- Avoid OS-specific imports (use pathlib instead of os.path for paths)

## 6. Error Handling & Security

### Graceful Degradation

**When external dependencies fail:**
- Log the failure securely (no sensitive data)
- Provide fallback behavior
- Document limitations
- Continue if possible

### Error Messages

**Good error messages:**
- Specific about what failed
- Explain why it failed
- Suggest how to fix
- Include relevant context
- Never expose sensitive information

**Example:**
```
 "Failed to create skill"
 "Failed to create skill: Directory 'my-skill' already exists at .claude/skills/my-skill. Remove existing directory or use different name."
```

### Security Considerations

**Input Validation:**
- Validate all user inputs
- Sanitize file paths
- Check for directory traversal attempts
- Limit input length and complexity

**Output Sanitization:**
- Escape special characters in generated files
- Validate generated YAML
- Check file permissions
- Ensure no sensitive data leakage

## 7. Template Usage Security

### Template Customization

**Allowed customizations:**
- Content within sections
- Additional sections
- Custom success criteria
- Specialized validation

**Prohibited customizations:**
- Removing required YAML fields
- Breaking directory structure
- Violating naming conventions
- Introducing security vulnerabilities

## 8. Dependency Management Security

### When modifying skills that other components depend on:

1. Identify all dependents:
   - Agents listing this skill
   - Commands invoking this skill
   - Other skills referencing this skill

2. Assess security impact:
   - Will changes introduce new vulnerabilities?
   - Are security boundaries maintained?
   - Is least privilege preserved?

3. Update dependents:
   - Update agent skill bindings
   - Update command invocations
   - Update skill references

### Breaking Changes Security

**When introducing breaking changes:**
1. Document the security implications
2. Provide migration guide
3. Update all dependents
4. Increment version (if versioned)
5. Communicate to users

## 9. Integration Security

### Slash Command Integration

**When creating slash commands:**
- Validate argument inputs
- Sanitize command execution
- Check file permissions
- Log security-relevant events

### Agent Binding Security

**When agents should use skills:**
- Verify skill permissions are compatible
- Ensure least privilege maintained
- Check tool access boundaries
- Validate execution context

**Skill binding in agents:**
```yaml
---
skills: [toolkit-registry, builder-core, plan-execution]
---
```

## 10. Testing Security

### Security Testing

**Skills should include:**
- Input validation tests
- Permission boundary tests
- Path traversal protection tests
- Cross-platform compatibility tests

### Integration Testing

**Test with:**
- Different execution contexts (foreground/background)
- Various permission levels
- Edge cases and malicious inputs
- Cross-platform scenarios
