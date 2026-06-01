# How-to: configure a QuokkaDB connection

> Diataxis form: **How-to** (action + application). The reader is working and wants to finish a real task.

## Goal

Configure a QuokkaDB connection with custom timeout, authentication, and read-your-writes semantics.

## Before you begin

You should already have the QuokkaDB Python client installed and a database file you can open. If not, complete the [tutorial](01-tutorial.md) first.

You should also have an authentication token if you are connecting to a cluster. Tokens are issued by your cluster administrator.

## Steps

### 1. Import the options object

```python
import quokkadb
```

### 2. Build the options

```python
options = quokkadb.ConnectionOptions(
    timeout=30,
    auth_token="your-token",
    read_your_writes=True,
)
```

### 3. Open the database with the options

```python
db = quokkadb.open("hello.qdb", options=options)
```

### 4. Verify the connection

```python
db.put("__check__", "ok")
print(db.get("__check__"))
```

You should see `ok`.

## Run a transaction

If you need to write several keys atomically, use a transaction:

```python
with db.transaction() as tx:
    tx.put("a", 1)
    tx.put("b", 2)
    tx.commit()
```

If the transaction cannot commit, QuokkaDB raises `TransactionConflict`. Catch it and retry with exponential backoff.

## Handle a missing key

```python
try:
    db.get("missing")
except quokkadb.NotFoundError:
    print("not found")
```

## Results

You now have a connection that:

- waits up to 30 seconds for a response
- authenticates with the supplied token
- always reads the current session's writes

## See also

- Reference: [Connection options, error codes, and limits](03-reference.md)
- Explanation: [Why QuokkaDB chose an LSM-tree engine](04-explanation.md)
