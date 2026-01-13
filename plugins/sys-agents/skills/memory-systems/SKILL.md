---
name: memory-systems
description: "Implements progression from Vector RAG → GraphRAG → Temporal Knowledge Graphs, with CrewAI three-tier approach for short-term, long-term, and entity memory. Use when designing persistent memory architectures for AI agent systems."
user-invocable: true
allowed-tools: [Read, Write, Bash, Grep, Glob]
---

# Memory Systems for AI Agents

You are a **Memory Architecture Specialist** focused on designing persistent memory systems for AI agent systems. Your expertise lies in implementing the right memory architecture for each use case: Vector RAG for semantic retrieval, GraphRAG for relationship modeling, and Temporal Knowledge Graphs for time-sensitive information.

## Core Capability

Design and implement memory systems that provide persistent, retrievable context for agents across sessions and tasks. Memory systems are essential for agent continuity, knowledge accumulation, and avoiding context window limitations.

## The Memory Architecture Progression

### Stage 1: Vector RAG (Semantic Retrieval)

**Definition:** Store embeddings in vector database for semantic similarity search.

**When to Use:**
- Simple semantic retrieval needs
- Document search and Q&A
- Knowledge base lookup
- Minimal relationship modeling required

**Benefits:**
- Simple to implement
- Fast semantic search
- Good for document retrieval
- Well-supported ecosystem

**Limitations:**
- No relationship modeling
- Loses document structure
- No temporal awareness
- Cannot model complex dependencies

**See:** `references/vector-rag.md` for complete implementation guide

### Stage 2: GraphRAG (Relationship Modeling)

**Definition:** Model entities and relationships as knowledge graph, combine with vector search.

**When to Use:**
- Need relationship modeling
- Complex entity interactions
- Multi-hop reasoning required
- Can extract entities and relationships

**Benefits:**
- Models entity relationships
- Enables multi-hop reasoning
- Preserves document structure
- Better for complex queries

**Limitations:**
- More complex to implement
- Requires entity extraction
- Graph traversal overhead
- Maintenance overhead

**See:** `references/graph-rag.md` for complete implementation guide

### Stage 3: Temporal Knowledge Graphs (Time-Aware)

**Definition:** Extend knowledge graphs with temporal dimensions for time-sensitive reasoning.

**When to Use:**
- Time-dependent information
- Event sequences
- Historical tracking
- Predictive modeling

**Benefits:**
- Temporal reasoning
- Event sequence modeling
- Historical context
- Predictive capabilities

**Limitations:**
- Most complex to implement
- Requires temporal data
- Complex queries
- Higher storage costs

**See:** `references/temporal-kg.md` for complete implementation guide

## Architecture Selection Guide

### Decision Matrix

| Use Case | Vector RAG | GraphRAG | Temporal KG |
|----------|-----------|----------|-------------|
| **Document Search** | ✅ Best | ⚠️ Overkill | ❌ Unnecessary |
| **Q&A Systems** | ✅ Good | ✅ Better | ⚠️ Complex |
| **Entity Relationships** | ❌ No | ✅ Yes | ✅ Yes |
| **Multi-hop Reasoning** | ❌ Limited | ✅ Yes | ✅ Yes |
| **Time-sensitive** | ❌ No | ⚠️ Limited | ✅ Best |
| **Simple Implementation** | ✅ Easy | ⚠️ Medium | ❌ Hard |

### Selection Criteria

**Choose Vector RAG when:**
- Primary need is semantic search
- Simple document retrieval
- Minimal relationship requirements
- Quick implementation needed

**Choose GraphRAG when:**
- Need to model relationships
- Multi-hop reasoning required
- Entity extraction is feasible
- Complex queries anticipated

**Choose Temporal KG when:**
- Time is critical dimension
- Event sequences matter
- Historical analysis needed
- Predictive modeling required

## CrewAI Three-Tier Memory Approach

### Short-Term Memory
- **Purpose:** Current conversation context
- **Duration:** Session lifetime
- **Storage:** In-memory
- **Access:** Immediate
- **Use:** Active reasoning, immediate context

### Long-Term Memory
- **Purpose:** Persistent knowledge
- **Duration:** Permanent
- **Storage:** Vector DB + Graph
- **Access:** Retrieval-based
- **Use:** Knowledge accumulation, learning

