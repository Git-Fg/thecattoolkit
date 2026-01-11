# Plugin Tools Inventory & Overlap Analysis
**Date**: 2026-01-11
**Purpose**: Identify overlapping capabilities and design domain/function taxonomy

## Current Plugin Structure

### 1. **sys-core** - Infrastructure & Safety
**Description**: Infrastructure and Safety layer for plugin management, security auditing, Python tooling, and toolkit maintenance

**Tools**:
- **Skills**:
  - `audit-security` - Security code verification (MUST USE)
  - `check-types` - Python type validation (MUST USE)
  - `manage-healing` - Component failure diagnosis (MUST USE)
  - `python-tools` - Python project management (uv, ruff)
  - `scaffold-component` - Plugin component creation (MUST USE)
  - `test-writer` - Vitest test generation (MUST USE)
  - `toolkit-registry` - Plugin component authority (MUST USE)
  - `validate-toolkit` - Plugin validation (MUST USE)

**Domain**: Infrastructure, Safety, Validation, Python Development

---

### 2. **sys-builder** - Action Layer
**Description**: Action layer for execution, architecture design, and project implementation

**Tools**:
- **Skills**:
  - `architecture` - System design (PROACTIVELY USE)
  - `execution-core` - Agent behavior standards (PROACTIVELY USE)
  - `manage-planning` - Project planning (PROACTIVELY USE)
  - `software-engineering` - Code implementation (PROACTIVELY USE)

- **Commands**:
  - `build` - Execute current phase
  - `plan` - Initialize/update project plan

- **Agents**:
  - `designer` - System design architect
  - `director` - Massive-scale orchestrator
  - `worker` - Universal builder worker

**Domain**: Architecture, Planning, Execution, Software Engineering

---

### 3. **sys-cognition** - Brain Layer
**Description**: Brain layer for thinking frameworks, prompt engineering, context management, and cognitive optimization

**Tools**:
- **Skills**:
  - `agent-orchestration` - Multi-agent design (MUST USE)
  - `context-compression` - Token optimization (MUST USE)
  - `context-degradation` - Context failure detection (MUST USE)
  - `context-management` - Session state management (USE)
  - `deep-analysis` - Strategic analysis (USE)
  - `kv-cache` - Cost/latency optimization (MUST USE)
  - `memory-systems` - Persistent memory design (MUST USE)
  - `planning-with-files` - Markdown planning (USE)
  - `prompt-engineering` - AI prompt optimization (USE)
  - `thinking-frameworks` - Structured reasoning (USE)

- **Commands**:
  - `think` - Structured thinking wizard

- **Agents**:
  - `reasoner` - Deep codebase analysis

**Domain**: Cognitive Optimization, Context Engineering, AI Reasoning

---

### 4. **sys-meta** - Meta-build Tools
**Description**: Meta-build tools for plugin creation, auditing, MCP integration, and maintenance

**Tools**:
- **Skills**:
  - `meta-hooks` - Hook development guidance
  - `meta-mcp` - MCP database integration

- **Agents**:
  - `plugin-expert` - Agent Skills framework compliance

**Domain**: Plugin Development, Hooks, MCP, Meta-programming

---

### 5. **sys-research** - Research Layer
**Description**: Deep research, knowledge retrieval, and experimental analysis capabilities

**Tools**:
- **Skills**:
  - `alphafold-database` - Protein structure database
  - `scientific-slides` - Research presentation creation
  - `researcher` - Research protocol implementation

- **Commands**:
  - `deep-research` - Technical research playbook

**Domain**: Scientific Research, Knowledge Retrieval, Documentation

---

### 6. **sys-multimodal** - Media Processing
**Description**: Multimodal AI for video editing and media processing

**Tools**:
- **Skills**:
  - `intent-translation` - Intent to editing commands
  - `canvas-design` - Design system
  - `multimodal-understanding` - Video/audio analysis

- **Commands**:
  - `edit-video` - Video editing shortcut

- **Agents**:
  - `video-editor` - Autonomous video editing

**Domain**: Video Editing, Media Processing, Multimodal AI

---

### 7. **sys-edge** - Edge & Mobile
**Description**: Edge AI and mobile optimization for resource-constrained environments

