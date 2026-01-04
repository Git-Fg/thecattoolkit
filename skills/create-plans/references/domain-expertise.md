# Domain Expertise

## Overview

Domain expertise skills are comprehensive knowledge bases generated on-demand into user-space paths. They provide framework-specific patterns, best practices, and complete lifecycle workflows for various technology stacks.

**Critical:** Domain expertise is NOT shipped with the plugin. It is generated into your project or user space as needed.

## Location Structure

Domain expertise lives in two possible locations:

### Project-Level (Recommended)
```
.claude/skills/expertise/{domain-name}/
├── SKILL.md                          # Router with essential principles
├── workflows/
│   ├── build-new-{thing}.md          # Create from scratch
│   ├── add-feature.md                # Extend existing
│   ├── debug-{thing}.md              # Find and fix bugs
│   ├── write-tests.md                # Test for correctness
│   ├── optimize-performance.md       # Profile and speed up
│   └── ship-{thing}.md               # Deploy/distribute
└── references/
    ├── architecture.md               # Project structure patterns
    ├── libraries.md                  # Ecosystem overview
    ├── patterns.md                   # Design patterns
    ├── testing-debugging.md          # Verification approaches
    ├── performance.md                # Optimization strategies
    └── anti-patterns.md              # Common mistakes
```

### User-Level
```
~/.claude/skills/expertise/{domain-name}/
[Same structure as project-level]
```

## Generation

**How to create domain expertise:**

1. Use the central router: `/toolkit` → Create → Domain Expertise Skill
2. Specify your technology stack (e.g., "macOS apps with SwiftUI")
3. Choose location (project-level or user-level)
4. Skill generates comprehensive knowledge base with:
   - 5+ research phases covering ecosystem, architecture, tooling, pitfalls
   - Complete lifecycle workflows (build → debug → test → optimize → ship)
   - Decision trees and library comparisons
   - Platform-specific considerations
   - Anti-patterns and common mistakes

## Discovery

The `create-plans` skill automatically scans for domain expertise:

```bash
# Check for project-level
ls -la .claude/skills/expertise/

# Check for user-level
ls -la ~/.claude/skills/expertise/
```

**If no expertise found for your stack:**
create-plans will suggest: "No domain expertise found for this stack. Run `/toolkit` → Create → Domain Expertise Skill"

## Usage

### Direct Invocation
Users can invoke domain expertise skills directly:
```
> Use the build-macos-apps skill to create a menu bar app
```

The skill will:
1. Route to appropriate workflow (build, debug, add feature, etc.)
2. Load relevant reference files
3. Provide step-by-step implementation
4. Include verification steps

### Planning Integration
The `create-plans` skill loads domain expertise references when:
- Planning a project in that domain
- Making framework-specific decisions
- Choosing between libraries or patterns
- Understanding best practices

## Examples

### Platform-Specific Expertise
**Location:** `.claude/skills/expertise/{platform-name}/` (user-generated)

**Provides:**
- Framework-specific patterns and best practices
- Platform-specific APIs and frameworks
- Tooling and build configuration
- Distribution and signing workflows
- Performance optimization strategies
- Common pitfalls and anti-patterns

**Workflows:**
- `build-new-{thing}.md` - Create from scratch
- `debug-{thing}.md` - Debug and fix issues
- `optimize-{thing}.md` - Performance tuning
- `ship-{thing}.md` - Build and distribute

### Python Games Expertise
**Location:** `.claude/skills/expertise/python-games/`

**Provides:**
- Library comparisons (Pygame vs Arcade vs Panda3D)
- Game loop patterns and state management
- Physics and collision detection
- Audio and graphics optimization
- Asset pipeline management
- Performance profiling

**Workflows:**
- `build-new-python-game.md` - Complete game from scratch
- `add-game-mechanic.md` - Implement specific features
- `optimize-game-performance.md` - Profile and optimize

## Best Practices

### When to Create Domain Expertise
- Working with unfamiliar technology stack
- Need comprehensive guidance beyond basic tutorials
- Want framework-specific patterns and best practices
- Building complete projects (not just prototypes)
- Need decision guidance (which library, approach, pattern)

### What Makes Good Domain Expertise
- **Comprehensive:** Covers full lifecycle (build → ship)
- **Current:** Verified for 2024-2025 ecosystem
- **Practical:** Decision trees and "when to use X vs Y"
- **Actionable:** Workflows that execute real tasks
- **Complete:** Anti-patterns and common mistakes documented

## Integration with Planning

Domain expertise enhances planning by:

1. **Providing Context:** Framework-specific patterns inform task breakdown
2. **Library Decisions:** Comparisons guide architecture choices
3. **Best Practices:** Prevent common mistakes and anti-patterns
4. **Verification:** Domain-specific testing and debugging approaches
5. **Optimization:** Performance patterns and profiling techniques

## Success Criteria

Well-designed domain expertise:
- [ ] Enables building professional projects from scratch
- [ ] Covers complete lifecycle (build → debug → test → optimize → ship)
- [ ] Includes current library comparisons and decision trees
- [ ] Documents platform-specific considerations
- [ ] Provides actionable workflows (not just reference material)
- [ ] Located in user-space paths (project or user level)
- [ ] Can be invoked directly AND loaded by create-plans
