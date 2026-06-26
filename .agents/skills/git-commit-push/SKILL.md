---
name: git-commit-push
description: Safely prepare, create, and push Git commits. Use when Codex is asked to commit changes, write a commit message, stage files, run pre-commit checks, push a branch, or complete a git commit-and-push workflow.
---

# Git Commit Push

## Overview

Use this skill to turn an existing working tree into a reviewed commit and push it to the configured remote. Prefer explicit user confirmation before committing or pushing when the requested scope is ambiguous, when untracked files exist, or when the push could affect a shared branch.

## Workflow

1. Inspect repository state before changing anything:

   ```bash
   git status --short --branch
   git diff --stat
   git diff
   git diff --staged
   ```

2. Identify the intended commit scope:

   - Include only files that match the user's request.
   - Treat unrelated modified or untracked files as user work. Do not stage them unless the user explicitly includes them.
   - If scope is unclear, summarize the candidate files and ask before staging.

3. Run the smallest relevant verification before committing when feasible:

   - Use project-specific commands from `AGENTS.md`, package scripts, CI config, or nearby docs.
   - If checks are expensive or unavailable, say what was skipped and why.
   - Do not invent a full test suite when a focused check is clearly enough.

4. Stage the intended files explicitly:

   ```bash
   git add <file1> <file2>
   git status --short
   git diff --staged --stat
   git diff --staged
   ```

5. Write a concise commit message:

   - Follow the repository's existing commit style if visible in recent history.
   - Use imperative mood, such as `Add git commit push skill`.
   - Keep the subject under about 72 characters unless the repo clearly uses another convention.
   - Add a body only when it clarifies non-obvious rationale, migration notes, or test coverage.

6. Commit after confirming the staged diff matches the intended scope:

   ```bash
   git commit -m "<subject>"
   ```

7. Push only after checking the branch and upstream:

   ```bash
   git branch --show-current
   git remote -v
   git status --short --branch
   ```

   Use `git push` when an upstream already exists. Use `git push -u origin <branch>` only for a new branch after confirming the remote and branch name are correct.

8. Report the result with:

   - commit hash and subject
   - pushed branch and remote
   - verification commands and outcomes
   - any files intentionally left unstaged

## Safety Rules

- Never use `git add .` or `git add -A` when unrelated changes are present.
- Never amend, rebase, force-push, reset, clean, or delete branches unless the user explicitly asks for that exact operation.
- Never commit secrets or likely sensitive files such as `.env`, private keys, tokens, kubeconfigs, or credential exports.
- Do not push to `main`, `master`, `prod`, `production`, or a protected-looking shared branch without explicit confirmation.
- If a command fails because authentication, remote permissions, branch protection, or network access is required, report the failure and ask for the required approval or user action.

## Common Commands

Use these as building blocks, adjusted to the repository:

```bash
git status --short --branch
git log --oneline -5
git diff --stat
git diff -- <path>
git add <path>
git diff --staged
git commit -m "<subject>"
git push
git push -u origin <branch>
```

Prefer explicit paths in staging commands and quote paths that contain spaces.
