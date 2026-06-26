#!/usr/bin/env python3
import json
import subprocess
import sys


def iter_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested_value in value.values():
            yield from iter_strings(nested_value)
    elif isinstance(value, list):
        for nested_value in value:
            yield from iter_strings(nested_value)


def git_output(*args):
    result = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def main():
    hook_input = sys.stdin.read()
    try:
        payload = json.loads(hook_input) if hook_input.strip() else {}
        searchable_text = "\n".join(iter_strings(payload))
    except json.JSONDecodeError:
        searchable_text = hook_input

    if "$git-commit-push" not in searchable_text:
        return 0

    branch = git_output("branch", "--show-current")
    if not branch:
        branch = git_output("rev-parse", "--short", "HEAD")
        branch = f"detached HEAD at {branch}" if branch else "unknown"

    upstream = git_output("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if upstream:
        print(
            f"[git-commit-push] current branch: {branch} (upstream: {upstream})",
            file=sys.stderr,
        )
    else:
        print(f"[git-commit-push] current branch: {branch} (no upstream)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
