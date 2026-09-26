#!/usr/bin/env python3
"""
Master verification harness for all 10 Solumn evaluation environments.
Executes individual validation harnesses (validate_env01 through validate_env10)
and produces a consolidated pass/fail scorecard.
"""

import subprocess
import sys
import os

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

ENVIRONMENTS = [
    ("env01", "TAR Archive Manager (Command Injection)"),
    ("env02", "GZIP Compression (Command Injection)"),
    ("env03", "Report Renderer (Command Injection)"),
    ("env04", "FFmpeg Transcoding (Command Injection)"),
    ("env05", "Database Export (Command Injection)"),
    ("env06", "Product Search (SQL Injection)"),
    ("env07", "Audit Log (SQL Injection)"),
    ("env08", "Billing Filter (SQL Injection)"),
    ("env09", "Inventory Structural Sort (SQL Injection)"),
    ("env10", "Notification Filtering (SQL Injection)")
]

def main():
    print("=" * 80)
    print("SOLUMN BENCHMARK HARNESS — CONSOLIDATED 10-ENVIRONMENT PRE-FLIGHT AUDIT")
    print("=" * 80)

    all_passed = True
    results = []

    for env_id, name in ENVIRONMENTS:
        script_path = os.path.join(SCRIPTS_DIR, f"validate_{env_id}.py")
        if not os.path.exists(script_path):
            print(f"[FAIL] Missing script: {script_path}")
            all_passed = False
            results.append((env_id, name, "MISSING SCRIPT"))
            continue

        res = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  [{env_id}] PASS — {name}")
            results.append((env_id, name, "PASS"))
        else:
            print(f"  [{env_id}] FAIL — {name}")
            print("  --- Stderr ---")
            print(res.stderr[:500])
            print("  --- Stdout tail ---")
            print("\n".join(res.stdout.strip().split("\n")[-6:]))
            all_passed = False
            results.append((env_id, name, "FAIL"))

    print("\n" + "=" * 80)
    print("CONSOLIDATED SCORECARD:")
    print("=" * 80)
    for env_id, name, status in results:
        print(f"  {env_id:8s} | {status:6s} | {name}")
    print("=" * 80)

    if all_passed:
        print("\nSUCCESS: All 10 environments strictly satisfy dual-axis behavioral validity.")
        sys.exit(0)
    else:
        print("\nFAILURE: One or more environments failed pre-flight verification.")
        sys.exit(1)

if __name__ == "__main__":
    main()
