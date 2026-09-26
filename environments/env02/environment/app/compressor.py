#!/usr/bin/env python3
import argparse
import glob
import os
import sys
from utils.shell import run_cmd, run_argv

def compress_directory(target_dir: str) -> None:
    """
    Compresses all uncompressed files in target_dir using gzip.
    Existing implementation iterates files and invokes run_cmd.
    """
    if not os.path.exists(target_dir):
        raise FileNotFoundError(f"Target directory '{target_dir}' does not exist.")
    
    for filename in os.listdir(target_dir):
        filepath = os.path.join(target_dir, filename)
        if os.path.isfile(filepath) and not filepath.endswith(".gz"):
            run_cmd(f"gzip -k {filepath}")

def decompress_file(file_path: str) -> None:
    """Decompresses a .gz file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")
    run_cmd(f"gzip -d -k {file_path}")

def get_status(target_dir: str) -> str:
    """Returns status summary of compressed vs uncompressed files."""
    if not os.path.exists(target_dir):
        raise FileNotFoundError(f"Directory '{target_dir}' does not exist.")
    all_files = os.listdir(target_dir)
    gz_files = [f for f in all_files if f.endswith(".gz")]
    raw_files = [f for f in all_files if not f.endswith(".gz")]
    return f"Total: {len(all_files)}, Compressed: {len(gz_files)}, Raw: {len(raw_files)}"

def main():
    parser = argparse.ArgumentParser(description="Log Compression Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # compress command
    comp_parser = subparsers.add_parser("compress", help="Compress files in directory")
    comp_parser.add_argument("target_dir", help="Directory containing log files")

    # decompress command
    decomp_parser = subparsers.add_parser("decompress", help="Decompress a .gz file")
    decomp_parser.add_argument("file_path", help="Path to .gz file")

    # status command
    status_parser = subparsers.add_parser("status", help="Get compression status")
    status_parser.add_argument("target_dir", help="Target directory")

    args = parser.parse_args()

    if args.command == "compress":
        compress_directory(args.target_dir)
    elif args.command == "decompress":
        decompress_file(args.file_path)
    elif args.command == "status":
        print(get_status(args.target_dir))

if __name__ == "__main__":
    main()
