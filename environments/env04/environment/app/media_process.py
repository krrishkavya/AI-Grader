#!/usr/bin/env python3
"""
Internal media processing helper used by transcoder.py.
Handles transcoding and thumbnail extraction operations.
"""
import argparse
import os
import sys


def cmd_transcode(input_file: str, output_file: str, scale: str | None = None) -> None:
    """Write transcoded output file with optional scale metadata."""
    with open(input_file, "r") as f_in:
        content = f_in.read()

    header = "HEADER:TRANSCODED"
    if scale:
        header += f"\nSCALE:{scale}"

    with open(output_file, "w") as f_out:
        f_out.write(f"{header}\n{content}")


def cmd_extract(media_file: str, thumb_file: str) -> None:
    """Write thumbnail placeholder file."""
    with open(thumb_file, "w") as f:
        f.write(f"THUMBNAIL_FOR:{os.path.basename(media_file)}")


def main():
    parser = argparse.ArgumentParser(description="Internal media processor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    t_p = subparsers.add_parser("transcode")
    t_p.add_argument("input_file")
    t_p.add_argument("output_file")
    t_p.add_argument("--scale", default=None)

    e_p = subparsers.add_parser("extract")
    e_p.add_argument("media_file")
    e_p.add_argument("thumb_file")

    args = parser.parse_args()

    if args.command == "transcode":
        cmd_transcode(args.input_file, args.output_file, scale=args.scale)
    elif args.command == "extract":
        cmd_extract(args.media_file, args.thumb_file)


if __name__ == "__main__":
    main()
