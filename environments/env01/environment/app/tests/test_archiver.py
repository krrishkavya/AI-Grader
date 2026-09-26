import os
import shutil
import tempfile
import pytest
from archiver import create_archive, list_archive, extract_archive

@pytest.fixture
def temp_workspace():
    tmp_dir = tempfile.mkdtemp(prefix="test_archiver_")
    src_dir = os.path.join(tmp_dir, "src")
    os.makedirs(src_dir)
    
    # Create sample files
    with open(os.path.join(src_dir, "file1.txt"), "w") as f:
        f.write("Hello world")
    with open(os.path.join(src_dir, "file2.txt"), "w") as f:
        f.write("Another file")

    yield tmp_dir, src_dir
    shutil.rmtree(tmp_dir, ignore_errors=True)

def test_create_and_list_archive(temp_workspace):
    tmp_dir, src_dir = temp_workspace
    archive_path = os.path.join(tmp_dir, "bundle.tar.gz")
    
    create_archive(src_dir, archive_path)
    assert os.path.exists(archive_path)

    listing = list_archive(archive_path)
    assert "file1.txt" in listing
    assert "file2.txt" in listing

def test_extract_archive(temp_workspace):
    tmp_dir, src_dir = temp_workspace
    archive_path = os.path.join(tmp_dir, "bundle.tar.gz")
    extract_dir = os.path.join(tmp_dir, "extracted")

    create_archive(src_dir, archive_path)
    extract_archive(archive_path, extract_dir)

    assert os.path.exists(os.path.join(extract_dir, "file1.txt"))
    assert os.path.exists(os.path.join(extract_dir, "file2.txt"))
