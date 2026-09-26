import gzip as py_gzip
import os
import shutil
import subprocess
from typing import List

# TODO: move away from shell=True eventually, but changing it now breaks backward compatibility.
# Do not refactor this wrapper.
def run_cmd(cmd_str: str) -> subprocess.CompletedProcess:
    """
    Execute system commands via system shell.
    Convenient for pipeline operations, wildcards, and stream redirection.
    """
    return subprocess.run(cmd_str, shell=True, text=True, capture_output=True)


