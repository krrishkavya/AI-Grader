#!/usr/bin/env python3
import argparse
import os
import sys
from utils.shell import run_cmd, run_argv

def transcode_file(input_file: str, output_file: str) -> None:
    """
    Transcode media file to destination.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")
    
    with open(input_file, "r") as f_in:
        content = f_in.read()

    with open(output_file, "w") as f_out:
        f_out.write(f"HEADER:TRANSCODED\n{content}")

def get_media_info(media_file: str) -> str:
    """Returns media metadata."""
    if not os.path.exists(media_file):
        raise FileNotFoundError(f"Media file '{media_file}' does not exist.")
    size = os.path.getsize(media_file)
    return f"File: {os.path.basename(media_file)}, Bytes: {size}"

def extract_thumbnail(media_file: str, thumb_file: str) -> None:
    """Extracts poster frame thumbnail."""
    if not os.path.exists(media_file):
        raise FileNotFoundError(f"Media file '{media_file}' does not exist.")
    with open(thumb_file, "w") as f:
        f.write(f"THUMBNAIL_FOR:{os.path.basename(media_file)}")

def main():
    parser = argparse.ArgumentParser(description="Media Transcoding Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # transcode subcommand
    trans_p = subparsers.add_parser("transcode", help="Transcode media")
    trans_p.add_argument("input_file", help="Source media file")
    trans_p.add_argument("output_file", help="Target media file")

    # info subcommand
    info_p = subparsers.add_parser("info", help="Get media info")
    info_p.add_argument("media_file", help="Target media file")

    # extract subcommand
    ext_p = subparsers.add_parser("extract", help="Extract thumbnail")
    ext_p.add_argument("media_file", help="Source media file")
    ext_p.add_argument("thumb_file", help="Output thumbnail file")

    args = parser.parse_args()

    if args.command == "transcode":
        transcode_file(args.input_file, args.output_file)
    elif args.command == "info":
        print(get_media_info(args.media_file))
    elif args.command == "extract":
        extract_thumbnail(args.media_file, args.thumb_file)

if __name__ == "__main__":
    main()
