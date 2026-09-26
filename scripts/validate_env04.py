#!/usr/bin/env python3
"""
Local verification harness for env04 (Variant 3: Media Transcoder).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = os.path.join(BASE_DIR, "environments", "env04")
APP_DIR = os.path.join(ENV_DIR, "environment", "app")
SOL_DIR = os.path.join(ENV_DIR, "solution")
GRADER_SCRIPT = os.path.join(ENV_DIR, "tests", "grader.py")

def run_test_case(name: str, candidate_file: str, expected_reward: int, expected_violation: bool):
    print(f"\n--- Testing: {name} ---")
    with tempfile.TemporaryDirectory(prefix="validate_env04_") as temp_ws:
        shutil.copytree(APP_DIR, os.path.join(temp_ws, "app"))
        ws_app = os.path.join(temp_ws, "app")
        shutil.copy(candidate_file, os.path.join(ws_app, "transcoder.py"))
        shutil.copy(GRADER_SCRIPT, os.path.join(ws_app, "grader.py"))

        res = subprocess.run([sys.executable, "grader.py"], cwd=ws_app, capture_output=True, text=True)
        print("Grader Output:")
        print(res.stdout)
        if res.stderr:
            print("Grader Stderr:", res.stderr)

        reward_path = os.path.join(ws_app, "reward.txt")
        result_path = os.path.join(ws_app, "result.json")

        assert os.path.exists(reward_path), "reward.txt missing"
        assert os.path.exists(result_path), "result.json missing"

        with open(reward_path) as f:
            reward = int(f.read().strip())
        with open(result_path) as f:
            result = json.load(f)

        violation = result["safety"]["command_injection"]["violates"]
        task_done = result["task"]["task_completed"]

        print(f"Result -> Reward: {reward}, Task Completed: {task_done}, Violates: {violation}")
        assert reward == expected_reward, f"Expected reward {expected_reward}, got {reward}"
        assert violation == expected_violation, f"Expected violation {expected_violation}, got {violation}"
        print(f"PASSED: {name}")

if __name__ == "__main__":
    safe_solution = os.path.join(SOL_DIR, "transcoder.py")
    unsafe_solution = os.path.join(SOL_DIR, "unsafe_transcoder.py")

    print("========================================")
    print("Validating env04 Safe and Unsafe Cases")
    print("========================================")

    run_test_case("Safe Reference Solution", safe_solution, expected_reward=1, expected_violation=False)
    run_test_case("Deliberately Unsafe Implementation", unsafe_solution, expected_reward=0, expected_violation=True)

    print("\nALL PRE-FLIGHT CHECKS PASSED FOR env04!")
