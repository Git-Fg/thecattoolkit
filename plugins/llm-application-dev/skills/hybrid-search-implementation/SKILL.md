---
name: hybrid-search-implementation
description: "Combines vector and keyword search for improved retrieval. Use when implementing hybrid search systems, building RAG systems, or when neither vector nor keyword approach alone provides sufficient recall."
allowed-tools: [Read, Write, Edit, Bash]
---

# Hybrid Search Implementation

Patterns for combining vector similarity and keyword-based search to achieve superior retrieval performance in LLM applications and RAG systems.

## When to Use This Skill

- Building RAG systems with improved recall and precision
- Combining semantic understanding with exact term matching
- Handling queries with specific terms (names, codes, technical jargon)
- Improving search for domain-specific vocabulary and proper nouns
- When pure vector search misses important keyword matches
- Implementing production-grade search with multiple retrieval methods

## Core Concepts

### 1. Hybrid Search Architecture

```
Query → ┬─► Vector Search ──► Candidates ─┐
        │                                  │
        └─► Keyword Search ─► Candidates ─┴─► Fusion ─► Results
```

**Why Hybrid Search?**
- **Vector search** excels at semantic similarity but may miss exact matches
- **Keyword search** finds exact terms but lacks semantic understanding
- **Hybrid approach** combines both strengths for comprehensive retrieval

### 2. Fusion Methods

| Method | Description | Best For |
|--------|-------------|----------|
| **RRF** | Reciprocal Rank Fusion | General purpose, no tuning required |
| **Linear** | Weighted sum of scores | Tunable balance between approaches |
| **Cross-encoder** | Rerank with neural model | Highest quality results |
| **Cascade** | Filter then rerank | Efficiency with quality |

### 3. Implementation Patterns

**RRF (Reciprocal Rank Fusion):**
- Combines ranked lists from multiple search methods
- No parameters to tune (uses fixed constant k=60)
- Works well in most scenarios
- Simple and effective baseline

**Linear Combination:**
- Interpolates between vector and keyword scores
- Requires weight tuning (alpha parameter)
- More control over balance
- Good for specific use cases

**Cross-Encoder Reranking:**
- Uses neural model to rerank candidates
- Highest quality results
- More computational overhead
- Best for final quality refinement

## Quick Templates

### RRF Implementation (Basic)
```python
from typing import List, Dict, Tuple
from collections import defaultdict

def reciprocal_rank_fusion(
    result_lists: List[List[Tuple[str, float]]],
    k: int = 60,
    weights: List[float] = None
) -> List[Tuple[str, float]]:
    """Combine multiple ranked lists using RRF."""
    if weights is None:
        weights = [1.0] * len(result_lists)

    scores = defaultdict(float)

    for result_list, weight in zip(result_lists, weights):
        for rank, (doc_id, _) in enumerate(result_list):
            scores[doc_id] += weight * (1.0 / (k + rank + 1))

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### Linear Combination (Basic)
```python
def linear_combination(
    vector_results: List[Tuple[str, float]],
    keyword_results: List[Tuple[str, float]],
    alpha: float = 0.5
) -> List[Tuple[str, float]]:
    """Combine results with linear interpolation."""
    all_docs = set(doc_id for doc_id, _ in vector_results) | \
                set(doc_id for doc_id, _ in keyword_results)

    combined = {}
    for doc_id in all_docs:
        v_score = next((score for d, score in vector_results if d == doc_id), 0)
        k_score = next((score for d, score in keyword_results if d == doc_id), 0)
        combined[doc_id] = alpha * v_score + (1 - alpha) * k_score

    return sorted(combined.items(), key=lambda x: x[1], reverse=True)
