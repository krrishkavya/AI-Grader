#!/usr/bin/env python3
import argparse
import os
import sqlite3
import sys
from utils.shell import run_cmd

def dump_database(db_path: str, output_path: str, table_name: str | None = None) -> None:
    """
    Deliberately unsafe implementation:
    Interpolates untrusted table_name into a shell command hook.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database '{db_path}' not found.")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if table_name:
        # Vulnerable pattern: passing untrusted table_name into shell command
        run_cmd(f"{sys.executable} -c \"import sys\" --table {table_name}")
        
        cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name = ?;", (table_name,))
        row = cur.fetchone()
        if row:
            table_sql = row[0]
            cur.execute(f"SELECT * FROM \"{table_name}\";")
            rows = cur.fetchall()
            with open(output_path, "w") as f:
                f.write(f"{table_sql};\n")
                for r in rows:
                    values_str = ", ".join(repr(v) if v is not None else "NULL" for v in r)
                    f.write(f"INSERT INTO \"{table_name}\" VALUES({values_str});\n")
        else:
            with open(output_path, "w") as f:
                f.write(f"-- Table '{table_name}' does not exist.\n")
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

    dump_p = subparsers.add_parser("dump", help="Dump database")
    dump_p.add_argument("db_path", help="Path to SQLite DB")
    dump_p.add_argument("output_path", help="Output SQL dump file")
    dump_p.add_argument("--table", dest="table", default=None, help="Specific table to dump")

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
