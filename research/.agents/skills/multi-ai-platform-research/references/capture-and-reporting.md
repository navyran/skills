# Capture, Save, and Reporting Protocol

## Contents

- Raw File Metadata
- Capture Priority
- Synthesis Requirements
- Success Criteria
- Invocation Examples
- Operational Lessons

## Raw File Metadata

Save direct-extraction runs under:

```text
/Users/navin/Workspace/docs/clipboard/<YYYYMMDD>/
```

Put this provenance block at the top of every raw Markdown file:

```markdown
# <platform> 原始回答

- 浏览器后端：<ego-lite / browser-use / edge-computer-use>
- Task Space ID：<ego-lite numeric id or N/A>
- 平台：<platform>
- 请求模型/模式：<requested>
- 实际模型/模式：<actual>
- 登录状态：<logged-in / guest / blocked>
- 对话链接：<url>
- 获取方式：<page-copy / DOM extraction / clipboard shortcut / fallback>
- 平台下载产物：<absolute path in capture directory or N/A>
- 提交时间：<timestamp>
- 完成/提取时间：<timestamp>
- 异常与降级：<none or details>

---
```

Preserve the platform response without silently correcting factual claims. Normalizing rendered headings/tables into Markdown is allowed; state that normalization occurred. Preserve platform duplication, truncation, continuation, diagram failures, and network reconnect caveats explicitly.

For Baidu Wenxin `任务` mode:

1. Set the browser download destination to the current run capture directory before downloading when the backend supports it.
2. Otherwise download normally, then copy the completed artifact into the capture directory; do not treat the default Downloads copy as the final target artifact.
3. Verify the target artifact with filename, byte size, and successful read/open before capture.
4. If Wenxin returns DOCX/PDF instead of inline text, retain the original artifact and extract or convert its complete contents into the platform raw Markdown. Record both the artifact path and conversion method.

## Capture Priority

1. Use the platform's copy action when it provides the entire final answer.
2. Otherwise extract the final assistant DOM.
3. For virtualized output, scroll/read all content or use the official copy action.
4. Treat screenshots/OCR as a last resort and label it.
5. Never save sidebars, chat history, prompt suggestions, hidden export cards, or thinking text as final output unless the user requested them.

After every file write, verify:

```bash
ls -lh /absolute/path/to/file.md
wc -m /absolute/path/to/file.md
sed -n '1,18p' /absolute/path/to/file.md
tail -18 /absolute/path/to/file.md
```

Also check required sections/keywords from the prompt. A non-empty file is not proof of a complete answer.

## Synthesis Requirements

Use only files created for the current run. Match provenance using task-space ID/browser backend, platform, conversation URL, timestamp, run order, filename, and answer text. Put ambiguous files in a needs-review list instead of guessing.

The synthesized Markdown report must include:

- run date, prompt, scenario, browser backend, and raw directory;
- requested versus actual model/mode status;
- source-file index with platform, URL, raw path, capture method, and caveats;
- cross-platform consensus;
- disagreements and unique insights;
- missing evidence and claims requiring independent verification;
- prioritized recommendations and action checklist;
- blockers, downgrades, captcha, rate limit, generation failures, and continuations.

Use this status shape:

```markdown
## 页面与模式状态

| 平台 | 要求 | 实际状态 | 浏览器/任务空间 | 原始文件 | 获取方式 |
| --- | --- | --- | --- | --- | --- |
| <platform> | <requested model/mode> | <actual state> | <backend / task id> | `<path>` | <copy/dom/blocker> |
```

## Success Criteria

A run is complete only when:

- every selected platform was attempted;
- login and actual model/mode were observed;
- each submitted prompt has a conversation URL or a recorded blocker;
- generation completion was verified, not inferred from the first visible text;
- each raw file was read back and checked for completeness;
- every Baidu Wenxin native result artifact was downloaded into and verified from the run capture directory;
- synthesis covers consensus, disagreement, evidence gaps, and recommended actions;
- ego-lite task-space cleanup or preservation was verified when ego-lite was used.

## Invocation Examples

Ego-lite simple report:

```text
使用 $multi-ai-platform-research，走 ego-lite + 用户登录态，用简单场景打开 DeepSeek、千问、豆包，分别调研「<问题>」。等待全部回答完成，保存原始 Markdown，并综合共识、分歧和建议。完成后关闭本次 ego-lite Task Space。
```

Ego-lite raw collection only:

```text
使用 $multi-ai-platform-research，走 ego-lite，只打开 DeepSeek、千问、豆包调研「<问题>」。保存每个平台的原始 Markdown，列出实际模型、Task Space ID、对话链接、文件路径和阻塞；本次不要综合。
```

Browser Use with exact Chrome state:

```text
使用 $multi-ai-platform-research，走 Browser Use + 现有 Chrome 登录态，不使用 Computer Use。打开 DeepSeek、千问、豆包调研「<问题>」，保存原始 Markdown 并综合。
```

Complex report:

```text
使用 $multi-ai-platform-research，复杂场景调研「<问题>」。按明确指定的浏览器后端执行全部预设平台，保存每份原始回答，再输出包含共识、分歧、盲区、证据核验项和行动清单的综合报告。
```

## Operational Lessons

- Qwen guest conversations can disappear after restart; save before closing the session.
- Qwen must use Qwen3.8-Max + Thinking; do not select Preview.
- Kimi must use K2.6 + 快速 and record any automatic substitution.
- Baidu Wenxin uses the current `任务` mode; its generated native artifacts belong in the run capture directory and must be verified there.
- Doubao expert/deep modes may require login. Record downgrade or hand off instead of pretending selection succeeded.
- DeepSeek DOM may mix thinking and final text; prefer the final-answer selector or copy action.
- A copied browser profile may retain some sites but lose others; verify each page.
- Network reconnection can create duplicate answer fragments. Preserve raw output and deduplicate only in the synthesis with a note.
- `Shift + Command + P` is authoritative only after the newly created Markdown file is found and read back.
