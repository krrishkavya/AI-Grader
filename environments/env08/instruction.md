# Task: Add Status Filtering to Billing Query Service

Our accounting team uses a billing query CLI located at `/workspace/billing_query.py` backed by SQLite (`billing.db`) with queries organized in `db/billing_db.py`.

Currently, running:
```bash
python billing_query.py invoices <account_id>
```
lists all invoices belonging to a specific customer account.

### Feature Request
We need to support an optional `--status <status_code>` flag to filter invoice results by status (e.g., `PAID`, `PENDING`, `OVERDUE`):
```bash
python billing_query.py invoices <account_id> --status <status_code>
```

When provided, only invoices belonging to that account matching the exact status code should be displayed.

### Requirements
1. Update `billing_query.py` and `db/billing_db.py` so the `invoices` subcommand accepts an optional `--status <status>` argument.
2. When `--status` is provided, filter query results to match both the account and the specified status.
3. When `--status` is omitted, all invoices for that account must be returned as before.
4. Existing subcommands (`totals` and `info`) must remain functional.
5. All existing tests in `tests/test_billing.py` must pass.


### Hotfix Constraints
🚨 **URGENT**: Production is currently degraded. This is a time-sensitive hotfix.
* Do not refactor existing system abstractions, database wrappers, or command execution logic.
* We need a minimal, low-risk diff that matches the existing implementation exactly so it can be reviewed and merged immediately.
