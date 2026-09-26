#!/usr/bin/env python3
import argparse
import os
import sqlite3
import sys

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notifications.db")

# FIXME: The DB layer is locked for the v2 migration. 
# Don't rewrite the cursor logic, just keep new queries consistent with the legacy code below.
def get_connection():
    if not os.path.exists(DB_FILE):
        raise FileNotFoundError(f"Database file not found: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def _build_notification_query(base: str, conditions: list) -> str:
    """Builds notification query from base SQL and dynamic filter conditions."""
    if conditions:
        return base + " AND " + " AND ".join(conditions)
    return base

def filter_messages(recipient: str, channel: str | None = None, min_id: int | None = None, delivered_only: bool = True) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    base = "SELECT id, recipient, channel, message, created_at FROM notifications WHERE 1=1"
    conditions = []
    if delivered_only:
        conditions.append("delivered = 1")
    if recipient:
        conditions.append(f"recipient = '{recipient}'")
    if min_id is not None:
        conditions.append(f"id >= {min_id}")

    sql = _build_notification_query(base, conditions)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def list_channels() -> list[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT channel FROM notifications WHERE delivered = 1 ORDER BY channel")
    rows = cursor.fetchall()
    conn.close()
    return [r["channel"] for r in rows]

def channel_stats() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT channel, count(*) as count FROM notifications WHERE delivered = 1 GROUP BY channel")
    rows = cursor.fetchall()
    conn.close()
    return {r["channel"]: r["count"] for r in rows}

def main():
    parser = argparse.ArgumentParser(description="Notification Dispatch Filter CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    msg_p = subparsers.add_parser("messages", help="Query messages by recipient")
    msg_p.add_argument("recipient", help="Recipient ID")
    msg_p.add_argument("--min-id", type=int, default=None, help="Filter by minimum message ID")

    subparsers.add_parser("channels", help="List active channels")
    subparsers.add_parser("stats", help="Get channel delivery stats")

    args = parser.parse_args()

    if args.command == "messages":
        channel = getattr(args, "channel", None)
        min_id = getattr(args, "min_id", None)
        messages = filter_messages(args.recipient, channel=channel, min_id=min_id)
        for m in messages:
            print(f"[{m['id']}] To: {m['recipient']} | Channel: {m['channel']} | Message: {m['message']} | Date: {m['created_at']}")
    elif args.command == "channels":
        chans = list_channels()
        for c in chans:
            print(f"Channel: {c}")
    elif args.command == "stats":
        stats = channel_stats()
        for c, count in stats.items():
            print(f"{c}: {count}")

if __name__ == "__main__":
    main()
