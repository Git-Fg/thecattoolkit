# Custom Hybrid Search Pipeline

## Overview

A custom pipeline provides maximum flexibility for hybrid search, allowing you to control every aspect of the search process, from indexing to reranking.

## Architecture

```
Query Input
    ↓
Query Processing (embedding, tokenization)
    ↓
Parallel Execution
    ├── Vector Search → Candidates (Top N)
    └── Keyword Search → Candidates (Top N)
    ↓
Fusion (RRF/Linear/Cross-Encoder)
    ↓
Reranking (Optional)
    ↓
Results (Top K)
```

## Implementation Patterns

### 1. Async/Await Pattern

```python
import asyncio
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

@dataclass
class SearchResult:
    doc_id: str
    content: str
    score: float
    source: str  # 'vector', 'keyword', or 'hybrid'

class HybridSearchPipeline:
    def __init__(
        self,
        vector_store,
        keyword_store,
        embedding_model,
        reranker=None,
        max_workers: int = 4
    ):
        self.vector_store = vector_store
        self.keyword_store = keyword_store
        self.embedding_model = embedding_model
        self.reranker = reranker
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def search(
        self,
        query: str,
        k: int = 10,
        fusion_method: str = 'rrf',
        alpha: float = 0.5,
        use_reranking: bool = False,
        num_candidates: int = 100
    ) -> List[SearchResult]:
        """Main search pipeline."""

        # Process query
        query_embedding = await self.get_embedding(query)

        # Execute searches in parallel
        vector_task = self.vector_search(
            query_embedding,
            num_candidates=num_candidates
        )
        keyword_task = self.keyword_search(query, num_candidates=num_candidates)

        vector_results, keyword_results = await asyncio.gather(
            vector_task, keyword_task
        )

        # Apply fusion
        if fusion_method == 'rrf':
            results = self.apply_rrf(vector_results, keyword_results, k=k)
        elif fusion_method == 'linear':
            results = self.apply_linear(vector_results, keyword_results, alpha=alpha, k=k)
        else:
            raise ValueError(f"Unknown fusion method: {fusion_method}")

        # Apply reranking if requested
        if use_reranking and results and self.reranker:
            results = await self.rerank(results, query)

        return results[:k]

    async def get_embedding(self, query: str) -> List[float]:
        """Get query embedding asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.embedding_model.encode,
            query
        )

    async def vector_search(
        self,
        query_embedding: List[float],
        num_candidates: int = 100
    ) -> List[SearchResult]:
        """Perform vector similarity search."""

        def _search():
            results = self.vector_store.search(
                query_embedding,
                k=num_candidates
            )
            return [
                SearchResult(
                    doc_id=doc_id,
                    content=content,
                    score=score,
                    source='vector'
                )
                for doc_id, content, score in results
            ]

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, _search)

    async def keyword_search(
        self,
        query: str,
        num_candidates: int = 100
    ) -> List[SearchResult]:
        """Perform keyword search."""

        def _search():
            results = self.keyword_store.search(
                query,
                k=num_candidates
            )
            return [
                SearchResult(
                    doc_id=doc_id,
                    content=content,
                    score=score,
                    source='keyword'
                )
                for doc_id, content, score in results
            ]

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, _search)

    def apply_rrf(
        self,
        vector_results: List[SearchResult],
        keyword_results: List[SearchResult],
        k: int = 60
    ) -> List[SearchResult]:
        """Apply Reciprocal Rank Fusion."""

        scores = {}

        # Process vector results
        for rank, result in enumerate(vector_results):
            scores[result.doc_id] = scores.get(result.doc_id, 0) + 1.0 / (k + rank + 1)

        # Process keyword results
        for rank, result in enumerate(keyword_results):
            scores[result.doc_id] = scores.get(result.doc_id, 0) + 1.0 / (k + rank + 1)

        # Combine and sort
        all_results = {r.doc_id: r for r in vector_results + keyword_results}

        final_results = [
            SearchResult(
                doc_id=doc_id,
                content=all_results[doc_id].content,
                score=scores[doc_id],
                source='hybrid'
            )
            for doc_id in sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        ]

        return final_results

    def apply_linear(
        self,
        vector_results: List[SearchResult],
        keyword_results: List[SearchResult],
        alpha: float = 0.5,
        k: int = 10
    ) -> List[SearchResult]:
        """Apply linear combination."""

        # Create score maps
        vector_scores = {r.doc_id: r.score for r in vector_results}
        keyword_scores = {r.doc_id: r.score for r in keyword_results}

        # Get all document IDs
        all_ids = set(vector_scores.keys()) | set(keyword_scores.keys())

        # Normalize scores (min-max normalization)
        all_scores = list(vector_scores.values()) + list(keyword_scores.values())
        min_score = min(all_scores) if all_scores else 0
        max_score = max(all_scores) if all_scores else 1

        if max_score > min_score:
            vector_scores = {
                k: (v - min_score) / (max_score - min_score)
                for k, v in vector_scores.items()
            }
            keyword_scores = {
                k: (v - min_score) / (max_score - min_score)
                for k, v in keyword_scores.items()
            }

        # Combine scores
        combined_scores = {}
        for doc_id in all_ids:
            v_score = vector_scores.get(doc_id, 0)
            k_score = keyword_scores.get(doc_id, 0)
            combined_scores[doc_id] = alpha * v_score + (1 - alpha) * k_score

        # Sort and return
        all_results = {r.doc_id: r for r in vector_results + keyword_results}

        sorted_ids = sorted(
            combined_scores.keys(),
            key=lambda x: combined_scores[x],
            reverse=True
        )

        return [
            SearchResult(
                doc_id=doc_id,
                content=all_results[doc_id].content,
                score=combined_scores[doc_id],
                source='hybrid'
            )
            for doc_id in sorted_ids[:k]
        ]

    async def rerank(
        self,
        results: List[SearchResult],
        query: str
    ) -> List[SearchResult]:
        """Rerank results using cross-encoder."""

        if not self.reranker:
            return results

        # Prepare query-document pairs
        pairs = [(query, result.content) for result in results]

        # Get reranking scores
        def _rerank():
            return self.reranker.predict(pairs)

        loop = asyncio.get_event_loop()
        rerank_scores = await loop.run_in_executor(self.executor, _rerank)

        # Update results with rerank scores
        for result, score in zip(results, rerank_scores):
            result.score = score
            result.source = 'reranked'

        # Sort by rerank score
        return sorted(results, key=lambda x: x.score, reverse=True)

    async def batch_search(
        self,
        queries: List[str],
        **kwargs
    ) -> List[List[SearchResult]]:
        """Search multiple queries in parallel."""

        tasks = [
            self.search(query, **kwargs)
            for query in queries
        ]

        return await asyncio.gather(*tasks)
```

