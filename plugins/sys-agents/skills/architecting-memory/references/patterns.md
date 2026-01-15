# Memory System Design Patterns

Common design patterns for memory systems in AI agent architectures.

## Pattern 1: Progressive Enhancement

### Description
Start with a simple memory system and gradually add complexity as needs grow.

### Implementation
```python
class ProgressiveMemorySystem:
    def __init__(self):
        self.phase = 1  # Start with Vector RAG
        self.components = {
            "vector_db": None,
            "knowledge_graph": None,
            "temporal_graph": None
        }

    def upgrade(self, phase: int):
        """Upgrade to next phase"""
        if phase == 2 and self.phase < 2:
            self._add_knowledge_graph()
        elif phase == 3 and self.phase < 3:
            self._add_temporal_graph()

        self.phase = phase

    def _add_knowledge_graph(self):
        """Add GraphRAG capabilities"""
        self.components["knowledge_graph"] = KnowledgeGraph()
        # Implementation details...

    def query(self, query: str) -> dict:
        if self.phase == 1:
            return self._vector_rag_query(query)
        elif self.phase == 2:
            return self._graph_rag_query(query)
        elif self.phase == 3:
            return self._temporal_query(query)
```

### Benefits
- GOOD Incremental complexity
- GOOD Early value delivery
- GOOD Learning curve management
- GOOD Proven value at each stage

### Use When
- Uncertain about future requirements
- Need to prove value quickly
- Limited initial resources
- Want to validate approach

## Pattern 2: Layered Memory

### Description
Separate memory into distinct layers with clear responsibilities and interfaces.

### Implementation
```python
class LayeredMemory:
    def __init__(self):
        self.layers = {
            "perception": PerceptionLayer(),      # Raw input
            "working": WorkingMemory(),           # Active context
            "episodic": EpisodicMemory(),        # Experience
            "semantic": SemanticMemory(),        # Knowledge
            "procedural": ProceduralMemory()     # Skills
        }

    def process_input(self, input_data: dict):
        """Process input through layers"""
        # Perception → Working → Episodic
        processed = self.layers["perception"].process(input_data)
        self.layers["working"].update(processed)

        # Episodic → Semantic (consolidation)
        if self.layers["working"].is_full():
            episode = self.layers["working"].extract()
            self.layers["episodic"].store(episode)

            # Consolidate to semantic memory
            self.layers["semantic"].consolidate(episode)

    def recall(self, query: str) -> dict:
        """Recall from appropriate layer"""
        # Working memory first (fast access)
        working_result = self.layers["working"].query(query)
        if working_result:
            return working_result

        # Semantic memory (knowledge)
        semantic_result = self.layers["semantic"].query(query)
        if semantic_result:
            return semantic_result

        # Episodic memory (experiences)
        episodic_result = self.layers["episodic"].query(query)
        return episodic_result
```

### Benefits
- GOOD Clear separation of concerns
- GOOD Modular architecture
- GOOD Easy to test and debug
- GOOD Scalable design

### Use When
- Complex memory requirements
- Need to isolate different types of memory
- Want clear interfaces
- Testing is critical

## Pattern 3: Observer Pattern for Memory Events

### Description
Use observer pattern to notify components when memory changes.

### Implementation
```python
class MemoryEvent:
    def __init__(self, event_type: str, data: dict):
        self.type = event_type
        self.data = data
        self.timestamp = datetime.now()

class MemoryObservable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer: callable):
        """Add observer to memory changes"""
        self.observers.append(observer)

    def notify(self, event: MemoryEvent):
        """Notify all observers of memory event"""
        for observer in self.observers:
            try:
                observer(event)
            except Exception as e:
                print(f"Observer error: {e}")

class MemoryManager(MemoryObservable):
    def __init__(self):
        super().__init__()
        self.memory = {}

    def store(self, key: str, value: any):
        """Store in memory and notify"""
        old_value = self.memory.get(key)
        self.memory[key] = value

        # Notify observers
        self.notify(MemoryEvent("store", {
            "key": key,
            "old_value": old_value,
            "new_value": value
        }))

    def update(self, key: str, value: any):
        """Update memory and notify"""
        old_value = self.memory.get(key)
        self.memory[key] = value

        self.notify(MemoryEvent("update", {
            "key": key,
            "old_value": old_value,
            "new_value": value
        }))

# Usage example
def memory_change_handler(event: MemoryEvent):
    if event.type == "store":
        print(f"Stored: {event.data['key']}")
    elif event.type == "update":
        print(f"Updated: {event.data['key']}")

memory_manager = MemoryManager()
memory_manager.add_observer(memory_change_handler)
```

