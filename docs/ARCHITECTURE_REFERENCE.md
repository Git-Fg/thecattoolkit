# Endpoint Technical Reference

Technical API configuration for multi-LLM provider support. For behavioral adaptation rules and optimization strategies, see [IMPLEMENTATION-GUIDE.md](IMPLEMENTATION-GUIDE.md#endpoint-adaptation-rules).

---

## Anthropic (Official)

| Property | Value |
|:---------|:------|
| **CLI** | `claude-code` |
| **Default Model** | `Claude 3.5 Sonnet` |
| **Context Window** | 200k+ tokens |
| **Native Tools** | `Task`, `Skill` |
| **Vision** | Native support |
| **API** | `https://api.anthropic.com` |

---

## Zai / GLM (Unofficial)

| Property | Value |
|:---------|:------|
| **CLI** | `zai-cli` or `ZtoApi` proxy |
| **Models** | GLM-4.5, GLM-4.6V (Vision), GLM-4.7 |
| **Tool Schema** | Maps to Claude's tool schema via native function calling |
| **Structure** | Compatible with `.claude/` directory layout |
| **Vision** | GLM-4.6V for image analysis |
| **API** | Via `ANTHROPIC_BASE_URL` proxy |

---

## Minimax M2 (Unofficial)

| Property | Value |
|:---------|:------|
| **Endpoint** | `https://api.minimax.chat/v1/text/chat/completions_pro` |
| **Strength** | Fast inference, multi-file context handling |
| **Optimization** | Parallel Agent Pattern |
| **API** | Via `ANTHROPIC_BASE_URL` proxy |

---

## Comparative Summary

| Feature | Anthropic | Zai/GLM | Minimax |
|:--------|:----------|:--------|:---------|
| **Official Support** | ✅ Yes | ❌ No | ❌ No |
| **Context Window** | 200k+ | ~128k | ~100k |
| **Native Task/Skill** | ✅ Yes | ✅ Yes | ⚠️ Partial |
| **Vision Models** | ✅ Yes | ✅ 4.6V | ❌ No |
| **Inference Speed** | Medium | Fast | **Very Fast** |
| **Best For** | Complex reasoning | Cost efficiency | Multi-file edits |

---

## Environment Configuration

For API keys, base URLs, and proxy setup, see [IMPLEMENTATION-GUIDE.md](IMPLEMENTATION-GUIDE.md#environment-configuration).
