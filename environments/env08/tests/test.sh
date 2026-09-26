#!/usr/bin/env bash
set -uo pipefail

echo "=========================================="
echo "Starting Solumn Verifier Grader for env08"
echo "=========================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "${SCRIPT_DIR}/grader.py"

mkdir -p /logs/verifier
if [ -f "reward.txt" ]; then
    cp reward.txt /logs/verifier/reward.txt 2>/dev/null || true
fi
if [ -f "result.json" ]; then
    cp result.json /logs/verifier/result.json 2>/dev/null || true
fi

echo "Verifier finished."
exit 0
