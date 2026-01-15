# Conflict Resolution

## Overview

The `ConflictResolver` class implements intelligent strategies for resolving data conflicts during offline-first synchronization. It supports multiple resolution strategies and automatically detects conflict types.

## Implementation

```python
class ConflictResolver:
    def __init__(self):
        self.resolution_strategies = {
            'timestamp': self._resolve_by_timestamp,
            'priority': self._resolve_by_priority,
            'merge': self._resolve_by_merging,
            'user_choice': self._resolve_by_user_choice
        }

    def resolve_conflict(self, local_data: Dict, remote_data: Dict, context: Dict) -> Dict:
        """Resolve sync conflicts using appropriate strategy"""
        conflict_type = self._detect_conflict_type(local_data, remote_data)

        if conflict_type == 'no_conflict':
            return remote_data if context.get('prefer_remote', False) else local_data

        strategy = context.get('resolution_strategy', 'timestamp')
        resolver = self.resolution_strategies[strategy]

        return resolver(local_data, remote_data, context)

    def _resolve_by_timestamp(self, local: Dict, remote: Dict, context: Dict) -> Dict:
        """Use timestamps to resolve conflicts"""
        local_time = local.get('updated_at', 0)
        remote_time = remote.get('updated_at', 0)

        return remote if remote_time > local_time else local

    def _resolve_by_priority(self, local: Dict, remote: Dict, context: Dict) -> Dict:
        """Use data priority to resolve conflicts"""
        local_priority = local.get('priority', 0)
        remote_priority = remote.get('priority', 0)

        return remote if remote_priority > local_priority else local

    def _resolve_by_merging(self, local: Dict, remote: Dict, context: Dict) -> Dict:
        """Merge compatible data structures"""
        merged = local.copy()

        # Merge compatible fields
        for key, value in remote.items():
            if key not in merged:
                merged[key] = value
            elif isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._resolve_by_merging(merged[key], value, context)
            elif isinstance(merged[key], list) and isinstance(value, list):
                # Merge lists, removing duplicates
                merged[key] = list(set(merged[key] + value))

        merged['merged_from'] = {'local': local.get('id'), 'remote': remote.get('id')}
        merged['merge_conflict'] = True

        return merged

    def _detect_conflict_type(self, local: Dict, remote: Dict) -> str:
        """Detect type of conflict"""
        if not remote:
            return 'no_conflict'

        local_id = local.get('id')
        remote_id = remote.get('id')

        if local_id != remote_id:
            return 'different_records'

        local_version = local.get('version', 0)
        remote_version = remote.get('version', 0)

        if local_version != remote_version:
            return 'version_conflict'

        return 'no_conflict'
```

## Resolution Strategies

### 1. Timestamp-Based Resolution
**Use case**: Most common for user-generated content
- Uses `updated_at` timestamps
- Most recent change wins
- Simple and predictable

### 2. Priority-Based Resolution
**Use case**: Administrative or system-generated data
- Uses `priority` field
- Higher priority wins
- Useful for system updates

### 3. Merge-Based Resolution
**Use case**: Complex nested data structures
- Recursively merges dictionaries
- Combines lists (removing duplicates)
- Marks conflicts for review
- Maintains data lineage

### 4. User Choice Resolution
**Use case**: Critical conflicts requiring human input
- Presents options to user
- Records user decision
- Learns from user preferences

## Conflict Detection

The system automatically detects:

- **No Conflict**: Data is identical or compatible
- **Different Records**: Different IDs (not a conflict)
- **Version Conflict**: Same ID, different versions (requires resolution)

## Usage

```python
resolver = ConflictResolver()

# Resolve with timestamp strategy
result = resolver.resolve_conflict(
    local_data=local,
    remote_data=remote,
    context={'resolution_strategy': 'timestamp'}
)

# Resolve with merge strategy
result = resolver.resolve_conflict(
    local_data=local,
    remote_data=remote,
    context={'resolution_strategy': 'merge'}
)
```

## Integration Points

- Used by `IncrementalSync.apply_remote_changes()` for conflict resolution
- Returns conflict metadata for UI display
- Supports custom resolution strategies via context

## Best Practices

1. **Default to timestamp** for user-generated content
2. **Use priority** for system data
3. **Merge cautiously** for complex structures
4. **Log conflicts** for debugging
5. **Test all strategies** with your data types
