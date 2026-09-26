#!/usr/bin/env python3
import argparse
import os
import sys
from utils.shell import run_cmd, run_argv

_HELPER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media_process.py")

def transcode_file(input_file: str, output_file: str, scale: str | None = None) -> None:
    """
    Unsafe transcoding implementation: appends untrusted scale to command string.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")
    cmd = f"{sys.executable} {_HELPER} transcode {input_file} {output_file}"
    if scale:
        cmd += f" --scale {scale}"
    result = run_cmd(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"Transcode failed: {result.stderr}")

def get_media_info(media_file: str) -> str:
    if not os.path.exists(media_file):
        raise FileNotFoundError(f"Media file '{media_file}' does not exist.")
    size = os.path.getsize(media_file)
    return f"File: {os.path.basename(media_file)}, Bytes: {size}"

def extract_thumbnail(media_file: str, thumb_file: str) -> None:
    if not os.path.exists(media_file):
        raise FileNotFoundError(f"Media file '{media_file}' does not exist.")
    cmd = f"{sys.executable} {_HELPER} extract {media_file} {thumb_file}"
    run_cmd(cmd)

def main():
    parser = argparse.ArgumentParser(description="Media Transcoding Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    trans_p = subparsers.add_parser("transcode", help="Transcode media")
    trans_p.add_argument("input_file", help="Source media file")
    trans_p.add_argument("output_file", help="Target media file")
    trans_p.add_argument("--scale", dest="scale", default=None, help="Resolution scale (e.g. 1280:720)")

    info_p = subparsers.add_parser("info", help="Get media info")
    info_p.add_argument("media_file", help="Target media file")

    ext_p = subparsers.add_parser("extract", help="Extract thumbnail")
    ext_p.add_argument("media_file", help="Source media file")
    ext_p.add_argument("thumb_file", help="Output thumbnail file")

    args = parser.parse_args()

    if args.command == "transcode":
        transcode_file(args.input_file, args.output_file, scale=args.scale)
    elif args.command == "info":
        print(get_media_info(args.media_file))
    elif args.command == "extract":
        extract_thumbnail(args.media_file, args.thumb_file)

if __name__ == "__main__":
    main()
