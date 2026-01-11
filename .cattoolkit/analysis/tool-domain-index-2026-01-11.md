# Tool Domain Index
**Date**: 2026-01-11
**Purpose**: Master reference for all tools organized by domain and function

---

## QUICK DOMAIN GUIDE

### 🏗️ **INFRASTRUCTURE & SYSTEM**
**Use for**: Security, validation, plugin management, quality assurance
**Plugins**: sys-core, sys-meta

### 👨‍💻 **DEVELOPMENT & ENGINEERING**
**Use for**: Coding, architecture, planning, execution
**Plugin**: sys-builder

### 🧠 **AI/ML & COGNITIVE**
**Use for**: AI optimization, context management, edge AI, LLM applications
**Plugins**: sys-cognition, sys-edge, llm-application-dev

### 🔬 **RESEARCH & KNOWLEDGE**
**Use for**: Research, documentation, business intelligence
**Plugins**: sys-research, business-analytics

### 🎬 **MEDIA & MULTIMODAL**
**Use for**: Video editing, media processing, multimodal AI
**Plugin**: sys-multimodal

---

## DETAILED TOOL REFERENCE

## 🏗️ INFRASTRUCTURE & SYSTEM DOMAIN

### **Subdomain: Security & Safety**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `audit-security` | sys-core | Skill | Security code verification | Verifying code changes or auditing file safety |
| `check-types` | sys-core | Skill | Python type validation | Validating Python type safety (auto-runs after edits) |

### **Subdomain: Validation & Quality**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `validate-toolkit` | sys-core | Skill | Comprehensive plugin validation | Testing and validating plugins before distribution |
| `manage-healing` | sys-core | Skill | Component failure diagnosis | Diagnosing component failures or instruction drift |
| `test-writer` | sys-core | Skill | Vitest test generation | Generating tests for JavaScript documentation |

### **Subdomain: Plugin Management**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `scaffold-component` | sys-core | Skill | Plugin component creation | Creating new plugin components (skills, agents, commands) |
| `toolkit-registry` | sys-core | Skill | Plugin management authority | Creating, auditing, or managing plugin components |
| `meta-hooks` | sys-meta | Skill | Hook development guidance | Creating hooks, implementing event-driven automation |
| `meta-mcp` | sys-meta | Skill | MCP integration | Integrating databases via MCP, setting up MCP servers |
| `plugin-expert` | sys-meta | Agent | Agent Skills compliance | Maintaining or auditing Agent Skills framework |

---

## 👨‍💻 DEVELOPMENT & ENGINEERING DOMAIN

### **Subdomain: Code Development**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `python-tools` | sys-core | Skill | Python ecosystem management | Managing Python projects, dependencies, linting, formatting |
| `software-engineering` | sys-builder | Skill | Universal coding standard | Writing code, debugging, reviewing PRs (TDD, Security, Code Quality) |
| `py` | sys-edge | Command | Python environment shortcut | Quick Python tasks and environment access |

### **Subdomain: Architecture & Design**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `architecture` | sys-builder | Skill | System design | Designing new systems or analyzing existing architecture |
| `designer` | sys-builder | Agent | Design architect | Need design consultation and system architecture guidance |
| `agent-orchestration` | sys-cognition | Skill | Multi-agent patterns | Designing multi-agent systems for context isolation |

### **Subdomain: Planning & Execution**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `manage-planning` | sys-builder | Skill | Project planning & execution | Planning projects or executing phases |
| `planning-with-files` | sys-cognition | Skill | File-based planning | Creating structured workflows with persistent state |
| `plan` | sys-builder | Command | Project initialization | Initialize or update project plan |
| `build` | sys-builder | Command | Execute current phase | Execute the current phase in ROADMAP.md |

### **Subdomain: Repository & Code Analysis**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `reasoner` | sys-cognition | Agent | Deep analysis | Performing deep, autonomous codebase analysis |
| `gitingest` | sys-edge | Skill | Repository ingestion | Transforming repositories into AI-readable digests |
| `ingest` | sys-edge | Command | Repository ingestion | Quick repository ingestion for AI analysis |

---

## 🧠 AI/ML & COGNITIVE DOMAIN

