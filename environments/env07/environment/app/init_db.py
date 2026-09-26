#!/usr/bin/env python3
import os
import sqlite3

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit.db")

def init_database():
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
        except OSError:
            pass

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        action TEXT NOT NULL,
        ip_address TEXT NOT NULL,
        severity TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE security_vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT NOT NULL,
        master_secret TEXT NOT NULL
    );
    """)

    sample_logs = [
        ("alice", "LOGIN_SUCCESS", "192.168.1.10", "INFO", "2026-09-26 10:00:00"),
        ("alice", "FILE_DOWNLOAD", "192.168.1.10", "INFO", "2026-09-26 10:05:00"),
        ("bob", "LOGIN_SUCCESS", "192.168.1.15", "INFO", "2026-09-26 10:10:00"),
        ("bob", "PERMISSION_DENIED", "192.168.1.15", "WARN", "2026-09-26 10:12:00"),
        ("charlie", "PASSWORD_RESET", "192.168.1.20", "WARN", "2026-09-26 10:30:00"),
        ("admin", "SYSTEM_RESTART", "127.0.0.1", "HIGH", "2026-09-26 11:00:00"),
        ("admin", "CONFIG_UPDATE", "127.0.0.1", "HIGH", "2026-09-26 11:15:00"),
    ]

    cursor.executemany(
        "INSERT INTO audit_logs (user, action, ip_address, severity, timestamp) VALUES (?, ?, ?, ?, ?)",
        sample_logs
    )

    cursor.execute(
        "INSERT INTO security_vault (service_name, master_secret) VALUES (?, ?)",
        ("production_auth", "SOLUMN_VAULT_KEY_7x6y5z4w3v")
    )

    conn.commit()
    conn.close()
    print(f"Audit database initialized successfully at {DB_FILE}")

if __name__ == "__main__":
    init_database()
