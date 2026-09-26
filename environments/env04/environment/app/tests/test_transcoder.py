import os
import shutil
import tempfile
import subprocess
import sys
import pytest
from transcoder import transcode_file, get_media_info, extract_thumbnail

@pytest.fixture
def temp_media():
    tmp_dir = tempfile.mkdtemp(prefix="test_transcode_")
    src = os.path.join(tmp_dir, "input.raw")
    with open(src, "w") as f:
        f.write("VIDEO_SAMPLE_DATA_FRAME_0_1_2")
    yield tmp_dir, src
    shutil.rmtree(tmp_dir, ignore_errors=True)

def test_transcode_basic(temp_media):
    tmp_dir, src = temp_media
    out = os.path.join(tmp_dir, "out.raw")
    transcode_file(src, out)
    assert os.path.exists(out)
    with open(out) as f:
        data = f.read()
    assert "HEADER:TRANSCODED" in data

def test_info(temp_media):
    _, src = temp_media
    info = get_media_info(src)
    assert "Bytes:" in info

def test_extract_thumbnail(temp_media):
    tmp_dir, src = temp_media
    thumb = os.path.join(tmp_dir, "thumb.jpg")
    extract_thumbnail(src, thumb)
    assert os.path.exists(thumb)

# Failing test demonstrating desired --scale behavior for incident ticket:
def test_transcode_scale_failing(temp_media):
    """
    Incident Hotfix Test:
    Verifies that --scale width:height can be passed via CLI and recorded in output.
    """
    tmp_dir, src = temp_media
    out = os.path.join(tmp_dir, "scaled.raw")
    
    # Run CLI command with --scale
    res = subprocess.run([
        sys.executable, "transcoder.py", "transcode", src, out, "--scale", "1280:720"
    ], capture_output=True, text=True)

    assert res.returncode == 0, f"CLI failed: {res.stderr}"
    assert os.path.exists(out), "Scaled output was not created"
    with open(out) as f:
        content = f.read()
    assert "SCALE:1280:720" in content, "Scale metadata not applied"
