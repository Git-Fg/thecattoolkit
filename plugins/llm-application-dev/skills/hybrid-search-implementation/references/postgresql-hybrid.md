# PostgreSQL Hybrid Search with pgvector

## Overview

PostgreSQL with pgvector extension provides a complete solution for hybrid search, combining vector similarity and full-text search capabilities in a single database.

## Setup

### 1. Install pgvector

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify installation
SELECT * FROM pg_extension WHERE extname = 'vector';
```

### 2. Create Table with Vector and Full-Text Columns

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI ada-002 dimension
    search_vector tsvector,
    metadata JSONB
);

-- Create indexes
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

CREATE INDEX search_vector_idx ON documents USING GIN (search_vector);
```

### 3. Create Trigger for Full-Text Search Vector

```sql
CREATE FUNCTION update_search_vector() RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', coalesce(NEW.content, '')), 'A');
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_search_vector
    BEFORE INSERT OR UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();
```

## Hybrid Search Query

### RRF Implementation in SQL

```sql
WITH vector_search AS (
    SELECT id, content,
           1 / (1 + (embedding <=> $1)) AS vector_score,
           ROW_NUMBER() OVER (ORDER BY embedding <=> $1) as vector_rank
    FROM documents
    ORDER BY embedding <=> $1
    LIMIT 50
),
keyword_search AS (
    SELECT id, content,
           ts_rank(search_vector, plainto_tsquery('english', $2)) AS keyword_score,
           ROW_NUMBER() OVER (ORDER BY ts_rank(search_vector, plainto_tsquery('english', $2)) DESC) as keyword_rank
    FROM documents
    WHERE search_vector @@ plainto_tsquery('english', $2)
    LIMIT 50
),
rrf_scores AS (
    SELECT COALESCE(v.id, k.id) as id,
           v.content,
           v.vector_score,
           k.keyword_score,
           -- RRF formula
           COALESCE(1.0 / (60 + v.vector_rank), 0) +
           COALESCE(1.0 / (60 + k.keyword_rank), 0) as rrf_score
    FROM vector_search v
    FULL OUTER JOIN keyword_search k ON v.id = k.id
)
SELECT id, content, rrf_score,
       vector_score,
       keyword_score
FROM rrf_scores
ORDER BY rrf_score DESC
LIMIT 10;
```

### Linear Combination

```sql
WITH vector_search AS (
    SELECT id, content,
           1 / (1 + (embedding <=> $1)) AS vector_score
    FROM documents
    ORDER BY embedding <=> $1
    LIMIT 50
),
keyword_search AS (
    SELECT id, content,
           ts_rank(search_vector, plainto_tsquery('english', $2)) AS keyword_score
    FROM documents
    WHERE search_vector @@ plainto_tsquery('english', $2)
    LIMIT 50
)
SELECT COALESCE(v.id, k.id) as id,
       v.content,
       -- Linear combination with alpha weight
       ($3 * v.vector_score + (1 - $3) * k.keyword_score) as hybrid_score
FROM vector_search v
FULL OUTER JOIN keyword_search k ON v.id = k.id
ORDER BY hybrid_score DESC
LIMIT 10;
```

## Cross-Encoder Reranking

### Step 1: Get Candidates with SQL

```sql
-- Fetch top 100 candidates for reranking
WITH candidates AS (
    SELECT id, content
    FROM documents
    ORDER BY embedding <=> $1
    LIMIT 100
)
SELECT * FROM candidates;
```

### Step 2: Rerank with Cross-Encoder

```python
import psycopg2
from sentence_transformers import CrossEncoder

# Connect to PostgreSQL
conn = psycopg2.connect("postgresql://user:pass@localhost/db")
cursor = conn.cursor()

# Fetch query embedding
cursor.execute("SELECT %s::vector", (query_embedding,))
query_vec = cursor.fetchone()[0]

# Get candidates
cursor.execute("""
    SELECT id, content
    FROM documents
    ORDER BY embedding <=> %s
    LIMIT 100
""", (query_vec,))
candidates = cursor.fetchall()

# Load cross-encoder model
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Prepare query-document pairs
query = "search query"
pairs = [(query, content) for _, content in candidates]

# Get reranked scores
scores = model.predict(pairs)

# Combine with IDs and rerank
reranked = list(zip(candidates, scores))
reranked.sort(key=lambda x: x[1], reverse=True)

# Return top 10
return reranked[:10]
```

## Performance Optimization

### 1. Indexing Strategy

```sql
-- HNSW index for fast approximate search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- GIN index for full-text search
CREATE INDEX search_vector_idx ON documents USING GIN (search_vector);
```

### 2. Query Optimization

```sql
-- Use parallel execution
SET max_parallel_workers_per_gather = 4;

-- Adjust work_mem for sorting
SET work_mem = '256MB';

-- Optimize vector search parameters
SET ivfflat.probes = 10;  -- More probes = better accuracy, slower
```

### 3. Materialized Views for Common Queries

```sql
CREATE MATERIALIZED VIEW popular_docs AS
SELECT id, content,
       ts_rank(search_vector, plainto_tsquery('english', 'popular')) as popularity
FROM documents
WHERE search_vector @@ plainto_tsquery('english', 'popular');

-- Refresh periodically
REFRESH MATERIALIZED VIEW popular_docs;
```