### 2. Streaming Pattern

```python
import asyncio
from typing import AsyncIterator

class StreamingHybridSearch:
    def __init__(self, pipeline: HybridSearchPipeline):
        self.pipeline = pipeline

    async def search_stream(
        self,
        query: str,
        **kwargs
    ) -> AsyncIterator[SearchResult]:
        """Stream search results as they become available."""

        # Start vector search
        vector_task = asyncio.create_task(
            self.pipeline.vector_search(query)
        )

        # Start keyword search
        keyword_task = asyncio.create_task(
            self.pipeline.keyword_search(query)
        )

        # Wait for both to complete
        vector_results, keyword_results = await asyncio.gather(
            vector_task, keyword_task
        )

        # Apply fusion
        fused_results = self.pipeline.apply_rrf(vector_results, keyword_results)

        # Yield results one by one
        for result in fused_results:
            yield result
            await asyncio.sleep(0)  # Allow other tasks to run

# Usage
async def main():
    streaming_search = StreamingHybridSearch(pipeline)

    async for result in streaming_search.search_stream("my query"):
        print(f"Result: {result.content} (score: {result.score})")
```

### 3. Caching Pattern

```python
from functools import lru_cache
import hashlib
import json

class CachedHybridSearch:
    def __init__(self, pipeline: HybridSearchPipeline):
        self.pipeline = pipeline
        self.cache = {}

    def _get_cache_key(self, query: str, **kwargs) -> str:
        """Generate cache key from query and parameters."""
        key_data = {
            'query': query,
            **kwargs
        }
        return hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()

    @lru_cache(maxsize=1000)
    async def search(
        self,
        query: str,
        k: int = 10,
        fusion_method: str = 'rrf',
        alpha: float = 0.5,
        use_reranking: bool = False,
        num_candidates: int = 100
    ) -> List[SearchResult]:
        """Search with caching."""

        cache_key = self._get_cache_key(
            query, k=k, fusion_method=fusion_method,
            alpha=alpha, use_reranking=use_reranking,
            num_candidates=num_candidates
        )

        if cache_key in self.cache:
            return self.cache[cache_key]

        results = await self.pipeline.search(
            query=query,
            k=k,
            fusion_method=fusion_method,
            alpha=alpha,
            use_reranking=use_reranking,
            num_candidates=num_candidates
        )

        self.cache[cache_key] = results
        return results
```

### 4. Configurable Fusion

