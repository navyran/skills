# A 股名称与代码解析

## Resolution Order

1. Exact Yahoo-style ticker:
   - `600519.SS`, `000001.SZ`
2. Six-digit code:
   - Shanghai: `600`, `601`, `603`, `605`, `688`, `689` -> `.SS`
   - Shenzhen: `000`, `001`, `002`, `003`, `300`, `301` -> `.SZ`
   - Beijing: `4`, `8`, `9` prefix -> ask for confirmation unless a source says otherwise.
3. Chinese stock name:
   - Run `scripts/resolve_ashare.py`.
   - Prefer exact AStock matches from Eastmoney.
   - Fall back to Sina suggest.
   - If multiple candidates remain, ask the user.
4. If script fails:
   - Web search: `"<name> 股票代码 A股"`
   - Confirm with at least one credible source such as Eastmoney, Sina Finance, exchange page, company IR, or a major financial portal.

## Eastmoney Suggest

The resolver uses Eastmoney's public suggest endpoint:

```text
https://searchapi.eastmoney.com/api/suggest/get?input={query}&type=14&token=D43BF722C8E33B9C85D1B1C2E75F7E64
```

Relevant fields:

- `Code`: six-digit code
- `Name`: security name
- `Classify`: prefer `AStock`
- `SecurityTypeName`: often `沪A` or `深A`
- `MktNum`: `1` commonly Shanghai, `0` commonly Shenzhen
- `QuoteID`: Eastmoney market prefix plus code, e.g. `1.600519`

## Sina Suggest Fallback

The resolver falls back to:

```text
https://suggest3.sinajs.cn/suggest/type=11,12,13,14,15&key={query}&name=suggestdata
```

It returns GBK-encoded text with fields like:

```text
贵州茅台,11,600519,sh600519,贵州茅台,...
```

Use `sh` -> `.SS`, `sz` -> `.SZ`.

## MCP Options

If the user asks for MCP-based data access, search/install only after explicit approval. Candidate MCP servers found online:

- `firmmaple/a-share-mcp-server`: https://github.com/firmmaple/a-share-mcp-server
  - A-share basics, historical K data, financials, macro data.
- `zwldarren/akshare-one-mcp`: https://github.com/zwldarren/akshare-one-mcp
  - China stock data via akshare-one, including historical prices, real-time data, news, financial statements.
- `stockmcp/stock-data-mcp`: https://github.com/stockmcp/stock-data-mcp
  - A-shares, HK, US stocks, crypto with multi-source failover.
- AKShare MCP variants: broad financial data via AKShare.

Security rule: MCP servers are executable code. Inspect source and configuration before installing; prefer read-only tools and avoid sharing secrets unless necessary. Use the local resolver first for stock-name/code normalization; add an MCP only when live market, financial, news, funds, or announcement data is required.
