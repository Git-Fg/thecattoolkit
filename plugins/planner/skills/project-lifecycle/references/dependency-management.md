# Dependency Management Reference

## Autonomous Dependency Detection

The Project Orchestrator uses AI-native capabilities to detect and manage dependencies across all technology stacks without hardcoding specific package managers.

### Detection Approach

**AI-Native Discovery:**
1. **Filesystem Analysis:** Agents use filesystem tools to identify project structure and configuration files
2. **Pattern Recognition:** Recognize lock files, configuration files, and manifest files using your natural language understanding
3. **Technology Stack Inference:** Infer the programming language and ecosystem from project structure
4. **Package Manager Identification:** Identify the appropriate dependency management tool for the detected stack

**Universal Detection:**
Rather than hardcoding specific files, the orchestrator:
- Scans for lock files using your filesystem exploration capabilities
- Identifies configuration files that indicate package management systems
- Analyzes project structure to determine the technology stack
- Adapts to any language or framework

### Best Practices

1. **Autonomous Detection:** Agents should use their natural language and reasoning capabilities to identify dependency management systems
2. **Technology Agnostic:** Approach works for any language: JavaScript, Python, Rust, Go, Ruby, PHP, etc.
3. **Consistency:** Use the detected package manager consistently throughout the project
4. **Documentation:** All dependency changes must be documented in ADR.md with:
   - What was added/changed
   - Why it was necessary
   - Package management approach used
   - Verification steps taken

### Agent Behavior

Task executors autonomously:
- Use AI-native discovery to detect missing dependencies
- Identify and use the appropriate tool for the project's ecosystem
- Update configuration files using their natural language understanding
- Verify installations through testing and validation
- Document all changes in ADR.md

**Remember:** Trust your AI capabilities to identify the right package manager for any technology stack, rather than following hardcoded lists.
