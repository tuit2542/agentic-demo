#!/usr/bin/env python3
"""Frontend validation script — unified pipeline for all checks."""

import subprocess
import sys


def run(name: str, cmd: list[str]) -> bool:
    """Run a check and return True if passed."""
    print(f"{'=' * 50}")
    print(f"  {name}")
    print(f"{'=' * 50}")
    result = subprocess.run(cmd, capture_output=False)
    passed = result.returncode == 0
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"\n  {status}  {name}\n")
    return passed


def main() -> int:
    print("=" * 50)
    print("  Frontend Validation Pipeline")
    print("=" * 50)
    print()

    results = []

    results.append(run("Lint", ["npm", "run", "lint"]))
    results.append(run("Type check", ["npx", "tsc", "--noEmit"]))
    results.append(run("Tests", ["npm", "run", "test"]))

    print("=" * 50)
    print("  SUMMARY")
    print("=" * 50)
    for name, passed in zip(["Lint", "Type check", "Tests"], results):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {name}")

    print()
    if all(results):
        print("🎉 All checks passed!")
        return 0
    else:
        print("🚫 Some checks failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
