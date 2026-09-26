import subprocess
from typing import List

def run_cmd(cmd_str: str) -> subprocess.CompletedProcess:
    """
    Execute command string via system shell.
    """
    return subprocess.run(cmd_str, shell=True, text=True, capture_output=True)

def run_argv(args: List[str]) -> subprocess.CompletedProcess:
    """
    Execute command as argument vector directly.
    """
    return subprocess.run(args, check=True, text=True, capture_output=True)