**Tools**:
- **Skills**:
  - `edge-ai-management` - Mobile AI model management
  - `gitingest` - Git repository analysis
  - `mobile-optimization` - Mobile AI optimization
  - `offline-sync` - Offline-first sync

- **Commands**:
  - `ingest` - Git repository ingestion
  - `py` - Python environment shortcut

**Domain**: Edge Computing, Mobile AI, Repository Analysis

---

### 8. **business-analytics** - Business Intelligence
**Description**: Business Analytics - Data visualization, storytelling, and business intelligence capabilities

**Tools**:
- **Skills**:
  - `data-storytelling` - Data narrative transformation

**Domain**: Data Visualization, Business Intelligence, Analytics

---

### 9. **llm-application-dev** - LLM Applications
**Description**: LLM Application Development - RAG systems, hybrid search, vector databases, and LLM application patterns

**Tools**:
- **Skills**:
  - `hybrid-search-implementation` - Hybrid search systems

**Domain**: LLM Applications, RAG, Vector Search

---

## OVERLAP ANALYSIS

### **1. Code Analysis & Repository Understanding**
- **`sys-cognition:reasoner`** - Deep codebase analysis
- **`sys-edge:gitingest`** - Git repository analysis
- **`sys-edge:ingest`** (command) - Git repository ingestion

**Overlap**: Multiple tools for analyzing codebases/repositories
**Problem**: Users confused about which to use

### **2. System Architecture & Design**
- **`sys-builder:architecture`** - System design
- **`sys-builder:designer`** - System design architect
- **`sys-cognition:agent-orchestration`** - Multi-agent system design

**Overlap**: Architecture design capabilities
**Problem**: Unclear boundaries between system architecture and agent orchestration

### **3. Planning & Project Management**
- **`sys-builder:manage-planning`** - Project planning
- **`sys-cognition:planning-with-files`** - Markdown planning
- **`sys-builder:plan`** (command) - Project plan initialization
- **`sys-builder:build`** (command) - Execute current phase

**Overlap**: Multiple planning tools
**Problem**: Different types of planning not clearly distinguished

### **4. Security & Validation**
- **`sys-core:audit-security`** - Security auditing
- **`sys-core:validate-toolkit`** - Plugin validation
- **`sys-core:check-types`** - Type safety validation

**Overlap**: Validation and security checks
**Problem**: Different validation types not categorized

### **5. Plugin Development & Meta-programming**
- **`sys-core:scaffold-component`** - Plugin component creation
- **`sys-core:toolkit-registry`** - Plugin management
- **`sys-meta:meta-hooks`** - Hook development
- **`sys-meta:meta-mcp`** - MCP integration
- **`sys-meta:plugin-expert`** - Agent Skills compliance

**Overlap**: Plugin development tools
**Problem**: Meta-level vs core plugin tools unclear

### **6. Python Development**
- **`sys-core:python-tools`** - Python project management
- **`sys-edge:py`** (command) - Python environment shortcut

**Overlap**: Python tooling
**Problem**: Command vs skill distinction unclear

### **7. Context & Memory Management**
- **`sys-cognition:context-compression`** - Token optimization
- **`sys-cognition:context-degradation`** - Context failure detection
- **`sys-cognition:context-management`** - Session state
- **`sys-cognition:kv-cache`** - Cache optimization
- **`sys-cognition:memory-systems`** - Persistent memory

**Overlap**: Context/memory optimization
**Problem**: Different aspects of context not clearly separated

## ROOT CAUSE OF OVERLAPS

1. **Lack of Clear Domain Boundaries**: Tools span multiple domains without clear categorization
2. **Plugin-Centric Organization**: Tools organized by plugin rather than function
3. **No Unified Taxonomy**: No standardized way to classify tools by domain
4. **Command/Skill Ambiguity**: Shortcuts and full capabilities overlap
5. **Multi-Purpose Tools**: Some tools serve multiple domains (e.g., `gitingest` for both edge AI and research)

## RECOMMENDATION

Create a **Domain/Function Taxonomy** that:
1. Groups tools by primary domain (Infrastructure, Development, AI/ML, etc.)
2. Sub-categorizes by function within domain
3. Provides clear naming conventions
4. Defines boundaries between overlapping tools
5. Maps tools to user intent scenarios
