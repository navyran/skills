---
name: save-concept-events
description: Use when saving stock concept events, research catalysts, theme events, or when the user provides a concept/theme name and stock list to save into the stock concept library.
---

# Save Concept Events

## Core Rule

First decide the mode, then call exactly one matching API. Do not call both APIs unless the user explicitly asks to save both events and a separate stock list.

## Quick Start

Save concept events with industry and concept information:

```bash
node scripts/save-concept.js "金盘科技\n数据中心领域大幅增长\n\n拓普集团\n机器人、液冷蓄势待发" "科技行业" "AI概念"
```

Save only concept stocks when the user provides a concept name and stock list:

```bash
node scripts/save-concept.js stocks "AI应用" "寒武纪,中科曙光,海光信息"
```

## When to Use

- Use event mode when the input has `股票名称 + 事件描述`, plus `industry_in` and `concept_in`.
- Use stock-only mode when the input only has `题材名/概念名 + 股票列表`.
- Do not invent event descriptions or industry names for stock-only requests.

## Routing Rules

| User intent or input shape | Mode | API function |
|---|---|---|
| "只保存题材股票", "保存到题材库", "概念名 + 股票列表", "题材名 + 股票列表" | `stocks` | `save_stock_to_concept_db` |
| Plain stock names separated by comma, Chinese comma, spaces, or newlines, plus one concept/theme name | `stocks` | `save_stock_to_concept_db` |
| "题材事件", "研报事件", "催化", "逻辑", "原因", with stock names and event descriptions | `events` | `parse_txt_and_save_event_and_save_concept` |
| User explicitly says `stocks 模式` | `stocks` | `save_stock_to_concept_db` |
| User explicitly says `events 模式` | `events` | `parse_txt_and_save_event_and_save_concept` |

## Ambiguity Rules

- If there is no event description text, choose `stocks`.
- If there are event descriptions but `industry_in` or `concept_in` is missing, ask for the missing field instead of guessing.
- If the user provides both a stock list and event descriptions, choose `events` unless they explicitly say "只保存股票列表" or `stocks 模式`.
- Never convert a plain stock list into fake event text.
- Never invent an industry, concept, catalyst, or reason to make the event API fit.
- Normalize stock-only lists into English-comma `namestr`, preserving stock names and removing duplicates.

## Event API Details

**Endpoint**: `https://pi.navyran.top:3001/devops/module_func`  
**Method**: POST  
**Authentication**: None required

**Request Format**:
```json
{
  "module": "mystock",
  "func_name": "parse_txt_and_save_event_and_save_concept",
  "func_kwargs_json": {
    "txt": "股票名称1\n事件描述1\n\n股票名称2\n事件描述2",
    "industry_in": "科技行业",
    "concept_in": "人工智能概念"
  }
}
```

**Parameters**:
- `txt`: Stock event text in format "股票名称\n事件描述\n\n股票名称2\n事件描述2"
- `industry_in`: Industry classification (e.g., "科技行业", "汽车行业")
- `concept_in`: Concept category (e.g., "AI概念", "新能源汽车")

## Stock-Only API Details

**Endpoint**: `https://pi.navyran.top:3001/devops/module_func`  
**Method**: POST  
**Authentication**: None required

**Request Format**:
```json
{
  "module": "mystock",
  "func_name": "save_stock_to_concept_db",
  "func_kwargs_json": {
    "concept": "AI应用",
    "namestr": "寒武纪,中科曙光,海光信息"
  }
}
```

**Parameters**:
- `concept`: Concept name saved to the stock concept library.
- `namestr`: Stock names separated by English commas.

This mode saves the provided list to the concept. Use it when the task is only to save concept stocks, not event descriptions.

## Usage Examples

### Example 1: Save single stock event
```bash
node scripts/save-concept.js "金盘科技\n数据中心领域大幅增长" "科技行业" "数据中心概念"
```

### Example 2: Save multiple stock events
```bash
node scripts/save-concept.js "金盘科技\n数据中心领域大幅增长\n\n拓普集团\n机器人、液冷蓄势待发" "科技行业" "AI概念"
```

### Example 3: From email summary
```bash
node scripts/save-concept.js "金盘科技\n业绩基本符合预期，数据中心领域大幅增长\n\n拓普集团\n2025年业绩符合预期，机器人、液冷蓄势待发" "汽车行业" "新能源汽车"
```

### Example 4: Save concept stocks only
```bash
node scripts/save-concept.js stocks "AI应用" "寒武纪,中科曙光,海光信息"
```

### Example 5: Save concept stocks from a newline list
```bash
node scripts/save-concept.js stocks "液冷服务器" "英维克
高澜股份
申菱环境"
```

## Script Reference

See `scripts/save-concept.js` for the complete implementation with error handling and logging.

## Auto-Generated K-Line Link

After successfully saving concept events, the script automatically generates a K-line chart link.
After successfully saving concept stocks, it generates the same K-line chart link from the provided stock list.

**Output Format:**
```
✅ Concept events saved successfully!

📊 股票数量：X 只
📈 K 线筹码链接：https://pi.navyran.top:8501/?page=K%E7%BA%BF%E7%AD%B9%E7%A0%81&namestr=...
```

**Link Details:**
- Base URL: `https://pi.navyran.top:8501/`
- Parameters (URL-encoded):
  - `page`: K 线筹码
  - `namestr`: Comma-separated stock names (English commas, no spaces)
- Stock names are automatically extracted from the event text or the provided stock list
