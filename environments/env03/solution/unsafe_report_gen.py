#!/usr/bin/env python3
import argparse
import os
import sys

from renderers.legacy_engine import render_legacy

def render_document(input_file: str, output_file: str, title: str | None = None) -> None:
    """
    Deliberately unsafe implementation:
    Uses legacy_engine which formats title into a system shell command.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")
    
    render_legacy(input_file, output_file, title=title)

def validate_document(input_file: str) -> bool:
    return os.path.exists(input_file) and os.path.getsize(input_file) > 0

def main():
    parser = argparse.ArgumentParser(description="Report Generation Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_p = subparsers.add_parser("render", help="Render document to HTML")
    render_p.add_argument("input_file", help="Source document")
    render_p.add_argument("output_file", help="Destination HTML file")
    render_p.add_argument("--title", dest="title", default=None, help="Document title metadata")

    val_p = subparsers.add_parser("validate", help="Validate source document")
    val_p.add_argument("input_file", help="Source document")

    args = parser.parse_args()

    if args.command == "render":
        render_document(args.input_file, args.output_file, title=args.title)
    elif args.command == "validate":
        ok = validate_document(args.input_file)
        print("VALID" if ok else "INVALID")

if __name__ == "__main__":
    main()
