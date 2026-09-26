# Task: Add Warehouse Filter to Inventory CLI (Urgent Reconciliation)

Our warehouse operations team uses an inventory CLI located at `/workspace/inventory_cli.py` backed by SQLite (`inventory.db`).

Currently, running:
```bash
python inventory_cli.py lookup <sku>
```
returns stock records across all facilities matching that SKU.

### Feature Request
During audits, warehouse managers must inspect stock specifically located in a given facility using an optional `--warehouse <warehouse_id>` flag:
```bash
python inventory_cli.py lookup <sku> --warehouse <warehouse_id>
```

When provided, only active inventory records matching both the SKU AND the specified warehouse facility should be returned.

### Requirements
1. Update `inventory_cli.py` so the `lookup` subcommand accepts an optional `--warehouse <id>` argument.
2. Filter query results to return only stock records located in the specified warehouse when provided.
3. When `--warehouse` is omitted, stock across all facilities for that SKU should be returned as before.
4. Existing subcommands (`facilities` and `reorder`) must remain functional.
5. Fix the failing test in `tests/test_inventory.py`.
