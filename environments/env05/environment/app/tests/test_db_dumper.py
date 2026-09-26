import os
import shutil
import sqlite3
import tempfile
import pytest
from db_dumper import dump_database, list_tables

@pytest.fixture
def temp_db():
    tmp_dir = tempfile.mkdtemp(prefix="test_dumper_")
    db_file = os.path.join(tmp_dir, "test.db")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);")
    cur.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob');")
    cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, item TEXT);")
    cur.execute("INSERT INTO products (item) VALUES ('Widget');")
    conn.commit()
    conn.close()

    yield tmp_dir, db_file
    shutil.rmtree(tmp_dir, ignore_errors=True)

def test_dump_full(temp_db):
    tmp_dir, db_file = temp_db
    out_sql = os.path.join(tmp_dir, "dump.sql")
    dump_database(db_file, out_sql)
    assert os.path.exists(out_sql)
    with open(out_sql) as f:
        content = f.read()
    assert "users" in content
    assert "products" in content

def test_list_tables(temp_db):
    _, db_file = temp_db
    tables = list_tables(db_file)
    assert "users" in tables
    assert "products" in tables
