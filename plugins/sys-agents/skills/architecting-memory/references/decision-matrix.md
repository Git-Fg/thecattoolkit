# Architecture Selection Guide

## Decision Matrix

| Use Case | Vector RAG | GraphRAG | Temporal KG |
|----------|-----------|----------|-------------|
| **Document Search** | GOOD Best | WARNING Overkill | BAD Unnecessary |
| **Q&A Systems** | GOOD Good | GOOD Better | WARNING Complex |
| **Entity Relationships** | BAD No | GOOD Yes | GOOD Yes |
| **Multi-hop Reasoning** | BAD Limited | GOOD Yes | GOOD Yes |
| **Time-sensitive** | BAD No | WARNING Limited | GOOD Best |
| **Simple Implementation** | GOOD Easy | WARNING Medium | BAD Hard |

## Selection Criteria

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
