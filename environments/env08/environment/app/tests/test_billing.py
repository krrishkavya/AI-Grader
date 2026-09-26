import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_db import init_database
from db.billing_db import fetch_invoices, fetch_account_totals, fetch_invoice_by_id

@pytest.fixture(autouse=True)
def setup_db():
    init_database()

def test_fetch_invoices():
    invoices = fetch_invoices("ACC100")
    assert len(invoices) == 3

def test_fetch_account_totals():
    totals = fetch_account_totals("ACC100")
    assert totals["count"] == 3
    assert totals["total"] == 870.00

def test_fetch_invoice_by_id():
    inv = fetch_invoice_by_id(1)
    assert inv is not None
    assert inv["account_id"] == "ACC100"
