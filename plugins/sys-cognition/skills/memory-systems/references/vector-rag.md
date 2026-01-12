# Vector RAG Implementation Guide

Complete guide to implementing Vector RAG (Retrieval-Augmented Generation) for semantic retrieval.

## Architecture Overview

```
QUERY → Embed Query → Vector Search → Retrieve Top-K → Add to Context
```

## Implementation Steps

### Step 1: Setup Vector Database

```python
import chromadb
from chromadb.config import Settings

# Initialize ChromaDB
client = chromadb.Client(Settings(
    persist_directory="./vector_db",
    anonymized_telemetry=False
))

# Create collection
collection = client.create_collection(
    name="documents",
    embedding_function=embedding_function
)
```

### Step 2: Document Ingestion

```python
def ingest_document(document_id: str, content: str, metadata: dict):
    """Ingest document into vector database"""
    # Generate embedding
    embedding = embedding_function.embed_query(content)

    # Add to collection
    collection.add(
        ids=[document_id],
        documents=[content],
        embeddings=[embedding],
        metadatas=[metadata]
    )
```

### Step 3: Query Processing

```python
def retrieve_relevant_docs(query: str, top_k: int = 5):
    """Retrieve relevant documents for query"""
    # Embed query
    query_embedding = embedding_function.embed_query(query)

    # Search
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results
```

## Embedding Models

### OpenAI Embeddings
```python
import openai

class OpenAIEmbeddings:
    def __init__(self, model="text-embedding-ada-002"):
        self.client = openai.OpenAI()
        self.model = model

    def embed_query(self, text: str):
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
```

### Local Embeddings (Hugging Face)
```python
from sentence_transformers import SentenceTransformer

class LocalEmbeddings:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, text: str):
        return self.model.encode(text).tolist()
```

## Chunking Strategies

### Fixed-Size Chunking
```python
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append({
            "text": chunk,
            "start": start,
            "end": end
        })

        start = end - overlap

    return chunks
```

### Semantic Chunking
```python
def semantic_chunk_text(text: str, sentences: int = 5):
    """Split text into semantic chunks"""
    # Use NLTK or spaCy to split into sentences
    sentences = split_into_sentences(text)

    chunks = []
    for i in range(0, len(sentences), sentences):
        chunk = " ".join(sentences[i:i + sentences])
        chunks.append(chunk)

    return chunks
```

## Retrieval Strategies

### Hybrid Search
```python
def hybrid_search(query: str, top_k: int = 5):
    """Combine vector search with keyword search"""
    # Vector search
    vector_results = collection.query(
        query_embeddings=[embedding_function.embed_query(query)],
        n_results=top_k * 2  # Get more to filter
    )

    # Keyword search (using BM25 or similar)
    keyword_results = keyword_search(query, top_k=top_k)

    # Combine and rerank
    combined = combine_results(vector_results, keyword_results)

    return combined[:top_k]
```

### Reranking
```python
def rerank_results(query: str, results: list, reranker: callable):
    """Rerank results using cross-encoder"""
    # Use cross-encoder for better ranking
    pairs = [(query, doc) for doc in results["documents"]]
    scores = reranker(pairs)

    # Sort by score
    ranked = sorted(zip(results["documents"], scores), key=lambda x: x[1], reverse=True)

    return ranked
```

## Advanced Techniques

### Query Expansion
```python
def expand_query(query: str, llm: callable):
    """Expand query using LLM to improve retrieval"""
    prompt = f"""
    Expand this query to improve document retrieval:
    Original: {query}

    Provide 3 alternative phrasings that capture the same meaning:
    """

    response = llm(prompt)
    expanded_queries = parse_queries(response)

    # Search with all queries
    all_results = []
    for q in expanded_queries:
        results = retrieve_relevant_docs(q, top_k=3)
        all_results.extend(results)

    # Deduplicate and rerank
    return deduplicate_and_rerank(all_results)
```

### Self-Query
```python
def self_query(query: str, metadata: dict, llm: callable):
    """Use LLM to extract semantic query and filters"""
    prompt = f"""
    Given this query and metadata schema, extract:
    1. Semantic search query
    2. Metadata filters

    Query: {query}
    Metadata schema: {list(metadata.keys())}

    Respond as JSON:
    {{
        "query": "semantic query",
        "filters": {{"field": "value"}}
    }}
    """

    response = llm(prompt)
    parsed = json.loads(response)

    # Search with filters
    results = collection.query(
        query_embeddings=[embedding_function.embed_query(parsed["query"])],
        n_results=10,
        where=parsed["filters"]
    )

    return results
```

## Evaluation

### Retrieval Metrics
```python
def evaluate_retrieval(queries: list, relevant_docs: dict, retrieved_docs: dict):
    """Evaluate retrieval quality"""
    results = []

    for query in queries:
        relevant = set(relevant_docs[query])
        retrieved = set(retrieved_docs[query])

        precision = len(relevant & retrieved) / len(retrieved)
        recall = len(relevant & retrieved) / len(relevant)
        f1 = 2 * (precision * recall) / (precision + recall)

        results.append({
            "query": query,
            "precision": precision,
            "recall": recall,
            "f1": f1
        })

    # Calculate averages
    avg_precision = sum(r["precision"] for r in results) / len(results)
    avg_recall = sum(r["recall"] for r in results) / len(results)
    avg_f1 = sum(r["f1"] for r in results) / len(results)

    return {
        "precision": avg_precision,
        "recall": avg_recall,
        "f1": avg_f1
    }
```

## Best Practices

### Do's
✅ Use appropriate chunk sizes (500-1000 tokens)
✅ Add overlap between chunks to preserve context
✅ Store metadata for filtering
✅ Use domain-specific embedding models when available
✅ Implement query expansion for better recall
✅ Monitor and evaluate retrieval quality regularly

### Don'ts
❌ Don't use chunks that are too large
❌ Don't ignore metadata
❌ Don't rely solely on semantic similarity
❌ Don't forget to update embeddings when models improve
❌ Don't use generic embeddings for specialized domains
❌ Don't skip evaluation

## Common Issues

### Issue 1: Low Recall
**Solution:**
- Expand queries
- Use hybrid search (semantic + keyword)
- Adjust chunk sizes
- Add query variations

### Issue 2: Low Precision
**Solution:**
- Use reranking
- Add metadata filters
- Use domain-specific embeddings
- Implement query expansion

### Issue 3: Slow Retrieval
**Solution:**
- Use approximate nearest neighbor (ANN) indexes
- Implement caching
- Use smaller embedding dimensions
- Optimize chunk sizes

## Performance Optimization

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_embed(text: str):
    """Cache embeddings to avoid recomputation"""
    return embedding_function.embed_query(text)
```

### Batch Processing
```python
def batch_embed_texts(texts: list, batch_size: int = 100):
    """Batch process embeddings for efficiency"""
    results = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        embeddings = embedding_function.encode(batch)
        results.extend(embeddings)

    return results
```

### Approximate Nearest Neighbor
```python
# Use FAISS for fast approximate search
import faiss

class FAISSIndex:
    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatIP(dimension)  # Inner product
        self.dimension = dimension

    def add(self, embeddings: list):
        """Add embeddings to index"""
        self.index.add(embeddings)

    def search(self, query_embedding: list, top_k: int = 5):
        """Search for similar embeddings"""
        scores, indices = self.index.search(query_embedding, top_k)
        return scores, indices
```
