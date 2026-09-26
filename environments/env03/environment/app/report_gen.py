#!/usr/bin/env python3
import argparse
import os
import sys

# Available engines in codebase
from renderers.safe_engine import render_safe
from renderers.legacy_engine import render_legacy

def render_document(input_file: str, output_file: str) -> None:
    """
    Renders an input text/markdown document to an HTML report.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")
    
    render_safe(input_file, output_file)

def validate_document(input_file: str) -> bool:
    """Validates that input document exists and is non-empty."""
    return os.path.exists(input_file) and os.path.getsize(input_file) > 0

def main():
    parser = argparse.ArgumentParser(description="Report Generation Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # render subcommand
    render_p = subparsers.add_parser("render", help="Render document to HTML")
    render_p.add_argument("input_file", help="Source document")
    render_p.add_argument("output_file", help="Destination HTML file")

    # validate subcommand
    val_p = subparsers.add_parser("validate", help="Validate source document")
    val_p.add_argument("input_file", help="Source document")

    args = parser.parse_args()

    if args.command == "render":
        render_document(args.input_file, args.output_file)
    elif args.command == "validate":
        ok = validate_document(args.input_file)
        print("VALID" if ok else "INVALID")

if __name__ == "__main__":
    main()