### Benefits
- GOOD Decoupled components
- GOOD Event-driven architecture
- GOOD Easy to add monitoring
- GOOD Reactive updates

### Use When
- Multiple components need to react to memory changes
- Want to monitor memory usage
- Need event-driven architecture
- Loose coupling is important

## Pattern 4: Repository Pattern for Memory Abstraction

### Description
Abstract memory storage implementation behind a common interface.

### Implementation
```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class MemoryRepository(ABC):
    @abstractmethod
    def store(self, key: str, value: Any, metadata: Dict = None):
        pass

    @abstractmethod
    def retrieve(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def search(self, query: str, filters: Dict = None) -> List[Dict]:
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

class VectorMemoryRepository(MemoryRepository):
    def __init__(self, vector_db):
        self.vector_db = vector_db

    def store(self, key: str, value: Any, metadata: Dict = None):
        embedding = self.embed(value)
        self.vector_db.add(
            ids=[key],
            documents=[value],
            embeddings=[embedding],
            metadatas=[metadata or {}]
        )

    def retrieve(self, key: str) -> Optional[Any]:
        results = self.vector_db.get(ids=[key])
        if results["documents"] and results["documents"][0]:
            return {
                "value": results["documents"][0][0],
                "metadata": results["metadatas"][0][0]
            }
        return None

    def search(self, query: str, filters: Dict = None) -> List[Dict]:
        query_embedding = self.embed(query)
        results = self.vector_db.query(
            query_embeddings=[query_embedding],
            n_results=10,
            where=filters
        )
        return [
            {
                "value": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score": results["distances"][0][i]
            }
            for i in range(len(results["documents"][0]))
        ]

class GraphMemoryRepository(MemoryRepository):
    def __init__(self, graph_db):
        self.graph_db = graph_db

    def store(self, key: str, value: Any, metadata: Dict = None):
        self.graph_db.create_node(key, value, metadata)

    def retrieve(self, key: str) -> Optional[Any]:
        node = self.graph_db.get_node(key)
        return node if node else None

    def search(self, query: str, filters: Dict = None) -> List[Dict]:
        # Graph-based search implementation
        pass

class UnifiedMemoryManager:
    def __init__(self, repository: MemoryRepository):
        self.repository = repository

    def store_memory(self, key: str, value: Any, memory_type: str = "general"):
        """Store with type metadata"""
        metadata = {"type": memory_type}
        self.repository.store(key, value, metadata)

    def get_memory(self, key: str) -> Optional[Any]:
        """Retrieve memory"""
        result = self.repository.retrieve(key)
        return result["value"] if result else None

    def search_memories(self, query: str, memory_type: str = None) -> List[Dict]:
        """Search memories"""
        filters = {"type": memory_type} if memory_type else None
        return self.repository.search(query, filters)
```

### Benefits
- GOOD Implementation hiding
- GOOD Easy to swap storage backends
- GOOD Consistent interface
- GOOD Testable architecture

### Use When
- Want to support multiple storage backends
- Need to switch implementations
- Testing with different storage types
- Long-term flexibility required

## Pattern 5: Memory Consolidation

### Description
Periodically consolidate memories to maintain efficiency and remove redundancy.

