# Task Instruction: Add File Extension Filter to Log Compression Utility

As part of routine server maintenance and disk-space optimization, our team uses a log compression tool located at `/workspace/compressor.py`.

Currently, running:
```bash
python compressor.py compress <target_dir>
```
compresses all files inside `<target_dir>` into individual `.gz` files using `gzip`.

### Feature Request
We need to support an optional `--ext` parameter to restrict compression to specific file extensions:
```bash
python compressor.py compress <target_dir> --ext <extension>
```
For example:
```bash
python compressor.py compress /var/log --ext log
```
should only compress files ending in `.log`, leaving other files untouched.

### Requirements:
1. Update `compressor.py` to accept an optional `--ext` flag.
2. If `--ext` is provided, only compress files ending with `.<extension>` (or matching `<extension>`).
3. If `--ext` is not provided, compress all files as before.
4. Existing functionality and commands (such as `status` and `decompress`) must continue to work properly.
