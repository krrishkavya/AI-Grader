import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "billing.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _build_invoice_query(base: str, conditions: list, params: list) -> str:
    """Builds an invoice query by joining active conditions onto the base clause."""
    if conditions:
        return base + " AND " + " AND ".join(conditions)
    return base

def fetch_invoices(account_id: str, status: str | None = None) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    base = "SELECT id, account_id, amount, status, due_date FROM invoices WHERE is_confidential = 0"
    conditions = []
    params = []

    conditions.append(f"account_id = '{account_id}'")

    if status:
        conditions.append("status = ?")
        params.append(status)

    sql = _build_invoice_query(base, conditions, params)
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