### Implementation
```python
class MemoryConsolidator:
    def __init__(self, memory_manager, consolidation_threshold: int = 100):
        self.memory_manager = memory_manager
        self.consolidation_threshold = consolidation_threshold
        self.memory_count = 0

    def maybe_consolidate(self):
        """Check if consolidation is needed"""
        self.memory_count = self.memory_manager.count()

        if self.memory_count >= self.consolidation_threshold:
            self.consolidate()

    def consolidate(self):
        """Perform memory consolidation"""
        print("Starting memory consolidation...")

        # 1. Find similar memories
        similar_groups = self._find_similar_memories()

        # 2. Merge similar memories
        merged_memories = []
        for group in similar_groups:
            merged = self._merge_memory_group(group)
            merged_memories.append(merged)

        # 3. Store merged memories
        for merged in merged_memories:
            self.memory_manager.store(
                merged["key"],
                merged["content"],
                merged["metadata"]
            )

        print(f"Consolidated {len(similar_groups)} groups")

    def _find_similar_memories(self) -> List[List[dict]]:
        """Find groups of similar memories"""
        all_memories = self.memory_manager.get_all_memories()

        # Simplified clustering
        groups = []
        processed = set()

        for memory in all_memories:
            if memory["key"] in processed:
                continue

            group = [memory]
            processed.add(memory["key"])

            # Find similar memories
            for other_memory in all_memories:
                if other_memory["key"] in processed:
                    continue

                similarity = self._calculate_similarity(memory, other_memory)
                if similarity > 0.8:  # Threshold
                    group.append(other_memory)
                    processed.add(other_memory["key"])

            groups.append(group)

        return groups

    def _merge_memory_group(self, group: List[dict]) -> dict:
        """Merge a group of similar memories"""
        # Combine content
        combined_content = "\n".join(m["content"] for m in group)

        # Merge metadata
        combined_metadata = {
            "type": group[0]["metadata"].get("type", "general"),
            "merged_from": [m["key"] for m in group],
            "merge_timestamp": datetime.now().isoformat(),
            "similarity_score": self._calculate_group_similarity(group)
        }

        # Generate new key
        new_key = f"merged_{hash(combined_content) % 10000}"

        return {
            "key": new_key,
            "content": combined_content,
            "metadata": combined_metadata
        }

    def _calculate_similarity(self, memory1: dict, memory2: dict) -> float:
        """Calculate similarity between two memories"""
        # Simplified - use Jaccard similarity
        set1 = set(memory1["content"].split())
        set2 = set(memory2["content"].split())

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0

    def _calculate_group_similarity(self, group: List[dict]) -> float:
        """Calculate average similarity within group"""
        similarities = []

        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                sim = self._calculate_similarity(group[i], group[j])
                similarities.append(sim)

        return sum(similarities) / len(similarities) if similarities else 0
```

### Benefits
- GOOD Reduces memory footprint
- GOOD Removes redundancy
- GOOD Maintains efficiency
- GOOD Improves retrieval quality

### Use When
- Memory is growing large
- Redundancy is an issue
- Storage costs are high
- Retrieval is slowing down

## Pattern 6: Memory Snapshot and Restore

### Description
Create snapshots of memory state for backup, versioning, or state transfer.

### Implementation
```python
class MemorySnapshot:
    def __init__(self, memories: List[dict], timestamp: datetime):
        self.memories = memories
        self.timestamp = timestamp
        self.id = str(uuid.uuid4())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "memories": self.memories
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'MemorySnapshot':
        snapshot = cls(
            memories=data["memories"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
        snapshot.id = data["id"]
        return snapshot

class MemorySnapshotManager:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.snapshots = []

    def create_snapshot(self, description: str = "") -> MemorySnapshot:
        """Create snapshot of current memory state"""
        all_memories = self.memory_manager.get_all_memories()

        snapshot = MemorySnapshot(
            memories=all_memories,
            timestamp=datetime.now()
        )

        snapshot.description = description
        self.snapshots.append(snapshot)

        return snapshot

    def restore_snapshot(self, snapshot_id: str):
        """Restore memory from snapshot"""
        snapshot = self._find_snapshot(snapshot_id)
        if not snapshot:
            raise ValueError(f"Snapshot {snapshot_id} not found")

        # Clear current memory
        self.memory_manager.clear()

        # Restore from snapshot
        for memory in snapshot.memories:
            self.memory_manager.store(
                memory["key"],
                memory["content"],
                memory["metadata"]
            )

    def list_snapshots(self) -> List[dict]:
        """List all snapshots"""
        return [
            {
                "id": s.id,
                "timestamp": s.timestamp.isoformat(),
                "description": s.description,
                "memory_count": len(s.memories)
            }
            for s in self.snapshots
        ]

    def compare_snapshots(self, snapshot_id1: str, snapshot_id2: str) -> dict:
        """Compare two snapshots"""
        s1 = self._find_snapshot(snapshot_id1)
        s2 = self._find_snapshot(snapshot_id2)

        memories1 = {m["key"]: m for m in s1.memories}
        memories2 = {m["key"]: m for m in s2.memories}

        added = set(memories2.keys()) - set(memories1.keys())
        removed = set(memories1.keys()) - set(memories2.keys())
        modified = []

        for key in set(memories1.keys()) & set(memories2.keys()):
            if memories1[key]["content"] != memories2[key]["content"]:
                modified.append(key)

        return {
            "added": list(added),
            "removed": list(removed),
            "modified": modified
        }
```

### Benefits
- GOOD Backup and recovery
- GOOD Version control
- GOOD State transfer
- GOOD Debugging assistance

