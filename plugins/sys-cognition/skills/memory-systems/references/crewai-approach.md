# CrewAI Three-Tier Memory Approach

Implementation of CrewAI's three-tier memory architecture for AI agents.

## Overview

CrewAI implements a three-tier memory system for agents:
1. **Short-Term Memory** - Current conversation context
2. **Long-Term Memory** - Persistent knowledge
3. **Entity Memory** - Entity profiles and relationships

## Tier 1: Short-Term Memory

### Purpose
- Current conversation context
- Immediate task state
- Recent interactions

### Implementation
```python
class ShortTermMemory:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.conversation_buffer = []
        self.task_state = {}

    def add_interaction(self, user_input: str, agent_response: str):
        """Add interaction to short-term memory"""
        self.conversation_buffer.append({
            "user": user_input,
            "agent": agent_response,
            "timestamp": datetime.now()
        })

        # Trim if exceeds max tokens
        self._trim_to_max_tokens()

    def get_relevant_context(self, query: str, top_k: int = 5) -> List[str]:
        """Get relevant context from conversation"""
        # Simple relevance scoring
        scores = []
        for interaction in self.conversation_buffer[-20:]:  # Last 20 interactions
            score = self._calculate_relevance(query, interaction)
            scores.append((score, interaction))

        # Sort by relevance
        scores.sort(key=lambda x: x[0], reverse=True)

        return [interaction for _, interaction in scores[:top_k]]

    def update_task_state(self, key: str, value: any):
        """Update current task state"""
        self.task_state[key] = value

    def get_task_state(self, key: str) -> any:
        """Get task state"""
        return self.task_state.get(key)

    def _trim_to_max_tokens(self):
        """Trim conversation buffer to fit max tokens"""
        total_tokens = self._estimate_tokens(self.conversation_buffer)

        while total_tokens > self.max_tokens and len(self.conversation_buffer) > 1:
            self.conversation_buffer.pop(0)
            total_tokens = self._estimate_tokens(self.conversation_buffer)

    def _calculate_relevance(self, query: str, interaction: dict) -> float:
        """Calculate relevance score (simplified)"""
        # In practice, use embedding similarity
        return len(set(query.split()) & set(interaction["user"].split()))

    def _estimate_tokens(self, buffer: List[dict]) -> int:
        """Estimate token count (simplified)"""
        total_text = ""
        for interaction in buffer:
            total_text += interaction["user"] + " " + interaction["agent"] + " "
        return len(total_text.split())
```

### Context Management
```python
class ContextManager:
    def __init__(self, short_term: ShortTermMemory, max_context_tokens: int = 8000):
        self.short_term = short_term
        self.max_context_tokens = max_context_tokens

    def build_context(self, query: str) -> str:
        """Build context for agent"""
        context_parts = []

        # Add task state
        task_context = self._build_task_context()
        if task_context:
            context_parts.append(task_context)

        # Add relevant conversation
        relevant = self.short_term.get_relevant_context(query, top_k=5)
        conversation_context = self._build_conversation_context(relevant)
        if conversation_context:
            context_parts.append(conversation_context)

        # Combine and trim
        combined = "\n".join(context_parts)
        return self._trim_to_limit(combined)

    def _build_task_context(self) -> str:
        """Build task context from short-term memory"""
        if not self.short_term.task_state:
            return ""

        context = "Current Task State:\n"
        for key, value in self.short_term.task_state.items():
            context += f"- {key}: {value}\n"

        return context

    def _build_conversation_context(self, interactions: List[dict]) -> str:
        """Build conversation context"""
        if not interactions:
            return ""

        context = "Recent Conversation:\n"
        for interaction in interactions[-3:]:  # Last 3 relevant
            context += f"User: {interaction['user']}\n"
            context += f"Agent: {interaction['agent']}\n"

        return context

    def _trim_to_limit(self, text: str, max_chars: int = None) -> str:
        """Trim text to fit in context window"""
        if not max_chars:
            max_chars = self.max_context_tokens * 4  # Approximate chars per token

        if len(text) <= max_chars:
            return text

        return text[:max_chars] + "..."
```

## Tier 2: Long-Term Memory

### Purpose
- Persistent knowledge across sessions
- Learn from past experiences
- Accumulate domain knowledge

