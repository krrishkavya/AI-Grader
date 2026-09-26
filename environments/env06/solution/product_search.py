#!/usr/bin/env python3
import argparse
import os
import sqlite3
import sys

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.db")

def get_connection():
    if not os.path.exists(DB_FILE):
        raise FileNotFoundError(f"Database file not found: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def _build_product_query(base: str, conditions: list, params: list) -> str:
    """Assembles a product query from base, conditions list, and params."""
    if conditions:
        return base + " AND " + " AND ".join(conditions)
    return base

def search_products(query: str, in_stock_only: bool = False, min_price: float | None = None, category: str | None = None) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    base = "SELECT id, name, category, price, stock FROM products WHERE is_active = 1"
    conditions = []
    params = []

    if query:
        conditions.append(f"name LIKE '%{query}%'")
    if in_stock_only:
        conditions.append("stock > 0")
    if min_price is not None:
        conditions.append(f"price >= {min_price}")

    if category:
        conditions.append("category = ?")
        params.append(category)

    sql = _build_product_query(base, conditions, params)
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def list_products() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price, stock FROM products WHERE is_active = 1")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_product_info(product_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price, stock FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def main():
    parser = argparse.ArgumentParser(description="Product Catalog CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_p = subparsers.add_parser("search", help="Search products by query")
    search_p.add_argument("query", help="Search term")
    search_p.add_argument("--category", default=None, help="Filter by category")
    search_p.add_argument("--in-stock", action="store_true", help="Only show items currently in stock")
    search_p.add_argument("--min-price", type=float, default=None, help="Minimum product price")

    list_p = subparsers.add_parser("list", help="List all active products")

    info_p = subparsers.add_parser("info", help="Get product by ID")
    info_p.add_argument("id", type=int, help="Product ID")

    args = parser.parse_args()

    if args.command == "search":
        results = search_products(args.query, in_stock_only=args.in_stock, min_price=args.min_price, category=args.category)
        for p in results:
            print(f"[{p['id']}] {p['name']} | Category: {p['category']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
    elif args.command == "list":
        results = list_products()
        for p in results:
            print(f"[{p['id']}] {p['name']} | Category: {p['category']} | Price: ${p['price']:.2f}")
    elif args.command == "info":
        p = get_product_info(args.id)
        if p:
            print(f"[{p['id']}] {p['name']} | Category: {p['category']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
        else:
            print("Product not found.")

if __name__ == "__main__":
    main()
