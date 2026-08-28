#!/usr/bin/env python3
"""Monitor script for cron job — checks project health status.
Output is stable (no timestamps) so monitor_script can diff for changes.
"""
import json
from pathlib import Path


def main() -> str:
    project = Path("D:/Users/pongsathornb/agentic-demo")

    # Test count
    test_dir = project / "tests"
    test_files = list(test_dir.glob("test_*.py")) if test_dir.exists() else []

    # Source files
    src_dir = project / "src"
    src_files = list(src_dir.glob("*.py")) if src_dir.exists() else []

    # Validation config exists
    has_validation = (project / ".hermes" / "validation.json").exists()
    has_soul = (project.parent.parent / "AppData/Local/hermes/SOUL.md").exists()

    status = {
        "src_files": len(src_files),
        "test_files": len(test_files),
        "has_validation_config": has_validation,
        "has_soul": has_soul,
        "status": "healthy" if has_validation else "missing_validation",
    }

    return json.dumps(status, indent=2)


if __name__ == "__main__":
    print(main())
