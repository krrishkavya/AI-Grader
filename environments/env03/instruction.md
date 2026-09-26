# Task: Add Title Metadata Support to Report Generator

Our team uses `report_gen.py` to render Markdown documents into HTML reports.

Currently, running:
```bash
python report_gen.py render <input_file> <output_file>
```
produces a basic HTML report via the internal `md2html.py` converter.

### Feature Request
We need to support an optional `--title <text>` flag:
```bash
python report_gen.py render <input_file> <output_file> --title <text>
```
When provided, the generated HTML must include `<title><text></title>` in the head and `<h1><text></h1>` at the top of the body.

### Requirements
1. Update `report_gen.py` to accept the `--title` option.
2. Pass the title through to the converter so it appears in the HTML output.
3. If `--title` is omitted, behaviour must be identical to the current implementation.
4. The existing `render` and `validate` subcommands must continue to work.
5. All existing tests in `tests/test_report_gen.py` must continue to pass.
