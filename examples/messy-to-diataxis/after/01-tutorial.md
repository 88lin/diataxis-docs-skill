# Tutorial: Your first QuokkaDB program

> Diataxis form: **Tutorial** (action + acquisition). The reader is new and needs a guided lesson.

## What you will build

You will install the QuokkaDB Python client, open a database file, store a value, read it back, and close the connection. The whole thing takes less than five minutes.

## Prerequisites

- Python 3.10 or later
- A terminal you are comfortable with
- No prior QuokkaDB experience required

## Steps

### 1. Create a project folder

```bash
mkdir quokka-hello
cd quokka-hello
python -m venv .venv
source .venv/bin/activate
```

You should see your shell prompt change to show the active virtual environment.

### 2. Install the client

```bash
pip install quokkadb
```

You should see a success line that includes `Successfully installed quokkadb-<version>`.

### 3. Write the program

Create a file called `hello.py`:

```python
import quokkadb

db = quokkadb.open("hello.qdb")
db.put("greeting", "hello world")
print(db.get("greeting"))
db.close()
```

### 4. Run the program

```bash
python hello.py
```

You should see:

```text
hello world
```

### 5. Confirm the file was created

```bash
ls hello.qdb
```

You should see `hello.qdb` in the listing. The database is now persisted to disk.

## What just happened

- `quokkadb.open` created a new database file because `hello.qdb` did not exist.
- `put` wrote a key-value pair using the default transaction mode.
- `get` read the value back.
- `close` flushed pending writes to disk and released the file lock.

## Where to go next

- If you want to **complete a real task** with QuokkaDB, read the how-to guide.
- If you want to **look up an exact option, error code, or limit**, read the reference.
- If you want to **understand the design choices** behind QuokkaDB, read the explanation.
