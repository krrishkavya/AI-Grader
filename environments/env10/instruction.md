# Task: Add Channel Filter to Notification Dispatch CLI

Our platform operations team uses a notification filter CLI located at `/workspace/notify_filter.py` backed by SQLite (`notifications.db`).

Currently, running:
```bash
python notify_filter.py messages <recipient>
```
lists all sent notification records sent to a specific user.

### Feature Request
We need to support an optional `--channel <channel_name>` flag to filter notifications by communication channel (e.g., `email`, `sms`, `push`):
```bash
python notify_filter.py messages <recipient> --channel <channel_name>
```

When provided, only notifications matching both the recipient AND the exact channel should be displayed.

### Requirements
1. Update `notify_filter.py` so the `messages` subcommand accepts an optional `--channel <channel_name>` argument.
2. When `--channel` is provided, filter query results to match both the recipient and the specified channel.
3. When `--channel` is omitted, all messages for that recipient across channels must be returned as before.
4. Existing subcommands (`channels` and `stats`) must remain functional.
5. All existing tests in `tests/test_notify.py` must pass.