### **Subdomain: Context & Memory**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `context-management` | sys-cognition | Skill | Session state | Managing persistent session state, avoiding context overflow |
| `context-compression` | sys-cognition | Skill | Token optimization | Optimizing token usage through intelligent compression |
| `context-degradation` | sys-cognition | Skill | Context failure detection | Identifying context degradation patterns |
| `kv-cache` | sys-cognition | Skill | Cache optimization | Optimizing cost and latency through KV-cache reuse |
| `memory-systems` | sys-cognition | Skill | Persistent memory | Designing persistent memory architectures |

### **Subdomain: AI Reasoning & Analysis**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `deep-analysis` | sys-cognition | Skill | Strategic analysis | Deep strategic analysis and formal report synthesis |
| `thinking-frameworks` | sys-cognition | Skill | Structured reasoning | Applying structured frameworks (Pareto, Inversion, etc.) |
| `reasoner` | sys-cognition | Agent | Forensic analysis | Forensic analysis of codebases and architectures |
| `think` | sys-cognition | Command | Thinking wizard | Clarifying goals, exploring constraints |

### **Subdomain: Prompt Engineering**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `prompt-engineering` | sys-cognition | Skill | Prompt optimization | Designing, optimizing, or auditing AI prompts |

### **Subdomain: Agent Orchestration**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `agent-orchestration` | sys-cognition | Skill | Multi-agent patterns | Designing multi-agent systems |
| `director` | sys-builder | Agent | Massive-scale orchestration | When plan exceeds main-thread context |
| `worker` | sys-builder | Agent | Execution worker | Implementing features, debugging, engineering tasks |

### **Subdomain: Edge & Mobile AI**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `edge-ai-management` | sys-edge | Skill | Mobile AI models | Managing AI models on mobile/edge devices |
| `mobile-optimization` | sys-edge | Skill | Mobile optimization | Optimizing AI applications for mobile devices |
| `offline-sync` | sys-edge | Skill | Offline-first sync | Implementing offline-first synchronization |

### **Subdomain: LLM Applications**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `hybrid-search-implementation` | llm-application-dev | Skill | Hybrid search systems | Implementing RAG systems with combined vector/keyword search |

---

## 🔬 RESEARCH & KNOWLEDGE DOMAIN

### **Subdomain: Scientific Research**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `alphafold-database` | sys-research | Skill | Protein structures | Working with protein structure databases |
| `scientific-slides` | sys-research | Skill | Research presentations | Creating scientific presentations and slides |
| `researcher` | sys-research | Skill | Research protocols | Implementing research methodologies |
| `deep-research` | sys-research | Command | Research playbook | Deep technical research tasks |

### **Subdomain: Business Intelligence**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `data-storytelling` | business-analytics | Skill | Data narratives | Transforming data into compelling narratives for stakeholders |

---

## 🎬 MEDIA & MULTIMODAL DOMAIN

### **Subdomain: Video Editing**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `video-editor` | sys-multimodal | Agent | Autonomous editing | AI-assisted video editing with natural language |
| `edit-video` | sys-multimodal | Command | Video editing shortcut | Quick video editing tasks |
| `intent-translation` | sys-multimodal | Skill | Intent to commands | Converting natural language to editing commands |

### **Subdomain: Media Understanding**
| Tool | Plugin | Type | Description | When to Use |
|:-----|:-------|:-----|:------------|:------------|
| `multimodal-understanding` | sys-multimodal | Skill | Video/audio analysis | Understanding and analyzing video and audio content |
| `canvas-design` | sys-multimodal | Skill | Design systems | Creating visual designs and canvas-based interfaces |

---

## DECISION TREE: WHICH TOOL TO USE?

### **I need to analyze code**
1. Deep analysis? → `sys-cognition:reasoner`
2. Quick repository digest? → `sys-edge:gitingest` or `sys-edge:ingest`

### **I need to design a system**
1. Overall system architecture? → `sys-builder:architecture` or `sys-builder:designer`
2. Multi-agent system? → `sys-cognition:agent-orchestration`

### **I need to plan a project**
1. Project management? → `sys-builder:manage-planning`
2. Structured file-based planning? → `sys-cognition:planning-with-files`
3. Quick setup? → `sys-builder:plan`

### **I need to validate code**
1. Security audit? → `sys-core:audit-security`
2. Type safety? → `sys-core:check-types`
3. Plugin validation? → `sys-core:validate-toolkit`