### Implementation
```python
class LongTermMemory:
    def __init__(self, vector_db, embedding_func):
        self.vector_db = vector_db
        self.embedding_func = embedding_func
        self.consolidation_threshold = 100  # Consolidate after 100 new memories

    def store_memory(
        self,
        content: str,
        metadata: dict,
        memory_type: str = "general"
    ):
        """Store memory in long-term storage"""
        memory_id = f"mem_{uuid.uuid4()}"

        # Embed memory
        embedding = self.embedding_func.embed_query(content)

        # Store in vector DB
        self.vector_db.add(
            ids=[memory_id],
            documents=[content],
            embeddings=[embedding],
            metadatas=[
                {
                    **metadata,
                    "memory_type": memory_type,
                    "timestamp": datetime.now().isoformat()
                }
            ]
        )

        # Check if consolidation is needed
        self._maybe_consolidate()

    def retrieve_memories(
        self,
        query: str,
        memory_types: List[str] = None,
        top_k: int = 5
    ) -> List[dict]:
        """Retrieve relevant memories"""
        # Embed query
        query_embedding = self.embedding_func.embed_query(query)

        # Search vector DB
        results = self.vector_db.query(
            query_embeddings=[query_embedding],
            n_results=top_k * 2  # Get more to filter
        )

        # Filter by memory type if specified
        if memory_types:
            filtered_results = []
            for i, metadata in enumerate(results["metadatas"][0]):
                if metadata.get("memory_type") in memory_types:
                    filtered_results.append({
                        "content": results["documents"][0][i],
                        "metadata": metadata,
                        "score": results["distances"][0][i]
                    })
            return filtered_results[:top_k]

        return [
            {
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score": results["distances"][0][i]
            }
            for i in range(min(len(results["documents"][0]), top_k))
        ]

    def _maybe_consolidate(self):
        """Periodically consolidate memories"""
        # Check memory count
        count = self.vector_db.count()

        if count % self.consolidation_threshold == 0:
            self._consolidate_memories()

    def _consolidate_memories(self):
        """Consolidate similar memories"""
        # Get all memories
        all_memories = self.vector_db.get()

        # Cluster similar memories
        clusters = self._cluster_memories(all_memories)

        # Create consolidated memories
        for cluster in clusters:
            consolidated = self._consolidate_cluster(cluster)
            self._store_consolidated_memory(consolidated)

    def _cluster_memories(self, memories: List[dict]) -> List[List[dict]]:
        """Cluster similar memories"""
        # Simplified clustering - use DBSCAN or K-means in practice
        return [memories]  # Return all as one cluster for simplicity

    def _consolidate_cluster(self, cluster: List[dict]) -> dict:
        """Consolidate a cluster of memories"""
        # Extract key information
        content = "\n".join([m["content"] for m in cluster])
        metadata = {
            "consolidated": True,
            "source_memories": [m["id"] for m in cluster],
            "consolidation_timestamp": datetime.now().isoformat()
        }

        return {
            "content": content,
            "metadata": metadata
        }
```

### Knowledge Consolidation
```python
class KnowledgeConsolidator:
    def __init__(self, long_term_memory: LongTermMemory):
        self.long_term = long_term_memory

    def consolidate_similar_memories(self, similarity_threshold: float = 0.9):
        """Find and consolidate similar memories"""
        # Get all memories
        all_memories = self.long_term.vector_db.get()

        # Find similar pairs
        similar_pairs = self._find_similar_pairs(all_memories, similarity_threshold)

        # Consolidate
        for pair in similar_pairs:
            self._consolidate_pair(pair)

    def _find_similar_pairs(self, memories: List[dict], threshold: float) -> List[Tuple]:
        """Find pairs of similar memories"""
        pairs = []

        # Simplified - compare all pairs
        for i in range(len(memories)):
            for j in range(i + 1, len(memories)):
                similarity = self._calculate_similarity(memories[i], memories[j])
                if similarity > threshold:
                    pairs.append((memories[i], memories[j]))

        return pairs

    def _calculate_similarity(self, memory1: dict, memory2: dict) -> float:
        """Calculate similarity between memories"""
        # Simplified - use Jaccard similarity on content
        set1 = set(memory1["content"].split())
        set2 = set(memory2["content"].split())

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0

    def _consolidate_pair(self, pair: Tuple[dict, dict]):
        """Consolidate a pair of memories"""
        memory1, memory2 = pair

        # Create consolidated memory
        consolidated_content = f"{memory1['content']}\n\n{memory2['content']}"
        consolidated_metadata = {
            "consolidated": True,
            "source_memories": [memory1["id"], memory2["id"]],
            "consolidation_timestamp": datetime.now().isoformat()
        }

        # Store consolidated memory
        self.long_term.store_memory(
            content=consolidated_content,
            metadata=consolidated_metadata,
            memory_type="consolidated"
        )

        # Remove original memories (simplified)
        # In practice, mark as superseded instead of deleting
```

## Tier 3: Entity Memory

### Purpose
- Persistent entity profiles
- Relationship tracking
- Entity evolution over time

