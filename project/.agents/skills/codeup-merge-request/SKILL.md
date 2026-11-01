---
name: codeup-merge-request
description: Push a Git branch and create or reuse an Alibaba Cloud Codeup merge request through its GitLab V4-compatible API. Use when the user asks to publish code, push a feature branch, create a Codeup MR/PR, or submit code for review in 云效 Codeup.
---

# Codeup Merge Request

Use `scripts/create_merge_request.py` for the API call. Read the script help before using an unfamiliar option.

## Required configuration

Read secrets only from the environment; never put tokens in a command, commit message, MR description, skill file, or log.

```bash
export CODEUP_BASE_URL='https://codeup.aliyun.com'  # Optional: enterprise domain
export CODEUP_PROJECT_ID='123456'                   # Or pass --project-id
export CODEUP_PRIVATE_TOKEN='...'                   # API-scoped personal token
```

## Workflow

1. Inspect `git status --short`, current branch, remote, and the target branch. Stop if the working tree is dirty or branch/target/project are ambiguous.
2. Run tests and builds appropriate to the changed code before publishing.
3. Run a preflight without `--confirm`; it verifies the Git state and reports the intended push/MR without changing remote state.
4. Before any external mutation, make sure the user explicitly authorized the exact source branch, target branch, title, and publish action. Do not assume `master`; use the repository default branch only when it is discovered and unambiguous.
5. Run with `--confirm` to push the source branch and create the MR. The script reuses an existing open MR for the same source/target pair.
6. Return the MR URL, IID, source/target branches, and test results. Never output the token.

## Commands

```bash
# Safe preflight
python /Users/navin/.codex/skills/codeup-merge-request/scripts/create_merge_request.py \
  --target-branch main --title 'feat: concise summary'

# Push and create/reuse the MR after explicit authorization
python /Users/navin/.codex/skills/codeup-merge-request/scripts/create_merge_request.py \
  --target-branch main --title 'feat: concise summary' \
  --description-file /absolute/path/to/mr-description.md --confirm
```

Use `--project-id`, `--source-branch`, `--remote`, `--base-url`, or `--description` only when the defaults do not match the verified repository state.

## Safety rules

- Require a clean worktree. Do not auto-commit, amend, rebase, force-push, merge, or delete branches.
- Use normal `git push --set-upstream <remote> <source>` only; never force-push.
- The token must have Codeup `api` scope. If authentication fails, report the status code without exposing credentials.
- Treat a failed push or API error as a stop condition; do not retry blindly.
