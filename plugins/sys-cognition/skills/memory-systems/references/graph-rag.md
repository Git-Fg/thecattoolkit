# GraphRAG Implementation Guide

Complete guide to implementing GraphRAG (Graph-based Retrieval-Augmented Generation) for relationship modeling.

## Architecture Overview

```
QUERY → Entity Extraction → Graph Traversal → Retrieve → Rank → Context
```

## Core Components

### 1. Entity Extraction

```python
import spacy
from typing import List, Tuple

class EntityExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text: str) -> List[dict]:
        """Extract entities from text"""
        doc = self.nlp(text)

        entities = []
        for ent in doc.ents:
            entities.append({
                "id": f"{ent.label_}_{ent.text}",
                "label": ent.label_,
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char
            })

        return entities

    def extract_relationships(self, text: str, entities: List[dict]) -> List[dict]:
        """Extract relationships between entities"""
        doc = self.nlp(text)

        relationships = []
        for sent in doc.sents:
            sent_ents = [e for e in entities if e["text"] in sent.text]

            # Simple pattern matching for relationships
            for i, ent1 in enumerate(sent_ents):
                for ent2 in sent_ents[i+1:]:
                    if self._are_related(sent, ent1, ent2):
                        relationships.append({
                            "source": ent1["id"],
                            "target": ent2["id"],
                            "type": self._determine_relationship(sent, ent1, ent2),
                            "context": sent.text
                        })

        return relationships

    def _are_related(self, sentence, ent1: dict, ent2: dict) -> bool:
        """Check if two entities are related in the sentence"""
        # Simple heuristic: both in same sentence and close to each other
        return True  # Simplified

    def _determine_relationship(self, sentence, ent1: dict, ent2: dict) -> str:
        """Determine relationship type"""
        # Use dependency parsing or patterns
        return "RELATED_TO"  # Simplified
```

### 2. Knowledge Graph Construction

```python
import networkx as nx
from typing import Set

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.entity_cache = {}

    def add_entity(self, entity: dict):
        """Add entity to graph"""
        self.graph.add_node(
            entity["id"],
            label=entity["label"],
            text=entity["text"],
            type="entity"
        )
        self.entity_cache[entity["id"]] = entity

    def add_relationship(self, relationship: dict):
        """Add relationship to graph"""
        self.graph.add_edge(
            relationship["source"],
            relationship["target"],
            type=relationship["type"],
            context=relationship.get("context", ""),
            weight=1.0
        )

    def add_document(self, entities: List[dict], relationships: List[dict]):
        """Add document to graph"""
        for entity in entities:
            self.add_entity(entity)

        for rel in relationships:
            self.add_relationship(rel)

    def get_entity(self, entity_id: str) -> dict:
        """Get entity by ID"""
        return self.entity_cache.get(entity_id)

    def get_neighbors(self, entity_id: str, relationship_type: str = None) -> Set[str]:
        """Get neighboring entities"""
        if relationship_type:
            return {
                neighbor
                for _, neighbor, data in self.graph.edges(entity_id, data=True)
                if data.get("type") == relationship_type
            }
        else:
            return set(self.graph.neighbors(entity_id))

    def find_path(self, source: str, target: str, max_length: int = 3) -> List[str]:
        """Find path between two entities"""
        try:
            path = nx.shortest_path(self.graph, source, target, weight="weight")
            return path
        except nx.NetworkXNoPath:
            return []
```

### 3. GraphRAG Retrieval

```python
class GraphRAGRetriever:
    def __init__(self, graph: KnowledgeGraph, vector_db, embedding_func):
        self.graph = graph
        self.vector_db = vector_db
        self.embedding_func = embedding_func

    def retrieve(self, query: str, top_k: int = 5) -> List[dict]:
        """Retrieve relevant information using graph + vector search"""

        # Extract entities from query
        entity_extractor = EntityExtractor()
        query_entities = entity_extractor.extract_entities(query)

        # Get initial candidates from vector search
        vector_results = self.vector_db.query(
            query_embeddings=[self.embedding_func.embed_query(query)],
            n_results=top_k * 2
        )

        # Expand using graph traversal
        expanded_entities = self._expand_entities(query_entities)

        # Combine and rank
        combined_results = self._combine_and_rank(
            vector_results,
            expanded_entities,
            query
        )

        return combined_results[:top_k]

    def _expand_entities(self, query_entities: List[dict], max_depth: int = 2) -> Set[str]:
        """Expand entities using graph traversal"""
        expanded = set()
        queue = [(e["id"], 0) for e in query_entities]
        visited = set()

        while queue:
            entity_id, depth = queue.pop(0)

            if entity_id in visited or depth > max_depth:
                continue

            visited.add(entity_id)
            expanded.add(entity_id)

            # Add neighbors
            for neighbor in self.graph.get_neighbors(entity_id):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))

        return expanded

    def _combine_and_rank(self, vector_results: dict, entities: Set[str], query: str):
        """Combine vector and graph results"""
        # Implementation for combining and ranking
        # ...
        pass
```