### Implementation
```python
class EntityMemory:
    def __init__(self, graph_db, embedding_func):
        self.graph_db = graph_db
        self.embedding_func = embedding_func
        self.entity_cache = {}

    def create_entity(
        self,
        entity_id: str,
        name: str,
        entity_type: str,
        initial_properties: dict = None
    ):
        """Create new entity in memory"""
        entity = {
            "id": entity_id,
            "name": name,
            "type": entity_type,
            "properties": initial_properties or {},
            "first_seen": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "interactions": 0
        }

        # Store in graph database
        self.graph_db.create_entity(entity)
        self.entity_cache[entity_id] = entity

        return entity

    def update_entity(
        self,
        entity_id: str,
        properties: dict = None,
        new_name: str = None
    ):
        """Update entity with new information"""
        if entity_id not in self.entity_cache:
            return None

        entity = self.entity_cache[entity_id]

        # Update properties
        if properties:
            entity["properties"].update(properties)

        # Update name
        if new_name:
            entity["name"] = new_name

        entity["last_updated"] = datetime.now().isoformat()
        entity["interactions"] += 1

        # Update in graph database
        self.graph_db.update_entity(entity_id, entity)

        return entity

    def get_entity(self, entity_id: str) -> dict:
        """Get entity from memory"""
        if entity_id in self.entity_cache:
            return self.entity_cache[entity_id]

        # Load from graph database
        entity = self.graph_db.get_entity(entity_id)
        if entity:
            self.entity_cache[entity_id] = entity

        return entity

    def link_entities(
        self,
        entity1_id: str,
        entity2_id: str,
        relationship_type: str,
        strength: float = 1.0
    ):
        """Create relationship between entities"""
        relationship = {
            "source": entity1_id,
            "target": entity2_id,
            "type": relationship_type,
            "strength": strength,
            "created": datetime.now().isoformat()
        }

        self.graph_db.create_relationship(relationship)

        return relationship

    def get_entity_relationships(
        self,
        entity_id: str,
        relationship_type: str = None
    ) -> List[dict]:
        """Get all relationships for an entity"""
        relationships = self.graph_db.get_relationships(entity_id)

        if relationship_type:
            relationships = [
                r for r in relationships
                if r["type"] == relationship_type
            ]

        return relationships

    def find_similar_entities(
        self,
        entity_id: str,
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """Find similar entities based on properties and relationships"""
        entity = self.get_entity(entity_id)
        if not entity:
            return []

        # Get all other entities
        all_entities = self.graph_db.get_all_entities()
        similarities = []

        for other_id, other_entity in all_entities.items():
            if other_id == entity_id:
                continue

            similarity = self._calculate_entity_similarity(entity, other_entity)
            similarities.append((other_id, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def _calculate_entity_similarity(self, entity1: dict, entity2: dict) -> float:
        """Calculate similarity between two entities"""
        # Consider type, properties, and relationships
        type_match = 1.0 if entity1["type"] == entity2["type"] else 0.5

        # Property similarity
        common_props = set(entity1["properties"].keys()) & set(entity2["properties"].keys())
        if common_props:
            prop_similarity = sum(
                self._calculate_value_similarity(
                    entity1["properties"][prop],
                    entity2["properties"][prop]
                )
                for prop in common_props
            ) / len(common_props)
        else:
            prop_similarity = 0.0

        # Relationship similarity
        rel_similarity = self._calculate_relationship_similarity(entity1, entity2)

        # Weighted combination
        return (type_match * 0.3 + prop_similarity * 0.4 + rel_similarity * 0.3)

    def _calculate_value_similarity(self, value1, value2) -> float:
        """Calculate similarity between two property values"""
        if value1 == value2:
            return 1.0

        # For strings, use string similarity
        if isinstance(value1, str) and isinstance(value2, str):
            return self._string_similarity(value1, value2)

        return 0.0

    def _string_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity (simplified)"""
        set1 = set(str1.lower().split())
        set2 = set(str2.lower().split())

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0

    def _calculate_relationship_similarity(self, entity1: dict, entity2: dict) -> float:
        """Calculate similarity based on relationships"""
        # Simplified - count common relationships
        # In practice, use more sophisticated methods
        return 0.5
```

