# AI Platform Adapters

Read this file for every multi-platform run. Verify the current page rather than assuming selectors or models remain unchanged.

## Simple Preset

| Platform | URL | Requested model/mode | Preferred final-answer selector |
| --- | --- | --- | --- |
| DeepSeek | `https://chat.deepseek.com/` | `Expert`; enable `DeepThink` when available | `.ds-assistant-message-main-content` |
| Qwen | `https://chat.qwen.ai/` | `Qwen3.8-Max`; select `Thinking` | `.response-message-content.t2t.phase-answer`, `.custom-qwen-markdown`, `.qwen-markdown` |
| Doubao | `https://www.doubao.com/chat` | `专家` / `研究级专业问答 - 2.1 Turbo` | `.container-qX9Csx.md-box-root`, `.md-box-root`, `.container-h3Yzeb` |

## Complex Preset

| Platform | URL | Requested model/mode cue | Verification notes |
| --- | --- | --- | --- |
| DeepSeek | `https://chat.deepseek.com/` | Expert + DeepThink when available | Record any warning that Search is unavailable in Expert mode |
| Qwen | `https://chat.qwen.ai/` | Qwen3.8-Max; Thinking | Do not use Preview, an older model, or a Plus model |
| Doubao | `https://www.doubao.com/chat` | 专家模式 | Record login/paywall downgrade |
| Kimi | `https://www.kimi.com/` | K2.6 + 快速 | Verify both model and mode; copy only after streaming stops |
| Z.ai | `https://chat.z.ai/` | Enable search; choose GLM-5.2 when available | Verify both model label and search state |
| ChatGPT | `https://chatgpt.com/` | User-specified model/mode | Record login or model limits |
| Xiaomi MiMo | `https://aistudio.xiaomimimo.com/#/c` | Visible MiMo model; prior run used MiMo-V2.5-Pro | Verify search/thinking traces when requested |
| Tencent AI Studio | `https://aistudio.tencent.com/` | Enable 联网搜索; prior run used Hy3 preview + High | Verify globe/search state and thinking trace |
| Baidu Wenxin | `https://wenxin.baidu.com/?enter_type=chat_site` | 新版 `任务` 模式 | Verify the `任务` label before send; download the completed native result into the run capture directory |

## Paused Platforms

- Claude and Gemini are paused and are not part of Simple, Complex, explicit custom, or “all AI” runs.
- Do not open or attempt them merely because the user names “all supported platforms.”
- Re-enable them only after the user explicitly says to restore or unpause Claude/Gemini. A request that merely repeats an old platform list is not an unpause instruction.

## Shared Adapter Rules

- Prefer visible model/mode labels and semantic controls. After every selection, inspect the page again and record the actual label/state.
- For DeepSeek, choose Expert first and enable DeepThink when available. Record if the mode disables search.
- For Qwen, select Qwen3.8-Max and Thinking. Preview, older, Plus, and automatic substitutions are not acceptable silent fallbacks; record a blocker or ask for direction if Qwen3.8-Max is unavailable.
- For Doubao, open the mode menu and choose 专家. Verify the selected button/label after the menu closes.
- For Kimi, select K2.6 and 快速. Verify both visible labels before filling the prompt. Any automatic model or mode substitution is a recorded downgrade.
- For Baidu Wenxin, select the current `任务` mode before filling or sending the prompt and verify the visible mode label. After completion, download each generated DOCX/PDF/other native result into the run capture directory, verify filename and size, and record the artifact path in the raw Markdown metadata. If the backend cannot set a download directory, copy the completed download into the run capture directory before capture is considered complete. Convert or extract the native artifact to Markdown without altering its claims, and retain the downloaded original.
- When selectors fail, inspect visible assistant blocks sorted by text length, nearby role/message containers, and bounding rectangles. Exclude sidebars, histories, prompt suggestions, hidden export cards, duplicate mind maps, and user messages.
- If a page contains multiple final-answer fragments because of network reconnection, concatenate them in document order and note any duplicate sections.
- When a platform renders diagrams separately from the answer, preserve the textual error or fallback in the raw file and do not invent missing diagram content.
