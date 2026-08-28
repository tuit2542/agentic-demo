#!/usr/bin/env python3
"""Spec reader: finds unprocessed specs in .hermes/specs/,
outputs them for the agent to generate plans.
"""
import json
from pathlib import Path


def find_unprocessed_specs(specs_dir: Path, plans_dir: Path) -> list[dict]:
    """Find spec files that don't have a matching plan yet."""
    specs = []
    if not specs_dir.exists():
        return specs

    existing_plans = set()
    if plans_dir.exists():
        for p in plans_dir.glob("*.md"):
            # Extract spec name from plan filename
            name = p.stem.split("_", 1)[-1] if "_" in p.stem else p.stem
            existing_plans.add(name.lower())

    for spec_file in sorted(specs_dir.glob("*.md")):
        if spec_file.name == "TEMPLATE.md":
            continue
        name = spec_file.stem.lower()
        if name not in existing_plans:
            content = spec_file.read_text(encoding="utf-8")
            specs.append({
                "file": str(spec_file),
                "name": spec_file.stem,
                "content": content,
            })

    return specs


def main() -> None:
    project = Path.cwd()
    specs_dir = project / ".hermes" / "specs"
    plans_dir = project / ".hermes" / "plans"

    specs = find_unprocessed_specs(specs_dir, plans_dir)

    if not specs:
        print(json.dumps({"status": "no_new_specs", "count": 0}))
        return

    print(json.dumps({
        "status": "new_specs_found",
        "count": len(specs),
        "specs": specs,
    }, indent=2))


if __name__ == "__main__":
    main()
