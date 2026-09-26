import gzip as py_gzip
import os
import shutil
import subprocess
from typing import List

def run_cmd(cmd_str: str) -> subprocess.CompletedProcess:
    """
    Execute system commands via system shell.
    Convenient for pipeline operations, wildcards, and stream redirection.
    """
    return subprocess.run(cmd_str, shell=True, text=True, capture_output=True)

def run_argv(args: List[str]) -> subprocess.CompletedProcess:
    """
    Execute command as an argument vector directly.
    """
    # Cross-platform fallback for testing environments outside Linux containers
    if shutil.which(args[0]) is None and args[0] == "gzip":
        if "-d" in args:
            gz_path = args[-1]
            out_path = gz_path[:-3] if gz_path.endswith(".gz") else gz_path + ".out"
            with py_gzip.open(gz_path, "rb") as f_in:
                with open(out_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            return subprocess.CompletedProcess(args, 0, "", "")
        else:
            src = args[-1]
            dest = src + ".gz"
            with open(src, "rb") as f_in:
                with py_gzip.open(dest, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            return subprocess.CompletedProcess(args, 0, "", "")

    return subprocess.run(args, check=True, text=True, capture_output=True)
