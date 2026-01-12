---
description: "Scaffold a Hybrid Search RAG architecture (Postgres/pgvector + Keyword). Generates production-ready search pipeline with PostgreSQL, vector embeddings, and keyword search."
argument-hint: "<database_type> (default: postgres)"
allowed-tools: [Skill(hybrid-search-implementation)]
disable-model-invocation: true
---

# RAG Scaffolder

Generate a complete Hybrid Search RAG (Retrieval-Augmented Generation) architecture.

**What you get:**
- PostgreSQL + pgvector schema
- Hybrid search implementation (Vector + Keyword)
- RRF Fusion for result ranking
- API endpoints for search and retrieval
- Complete Python/TypeScript implementation

Invoke `hybrid-search-implementation` to scaffold the architecture:

1. **Detect project language** (Python/TypeScript)
2. **Generate database schema** (SQL/ORM models)
3. **Create search class** (RRF Fusion algorithm)
4. **Build API layer** (FastAPI/Express endpoints)
5. **Add configuration** (Environment setup, Docker)

**Default**: PostgreSQL database with pgvector extension for vector similarity search.
