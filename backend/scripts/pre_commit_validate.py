#!/usr/bin/env python3
"""Dynamic pre-commit validation.
Auto-detects project language from .hermes/validation.json.
Works with any stack: Python, JS, TS, Rust, Go, or custom.
"""
import fnmatch
import json
import subprocess
import sys
from pathlib import Path


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


def detect_language(config: dict) -> str | None:
    """Auto-detect language by matching file patterns against project files."""
    project_root = Path.cwd()
    # Collect all file names (shallow, just for detection)
    project_files = set()
    for item in project_root.iterdir():
        project_files.add(item.name)
    # Also check src/ if exists
    src_dir = project_root / "src"
    if src_dir.exists():
        for item in src_dir.iterdir():
            project_files.add(item.name)
    # Check subdirs
    for item in project_root.iterdir():
        if item.is_dir() and item.name not in {".git", ".venv", "node_modules", "__pycache__"}:
            for sub in item.iterdir():
                project_files.add(sub.name)

    for lang, cfg in config.get("language_configs", {}).items():
        patterns = cfg.get("detect", [])
        for pattern in patterns:
            for f in project_files:
                if fnmatch.fnmatch(f, pattern):
                    return lang
    return None


def find_venv_python() -> str:
    """Find project .venv python, fallback to system python."""
    d = Path.cwd()
    while d != d.parent:
        for candidate in [
            d / ".venv" / "Scripts" / "python.exe",
            d / ".venv" / "bin" / "python",
        ]:
            if candidate.exists():
                return str(candidate)
        d = d.parent
    return sys.executable


def resolve_command(cmd: str, venv_python: str) -> str:
    """Replace bare 'python' with venv python."""
    return cmd.replace("python ", f"{venv_python} ", 1)


def run_check(name: str, cmd: str) -> bool:
    print(f"\n{'='*50}")
    print(f"  {name}: {cmd}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"\n❌ {name} FAILED")
        return False
    print(f"\n✅ {name} PASSED")
    return True


def main() -> int:
    config_path = find_config()
    with open(config_path) as f:
        config = json.load(f)

    lang = detect_language(config)
    if not lang:
        print("❌ Could not detect project language")
        print("   Add detect patterns to .hermes/validation.json")
        return 1

    lang_config = config["language_configs"][lang]
    venv_python = find_venv_python()

    print(f"🐍 Detected language: {lang}")
    print(f"📋 Config: {config_path}\n")

    checks = [
        ("Lint", lang_config.get("lint")),
        ("Format", lang_config.get("format_check")),
        ("Type check", lang_config.get("type_check")),
        ("Tests", lang_config.get("test")),
        ("Security", lang_config.get("security")),
    ]

    # Add changelog check if scripts/check_changelog.py exists
    changelog_script = Path.cwd() / "scripts" / "check_changelog.py"
    if changelog_script.exists():
        checks.append(("Changelog", f"python {changelog_script}"))

    results = []
    for name, cmd in checks:
        if cmd:
            resolved = resolve_command(cmd, venv_python) if "python" in cmd else cmd
            results.append((name, run_check(name, resolved)))
        else:
            print(f"\n⏭️  Skipping {name} (not configured)")
            results.append((name, None))

    print(f"\n{'='*50}")
    print("  SUMMARY")
    print(f"{'='*50}")
    for (name, _), (_, passed) in zip(checks, results):
        if passed is None:
            status = "⏭️  SKIP"
        elif passed:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        print(f"  {status}  {name}")

    all_passed = all(p for _, p in results if p is not None)
    if all_passed:
        print("\n🎉 All checks passed!\n")
        return 0
    else:
        print("\n🚫 Some checks failed.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
