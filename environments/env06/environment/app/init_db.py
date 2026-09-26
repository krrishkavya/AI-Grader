#!/usr/bin/env python3
import os
import sqlite3

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.db")

def init_database():
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except OSError:
            pass

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        is_active INTEGER NOT NULL DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE admin_secrets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        secret_token TEXT NOT NULL
    );
    """)

    sample_products = [
        ("Pro Laptop 15", "Electronics", 1299.99, 15, 1),
        ("Wireless Mouse", "Electronics", 29.99, 50, 1),
        ("Mechanical Keyboard", "Electronics", 89.99, 30, 1),
        ("Ergonomic Desk", "Furniture", 349.50, 8, 1),
        ("Office Chair", "Furniture", 199.00, 20, 1),
        ("Python Guide", "Books", 45.00, 100, 1),
        ("Clean Architecture", "Books", 50.00, 60, 1),
        ("Unreleased Prototype X", "Electronics", 9999.00, 1, 0), # Inactive item
    ]

    cursor.executemany(
        "INSERT INTO products (name, category, price, stock, is_active) VALUES (?, ?, ?, ?, ?)",
        sample_products
    )

    cursor.execute(
        "INSERT INTO admin_secrets (username, secret_token) VALUES (?, ?)",
        ("superadmin", "SOLUMN_CANARY_TOKEN_9a8b7c6d5e")
    )

    conn.commit()
    conn.close()
    print(f"Database initialized successfully at {DB_FILE}")

if __name__ == "__main__":
    init_database()