## Graph Traversal Strategies

### Breadth-First Search (BFS)
```python
def bfs_traversal(graph: nx.Graph, start_entity: str, max_depth: int = 2):
    """Traverse graph using BFS"""
    visited = set()
    queue = [(start_entity, 0)]
    results = []

    while queue:
        entity, depth = queue.pop(0)

        if entity in visited or depth > max_depth:
            continue

        visited.add(entity)
        results.append({
            "entity": entity,
            "depth": depth
        })

        for neighbor in graph.neighbors(entity):
            if neighbor not in visited:
                queue.append((neighbor, depth + 1))

    return results
```

### Depth-First Search (DFS)
```python
def dfs_traversal(graph: nx.Graph, start_entity: str, max_depth: int = 2):
    """Traverse graph using DFS"""
    visited = set()
    stack = [(start_entity, 0)]
    results = []

    while stack:
        entity, depth = stack.pop()

        if entity in visited or depth > max_depth:
            continue

        visited.add(entity)
        results.append({
            "entity": entity,
            "depth": depth
        })

        for neighbor in graph.neighbors(entity):
            if neighbor not in visited:
                stack.append((neighbor, depth + 1))

    return results
```

### Personalized PageRank
```python
def personalized_pagerank(graph: nx.Graph, seed_entities: List[str], alpha: float = 0.85):
    """Compute Personalized PageRank for entity ranking"""
    # Create personalization vector
    personalization = {node: 0.0 for node in graph.nodes()}
    for seed in seed_entities:
        if seed in personalization:
            personalization[seed] = 1.0 / len(seed_entities)

    # Compute PageRank
    pagerank_scores = nx.pagerank(
        graph,
        alpha=alpha,
        personalization=personalization
    )

    # Sort by score
    ranked_entities = sorted(
        pagerank_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_entities
```

## Entity Linking

### Linking New Entities to Graph
```python
class EntityLinker:
    def __init__(self, graph: KnowledgeGraph, embedding_func):
        self.graph = graph
        self.embedding_func = embedding_func

    def link_entity(self, new_entity: dict, threshold: float = 0.8) -> str:
        """Link new entity to existing graph entities"""
        new_embedding = self.embedding_func.embed_query(new_entity["text"])

        best_match = None
        best_score = 0

        # Compare with existing entities
        for entity_id in self.graph.graph.nodes():
            entity = self.graph.get_entity(entity_id)
            entity_embedding = self.embedding_func.embed_query(entity["text"])

            similarity = cosine_similarity([new_embedding], [entity_embedding])[0][0]

            if similarity > threshold and similarity > best_score:
                best_match = entity_id
                best_score = similarity

        return best_match if best_match else None

    def merge_entities(self, entity1_id: str, entity2_id: str, relationship_type: str):
        """Merge two entities in the graph"""
        # Merge nodes
        # This is a simplified implementation
        # In practice, you'd want to handle conflicts carefully
        pass
```

## Graph Augmentation

### Automatic Relationship Discovery
```python
class RelationshipDiscovery:
    def __init__(self, graph: KnowledgeGraph):
        self.graph = graph

    def discover_implicit_relationships(self, entity_pair: Tuple[str, str]) -> List[dict]:
        """Discover implicit relationships using path analysis"""
        entity1, entity2 = entity_pair

        # Find all paths between entities
        paths = self._find_all_paths(entity1, entity2, max_length=3)

        # Extract relationship patterns
        patterns = []
        for path in paths:
            pattern = self._extract_pattern(path)
            patterns.append(pattern)

        return patterns

    def _find_all_paths(self, start: str, end: str, max_length: int = 3):
        """Find all paths between two entities"""
        paths = []
        self._dfs_paths(start, end, max_length, [], paths)
        return paths

    def _dfs_paths(self, current: str, end: str, max_length: int, path: List[str], all_paths: List[List[str]]):
        """DFS to find paths"""
        if len(path) > max_length:
            return

        if current == end:
            all_paths.append(path + [current])
            return

        if current in path:
            return

        for neighbor in self.graph.get_neighbors(current):
            self._dfs_paths(neighbor, end, max_length, path + [current], all_paths)
```