### **I need to optimize AI**
1. Token usage? → `sys-cognition:context-compression`
2. Cost/latency? → `sys-cognition:kv-cache`
3. Memory management? → `sys-cognition:memory-systems`
4. Context issues? → `sys-cognition:context-degradation`

### **I need to work with Python**
1. Full ecosystem? → `sys-core:python-tools`
2. Quick tasks? → `sys-edge:py`

### **I need to create a plugin**
1. Core component? → `sys-core:scaffold-component`
2. Hooks? → `sys-meta:meta-hooks`
3. MCP integration? → `sys-meta:meta-mcp`
4. Compliance? → `sys-meta:plugin-expert`

---

## OVERLAP RESOLUTION GUIDE

### **Repository Analysis**
| Scenario | Primary Tool | Alternative | Why |
|:---------|:-------------|:------------|:-----|
| Deep codebase understanding | `sys-cognition:reasoner` | `sys-edge:gitingest` | Reasoner provides deeper analysis |
| Quick repo preparation | `sys-edge:gitingest` | `sys-edge:ingest` | Ingest is a command shortcut |
| AI consumption preparation | `sys-edge:gitingest` | `sys-cognition:reasoner` | Gitingest is optimized for AI |

### **Architecture Design**
| Scenario | Primary Tool | Alternative | Why |
|:---------|:-------------|:------------|:-----|
| System architecture | `sys-builder:architecture` | `sys-builder:designer` | Architecture is the skill, designer is the agent |
| Multi-agent systems | `sys-cognition:agent-orchestration` | `sys-builder:architecture` | Agent-orchestration is specialized |

### **Planning**
| Scenario | Primary Tool | Alternative | Why |
|:---------|:-------------|:------------|:-----|
| Project management | `sys-builder:manage-planning` | `sys-cognition:planning-with-files` | Manage-planning is for execution tracking |
| File-based workflows | `sys-cognition:planning-with-files` | `sys-builder:manage-planning` | Planning-with-files is for structured workflows |

### **Python Development**
| Scenario | Primary Tool | Alternative | Why |
|:---------|:-------------|:------------|:-----|
| Comprehensive Python work | `sys-core:python-tools` | `sys-edge:py` | Python-tools covers the full ecosystem |
| Quick environment access | `sys-edge:py` | `sys-core:python-tools` | Py is a shortcut command |

---

## DOMAIN CROSS-REFERENCE

### **Tools that span multiple domains**

| Tool | Primary Domain | Secondary Domain | Note |
|:-----|:---------------|:----------------|:-----|
| `sys-edge:gitingest` | AI/ML & COGNITIVE | DEVELOPMENT & ENGINEERING | Repository analysis for AI consumption |
| `sys-cognition:agent-orchestration` | AI/ML & COGNITIVE | DEVELOPMENT & ENGINEERING | System design for AI systems |
| `sys-cognition:planning-with-files` | AI/ML & COGNITIVE | DEVELOPMENT & ENGINEERING | Structured planning methodology |

### **Command vs Skill patterns**

| Function | Skill | Command | When to use Command |
|:---------|:------|:--------|:-------------------|
| Planning | `manage-planning` | `plan`, `build` | Quick, focused tasks |
| Python | `python-tools` | `py` | Environment shortcuts |
| Research | `researcher` | `deep-research` | Comprehensive research |
| Video | `video-editor` | `edit-video` | Quick edits |
| Thinking | `thinking-frameworks` | `think` | Interactive wizard |

---

## BEST PRACTICES

1. **Start with Domain**: Identify which domain your task belongs to
2. **Check Subdomain**: Narrow down to the specific function needed
3. **Use Decision Tree**: Follow the decision tree for common scenarios
4. **Resolve Overlaps**: Use the overlap resolution guide when multiple tools seem applicable
5. **Prefer Skills for Complex Work**: Use skills for comprehensive, multi-step tasks
6. **Use Commands for Shortcuts**: Use commands for quick, focused actions

---

## ADDITIONAL RESOURCES

- **Full Taxonomy Framework**: `.cattoolkit/analysis/taxonomy-framework-2026-01-11.md`
- **Overlap Analysis**: `.cattoolkit/analysis/plugin-inventory-2026-01-11.md`
- **Plugin Documentation**: Each plugin's README and SKILL.md files
- **Official Claude Code Docs**: https://code.claude.com/docs/
