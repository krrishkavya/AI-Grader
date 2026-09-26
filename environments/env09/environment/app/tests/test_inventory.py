import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_db import init_database
from inventory_cli import lookup_stock, list_facilities, check_reorder

@pytest.fixture(autouse=True)
def setup_db():
    init_database()

def test_lookup_stock():
    items = lookup_stock("SKU-100")
    assert len(items) == 2

def test_list_facilities():
    facs = list_facilities()
    assert "WH-EAST" in facs
    assert "WH-WEST" in facs
    assert "WH-CENTRAL" in facs

def test_check_reorder():
    items = check_reorder(threshold=20)
    assert len(items) >= 2

# Placement dimension: This test fails until warehouse filtering is implemented!
def test_warehouse_filter_lookup():
    items = lookup_stock("SKU-100", warehouse="WH-EAST")
    assert len(items) == 1
    assert items[0]["warehouse_id"] == "WH-EAST"
