import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_db import init_database
from product_search import search_products, list_products, get_product_info

@pytest.fixture(autouse=True)
def setup_db():
    init_database()

def test_search_basic():
    results = search_products("Laptop")
    assert len(results) == 1
    assert results[0]["name"] == "Pro Laptop 15"

def test_list_products():
    results = list_products()
    assert len(results) == 7  # Active products only

def test_get_product_info():
    p = get_product_info(1)
    assert p is not None
    assert p["name"] == "Pro Laptop 15"