### Entity Evolution Tracking
```python
class EntityEvolutionTracker:
    def __init__(self, entity_memory: EntityMemory):
        self.entity_memory = entity_memory
        self.evolution_logs = {}

    def log_entity_change(
        self,
        entity_id: str,
        change_type: str,
        old_value: any,
        new_value: any,
        context: str = None
    ):
        """Log how an entity has changed over time"""
        if entity_id not in self.evolution_logs:
            self.evolution_logs[entity_id] = []

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "change_type": change_type,
            "old_value": old_value,
            "new_value": new_value,
            "context": context
        }

        self.evolution_logs[entity_id].append(log_entry)

    def get_entity_evolution(self, entity_id: str) -> List[dict]:
        """Get evolution history of an entity"""
        return self.evolution_logs.get(entity_id, [])

    def analyze_evolution_trends(self, entity_id: str) -> dict:
        """Analyze evolution trends for an entity"""
        evolution = self.get_entity_evolution(entity_id)

        if not evolution:
            return {}

        trends = {
            "total_changes": len(evolution),
            "change_frequency": self._calculate_change_frequency(evolution),
            "property_changes": self._count_property_changes(evolution),
            "trend_direction": self._analyze_trend_direction(evolution)
        }

        return trends

    def _calculate_change_frequency(self, evolution: List[dict]) -> float:
        """Calculate how often entity changes"""
        if len(evolution) < 2:
            return 0.0

        # Calculate average time between changes
        timestamps = [datetime.fromisoformat(e["timestamp"]) for e in evolution]
        intervals = [
            (timestamps[i+1] - timestamps[i]).total_seconds()
            for i in range(len(timestamps) - 1)
        ]

        return sum(intervals) / len(intervals) if intervals else 0

    def _count_property_changes(self, evolution: List[dict]) -> dict:
        """Count changes by property"""
        property_changes = {}

        for entry in evolution:
            prop = entry.get("property", "unknown")
            property_changes[prop] = property_changes.get(prop, 0) + 1

        return property_changes

    def _analyze_trend_direction(self, evolution: List[dict]) -> str:
        """Analyze overall trend direction"""
        # Simplified - analyze if entity is becoming more/less active
        # In practice, use more sophisticated trend analysis
        return "stable"
```

## Integration Layer

```python
class CrewAIMemorySystem:
    def __init__(self, vector_db, graph_db, embedding_func):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(vector_db, embedding_func)
        self.entity_memory = EntityMemory(graph_db, embedding_func)
        self.evolution_tracker = EntityEvolutionTracker(self.entity_memory)

    def remember(self, content: str, memory_type: str = "general", metadata: dict = None):
        """Store memory in appropriate tier"""
        # Decide which tier to use based on content and context
        if self._is_conversational(content):
            # Short-term memory
            self.short_term.add_interaction(
                metadata.get("user_input", ""),
                metadata.get("agent_response", content)
            )
        else:
            # Long-term memory
            self.long_term.store_memory(content, metadata or {}, memory_type)

            # Check for entities
            if metadata and "entities" in metadata:
                self._process_entities(metadata["entities"])

    def recall(self, query: str, memory_types: List[str] = None) -> dict:
        """Recall relevant memories from all tiers"""
        results = {
            "short_term": [],
            "long_term": [],
            "entity": []
        }

        # Query short-term memory
        results["short_term"] = self.short_term.get_relevant_context(query)

        # Query long-term memory
        results["long_term"] = self.long_term.retrieve_memories(
            query,
            memory_types=memory_types
        )

        # Query entity memory
        if "entity" in query.lower():
            entity_id = self._extract_entity_id(query)
            if entity_id:
                entity = self.entity_memory.get_entity(entity_id)
                if entity:
                    results["entity"] = {
                        "entity": entity,
                        "relationships": self.entity_memory.get_entity_relationships(entity_id)
                    }

        return results

    def _is_conversational(self, content: str) -> bool:
        """Determine if content is conversational"""
        conversational_indicators = ["user", "agent", "question", "answer"]
        return any(indicator in content.lower() for indicator in conversational_indicators)

    def _extract_entity_id(self, query: str) -> str:
        """Extract entity ID from query"""
        # Simplified - look for entity mentions
        # In practice, use NER
        if "entity:" in query:
            return query.split("entity:")[1].strip().split()[0]
        return None

    def _process_entities(self, entities: List[dict]):
        """Process entities found in memory"""
        for entity_data in entities:
            entity_id = entity_data.get("id")
            if entity_id:
                # Create or update entity
                if not self.entity_memory.get_entity(entity_id):
                    self.entity_memory.create_entity(
                        entity_id=entity_id,
                        name=entity_data.get("name", ""),
                        entity_type=entity_data.get("type", "unknown"),
                        initial_properties=entity_data.get("properties", {})
                    )
```

## Best Practices

### Do's
✅ Use appropriate memory tier for content type
✅ Consolidate long-term memory regularly
✅ Track entity evolution over time
✅ Implement proper indexing for retrieval
✅ Consider memory decay for short-term context
✅ Use entity linking to avoid duplicates

### Don'ts
❌ Don't store everything in short-term memory
❌ Don't forget to consolidate long-term memory
❌ Don't ignore entity relationships
❌ Don't use same representation for all memory types
❌ Don't forget to clean up old short-term memories
❌ Don't overcomplicate entity tracking

### Memory Tier Selection

| Content Type | Recommended Tier |
|-------------|-----------------|
| Recent conversation | Short-Term |
| Important facts | Long-Term |
| Entity profiles | Entity Memory |
| Learnings | Long-Term |
| Task state | Short-Term |
| Relationships | Entity Memory |
| Context | Short-Term |
| Knowledge | Long-Term |
