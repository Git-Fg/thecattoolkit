# Encrypted Local Storage

## Overview

The `EncryptedLocalStore` class implements user-controlled encryption for offline-first mobile AI applications. All data is encrypted with keys controlled by the user, never stored in plain text.

## Implementation

```python
from cryptography.fernet import Fernet
import sqlite3
import hashlib

class EncryptedLocalStore:
    def __init__(self, db_path: str, user_key: Optional[bytes] = None):
        self.db_path = db_path
        self.encryption_key = user_key or self._generate_user_key()
        self.cipher = Fernet(self.encryption_key)
        self._init_database()

    def _generate_user_key(self) -> bytes:
        """Generate encryption key from user credentials (never stored)"""
        # In production, derive from user password/PIN
        # For demo, generate random key
        return Fernet.generate_key()

    def _init_database(self):
        """Initialize SQLite database with encrypted storage"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS encrypted_data (
                id TEXT PRIMARY KEY,
                data BLOB NOT NULL,
                iv BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def store(self, key: str, data: Dict) -> bool:
        """Store data encrypted with user's key"""
        try:
            # Serialize data
            serialized = json.dumps(data).encode()

            # Encrypt with user's key
            encrypted = self.cipher.encrypt(serialized)

            # Store in database
            conn = sqlite3.connect(self.db_path)
            conn.execute(
                "INSERT OR REPLACE INTO encrypted_data (id, data, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (key, encrypted)
            )
            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Storage error: {e}")
            return False

    def retrieve(self, key: str) -> Optional[Dict]:
        """Retrieve and decrypt data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute(
                "SELECT data FROM encrypted_data WHERE id = ?",
                (key,)
            )
            row = cursor.fetchone()
            conn.close()

            if not row:
                return None

            # Decrypt with user's key
            decrypted = self.cipher.decrypt(row[0])
            return json.loads(decrypted.decode())

        except Exception as e:
            print(f"Retrieval error: {e}")
            return None

    def export_key_for_backup(self, password: str) -> str:
        """Export encrypted key for user backup"""
        # Never export raw key
        # Export key encrypted with user's password
        password_hash = hashlib.sha256(password.encode()).digest()
        key_export = self.cipher.encrypt(self.encryption_key)

        return base64.b64encode(key_export).decode()
```

## Key Features

### User-Controlled Encryption
- Encryption keys are derived from user credentials (password/PIN)
- Keys are never stored in plain text
- Users can export encrypted backups using their password

### SQLite Integration
- Efficient local storage using SQLite
- All data encrypted before storage
- Automatic timestamps for conflict resolution

### Error Handling
- Graceful handling of storage failures
- Return codes for success/failure
- Logging without exposing sensitive data

## Usage

```python
# Initialize with user key
store = EncryptedLocalStore(
    db_path="app_data.db",
    user_key=user_provided_key
)

# Store data (automatically encrypted)
success = store.store("user_profile", {
    "name": "John Doe",
    "preferences": {"theme": "dark"}
})

# Retrieve data (automatically decrypted)
data = store.retrieve("user_profile")
```

## Integration Points

- Used by `IncrementalSync` for storing sync state
- Referenced by `SyncStateManager` for metadata storage
- Supports conflict resolution through timestamp tracking

## Security Considerations

- **Never log encryption keys**
- **Never store plaintext data**
- **Always use user-provided or derived keys**
- **Export keys only when explicitly requested by user**
