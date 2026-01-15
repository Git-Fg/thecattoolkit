---
name: architecting-memory
description: "Implements progression from Vector RAG → GraphRAG → Temporal Knowledge Graphs. Use when designing persistent memory architectures for AI agent systems."
user-invocable: true
allowed-tools: [Read, Write, Bash, Grep, Glob]
---

# Memory Systems for AI Agents

You are a **Memory Architecture Specialist**. Your expertise lies in implementing the right memory architecture for each use case.

## Architecture Selection

Start here to choose the right approach.
- **Decision Matrix**: [references/decision-matrix.md](references/decision-matrix.md)
- **Detailed Design Patterns**: [references/patterns.md](references/patterns.md)

## The Core Progression

### Stage 1: Vector RAG (Semantic)
Store embeddings in vector database for semantic similarity search.
- **Guide**: [references/vector-rag.md](references/vector-rag.md)

### Stage 2: GraphRAG (Relational)
Model entities and relationships as knowledge graph.
- **Guide**: [references/graph-rag.md](references/graph-rag.md)

### Stage 3: Temporal KG (Time-Series)
Extend knowledge graphs with temporal dimensions.
- **Guide**: [references/temporal-kg.md](references/temporal-kg.md)

## Specialized Approaches

### CrewAI Memory Model
Three-tier approach (Short-term, Long-term, Entity).
- **Guide**: [references/crewai-approach.md](references/crewai-approach.md)

### Technical Implementation
- **Tech Stack Options**: [references/tech-stack.md](references/tech-stack.md)
- **Common Architectures**: [references/architectures.md](references/architectures.md)
