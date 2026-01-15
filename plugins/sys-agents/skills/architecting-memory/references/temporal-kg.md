# Temporal Knowledge Graphs Implementation

Complete guide to implementing Temporal Knowledge Graphs for time-sensitive reasoning.

## Architecture Overview

```
QUERY → Extract Time → Graph Traversal → Temporal Filtering → Rank → Context
```

## Core Concepts

### Temporal Entities
- **Events**: Things that happen at specific times
- **States**: Conditions that persist over time periods
- **Time Intervals**: Start and end times for events/states

### Temporal Relationships
- **Before/After**: Chronological ordering
- **During**: Event happens within time period
- **Overlaps**: Time periods intersect
- **Starts/Ends**: Temporal boundaries

## Temporal Graph Structure

### Time Representation
```python
from datetime import datetime, timedelta
from typing import Optional, List, Tuple

class TemporalEntity:
    def __init__(
        self,
        id: str,
        type: str,
        text: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        valid_time: Optional[Tuple[datetime, datetime]] = None
    ):
        self.id = id
        self.type = type
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.valid_time = valid_time  # (valid_from, valid_until)

    def is_active_at(self, timestamp: datetime) -> bool:
        """Check if entity is active at given time"""
        if self.valid_time:
            return self.valid_time[0] <= timestamp <= self.valid_time[1]
        return True  # Always valid if no time constraint
```

### Temporal Relationship
```python
class TemporalRelationship:
    def __init__(
        self,
        source: str,
        target: str,
        type: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        timestamp: Optional[datetime] = None
    ):
        self.source = source
        self.target = target
        self.type = type
        self.start_time = start_time
        self.end_time = end_time
        self.timestamp = timestamp  # For instantaneous events

    def is_valid_at(self, timestamp: datetime) -> bool:
        """Check if relationship is valid at given time"""
        if self.timestamp:
            return abs((timestamp - self.timestamp).total_seconds()) < 1  # Within 1 second

        if self.start_time and self.end_time:
            return self.start_time <= timestamp <= self.end_time

        return True
```

## Temporal Knowledge Graph

```python
import networkx as nx
from datetime import datetime
from collections import defaultdict

class TemporalKnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.time_index = defaultdict(list)  # time -> list of entities/relationships
        self.event_sequence = []  # Chronological sequence of events

    def add_temporal_entity(self, entity: TemporalEntity):
        """Add entity with temporal information"""
        self.graph.add_node(
            entity.id,
            **entity.__dict__,
            temporal=True
        )

        # Index by time
        if entity.valid_time:
            self._index_temporal(entity.id, entity.valid_time[0], entity.valid_time[1])

    def add_temporal_relationship(self, relationship: TemporalRelationship):
        """Add relationship with temporal information"""
        self.graph.add_edge(
            relationship.source,
            relationship.target,
            **relationship.__dict__,
            temporal=True
        )

        # Index by time
        if relationship.timestamp:
            self._index_event(relationship)
        elif relationship.start_time and relationship.end_time:
            self._index_temporal(relationship.source, relationship.start_time, relationship.end_time)

    def _index_event(self, relationship: TemporalRelationship):
        """Index instantaneous event"""
        self.time_index[relationship.timestamp].append({
            "type": "event",
            "relationship": relationship
        })

        self.event_sequence.append({
            "timestamp": relationship.timestamp,
            "source": relationship.source,
            "target": relationship.target,
            "type": relationship.type
        })

        # Keep sorted
        self.event_sequence.sort(key=lambda x: x["timestamp"])

    def _index_temporal(self, entity_id: str, start: datetime, end: datetime):
        """Index entity active over time period"""
        current = start
        while current <= end:
            self.time_index[current].append({
                "type": "entity",
                "id": entity_id,
                "active": True
            })
            current += timedelta(days=1)

    def get_entities_active_at(self, timestamp: datetime) -> List[str]:
        """Get all entities active at specific time"""
        active_entities = []

        for entity_id in self.graph.nodes():
            entity_data = self.graph.nodes[entity_id]
            if entity_data.get("temporal", False):
                temporal_entity = TemporalEntity(**entity_data)
                if temporal_entity.is_active_at(timestamp):
                    active_entities.append(entity_id)

        return active_entities

    def get_events_between(self, start: datetime, end: datetime) -> List[dict]:
        """Get all events in time range"""
        events = []
        for event in self.event_sequence:
            if start <= event["timestamp"] <= end:
                events.append(event)
        return events

    def find_causal_paths(self, source: str, target: str, max_hops: int = 3) -> List[dict]:
        """Find causal paths between entities"""
        # Implementation for finding causal chains
        # Consider temporal ordering of events
        pass

    def predict_future_state(self, entity_id: str, future_time: datetime) -> dict:
        """Predict entity state at future time"""
        # Use temporal patterns to predict state
        # This is simplified - in practice use ML models
        pass
```

## Temporal Query Processing

