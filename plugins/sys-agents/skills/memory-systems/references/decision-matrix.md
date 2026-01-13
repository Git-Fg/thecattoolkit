# Architecture Selection Guide

## Decision Matrix

| Use Case | Vector RAG | GraphRAG | Temporal KG |
|----------|-----------|----------|-------------|
| **Document Search** | ✅ Best | ⚠️ Overkill | ❌ Unnecessary |
| **Q&A Systems** | ✅ Good | ✅ Better | ⚠️ Complex |
| **Entity Relationships** | ❌ No | ✅ Yes | ✅ Yes |
| **Multi-hop Reasoning** | ❌ Limited | ✅ Yes | ✅ Yes |
| **Time-sensitive** | ❌ No | ⚠️ Limited | ✅ Best |
| **Simple Implementation** | ✅ Easy | ⚠️ Medium | ❌ Hard |

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
