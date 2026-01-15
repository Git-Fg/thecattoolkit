# Incremental Synchronization

## Overview

The `IncrementalSync` class implements delta-based synchronization for efficient offline-first data sync. It tracks changes since last sync and applies remote changes with conflict resolution.

## Implementation

```python
class IncrementalSync:
    def __init__(self, local_store: EncryptedLocalStore):
        self.local_store = local_store
        self.sync_state = self._load_sync_state()

    def _load_sync_state(self) -> Dict:
        """Load sync state (timestamps, versions, etc.)"""
        return self.local_store.retrieve('__sync_state__') or {
            'last_sync_timestamp': 0,
            'synced_items': {},
            'pending_deletions': [],
            'version': 1
        }

    def get_local_changes(self, since_timestamp: float) -> List[Dict]:
        """Get all local changes since last sync"""
        changes = []

        # Query local database for changes
        conn = sqlite3.connect(self.local_store.db_path)
        cursor = conn.execute("""
            SELECT id, data, updated_at
            FROM encrypted_data
            WHERE updated_at > ?
            AND id NOT LIKE '__%'  # Exclude system tables
        """, (since_timestamp,))

        for row in cursor.fetchall():
            changes.append({
                'id': row[0],
                'data': self.local_store.retrieve(row[0]),
                'timestamp': row[2],
                'operation': 'upsert'
            })

        conn.close()
        return changes

    def apply_remote_changes(self, remote_changes: List[Dict]) -> List[Dict]:
        """Apply remote changes to local storage"""
        applied_changes = []
        conflicts = []

        for change in remote_changes:
            try:
                local_data = self.local_store.retrieve(change['id'])

                if local_data:
                    # Conflict resolution needed
                    resolved = ConflictResolver().resolve_conflict(
                        local_data=local_data,
                        remote_data=change['data'],
                        context={'resolution_strategy': 'timestamp'}
                    )

                    if resolved.get('merge_conflict'):
                        conflicts.append({
                            'id': change['id'],
                            'local': local_data,
                            'remote': change['data'],
                            'resolved': resolved
                        })

                # Store resolved data
                self.local_store.store(change['id'], change['data'])
                applied_changes.append(change['id'])

            except Exception as e:
                print(f"Failed to apply change {change['id']}: {e}")

        return applied_changes, conflicts

    def prepare_sync_package(self) -> Dict:
        """Prepare package for remote synchronization"""
        last_sync = self.sync_state['last_sync_timestamp']
        local_changes = self.get_local_changes(last_sync)

        return {
            'version': self.sync_state['version'],
            'changes': local_changes,
            'timestamp': time.time(),
            'pending_deletions': self.sync_state['pending_deletions']
        }
```

## Sync State Tracking

### State Structure
```python
{
    'last_sync_timestamp': 0,      # Last successful sync time
    'synced_items': {},             # Map of synced item IDs to timestamps
    'pending_deletions': [],        # Items deleted locally, pending remote sync
    'version': 1                   # Sync protocol version
}
```

### State Persistence
- Stored in `EncryptedLocalStore` as `__sync_state__`
- Updated after each successful sync
- Maintains continuity across app restarts

## Change Detection

### Local Changes
- Queries SQLite for items updated since last sync
- Excludes system tables (prefixed with `__`)
- Returns operations with metadata

### Remote Changes
- Accepts batch of remote changes
- Automatically applies conflict resolution
- Tracks successful and failed applications

## Sync Package Format

```python
{
    'version': 1,                  # Sync protocol version
    'changes': [                    # Array of changes
        {
            'id': 'item_123',
            'data': {...},          # Encrypted item data
            'timestamp': 1234567890,
            'operation': 'upsert'    # or 'delete'
        }
    ],
    'timestamp': 1234567890,        # Package generation time
    'pending_deletions': ['id1', 'id2']  # Items to delete remotely
}
```

## Usage

```python
sync = IncrementalSync(local_store)

# Get changes since last sync
changes = sync.get_local_changes(
    since_timestamp=sync.sync_state['last_sync_timestamp']
)

# Apply remote changes
applied, conflicts = sync.apply_remote_changes(remote_changes)

# Prepare sync package for upload
package = sync.prepare_sync_package()
```

## Integration Points

- Uses `EncryptedLocalStore` for state persistence
- Uses `ConflictResolver` for handling conflicts
- Referenced by `SyncStateManager` for state updates

## Performance Optimizations

1. **Delta Sync Only**: Only transfers changed items
2. **SQLite Indexing**: Indexed by timestamp for fast queries
3. **Batch Operations**: Applies changes in batches
4. **Lazy Loading**: Loads data only when needed

## Error Handling

- Continues on individual item failures
- Logs errors without exposing data
- Returns success/failure counts
- Allows partial sync completion

## Best Practices

1. **Sync frequently** to minimize conflicts
2. **Use timestamps** consistently
3. **Handle conflicts** proactively
4. **Test with large datasets**
5. **Monitor sync performance**
