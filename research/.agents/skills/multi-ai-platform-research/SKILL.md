---
name: multi-ai-platform-research
description: Use when Codex must research, compare, or synthesize answers across multiple AI chat platforms. Supports ego-lite/ego-browser isolated task spaces that inherit user login state, Browser Use control of exact existing Chrome tabs and cookies, Edge/Computer Use clipboard-save flows, simple DeepSeek/Qwen/Doubao runs, explicit custom platform lists, and broad active-platform studies.
---

# Multi AI Platform Research

## Objective

Run a controlled multi-platform AI research pass. Treat every page as a live system: verify login, model, mode, prompt submission, generation completion, capture, saved output, and cleanup instead of assuming any step worked.

## Resolve the Run

Before browser work, identify and briefly record:

- platforms, URLs, requested models/modes, and login requirements;
- scenario: simple, complex, or explicit custom list;
- shared prompt versus platform-specific prompts;
- browser backend: `ego-lite`, `browser-use`, or `edge-computer-use`;
- capture directory, defaulting to `/Users/navin/Workspace/docs/clipboard/<YYYYMMDD>/`;
- raw-only versus synthesized Markdown report;
- completion requirements implied by the prompt, such as required numbered sections.

Claude and Gemini are paused. Do not open, attempt, or count them in any preset or “all AI” run unless the user explicitly says to restore or unpause them.

Choose conservative defaults when details are omitted and state assumptions briefly.

## Browser Backend Routing

Apply explicit user intent first:

1. Use ego-lite when the user says `ego-lite`, `ego-browser`, or asks for an isolated agent browser that inherits login state without disturbing normal browser windows.
2. Use Browser Use when the user says `Browser Use`, rejects Computer Use, asks for the existing Chrome session, or needs exact current Chrome tabs/page state.
3. Use Edge + Computer Use when the user explicitly requests Edge, the already-open Edge window, or the `Shift + Command + P` clipboard-save workflow.
4. During the ego-lite rollout, default to Browser Use when the user names no browser backend. Do not silently change established behavior.

Do not silently change an explicitly requested backend. Ego-lite inherits the user's login state but creates isolated tabs; it does not reuse the exact currently open Chrome tabs.

Read exactly the backend reference needed for the run:

- Ego-lite: read [references/ego-lite-protocol.md](references/ego-lite-protocol.md) completely and load the available `ego-browser` skill.
- Browser Use or Edge: read [references/browser-use-protocol.md](references/browser-use-protocol.md) completely and load the matching browser-control skill.

For all runs, read [references/platform-adapters.md](references/platform-adapters.md) and [references/capture-and-reporting.md](references/capture-and-reporting.md) completely before opening platform pages.

## Scenario Selection

- Simple: use DeepSeek, Qwen, and Doubao for narrow/default/quick research or when depth is omitted.
- Complex: use the full active-platform preset (currently 9 platforms; Claude and Gemini excluded) when the user says `复杂`, `全部AI`, `全部预设平台`, broad cross-checking, high-confidence comparison, or equivalent.
- Explicit list: use exactly the named active platforms and record `custom scenario`; paused Claude/Gemini remain excluded unless the user explicitly unpauses them.
- If the user says “previous AI sites” after a complex run, treat it as complex unless they also say quick/simple.

Platform URLs, model/mode rules, selectors, and the complex preset live in `references/platform-adapters.md`.

## Unified Workflow

### 1. Prepare

- Optimize the research prompt when requested, preserving the user's intent.
- Save the final shared prompt when the user requests raw artifacts or reproducibility.
- Create a run timestamp for file provenance.
- Create or verify the capture directory before browser work; it is also the required download destination for Baidu Wenxin native result artifacts.
- For ego-lite, create one task space and record its numeric ID.

### 2. Open and Inspect

- Open one controlled tab per selected platform.
- Open/configure tabs sequentially to avoid focus races.
- Capture a screenshot or semantic/body-text summary before interaction.
- Record login state as logged-in, guest, logged-out, captcha, or blocked.
- Never infer login from inherited cookies alone.

