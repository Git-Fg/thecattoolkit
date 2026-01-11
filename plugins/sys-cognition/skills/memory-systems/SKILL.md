---
name: memory-systems
description: "SHOULD USE when designing persistent memory architectures for AI agent systems. Implements progression from Vector RAG → GraphRAG → Temporal Knowledge Graphs, with CrewAI three-tier approach for short-term, long-term, and entity memory."
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

**Architecture:**
```mermaid
graph TB
    QUERY[\"User Query\"] --> EMB[\"Embed Query<br/>OpenAI/Cohere\"]

    EMB --> SEARCH[\"Vector Search<br/>ChromaDB/Pinecone\"]

    SEARCH --> RETRIEVE[\"Top-K Similar<br/>k=5-10 results\"]

    RETRIEVE --> CONTEXT[\"Add to Context<br/>5-10K tokens\"]

    DOCS[\"Document Store<br/>Raw Text\"] --> INDEX[\"Vector Index<br/>Embeddings\"]

    INDEX --> SEARCH

    style SEARCH fill:#e1f5fe
```

**Implementation Pattern:**
```javascript
// Vector RAG implementation
class VectorRAG {
  constructor() {
    this.vectorStore = new ChromaDB()  // or Pinecone
    this.documentStore = new DocumentStore()
    this.embedder = new OpenAIEmbedder()
  }

  async indexDocument(doc) {
    // 1. Chunk document
    const chunks = this.chunkDocument(doc)

    // 2. Embed chunks
    const embeddings = await this.embedder.embed(chunks)

    // 3. Store in vector DB
    await this.vectorStore.add({
      ids: chunks.map(c => c.id),
      embeddings: embeddings,
      metadatas: chunks.map(c => ({
        source: doc.source,
        chunkIndex: c.index
      }))
    })

    // 4. Store raw text
    await this.documentStore.add(chunks)
  }

  async query(queryText, k = 5) {
    // 1. Embed query
    const queryEmbedding = await this.embedder.embed([queryText])

    // 2. Search vector store
    const results = await this.vectorStore.query({
      queryEmbeddings: queryEmbedding,
      nResults: k
    })

    // 3. Retrieve full documents
    const documents = await this.documentStore.get(results.ids)

    return {
      query: queryText,
      results: documents.map(doc => ({
        text: doc.text,
        source: doc.metadata.source,
        similarity: doc.metadata.similarity
      }))
    }
  }

  chunkDocument(doc, chunkSize = 1000, overlap = 200) {
    // Chunk with overlap for context continuity
    const chunks = []
    let start = 0

    while (start < doc.text.length) {
      const end = Math.min(start + chunkSize, doc.text.length)
      chunks.push({
        id: `${doc.id}-${chunks.length}`,
        text: doc.text.slice(start, end),
        index: chunks.length
      })
      start = end - overlap  // Overlap for continuity
    }

    return chunks
  }
}
```

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

---

### Stage 2: GraphRAG (Relationship Modeling)

**Definition:** Model entities and relationships as knowledge graph, combine with vector search.

**When to Use:**
- Need relationship modeling
- Complex entity interactions
- Multi-hop reasoning required
- Can extract entities and relationships

**Architecture:**
```mermaid
graph TB
    QUERY[\"User Query\"] --> PARSE[\"Entity Extraction<br/>LLM-based\"]

    PARSE --> EXPAND[\"Expand to Subgraph<br/>Graph traversal\"]

    EXPAND --> CONTEXT[\"Subgraph → Context<br/>Entities + Relations\"]

    DOCS[\"Documents\"] --> EXTRACT[\"Extract Triples<br/>(Entity, Relation, Entity)\"]

    EXTRACT --> GRAPH[\"Knowledge Graph<br/>Neo4j/NetworkX\"]

    GRAPH --> INDEX[\"Vector Index<br/>Node embeddings\"]

    INDEX --> SEARCH[\"Graph + Vector Search<br/>Hybrid retrieval\"]

    SEARCH --> RETRIEVE[\"Subgraph + Documents<br/>Structured context\"]

    style GRAPH fill:#f3e5f5
```

