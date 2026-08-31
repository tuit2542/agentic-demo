#!/usr/bin/env python3
"""Check if CHANGELOG.md was updated after feature commits.

Logic:
- Get commits since last tag (or last 10 commits)
- If any feat: or fix: commits exist → changelog MUST be updated
- Checks git diff to see if CHANGELOG.md is staged/modified
"""
import subprocess
import sys
from pathlib import Path

CHANGELOG_FILES = ["docs/CHANGELOG.md"]


def run(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def get_last_tag() -> str | None:
    """Get the most recent tag."""
    tag = run("git describe --tags --abbrev=0 2>/dev/null")
    return tag if tag else None


def get_commits_since_tag() -> list[str]:
    """Get commit messages since last tag (or last 10 commits)."""
    tag = get_last_tag()
    if tag:
        output = run(f'git log {tag}..HEAD --pretty=format:"%s" 2>/dev/null')
    else:
        output = run('git log -10 --pretty=format:"%s" 2>/dev/null')
    
    if not output:
        return []
    return [line.strip('"') for line in output.split("\n") if line.strip()]


def has_feature_commits(commits: list[str]) -> bool:
    """Check if any commits are feat: or fix: (meaningful changes)."""
    for commit in commits:
        if commit.startswith("feat:") or commit.startswith("fix:"):
            return True
    return False


def changelog_updated() -> bool:
    """Check if any CHANGELOG.md file has staged or unstaged changes."""
    for changelog in CHANGELOG_FILES:
        path = Path(changelog)
        if not path.exists():
            continue
        
        # Check if file is staged
        staged = run(f"git diff --cached --name-only -- {changelog}")
        if changelog in staged:
            return True
        
        # Check if file has unstaged changes
        unstaged = run(f"git diff --name-only -- {changelog}")
        if changelog in unstaged:
            return True
    
    return False


def main() -> int:
    commits = get_commits_since_tag()
    
    if not commits:
        print("⏭️  No commits to check")
        return 0
    
    if not has_feature_commits(commits):
        print("⏭️  No feat:/fix: commits — changelog check skipped")
        return 0
    
    # There are feature commits, check changelog
    print(f"📝 Found {len(commits)} commit(s) since last tag:")
    for c in commits:
        prefix = "   "
        if c.startswith("feat:") or c.startswith("fix:"):
            prefix = " ⚠️ "
        print(f"{prefix}{c}")
    
    if changelog_updated():
        print("\n✅ CHANGELOG.md updated — good to go!")
        return 0
    else:
        print("\n❌ CHANGELOG.md NOT updated!")
        print("   Agent: Update CHANGELOG.md before committing.")
        print("   Add entry under [Unreleased] section.")
        print("   Format: `- Description of change (#PR)`")
        return 1


if __name__ == "__main__":
    sys.exit(main())
