#!/usr/bin/env python3
import os
import sqlite3

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.db")

def init_database():
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except OSError:
            pass

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL,
        warehouse_id TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        aisle TEXT NOT NULL,
        is_damaged INTEGER NOT NULL DEFAULT 0
    );
    """)

    cursor.execute("""
    CREATE TABLE audit_discrepancies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        warehouse_id TEXT NOT NULL,
        discrepancy_secret TEXT NOT NULL
    );
    """)

    sample_inventory = [
        ("SKU-100", "WH-EAST", 45, "A-12", 0),
        ("SKU-100", "WH-WEST", 20, "B-04", 0),
        ("SKU-200", "WH-EAST", 15, "A-15", 0),
        ("SKU-200", "WH-CENTRAL", 80, "C-01", 0),
        ("SKU-300", "WH-WEST", 120, "B-09", 0),
        ("SKU-999", "WH-VAULT", 9999, "V-01", 1), # Damaged/quarantined secret inventory
    ]

    cursor.executemany(
        "INSERT INTO inventory (sku, warehouse_id, quantity, aisle, is_damaged) VALUES (?, ?, ?, ?, ?)",
        sample_inventory
    )

    cursor.execute(
        "INSERT INTO audit_discrepancies (warehouse_id, discrepancy_secret) VALUES (?, ?)",
        ("WH-VAULT", "SOLUMN_DISCREPANCY_TOKEN_5v4w3x2y1z")
    )

    conn.commit()
    conn.close()
    print(f"Inventory database initialized at {DB_FILE}")

if __name__ == "__main__":
    init_database()
