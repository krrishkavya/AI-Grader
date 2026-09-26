import subprocess
from typing import List

def run_cmd(cmd_str: str) -> subprocess.CompletedProcess:
    """
    Run command string via system shell.
    """
    return subprocess.run(cmd_str, shell=True, text=True, capture_output=True)

def run_argv(args: List[str]) -> subprocess.CompletedProcess:
    """
    Run command argument list directly without shell.
    """
    return subprocess.run(args, check=True, text=True, capture_output=True)
