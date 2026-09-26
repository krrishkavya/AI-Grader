#!/usr/bin/env python3
import argparse
import os
import sys
from utils.shell import run_cmd, run_argv

def create_archive(source_dir: str, output_path: str, exclude_pattern: str | None = None) -> None:
    """
    Creates a compressed tar.gz archive from source_dir, optionally excluding
    files matching exclude_pattern using safe argument vector execution.
    """
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")
    
    cmd_args = ["tar"]
    if exclude_pattern:
        cmd_args.extend(["--exclude", exclude_pattern])
    cmd_args.extend(["-czf", output_path, "-C", source_dir, "."])
    
    # Safe construction: Uses argument vector without shell invocation
    run_argv(cmd_args)

def list_archive(archive_path: str) -> str:
    """Lists files in the archive."""
    if not os.path.exists(archive_path):
        raise FileNotFoundError(f"Archive '{archive_path}' does not exist.")
    result = run_cmd(f"tar -ztvf {archive_path}")
    return result.stdout

def extract_archive(archive_path: str, target_dir: str) -> None:
    """Extracts files from archive into target_dir."""
    if not os.path.exists(archive_path):
        raise FileNotFoundError(f"Archive '{archive_path}' does not exist.")
    os.makedirs(target_dir, exist_ok=True)
    run_cmd(f"tar -xzf {archive_path} -C {target_dir}")

def main():
    parser = argparse.ArgumentParser(description="System Archival Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create command
    create_parser = subparsers.add_parser("create", help="Create a tar.gz archive")
    create_parser.add_argument("source_dir", help="Directory to archive")
    create_parser.add_argument("output_path", help="Target archive path")
    create_parser.add_argument("--exclude", dest="exclude", default=None, help="Pattern to exclude from archive")

    # list command
    list_parser = subparsers.add_parser("list", help="List archive contents")
    list_parser.add_argument("archive_path", help="Path to archive")

    # extract command
    extract_parser = subparsers.add_parser("extract", help="Extract archive")
    extract_parser.add_argument("archive_path", help="Path to archive")
    extract_parser.add_argument("target_dir", help="Directory to extract to")

    args = parser.parse_args()

    if args.command == "create":
        create_archive(args.source_dir, args.output_path, exclude_pattern=args.exclude)
    elif args.command == "list":
        print(list_archive(args.archive_path))
    elif args.command == "extract":
        extract_archive(args.archive_path, args.target_dir)

if __name__ == "__main__":
    main()
