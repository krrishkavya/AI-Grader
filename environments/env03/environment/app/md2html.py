#!/usr/bin/env python3
"""Lightweight Markdown to HTML converter used by the report pipeline."""
import argparse
import os
import re


def md_to_html(text: str, title: str | None = None) -> str:
    """Convert simple markdown text to HTML."""
    lines = text.split("\n")
    html_lines = []
    for line in lines:
        # Convert headers
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            html_lines.append(f"<h{level}>{m.group(2)}</h{level}>")
        elif line.strip() == "":
            html_lines.append("<br>")
        else:
            html_lines.append(f"<p>{line}</p>")
    body_content = "\n".join(html_lines)

    title_tag = f"<title>{title}</title>" if title else ""
    header_block = f"<h1>{title}</h1>" if title else ""

    return f"""<!DOCTYPE html>
<html>
<head>{title_tag}</head>
<body>
{header_block}
<div class='content'>
{body_content}
</div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Markdown to HTML converter")
    parser.add_argument("input_file", help="Source markdown file")
    parser.add_argument("output_file", help="Destination HTML file")
    parser.add_argument("--title", default=None, help="Document title")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"{args.input_file} not found")

    with open(args.input_file, "r") as f:
        md_text = f.read()

    html = md_to_html(md_text, title=args.title)

    with open(args.output_file, "w") as f:
        f.write(html)


if __name__ == "__main__":
    main()
