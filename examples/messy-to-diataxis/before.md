# Getting Started with QuokkaDB

> This is the **before** state. This single page mixes four Diataxis forms. It is realistic — many real projects ship a "Getting Started" page that looks exactly like this.

## Introduction

QuokkaDB is a lightweight, embeddable key-value store written in Rust. It supports ACID transactions, secondary indexes, and an easy-to-use HTTP API. Many teams pick QuokkaDB when they need a fast local cache, a small embedded database for a CLI tool, or a quick prototyping store before scaling to a larger system.

The QuokkaDB client is available for Python, Node.js, Go, and Rust. The Python client is the most mature. In this guide we will focus on the Python client.

## Why we built QuokkaDB

When we started QuokkaDB, the team had been burned by overly complex distributed databases. We wanted something that would fit in a single binary, would not surprise us with a query planner, and would make transactions boring. ACID was non-negotiable, but the CAP trade-off was acceptable because most of our use cases are single-node. We deliberately chose an LSM-tree based storage engine over a B-tree because of write-heavy workloads. This choice has implications for range scans, which are slower than they would be on a B-tree store, but it makes writes constant-time under most conditions.

## Quick install and first connection

In this tutorial we will install the Python client, open a database file, store a value, read it back, and then close the connection. The whole thing should take less than five minutes.

First, install the package:

```bash
pip install quokkadb
```

Then create a new file called `hello.py`:

```python
import quokkadb

db = quokkadb.open("hello.qdb")
db.put("greeting", "hello world")
print(db.get("greeting"))
db.close()
```

Run it:

```bash
python hello.py
```

You should see `hello world` printed in your terminal. Congratulations — you have a working QuokkaDB database.

### What just happened

When you called `quokkadb.open("hello.qdb")`, the client created a new database file if one did not exist, or opened the existing one. The `put` method writes a key-value pair using the default transaction mode. The `get` method reads it back, and `close` flushes pending writes to disk.

## Common tasks

### How to configure the connection

Use the `ConnectionOptions` object to configure timeouts, authentication, and replication:

```python
import quokkadb

options = quokkadb.ConnectionOptions(
    timeout=30,
    auth_token="your-token",
    read_your_writes=True,
)
db = quokkadb.open("hello.qdb", options=options)
```

### How to run a transaction

```python
with db.transaction() as tx:
    tx.put("a", 1)
    tx.put("b", 2)
    tx.commit()
```

### How to handle errors

```python
try:
    db.get("missing")
except quokkadb.NotFoundError:
    print("not found")
```

## Reference

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `timeout` | int (seconds) | `10` | Maximum time to wait for a response |
| `auth_token` | string | `null` | Token for authenticated clusters |
| `read_your_writes` | bool | `true` | Whether reads see the current session's writes |
| `max_pool_size` | int | `8` | Maximum number of pooled connections |
| `transaction_mode` | string | `"strict"` | One of `strict`, `lazy`, or `snapshot"` |
| `cache_size_mb` | int | `64` | In-memory cache size in megabytes |

### Error codes

| Code | Meaning |
| --- | --- |
| `QDB-001` | Connection refused |
| `QDB-014` | Authentication failed |
| `QDB-101` | Key not found |
| `QDB-203` | Transaction conflict |
| `QDB-500` | Internal server error |

## Troubleshooting

- **`ModuleNotFoundError: No module named 'quokkadb'`**: you forgot to activate your virtual environment. Run `source .venv/bin/activate` and try again.
- **Slow writes**: check `cache_size_mb`. A small cache causes constant flushes to disk. This is a known tradeoff of the LSM-tree engine.
- **`QDB-203 Transaction conflict`**: another writer is touching the same key. Retry with exponential backoff.

## Next steps

- Read the architecture overview in the docs to understand the storage engine.
- See the migration guide if you are coming from LevelDB or RocksDB.
- Join the community Discord for support.
