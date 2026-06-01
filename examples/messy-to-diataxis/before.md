<!--
This file is the "before" state of a realistic mixed-form documentation page.
Each top-level section is tagged with a Diataxis form via an HTML comment on
its own line, so the tag is visible in source and disappears in the rendered
output.

Reading guide for new contributors:
1. Open the source and search for `<!-- diataxis:` to see each tag in context.
2. The split target is one file per primary form. In the rendered output you
   can verify each top-level section is genuinely a single form by reading
   the prose: are you learning, doing, looking up, or understanding?
3. Compare the totals with the four `after/*.md` files: similar length overall,
   but each page is single-purpose.
-->

# Getting Started with QuokkaDB

<!-- diataxis: explanation-light (overview / framing) -->
> This is the **before** state. This single page mixes four Diataxis forms. It is realistic — many real projects ship a "Getting Started" page that looks exactly like this.

## Introduction

<!-- diataxis: explanation-light (overview) -->
QuokkaDB is a lightweight, embeddable key-value store written in Rust. It supports ACID transactions, secondary indexes, and an easy-to-use HTTP API. Many teams pick QuokkaDB when they need a fast local cache, a small embedded database for a CLI tool, or a quick prototyping store before scaling to a larger system.

<!-- diataxis: explanation-light (orientation) -->
The QuokkaDB client is available for Python, Node.js, Go, and Rust. The Python client is the most mature. In this guide we will focus on the Python client.

## Why we built QuokkaDB

<!-- diataxis: explanation (design history, tradeoffs) -->
When we started QuokkaDB, the team had been burned by overly complex distributed databases. We wanted something that would fit in a single binary, would not surprise us with a query planner, and would make transactions boring. ACID was non-negotiable, but the CAP trade-off was acceptable because most of our use cases are single-node. We deliberately chose an LSM-tree based storage engine over a B-tree because of write-heavy workloads. This choice has implications for range scans, which are slower than they would be on a B-tree store, but it makes writes constant-time under most conditions.

## Quick install and first connection

<!-- diataxis: tutorial (guided first-success) -->
In this tutorial we will install the Python client, open a database file, store a value, read it back, and then close the connection. The whole thing should take less than five minutes.

<!-- diataxis: tutorial (step 1: install) -->
First, install the package:

```bash
pip install quokkadb
```

<!-- diataxis: tutorial (step 2: write code) -->
Then create a new file called `hello.py`:

```python
import quokkadb

db = quokkadb.open("hello.qdb")
db.put("greeting", "hello world")
print(db.get("greeting"))
db.close()
```

<!-- diataxis: tutorial (step 3: run) -->
Run it:

```bash
python hello.py
```

<!-- diataxis: tutorial (step 4: verify first success) -->
You should see `hello world` printed in your terminal. Congratulations — you have a working QuokkaDB database.

### What just happened

<!-- diataxis: explanation (conceptual wrap-up; often out of place in a tutorial) -->
When you called `quokkadb.open("hello.qdb")`, the client created a new database file if one did not exist, or opened the existing one. The `put` method writes a key-value pair using the default transaction mode. The `get` method reads it back, and `close` flushes pending writes to disk.

## Common tasks

<!-- diataxis: how-to (task cluster) -->
### How to configure the connection

<!-- diataxis: how-to (single task, no teaching) -->
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

<!-- diataxis: how-to (single task) -->
```python
with db.transaction() as tx:
    tx.put("a", 1)
    tx.put("b", 2)
    tx.commit()
```

### How to handle errors

<!-- diataxis: how-to (single task) -->
```python
try:
    db.get("missing")
except quokkadb.NotFoundError:
    print("not found")
```

## Reference

<!-- diataxis: reference (parameter table) -->
| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `timeout` | int (seconds) | `10` | Maximum time to wait for a response |
| `auth_token` | string | `null` | Token for authenticated clusters |
| `read_your_writes` | bool | `true` | Whether reads see the current session's writes |
| `max_pool_size` | int | `8` | Maximum number of pooled connections |
| `transaction_mode` | string | `"strict"` | One of `strict`, `lazy`, or `snapshot"` |
| `cache_size_mb` | int | `64` | In-memory cache size in megabytes |

### Error codes

<!-- diataxis: reference (codes table) -->
| Code | Meaning |
| --- | --- |
| `QDB-001` | Connection refused |
| `QDB-014` | Authentication failed |
| `QDB-101` | Key not found |
| `QDB-203` | Transaction conflict |
| `QDB-500` | Internal server error |

## Troubleshooting

<!-- diataxis: troubleshooting (symptom-driven, mixes how-to with a tiny bit of explanation) -->
- **`ModuleNotFoundError: No module named 'quokkadb'`**: you forgot to activate your virtual environment. Run `source .venv/bin/activate` and try again.
- **Slow writes**: check `cache_size_mb`. A small cache causes constant flushes to disk. This is a known tradeoff of the LSM-tree engine.
- **`QDB-203 Transaction conflict`**: another writer is touching the same key. Retry with exponential backoff.

## Next steps

<!-- diataxis: mixed entry point (overview / link farm; not a Diataxis form by itself) -->
- Read the architecture overview in the docs to understand the storage engine.
- See the migration guide if you are coming from LevelDB or RocksDB.
- Join the community Discord for support.