### Time-Based Retrieval
```python
class TemporalQueryProcessor:
    def __init__(self, graph: TemporalKnowledgeGraph):
        self.graph = graph

    def process_query(self, query: str, time_constraint: Optional[str] = None) -> List[dict]:
        """Process query with temporal constraints"""

        # Parse time from query
        parsed_time = self._parse_temporal_expression(query)

        if time_constraint:
            start, end = self._parse_time_constraint(time_constraint)
        else:
            start, end = None, None

        # Retrieve based on time
        if start and end:
            return self._retrieve_in_range(start, end)
        elif start:
            return self._retrieve_from_time(start)
        elif parsed_time:
            return self._retrieve_at_time(parsed_time)
        else:
            return self._retrieve_without_time(query)

    def _retrieve_in_range(self, start: datetime, end: datetime) -> List[dict]:
        """Retrieve all entities and events in time range"""
        results = []

        # Get entities active in range
        for entity_id in self.graph.nodes():
            entity_data = self.graph.nodes[entity_id]
            if entity_data.get("temporal", False):
                temporal_entity = TemporalEntity(**entity_data)
                if temporal_entity.is_active_at(start) or temporal_entity.is_active_at(end):
                    results.append({
                        "entity": temporal_entity,
                        "relevance": 1.0
                    })

        # Get events in range
        events = self.graph.get_events_between(start, end)
        for event in events:
            results.append({
                "event": event,
                "relevance": 1.0
            })

        return results

    def _parse_temporal_expression(self, query: str) -> Optional[datetime]:
        """Parse temporal expressions in natural language"""
        # Handle expressions like "last week", "yesterday", "5 days ago"
        # This is simplified - use libraries like dateutil or chrono
        import re

        patterns = {
            r"yesterday": datetime.now() - timedelta(days=1),
            r"last week": datetime.now() - timedelta(weeks=1),
            r"last month": datetime.now() - timedelta(days=30),
        }

        for pattern, time in patterns.items():
            if re.search(pattern, query.lower()):
                return time

        return None
```

### Event Sequence Analysis
```python
class EventSequenceAnalyzer:
    def __init__(self, graph: TemporalKnowledgeGraph):
        self.graph = graph

    def find_patterns(self, pattern_type: str = "sequential") -> List[dict]:
        """Find temporal patterns in event sequences"""
        if pattern_type == "sequential":
            return self._find_sequential_patterns()
        elif pattern_type == "periodic":
            return self._find_periodic_patterns()
        elif pattern_type == "causal":
            return self._find_causal_patterns()

    def _find_sequential_patterns(self) -> List[dict]:
        """Find sequential event patterns"""
        patterns = []

        # Look for event chains
        for i in range(len(self.graph.event_sequence) - 1):
            for j in range(i + 1, min(i + 5, len(self.graph.event_sequence))):
                chain = self.graph.event_sequence[i:j]
                pattern = {
                    "type": "sequential",
                    "events": [e["type"] for e in chain],
                    "count": 1,
                    "occurrences": [(chain[0]["timestamp"], chain[-1]["timestamp"])]
                }
                patterns.append(pattern)

        return patterns

    def _find_periodic_patterns(self) -> List[dict]:
        """Find periodic event patterns"""
        patterns = []

        # Group events by type
        events_by_type = defaultdict(list)
        for event in self.graph.event_sequence:
            events_by_type[event["type"]].append(event["timestamp"])

        # Check for periodicity
        for event_type, timestamps in events_by_type.items():
            if len(timestamps) < 3:
                continue

            # Calculate intervals
            intervals = []
            for i in range(len(timestamps) - 1):
                interval = (timestamps[i+1] - timestamps[i]).total_seconds()
                intervals.append(interval)

            # Check if intervals are similar
            avg_interval = sum(intervals) / len(intervals)
            variance = sum((i - avg_interval)**2 for i in intervals) / len(intervals)

            if variance < avg_interval * 0.1:  # Low variance = periodic
                patterns.append({
                    "type": "periodic",
                    "event_type": event_type,
                    "avg_interval": avg_interval,
                    "occurrences": timestamps
                })

        return patterns
```

### Predictive Temporal Modeling
```python
class TemporalPredictor:
    def __init__(self, graph: TemporalKnowledgeGraph):
        self.graph = graph
        self.patterns = self._learn_patterns()

    def _learn_patterns(self) -> dict:
        """Learn temporal patterns from graph"""
        patterns = {
            "sequential": {},
            "periodic": {},
            "causal": {}
        }

        # Learn sequential patterns
        event_types = [e["type"] for e in self.graph.event_sequence]
        for i in range(len(event_types) - 1):
            pair = (event_types[i], event_types[i+1])
            patterns["sequential"][pair] = patterns["sequential"].get(pair, 0) + 1

        return patterns

    def predict_next_event(self, current_event: str) -> List[Tuple[str, float]]:
        """Predict likely next events"""
        predictions = []

        for next_event, count in patterns["sequential"].items():
            if next_event[0] == current_event:
                probability = count / sum(patterns["sequential"].values())
                predictions.append((next_event[1], probability))

        return sorted(predictions, key=lambda x: x[1], reverse=True)

    def predict_entity_state(self, entity_id: str, future_time: datetime) -> dict:
        """Predict entity state at future time"""
        # Get historical states
        states = self._get_entity_state_history(entity_id)

        if not states:
            return {"prediction": "unknown", "confidence": 0.0}

        # Simple prediction based on trend
        # In practice, use time series models
        last_state = states[-1]

        return {
            "prediction": last_state["state"],
            "confidence": 0.6,  # Simplified
            "basis": "trend_analysis"
        }

    def _get_entity_state_history(self, entity_id: str) -> List[dict]:
        """Get historical states of entity"""
        # Simplified - track state changes over time
        # In practice, extract from temporal graph
        return []
```