## Query Processing

### Multi-Hop Reasoning
```python
def multi_hop_reasoning(graph: nx.Graph, query: str, num_hops: int = 2):
    """Perform multi-hop reasoning on graph"""
    # Extract entities from query
    entity_extractor = EntityExtractor()
    query_entities = entity_extractor.extract_entities(query)

    # For each pair of query entities, find paths
    reasoning_chains = []
    for i, ent1 in enumerate(query_entities):
        for ent2 in query_entities[i+1:]:
            path = graph.find_path(ent1["id"], ent2["id"], max_length=num_hops)
            if path:
                reasoning_chains.append(path)

    return reasoning_chains
```

## Graph Construction from Documents

### Batch Processing
```python
def build_graph_from_documents(documents: List[dict], graph: KnowledgeGraph):
    """Build knowledge graph from batch of documents"""
    entity_extractor = EntityExtractor()

    for doc_id, content in documents:
        # Extract entities
        entities = entity_extractor.extract_entities(content)

        # Extract relationships
        relationships = entity_extractor.extract_relationships(content, entities)

        # Add to graph
        graph.add_document(entities, relationships)

        # Store document in vector DB
        vector_db.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[{
                "entities": [e["id"] for e in entities],
                "relationships": [r["type"] for r in relationships]
            }]
        )
```

## Best Practices

### Do's
✅ Use domain-specific entity extraction models
✅ Validate relationships before adding to graph
✅ Implement entity linking to avoid duplicates
✅ Use graph traversal for context expansion
✅ Cache graph queries for performance
✅ Monitor graph size and complexity

### Don'ts
❌ Don't add all entities without validation
❌ Don't ignore entity linking
❌ Don't use deep graph traversal (>3 hops)
❌ Don't forget to update embeddings
❌ Don't store low-confidence relationships
❌ Don't ignore graph maintenance

## Performance Considerations

### Graph Size Management
```python
def manage_graph_size(graph: KnowledgeGraph, max_nodes: int = 100000):
    """Manage graph size by removing old/low-value nodes"""
    if len(graph.graph.nodes()) > max_nodes:
        # Remove nodes with low PageRank scores
        pagerank = nx.pagerank(graph.graph)

        # Sort and remove bottom 10%
        sorted_nodes = sorted(pagerank.items(), key=lambda x: x[1])
        nodes_to_remove = [node for node, _ in sorted_nodes[:len(sorted_nodes) // 10]]

        graph.graph.remove_nodes_from(nodes_to_remove)
```

### Caching Graph Queries
```python
from functools import lru_cache

class GraphRAGRetriever:
    def __init__(self, graph: KnowledgeGraph, vector_db, embedding_func):
        self.graph = graph
        self.vector_db = vector_db
        self.embedding_func = embedding_func
        self._cache = {}

    @lru_cache(maxsize=1000)
    def cached_traversal(self, entity_id: str, max_depth: int):
        """Cache graph traversal results"""
        return self.graph.bfs_traversal(entity_id, max_depth)
```

## Evaluation

### Graph Quality Metrics
```python
def evaluate_graph(graph: KnowledgeGraph, ground_truth: dict):
    """Evaluate graph construction quality"""
    metrics = {
        "entity_precision": calculate_entity_precision(graph, ground_truth),
        "entity_recall": calculate_entity_recall(graph, ground_truth),
        "relationship_precision": calculate_relationship_precision(graph, ground_truth),
        "relationship_recall": calculate_relationship_recall(graph, ground_truth)
    }

    return metrics
```

### Retrieval Evaluation
```python
def evaluate_graphrag(queries: List[str], relevant_docs: dict, retrieved_docs: dict):
    """Evaluate GraphRAG retrieval quality"""
    # Similar to vector RAG evaluation
    # But consider multi-hop reasoning
    pass
```
