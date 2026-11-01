---
name: update-xueqiu-cookie
description: Refresh the Xueqiu cookie stored in the user's stock-data admin tool. Use when the user asks to update, refresh, replace, or sync Xueqiu or 雪球 cookies for pi.navyran.top, cookie_xueqiu, PyWebIO deal_text update_config, stock data, or the Xueqiu browser cookie export workflow.
---

# Update Xueqiu Cookie

## Goal

Update the `cookie_xueqiu` config value in the stock-data admin tool from the current logged-in Xueqiu browser session.

Treat the cookie as sensitive. Never paste, summarize, log, or include the cookie value in final responses, notes, skill edits, screenshots, or diagnostics. Refer to it as `<XUEQIU_COOKIE_HEADER>`.

## Workflow

1. Open Microsoft Edge and go to `https://xueqiu.com/`.
2. Confirm the page is logged in enough for cookies to include Xueqiu auth fields. If the user is not logged in, stop and ask them to log in manually.
3. Open the cookie-export browser extension from Edge's toolbar.
4. In the extension popup, use `Export`, then choose `Header String`. This places the cookie header string on the clipboard.
5. Open the stock admin update page:

```text
https://pi.navyran.top:3001/pywebio/?app=deal_text&func=update_config&param2=cookie_xueqiu
```

6. In the PyWebIO page, verify:
   - the page title or header is `文本处理`
   - `类型` is `更新配置`
   - `param2` is `cookie_xueqiu`
7. Paste the cookie header into the `param1` text area.
8. Click `处理`.
9. Verify completion by reloading the page and checking that `param1` is populated for `cookie_xueqiu`, without exposing the value.

## Stable Targets

- Xueqiu source site: `https://xueqiu.com/`
- Cookie extension popup: `chrome-extension://neaplmfkghagebokkhpjpoebhdledlfi/interface/popup/cookie-list.html`
- Cookie extension controls: `Export` button, then `Header String` button.
- Admin destination page: `https://pi.navyran.top:3001/pywebio/?app=deal_text&func=update_config&param2=cookie_xueqiu`
- Destination fields: `param1` text area, `param2` combo box with value `cookie_xueqiu`, `处理` button.

## Verification And Recovery

- If clicking `处理` appears to do nothing, wait briefly, reload once, and re-check whether `param1` remains populated for `cookie_xueqiu`.
- If the pasted value disappears after reload, repeat the paste and click `处理` once more.
- If the extension cannot export, ask the user to confirm the cookie extension is installed and has access to `xueqiu.com`.
- If Xueqiu requires login, ask the user to log in manually; do not request or handle passwords or OTPs.
- In the final response, state whether the update appeared to succeed and what was verified. Do not include cookie contents.
