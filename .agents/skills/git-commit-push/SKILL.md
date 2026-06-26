---
name: git-commit-push
description: Safely prepare, create, and push Git commits. Use when Codex is asked to commit changes, write a commit message, stage files, run pre-commit checks, push a branch, or complete a git commit-and-push workflow.
---

# Git Commit Push

## Overview

Use this skill to turn an existing working tree into a reviewed commit and push it to the configured remote. Prefer explicit user confirmation before committing or pushing when the requested scope is ambiguous, when untracked files exist, or when the push could affect a shared branch.

## Workflow

1. Report the current branch before changing anything:

   - If the `UserPromptSubmit` hook prints the branch, use that value.
   - If no hook output is visible, run the command below and tell the user the result before staging, committing, or pushing.

   ```bash
   git branch --show-current
   ```

2. Inspect repository state before changing anything:

   ```bash
   git status --short --branch
   git diff --stat
   git diff
   git diff --staged
   ```

3. Identify the intended commit scope:

   - Include only files that match the user's request.
   - Treat unrelated modified or untracked files as user work. Do not stage them unless the user explicitly includes them.
   - If scope is unclear, summarize the candidate files and ask before staging.

4. Run the smallest relevant verification before committing when feasible:

   - Use project-specific commands from `AGENTS.md`, package scripts, CI config, or nearby docs.
   - For Python hook or helper script syntax checks, prefer `ast.parse` over `py_compile` when bytecode cache writes may be blocked.
   - If checks are expensive or unavailable, say what was skipped and why.
   - Do not invent a full test suite when a focused check is clearly enough.

5. Stage the intended files explicitly:

   ```bash
   git add <file1> <file2>
   git status --short
   git diff --staged --stat
   git diff --staged
   ```

6. Write a concise commit message using the AngularJS convention:

   - Use `<type>(<scope>): <subject>` when a meaningful scope exists.
   - Use `<type>: <subject>` when no clear scope exists.
   - Prefer these types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, and `revert`.
   - Write the subject in imperative mood, lowercase after the type, without a trailing period.
   - Keep the first line under about 72 characters unless the repository clearly uses another limit.
   - Add a body only when it explains why the change was made or calls out tradeoffs.
   - Add a footer for issue references or breaking changes. Mark breaking changes with `BREAKING CHANGE:`.

   Examples:

   ```text
   feat(skills): add git commit push workflow
   fix(git): avoid staging unrelated files
   docs(skills): clarify push safety rules
   ```

7. Commit after confirming the staged diff matches the intended scope:

   ```bash
   git commit -m "<subject>"
   ```

8. Push only after checking the branch and upstream:

   ```bash
   git branch --show-current
   git remote -v
   git status --short --branch
   ```

   Use `git push` when an upstream already exists. Use `git push -u origin <branch>` only for a new branch after confirming the remote and branch name are correct.

9. Report the result with:

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
git commit -m "<type>(<scope>): <subject>"
git push
git push -u origin <branch>
```

Prefer explicit paths in staging commands and quote paths that contain spaces.
