# Endpoint Compatibility

This document contains endpoint-specific optimizations for non-Anthropic usage. For core architecture specifications, see [CLAUDE.md](../CLAUDE.md).

## Endpoint Optimization (Universal Compatibility)

While optimized for `anthropics/claude-code`, the toolkit is designed for **Universal Compatibility** across major agentic endpoints.

### Official (Anthropic)
- **Standard**: Uses `claude-code` CLI and `Claude 3.5 Sonnet`.
- **Primary Mechanic**: Native `Task` and `Skill` tools.
- **Context**: Optimized for large context windows (200k+).

### Unofficial: Zai Code (Z.ai / GLM)
- **Standard**: Uses `zai-cli` or `ZtoApi` proxy.
- **Models**: GLM-4.5, GLM-4.6V (Vision), GLM-4.7.
- **Optimization**:
  - **Tool Calling**: Leverages GLM's native function calling which maps to Claude's tool schema.
  - **Vision**: Optimized for skill-based image analysis using `GLM-4.6V`.
  - **Auto-Discovery**: Compatible with the `.claude/` structure for rules and commands.

### Unofficial: Minimax Code (MiniMax-M2)
- **Standard**: Model endpoint `https://api.minimax.chat/v1/text/chat/completions_pro`.
- **Optimization**:
  - **Multi-File Context**: Optimized for the `MiniMax-M2` ability to handle complex multi-file edits.
  - **Parallelism**: Highly efficient when using the **Parallel Agent Pattern** due to fast inference.
  - **Testing**: Native support for coding-run-fix loops.

For environment configuration (API keys, base URLs), see [IMPLEMENTATION-GUIDE.md](IMPLEMENTATION-GUIDE.md#environment-configuration).
