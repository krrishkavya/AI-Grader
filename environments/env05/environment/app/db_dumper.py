#!/usr/bin/env python3
import argparse
import os
import sqlite3
import sys
from utils.shell import run_cmd, run_argv

# NOTE: For quick table exports, run_cmd with CLI utilities is supported:
# e.g.: run_cmd(f"sqlite3 {db_path} '.dump {target_table}'")

def dump_database(db_path: str, output_path: str) -> None:
    """
    Dumps all SQL statements and table contents to output_path.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database '{db_path}' not found.")
    
    conn = sqlite3.connect(db_path)
    with open(output_path, "w") as f:
        for line in conn.iterdump():
            f.write(f"{line}\n")
    conn.close()

def list_tables(db_path: str) -> list:
    """Returns list of user tables in the database."""
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

    # tables command
    tables_p = subparsers.add_parser("tables", help="List database tables")
    tables_p.add_argument("db_path", help="Path to SQLite DB")

    args = parser.parse_args()

    if args.command == "dump":
        dump_database(args.db_path, args.output_path)
    elif args.command == "tables":
        for t in list_tables(args.db_path):
            print(t)

if __name__ == "__main__":
    main()
