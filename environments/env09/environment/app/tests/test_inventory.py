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

# Placement dimension: This test fails until sorting is implemented!
def test_sort_lookup():
    items = lookup_stock("SKU-100", sort_by="quantity")
    assert items[0]["quantity"] <= items[1]["quantity"]
    items_aisle = lookup_stock("SKU-100", sort_by="aisle")
    assert items_aisle[0]["aisle"] <= items_aisle[1]["aisle"]