### 3. Select Model and Mode

- Use visible labels and semantic controls before coordinates or direct DOM logic.
- Verify the selected state after every click.
- Record requested and actual model/mode separately.
- Never silently downgrade a model or deep/expert mode.
- If a paywall/login wall blocks the requested mode, record it and use handoff or ask for direction rather than pretending success.

### 4. Submit

- Fill the visible composer, not a hidden mirror textarea.
- For long Chinese/mixed prompts, use the backend's reliable fill method and verify input length/head before sending.
- Submit only after exact prompt visibility/focus is confirmed.
- Record the resulting conversation URL.

### 5. Wait for Completion

- Poll platform generation indicators and final-answer length.
- Require the stop indicator to disappear and answer length to remain stable for three polls.
- Validate requested structure and ending content; stable but truncated output is not complete.
- Continue waiting through recoverable network reconnects.
- If truncated, continue in the same conversation and preserve all raw parts.

### 6. Capture and Save

- Prefer a verified platform copy action; otherwise extract the final assistant DOM.
- Exclude sidebars, histories, prompt suggestions, user messages, thinking text, hidden export cards, and duplicate visualization containers.
- Save each platform immediately after completion with full provenance metadata.
- For Baidu Wenxin, use the current `任务` mode. Download every generated native result artifact into the run capture directory, verify the downloaded file, then preserve or convert its full content to Markdown as described in the adapter and capture protocol.
- Read each saved file back and verify size, header, ending, required sections, and caveats.

Follow `references/capture-and-reporting.md` for the metadata block and verification commands.

### 7. Synthesize

- Use only raw files from the current run as model-response sources.
- Separate cross-platform consensus, disagreements, unique insights, evidence gaps, and recommended actions.
- Do not convert model agreement into factual certainty. Independently verify current/high-stakes claims when required.
- Include a status/source table with platform, requested/actual mode, browser backend/task-space ID, conversation URL, raw path, capture method, and caveats.

### 8. Finish

- Verify every selected platform was attempted and every completed answer has a readable raw file.
- Report blockers, downgrades, reconnects, continuations, duplicate sections, and extraction fallbacks.
- For ego-lite, finish with `completeTaskSpace(id, { keep })` in a dedicated final heredoc after output validation. Default to `keep: false`; retain pages only when explicitly requested or required for manual continuation.
- Never close unrelated user tabs in Browser Use or Edge.

## Login and Control Safety

- Never type passwords, solve MFA/captcha, grant consent, or choose an ambiguous account for the user.
- With ego-lite, hand off the task space for manual action and resume only after explicit user confirmation. User-control/inactive errors are hard stops; do not retry around them.
- With Browser Use/Edge, stop and ask when manual login, MFA, captcha, consent, or account choice is required.
- Guest/basic mode is acceptable only when it still satisfies the request and the downgrade is recorded.

## Success Criteria

A run succeeds only when:

- every requested platform was attempted;
- login and actual model/mode were observed;
- submission and conversation URL were verified, or a blocker was recorded;
- completion was checked against indicators, stable length, and requested structure;
- raw Markdown was saved and read back for every completed platform;
- synthesis was produced when requested;
- the requested browser backend and cleanup policy were honored.

## Failure Policy

- Record platform-specific login, model, captcha, rate-limit, copy, network, or generation failures without hiding them.
- Do not downgrade model, mode, platform set, browser backend, or capture method silently.
- Do not synthesize a missing platform as though it answered.
- If source files are ambiguous, place them in a needs-review list rather than guessing provenance.

## Invocation Examples

Use the complete invocation templates in `references/capture-and-reporting.md`. Preferred ego-lite form:

```text
使用 $multi-ai-platform-research，走 ego-lite + 用户登录态，打开 DeepSeek、千问、豆包，分别调研「<问题>」。等待回答完成，保存原始 Markdown，并综合各平台的共识、分歧和建议。完成后关闭本次 ego-lite Task Space。
```
