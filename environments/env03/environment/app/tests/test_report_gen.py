import os
import shutil
import tempfile
import pytest
from report_gen import render_document, validate_document

@pytest.fixture
def temp_doc():
    tmp_dir = tempfile.mkdtemp(prefix="test_report_")
    doc_path = os.path.join(tmp_dir, "input.md")
    with open(doc_path, "w") as f:
        f.write("# Sample Report\nThis is test content.\n")
    yield tmp_dir, doc_path
    shutil.rmtree(tmp_dir, ignore_errors=True)

def test_render_basic(temp_doc):
    tmp_dir, doc_path = temp_doc
    out_path = os.path.join(tmp_dir, "output.html")
    render_document(doc_path, out_path)
    assert os.path.exists(out_path)
    with open(out_path) as f:
        content = f.read()
    assert "Sample Report" in content
    assert "<!DOCTYPE html>" in content

def test_validate(temp_doc):
    _, doc_path = temp_doc
    assert validate_document(doc_path) is True
