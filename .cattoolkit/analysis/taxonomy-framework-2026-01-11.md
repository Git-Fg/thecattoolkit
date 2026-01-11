# Domain/Function Taxonomy Framework
**Date**: 2026-01-11
**Purpose**: Organize tools by domain and function for clarity

---

## TAXONOMY STRUCTURE

### **DOMAIN 1: INFRASTRUCTURE & SYSTEM**
*Tools for system stability, security, and infrastructure management*

#### **Subdomain 1.1: Security & Safety**
- `sys-core:audit-security` - Security code verification
- `sys-core:check-types` - Type safety validation

#### **Subdomain 1.2: Validation & Quality**
- `sys-core:validate-toolkit` - Plugin validation
- `sys-core:manage-healing` - Component failure diagnosis
- `sys-core:test-writer` - Test generation

#### **Subdomain 1.3: Plugin Management**
- `sys-core:scaffold-component` - Component scaffolding
- `sys-core:toolkit-registry` - Plugin registry authority
- `sys-meta:meta-hooks` - Hook development
- `sys-meta:meta-mcp` - MCP integration
- `sys-meta:plugin-expert` - Agent Skills compliance

---

### **DOMAIN 2: DEVELOPMENT & ENGINEERING**
*Tools for software development, coding, and technical implementation*

#### **Subdomain 2.1: Code Development**
- `sys-core:python-tools` - Python ecosystem (uv, ruff)
- `sys-builder:software-engineering` - Universal coding standard
- `sys-edge:py` - Python environment shortcut

#### **Subdomain 2.2: Architecture & Design**
- `sys-builder:architecture` - System architecture design
- `sys-builder:designer` - Design architect agent
- `sys-cognition:agent-orchestration` - Multi-agent system design

#### **Subdomain 2.3: Planning & Execution**
- `sys-builder:manage-planning` - Project planning & execution
- `sys-cognition:planning-with-files` - File-based planning
- `sys-builder:plan` - Project initialization
- `sys-builder:build` - Phase execution

#### **Subdomain 2.4: Repository & Code Analysis**
- `sys-cognition:reasoner` - Deep codebase analysis
- `sys-edge:gitingest` - Git repository ingestion
- `sys-edge:ingest` - Repository ingestion command

---

### **DOMAIN 3: AI/ML & COGNITIVE**
*Tools for AI model management, optimization, and cognitive engineering*

#### **Subdomain 3.1: Context & Memory**
- `sys-cognition:context-management` - Session state management
- `sys-cognition:context-compression` - Token optimization
- `sys-cognition:context-degradation` - Context failure detection
- `sys-cognition:kv-cache` - Cache optimization
- `sys-cognition:memory-systems` - Persistent memory

#### **Subdomain 3.2: AI Reasoning & Analysis**
- `sys-cognition:deep-analysis` - Strategic analysis
- `sys-cognition:thinking-frameworks` - Structured reasoning
- `sys-cognition:reasoner` - Forensic analysis
- `sys-cognition:think` - Thinking wizard

#### **Subdomain 3.3: Prompt Engineering**
- `sys-cognition:prompt-engineering` - Prompt optimization

#### **Subdomain 3.4: Agent Orchestration**
- `sys-cognition:agent-orchestration` - Multi-agent patterns
- `sys-builder:director` - Massive-scale orchestration
- `sys-builder:worker` - Execution worker

#### **Subdomain 3.5: Edge & Mobile AI**
- `sys-edge:edge-ai-management` - Mobile AI models
- `sys-edge:mobile-optimization` - Mobile optimization
- `sys-edge:offline-sync` - Offline-first sync

---

### **DOMAIN 4: RESEARCH & KNOWLEDGE**
*Tools for research, documentation, and knowledge management*

#### **Subdomain 4.1: Scientific Research**
- `sys-research:alphafold-database` - Protein structures
- `sys-research:scientific-slides` - Research presentations
- `sys-research:researcher` - Research protocols
- `sys-research:deep-research` - Research playbook

#### **Subdomain 4.2: Business Intelligence**
- `business-analytics:data-storytelling` - Data narratives

#### **Subdomain 4.3: LLM Applications**
- `llm-application-dev:hybrid-search-implementation` - Hybrid search
- `sys-cognition:prompt-engineering` - Prompt systems

---

### **DOMAIN 5: MEDIA & MULTIMODAL**
*Tools for media processing, video editing, and multimodal AI*

#### **Subdomain 5.1: Video Editing**
- `sys-multimodal:video-editor` - Autonomous editing
- `sys-multimodal:edit-video` - Editing command
- `sys-multimodal:intent-translation` - Intent to commands