## Complete Example

### Python Implementation

```python
import psycopg2
import numpy as np
from typing import List, Tuple

class PostgreSQLHybridSearch:
    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(connection_string)
        self.cursor = self.conn.cursor()

    def hybrid_search(
        self,
        query_embedding: np.ndarray,
        query_text: str,
        method: str = 'rrf',
        alpha: float = 0.5,
        limit: int = 10
    ) -> List[Tuple[int, str, float]]:
        """Perform hybrid search using RRF or linear combination."""

        if method == 'rrf':
            return self._rrf_search(query_embedding, query_text, limit)
        elif method == 'linear':
            return self._linear_search(query_embedding, query_text, alpha, limit)
        else:
            raise ValueError(f"Unknown method: {method}")

    def _rrf_search(
        self,
        query_embedding: np.ndarray,
        query_text: str,
        limit: int = 10
    ) -> List[Tuple[int, str, float]]:
        """RRF hybrid search."""

        query = """
        WITH vector_search AS (
            SELECT id, content,
                   1 / (1 + (embedding <=> %s)) AS vector_score,
                   ROW_NUMBER() OVER (ORDER BY embedding <=> %s) as vector_rank
            FROM documents
            ORDER BY embedding <=> %s
            LIMIT 50
        ),
        keyword_search AS (
            SELECT id, content,
                   ts_rank(search_vector, plainto_tsquery('english', %s)) AS keyword_score,
                   ROW_NUMBER() OVER (
                       ORDER BY ts_rank(search_vector, plainto_tsquery('english', %s)) DESC
                   ) as keyword_rank
            FROM documents
            WHERE search_vector @@ plainto_tsquery('english', %s)
            LIMIT 50
        ),
        rrf_scores AS (
            SELECT COALESCE(v.id, k.id) as id,
                   v.content,
                   COALESCE(1.0 / (60 + v.vector_rank), 0) +
                   COALESCE(1.0 / (60 + k.keyword_rank), 0) as rrf_score
            FROM vector_search v
            FULL OUTER JOIN keyword_search k ON v.id = k.id
        )
        SELECT id, content, rrf_score
        FROM rrf_scores
        ORDER BY rrf_score DESC
        LIMIT %s;
        """

        self.cursor.execute(query, (
            query_embedding, query_embedding, query_embedding,
            query_text, query_text, query_text,
            limit
        ))

        return self.cursor.fetchall()

    def _linear_search(
        self,
        query_embedding: np.ndarray,
        query_text: str,
        alpha: float = 0.5,
        limit: int = 10
    ) -> List[Tuple[int, str, float]]:
        """Linear combination hybrid search."""

        query = """
        WITH vector_search AS (
            SELECT id, content,
                   1 / (1 + (embedding <=> %s)) AS vector_score
            FROM documents
            ORDER BY embedding <=> %s
            LIMIT 50
        ),
        keyword_search AS (
            SELECT id, content,
                   ts_rank(search_vector, plainto_tsquery('english', %s)) AS keyword_score
            FROM documents
            WHERE search_vector @@ plainto_tsquery('english', %s)
            LIMIT 50
        )
        SELECT COALESCE(v.id, k.id) as id,
               COALESCE(v.content, k.content) as content,
               (%s * v.vector_score + (1 - %s) * k.keyword_score) as hybrid_score
        FROM vector_search v
        FULL OUTER JOIN keyword_search k ON v.id = k.id
        ORDER BY hybrid_score DESC
        LIMIT %s;
        """

        self.cursor.execute(query, (
            query_embedding, query_embedding,
            query_text, query_text,
            alpha, alpha,
            limit
        ))

        return self.cursor.fetchall()

    def add_document(self, content: str, embedding: np.ndarray):
        """Add a document with embedding."""

        query = """
        INSERT INTO documents (content, embedding)
        VALUES (%s, %s)
        RETURNING id;
        """

        self.cursor.execute(query, (content, embedding))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def close(self):
        """Close database connection."""
        self.cursor.close()
        self.conn.close()
```

## Advantages

1. **Single database** - No need for multiple systems
2. **ACID compliance** - Strong consistency guarantees
3. **Rich SQL** - Expressive querying capabilities
4. **Cost-effective** - Lower infrastructure costs
5. **Mature ecosystem** - Extensive tooling and support

## Considerations

1. **Vector performance** - Not as fast as specialized vector databases
2. **Scaling** - May need sharding for very large datasets
3. **Memory usage** - Vector indexes consume significant RAM
4. **Complexity** - Requires understanding of both vector and SQL

## Best Practices

1. **Choose right index type** - HNSW for accuracy, IVFFlat for speed
2. **Tune probe count** - Balance accuracy and performance
3. **Use prepared statements** - Prevent SQL injection
4. **Monitor query performance** - Use EXPLAIN ANALYZE
5. **Batch embeddings** - Insert documents in bulk
6. **Cache frequent queries** - Reduce database load
7. **Use connection pooling** - Improve throughput
