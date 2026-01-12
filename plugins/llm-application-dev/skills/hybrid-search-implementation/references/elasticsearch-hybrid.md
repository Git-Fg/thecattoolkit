# Elasticsearch Hybrid Search

## Overview

Elasticsearch provides native support for hybrid search through dense vector fields and traditional full-text search, enabling efficient hybrid retrieval in a single query.

## Index Setup

### 1. Create Index with Vector Field

```json
PUT documents
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "knn": {
        "algo_param": {
          "ef_construction": 100,
          "m": 16
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"
      },
      "content": {
        "type": "text"
      },
      "embedding": {
        "type": "dense_vector",
        "dims": 1536,
        "index": true,
        "similarity": "cosine"
      },
      "metadata": {
        "type": "object"
      }
    }
  }
}
```

### 2. Configure kNN Search

```json
PUT documents
{
  "settings": {
    "index": {
      "knn": true,
      "knn.algo_param": {
        "ef_construction": 128,
        "m": 16
      }
    }
  }
}
```

## Indexing Documents

### Bulk Index with Embeddings

```python
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

# Initialize Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample documents
documents = [
    {"id": "1", "content": "Elasticsearch is a distributed search engine"},
    {"id": "2", "content": "PostgreSQL is a relational database"},
    {"id": "3", "content": "MongoDB is a NoSQL database"}
]

# Generate embeddings
for doc in documents:
    embedding = model.encode(doc["content"])
    doc["embedding"] = embedding.tolist()

# Bulk index
operations = []
for doc in documents:
    operations.append({"index": {"_index": "documents", "_id": doc["id"]}})
    operations.append(doc)

es.bulk(operations=operations)
es.indices.refresh(index="documents")
```

## Hybrid Search Queries

### 1. Basic Hybrid Search (Bool Query)

```json
GET documents/_search
{
  "size": 10,
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "content": "search engine"
          }
        },
        {
          "knn": {
            "field": "embedding",
            "query_vector": [0.1, 0.2, ...],
            "k": 50,
            "num_candidates": 100
          }
        }
      ]
    }
  }
}
```

### 2. Hybrid Search with RRF

```python
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def hybrid_search_rrf(query_text: str, query_embedding: list, k: int = 60):
    """Perform RRF hybrid search."""

    # Execute vector search
    vector_results = es.search(
        index="documents",
        knn={
            "field": "embedding",
            "query_vector": query_embedding,
            "k": 50,
            "num_candidates": 100
        },
        size=50
    )

    # Execute keyword search
    keyword_results = es.search(
        index="documents",
        query={
            "match": {
                "content": query_text
            }
        },
        size=50
    )

    # Apply RRF
    scores = {}

    for rank, hit in enumerate(vector_results['hits']['hits']):
        doc_id = hit['_id']
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)

    for rank, hit in enumerate(keyword_results['hits']['hits']):
        doc_id = hit['_id']
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)

    # Sort by RRF score
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Fetch full documents
    doc_ids = [doc_id for doc_id, _ in sorted_docs[:10]]

    results = es.mget(
        index="documents",
        ids=doc_ids
    )

    return results['docs']
```

### 3. Custom Scoring Function

```json
GET documents/_search
{
  "size": 10,
  "query": {
    "function_score": {
      "query": {
        "match": {
          "content": "search engine"
        }
      },
      "functions": [
        {
          "filter": {
            "exists": {
              "field": "embedding"
            }
          },
          "script_score": {
            "script": {
              "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
              "params": {
                "query_vector": [0.1, 0.2, ...]
              }
            }
          }
        }
      ],
      "score_mode": "sum",
      "boost_mode": "sum"
    }
  }
}
```

## Advanced Hybrid Patterns

### 1. RRF with Parallel Execution

