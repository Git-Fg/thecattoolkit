---
name: synchronizing-data
description: "Implements offline-first synchronization with encrypted local storage and intelligent conflict resolution for mobile AI applications. Use when building offline-capable mobile apps, implementing sync with privacy requirements, or managing encrypted local data persistence. Do not use for cloud databases, real-time websocket sync, or server-side data management."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Offline-First Sync Protocol



## Core Responsibilities

### 1. Encrypted Local Storage
**User-Controlled Encryption**

- All data encrypted with user-controlled keys
- SQLite database with encryption at rest
- Keys never stored in plain text
- User can export encrypted backups

**Key Features:**
- Fernet encryption for secure storage
- Automatic timestamp tracking
- Efficient query performance
- Export/import capabilities

**Reference:** [encryption.md](references/encryption.md) for complete implementation

### 2. Conflict Resolution
**Intelligent Conflict Resolution**

- Multiple resolution strategies (timestamp, priority, merge)
- Automatic conflict type detection
- User choice for critical conflicts
- Merge-compatible data structures

**Resolution Strategies:**
- **Timestamp**: Most recent change wins
- **Priority**: Higher priority data wins
- **Merge**: Recursively merge compatible structures
- **User Choice**: Explicit user decision

**Reference:** [conflict-resolution.md](references/conflict-resolution.md) for strategies and algorithms

### 3. Incremental Sync
**Delta-Based Synchronization**

- Only sync changed data (delta sync)
- Tracks sync state across sessions
- Handles batch operations efficiently
- Automatic retry on failure

**Sync Components:**
- Local change detection
- Remote change application
- State persistence
- Conflict handling

**Reference:** [incremental-sync.md](references/incremental-sync.md) for sync logic and state management

### 4. Privacy-First Architecture
**Zero-Knowledge Sync**

- Explicit user permission for all data sharing
- Anonymization of sensitive fields
- End-to-end encryption
- Purpose-limited data usage

**Privacy Principles:**
- Data minimization
- Explicit consent
- Encryption everywhere
- Zero-knowledge design

**Reference:** [privacy-first.md](references/privacy-first.md) for anonymization and permission models

## Implementation Patterns

### Pattern 1: Offline-First App Storage
```python
# Initialize encrypted storage
store = EncryptedLocalStore(
    db_path="./app_data.db",
    user_key=user_provided_key
)

# Store data (automatically encrypted)
store.store("user_preferences", {
    "theme": "dark",
    "language": "en",
    "model_preferences": {"quality": "high"}
})

# Data encrypted with user's key, never leaves device unencrypted
```

### Pattern 2: Conflict-Aware Sync
```python
# Configure incremental sync
sync_manager = IncrementalSync(local_store=store)

# Prepare and send sync package
sync_package = sync_manager.prepare_sync_package()
server_response = sync_to_server(sync_package)

# Apply remote changes with automatic conflict resolution
applied, conflicts = sync_manager.apply_remote_changes(
    server_response['changes']
)

# Conflicts automatically resolved, user notified if needed
```

### Pattern 3: Privacy-Preserving Sync
```python
# Request explicit permission
if privacy_sync.request_sync_permission(
    data_type="model_usage_stats",
    purpose="improve_model_quality"
):
    # Sync only anonymized data
    privacy_sync.sync_with_privacy(
        data=usage_stats,
        destination="model_improvement_server"
    )
```

## Sync States

The system operates through clear state transitions:

- **Offline**: All changes stored locally
- **Syncing**: In progress with remote server
- **Conflict**: Conflicts detected, awaiting resolution
- **Up-to-Date**: Synchronized successfully
- **Error**: Sync failed, will retry

**State Management:** [sync-states.md](references/sync-states.md) for state machine and transitions

## Quality Gates

✓ All data encrypted with user-controlled keys
✓ No raw sensitive data transmitted
✓ Conflicts detected and resolved within 24 hours
✓ Sync completes within 30 seconds on stable connection
✓ Offline mode fully functional for 30+ days
✓ User can export/import their encrypted data
✓ Explicit permission for all data sharing
✓ Privacy-preserving sync patterns enforced

## Files Generated

- `encrypted_storage.py`: User-key encrypted local database
- `conflict_resolution.py`: Intelligent conflict resolution strategies
- `incremental_sync.py`: Delta-based synchronization logic
- `privacy_sync.py`: Privacy-preserving sync patterns
- `sync_state_manager.py`: Sync state tracking and management

## Next Steps

1. Initialize `EncryptedLocalStore` with user key
2. Configure conflict resolution strategy
3. Set up incremental sync with state tracking
4. Implement privacy-first permission system
5. Test sync across network disruptions
6. Verify encryption and privacy guarantees
7. Add sync state monitoring to UI
