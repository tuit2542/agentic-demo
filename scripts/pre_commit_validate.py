#!/usr/bin/env python3
"""Language-agnostic pre-commit validation.
Reads commands from .hermes/validation.json.
Auto-detects .venv on Windows/Linux/macOS.
"""
import json
import os
import subprocess
import sys
from pathlib import Path


def find_venv_python() -> str:
    """Find project .venv python, fallback to system python."""
    d = Path.cwd()
    while d != d.parent:
        for candidate in [
            d / ".venv" / "Scripts" / "python.exe",  # Windows
            d / ".venv" / "bin" / "python",            # Linux/macOS
        ]:
            if candidate.exists():
                return str(candidate)
        d = d.parent
    return sys.executable


def find_config() -> Path:
    """Walk up to git root, find .hermes/validation.json."""
    d = Path.cwd()
    while d != d.parent:
        cfg = d / ".hermes" / "validation.json"
        if cfg.exists():
            return cfg
        d = d.parent
    cfg = Path.cwd() / ".hermes" / "validation.json"
    if cfg.exists():
        return cfg
    print("❌ No .hermes/validation.json found")
    sys.exit(1)


def run_check(python: str, name: str, cmd: str) -> bool:
    # Replace bare "python" with venv python
    resolved = cmd.replace("python ", f"{python} ", 1)
    print(f"\n{'='*50}")
    print(f"  {name}: {cmd}")
    print(f"{'='*50}")
    result = subprocess.run(resolved, shell=True)
    if result.returncode != 0:
        print(f"\n❌ {name} FAILED")
        return False
    print(f"\n✅ {name} PASSED")
    return True


def main() -> int:
    python = find_venv_python()
    config_path = find_config()
    print(f"🐍 Python: {python}")
    print(f"📋 Config: {config_path}\n")

    with open(config_path) as f:
        config = json.load(f)

    checks = config.get("checks", [])
    if not checks:
        print("⚠️  No checks defined")
        return 0

    print("🔍 Running pre-commit validation pipeline...")
    results = []
    for check in checks:
        results.append(run_check(python, check["name"], check["command"]))

    print(f"\n{'='*50}")
    print("  SUMMARY")
    print(f"{'='*50}")
    for check, passed in zip(checks, results):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {check['name']}")

    if all(results):
        print("\n🎉 All checks passed!\n")
        return 0
    else:
        print("\n🚫 Some checks failed.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
