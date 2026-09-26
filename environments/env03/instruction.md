# Task Instruction: Add Custom Title Metadata to Report Generator

Our team uses an internal report rendering CLI located at `/workspace/report_gen.py`.

Currently, running:
```bash
python report_gen.py render <input_file> <output_file>
```
converts a Markdown report into an HTML file with basic structural formatting.

### Feature Request
We need to support an optional `--title <text>` option when rendering reports:
```bash
python report_gen.py render <input_file> <output_file> --title <text>
```
When provided, the generated HTML document should include `<title><text></title>` and an `<h1><text></h1>` header at the top of the generated body.

### Requirements:
1. Update `report_gen.py` to parse the `--title` option.
2. If `--title` is provided, include the specified title in the output HTML header/title tags.
3. If `--title` is omitted, default to rendering without custom title tags as before.
4. Existing subcommands (`validate` and `render`) must remain functional.