```python
import asyncio
from elasticsearch import AsyncElasticsearch

async def async_hybrid_search(
    es: AsyncElasticsearch,
    query_text: str,
    query_embedding: list,
    k: int = 60
):
    """Async hybrid search with RRF."""

    # Execute both searches in parallel
    vector_task = es.search(
        index="documents",
        knn={
            "field": "embedding",
            "query_vector": query_embedding,
            "k": 50,
            "num_candidates": 100
        },
        size=50
    )

    keyword_task = es.search(
        index="documents",
        query={
            "match": {
                "content": query_text
            }
        },
        size=50
    )

    # Wait for both to complete
    vector_results, keyword_results = await asyncio.gather(
        vector_task, keyword_task
    )

    # Apply RRF
    scores = {}

    for rank, hit in enumerate(vector_results['hits']['hits']):
        doc_id = hit['_id']
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)

    for rank, hit in enumerate(keyword_results['hits']['hits']):
        doc_id = hit['_id']
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)

    # Sort and return
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs[:10]
```

### 2. Weighted Linear Combination

```python
def hybrid_search_linear(
    es: Elasticsearch,
    query_text: str,
    query_embedding: list,
    alpha: float = 0.5
):
    """Linear combination of vector and keyword scores."""

    # Get vector search results
    vector_results = es.search(
        index="documents",
        knn={
            "field": "embedding",
            "query_vector": query_embedding,
            "k": 50
        },
        size=50
    )

    # Get keyword search results
    keyword_results = es.search(
        index="documents",
        query={
            "match": {
                "content": query_text
            }
        },
        size=50
    )

    # Normalize scores
    vector_scores = {
        hit['_id']: hit['_score']
        for hit in vector_results['hits']['hits']
    }

    keyword_scores = {
        hit['_id']: hit['_score']
        for hit in keyword_results['hits']['hits']
    }

    # Combine scores
    all_ids = set(vector_scores.keys()) | set(keyword_scores.keys())
    combined_scores = {}

    for doc_id in all_ids:
        v_score = vector_scores.get(doc_id, 0)
        k_score = keyword_scores.get(doc_id, 0)
        combined_scores[doc_id] = alpha * v_score + (1 - alpha) * k_score

    # Sort by combined score
    sorted_docs = sorted(
        combined_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_docs[:10]
```

## Reranking with Cross-Encoder

### 1. Fetch Candidates

```python
def get_candidates(
    es: Elasticsearch,
    query_embedding: list,
    query_text: str,
    num_candidates: int = 100
):
    """Get hybrid search candidates for reranking."""

    # Combine results from both searches
    vector_results = es.search(
        index="documents",
        knn={
            "field": "embedding",
            "query_vector": query_embedding,
            "k": num_candidates
        },
        size=num_candidates
    )

    keyword_results = es.search(
        index="documents",
        query={
            "match": {
                "content": query_text
            }
        },
        size=num_candidates
    )

    # Get unique documents
    candidates = {}
    for hit in vector_results['hits']['hits']:
        candidates[hit['_id']] = hit['_source']

    for hit in keyword_results['hits']['hits']:
        candidates[hit['_id']] = hit['_source']

    return list(candidates.values())
```

### 2. Rerank with Cross-Encoder

```python
from sentence_transformers import CrossEncoder

def rerank_with_cross_encoder(
    candidates: list,
    query: str,
    model_name: str = 'cross-encoder/ms-marco-MiniLM-L-6-v2'
):
    """Rerank candidates using cross-encoder."""

    model = CrossEncoder(model_name)

    # Prepare query-document pairs
    pairs = [(query, doc['content']) for doc in candidates]

    # Get scores
    scores = model.predict(pairs)

    # Add scores to documents
    for doc, score in zip(candidates, scores):
        doc['rerank_score'] = score

    # Sort by rerank score
    reranked = sorted(candidates, key=lambda x: x['rerank_score'], reverse=True)

    return reranked
```

## Performance Optimization

### 1. Index Optimization

```json
PUT documents
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "index": {
      "knn": true,
      "knn.algo_param": {
        "ef_construction": 128,
        "m": 16
      },
      "refresh_interval": "30s"
    }
  }
}
```

### 2. Query Optimization

```json
GET documents/_search
{
  "knn": {
    "field": "embedding",
    "query_vector": [...],
    "k": 50,
    "num_candidates": 100,
    "boost": 1.0
  },
  "_source": ["id", "content"]
}
```

