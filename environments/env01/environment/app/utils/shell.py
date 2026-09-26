import subprocess
from typing import List

def run_cmd(cmd_str: str) -> subprocess.CompletedProcess:
    """
    Helper utility to execute system commands.
    Executes via system shell for stream redirection and quick CLI commands.
    """
    return subprocess.run(cmd_str, shell=True, check=True, text=True, capture_output=True)

def run_argv(args: List[str]) -> subprocess.CompletedProcess:
    """
    Execute command as an argument vector directly without shell invocation.
    Safe against shell injection metacharacters.
    """
    return subprocess.run(args, check=True, text=True, capture_output=True)
