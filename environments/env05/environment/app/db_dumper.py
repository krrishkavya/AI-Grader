#!/usr/bin/env python3
import argparse
import os
import sqlite3
import sys
from utils.shell import run_cmd


def dump_database(db_path: str, output_path: str, table: str | None = None) -> None:
    """
    Dumps all SQL statements and table contents to output_path.
    Uses Python sqlite3 for full database dumps (all tables).
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database '{db_path}' not found.")
    
    conn = sqlite3.connect(db_path)
    with open(output_path, "w") as f:
        for line in conn.iterdump():
            f.write(f"{line}\n")
    conn.close()


def list_tables(db_path: str) -> list:
    """Returns list of user tables in the database via sqlite3 CLI."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database '{db_path}' not found.")
    result = run_cmd(f"sqlite3 {db_path} \".tables\"")
    if result.returncode != 0 or not result.stdout.strip():
        # Fallback via Python API if sqlite3 binary unavailable
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cur.fetchall()]
        conn.close()
        return tables
    return result.stdout.strip().split()


def main():
    parser = argparse.ArgumentParser(description="SQLite Dump Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # dump command
    dump_p = subparsers.add_parser("dump", help="Dump database")
    dump_p.add_argument("db_path", help="Path to SQLite DB")
    dump_p.add_argument("output_path", help="Output SQL dump file")

    # tables command
    tables_p = subparsers.add_parser("tables", help="List database tables")
    tables_p.add_argument("db_path", help="Path to SQLite DB")

    args = parser.parse_args()

    if args.command == "dump":
        table = getattr(args, "table", None)
        dump_database(args.db_path, args.output_path, table=table)
    elif args.command == "tables":
        for t in list_tables(args.db_path):
            print(t)

if __name__ == "__main__":
    main()
