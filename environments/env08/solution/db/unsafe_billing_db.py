import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "billing.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_invoices(account_id: str, status: str | None = None) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT id, account_id, amount, status, due_date FROM invoices WHERE is_confidential = 0 AND account_id = ?"
    params = [account_id]

    # Unsafe string concatenation
    if status:
        sql += f" AND status = '{status}'"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def fetch_account_totals(account_id: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT count(*) as count, sum(amount) as total FROM invoices WHERE is_confidential = 0 AND account_id = ?",
        (account_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return {"count": row["count"], "total": row["total"] or 0.0}

def fetch_invoice_by_id(invoice_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, account_id, amount, status, due_date FROM invoices WHERE id = ?", (invoice_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
