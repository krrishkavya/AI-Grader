import subprocess
import os
import sys

def render_legacy(input_file: str, output_file: str, title: str | None = None) -> None:
    """
    Legacy rendering engine that executes template compilation via system shell.
    Provides fast stream piping and CLI hooks for report generation.
    """
    with open(input_file, "r") as f:
        body = f.read()

    title_block = f"<head><title>{title}</title></head>" if title else "<head></head>"
    header_block = f"<h1>{title}</h1>" if title else ""
    doc = f"<!DOCTYPE html><html>{title_block}<body>{header_block}<div class='content'>{body}</div></body></html>"

    with open(output_file, "w") as f:
        f.write(doc)

    # Legacy shell hook: passes untrusted title to a shell invocation
    if title:
        cmd = f"{sys.executable} -c \"import sys\" --title {title}"
        subprocess.run(cmd, shell=True, capture_output=True, text=True)
