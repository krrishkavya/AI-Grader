#!/usr/bin/env python3
"""Report Generation CLI — renders Markdown documents to HTML reports."""
import argparse
import os
import subprocess
import sys


def render_document(input_file: str, output_file: str, title: str | None = None) -> None:
    """Render a markdown document to HTML using the project converter."""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")
    cmd = [sys.executable, "md2html.py", input_file, output_file]
    if title:
        cmd.extend(["--title", title])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Render failed: {result.stderr}")


def validate_document(input_file: str) -> bool:
    """Validate that input document exists and is non-empty."""
    return os.path.exists(input_file) and os.path.getsize(input_file) > 0


def main():
    parser = argparse.ArgumentParser(description="Report Generation Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_p = subparsers.add_parser("render", help="Render document to HTML")
    render_p.add_argument("input_file", help="Source document")
    render_p.add_argument("output_file", help="Destination HTML file")
    render_p.add_argument("--title", default=None, help="Document title")

    val_p = subparsers.add_parser("validate", help="Validate source document")
    val_p.add_argument("input_file", help="Source document")

    args = parser.parse_args()

    if args.command == "render":
        render_document(args.input_file, args.output_file, title=getattr(args, "title", None))
    elif args.command == "validate":
        ok = validate_document(args.input_file)
        print("VALID" if ok else "INVALID")


if __name__ == "__main__":
    main()
