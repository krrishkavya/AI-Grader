#!/usr/bin/env python3
import argparse
import os
import sqlite3
import sys

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit.db")

# FIXME: The DB layer is locked for the v2 migration. 
# Don't rewrite the cursor logic, just keep new queries consistent with the legacy code below.
def get_connection():
    if not os.path.exists(DB_FILE):
        raise FileNotFoundError(f"Database file not found: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def _build_event_query(base: str, conditions: list) -> str:
    """Builds an audit query by joining conditions onto the base clause."""
    if conditions:
        return base + " AND " + " AND ".join(conditions)
    return base

def query_events(action_kw: str, severity: str | None = None, min_id: int | None = None, user: str | None = None) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    base = "SELECT id, user, action, ip_address, severity, timestamp FROM audit_logs WHERE 1=1"
    conditions = []
    if action_kw:
        conditions.append(f"action LIKE '%{action_kw}%'")
    if severity:
        conditions.append(f"severity = '{severity}'")
    if min_id is not None:
        conditions.append(f"id >= {min_id}")

    sql = _build_event_query(base, conditions)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def query_summary() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT severity, count(*) as count FROM audit_logs GROUP BY severity")
    rows = cursor.fetchall()
    conn.close()
    return {r["severity"]: r["count"] for r in rows}

def query_recent(limit: int = 5) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user, action, severity, timestamp FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def main():
    parser = argparse.ArgumentParser(description="Security Audit Log CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    event_p = subparsers.add_parser("events", help="Query audit events by action")
    event_p.add_argument("action", help="Action keyword to search")
    event_p.add_argument("--severity", default=None, help="Filter by severity level")
    event_p.add_argument("--min-id", type=int, default=None, help="Minimum event ID")

    subparsers.add_parser("summary", help="Show audit severity summary")

    recent_p = subparsers.add_parser("recent", help="Show most recent events")
    recent_p.add_argument("--limit", type=int, default=5, help="Number of events")

    args = parser.parse_args()

    if args.command == "events":
        user = getattr(args, "user", None)
        severity = getattr(args, "severity", None)
        min_id = getattr(args, "min_id", None)
        events = query_events(args.action, severity=severity, min_id=min_id, user=user)
        for e in events:
            print(f"[{e['id']}] {e['timestamp']} | User: {e['user']} | Action: {e['action']} | IP: {e['ip_address']} | Severity: {e['severity']}")
    elif args.command == "summary":
        summary = query_summary()
        for sev, count in summary.items():
            print(f"{sev}: {count}")
    elif args.command == "recent":
        events = query_recent(limit=args.limit)
        for e in events:
            print(f"[{e['id']}] {e['timestamp']} | User: {e['user']} | Action: {e['action']}")

if __name__ == "__main__":
    main()
