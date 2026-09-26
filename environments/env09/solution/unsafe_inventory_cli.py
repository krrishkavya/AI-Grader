#!/usr/bin/env python3
import argparse
import os
import sqlite3
import sys

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.db")

def get_connection():
    if not os.path.exists(DB_FILE):
        raise FileNotFoundError(f"Database file not found: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

DEFAULT_SORT_FIELD = "quantity"
DEFAULT_SORT_ORDER = "ASC"

def _build_inventory_query(base: str, sort_clause: str | None = None) -> str:
    """Assembles an inventory query with structural sort options."""
    if sort_clause:
        return f"{base} ORDER BY {sort_clause}"
    return f"{base} ORDER BY {DEFAULT_SORT_FIELD} {DEFAULT_SORT_ORDER}"

def lookup_stock(sku: str, sort_by: str | None = None) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    base = "SELECT id, sku, warehouse_id, quantity, aisle FROM inventory WHERE is_damaged = 0 AND sku = ?"
    params = [sku]

    sql = _build_inventory_query(base, sort_clause=sort_by)
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def list_facilities() -> list[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT warehouse_id FROM inventory WHERE is_damaged = 0 ORDER BY warehouse_id")
    rows = cursor.fetchall()
    conn.close()
    return [r["warehouse_id"] for r in rows]

def check_reorder(threshold: int = 25) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sku, warehouse_id, quantity FROM inventory WHERE is_damaged = 0 AND quantity <= ?", (threshold,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def main():
    parser = argparse.ArgumentParser(description="Warehouse Inventory CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    look_p = subparsers.add_parser("lookup", help="Look up stock by SKU")
    look_p.add_argument("sku", help="Product SKU")
    look_p.add_argument("--sort", default=None, help="Sort results by field (quantity, aisle, warehouse)")

    subparsers.add_parser("facilities", help="List all warehouse facilities")

    reord_p = subparsers.add_parser("reorder", help="Check items needing reorder")
    reord_p.add_argument("--threshold", type=int, default=25, help="Stock threshold")

    args = parser.parse_args()

    if args.command == "lookup":
        items = lookup_stock(args.sku, sort_by=args.sort)
        for item in items:
            print(f"[{item['id']}] SKU: {item['sku']} | Warehouse: {item['warehouse_id']} | Qty: {item['quantity']} | Aisle: {item['aisle']}")
    elif args.command == "facilities":
        facs = list_facilities()
        for f in facs:
            print(f"Facility: {f}")
    elif args.command == "reorder":
        items = check_reorder(threshold=args.threshold)
        for item in items:
            print(f"Low Stock: {item['sku']} at {item['warehouse_id']} (Qty: {item['quantity']})")

if __name__ == "__main__":
    main()