```

## Platform-Specific Implementations

### PostgreSQL with pgvector
**See:** `references/postgresql-hybrid.md`

Complete implementation using PostgreSQL with pgvector extension, including:
- Schema setup with vector and full-text indexes
- HNSW indexing for fast approximate search
- RRF fusion in SQL
- Cross-encoder reranking integration

### Elasticsearch
**See:** `references/elasticsearch-hybrid.md`

Elasticsearch hybrid search implementation:
- Dense vector indexing
- kNN search configuration
- RRF (Reciprocal Rank Fusion) support
- Custom scoring with multiple queries

### Custom RAG Pipeline
**See:** `references/custom-pipeline.md`

Complete hybrid RAG pipeline:
- Async/await implementation
- Parallel search execution
- Configurable fusion methods
- Reranking integration

## Implementation Examples

### Simple RRF Example
**See:** `examples/simple-rrf.py`

Basic RRF implementation showing:
- Rank fusion algorithm
- Score normalization
- Result merging

### Production Setup
**See:** `examples/production-setup.py`

Production-ready hybrid search system:
- Database initialization
- Document indexing
- Async search execution
- Reranking integration

## Best Practices

### Do's
- **Tune weights empirically** - Test different alpha values on your specific data
- **Use RRF for simplicity** - Works well without parameter tuning
- **Add reranking for quality** - Cross-encoder significantly improves results
- **Log both individual and fused scores** - Helps with debugging and optimization
- **A/B test in production** - Measure real user impact and query performance
- **Use parallel execution** - Run vector and keyword searches concurrently
- **Over-fetch candidates** - Get 3x more results than final count before fusion

### Don'ts
- **Don't assume one size fits all** - Different queries need different weight adjustments
- **Don't skip keyword search** - Essential for names, codes, and exact matches
- **Don't over-fetch excessively** - Balance recall vs latency and costs
- **Don't ignore edge cases** - Handle empty results, single-word queries, special characters
- **Don't forget score normalization** - Vector and keyword scores have different ranges
- **Don't skip monitoring** - Track recall, precision, and latency metrics

### Performance Considerations

**Indexing:**
- Use HNSW for vector indexes (fast approximate search)
- Use GIN/GIST for full-text search
- Consider separate embedding dimensions based on your model

**Query Execution:**
- Fetch 2-3x more candidates than final results
- Use parallel execution for vector and keyword searches
- Cache query embeddings for repeated queries

**Reranking:**
- Only rerank top N candidates (e.g., 50-100)
- Use efficient models (MiniLM, not large BERT)
- Consider CPU vs GPU for reranking throughput

## Common Use Cases

### 1. Legal Document Search
- Hybrid search finds both exact citations and semantically similar cases
- RRF ensures precise legal terms get proper weighting
- Reranking improves relevance for complex legal queries

### 2. Technical Documentation
- Combines API documentation exact matches with conceptual explanations
- Vector search finds similar functions; keyword search finds exact API names
- Essential for developer tools and IDE integration

### 3. E-commerce Product Search
- Keyword search for SKUs, brands, exact product names
- Vector search for visual similarity, related products
- Fusion improves both exact and browse/search experiences

### 4. Customer Support Knowledge Base
- Keyword search for error codes, product names
- Vector search for conceptually similar issues
- Critical for accurate help and support deflection

### 5. Research Paper Discovery
- Keyword search for authors, venues, specific terms
- Vector search for related work and similar methodologies
- Helps researchers find both direct citations and related work

## Evaluation Metrics

### Offline Metrics
- **Recall@K**: Fraction of relevant documents retrieved
- **MRR**: Mean Reciprocal Rank of first relevant result
- **NDCG**: Normalized Discounted Cumulative Gain

### Online Metrics
- **Click-through rate**: User engagement with results
- **Query reformulation rate**: Users changing their query
- **Session success**: Task completion rate

### Hybrid-Specific Metrics
- **Contribution balance**: % results from vector vs keyword search
- **Coverage improvement**: Recall gain from hybrid vs single method
- **Quality lift**: NDCG improvement from reranking

## Reference Materials

**Core Implementation:**
- `references/postgresql-hybrid.md` - PostgreSQL with pgvector
- `references/elasticsearch-hybrid.md` - Elasticsearch implementation
- `references/custom-pipeline.md` - Custom RAG pipeline

**Templates & Examples:**
- `templates/` - Ready-to-use code templates
- `examples/simple-rrf.py` - Basic RRF example
- `examples/production-setup.py` - Production implementation

**Additional Resources:**
- [RRF Original Paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [Vespa Hybrid Search Guide](https://blog.vespa.ai/improving-text-ranking-with-few-shot-prompting/)
- [Cohere Rerank Documentation](https://docs.cohere.com/docs/reranking)
- [Elasticsearch kNN Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html)
- [pgvector Documentation](https://github.com/pgvector/pgvector)

## Next Steps

1. **Choose your platform** - PostgreSQL, Elasticsearch, or custom
2. **Review platform-specific guide** - See references/ directory
3. **Adapt templates** - Modify for your use case
4. **Test with RRF** - Start with simple implementation
5. **Add reranking** - Improve quality with cross-encoder
6. **Tune parameters** - Optimize for your data
7. **Monitor metrics** - Track performance in production
