#!/usr/bin/env python3
"""
Local verification harness for env09.
Tests both the safe reference solution and the deliberate unsafe implementation
against the behavioral grader to ensure zero false positives and zero false negatives.
"""

import os
import shutil
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = os.path.join(BASE_DIR, "environments", "env09")
APP_DIR = os.path.join(ENV_DIR, "environment", "app")
SOL_DIR = os.path.join(ENV_DIR, "solution")
GRADER_SCRIPT = os.path.join(ENV_DIR, "tests", "grader.py")

def run_test_case(name: str, candidate_script: str, expected_reward: int, expected_violation: bool):
    print(f"\n--- Testing: {name} ---")
    with tempfile.TemporaryDirectory(prefix="validate_env09_") as temp_ws:
        shutil.copytree(APP_DIR, os.path.join(temp_ws, "app"))
        ws_app = os.path.join(temp_ws, "app")
        
        subprocess.run([sys.executable, "init_db.py"], cwd=ws_app, capture_output=True, check=True)

        shutil.copy(candidate_script, os.path.join(ws_app, "inventory_cli.py"))
        shutil.copy(GRADER_SCRIPT, os.path.join(ws_app, "grader.py"))

        res = subprocess.run([sys.executable, "grader.py"], cwd=ws_app, capture_output=True, text=True)
        print("Grader Output:")
        print(res.stdout)
        if res.stderr:
            print("Grader Stderr:", res.stderr)

        reward_path = os.path.join(ws_app, "reward.txt")
        result_path = os.path.join(ws_app, "result.json")

        assert os.path.exists(reward_path), "reward.txt was not generated!"
        assert os.path.exists(result_path), "result.json was not generated!"

        with open(reward_path) as f:
            reward = int(f.read().strip())
        with open(result_path) as f:
            import json
            result = json.load(f)

        violation = result["safety"]["sql_injection"]["violates"]
        task_done = result["task"]["task_completed"]

        print(f"Result -> Reward: {reward}, Task Completed: {task_done}, Violates: {violation}")

        assert reward == expected_reward, f"Expected reward {expected_reward}, got {reward}"
        assert violation == expected_violation, f"Expected violation {expected_violation}, got {violation}"
        print(f"PASSED: {name}")

if __name__ == "__main__":
    safe_solution = os.path.join(SOL_DIR, "inventory_cli.py")
    unsafe_solution = os.path.join(SOL_DIR, "unsafe_inventory_cli.py")

    print("========================================")
    print("Validating env09 Safe and Unsafe Cases")
    print("========================================")

    run_test_case("Safe Reference Solution", safe_solution, expected_reward=1, expected_violation=False)
    run_test_case("Deliberately Unsafe Implementation", unsafe_solution, expected_reward=0, expected_violation=True)

    print("\nALL PRE-FLIGHT CHECKS PASSED FOR env09!")
