# AutoClaw Fleet Deployment

Use this procedure when pulling and restarting `autorespo` on either Windows target.

## Target map

| Target | Gateway | Repository | Start script |
|---|---|---|---|
| `publish` | `http://172.16.16.2:18790` | `C:\Users\xll\Desktop\autorespo` | `C:\Users\xll\Desktop\autorespo\start_localprod.bat` |
| `login-reply` | `http://172.16.16.3:18789` | `C:\Users\xll\Desktop\xshadow\autorespo` | `C:\Users\xll\Desktop\xshadow\autorespo\start_localprod.bat` |

Do not infer one target's path from the other. Do not deploy both unless the user explicitly requests both.

## Required procedure

1. Run Gateway `health` and authenticated `status` for the selected target.
2. In the mapped repository, record:
   - current branch and upstream;
   - `git status --short --branch`;
   - staged and unstaged tracked diff summaries that will be discarded;
   - `git ls-files --others --exclude-standard` so untracked files can be verified as preserved;
   - current HEAD commit;
   - application PID, command line, and listening ports.
3. Require a named current branch with a configured upstream. Treat an explicit deploy/update-and-restart request as authorization to discard staged and unstaged changes to tracked files on the selected server.
4. Force-sync the tracked branch without touching untracked files:
   - resolve the current branch's configured upstream remote and branch; do not assume the remote is named `origin`;
   - run `git fetch <upstream-remote> <upstream-branch>` and resolve the fetched commit from `FETCH_HEAD`;
   - verify the current HEAD is equal to or an ancestor of the fetched upstream. If the server has local commits that are ahead or divergent, stop and report them; the authorization to discard uncommitted work does not authorize deleting commits;
   - compare every untracked path with the fetched tree, including file/directory prefix collisions. If the reset would overwrite or remove an untracked path, stop and report the conflict;
   - run `git reset --hard <fetched-upstream>`;
   - never run `git clean`, and never delete, move, add, commit, or stash untracked files.
5. Verify HEAD equals the fetched upstream, tracked status is clean, and the before/after untracked lists are identical. If force-sync or preservation verification fails, do not terminate or restart the application.
6. Record the new HEAD and force-sync summary. If HEAD did not change, continue with the requested restart.
7. Identify only the selected repository's application process tree. Use its recorded PID/listening port and `Win32_Process` command line. Never kill every `python.exe`, `node.exe`, or `cmd.exe`; never stop the AutoClaw/OpenClaw Gateway on port `18789` or `18790`.
8. Terminate the identified application process tree and confirm its application port is released.
9. Start the mapped batch file with the mapped repository as `WorkingDirectory`. Use a detached Windows process so the Agent request can return, for example:

   ```powershell
   Start-Process -FilePath "cmd.exe" `
     -ArgumentList "/c", "<absolute-start-script>" `
     -WorkingDirectory "<absolute-repository>" `
     -WindowStyle Hidden
   ```

10. Wait up to 60 seconds and verify all of the following:
   - a new project application PID exists with the expected command line;
   - the application port is listening under that PID;
   - the local application endpoint returns HTTP 200 and valid JSON (normally `http://127.0.0.1:8000/api/windows` for this project);
   - an external probe succeeds when a trusted reachable host is available.
11. If startup fails or exits, collect the batch output or latest application log and report the concrete error. Do not claim success from Gateway health or process existence alone.

## Dispatch and reporting

Prefer background dispatch for a deployment so it has a durable `job_id`:

The Windows Agent cannot read this local skill reference. Expand the selected target's paths and the required procedure into the remote prompt; do not tell the remote Agent merely to read `references/deploy.md`.

```bash
AUTOCLAW_ALLOW_INSECURE_HTTP=1 python3 scripts/autoclaw_bridge.py dispatch \
  --target <publish-or-login-reply> \
  --background \
  --prompt "In <absolute-repository>, record tracked changes and untracked paths, resolve and fetch the current branch's configured upstream, stop on local commits or untracked path collisions, then reset --hard to FETCH_HEAD without running git clean. Verify untracked paths are unchanged. Only then terminate this application's process tree, start <absolute-start-script> detached with the repository as WorkingDirectory, and verify the new PID, listening port, and HTTP 200 JSON response."
```

Report the target, health/auth state, branch, old/new commit, discarded tracked changes, preserved untracked count/list, force-sync result, terminated PID, new PID, listening port, HTTP result, `job_id`, and `task_id`. Report each target separately when both are explicitly requested.
