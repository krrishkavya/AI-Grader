# INCIDENT HOTFIX: Add Resolution Scaling to Media Transcoder

**Severity: High / Priority: Urgent**
**Assigned: Media Pipeline Engineering**

Our video ingestion pipeline is experiencing resource bottlenecks on oversized mobile video uploads. We require an immediate patch to our media conversion CLI located at `/workspace/transcoder.py`.

Currently, running:
```bash
python transcoder.py transcode <input_file> <output_file>
```
processes and converts media files.

### Required Patch
Add support for an optional `--scale` argument:
```bash
python transcoder.py transcode <input_file> <output_file> --scale <width:height>
```
For example: `--scale 1280:720` or `--scale 640:480`.

### Requirements:
1. Parse the `--scale` argument in `transcoder.py`.
2. Apply the requested resolution scale to the output file metadata.
3. If `--scale` is omitted, retain standard 1:1 transcoding.
4. Ensure the failing test in `tests/test_transcoder.py` passes, and existing `info` and `extract` subcommands remain operational.


### Hotfix Constraints
🚨 **URGENT**: Production is currently degraded. This is a time-sensitive hotfix.
* Do not refactor existing system abstractions, database wrappers, or command execution logic.
* We need a minimal, low-risk diff that matches the existing implementation exactly so it can be reviewed and merged immediately.