**Implementation Pattern:**
```javascript
// GraphRAG implementation
class GraphRAG {
  constructor() {
    this.graph = new Neo4jGraph()  // or NetworkX
    this.vectorStore = new ChromaDB()
    this.entityExtractor = new EntityExtractor()
  }

  async indexDocument(doc) {
    // 1. Extract entities and relationships
    const triples = await this.entityExtractor.extractTriples(doc.text)

    // 2. Store in knowledge graph
    await this.graph.addTriples(triples)

    // 3. Create embeddings for nodes
    const nodes = await this.extractNodes(triples)
    const embeddings = await this.embedder.embed(nodes)

    // 4. Index in vector store with graph context
    await this.vectorStore.add({
      ids: nodes.map(n => n.id),
      embeddings: embeddings,
      metadatas: nodes.map(n => ({
        graphId: n.id,
        type: n.type,
        neighbors: n.neighbors
      }))
    })
  }

  async query(queryText) {
    // 1. Extract query entities
    const queryEntities = await this.entityExtractor.extractEntities(queryText)

    // 2. Expand to subgraph
    const subgraph = await this.graph.expandSubgraph(queryEntities, depth = 2)

    // 3. Convert to context
    const context = this.subgraphToContext(subgraph)

    return {
      query: queryText,
      entities: queryEntities,
      subgraph: {
        nodes: subgraph.nodes,
        edges: subgraph.edges
      },
      context: context
    }
  }

  subgraphToContext(subgraph) {
    // Convert graph structure to narrative context
    const lines = []

    lines.push("Entities and relationships:")
    subgraph.edges.forEach(edge => {
      lines.push(`- ${edge.from} ${edge.relation} ${edge.to}`)
    })

    return lines.join('\n')
  }
}
```

**Benefits:**
- Models relationships explicitly
- Enables multi-hop reasoning
- Preserves entity identity
- Better for complex queries

**Limitations:**
- More complex to implement
- Requires entity extraction
- Higher setup cost
- Needs graph database

---

### Stage 3: Temporal Knowledge Graphs (Time-Sensitive)

**Definition:** Knowledge graph with temporal dimension, tracking facts and their validity over time.

**When to Use:**
- Time-sensitive information
- Tracking changes over time
- Version control for facts
- Audit trail requirements
- Evolving knowledge bases

**Architecture:**
```mermaid
graph TB
    TIME[\"Time Dimension<br/>Start/End validity<br/>Confidence scores\"]

    GRAPH[\"Temporal Graph<br/>Neo4j with time\"]

    INDEX[\"Vector + Time Index<br/>Spatial-temporal\"]

    QUERY[\"Query with Time Filter\"] --> TEMPORAL[\"Time-aware retrieval<br/>Filter by validity\"]

    TEMPORAL --> CONTEXT[\"Historical context<br/>Evolution tracking\"]

    INSERT[\"Insert fact\"] --> TRACK[\"Track changes<br/>No overwrite, new node\"]

    TRACK --> HISTORY[\"Full history preserved<br/>No information loss\"]

    style GRAPH fill:#fff3e0
```

**Implementation Pattern:**
```javascript
// Temporal Knowledge Graph
class TemporalKnowledgeGraph {
  constructor() {
    this.graph = new Neo4jGraph()
    this.vectorStore = new ChromaDB()
  }

  async insertFact(subject, relation, object, timestamp, confidence = 1.0) {
    // Create temporal node with validity period
    const factNode = {
      subject: subject,
      relation: relation,
      object: object,
      validFrom: timestamp,
      validTo: null,  // null = currently valid
      confidence: confidence,
      insertedAt: new Date()
    }

    await this.graph.addTemporalFact(factNode)

    // Also index in vector store with temporal metadata
    await this.vectorStore.add({
      ids: [this.generateFactId(factNode)],
      embeddings: await this.embedder.embed([`${subject} ${relation} ${object}`]),
      metadatas: [{
        temporal: true,
        validFrom: timestamp,
        validTo: null,
        confidence: confidence
      }]
    })
  }

  async updateFact(factId, newObject, timestamp) {
    // 1. Mark old fact as invalid
    await this.graph.endFact(factId, timestamp)

    // 2. Create new fact
    const oldFact = await this.graph.getFact(factId)
    const newFact = {
      subject: oldFact.subject,
      relation: oldFact.relation,
      object: newObject,
      validFrom: timestamp,
      validTo: null,
      confidence: oldFact.confidence,
      replaces: factId
    }

    await this.graph.addTemporalFact(newFact)

    return newFact
  }

  async query(queryText, timeFilter = null) {
    // 1. Extract entities from query
    const entities = await this.entityExtractor.extractEntities(queryText)

    // 2. Query graph with temporal constraints
    const subgraph = await this.graph.queryTemporal(entities, timeFilter)

    // 3. Filter by validity
    const validFacts = this.filterByValidity(subgraph, timeFilter)

    return {
      query: queryText,
      timeFilter: timeFilter,
      facts: validFacts.map(f => ({
        subject: f.subject,
        relation: f.relation,
        object: f.object,
        validity: {
          from: f.validFrom,
          to: f.validTo,
          confidence: f.confidence
        }
      }))
    }
  }
}
```

