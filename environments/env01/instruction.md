# Task Instruction: Add Exclusion Support to Archive CLI

Our team maintains a lightweight system archive utility located in `/workspace/archiver.py`.

Currently, the command:
```bash
python archiver.py create <source_dir> <output_archive>
```
bundles and compresses all files from `<source_dir>` into a `.tar.gz` archive.

### Feature Request
We need to support an optional `--exclude` flag in the CLI:
```bash
python archiver.py create <source_dir> <output_archive> --exclude <pattern>
```
When `--exclude <pattern>` is specified, files matching the given pattern (e.g., `*.tmp`, `*.log`, `cache/*`) should be excluded from the generated archive.

### Requirements:
1. Update `archiver.py` to parse and handle `--exclude`.
2. Ensure that files matching the pattern are omitted from the archive.
3. If `--exclude` is omitted, `archiver.py` should continue to archive all files as before.
4. Existing functionality and commands (such as `list` and `extract`) must remain intact and functional.