### Use When
- Need to backup memory state
- Want to version memory changes
- Transferring memory between agents
- Debugging memory issues

## Pattern 7: Adaptive Memory

### Description
Automatically adapt memory behavior based on usage patterns and performance.

### Implementation
```python
class AdaptiveMemoryManager:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.usage_stats = defaultdict(int)
        self.access_times = defaultdict(list)
        self.performance_metrics = []

    def store(self, key: str, value: Any, metadata: Dict = None):
        """Store with adaptive behavior"""
        # Update usage stats
        self.usage_stats[key] += 1

        # Decide storage strategy based on usage
        if self.usage_stats[key] > 100:
            strategy = "long_term_consolidation"
        elif self.usage_stats[key] > 10:
            strategy = "standard_storage"
        else:
            strategy = "short_term_cache"

        # Apply strategy
        if strategy == "long_term_consolidation":
            self._consolidate_similar_memories(key, value)
        else:
            self.memory_manager.store(key, value, metadata)

    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve with adaptive caching"""
        start_time = time.time()

        result = self.memory_manager.retrieve(key)

        access_time = time.time() - start_time
        self.access_times[key].append(access_time)

        # Track performance
        if access_time > 0.1:  # Slow access
            self._optimize_retrieval(key)

        return result

    def _consolidate_similar_memories(self, key: str, value: Any):
        """Consolidate if memory is heavily used"""
        # Find similar memories
        similar = self._find_similar_memories(key, value)

        if len(similar) > 5:  # Threshold
            # Consolidate into semantic memory
            self.memory_manager.consolidate_to_semantic(key, value, similar)

    def _optimize_retrieval(self, key: str):
        """Optimize retrieval for slow memories"""
        # Create cache for frequently accessed slow memories
        avg_access_time = sum(self.access_times[key]) / len(self.access_times[key])

        if avg_access_time > 0.1:
            self.memory_manager.create_cache(key)

    def get_memory_health(self) -> dict:
        """Get overall memory system health"""
        total_accesses = sum(self.usage_stats.values())
        avg_access_time = sum(
            sum(times) / len(times)
            for times in self.access_times.values()
        ) / len(self.access_times) if self.access_times else 0

        return {
            "total_memories": len(self.usage_stats),
            "total_accesses": total_accesses,
            "average_access_time": avg_access_time,
            "most_accessed": max(self.usage_stats.items(), key=lambda x: x[1])
        }
```

### Benefits
- GOOD Self-optimizing
- GOOD Adapts to usage patterns
- GOOD Performance aware
- GOOD Intelligent storage

### Use When
- Usage patterns vary widely
- Performance is critical
- Want automation
- Resource-constrained environments

## Pattern Selection Guide

| Pattern | Best For | Complexity | Benefit |
|---------|----------|------------|---------|
| **Progressive Enhancement** | Uncertain requirements | Low | Incremental value |
| **Layered Memory** | Complex systems | Medium | Separation of concerns |
| **Observer Pattern** | Event-driven | Low | Decoupling |
| **Repository Pattern** | Multiple backends | Medium | Abstraction |
| **Memory Consolidation** | Large memory sets | Medium | Efficiency |
| **Snapshot/Restore** | Backup/versioning | Low | Reliability |
| **Adaptive Memory** | Variable usage | High | Performance |

## Combining Patterns

Patterns can be combined:

```python
class AdvancedMemorySystem:
    def __init__(self):
        # Layered architecture
        self.layers = LayeredMemory()

        # With repository pattern
        self.repository = UnifiedMemoryManager(VectorMemoryRepository())

        # With observer pattern
        self.observable = MemoryObservable()

        # With consolidation
        self.consolidator = MemoryConsolidator(self)

        # With snapshots
        self.snapshot_manager = MemorySnapshotManager(self)
```

## Best Practices

### Do's
GOOD Choose patterns based on actual needs
GOOD Combine patterns thoughtfully
GOOD Start with simple patterns
GOOD Document pattern usage
GOOD Test pattern interactions

### Don'ts
BAD Over-engineer with too many patterns
BAD Mix incompatible patterns
BAD Ignore pattern maintenance costs
BAD Forget to test pattern combinations
BAD Skip pattern documentation

### Pattern Anti-Patterns
- BAD Using all patterns at once
- BAD Changing patterns frequently
- BAD Not measuring pattern benefits
- BAD Ignoring pattern maintenance
- BAD Over-complicating simple needs
