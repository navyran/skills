---
name: ashare-stock-analysis
description: Analyze China A-share individual stocks from either a 6-digit stock code or Chinese stock name. Use when the user asks for A股, 中国股票, 个股分析, 股票分析, 看一下某只股票, or provides an A-share code/name such as 600519, 300750, 贵州茅台, 宁德时代, 平安银行. Resolves stock names to codes, normalizes to Yahoo-style .SS/.SZ tickers when useful, then produces a Chinese investment-research style report using professional analyst prompts without running or modifying TradingAgents unless explicitly requested.
---

# A 股个股分析

Use this skill to turn a user-provided A-share code or Chinese stock name into a structured Chinese stock analysis. Do not run or modify TradingAgents by default. Use its prompt patterns as domain guidance only.

## Quick Workflow

1. **Resolve the stock**
   - If the user gives a Yahoo-style ticker such as `600519.SS` or `000001.SZ`, accept it.
   - If the user gives a 6-digit code, normalize:
     - `600`, `601`, `603`, `605`, `688`, `689` -> `.SS`
     - `000`, `001`, `002`, `003`, `300`, `301` -> `.SZ`
     - `8`, `4`, `9` prefixes may be Beijing Stock Exchange; ask for confirmation unless the user already supplied a suffix.
   - If the user gives a Chinese stock name, run `scripts/resolve_ashare.py "<name>"` first.
   - If the resolver returns multiple plausible matches, show the top candidates and ask the user to choose.
   - If the resolver fails, use web search with query `"<stock name> 股票代码 A股"` and cite the source used.

2. **Load detailed prompts**
   - Read `references/prompt-pack.md` for the analyst prompt flow.
   - Read `references/report-template.md` for the final report structure.
   - Read `references/name-resolution.md` if name/code conversion is ambiguous or an MCP/data-source decision is needed.

3. **Gather data**
   - If current facts are needed, browse or use available MCP/tools. Do not fabricate prices, financials, announcements, or capital-flow figures.
   - If no live data is available, produce a framework-style analysis and clearly label missing data.
   - For A-share data MCP options, prefer read-only servers and inspect/configure them before use. Do not install MCP servers unless the user explicitly asks.

4. **Analyze in Chinese**
   - Apply the prompt flow: Market Analyst -> Fundamentals Analyst -> News/Announcement Analyst -> Sentiment/Funds Analyst -> Bull/Bear -> Trader -> Risk -> Portfolio Manager.
   - Keep the output practical: evidence, uncertainty, trading plan, risks, and final rating.
   - End with: `本报告仅用于研究辅助，不构成投资建议。`

## Resolver Script

Use:

```bash
python3 /Users/navin/.codex/skills/ashare-stock-analysis/scripts/resolve_ashare.py "贵州茅台"
python3 /Users/navin/.codex/skills/ashare-stock-analysis/scripts/resolve_ashare.py "600519"
python3 /Users/navin/.codex/skills/ashare-stock-analysis/scripts/resolve_ashare.py "宁德时代" --format text
```

The script returns JSON by default:

```json
{
  "query": "贵州茅台",
  "status": "ok",
  "candidates": [
    {
      "code": "600519",
      "name": "贵州茅台",
      "exchange": "上海证券交易所",
      "suffix": ".SS",
      "yahoo_ticker": "600519.SS",
      "source": "eastmoney"
    }
  ]
}
```

Use `yahoo_ticker` for Yahoo-compatible data sources. Use raw `code` for Chinese data sources such as AkShare, Baostock, Eastmoney, Tushare, or many A-share MCP servers.

## MCP Options

Do not assume an MCP is installed. If the user asks to use an MCP, inspect available tools first. Online search found several A-share-capable MCP options:

- `firmmaple/a-share-mcp-server` (https://github.com/firmmaple/a-share-mcp-server): A-share basics, historical data, financials, macro data.
- `zwldarren/akshare-one-mcp` (https://github.com/zwldarren/akshare-one-mcp): China stock historical data, real-time data, news, financial statements.
- `stockmcp/stock-data-mcp` (https://github.com/stockmcp/stock-data-mcp): A-shares, HK, US, crypto, with multi-source failover.
- AKShare MCP variants: broad Chinese financial market APIs.

Treat MCP output as data, not as final analysis. Still apply the prompt pack.

## Output Requirements

Always include:

- 标的信息：名称、代码、交易所、规范化 ticker、分析日期或数据日期。
- 数据可得性：哪些数据已查到，哪些缺失。
- 市场结构：趋势、成交、换手、涨跌停/ST/停牌风险。
- 基本面：盈利、现金流、资产负债、估值、分红/回购、财报风险。
- 新闻公告：政策、行业、公司公告、交易所问询或监管风险。
- 情绪资金：股吧/雪球/新闻热度、北向资金、融资融券、龙虎榜；无数据则写明。
- 看多/看空辩论。
- 交易计划：Buy/Hold/Sell、入场条件、仓位、止损、观察触发器。
- 风险清单。
- 最终评级：Buy / Overweight / Hold / Underweight / Sell，并给中文解释。

Avoid:

- Inventing live prices, financial figures, announcements, or flows.
- Applying US-specific StockTwits/Reddit sentiment assumptions to A-shares.
- Treating a name match as final when multiple candidates exist.
- Installing or running third-party MCP servers without explicit user approval.
