# Save Concept Events Skill

这个skill用于保存题材事件和概念股信息到数据库，也支持只保存题材股票列表。

## 功能

- 调用 `parse_txt_and_save_event_and_save_concept` API，将股票事件描述与行业分类和概念分类一起保存到数据库。
- 调用 `save_stock_to_concept_db` API，根据题材名/概念名和股票列表保存股票题材库。

## 使用方法

### 命令行方式

```bash
node scripts/save-concept.js <txt> <industry_in> <concept_in>
node scripts/save-concept.js events <txt> <industry_in> <concept_in>
node scripts/save-concept.js stocks <concept> <stock_names>
```

**参数说明**：
- `txt`: 股票事件文本，格式为 "股票名称\n事件描述\n\n股票名称2\n事件描述2"
- `industry_in`: 行业分类（如："科技行业"、"汽车行业"）
- `concept_in`: 概念分类（如："AI概念"、"新能源汽车"）
- `concept`: 题材名/概念名
- `stock_names`: 股票列表，支持英文逗号、中文逗号、空格或换行分隔

**示例**：
```bash
node scripts/save-concept.js "金盘科技\n数据中心领域大幅增长" "科技行业" "AI概念"
node scripts/save-concept.js stocks "AI应用" "寒武纪,中科曙光,海光信息"
```

### 在对话中使用

当用户想要保存股票概念事件时，使用这个skill。例如：

**用户**：帮我保存一下今天的研报事件
**助手**：我来帮你调用接口保存这些概念事件...

当用户只提供题材名和股票列表时，使用 `stocks` 模式，不要补造事件描述或行业分类。

## API接口

- **地址**: https://pi.navyran.top:3001/devops/module_func
- **方法**: POST
- **认证**: 无需认证

**请求格式**：
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

只保存题材股票时：
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

## 输出格式

成功时返回：
```json
null
```

## 文件结构

```
save-concept-events/
├── SKILL.md              # Skill定义文档
├── README.md             # 使用说明
└── scripts/
    └── save-concept.js   # 调用接口的脚本
```

## 注意事项

- 文本格式必须严格遵循 "股票名称\n事件描述" 的格式
- 多个股票事件之间用双换行符 `\n\n` 分隔
- 行业和概念分类建议使用标准化的行业/概念名称
- 只保存题材股票时，使用 `stocks` 模式，并提供题材名和股票列表即可
