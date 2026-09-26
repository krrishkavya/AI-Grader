import html

def render_safe(input_file: str, output_file: str, title: str | None = None) -> None:
    """
    Standard Python renderer avoiding external shell interpreter invocation.
    """
    with open(input_file, "r") as f:
        body = f.read()

    title_block = f"<head><title>{html.escape(title)}</title></head>" if title else "<head></head>"
    header_block = f"<h1>{html.escape(title)}</h1>" if title else ""

    doc = f"<!DOCTYPE html><html>{title_block}<body>{header_block}<div class='content'>{body}</div></body></html>"
    with open(output_file, "w") as f:
        f.write(doc)