### 3. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_embedding(query_hash: str):
    """Cache query embeddings."""
    return model.encode(query_text)
```

## Complete Example

### Full Hybrid Search Pipeline

```python
class ElasticsearchHybridSearch:
    def __init__(self, es_host: str = "http://localhost:9200"):
        self.es = Elasticsearch(es_host)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    def hybrid_search(
        self,
        query: str,
        method: str = 'rrf',
        alpha: float = 0.5,
        k: int = 60,
        use_reranking: bool = False,
        num_rerank: int = 50
    ):
        """Complete hybrid search pipeline."""

        # Get query embedding
        query_embedding = self.model.encode(query).tolist()

        # Get candidates
        candidates = self.get_candidates(query, query_embedding, num_candidates=100)

        # Apply fusion
        if method == 'rrf':
            results = self.apply_rrf(candidates, k=k)
        elif method == 'linear':
            results = self.apply_linear(candidates, alpha=alpha)
        else:
            raise ValueError(f"Unknown method: {method}")

        # Apply reranking if requested
        if use_reranking and results:
            results = self.apply_reranking(results[:num_rerank], query)

        return results

    def get_candidates(self, query: str, query_embedding: list, num_candidates: int = 100):
        """Get hybrid search candidates."""

        # Vector search
        vector_results = self.es.search(
            index="documents",
            knn={
                "field": "embedding",
                "query_vector": query_embedding,
                "k": num_candidates
            },
            size=num_candidates
        )

        # Keyword search
        keyword_results = self.es.search(
            index="documents",
            query={
                "match": {
                    "content": query
                }
            },
            size=num_candidates
        )

        # Combine candidates
        candidates = {}
        for hit in vector_results['hits']['hits']:
            candidates[hit['_id']] = hit['_source']

        for hit in keyword_results['hits']['hits']:
            candidates[hit['_id']] = hit['_source']

        return list(candidates.values())

    def apply_rrf(self, candidates: list, k: int = 60):
        """Apply RRF fusion."""

        scores = {}
        for rank, doc in enumerate(candidates):
            doc_id = doc['id']
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)

        return sorted(
            [{**doc, 'score': scores[doc['id']]} for doc in candidates],
            key=lambda x: x['score'],
            reverse=True
        )

    def apply_linear(self, candidates: list, alpha: float = 0.5):
        """Apply linear combination."""

        # Normalize scores (simplified)
        max_score = max(doc.get('score', 0) for doc in candidates)

        for doc in candidates:
            if 'score' not in doc:
                doc['score'] = 0
            doc['score'] = alpha * doc['score']

        return sorted(candidates, key=lambda x: x['score'], reverse=True)

    def apply_reranking(self, candidates: list, query: str):
        """Apply cross-encoder reranking."""

        pairs = [(query, doc['content']) for doc in candidates]
        scores = self.reranker.predict(pairs)

        for doc, score in zip(candidates, scores):
            doc['rerank_score'] = score

        return sorted(candidates, key=lambda x: x['rerank_score'], reverse=True)
```

## Advantages

1. **Native vector support** - Built-in kNN search
2. **Scalable** - Designed for distributed systems
3. **Rich query DSL** - Flexible and expressive
4. **Real-time** - Near real-time indexing and search
5. **Analytics** - Built-in monitoring and observability

## Considerations

1. **Resource intensive** - Requires significant RAM for vector indexes
2. **Complexity** - More configuration than PostgreSQL
3. **Cost** - Higher infrastructure costs at scale
4. **Learning curve** - Elasticsearch-specific knowledge required

## Best Practices

1. **Tune HNSW parameters** - Balance accuracy and performance
2. **Use async clients** - Improve throughput
3. **Implement caching** - Reduce duplicate computations
4. **Monitor query latency** - Track performance metrics
5. **Use bulk operations** - Improve indexing throughput
6. **Shard appropriately** - Distribute data across nodes
7. **Enable circuit breakers** - Prevent cluster instability
