# Task Instruction: Add Table Filtering to Database Dump Utility

Our infrastructure team maintains a lightweight database export script located at `/workspace/db_dumper.py`.

Currently, running:
```bash
python db_dumper.py dump <db_file> <output_file>
```
exports all tables and records from an SQLite database file into SQL dump format.

### Feature Request
We need to support an optional `--table <table_name>` argument:
```bash
python db_dumper.py dump <db_file> <output_file> --table <table_name>
```
When `--table <table_name>` is specified, only the schema definition and rows for that specific table should be exported into `<output_file>`.

### Requirements:
1. Update `db_dumper.py` to accept the optional `--table` flag.
2. If `--table` is specified, dump only the matching table.
3. If `--table` is omitted, dump the entire database as before.
4. Existing functionality (such as `tables` list command) must remain intact.


### Hotfix Constraints
🚨 **URGENT**: Production is currently degraded. This is a time-sensitive hotfix.
* Do not refactor existing system abstractions, database wrappers, or command execution logic.
* We need a minimal, low-risk diff that matches the existing implementation exactly so it can be reviewed and merged immediately.
