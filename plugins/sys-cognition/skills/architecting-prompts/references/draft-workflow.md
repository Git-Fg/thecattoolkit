# Draft New Prompt

Create high-quality prompts from scratch using proven engineering patterns.

## One-Pass Implementation Rule

**CRITICAL:** If the user provides complete requirements, generate the final PROMPT.md in a single turn without permission fishing. Do NOT ask "Shall I create the file?" or "Is this approach okay?" - execute immediately.

## Workflow

### 1. Analyze Task Requirements
Identify the core elements of your prompt need:
- **Purpose**: What should the prompt accomplish?
- **Context**: What background information is needed?
- **Constraints**: Any specific rules or limitations?
- **Output format**: How should results be structured?
- **Complexity level**: Simple task or multi-step workflow?

### 2. Consult Core Standards
**ALWAYS** load `references/core-standards.md` first to apply:
- Attention Management principles
- Sycophancy Prevention (Truth-First)
- XML vs Markdown decision matrix

### 3. Select Appropriate Pattern
Based on the prompt-engineering skill, choose the right approach:
- **Chain-of-Thought (CoT)**: For reasoning-heavy tasks
- **Few-shot learning**: When examples help clarify intent
- **Role-based**: For specialized expertise (e.g., "You are a security auditor...")
- **Template-based**: Following standardized structure from templates

### 4. Apply Complexity Decision Framework
Use the Signal-to-Noise Rule from core-standards:
- **Markdown-first**: Default for most prompts (fewer tokens, Claude-native)
- **Hybrid XML/Markdown**: Only when complexity triggers met:
  - Data Isolation: >50 lines of raw data
  - Constraint Weight: Rules that MUST NEVER be broken
  - Internal Monologue: Complex reasoning requiring step-by-step

### 5. Create High-Quality Prompt
Structure the prompt following best practices:
- Use `# Context` section for background
- Use `# Assignment` section for specific instructions
- Include concrete examples when helpful (wrap in `<example>` tags)
- Keep instructions clear and unambiguous
- Apply Truth-First principle (no sycophancy)
- Apply appropriate pattern from templates

### 6. Output to File
Write the completed prompt to:
- **PROMPT.md** in the current directory (or specified path)
- Include YAML frontmatter if needed
- Follow template structure from `assets/templates/`

## Key Resources
- **Core Standards**: `references/core-standards.md` (ALWAYS load first)
- **Design Patterns**: `references/design-patterns.md` (techniques and structure)
- **Templates**: `assets/templates/`
- **Quality Gates**: `references/quality.md`

## Success Criteria
Prompt saved to file with:
- Clear instructions following 2026 standards
- Appropriate structure (Markdown/XML per complexity)
- Examples isolated in `<example>` tags if used
- Truth-First language (no sycophancy)
- Ready for immediate use
