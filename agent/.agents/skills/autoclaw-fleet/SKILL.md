---
name: autoclaw-fleet
description: Control, monitor, and deploy two Windows OpenClaw/AutoClaw Gateway instances from Codex. Use when Codex must run an automation or development prompt on the publish server, login-reply server, or both; pull and restart either autorespo application; launch independent Gateway agent runs in parallel/background mode; check Gateway reachability and authentication; or retrieve a background job result.
---

# AutoClaw Fleet

Control the configured Windows gateways with `scripts/autoclaw_bridge.py`. The publish server exposes its OpenAI-compatible AutoClaw endpoint on port `18790`, while the login/reply server uses port `18789`; do not install the unrelated `CodexBridge` server, which exposes Codex in the opposite direction.

## Prepare

Resolve this skill directory and run the bundled script from it. If configuration or health fails, read [references/setup.md](references/setup.md).

Never print, log, commit, or place a Gateway token in a URL, task prompt, or command argument. The client resolves tokens from a target-specific environment variable, a mode-`0600` token file, or macOS Keychain, then sends the secret only in the `Authorization` header.

## Dispatch workflow

1. Identify the requested target:
   - `publish`: Windows publish server (`http://172.16.16.2:18790`); token configured.
   - `login-reply`: Windows login/reply server (`http://172.16.16.3:18789`); token configured.
   - `all`: both servers.
2. Ask before expanding a state-changing request from one server to both. Do not send identical repository edits to both unless the workspaces/scopes are isolated.
3. Run `health`, then `status`. `health` proves network liveness; `status` proves the token and Agent HTTP endpoint work.
   Requests use `POST /v1/chat/completions`, a Bearer token, and model `openclaw` or `openclaw/<agentId>`.
4. Run a foreground task when the result is needed now:

   ```bash
   AUTOCLAW_ALLOW_INSECURE_HTTP=1 python3 scripts/autoclaw_bridge.py dispatch \
     --target login-reply \
     --prompt "Open the browser, inspect the requested page, and report the result" \
     --timeout 1800
   ```

5. Run independent long tasks without blocking Codex:

   ```bash
   AUTOCLAW_ALLOW_INSECURE_HTTP=1 python3 scripts/autoclaw_bridge.py dispatch \
     --target all \
     --background \
     --prompt "Run the assigned automation task and return a concise completion report"
   ```

   Record the returned `job_id` and `task_id`. Background mode detaches the local authenticated HTTP request; it does not weaken the remote agent's tool/approval policy.
6. Retrieve a background result:

   ```bash
   python3 scripts/autoclaw_bridge.py job --job-id <job-id>
   ```

7. Report every target separately with health/auth state, task/job ID, final response, and any target-specific failure.

Use `--prompt-file` for a long prompt and `--session` only when follow-up turns must share one OpenClaw conversation.

## Deploy autorespo

Use the exact target mapping below; the two Windows repositories are in different directories:

- `publish`: `C:\Users\xll\Desktop\autorespo`, restart with `C:\Users\xll\Desktop\autorespo\start_localprod.bat`.
- `login-reply`: `C:\Users\xll\Desktop\xshadow\autorespo`, restart with `C:\Users\xll\Desktop\xshadow\autorespo\start_localprod.bat`.

Before deploying, read and follow [references/deploy.md](references/deploy.md). Treat it as the required release procedure. Deploy only the target requested by the user; obtain explicit authorization before deploying both.

Deployment force-syncs the selected server's current tracked branch to its upstream: discard staged and unstaged tracked changes, but preserve untracked files. Never run `git clean`.

## Boundaries

- Treat the Gateway credential as full operator access.
- Require explicit authorization before destructive desktop/system actions or duplicated writes across both targets.
- Prefer WSS/HTTPS or a loopback tunnel. Plain `ws://`/HTTP to a non-loopback address requires `AUTOCLAW_ALLOW_INSECURE_HTTP=1` and explicit acceptance of plaintext LAN transport.
- Do not claim success from `health` alone. A task succeeds only when `/v1/chat/completions` returns an Agent result.
- Do not claim remote cancellation support. Stopping the local background worker may not stop an already-admitted remote Agent run.