### Entity Memory
- **Purpose:** Entity profiles and relationships
- **Duration:** Persistent
- **Storage:** Knowledge graph
- **Access:** Graph traversal
- **Use:** Entity understanding, relationship mapping

**See:** `references/crewai-approach.md` for implementation details

## Implementation Patterns

### Pattern 1: Progressive Enhancement
Start with Vector RAG, add GraphRAG when needed:
```
Vector RAG → Vector RAG + Entity Extraction → GraphRAG → Temporal KG
```

**Benefits:**
- Incremental complexity
- Early value delivery
- Gradual sophistication
- Learning curve management

### Pattern 2: Hybrid Architecture
Combine multiple approaches:
```
Vector Search ←→ Knowledge Graph ←→ Temporal Layer
       ↓              ↓              ↓
   Semantic      Relationships    Time-based
```

**Benefits:**
- Best of all worlds
- Flexible querying
- Comprehensive coverage
- Future-proof

## Common Architectures

### Architecture 1: Simple Q&A
**Stack:** Vector RAG + LLM
**Use:** Document Q&A, FAQ systems
**Complexity:** Low

### Architecture 2: Entity-Centric
**Stack:** Vector RAG + Entity Extraction + Graph
**Use:** Research, analysis, relationship discovery
**Complexity:** Medium

### Architecture 3: Temporal Analytics
**Stack:** Full Temporal KG
**Use:** Event tracking, predictive analytics, history analysis
**Complexity:** High

**See:** `references/architectures.md` for detailed architecture patterns

## Technology Stack Options

### Vector Databases
- **ChromaDB** - Open source, Python/JavaScript
- **Pinecone** - Managed, scalable
- **Weaviate** - Open source with GraphQL
- **Pgvector** - PostgreSQL extension

### Knowledge Graphs
- **Neo4j** - Graph database
- **Amazon Neptune** - Managed graph DB
- **ArangoDB** - Multi-model database
- **NetworkX** - Python graph library

### Embedding Models
- **OpenAI** - text-embedding-ada-002
- **Cohere** - embed-multilingual
- **Hugging Face** - Sentence transformers
- **Local models** - all-MiniLM-L6-v2

**See:** `references/tech-stack.md` for technology comparison

## Best Practices

### Do's

✅ **Start Simple**
- Begin with Vector RAG
- Add complexity incrementally
- Prove value at each stage

✅ **Design for Evolution**
- Choose extensible architectures
- Plan for relationship modeling
- Consider temporal needs

✅ **Validate Retrieval**
- Test retrieval quality
- Measure relevance
- A/B test approaches

✅ **Monitor Performance**
- Track retrieval latency
- Measure accuracy
- Monitor resource usage

### Don'ts

❌ **Don't Over-Engineer**
- Don't start with Temporal KG if Vector RAG suffices
- Avoid premature optimization
- Don't model relationships you don't need

❌ **Don't Ignore Scale**
- Consider data volume
- Plan for query performance
- Budget for storage costs

❌ **Don't Skip Evaluation**
- Test retrieval quality
- Measure against baselines
- Validate user value

## Reference Materials

**Core Implementation:**
- `references/vector-rag.md` - Vector RAG complete guide
- `references/graph-rag.md` - GraphRAG implementation
- `references/temporal-kg.md` - Temporal knowledge graphs
- `references/crewai-approach.md` - Three-tier memory system

**Architecture Patterns:**
- `references/architectures.md` - Common architectures
- `references/patterns.md` - Design patterns
- `references/tech-stack.md` - Technology stack options

**Examples:**
- `examples/vector-rag/` - Vector RAG implementation
- `examples/graph-rag/` - GraphRAG example
- `examples/temporal-kg/` - Temporal KG demo
- `examples/crewai-memory/` - CrewAI memory system

## Next Steps

1. **Assess Requirements**
   - What type of information?
   - Relationship complexity?
   - Temporal sensitivity?

2. **Choose Architecture**
   - Start simple (Vector RAG)
   - Plan for evolution
   - Select technology stack

3. **Implement Incrementally**
   - Build MVP
   - Test and validate
   - Add features gradually

4. **Evaluate and Iterate**
   - Measure retrieval quality
   - Monitor performance
   - Optimize based on data

5. **Scale as Needed**
   - Add relationships (GraphRAG)
   - Add temporal dimension (Temporal KG)
   - Optimize for production
