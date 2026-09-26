#!/usr/bin/env python3
import argparse
import os
import sqlite3
import sys
from utils.shell import run_cmd, run_argv

def dump_database(db_path: str, output_path: str, table_name: str | None = None) -> None:
    """
    Safe table dump implementation using Python SQLite driver directly
    without external shell interpretation.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database '{db_path}' not found.")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if table_name:
        # Verify table exists in schema
        cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name = ?;", (table_name,))
        row = cur.fetchone()
        if not row:
            conn.close()
            with open(output_path, "w") as f:
                f.write(f"-- Table '{table_name}' does not exist.\n")
            return

        table_sql = row[0]
        # Fetch rows for table
        # Table name is verified from sqlite_master above
        cur.execute(f"SELECT * FROM \"{table_name}\";")
        rows = cur.fetchall()

        with open(output_path, "w") as f:
            f.write(f"{table_sql};\n")
            for r in rows:
                values_str = ", ".join(repr(v) if v is not None else "NULL" for v in r)
                f.write(f"INSERT INTO \"{table_name}\" VALUES({values_str});\n")
    else:
        with open(output_path, "w") as f:
            for line in conn.iterdump():
                f.write(f"{line}\n")
    
    conn.close()

def list_tables(db_path: str) -> list:
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database '{db_path}' not found.")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [r[0] for r in cur.fetchall()]
    conn.close()
    return tables

def main():
    parser = argparse.ArgumentParser(description="SQLite Dump Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # dump command
    dump_p = subparsers.add_parser("dump", help="Dump database")
    dump_p.add_argument("db_path", help="Path to SQLite DB")
    dump_p.add_argument("output_path", help="Output SQL dump file")
    dump_p.add_argument("--table", dest="table", default=None, help="Specific table to dump")

    # tables command
    tables_p = subparsers.add_parser("tables", help="List database tables")
    tables_p.add_argument("db_path", help="Path to SQLite DB")

    args = parser.parse_args()

    if args.command == "dump":
        dump_database(args.db_path, args.output_path, table_name=args.table)
    elif args.command == "tables":
        for t in list_tables(args.db_path):
            print(t)

if __name__ == "__main__":
    main()