```python
from abc import ABC, abstractmethod
from typing import List

class FusionMethod(ABC):
    @abstractmethod
    def fuse(
        self,
        vector_results: List[SearchResult],
        keyword_results: List[SearchResult],
        **kwargs
    ) -> List[SearchResult]:
        pass

class RRFusion(FusionMethod):
    def fuse(
        self,
        vector_results: List[SearchResult],
        keyword_results: List[SearchResult],
        k: int = 60
    ) -> List[SearchResult]:
        scores = {}

        for rank, result in enumerate(vector_results):
            scores[result.doc_id] = scores.get(result.doc_id, 0) + 1.0 / (k + rank + 1)

        for rank, result in enumerate(keyword_results):
            scores[result.doc_id] = scores.get(result.doc_id, 0) + 1.0 / (k + rank + 1)

        all_results = {r.doc_id: r for r in vector_results + keyword_results}

        return sorted(
            [
                SearchResult(
                    doc_id=doc_id,
                    content=all_results[doc_id].content,
                    score=scores[doc_id],
                    source='hybrid'
                )
                for doc_id in sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
            ],
            key=lambda x: x.score,
            reverse=True
        )

class LinearFusion(FusionMethod):
    def fuse(
        self,
        vector_results: List[SearchResult],
        keyword_results: List[SearchResult],
        alpha: float = 0.5
    ) -> List[SearchResult]:
        # Implementation from earlier
        pass

class ConfigurableHybridSearch:
    def __init__(self, vector_store, keyword_store, embedding_model):
        self.vector_store = vector_store
        self.keyword_store = keyword_store
        self.embedding_model = embedding_model
        self.fusion_methods = {
            'rrf': RRFusion(),
            'linear': LinearFusion()
        }

    async def search(
        self,
        query: str,
        fusion_method: str = 'rrf',
        **kwargs
    ) -> List[SearchResult]:
        """Search with configurable fusion."""

        fusion = self.fusion_methods.get(fusion_method)
        if not fusion:
            raise ValueError(f"Unknown fusion method: {fusion_method}")

        # Get query embedding
        query_embedding = await self.get_embedding(query)

        # Execute searches
        vector_results = await self.vector_search(query_embedding)
        keyword_results = await self.keyword_search(query)

        # Apply fusion
        return fusion.fuse(vector_results, keyword_results, **kwargs)
```

## Production Considerations

### 1. Error Handling

```python
async def search_with_retry(
    query: str,
    max_retries: int = 3,
    backoff_factor: float = 1.5
):
    """Search with exponential backoff retry."""

    for attempt in range(max_retries):
        try:
            return await pipeline.search(query)
        except Exception as e:
            if attempt == max_retries - 1:
                raise

            wait_time = backoff_factor ** attempt
            await asyncio.sleep(wait_time)

    return []
```

### 2. Monitoring

```python
import time
from contextlib import asynccontextmanager

@asynccontextmanager
async def measure_search_time():
    """Measure search execution time."""
    start = time.time()
    try:
        yield
    finally:
        duration = time.time() - start
        print(f"Search took {duration:.3f}s")

# Usage
async with measure_search_time():
    results = await pipeline.search(query)
```

### 3. Load Balancing

```python
class LoadBalancedHybridSearch:
    def __init__(self, pipelines: List[HybridSearchPipeline]):
        self.pipelines = pipelines
        self.current = 0

    async def search(self, query: str, **kwargs):
        """Round-robin load balancing."""

        pipeline = self.pipelines[self.current]
        self.current = (self.current + 1) % len(self.pipelines)

        return await pipeline.search(query, **kwargs)
```

### 4. Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: float = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN

    async def call(self, func, *args, **kwargs):
        """Call function with circuit breaker protection."""

        if self.state == 'OPEN':
            if time.time() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is OPEN")
            else:
                self.state = 'HALF_OPEN'

        try:
            result = await func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'

            raise
```

## Complete Example

```python
async def main():
    # Initialize stores (implement your own)
    vector_store = MyVectorStore()
    keyword_store = MyKeywordStore()
    embedding_model = MyEmbeddingModel()
    reranker = MyReranker()

    # Create pipeline
    pipeline = HybridSearchPipeline(
        vector_store=vector_store,
        keyword_store=keyword_store,
        embedding_model=embedding_model,
        reranker=reranker
    )

    # Perform search
    results = await pipeline.search(
        query="machine learning algorithms",
        k=10,
        fusion_method='rrf',
        use_reranking=True,
        num_candidates=100
    )

    # Print results
    for result in results:
        print(f"Score: {result.score:.4f}, Source: {result.source}")
        print(f"Content: {result.content[:200]}...")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(main())
```

## Best Practices

1. **Use async/await** - Improve throughput with concurrent execution
2. **Implement caching** - Cache embeddings and frequent queries
3. **Add monitoring** - Track latency, throughput, and error rates
4. **Handle errors gracefully** - Implement retry and circuit breaker patterns
5. **Optimize for your use case** - Tune parameters based on evaluation
6. **Use appropriate data structures** - Optimize for your specific needs
7. **Profile performance** - Identify bottlenecks and optimize
8. **Test with real data** - Validate on actual queries and documents
9. **Monitor quality metrics** - Track recall, precision, and NDCG
10. **A/B test in production** - Measure real-world performance
