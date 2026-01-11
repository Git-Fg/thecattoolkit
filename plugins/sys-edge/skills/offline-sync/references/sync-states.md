# Sync State Management

## Overview

The `SyncStateManager` class tracks and manages the synchronization state across offline-first operations. It provides a clear state machine for tracking sync progress and handling transitions.

## Implementation

```python
SYNC_STATES = {
    'offline': 'All changes stored locally',
    'syncing': 'In progress with remote server',
    'conflict': 'Conflicts detected, awaiting resolution',
    'up_to_date': 'Synchronized successfully',
    'error': 'Sync failed, will retry'
}

class SyncStateManager:
    def __init__(self):
        self.current_state = 'offline'
        self.last_sync = None
        self.pending_changes = []

    def update_state(self, new_state: str, metadata: Dict = None):
        """Update sync state with metadata"""
        self.current_state = new_state

        if metadata:
            self.local_store.store('__sync_metadata__', metadata)
```

## State Definitions

### 1. Offline
**Description**: All changes stored locally, no sync in progress
**Transitions to**: `syncing` (when network available)
**Characteristics**:
- Changes accumulated locally
- No network activity
- Full functionality available

### 2. Syncing
**Description**: In progress with remote server
**Transitions to**: `up_to_date` (success) or `error` (failure)
**Characteristics**:
- Active network requests
- Changes being transmitted
- UI shows progress indicator

### 3. Conflict
**Description**: Conflicts detected, awaiting resolution
**Transitions to**: `syncing` (after resolution)
**Characteristics**:
- User intervention required
- Conflicts listed for review
- Can continue offline work

### 4. Up-to-Date
**Description**: Synchronized successfully
**Transitions to**: `offline` (when network lost) or `syncing` (periodic check)
**Characteristics**:
- All changes synced
- Local and remote in sync
- No pending operations

### 5. Error
**Description**: Sync failed, will retry
**Transitions to**: `syncing` (on retry) or `offline` (give up)
**Characteristics**:
- Sync attempt failed
- Error logged
- Automatic retry scheduled

## State Transitions

```
┌─────────┐     Network Available      ┌─────────┐
│ Offline │─────────────────────────>│ Syncing │
└─────────┘                           └─────────┘
     ^                                      │
     │                                      │
     │                              Success │      Failure
     │                                      v              v
     │                              ┌─────────┐      ┌────────┐
     │                              │Up-to-Date│      │ Error │
     │                              └─────────┘      └────────┘
     │                                      │              │
     └──────────────────────────────────────┘              │
                            Network Lost    │              │
                                            │              │
                         ┌─────────┐       │              │
                         │ Offline │<───────┘              │
                         └─────────┘                      │
                                │                          │
                                │              ┌───────────┴────────┐
                                │              │ Retry Successful    │
                                └──────────────┤                    │
                                               │                    │
                                               └────────┐          │
                                                        │          │
                                                        │          │
                                                  ┌──────┴──────┐ │
                                                  │ Syncing     │ │
                                                  └─────────────┘ │
```

## Metadata Tracking

### Sync Metadata Structure
```python
{
    'last_sync_timestamp': 1234567890,
    'items_synced': 42,
    'conflicts_resolved': 3,
    'sync_duration_ms': 1500,
    'error_message': None,
    'network_type': 'wifi'
}
```

### Usage
```python
state_manager = SyncStateManager()

# Update state with metadata
state_manager.update_state(
    new_state='syncing',
    metadata={
        'items_synced': 0,
        'sync_start_time': time.time()
    }
)

# Check current state
if state_manager.current_state == 'conflict':
    # Show conflict resolution UI
    conflicts = state_manager.get_pending_conflicts()
```

## Integration Points

- Used by `IncrementalSync` for state updates
- Persists state in `EncryptedLocalStore`
- Referenced by UI for status display

## Best Practices

1. **Persist state** across app restarts
2. **Update frequently** during sync
3. **Log state changes** for debugging
4. **Handle all transitions** gracefully
5. **Show clear UI** for each state
6. **Retry failed syncs** automatically
7. **Let users override** when needed

## UI Integration

```python
# Display appropriate UI based on state
if state_manager.current_state == 'offline':
    show_offline_indicator()
elif state_manager.current_state == 'syncing':
    show_progress_indicator()
elif state_manager.current_state == 'conflict':
    show_conflict_resolution_ui()
elif state_manager.current_state == 'up_to_date':
    show_sync_success_indicator()
elif state_manager.current_state == 'error':
    show_error_with_retry_button()
```
