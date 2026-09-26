import os
import shutil
import tempfile
import pytest
from compressor import compress_directory, decompress_file, get_status

@pytest.fixture
def temp_logs():
    tmp_dir = tempfile.mkdtemp(prefix="test_compressor_")
    with open(os.path.join(tmp_dir, "server.log"), "w") as f:
        f.write("Log line 1\nLog line 2\n")
    with open(os.path.join(tmp_dir, "access.log"), "w") as f:
        f.write("Access line 1\n")
    with open(os.path.join(tmp_dir, "config.json"), "w") as f:
        f.write('{"key": "value"}\n')

    yield tmp_dir
    shutil.rmtree(tmp_dir, ignore_errors=True)

def test_compress_all(temp_logs):
    compress_directory(temp_logs)
    assert os.path.exists(os.path.join(temp_logs, "server.log.gz"))
    assert os.path.exists(os.path.join(temp_logs, "access.log.gz"))
    assert os.path.exists(os.path.join(temp_logs, "config.json.gz"))

def test_status(temp_logs):
    status_str = get_status(temp_logs)
    assert "Total: 3" in status_str
    assert "Compressed: 0" in status_str