## Temporal Reasoning

### Before/After Reasoning
```python
def check_temporal_relationship(
    entity1: str,
    entity2: str,
    relationship_type: str,
    graph: TemporalKnowledgeGraph
) -> str:
    """Check temporal relationship between two entities"""

    # Get temporal data
    data1 = graph.graph.nodes[entity1]
    data2 = graph.graph.nodes[entity2]

    if relationship_type == "BEFORE":
        if data1.get("end_time") and data2.get("start_time"):
            return data1["end_time"] < data2["start_time"]

    elif relationship_type == "AFTER":
        if data1.get("start_time") and data2.get("end_time"):
            return data1["start_time"] > data2["end_time"]

    elif relationship_type == "DURING":
        if data1.get("start_time") and data1.get("end_time"):
            if data2.get("start_time"):
                return data1["start_time"] <= data2["start_time"] <= data1["end_time"]

    return None
```

### Temporal Consistency Checking
```python
class TemporalConsistencyChecker:
    def __init__(self, graph: TemporalKnowledgeGraph):
        self.graph = graph

    def check_consistency(self) -> List[dict]:
        """Check for temporal inconsistencies"""
        inconsistencies = []

        # Check for contradictions
        for node in self.graph.graph.nodes():
            node_data = self.graph.nodes[node]

            # Check if entity is active at multiple conflicting times
            active_times = self._get_active_times(node)
            if self._has_temporal_conflicts(active_times):
                inconsistencies.append({
                    "type": "temporal_conflict",
                    "entity": node,
                    "description": "Entity appears active at conflicting times"
                })

        return inconsistencies

    def _get_active_times(self, entity_id: str) -> List[Tuple[datetime, datetime]]:
        """Get all active time periods for entity"""
        # Simplified - extract from temporal graph
        return []

    def _has_temporal_conflicts(self, active_times: List[Tuple[datetime, datetime]]) -> bool:
        """Check if time periods conflict"""
        # Check for overlapping periods
        for i, (start1, end1) in enumerate(active_times):
            for start2, end2 in active_times[i+1:]:
                if self._periods_overlap(start1, end1, start2, end2):
                    return True
        return False

    def _periods_overlap(self, start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
        """Check if two time periods overlap"""
        return start1 < end2 and start2 < end1
```

## Integration with Vector RAG and GraphRAG

### Hybrid Temporal Retrieval
```python
class TemporalGraphRAG:
    def __init__(self, temporal_graph: TemporalKnowledgeGraph, vector_db):
        self.temporal_graph = temporal_graph
        self.vector_db = vector_db

    def retrieve(self, query: str, time_constraint: Optional[str] = None) -> List[dict]:
        """Retrieve using temporal + semantic search"""

        # Parse temporal constraints
        start, end = self._parse_time_constraint(time_constraint)

        # Get temporal results
        temporal_results = self._retrieve_temporal(start, end)

        # Get semantic results
        semantic_results = self.vector_db.query(
            query_embeddings=[self._embed_query(query)],
            n_results=10
        )

        # Combine and rank
        combined = self._combine_results(temporal_results, semantic_results, query)

        return combined

    def _retrieve_temporal(self, start: Optional[datetime], end: Optional[datetime]) -> List[dict]:
        """Retrieve from temporal graph"""
        if start and end:
            return self.temporal_graph.get_events_between(start, end)
        elif start:
            return self.temporal_graph.get_entities_active_at(start)
        else:
            return []
```

## Best Practices

### Do's
GOOD Use proper time representations (datetime objects)
GOOD Index temporal information for fast retrieval
GOOD Validate temporal consistency
GOOD Handle time zones appropriately
GOOD Support both instantaneous events and time periods
GOOD Use temporal reasoning for better context

### Don'ts
BAD Don't ignore time zones
BAD Don't use string representations for time
BAD Don't store all events without indexing
BAD Don't forget temporal consistency checks
BAD Don't assume time flows linearly
BAD Don't ignore uncertainty in temporal data

## Applications

### Use Case 1: Event Tracking
- Track events over time
- Find patterns and trends
- Predict future events

### Use Case 2: Historical Analysis
- Understand historical context
- Analyze temporal trends
- Extract temporal insights

### Use Case 3: Predictive Analytics
- Predict future states
- Forecast events
- Model temporal evolution

### Use Case 4: Audit and Compliance
- Track changes over time
- Verify temporal sequences
- Ensure compliance with time-based rules
