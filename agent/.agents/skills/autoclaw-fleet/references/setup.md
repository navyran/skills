# AutoClaw Fleet Setup

## Deployment map

| Target | Purpose | Gateway URL | State |
|---|---|---|---|
| `publish` | Windows publish server | `http://172.16.16.2:18790` | Address and Token confirmed; Token stored in macOS Keychain |
| `login-reply` | Windows login/reply server | `http://172.16.16.3:18789` | Token stored in macOS Keychain |

The existing `script1` and `script2` SSH aliases terminate on Linux login servers. Both Windows targets now use the AutoClaw HTTP endpoint on port `18790`; verify each target independently after its Token is configured.

## Call the Agent HTTP endpoint

Both servers expose the OpenAI-compatible endpoint at `/v1/chat/completions`. Use model `openclaw` for the default Agent or `openclaw/<agentId>` for a specific Agent:

```bash
curl http://172.16.16.2:18790/v1/chat/completions \
  -H "Authorization: Bearer $AUTOCLAW_PUBLISH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"你好"}]}'
```

`172.16.16.3:18789` uses the same path, headers, and request body. The credential grants full operator access, so keep both endpoints on a private network and restrict inbound ports `18790` and `18789` to trusted hosts.

## Configure targets

The skill has built-in default URLs for `publish` and `login-reply`. Override them when ports or tunnel addresses differ:

```bash
export AUTOCLAW_TARGETS=publish,login-reply
export AUTOCLAW_PUBLISH_URL=http://172.16.16.2:18790
export AUTOCLAW_LOGIN_REPLY_URL=http://172.16.16.3:18789
```

Because these supplied URLs use plaintext `ws://` on non-loopback addresses, either replace them with WSS/tunnel URLs or explicitly opt in:

```bash
export AUTOCLAW_ALLOW_INSECURE_HTTP=1
```

Optional per-target routing:

```bash
export AUTOCLAW_PUBLISH_MODEL=openclaw/main
export AUTOCLAW_LOGIN_REPLY_MODEL=openclaw/main
```

Omit the model variables to use the default `openclaw` model. Alternatively, set `AUTOCLAW_<TARGET>_AGENT_ID`; the bridge converts it to `openclaw/<agentId>` when no explicit model variable is set.

## Store tokens safely

Choose one source per target. Priority is environment, token file, then macOS Keychain.

Environment (matches the original proposal but can leak through process inspection or shell setup files):

```bash
export AUTOCLAW_PUBLISH_TOKEN=<publish-token>
export AUTOCLAW_LOGIN_REPLY_TOKEN=<login-reply-token>
```

Mode-`0600` token files:

```bash
export AUTOCLAW_PUBLISH_TOKEN_FILE=/secure/path/publish.token
export AUTOCLAW_LOGIN_REPLY_TOKEN_FILE=/secure/path/login-reply.token
```

macOS Keychain (recommended for a resident Codex app):

```bash
security add-generic-password -U -a publish -s autoclaw-fleet -w
security add-generic-password -U -a login-reply -s autoclaw-fleet -w
```

Each command reads the secret interactively. The client retrieves it without placing it in a command argument or log.

## Verify

From the skill directory:

```bash
python3 scripts/autoclaw_bridge.py config
python3 scripts/autoclaw_bridge.py health --target all
AUTOCLAW_ALLOW_INSECURE_HTTP=1 python3 scripts/autoclaw_bridge.py status --target all
```

- `health` calls unauthenticated `/healthz` and validates the network path.
- `status` calls authenticated `/v1/models`; use `dispatch` to verify the Agent completion endpoint itself.
- Only a successful `dispatch` response proves the Agent accepted and completed a task.

## Remaining live-deployment input

If connectivity fails, verify the route/listener for `172.16.16.3:18789`. The bridge deliberately bypasses HTTP proxies for private IP targets so a proxy-generated `502` is not mistaken for a Gateway response.