#### **Subdomain 5.2: Media Understanding**
- `sys-multimodal:multimodal-understanding` - Video/audio analysis
- `sys-multimodal:canvas-design` - Design systems

---

## NAMING CONVENTIONS

### **Skill Naming Pattern**
```
[domain]-[subdomain]-[function]
```

**Examples**:
- `infra-security-audit` instead of `audit-security`
- `dev-code-python` instead of `python-tools`
- `ai-context-compression` instead of `context-compression`
- `research-data-storytelling` instead of `data-storytelling`

### **Command Naming Pattern**
```
[domain]:[action]
```

**Examples**:
- `dev:plan` instead of `plan`
- `dev:build` instead of `build`
- `ai:think` instead of `think`
- `research:deep-research` instead of `deep-research`

### **Agent Naming Pattern**
```
[domain]-[role]
```

**Examples**:
- `dev-designer` instead of `designer`
- `dev-worker` instead of `worker`
- `ai-reasoner` instead of `reasoner`

---

## BOUNDARY DEFINITIONS

### **1. Repository Analysis**
| Tool | Primary Use | Secondary Use | Decision Rule |
|:-----|:------------|:---------------|:--------------|
| `sys-cognition:reasoner` | Deep codebase analysis | Strategic insights | Use when analyzing existing systems |
| `sys-edge:gitingest` | Repository ingestion for AI | Quick summaries | Use when preparing repos for AI consumption |
| `sys-edge:ingest` | Command wrapper | N/A | Use for quick ingestion tasks |

### **2. Architecture Design**
| Tool | Primary Use | Secondary Use | Decision Rule |
|:-----|:------------|:---------------|:--------------|
| `sys-builder:architecture` | System architecture | Design patterns | Use for overall system design |
| `sys-builder:designer` | Architecture agent | N/A | Use when needing design consultation |
| `sys-cognition:agent-orchestration` | Multi-agent patterns | Agent design | Use specifically for multi-agent systems |

### **3. Planning**
| Tool | Primary Use | Secondary Use | Decision Rule |
|:-----|:------------|:---------------|:--------------|
| `sys-builder:manage-planning` | Project management | Execution tracking | Use for project-level planning |
| `sys-cognition:planning-with-files` | Markdown workflows | Persistent state | Use for structured, file-based planning |
| `sys-builder:plan` | Quick initialization | N/A | Use for simple project setup |

### **4. Python Development**
| Tool | Primary Use | Secondary Use | Decision Rule |
|:-----|:------------|:---------------|:--------------|
| `sys-core:python-tools` | Full Python ecosystem | Project management | Use for comprehensive Python development |
| `sys-edge:py` | Quick commands | Environment access | Use for simple Python tasks |

---

## MIGRATION STRATEGY

### **Phase 1: Documentation Update**
1. Update all tool descriptions with domain/subdomain tags
2. Create cross-reference index
3. Update marketplace metadata

### **Phase 2: Skill Renaming** (Optional)
1. Create alias skills with new names
2. Maintain backward compatibility
3. Deprecate old names after transition period

### **Phase 3: Command Organization**
1. Reorganize commands by domain
2. Update help documentation
3. Create domain-specific command groups

---

## USER SCENARIO MAPPING

### **Scenario 1: "I need to audit my code for security"**
**Primary Path**: `sys-core:audit-security` (Security & Safety domain)
**Alternative**: `sys-core:check-types` (Type validation)

### **Scenario 2: "I want to design a new system"**
**Primary Path**: `sys-builder:architecture` (Architecture & Design domain)
**Alternative**: `sys-builder:designer` (Design consultation)

### **Scenario 3: "I need to plan a project"**
**Primary Path**: `sys-builder:manage-planning` (Planning & Execution domain)
**Alternative**: `sys-cognition:planning-with-files` (File-based workflows)

### **Scenario 4: "I want to analyze a codebase"**
**Primary Path**: `sys-cognition:reasoner` (AI Reasoning domain)
**Alternative**: `sys-edge:gitingest` (Repository analysis)

### **Scenario 5: "I need to optimize AI context usage"**
**Primary Path**: `sys-cognition:context-compression` (Context & Memory domain)
**Alternatives**: `sys-cognition:kv-cache`, `sys-cognition:memory-systems`

---

## TAXONOMY BENEFITS

1. **Clear Boundaries**: Each tool has a defined domain and subdomain
2. **Predictable Organization**: Users can find tools by domain
3. **Reduced Confusion**: Overlaps are explicitly mapped with decision rules
4. **Scalable Structure**: New tools fit into existing taxonomy
5. **User-Friendly**: Matches mental model of tool categories
6. **Plugin Independence**: Tools organized by function, not by plugin
