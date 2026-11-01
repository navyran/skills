# Ego-lite Browser Protocol

Use this protocol when the user explicitly requests `ego-lite` or `ego-browser`. Load and follow the available `ego-browser` skill before operating the browser; its ownership and handoff rules are authoritative.

## Contents

- Session Model
- Observe and Act
- Submission and Completion
- Login, Captcha, and User Control
- Capture
- Finish
- Failure Policy

## Session Model

- Create one isolated ego-lite task space for the whole research run. It inherits the current user's login state by default but does not reuse the user's current tabs.
- Use a short task-space name derived from the topic and date.
- Record the numeric task-space ID immediately and reuse it in every later heredoc.
- Open one tab per platform in that task space. Open and configure tabs sequentially to avoid focus races; after all prompts are submitted, poll tabs round-robin.
- Verify login separately on every platform. Inherited state is not proof that a session is valid.

Start a run:

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace('multi-ai-research-topic')
cliLog(JSON.stringify({ taskSpaceId: task.id, tabs: await listTabs() }))
EOF
```

Resume a normal agent-owned run with the numeric ID:

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace(123)
cliLog(JSON.stringify({ taskSpaceId: task.id, tabs: await listTabs() }))
EOF
```

Open pages sequentially:

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace(123)
for (const url of [
  'https://chat.deepseek.com/',
  'https://chat.qwen.ai/',
  'https://www.doubao.com/chat',
]) {
  await openOrReuseTab(url, { wait: true, timeout: 30 })
}
cliLog(await listTabs())
EOF
```

## Observe and Act

Use this order:

1. Call `snapshotText()` and use its `@N` refs or stable `loc=...` locators.
2. Use `click()` and `fillInput()` for ordinary DOM controls.
3. Verify every meaningful state change with a new `snapshotText()`, `pageInfo()`, or `captureScreenshot()`.
4. Use screenshot coordinates only when semantic controls are incomplete.
5. Use a single explicit IIFE with `js()` for compact DOM inspection, native input setters, or answer extraction.

Refs from `snapshotText()` are valid only for the latest snapshot. Keep a stable `loc=...` or CSS selector for later rounds.

For long Chinese or mixed-language prompts, first try `fillInput()` and verify the visible input value:

```javascript
await fillInput('textarea[placeholder="Message DeepSeek"]', prompt)
const check = await js(String.raw`(() => {
  const el = document.querySelector('textarea[placeholder="Message DeepSeek"]')
  return { length: el?.value.length || 0, head: el?.value.slice(0, 40) || '' }
})()`)
cliLog(check)
```

If framework state does not update, use the native setter plus `InputEvent`, then verify again before sending. Use focused `typeText()` only as the final fallback.

## Submission and Completion

- Store the conversation URL after submission.
- Do not treat the first answer chunk as completion.
- Poll the preferred answer selector and generation indicators such as `Stop`, `Thinking`, `正在思考`, `生成中`, or `停止生成`.
- Require the stop indicator to disappear and the answer length to remain unchanged for three polls. Also verify the requested structure is present.
- Use `wait(seconds)`; timeout values in ego-browser are seconds unless the parameter name ends in `Ms`.
- If the page shows a network reconnect but continues growing, keep waiting.
- If the answer is genuinely truncated, send a continuation prompt in the same conversation and preserve both raw parts.

Recommended polling shape:

```javascript
let previous = -1
let stable = 0
for (let i = 0; i < 120; i++) {
  const state = await js(String.raw`(() => {
    const answers = [...document.querySelectorAll('.assistant-answer')]
    const final = answers.at(-1)
    return {
      length: final?.innerText.length || 0,
      stopVisible: Boolean(document.querySelector('[aria-label="Stop"]')),
    }
  })()`)
  stable = !state.stopVisible && state.length > 0 && state.length === previous ? stable + 1 : 0
  if (stable >= 3) break
  previous = state.length
  await wait(5)
}
```

Replace selectors with the platform adapter. After the loop, check completeness rather than trusting length alone.

## Login, Captcha, and User Control

- If login, captcha, MFA, consent, or ambiguous account choice requires the user, call `handOffTaskSpace(task.id)` and check that its result has `done: true` before reporting handoff.
- Tell the user the exact platform and action required.
- While the user controls the task space, do not retry browser operations or switch to another browser to bypass the handoff.
- Resume only after the user explicitly says to continue. Start that heredoc with `takeOverTaskSpace(task.id)`.
- If a task space is user-owned, inactive, or unassigned, ask for confirmation before calling `claimTaskSpace(id)`.
- Never call `takeOverTaskSpace()` automatically.

## Capture

- Prefer the platform copy control when it returns the complete final answer reliably.
- Otherwise extract the final assistant DOM. Filter for visible assistant blocks and compare candidate lengths so hidden mind maps, duplicate export cards, histories, and sidebars are not saved as answers.
- When a page virtualizes long answers, use the official copy action or scroll/read through the full answer before extraction.
- Send extracted text through `cliLog()`; it is the only supported heredoc output mechanism.
- Save using the common capture protocol and record `browser backend: ego-lite`, task-space ID, extraction method, requested/actual mode, URL, timestamps, and caveats.

## Finish

Only after a prior heredoc confirms that all raw files and the synthesis are valid, finish in a dedicated final heredoc:

```bash
ego-browser nodejs <<'EOF'
const result = await completeTaskSpace(123, { keep: false })
cliLog(result)
EOF
```

- Default to `keep: false`.
- Use `keep: true` only when the user explicitly asks to keep pages open or must continue manually in that exact task space.
- If keeping the task space, close scratch tabs first and retain only useful result pages.
- Check `done` before claiming cleanup succeeded.

## Failure Policy

- When ego-lite was explicitly requested, do not silently switch to Browser Use or Computer Use.
- If the first command reports a missing ego-lite installation, load the ego-browser installation reference and follow it; report any blocker.
- If the browser backend was not explicitly requested and a fallback is allowed, record the failed backend and the actual fallback in every result file and the status table.