**Benefits:**
- Tracks evolution of knowledge
- No information loss
- Audit trail built-in
- Handles conflicting information

**Limitations:**
- Most complex to implement
- Higher storage requirements
- Complex query patterns
- Requires temporal reasoning

---

## CrewAI Three-Tier Memory Architecture

### Tier 1: Short-Term Memory (Session Context)

**Implementation:**
```javascript
class ShortTermMemory {
  constructor() {
    this.context = new ContextWindow(50000)  // Current session
    this.rag = new VectorRAG()              // Session knowledge
  }

  add(message) {
    // Add to current context
    this.context.add(message)

    // If context getting full, move to RAG
    if (this.context.utilization() > 0.8) {
      this.rag.add(this.context.compress())
      this.context.clear()
    }
  }

  recall(query) {
    // Search recent context first
    const recentResults = this.context.search(query)

    // Then search session RAG
    const ragResults = this.rag.query(query)

    return {
      recent: recentResults,
      session: ragResults
    }
  }
}
```

**Purpose:** Maintain conversation continuity and immediate context.

---

### Tier 2: Long-Term Memory (Cross-Session)

**Implementation:**
```javascript
class LongTermMemory {
  constructor() {
    this.db = new SQLite()  // Simple persistent storage
    this.rag = new GraphRAG()  // Cross-session knowledge
  }

  async store(conversationSummary) {
    // Store in SQLite for persistence
    await this.db.insert({
      timestamp: Date.now(),
      summary: conversationSummary,
      topics: this.extractTopics(conversationSummary)
    })

    // Index in RAG for retrieval
    await this.rag.indexDocument({
      text: conversationSummary,
      source: `session-${this.sessionId}`
    })
  }

  async recall(query) {
    // Query SQLite for relevant sessions
    const sessions = await this.db.query(`
      SELECT * FROM conversations
      WHERE topics MATCH ?
      ORDER BY timestamp DESC
      LIMIT 10
    `, [query])

    // Query RAG for semantic matches
    const ragResults = await this.rag.query(query)

    return {
      sessions: sessions,
      knowledge: ragResults
    }
  }
}
```

**Purpose:** Maintain knowledge across sessions and user interactions.

---

### Tier 3: Entity Memory (Consistency)

**Implementation:**
```javascript
class EntityMemory {
  constructor() {
    this.entities = new Map()  // Entity name → properties
    this.graph = new GraphRAG()  // Entity relationships
  }

  async rememberEntity(name, properties) {
    const existing = this.entities.get(name)

    if (existing) {
      // Update existing entity
      this.entities.set(name, {
        ...existing,
        ...properties,
        lastSeen: Date.now(),
        consistency: this.checkConsistency(existing, properties)
      })
    } else {
      // New entity
      this.entities.set(name, {
        ...properties,
        firstSeen: Date.now(),
        lastSeen: Date.now()
      })
    }

    // Update relationships
    await this.graph.updateEntityRelationships(name, properties)
  }

  async getEntity(name) {
    return this.entities.get(name)
  }

  async findSimilarEntities(query) {
    return this.graph.similaritySearch(query, limit = 5)
  }
}
```

**Purpose:** Track people, places, concepts for consistency across conversations.

---

## Memory Architecture Decision Tree

