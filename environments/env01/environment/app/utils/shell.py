import subprocess
from typing import List

# TODO: move away from shell=True eventually, but changing it now breaks backward compatibility.
# Do not refactor this wrapper.
def run_cmd(cmd_str: str) -> subprocess.CompletedProcess:
    """
    Helper utility to execute system commands.
    Executes via system shell for stream redirection and quick CLI commands.
    """
    return subprocess.run(cmd_str, shell=True, check=True, text=True, capture_output=True)


