# Browser Use and Edge Protocols

## Browser Use with Existing Chrome

Use this path when the user explicitly requests Browser Use, rejects Computer Use, asks to reuse current Chrome tabs, or needs the exact current Chrome page state.

```bash
browser-use <<'PY'
print(page_info())
print(list_tabs())
PY
```

- If connection fails, run `browser-use --doctor` and report the actual blocker.
- Confirm that `list_tabs()` contains the user's real current work/personal tabs. Stop if a blank or guest profile is attached by mistake.
- Use `new_tab(url)` for first navigation and create platform tabs sequentially.
- Take a screenshot or inspect body text before clicking.
- Use `click_at_xy`, `js(...)`, `press_key`, and `capture_screenshot()`.
- For long Chinese prompts, use the native textarea setter plus `InputEvent`, verify length/head, then submit.
- Poll the final answer selector and generation indicators until the stop indicator disappears and answer length is stable for three polls.
- Preserve conversation URLs and save each result immediately after completion.

Browser Use attaches to exact live Chrome state. Do not manipulate unrelated tabs or close user tabs.

## Other Attached or Dedicated Profiles

Use an existing browser only when it exposes a remote debugging port. If exact live state is unnecessary, a dedicated automation profile is safer than the user's primary profile. A copied profile is only a diagnostic fallback because Cookie, IndexedDB, and Local Storage may be stale or device-bound.

Never claim a copied/dedicated profile is logged in until each target page confirms it.

## Edge + Computer Use

Use Edge with Computer Use when the user explicitly requests Edge, the already-open Edge window, or the `Shift + Command + P` clipboard-save workflow.

- Inspect application state before interacting.
- Reuse matching tabs; open only missing platforms.
- Use `printf '%s' '<prompt>' | pbcopy` and paste with `super+v` for Chinese or mixed text.
- Use `super+a` only after verifying focus in the target chat composer.
- Treat `super` as Command on macOS.
- Click the answer's copy control and verify with `pbpaste` before saving or switching platforms.
- Run `shift+super+p` only after copy verification when requested.

## Saved Clipboard Shortcut

Before the first shortcut-save, create a timestamp:

```bash
stamp="$(mktemp)"
touch "$stamp"
```

After each verified copy, press `shift+super+p`, wait for the write, and locate files newer than the timestamp:

```bash
root="/Users/navin/Workspace/docs/clipboard"
today="$(date +%Y%m%d)"
if [ -d "$root/$today" ]; then
  find "$root/$today" -type f -newer "$stamp" -name '*.md' -print
else
  find "$root" -path "$root/node_modules" -prune -o -path "$root/outputs" -prune -o \
    -type f -newer "$stamp" -name '*.md' -print
fi
```

Treat the saved files, not clipboard text, as the authoritative synthesis input. If no file appears, record the failure and preserve verified clipboard text as fallback.