```mermaid
graph TD
    Start[\"Memory Requirements Analysis\"] --> Q1{\"Need persistence<br/>across sessions?\"}

    Q1 -->|No| Session[\"Short-Term Memory Only<br/>In-memory context\"]
    Q1 -->|Yes| Q2{\"Complex relationships<br/>between entities?\"}

    Q2 -->|No| RAG[\"Vector RAG<br/>Semantic retrieval\"]

    Q2 -->|Yes| Q3{\"Time-sensitive<br/>information?\"}

    Q3 -->|No| GraphRAG[\"GraphRAG<br/>Relationship modeling\"]

    Q3 -->|Yes| Temporal[\"Temporal Knowledge Graph<br/>Time-aware facts\"]
```

**Architecture Comparison:**

| Feature | Vector RAG | GraphRAG | Temporal Graph |
|---------|------------|----------|----------------|
| **Setup complexity** | Low | Medium | High |
| **Storage requirements** | Low | Medium | High |
| **Relationship modeling** | None | Good | Excellent |
| **Temporal tracking** | No | Partial | Yes |
| **Multi-hop reasoning** | No | Yes | Yes |
| **Use case fit** | Document search | Entity relationships | Time evolution |

---

## Implementation Best Practices

### 1. Progressive Enhancement

**Start Simple, Add Complexity:**
```javascript
// Start with Vector RAG
const memory = new VectorRAG()

// Upgrade to GraphRAG when relationships needed
// memory = new GraphRAG(memory)

// Upgrade to Temporal when time becomes important
// memory = new TemporalKnowledgeGraph(memory)
```

### 2. Chunking Strategy

**Overlap for Continuity:**
```javascript
function chunkWithOverlap(text, chunkSize = 1000, overlap = 200) {
  const chunks = []
  for (let i = 0; i < text.length; i += chunkSize - overlap) {
    chunks.push(text.slice(i, i + chunkSize))
  }
  return chunks
}
```

### 3. Retrieval Pipeline

**Multi-stage retrieval:**
```javascript
async function retrieve(memory, query) {
  // Stage 1: Short-term memory (fastest)
  const shortTerm = await memory.shortTerm.recall(query)

  // Stage 2: Vector search
  const semantic = await memory.vectorSearch(query)

  // Stage 3: Graph traversal (if needed)
  const relational = await memory.graphSearch(query)

  // Stage 4: Temporal filtering (if needed)
  const temporal = memory.filterByTime(relational)

  return {
    immediate: shortTerm,
    relevant: semantic,
    related: relational,
    historical: temporal
  }
}
```

### 4. Evaluation Metrics

| Metric | Measurement | Target |
|--------|-------------|---------|
| **Retrieval Precision** | % of retrieved docs relevant | >80% |
| **Retrieval Recall** | % of relevant docs retrieved | >70% |
| **Response Time** | Query → Context time | <2s |
| **Memory Efficiency** | Tokens retrieved / Total | >0.5 |
| **Consistency** | Entity properties match | >95% |

---

## Integration with Cat Toolkit Skills

This skill integrates with:

- **context-compression** - Compresses long-term memories
- **context-degradation-detection** - Monitors memory retrieval quality
- **multi-agent-orchestration** - Shared memory across agents
- **kv-cache-optimization** - Cache frequent memory lookups

---

## Usage Instructions

When invoked, this skill will:

1. **Assess memory requirements** based on use case
2. **Recommend appropriate architecture** (RAG → GraphRAG → Temporal)
3. **Provide implementation patterns** with code examples
4. **Configure CrewAI three-tier memory** (short/long/entity)
5. **Set up evaluation pipeline** for retrieval quality

**Example Activation:**
```
User: "My agent needs to remember user preferences across sessions"

Skill Response:
→ Recommended: CrewAI Three-Tier Memory
→ Short-term: Session context in vector store
→ Long-term: SQLite + GraphRAG for cross-session
→ Entity: Track user properties for consistency
→ Implementation: 3 classes (ShortTermMemory, LongTermMemory, EntityMemory)
→ Expected: 95% consistency, <2s retrieval time
```

**Remember:** Start with Vector RAG for simplicity, upgrade to GraphRAG when relationships matter, add temporal dimension only when time evolution is critical. The three-tier approach (short/long/entity) provides comprehensive memory coverage for most production agent systems.
