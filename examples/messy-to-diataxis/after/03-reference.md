# Reference: QuokkaDB Python client

> Diataxis form: **Reference** (cognition + application). The reader is looking up exact facts.

## Connection options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `timeout` | int (seconds) | `10` | Maximum time to wait for a response. |
| `auth_token` | string | `null` | Token for authenticated clusters. |
| `read_your_writes` | bool | `true` | Whether reads see the current session's writes. |
| `max_pool_size` | int | `8` | Maximum number of pooled connections. |
| `transaction_mode` | string | `"strict"` | One of `strict`, `lazy`, or `snapshot`. |
| `cache_size_mb` | int | `64` | In-memory cache size in megabytes. |

### Example

```python
options = quokkadb.ConnectionOptions(
    timeout=30,
    auth_token="your-token",
    read_your_writes=True,
)
```

## Functions

### `quokkadb.open(path, options=None)`

Opens a database file and returns a `Database` object.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `path` | string | required | Filesystem path to the database file. |
| `options` | `ConnectionOptions` | `None` | Connection options. |

Returns a `Database` object. Raises `ConnectionError` on failure.

### `Database.put(key, value)`

Writes a key-value pair in the default transaction mode.

| Parameter | Type | Description |
| --- | --- | --- |
| `key` | string | The key. |
| `value` | any | The value. Must be JSON-serializable. |

### `Database.get(key)`

Reads a value by key. Raises `NotFoundError` if the key is missing.

### `Database.close()`

Flushes pending writes and releases the file lock.

### `Database.transaction()`

Returns a transaction context manager. The context manager exposes `put`, `delete`, and `commit`. Rollback happens automatically on exception.

## Error codes

| Code | Class | Meaning |
| --- | --- | --- |
| `QDB-001` | `ConnectionError` | Connection refused. |
| `QDB-014` | `AuthError` | Authentication failed. |
| `QDB-101` | `NotFoundError` | Key not found. |
| `QDB-203` | `TransactionConflict` | Transaction conflict; retry. |
| `QDB-500` | `InternalError` | Internal server error. |

## Limits

| Limit | Value |
| --- | --- |
| Maximum key size | 1024 bytes |
| Maximum value size | 16 MB |
| Maximum transaction size | 1 MB |
| Maximum concurrent connections | 256 per process |
