# Endpoint Technical Reference

Technical API configuration for non-Anthropic endpoints. For behavioral adaptation rules, see [CLAUDE.md Section 5.6](../CLAUDE.md#56-runtime-constraints-endpoint-awareness).

---

## Anthropic (Official)

| Property | Value |
|:---------|:------|
| **CLI** | `claude-code` |
| **Default Model** | `Claude 3.5 Sonnet` |
| **Context Window** | 200k+ tokens |
| **Native Tools** | `Task`, `Skill` |

---

## Zai / GLM (Unofficial)

| Property | Value |
|:---------|:------|
| **CLI** | `zai-cli` or `ZtoApi` proxy |
| **Models** | GLM-4.5, GLM-4.6V (Vision), GLM-4.7 |
| **Tool Schema** | Maps to Claude's tool schema via native function calling |
| **Structure** | Compatible with `.claude/` directory layout |

---

## Minimax M2 (Unofficial)

| Property | Value |
|:---------|:------|
| **Endpoint** | `https://api.minimax.chat/v1/text/chat/completions_pro` |
| **Strength** | Fast inference, multi-file context handling |

---

For environment configuration (API keys, base URLs), see [IMPLEMENTATION-GUIDE.md](IMPLEMENTATION-GUIDE.md#environment-configuration).
